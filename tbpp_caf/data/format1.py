import glob
import os
import numpy as np
from ..instance import Instance

__all__ = ['read', 'read_all']


def read(filename):
    raw = np.loadtxt(filename, dtype=int)
    cap = raw[0, 1]
    s = raw[1:, 1].tolist()
    e = raw[1:, 2].tolist()
    c = raw[1:, 3].tolist()
    inst = Instance(s=s, e=e, c=c, cap=cap)
    inst.name = os.path.splitext(os.path.basename(filename))[0]
    return inst


def read_all(data_dir):
    groups = []
    for group_path in sorted(glob.glob(os.path.join(data_dir, '*'))):
        group_name = os.path.basename(group_path)
        tmp = group_name.split(' ')
        filenames = sorted(glob.glob(os.path.join(group_path, '*.txt')))
        group = dict(
            name=group_name,
            n=int(tmp[0][1:]),
            t=int(tmp[1][1:]),
            cls=tmp[2],
            instances=(read(filename) for filename in filenames),
        )
        groups.append(group)
    return groups
