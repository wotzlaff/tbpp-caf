import typing

import itikz
from .utils import pairwise, get_cliques
from .instance import Instance

__all__ = ['visualize']


class Args(typing.NamedTuple):
    temp_dir: bool


def key_set(n):
    return sum(2**i for i in n)


def patterns(inst):
    yield frozenset()
    active = [(0, frozenset())]

    for i, ci in enumerate(inst.c):
        to_add = []

        for c, subset in active:
            new_c = c + ci
            if new_c > inst.cap:
                continue
            new_subset = subset | {i}
            if new_c == inst.cap:
                yield new_subset
            else:
                to_add.append((new_c, new_subset))
                yield new_subset
        active += to_add


def format_jobs(n):
    if not n:
        return '\\emptyset'
    return '\\{' + ','.join(str(j + 1) for j in sorted(n)) + '\\}'


def tag_jobs(n):
    return 'u'.join(str(j + 1) for j in sorted(n))


def tex_template(s): return (
    r'''\documentclass[tikz]{standalone}
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}[
  yscale=0.65,
  xscale=1.3,
  act/.style={rectangle,fill=white,rounded corners=0,draw=black!60,inner sep=0,minimum height=20,minimum width=40,scale=0.8,},%
  nac/.style={act,white,draw=black!60,fill=black!60},%
  c/.style={rectangle,fill=white,draw=black!60,inner sep=0,minimum height=20,minimum width=28,rounded corners=6,scale=0.8,},%
  arc/.style={thick},%
  aarc/.style={arc,densely dotted},%
  darc/.style={out=0, in=180, looseness=0.15},%
  bg/.style={draw=none, fill=blue!60!black!10},%
]
'''
    + s
    + r'''
\end{tikzpicture}
\end{document}
'''
)


def visualize(
    inst: Instance,
    enumerate_all: bool = False,
    use_active: bool = False,
    get_tex: bool = False,
):
    pats = sorted(patterns(inst), key=key_set)
    cliques = [set()] + get_cliques(inst.s, inst.e) + [set()]
    pats_pc = [{frozenset(c) & p for p in pats} for c in cliques]
    max_len = max(len(p) for p in pats_pc)

    height = len(pats) if enumerate_all else max_len
    offset = -1.9 if use_active else -1.3

    # nodes
    s = ''

    for k, (c0, c1) in enumerate(pairwise(cliques)):
        cinter = frozenset(c0 & c1)
        pinter = sorted({cinter & p for p in pats}, key=key_set)

        s += f'\\begin{{scope}}[xshift={50+100*k}]\n'
        if k > 0:
            s += f'\\draw[bg] (-2.4, {offset}) rectangle (0.4, {height-0.5});\n'
            s += f'\\node at (-1, -0.9) {{$C_{k} = {format_jobs(c0)}$}};\n'

            s_min = min((inst.s[i] for i in c0 - cliques[k - 1]), default=None)
            if use_active and s_min is not None:
                s += f'\\node [anchor=west] at (-2.4, -1.5) {{$s^{k} = {s_min}$}};\n'

        for pos, p in enumerate(pinter):
            if not enumerate_all:
                pos = pats.index(p)
            s += f'\\node [c] (c{k}_{tag_jobs(p)}) at (0, {pos}) {{${format_jobs(p)}$}};\n'

        if use_active:
            # activity
            e_max = max((inst.e[i] for i in c0 - c1), default=None)
            s_min = min((inst.s[i] for i in c1 - c0), default=None)
            if e_max is not None:
                s += f'\\node [anchor=east] at (0.4, -1.5) {{$e^{k} = {e_max}$}};\n'
            if e_max == s_min:
                s += f'\\node [c] (c{k}_a) at (0, {height}) {{$A$}};\n'

        s += '\\end{scope}\n'

    # arcs
    for k, c in enumerate(cliques[1:-1], start=1):
        cinter = frozenset(c)
        pinter = pats if enumerate_all else sorted(
            {cinter & p for p in pats}, key=key_set
        )

        s += f'\\begin{{scope}}[xshift={100*k}]\n'
        for pos, p in enumerate(pinter):
            tag = 'act' if p == p & c else 'nac'
            s += f'\\node [{tag}] ({k}_{tag_jobs(p)}) at (0, {pos}) {{${format_jobs(p)}$}};\n'
        s += '\\end{scope}\n'

    # connections
    for k, c in enumerate(cliques[1:-1], start=1):
        cinter = frozenset(c)
        pinter = sorted({cinter & p for p in pats}, key=key_set)

        e_max = max((inst.e[i] for i in cliques[k - 1] - c), default=None)
        s_min = min((inst.s[i] for i in cliques[k + 1] - c), default=None)

        for p in pinter:
            p_head = p & cliques[k - 1]
            s += f'\\draw[arc] (c{k-1}_{tag_jobs(p_head)}.east) to[darc] ({k}_{tag_jobs(p)}.west);\n'
            p_tail = p & cliques[k + 1]
            s += f'\\draw[-stealth,arc] ({k}_{tag_jobs(p)}.east) to[darc] (c{k}_{tag_jobs(p_tail)}.west);\n'

            if use_active:
                if e_max is not None and min((inst.s[j] for j in p), default=None) == e_max:
                    s += f'\\draw[aarc] (c{k-1}_a.east) to[darc] ({k}_{tag_jobs(p)}.west);\n'
                if s_min is not None and max((inst.e[j] for j in p), default=None) == s_min:
                    s += f'\\draw[-stealth,aarc] ({k}_{tag_jobs(p)}.east) to[darc] (c{k}_a.west);\n'

    tex = tex_template(s)
    if get_tex:
        return tex
    return itikz.fetch_or_compile_svg(tex, working_dir=itikz.get_cwd(Args(True)))
