import gurobipy as gp

from .instance import Instance, Allocation
from .graph import Graph, generate_graph
from .start import set_start


__all__ = ['build', 'extract_solution']


def build_from_graph(inst: Instance, graph: Graph):
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
    model._update_gamma = _update_gamma
    _update_gamma(0.0)

    def _add_lb_servers(lb):
        if model._gamma == 0.0:
            model.addConstr(servers >= lb, name='lb_servers')
        else:
            fireups = gp.quicksum(x[arc] for arc in graph.fu_arcs)
            model.addConstr(servers >= lb, name='lb_servers')
            model.addConstr(fireups >= lb, name='lb_fireups')
    model._add_lb_servers = _add_lb_servers

    def _set_start(pats: Allocation):
        model.update()
        set_start(model, pats)
    model._set_start = _set_start

    return model


def build(inst: Instance):
    graph = generate_graph(inst)
    return build_from_graph(inst, graph)
