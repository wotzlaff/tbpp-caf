import gurobipy as gp
from .graph import Node

__all__ = ['extract']


def extract(
    model: gp.Model,
    tol: float = 1e-6,
    as_arcs: bool = False,
    with_vals: bool = False
):
    arcs = model._graph.arcs
    vals = {
        arc: val
        for arc in arcs
        if (val := model._x[arc].x) > tol
    }
    paths = []
    # reset to start from source node
    u = Node(0, frozenset(), 'O')
    path = []
    minval = float('inf')
    while True:
        # find connected arc with maximal flow
        res = max((
            (val, arc)
            for arc, val in vals.items()
            if arc[1] == u and val > tol
        ), default=None)
        if res is None:
            if len(path) == 0:
                break
            paths.append((minval, path))
            for arc in path:
                vals[arc] -= minval
            u = Node(0, frozenset(), 'O')
            path = []
            minval = float('inf')
            continue
        val1, arc1 = res
        minval = min(minval, val1)
        path.append(arc1)
        u = arc1[2]
    if as_arcs:
        if with_vals:
            return paths
        else:
            return [path for _, path in paths]
    else:
        if with_vals:
            return [
                (val, {i for arc in path for i in arc[0].state})
                for val, path in paths
            ]
        else:
            return [
                {i for arc in path for i in arc[0].state}
                for val, path in paths
            ]
