import math
import time
import gurobipy as gp
import tbpp_caf

__all__ = ['solve', 'format_result', 'format_header']


def format_header():
    return ','.join([
        'name',
        'v', 'servers', 'fireups',
        'nv', 'nc', 'nnz',
        'time_model', 'time_bound', 'time_solve', 'time_extract',
    ])


def format_result(res):
    return ','.join([
        f'{res["name"]}',
        f'{res["v"]},{res["servers"]},{res["fireups"]}',
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

    # compute server bound
    model_relaxed = model.relax()
    model_relaxed.optimize()
    if model_relaxed.Status != gp.GRB.OPTIMAL:
        return
    lb_servers = math.ceil(model_relaxed.ObjVal - 1e-6)
    ts.append(time.time())

    # solve integer model
    model._update_gamma(1.0)
    model._add_lb_servers(lb_servers)
    model.optimize()
    if model.Status != gp.GRB.OPTIMAL:
        return
    v = round(model.ObjVal)
    servers = round(model._servers.getValue())
    if hasattr(model, '_fireups'):
        fireups = round(model._fireups.getValue())
    else:
        fireups = 0
    ts.append(time.time())

    # extract solution
    sol = tbpp_caf.extract(model)
    assert len(sol) == servers
    ts.append(time.time())

    return dict(
        name=inst.name,
        v=v, servers=servers, fireups=fireups,
        nv=model.NumVars, nc=model.NumConstrs, nnz=model.NumNZs,
        sol=sol,
        times=[t1 - t0 for t0, t1 in zip(ts, ts[1:])],
    )
