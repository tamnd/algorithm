# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-strassen/. The authors are listed in prov/B0S9SD.jsonl.

"""Fork-join Strassen multiplication, run sequentially with work and span counters.

Cost model: an add, a subtract or a product of two entries costs 1. A group of k parallel
tasks (a spawn group, or a parallel loop over k items) adds k - 1 to the work and ceil(lg k)
to the span. Taking a block of a matrix is index arithmetic and costs nothing.
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
    k = len(costs)
    return Cost(sum(c.work for c in costs) + k - 1, ceil_lg(k) + max(c.span for c in costs))


def seq(*costs: Cost) -> Cost:
    return Cost(sum(c.work for c in costs), sum(c.span for c in costs))


def loops_cost(m: int, ops: int) -> Cost:
    """Two nested parallel loops over an m x m block with a body of `ops` unit steps."""
    row = par([Cost(ops, ops)] * m)
    return par([row] * m)


def block(x: Matrix, i: int, j: int, h: int) -> Matrix:
    return [row[j * h : (j + 1) * h] for row in x[i * h : (i + 1) * h]]


def combine(signs: list[int], *ms: Matrix) -> tuple[Matrix, Cost]:
    """Entry by entry, the sum of signs[t] * ms[t]; costs len(ms) - 1 unit steps per entry."""
    m = len(ms[0])
    out = [[sum(s * x[i][j] for s, x in zip(signs, ms)) for j in range(m)] for i in range(m)]
    return out, loops_cost(m, len(ms) - 1)


def strassen(a: Matrix, b: Matrix) -> tuple[Matrix, Cost]:
    """Return (A B, cost) for n x n matrices with n a power of 2."""
    n = len(a)  # @line L1
    if n == 1:  # @line L2
        return [[a[0][0] * b[0][0]]], Cost(1, 1)
    h = n // 2  # @line L3
    a11, a12, a21, a22 = block(a, 0, 0, h), block(a, 0, 1, h), block(a, 1, 0, h), block(a, 1, 1, h)
    b11, b12, b21, b22 = block(b, 0, 0, h), block(b, 0, 1, h), block(b, 1, 0, h), block(b, 1, 1, h)
    sums = [  # @line L4: ten independent sums of blocks
        combine([1, -1], b12, b22),  # S1
        combine([1, 1], a11, a12),  # S2
        combine([1, 1], a21, a22),  # S3
        combine([1, -1], b21, b11),  # S4
        combine([1, 1], a11, a22),  # S5
        combine([1, 1], b11, b22),  # S6
        combine([1, -1], a12, a22),  # S7
        combine([1, 1], b21, b22),  # S8
        combine([1, -1], a11, a21),  # S9
        combine([1, 1], b11, b12),  # S10
    ]
    s = [m for m, _ in sums]
    products = [  # @line L5: seven independent products
        strassen(a11, s[0]),  # P1 = A11 S1
        strassen(s[1], b22),  # P2 = S2 B22
        strassen(s[2], b11),  # P3 = S3 B11
        strassen(a22, s[3]),  # P4 = A22 S4
        strassen(s[4], s[5]),  # P5 = S5 S6
        strassen(s[6], s[7]),  # P6 = S7 S8
        strassen(s[8], s[9]),  # P7 = S9 S10
    ]
    p = [m for m, _ in products]  # @line L6: sync
    blocks = [  # @line L7: four independent blocks of C
        combine([1, 1, -1, 1], p[4], p[3], p[1], p[5]),  # C11 = P5 + P4 - P2 + P6
        combine([1, 1], p[0], p[1]),  # C12 = P1 + P2
        combine([1, 1], p[2], p[3]),  # C21 = P3 + P4
        combine([1, 1, -1, -1], p[4], p[0], p[2], p[6]),  # C22 = P5 + P1 - P3 - P7
    ]
    (c11, _), (c12, _), (c21, _), (c22, _) = blocks
    c = [r1 + r2 for r1, r2 in zip(c11, c12)] + [r1 + r2 for r1, r2 in zip(c21, c22)]  # @line L8
    cost = seq(par([k for _, k in sums]), par([k for _, k in products]), par([k for _, k in blocks]))
    return c, cost
