from typing import Collection
import gurobipy as gp
from .instance import Instance, Pattern
from . import heuristic


def _solve_pricing(inst: Instance, prices: list[float]):
    min_val = 1.0 + 1e-6
    model = gp.Model()
    x = model.addVars(inst.n, vtype=gp.GRB.BINARY, obj=prices)
    model.ModelSense = gp.GRB.MAXIMIZE
    model.setParam('OutputFlag', 0)
    model.setParam('Cutoff', min_val)
    model.setParam('PoolGap', 0.5)
    model.setParam('PoolSolutions', 50)

    # add capacity constraints
    mcs = inst.cliques
    model.addConstrs(
        gp.quicksum(inst.c[i] * x[i] for i in mcs[idx]) <= inst.cap
        for idx in range(len(mcs))
    )

    # add fireup handling
    if inst.gamma != 0.0:
        times = sorted(set(inst.s) | set(inst.e))
        prev_time = {t1: t0 for t0, t1 in zip(times, times[1:])}
        times_s = sorted(set(inst.s))
        active = {
            t: {
                i
                for i in range(inst.n)
                if inst.s[i] <= t and t < inst.e[i]
            }
            for t in times
        }
        y = model.addVars(
            times[:-1],
            vtype=gp.GRB.BINARY,
            name='y',
        )
        model.addConstrs(
            gp.quicksum(x[i] for i in active[t]) >= y[t]
            for t in times[:-1]
        )
        model.addConstrs(
            gp.quicksum(x[i] for i in active[t]) <= len(active[t]) * y[t]
            for t in times[:-1]
        )

        w = model.addVars(
            times_s,
            vtype=gp.GRB.BINARY,
            name='w',
            obj=-inst.gamma,
        )
        model.addConstrs(
            y[t] - (y[prev_time[t]] if t in prev_time else 0) <= w[t]
            for t in times_s
        )

    model.optimize()
    if model.Status == gp.GRB.Status.CUTOFF:
        return set[Pattern]()
    assert model.Status == gp.GRB.Status.OPTIMAL

    # extract solution(s)
    pats = set[Pattern]()
    for idx_sol in range(model.SolCount):
        model.setParam('SolutionNumber', idx_sol)
        val = model.PoolObjVal
        if val < min_val:
            break
        pat = frozenset({i for i in range(inst.n) if x[i].Xn > 0.5})
        if pat in pats:
            continue
        pats.add(pat)
    return pats


def solve(inst: Instance):
    rmp = gp.Model()
    rmp.setParam('OutputFlag', 0)
    con = rmp.addConstrs(
        gp.LinExpr() == 1
        for i in range(inst.n)
    )
    vars = []
    patterns = []

    def _add_patterns(patterns_new: Collection[Pattern]):
        for pattern in patterns_new:
            assert pattern not in patterns
            patterns.append(pattern)
            var = rmp.addVar(column=gp.Column(
                coeffs=[1] * len(pattern),
                constrs=[con[i] for i in pattern],
            ), obj=inst.compute_value([pattern]))
            vars.append(var)

    # use heuristic to find initial patterns
    patterns_init = heuristic.look_ahead(inst)
    _add_patterns(patterns_init)

    # start column generation
    while True:
        rmp.optimize()
        prices = [con[i].Pi for i in range(inst.n)]
        patterns_new = _solve_pricing(inst, prices)
        if not patterns_new:
            break
        _add_patterns(patterns_new)

    return dict(
        value=rmp.ObjVal,
        patterns=patterns,
        solution={
            pattern: xpval
            for pattern, xp in zip(patterns, vars)
            if (xpval := xp.X) > 1e-6
        },
    )
