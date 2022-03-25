from itertools import tee

__all__ = ['get_cliques', 'iterate_feasible_subsets', 'pairwise']


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def get_cliques(s: list[int], e: list[int]):
    n = len(s)
    tss = set(s)
    tes = set(e)
    ts = sorted(tss | tes)
    ndts = [
        t0
        for t0, t1 in pairwise(ts)
        if t0 in tss and t1 in tes
    ]
    return [
        {i for i in range(n) if s[i] <= t and t < e[i]}
        for t in ndts
    ]


def iterate_feasible_subsets(cs: list[int], subset: set[int], rem_cap: int, with_cap: bool = False):
    sets: list[tuple[float, set[int]]] = [(0, set())]
    for i in subset:
        new_sets: list[tuple[float, set[int]]] = []
        for c, s in sets:
            cn = c + cs[i]
            if cn > rem_cap:
                continue
            new_sets.append((cn, s | {i}))
        sets += new_sets
    if with_cap:
        return sets
    return [s for c, s in sets]
