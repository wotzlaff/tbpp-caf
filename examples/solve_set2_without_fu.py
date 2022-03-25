import os
import tbpp_caf
import without_fu
from utils import format_solution


def main():
    log_dir = './logs/set2_nofu'
    os.makedirs(log_dir, exist_ok=True)
    taus = range(10, 200+1, 10)
    data = tbpp_caf.data.format2.read_all('./data/set2', taus)
    for group in data:
        print(group['tau'])
        csv_path = os.path.join(log_dir, f'{group["tau"]}.csv')
        sol_path = os.path.join(log_dir, f'{group["tau"]}.sol')
        with open(csv_path, 'w') as fh_csv, open(sol_path, 'w') as fh_sol:
            fh_csv.write(without_fu.format_header() + '\n')
            for inst in group['instances']:
                res = without_fu.solve(inst)
                fh_csv.write(without_fu.format_result(res) + '\n')
                fh_sol.write(f'{inst.name}:' + format_solution(res['sol']))


if __name__ == '__main__':
    main()
