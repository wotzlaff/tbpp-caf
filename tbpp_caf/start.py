import gurobipy as gp
from .instance import Allocation


def set_start(model: gp.Model, pats: Allocation):
    inst = model._inst
    assert inst.is_feasible(pats)
    x = model._x
    mcs = inst.cliques
    for arc in x:
        state, u, v = arc
        x[arc].Start = sum(
            1 if (state.state == mcs[u.k] & pat) else 0
            for pat in pats
        )
