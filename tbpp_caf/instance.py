import dataclasses
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
    gamma: float

    @property
    def n(self) -> int:
        return len(self.s)

    def sorted(self):
        s, e, c = [list(t) for t in zip(*sorted(zip(self.s, self.e, self.c)))]
        return Instance(s, e, c, self.cap, self.gamma)

    def is_feasible(self, alloc: Allocation):
        for pat in alloc:
            for j in pat:
                load = sum(self.c[i] for i in pat if self.s[i]
                           <= self.s[j] and self.e[i] > self.s[j])
                if load > self.cap:
                    return False
        at_most_once = sum(len(pat) for pat in alloc) == self.n
        at_least_once = all(
            any(i in pat for pat in alloc)
            for i in range(self.n)
        )
        return at_most_once and at_least_once

    def compute_value(self, alloc: Allocation) -> float:
        fireups = 0
        for pat in alloc:
            last_e = float('-inf')
            for j in sorted(pat):
                if self.s[j] > last_e:
                    fireups += 1
                last_e = max(last_e, self.e[j])
        servers = len(alloc)
        return servers + self.gamma * fireups
