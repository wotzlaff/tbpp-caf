import os
import sys

import caf
import caf_fu
import caf_relax
import colgen
import colgen_ip

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

methods = {
    'caf': lambda gamma_key: caf if gamma_key == '0' else caf_fu,
    'caf_relax': lambda gamma_key: caf_relax,
    'colgen': lambda gamma_key: colgen,
    'colgen_ip': lambda gamma_key: colgen_ip,
}

gammas = {
    '0': lambda inst: 0,
    '1': lambda inst: 1,
}


def main():
    if len(sys.argv) != 4:
        raise ValueError('expected three args: bench_set, method, gamma')
    bench_set = sys.argv[1]
    if bench_set not in ['a1', 'a2', 'b1', 'b2']:
        raise ValueError('first arg should be in ["a1", "a2", "b1", "b2"]')
    method_key = sys.argv[2]
    if method_key not in methods.keys():
        raise ValueError('second arg should be in ' + str(methods.keys()))
    method_fun = methods[method_key]
    gamma_key = sys.argv[3]
    if gamma_key not in gammas.keys():
        raise ValueError('third arg should be in ' + str(gammas.keys()))
    gamma_fun = gammas[gamma_key]

    log_dir = f'./logs/set_{bench_set}_{method_key}_{gamma_key}'
    os.makedirs(log_dir, exist_ok=True)
    data = read_benchmarks(f'./data/{bench_set}')
    data.sort(key=sort_groups[bench_set[0]])
    for group in data:
        print(group['name'])
        csv_path = os.path.join(log_dir, group['name'] + '.csv')
        sol_path = os.path.join(log_dir, group['name'] + '.sol')
        with open(csv_path, 'w') as fh_csv, open(sol_path, 'w') as fh_sol:
            method = method_fun(gamma_key)
            fh_csv.write(method.format_header() + '\n')
            for inst in sorted(group['instances'], key=sort_instances[bench_set[0]]):
                inst.gamma = gamma_fun(inst)
                res = method.solve(inst)
                fh_csv.write(method.format_result(res) + '\n')
                fh_csv.flush()
                fh_sol.write(f'{inst.name}:' + format_solution(res['sol']))
                fh_sol.flush()


if __name__ == '__main__':
    main()
