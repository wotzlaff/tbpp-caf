import dataclasses
import os
from typing import Collection
from .utils import get_cliques

__all__ = ['Instance']


Pattern = frozenset[int]
Allocation = Collection[Pattern]


@dataclasses.dataclass
class Instance:
    s: list[int]
    e: list[int]
    c: list[int]
    cap: int

    @property
    def n(self) -> int:
        return len(self.s)
    
    @property
    def cliques(self) -> list[set[int]]:
        return get_cliques(self.s, self.e)

    def sorted(self):
        s, e, c = [list(t) for t in zip(*sorted(zip(self.s, self.e, self.c)))]
        return Instance(s, e, c, self.cap)

    def is_feasible(self, alloc: Allocation, verbose=False):
        for idx, pat in enumerate(alloc):
            for j in pat:
                load = sum(
                    self.c[i]
                    for i in pat
                    if self.s[i] <= self.s[j] and self.e[i] > self.s[j]
                )
                if load > self.cap:
                    if verbose:
                        print(f'capacity at {idx} violated: {load} > {self.cap}')
                    return False
        # check double packing
        items_set = set(range(self.n))
        at_most_once = True
        for pat in alloc:
            not_there = pat - items_set
            if not_there:
                at_most_once = False
                if verbose:
                    print(f'items {not_there} packed more than once')
                return False
            items_set -= pat
        # check actual packing
        at_least_once = not items_set
        if verbose and not at_least_once:
            print(f'items {items_set} not packed')
        return at_most_once and at_least_once

    def compute_value(self, alloc: Allocation):
        return len(alloc)

    @staticmethod
    def from_file(filename):
        with open(filename) as fh:
            lines = fh.readlines()
            n, cap = (int(v) for v in lines[0].split()[:2])
            s, e, c = [], [], []
            for i in range(n):
                _, si, ei, ci = (int(v) for v in lines[i+1].split())
                s.append(si)
                e.append(ei)
                c.append(ci)
            inst = Instance(s=s, e=e, c=c, cap=cap)
            inst.name = os.path.splitext(os.path.basename(filename))[0]
            return inst
