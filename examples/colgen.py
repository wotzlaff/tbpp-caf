import time
import tbpp_caf

__all__ = ['solve', 'format_result', 'format_header']


def format_header():
    return ','.join(['name', 'value', 'time', 'patterns'])


def format_result(res):
    return ','.join([res['name'], str(res['value']), str(res['time'])])


def solve(inst):
    t0 = time.time()
    cg_res = tbpp_caf.colgen.solve(inst)
    t1 = time.time()

    return dict(
        name=inst.name,
        value=cg_res['value'],
        time=t1-t0,
        sol=cg_res['patterns'],
    )
