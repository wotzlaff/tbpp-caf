import glob
import os
from ..instance import Instance

__all__ = ['read', 'read_all']


def read(filename):
    lines = open(filename).read().split('\n')
    n, cap, _ = [int(v) for v in lines[0].split('\t')]
    c = [int(ci) for ci in lines[1:][:n]]
    rem = lines[3 + n:]
    s = [-1] * n
    e = [-1] * n
    active = set()
    for t, step in enumerate(rem):
        items = set([int(v) for v in step.split('\t') if len(v) > 0])
        for item in active.copy():
            if item not in items:
                active.remove(item)
                e[item] = t
        for item in items:
            if item not in active:
                active.add(item)
                s[item] = t
    tlast = len(rem)
    for item in active:
        e[item] = tlast
    inst = Instance(s=s, e=e, c=c, cap=cap)
    inst.name = os.path.splitext(os.path.basename(filename))[0]
    return inst


def read_all(data_dir, taus):
    groups = []
    for tau in taus:
        pattern = f'I_*.txt_{tau}_100.txt'
        filenames = sorted(
            glob.glob(os.path.join(data_dir, pattern)),
            key=lambda f: int(os.path.basename(f).split('.txt')[0][2:])
        )
        group = dict(
            tau=tau,
            instances=(read(filename) for filename in filenames),
        )
        groups.append(group)
    return groups
