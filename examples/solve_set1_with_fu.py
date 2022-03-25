import os
import tbpp_caf
import with_fu
from utils import format_solution


def main():
    log_dir = './logs/set1'
    os.makedirs(log_dir, exist_ok=True)
    data = tbpp_caf.data.format1.read_all('./data/set1')
    data.sort(key=lambda d: (d['n'], d['t'], d['cls']))
    for group in data:
        print(group['name'])
        csv_path = os.path.join(log_dir, group['name'] + '.csv')
        sol_path = os.path.join(log_dir, group['name'] + '.sol')
        with open(csv_path, 'w') as fh_csv, open(sol_path, 'w') as fh_sol:
            fh_csv.write(with_fu.format_header() + '\n')
            for inst in group['instances']:
                res = with_fu.solve(inst)
                fh_csv.write(with_fu.format_result(res) + '\n')
                fh_sol.write(f'{inst.name}:' + format_solution(res['sol']))


if __name__ == '__main__':
    main()
