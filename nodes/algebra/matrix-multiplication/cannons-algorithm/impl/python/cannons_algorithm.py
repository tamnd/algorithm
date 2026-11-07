# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cannons-algorithm/. The authors are listed in prov/E9RHBT.jsonl.

from typing import NamedTuple, Optional

Matrix = list[list[int]]


class Cost(NamedTuple):
    """BSP cost of one run: supersteps S, total h-relation H, and the largest local work W."""

    supersteps: int
    h_total: int
    max_multiplications: int


def _local(c: Matrix, a: Matrix, b: Matrix, mod: Optional[int]) -> int:
    """c += a * b by the triple loop; return the number of scalar multiplications."""
    count = 0
    for i, row in enumerate(a):
        ci = c[i]
        for k, aik in enumerate(row):
            bk = b[k]
            for j in range(len(ci)):
                ci[j] += aik * bk[j]
            count += len(ci)
        if mod is not None:
            c[i] = [x % mod for x in ci]
    return count


def _block(x: Matrix, r0: int, r1: int, c0: int, c1: int) -> Matrix:
    return [row[c0:c1] for row in x[r0:r1]]


def _words(x: Matrix) -> int:
    return sum(len(row) for row in x)


def cannon_with_cost(a: Matrix, b: Matrix, q: int, p: Optional[int] = None,
                     mod: Optional[int] = None) -> tuple[Matrix, Cost]:
    """Simulate Cannon's algorithm on a q x q grid of processors; return (a * b, cost).

    a is n x m and b is m x p (lists of rows); pass p when m = 0. Each side is
    padded with zeros to a multiple of q, so processor (i, j) holds blocks of
    size ceil(n/q) x ceil(m/q) and ceil(m/q) x ceil(p/q). The ring is Z, or Z/mod Z.
    Cost: q + 1 supersteps, H = q (|A block| + |B block|) words for q >= 2,
    and n m p / q^2 multiplications per processor when q divides the sides.
    """
    if q < 1:
        raise ValueError("the grid side q must be at least 1")
    n, m = len(a), len(b)
    if p is None:
        p = len(b[0]) if m > 0 else 0
    if any(len(row) != m for row in a) or any(len(row) != p for row in b):
        raise ValueError("the shapes do not match")
    bn, bm, bp = -(-n // q), -(-m // q), -(-p // q)
    ap = [row + [0] * (bm * q - m) for row in a] + [[0] * (bm * q) for _ in range(bn * q - n)]
    bpd = [row + [0] * (bp * q - p) for row in b] + [[0] * (bp * q) for _ in range(bm * q - m)]
    grid = range(q)
    a_at = {(i, j): _block(ap, i * bn, (i + 1) * bn, j * bm, (j + 1) * bm) for i in grid for j in grid}
    b_at = {(i, j): _block(bpd, i * bm, (i + 1) * bm, j * bp, (j + 1) * bp) for i in grid for j in grid}
    c_at = {(i, j): [[0] * bp for _ in range(bn)] for i in grid for j in grid}  # @line L1

    def exchange(a_dest: dict, b_dest: dict) -> int:
        """One h-relation: move every block to its destination; return h."""
        nonlocal a_at, b_at
        sent = {key: 0 for key in a_at}
        recv = {key: 0 for key in a_at}
        new_a, new_b = {}, {}
        for src, blk in a_at.items():
            dst = a_dest[src]
            new_a[dst] = blk
            if dst != src:
                sent[src] += _words(blk)
                recv[dst] += _words(blk)
        for src, blk in b_at.items():
            dst = b_dest[src]
            new_b[dst] = blk
            if dst != src:
                sent[src] += _words(blk)
                recv[dst] += _words(blk)
        a_at, b_at = new_a, new_b
        return max(max(sent[k], recv[k]) for k in sent)

    supersteps, h_total = 1, 0
    h_total += exchange({(i, j): (i, (j - i) % q) for i in grid for j in grid},  # @line L2
                        {(i, j): ((i - j) % q, j) for i in grid for j in grid})
    work = {key: 0 for key in c_at}
    for t in range(q):  # @line L3
        supersteps += 1
        for key in c_at:  # @line L4
            work[key] += _local(c_at[key], a_at[key], b_at[key], mod)
        if t < q - 1:  # @line L5
            h_total += exchange({(i, j): (i, (j - 1) % q) for i in grid for j in grid},
                                {(i, j): ((i - 1) % q, j) for i in grid for j in grid})
    c = [[0] * p for _ in range(n)]  # @line L6
    for (i, j), blk in c_at.items():
        for r, row in enumerate(blk):
            gi = i * bn + r
            if gi < n:
                for s, x in enumerate(row):
                    gj = j * bp + s
                    if gj < p:
                        c[gi][gj] = x % mod if mod is not None else x
    return c, Cost(supersteps, h_total, max(work.values()))


def cannons_algorithm(a: Matrix, b: Matrix, q: int, p: Optional[int] = None,
                      mod: Optional[int] = None) -> Matrix:
    """Return a * b computed by Cannon's algorithm on a simulated q x q processor grid."""
    return cannon_with_cost(a, b, q, p, mod)[0]
