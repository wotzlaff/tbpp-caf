import os
import sys
import without_fu
import with_fu
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
    if len(sys.argv) != 3:
        raise ValueError('expected exactly two args')
    bench_set = sys.argv[1]
    if bench_set not in ['a1', 'a2', 'b1', 'b2']:
        raise ValueError('first arg should be in ["a1", "a2", "b1", "b2"]')
    ver = sys.argv[2]
    if ver not in ['without_fu', 'with_fu']:
        raise ValueError('second arg should be "without_fu" or "with_fu"')
    method = dict(without_fu=without_fu, with_fu=with_fu)[ver]
    log_dir = f'./logs/set_{bench_set}_{ver}'
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
                res = method.solve(inst)
                fh_csv.write(method.format_result(res) + '\n')
                fh_sol.write(f'{inst.name}:' + format_solution(res['sol']))


if __name__ == '__main__':
    main()
