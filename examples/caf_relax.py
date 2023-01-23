import time
import gurobipy as gp
import tbpp_caf

__all__ = ['solve', 'format_result', 'format_header']


def format_header():
    return ','.join([
        'name', 'v',
        'nv', 'nc', 'nnz',
        'time_model', 'time_solve', 'time_extract',
    ])


def format_result(res):
    return ','.join([
        res['name'], str(res['v']),
        str(res['nv']), str(res['nc']), str(res['nnz']),
        *(f'{t:.3f}' for t in res['times']),
    ])


def solve(inst):
    ts = []
    ts.append(time.time())

    # create model
    model = tbpp_caf.build(inst)
    model.setParam('OutputFlag', 0)
    model.setParam('Method', 3)
    model.update()
    ts.append(time.time())

    # solve integer model
    model = model.relax()
    model.optimize()
    if model.Status != gp.GRB.OPTIMAL:
        return
    v = round(model.ObjVal)
    ts.append(time.time())

    # extract solution
    sol = tbpp_caf.extract(model)
    assert len(sol) == v
    ts.append(time.time())

    return dict(
        name=inst.name,
        v=v,
        nv=model.NumVars, nc=model.NumConstrs, nnz=model.NumNZs,
        sol=sol,
        times=[t1 - t0 for t0, t1 in zip(ts, ts[1:])],
    )
