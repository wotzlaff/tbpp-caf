import os
import sys
from functools import partial
import without_fu
import with_fu
import colgen
from utils import format_solution, read_benchmarks


def _sort_groups_a(group):
    tmp = group['name'].split(' ')
    return (int(tmp[0][1:]), int(tmp[1][1:]), tmp[2])


sort_groups = dict(
    a=_sort_groups_a,
    b=lambda group: int(group['name']),
)
sort_instances = dict(
    a=lambda inst: inst.name,
    b=lambda inst: int(inst.name[2:]),
)


def main():
    if len(sys.argv) < 3:
        raise ValueError('expected three args (bench_set, method, gamma)')
    bench_set = sys.argv[1]
    if bench_set not in ['a1', 'a2', 'b1', 'b2']:
        raise ValueError('first arg should be in ["a1", "a2", "b1", "b2"]')
    ver = sys.argv[2]
    methods = dict(
        without_fu=without_fu,
        with_fu=with_fu,
        colgen=colgen,
    )
    if ver not in methods.keys():
        raise ValueError('second arg should be in ' + str(methods.keys()))
    method = methods[ver]
    gamma = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0

    log_dir = f'./logs/set_{bench_set}_{ver}_{gamma}'
    os.makedirs(log_dir, exist_ok=True)
    data = read_benchmarks(f'./data/{bench_set}')
    data.sort(key=sort_groups[bench_set[0]])
    for group in data:
        print(group['name'])
        csv_path = os.path.join(log_dir, group['name'] + '.csv')
        sol_path = os.path.join(log_dir, group['name'] + '.sol')
        with open(csv_path, 'w') as fh_csv, open(sol_path, 'w') as fh_sol:
            fh_csv.write(method.format_header() + '\n')
            for inst in sorted(group['instances'], key=sort_instances[bench_set[0]]):
                inst.gamma = gamma
                res = method.solve(inst)
                fh_csv.write(method.format_result(res) + '\n')
                fh_sol.write(f'{inst.name}:' + format_solution(res['sol']))


if __name__ == '__main__':
    main()
