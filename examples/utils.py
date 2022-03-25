__all__ = ['format_solution']


def format_solution(sol):
    return ';'.join([
        '{' + ','.join(f'{j+1}' for j in alloc) + '}'
        for alloc in sol
    ]) + '\n'
