import time
import gurobipy as gp
import tbpp_caf

__all__ = ['solve', 'format_result', 'format_header']


def format_header():
    return ','.join([
        'name', 'pb', 'db',
        'nv', 'nc', 'nnz',
        'time_model', 'time_solve', 'time_extract',
    ])


def format_result(res):
    return ','.join([
        f'{res["name"]},{res["v"]},{res["d"]}',
        f'{res["nv"]},{res["nc"]},{res["nnz"]}',
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
    model.optimize()

    if model.SolCount <= 0:
        print("No solution")
        return
    
    v = model.ObjVal
    d = model.ObjBoundC
    ts.append(time.time())

    # extract solution
    sol = tbpp_caf.extract(model)
    assert len(sol) == v
    ts.append(time.time())

    return dict(
        name=inst.name,
        v=v,
        d=d,
        nv=model.NumVars, nc=model.NumConstrs, nnz=model.NumNZs,
        sol=sol,
        times=[t1 - t0 for t0, t1 in zip(ts, ts[1:])],
    )
