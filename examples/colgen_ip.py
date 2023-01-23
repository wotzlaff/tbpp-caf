import time
import gurobipy as gp
import tbpp_caf

__all__ = ['solve', 'format_result', 'format_header']


def format_header():
    return ','.join([
        'name', 'v_cg', 'v',
        'patterns',
        'time_cg', 'time_model', 'time_ip', 'time_extract',
    ])


def format_result(res):
    return ','.join([
        res['name'],
        str(res['v_cg']),
        str(res['v']),
        str(len(res['sol'])),
        *(f'{t:.3f}' for t in res['times']),
    ])


def solve(inst):
    ts = []
    ts.append(time.time())

    cg_res = tbpp_caf.colgen.solve(inst)
    ts.append(time.time())

    model = tbpp_caf.caf.build_from_patterns(inst, cg_res['patterns'])
    model.setParam('OutputFlag', 0)
    model.setParam('Method', 3)
    model.update()
    ts.append(time.time())

    # solve integer model
    model.optimize()
    if model.Status != gp.GRB.OPTIMAL:
        return
    v = round(model.ObjVal)
    ts.append(time.time())

    sol = tbpp_caf.extract(model)
    ts.append(time.time())

    return dict(
        name=inst.name,
        v_cg=cg_res['value'],
        v=v, sol=sol,
        times=[t1 - t0 for t0, t1 in zip(ts, ts[1:])],
    )
