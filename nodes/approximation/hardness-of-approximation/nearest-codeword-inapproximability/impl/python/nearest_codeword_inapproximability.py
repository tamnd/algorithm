# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nearest-codeword-inapproximability/. The authors are listed in prov/2PHH3V.jsonl.
"""Nearest codeword as the least number of false equations mod 2, and the label cover reduction.

An NCP instance is (k, rows, rhs): rows[i] is a bit mask over k unknowns, and row i is the equation
<rows[i], x> = rhs[i] mod 2. The code is {Ax}, the received word is rhs, and the distance from rhs to
the codeword Ax is the number of false equations. For small instances only: ncp_opt tries all x.
"""

from itertools import product


def false_count(rows: list[int], rhs: list[int], x: int) -> int:
    return sum((bin(r & x).count("1") & 1) != b for r, b in zip(rows, rhs))


def ncp_opt(k: int, rows: list[int], rhs: list[int]) -> tuple[int, int]:
    """Return (least distance, an x that reaches it)."""
    return min((false_count(rows, rhs, x), x) for x in range(1 << k))


def lin_to_ncp(nvars: int, equations: list[tuple[tuple[int, ...], int]]) -> tuple[int, list[int], list[int]]:
    """Equations (variables, value) mod 2 become rows. OPT is the least number of false equations."""
    rows = [sum(1 << v for v in vs) for vs, _ in equations]
    return nvars, rows, [b for _, b in equations]


def label_cover_to_ncp(nu: int, nw: int, nl: int, nr: int, edges: list[tuple[int, int, tuple[int, ...]]]):
    """The ABSS reduction from total label cover. An edge (u, w, proj) has proj[a] = b for labels a of u.

    Unknown x[u, a] for each left vertex and label, and x[w, b] for each right vertex and label.
    Heavy equations, each repeated M times: sum over a with proj[a] = b of x[u, a] = x[w, b] for each edge
    and label b, and sum over b of x[w, b] = 1 for each right vertex. Light equations: x = 0, once each.
    Returns (k, rows, rhs, M).
    """
    def left(u, a):
        return u * nl + a

    def right(w, b):
        return nu * nl + w * nr + b

    k = nu * nl + nw * nr
    heavy = []
    for u, w, proj in edges:
        for b in range(nr):
            mask = sum(1 << left(u, a) for a in range(nl) if proj[a] == b) ^ (1 << right(w, b))
            heavy.append((mask, 0))
    for w in range(nw):
        heavy.append((sum(1 << right(w, b) for b in range(nr)), 1))
    m = k + 1
    rows = [1 << i for i in range(k)]
    rhs = [0] * k
    for mask, b in heavy:
        rows += [mask] * m
        rhs += [b] * m
    return k, rows, rhs, m


def decode(nu: int, nw: int, nl: int, nr: int, x: int) -> tuple[list[set[int]], list[set[int]]]:
    """Label sets: a is in L_u when x[u, a] = 1."""
    lu = [{a for a in range(nl) if x >> (u * nl + a) & 1} for u in range(nu)]
    lw = [{b for b in range(nr) if x >> (nu * nl + w * nr + b) & 1} for w in range(nw)]
    return lu, lw


def is_total_cover(edges, lu: list[set[int]], lw: list[set[int]]) -> bool:
    """Every edge has a in L_u and b in L_w with proj[a] = b."""
    return all(any(proj[a] in lw[w] for a in lu[u]) for u, w, proj in edges)


def min_total_cover(nu: int, nw: int, nl: int, nr: int, edges) -> int:
    best = nu * nl + nw * nr
    for bits in product((0, 1), repeat=nu * nl + nw * nr):
        x = sum(b << i for i, b in enumerate(bits))
        if sum(bits) < best and is_total_cover(edges, *decode(nu, nw, nl, nr, x)):
            best = sum(bits)
    return best
