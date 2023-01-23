from typing import Collection
from .instance import Instance

__all__ = ['look_ahead', 'best_look_ahead']

Pattern = frozenset[int]
Allocation = list[Pattern]


def best_fit_part(
    bins: list[Pattern],
    inst: Instance,
    jobs: list[int],
):
    bins = list(bins)
    for i in jobs:
        ci = inst.c[i]
        si = inst.s[i]
        bins_cap = [
            sum(inst.c[j] for j in b if inst.e[j] > si)
            for b in bins
        ]
        possible = [
            idx
            for idx, cap in enumerate(bins_cap)
            if cap + ci <= inst.cap
        ]
        if len(possible) == 0:
            bins.append(frozenset({i}))
        else:
            idx = max(possible, key=lambda idx: (bins_cap[idx], -idx))
            bins[idx] = bins[idx] | {i}
    return bins


def look_ahead_part(
    bins: list[Pattern],
    inst: Instance,
    jobs: list[int],
    recursion: int = 0,
) -> tuple[Allocation, Allocation]:
    def _compute_value(alloc: Allocation):
        return inst.compute_value(alloc)

    if len(jobs) == 0:
        return bins, bins

    # copy bins
    bins = list(bins)
    i, *rem_jobs = jobs

    ci = inst.c[i]
    si = inst.s[i]
    bins_cap = [
        sum(inst.c[j] for j in b if inst.e[j] > si)
        for b in bins
    ]
    possible = [
        idx
        for idx, cap in enumerate(bins_cap)
        if cap + ci <= inst.cap
    ]
    possible.append(len(bins))

    allocs = []
    for idx in possible:
        new_bins = list(bins)
        if idx == len(bins):
            new_bins.append(frozenset({i}))
        else:
            b = new_bins[idx]
            new_bins[idx] = b | {i}
        if recursion > 0:
            _, final_alloc = look_ahead_part(
                new_bins, inst, rem_jobs, recursion-1
            )
        else:
            final_alloc = best_fit_part(new_bins, inst, rem_jobs)
        allocs.append((new_bins, final_alloc))
    best_alloc, final_alloc = min(
        allocs, key=lambda alls: _compute_value(alls[1])
    )

    return best_alloc, final_alloc


def look_ahead(inst: Instance, future: int = 1, recursion: int = 0):
    alloc: Allocation = []
    for i in range(inst.n):
        pending_jobs = list(range(i, min(inst.n, i+1+future)))
        alloc = look_ahead_part(alloc, inst, pending_jobs, recursion)[0]
    return alloc


def best_look_ahead(inst: Instance, futures: Collection[int]):
    return min((
        look_ahead(inst, future)
        for future in futures
    ), key=lambda alloc: inst.compute_value(alloc))
