import gurobipy as gp

from .instance import Instance
from .graph import generate_graph

__all__ = ['build', 'extract_solution']


def build(inst: Instance):
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

    def _update_gamma(gamma):
        model._gamma = gamma
        if gamma == 0.0:
            obj = servers
        else:
            fireups = gp.quicksum(x[arc] for arc in graph.fu_arcs)
            model._fireups = fireups
            obj = servers + gamma * fireups
        model.setObjective(obj, gp.GRB.MINIMIZE)

    _update_gamma(0.0)
    model._update_gamma = _update_gamma

    def _add_lb_servers(lb):
        if model._gamma == 0.0:
            model.addConstr(servers >= lb, name='lb_servers')
        else:
            fireups = gp.quicksum(x[arc] for arc in graph.fu_arcs)
            model.addConstr(servers >= lb, name='lb_servers')
            model.addConstr(fireups >= lb, name='lb_fireups')

    model._add_lb_servers = _add_lb_servers

    return model
