import os
import with_fu
from utils import format_solution, read_benchmarks


def _sort_key(group):
    tmp = group['name'].split(' ')
    return (int(tmp[0][1:]), int(tmp[1][1:]), tmp[2])


def main():
    log_dir = './logs/set_a'
    os.makedirs(log_dir, exist_ok=True)
    data = read_benchmarks('./data/a')
    data.sort(key=_sort_key)
    for group in data:
        print(group['name'])
        csv_path = os.path.join(log_dir, group['name'] + '.csv')
        sol_path = os.path.join(log_dir, group['name'] + '.sol')
        with open(csv_path, 'w') as fh_csv, open(sol_path, 'w') as fh_sol:
            fh_csv.write(with_fu.format_header() + '\n')
            for inst in sorted(group['instances'], key=lambda inst: inst.name):
                res = with_fu.solve(inst)
                fh_csv.write(with_fu.format_result(res) + '\n')
                fh_sol.write(f'{inst.name}:' + format_solution(res['sol']))


if __name__ == '__main__':
    main()
