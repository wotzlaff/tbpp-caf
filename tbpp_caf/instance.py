import dataclasses
import os
from typing import Collection

__all__ = ['Instance']


Pattern = frozenset[int]
Allocation = Collection[Pattern]


@dataclasses.dataclass
class Instance:
    s: list[int]
    e: list[int]
    c: list[int]
    cap: int
    gamma: float = 0.0

    @property
    def n(self) -> int:
        return len(self.s)

    def sorted(self):
        s, e, c = [list(t) for t in zip(*sorted(zip(self.s, self.e, self.c)))]
        return Instance(s, e, c, self.cap)

    def is_feasible(self, alloc: Allocation):
        for pat in alloc:
            for j in pat:
                load = sum(
                    self.c[i]
                    for i in pat
                    if self.s[i] <= self.s[j] and self.e[i] > self.s[j]
                )
                if load > self.cap:
                    return False
        at_most_once = sum(len(pat) for pat in alloc) == self.n
        at_least_once = all(
            any(i in pat for pat in alloc)
            for i in range(self.n)
        )
        return at_most_once and at_least_once

    def compute_value(self, alloc: Allocation) -> float:
        n_servers = len(alloc)
        if self.gamma == 0.0:
            return n_servers
        n_fireups = 0
        for pat in alloc:
            last_e = float('-inf')
            for j in sorted(pat):
                if self.s[j] > last_e:
                    n_fireups += 1
                last_e = max(last_e, self.e[j])
        return n_servers + self.gamma * n_fireups

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
