import os
import without_fu
from utils import format_solution, read_benchmarks


def main():
    log_dir = './logs/set_b_nofu'
    os.makedirs(log_dir, exist_ok=True)
    data = read_benchmarks('./data/b')
    data.sort(key=lambda group: int(group['name']))
    for group in data:
        print(group['name'])
        csv_path = os.path.join(log_dir, f'{group["name"]}.csv')
        sol_path = os.path.join(log_dir, f'{group["name"]}.sol')
        with open(csv_path, 'w') as fh_csv, open(sol_path, 'w') as fh_sol:
            fh_csv.write(without_fu.format_header() + '\n')
            for inst in sorted(group['instances'], key=lambda inst: int(inst.name[2:])):
                res = without_fu.solve(inst)
                fh_csv.write(without_fu.format_result(res) + '\n')
                fh_sol.write(f'{inst.name}:' + format_solution(res['sol']))


if __name__ == '__main__':
    main()
