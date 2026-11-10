# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-matrix-multiplication/. The authors are listed in prov/QZM9BG.jsonl.

"""Three fork-join matrix products, run sequentially with work and span counters.

The cost model is the one of the page. A multiply-add step or an add costs 1. A group of
k >= 1 parallel tasks (a spawn group, or a parallel loop over k items) is a balanced binary
tree of forks: it adds k - 1 to the work and ceil(lg k) to the span, and its span is that
plus the largest span of a task. Steps in sequence add both their work and their span.
"""

from dataclasses import dataclass

Matrix = list[list[int]]


@dataclass(frozen=True)
class Cost:
    work: int
    span: int


def ceil_lg(k: int) -> int:
    return (k - 1).bit_length() if k > 1 else 0


def par(costs: list[Cost]) -> Cost:
    """The cost of running the tasks in parallel."""
    k = len(costs)
    return Cost(sum(c.work for c in costs) + k - 1, ceil_lg(k) + max(c.span for c in costs))


def seq(*costs: Cost) -> Cost:
    """The cost of running the steps one after the other."""
    return Cost(sum(c.work for c in costs), sum(c.span for c in costs))


UNIT = Cost(1, 1)


def zeros(n: int) -> Matrix:
    return [[0] * n for _ in range(n)]


def multiply_loops(a: Matrix, b: Matrix) -> tuple[Matrix, Cost]:
    """Parallel loops over i and j, a sequential loop over k."""
    n = len(a)
    c = zeros(n)
    rows = []
    for i in range(n):  # parallel for
        cells = []
        for j in range(n):  # parallel for
            s = 0
            for k in range(n):  # sequential: n steps of cost 1
                s += a[i][k] * b[k][j]
            c[i][j] = s
            cells.append(Cost(n, n))
        rows.append(par(cells))
    return c, (par(rows) if n else Cost(0, 0))


def _add_block(c: Matrix, t: Matrix, r: int, s: int, n: int) -> Cost:
    """C[r .. r + n - 1][s .. s + n - 1] += T[0 .. n - 1][0 .. n - 1] by two nested parallel loops."""
    rows = []
    for i in range(n):  # @line L8
        for j in range(n):  # @line L9
            c[r + i][s + j] += t[i][j]  # @line L10
        rows.append(par([UNIT] * n))
    return par(rows)


def _mm_temp(c: Matrix, cr: int, cs: int, a: Matrix, ar: int, as_: int, b: Matrix, br: int, bs: int, n: int) -> Cost:
    """Set the n x n block of C at (cr, cs) to the product of the blocks of A and B."""
    if n == 1:  # @line L2
        c[cr][cs] = a[ar][as_] * b[br][bs]
        return UNIT
    t = zeros(n)  # @line L3: a new matrix for the second half of the products
    h = n // 2  # @line L4
    calls = []
    for i in (0, 1):  # @line L5: C_ij <- A_i1 B_1j
        for j in (0, 1):
            calls.append(_mm_temp(c, cr + i * h, cs + j * h, a, ar + i * h, as_, b, br, bs + j * h, h))
    for i in (0, 1):  # @line L6: T_ij <- A_i2 B_2j
        for j in (0, 1):
            calls.append(_mm_temp(t, i * h, j * h, a, ar + i * h, as_ + h, b, br + h, bs + j * h, h))
    products = par(calls)  # @line L7: sync
    return seq(products, _add_block(c, t, cr, cs, n))


def multiply_temp(a: Matrix, b: Matrix) -> tuple[Matrix, Cost]:
    """Divide and conquer with a temporary matrix (CLRS 3rd edition, Section 27.2). n must be a power of 2."""
    n = len(a)  # @line L1
    c = zeros(n)
    return c, _mm_temp(c, 0, 0, a, 0, 0, b, 0, 0, n)


def _mm_add(c: Matrix, cr: int, cs: int, a: Matrix, ar: int, as_: int, b: Matrix, br: int, bs: int, n: int) -> Cost:
    """Add the product of the blocks of A and B to the n x n block of C at (cr, cs)."""
    if n == 1:
        c[cr][cs] += a[ar][as_] * b[br][bs]
        return UNIT
    h = n // 2
    phases = []
    for k in (0, 1):  # two phases with a sync between them
        calls = []
        for i in (0, 1):
            for j in (0, 1):  # four writes to four different blocks of C
                calls.append(_mm_add(c, cr + i * h, cs + j * h, a, ar + i * h, as_ + k * h, b, br + k * h, bs + j * h, h))
        phases.append(par(calls))
    return seq(*phases)


def multiply_no_temp(a: Matrix, b: Matrix) -> tuple[Matrix, Cost]:
    """Divide and conquer with no temporary matrix (CLRS 4th edition, Section 26.2). n must be a power of 2."""
    n = len(a)
    c = zeros(n)
    return c, _mm_add(c, 0, 0, a, 0, 0, b, 0, 0, n)
