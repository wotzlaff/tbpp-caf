import collections
import dataclasses
from .utils import pairwise, get_cliques, iterate_feasible_subsets
from .instance import Instance, Allocation

__all__ = ['Node', 'Arc', 'State', 'generate_graph']


@dataclasses.dataclass(frozen=True)
class Node:
    k: int
    state: frozenset[int]
    tag: str

    @property
    def name(self):
        state = ';'.join([str(j + 1) for j in sorted(self.state)])
        return f'{self.k}{self.tag}{{{state}}}'

    def __repr__(self):
        return self.name

    def _to_tuple(self):
        return (self.k, self.state, self.tag)

    def __lt__(self, other):
        return self._to_tuple() < other._to_tuple()


@dataclasses.dataclass(frozen=True)
class State:
    state: frozenset[int]

    def __repr__(self):
        return '{' + ';'.join([str(j + 1) for j in sorted(self.state)]) + '}'

    @property
    def value(self):
        return sum(2 ** i for i in self.state)

    def __lt__(self, other):
        return self.value < other.value


Arc = tuple[State, Node, Node]


@dataclasses.dataclass
class Graph:
    arcs: list[Arc]
    nodes: list[Node]
    starting_arcs: dict[int, list[Arc]]
    initial_arcs: list[Arc]
    fu_arcs: list[Arc]
    mcs: list[set[int]]


def generate_generic_graph(inst: Instance, iterate_subsets):
    mcs = get_cliques(inst.s, inst.e)

    m = len(mcs)

    mcs.insert(0, set())
    mcs.append(set())

    clique_s = {
        k: min(inst.s[i] for i in mcs[k] - mcs[k-1])
        for k in range(1, m+1)
    }
    clique_e = {
        k: max(inst.e[i] for i in mcs[k] - mcs[k+1])
        for k in range(1, m+1)
    }

    arcs: list[Arc] = list()
    nodes: list[Node] = list()
    starting_arcs: dict[int, list[Arc]] = collections.defaultdict(list)
    initial_arcs: list[Arc] = list()
    fu_arcs: list[Arc] = list()

    for k, (mc0, mc1) in enumerate(pairwise(mcs)):
        for state in iterate_subsets(mc0 & mc1):
            nodes.append(Node(k, frozenset(state), 'O'))
    for k in range(1, m):
        if clique_e[k] == clique_s[k+1]:
            nodes.append(Node(k, frozenset(), 'A'))

    for k, mc in enumerate(mcs[1:-1], start=1):
        sing = mc - mcs[k-1]

        for state in iterate_subsets(mc):
            state = frozenset(state)

            def _add_arc(k, state, tag):
                state_prev = frozenset(state & mcs[k-1])
                head = Node(
                    k-1, state_prev,
                    'O' if tag in ['o', '<-'] else 'A'
                )
                tail = Node(
                    k, frozenset(state & mcs[k+1]),
                    'O' if tag in ['o', '->'] else 'A'
                )
                arc = (State(state), head, tail)
                for i in sing & state:
                    starting_arcs[i].append(arc)
                if k == 1:
                    initial_arcs.append(arc)
                if not state_prev and state and tag in ['o', '<-']:
                    fu_arcs.append(arc)
                arcs.append(arc)

            # o-arc
            _add_arc(k, state, 'o')

            # a-arcs
            max_e = max((inst.e[i] for i in state), default=None)
            act_right = k < m and max_e == clique_s[k+1]
            if act_right:
                _add_arc(k, state, '<-')
            min_s = min((inst.s[i] for i in state), default=None)
            act_left = k > 1 and min_s == clique_e[k-1]
            if act_left:
                _add_arc(k, state, '->')

            if act_left and act_right:
                _add_arc(k, state, '<->')

    return Graph(arcs, nodes, starting_arcs, initial_arcs, fu_arcs, mcs)


def generate_pattern_graph(inst: Instance, pats: Allocation):
    return generate_generic_graph(
        inst,
        lambda ss: {pat & ss for pat in pats}
    )


def generate_graph(inst: Instance):
    return generate_generic_graph(
        inst,
        lambda ss: iterate_feasible_subsets(inst.c, ss, inst.cap)
    )
