import gurobipy as gp

from .instance import Instance
from .graph import generate_graph

__all__ = ['build', 'extract_solution']


def build(inst: Instance, lb_servers: int = 0):
    graph = generate_graph(inst)

    model = gp.Model()
    model._inst = inst
    model._graph = graph

    x = model.addVars(graph.arcs, vtype=gp.GRB.INTEGER, name='x')
    model._x = x
    model.addConstrs((
        gp.quicksum(x[arc] for arc in graph.starting_arcs[i]) == 1
        for i in range(inst.n)
    ), name='start')

    model.addConstrs((
        x.sum('*', node, '*') == x.sum('*', '*', node)
        for node in graph.nodes
        if node.k > 0 and node.k < len(graph.mcs) - 2
    ), name='fc')

    servers = gp.quicksum(x[arc] for arc in graph.initial_arcs)
    model._servers = servers

    no_fu = not hasattr(inst, 'gamma') or inst.gamma == 0.0
    if no_fu:
        obj = servers
        if lb_servers > 0:
            model.addConstr(servers >= lb_servers, name='lb_servers')
    else:
        fireups = gp.quicksum(x[arc] for arc in graph.fu_arcs)
        model._fireups = fireups
        obj = servers + inst.gamma * fireups
        if lb_servers > 0:
            model.addConstr(servers >= lb_servers, name='lb_servers')
            model.addConstr(fireups >= lb_servers, name='lb_fireups')

    model.setObjective(obj, gp.GRB.MINIMIZE)

    return model
