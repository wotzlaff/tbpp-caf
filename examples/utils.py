import glob
import os
from tbpp_caf import Instance

__all__ = ['format_solution', 'parse_solution', 'read_benchmarks']


def format_solution(sol):
    return ';'.join([
        '{' + ','.join(f'{j+1}' for j in alloc) + '}'
        for alloc in sol
    ]) + '\n'


def parse_solution(dat):
    return [
        frozenset(int(j)-1 for j in part[1:-1].split(','))
        for part in dat.split(';')
    ]


def read_benchmarks(data_dir):
    groups = []
    for group_path in sorted(glob.glob(os.path.join(data_dir, '*'))):
        group_name = os.path.basename(group_path)
        filenames = sorted(glob.glob(os.path.join(group_path, '*.txt')))
        group = dict(
            name=group_name,
            instances=(
                Instance.from_file(filename)
                for filename in filenames
            ),
        )
        groups.append(group)
    return groups
