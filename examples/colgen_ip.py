import time
import gurobipy as gp
import tbpp_caf

__all__ = ['solve', 'format_result', 'format_header']


def format_header():
    return ','.join([
        'name', 'v_cg', 'v', 'v_bound', 'patterns',
        'time_cg', 'time_model', 'time_ip', 'time_extract',
        'timeout_ip',
    ])


def format_result(res):
    return ','.join([
        res['name'],
        str(res['v_cg']),
        str(res['v']),
        str(res['v_bound']),
        str(len(res['patterns'])),
        *(f'{t:.3f}' for t in res['times']),
        '1' if res['timeout_ip'] else '0',
    ])


def solve(inst):
    ts = []
    ts.append(time.time())

    cg_res = tbpp_caf.colgen.solve(inst)
    ts.append(time.time())

    model = tbpp_caf.caf.build_from_patterns(inst, cg_res['patterns'])
    model.setParam('OutputFlag', 0)
    model.setParam('TimeLimit', 300)
    model.setParam('Method', 3)
    model.update()
    ts.append(time.time())

    # solve integer model
    model.optimize()
    if model.Status not in [gp.GRB.OPTIMAL, gp.GRB.TIME_LIMIT]:
        return
    ts.append(time.time())

    sol = tbpp_caf.extract(model)
    ts.append(time.time())

    return dict(
        name=inst.name,
        v_cg=cg_res['value'],
        patterns=cg_res['patterns'],
        v=model.ObjVal, v_bound=model.ObjBoundC,
        sol=sol,
        timeout_ip=model.Status == gp.GRB.TIME_LIMIT,
        times=[t1 - t0 for t0, t1 in zip(ts, ts[1:])],
    )
