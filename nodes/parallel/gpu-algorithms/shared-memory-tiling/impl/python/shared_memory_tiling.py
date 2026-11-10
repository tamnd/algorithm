# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shared-memory-tiling/.
"""Tiled matrix multiplication C = A B through shared memory, on a small SIMT simulator.

A block of T x T threads computes a T x T tile of C. In each phase it loads one T x T tile of A and
one of B into shared memory, waits at a barrier, multiplies the tiles, and waits again before the
next phase overwrites them. Each `yield` in a kernel is a __syncthreads(). The threads of a block
run one after another between two barriers, which is one legal schedule; a kernel that is
missing a barrier gives a wrong result under it.
"""


def ceil_div(a, b):
    return -(-a // b)


class Counter:
    def __init__(self):
        self.global_loads = 0
        self.shared_loads = 0


def _run_block(gens):
    while gens:
        live = []
        for g in gens:
            try:
                next(g)
                live.append(g)
            except StopIteration:
                pass
        gens = live


def tiled_kernel(tx, ty, bx, by, T, A, B, C, m, k, n, sh, cnt, barrier1=True, barrier2=True):
    row, col = by * T + ty, bx * T + tx
    acc = 0  # @line L1
    for p in range(ceil_div(k, T)):  # @line L2
        a_col, b_row = p * T + tx, p * T + ty
        if row < m and a_col < k:  # load one element of each tile; pad with 0 outside the matrix
            sh["A"][ty * T + tx] = A[row][a_col]  # @line L3
            cnt.global_loads += 1
        else:
            sh["A"][ty * T + tx] = 0
        if b_row < k and col < n:
            sh["B"][ty * T + tx] = B[b_row][col]
            cnt.global_loads += 1
        else:
            sh["B"][ty * T + tx] = 0
        if barrier1:
            yield  # @line L4 (the tiles are complete before anyone reads them)
        for j in range(T):
            acc += sh["A"][ty * T + j] * sh["B"][j * T + tx]  # @line L5
            cnt.shared_loads += 2
        if barrier2:
            yield  # @line L6 (everyone has finished with the tiles before they are overwritten)
    if row < m and col < n:
        C[row][col] = acc  # @line L7


def tiled_matmul(A, B, T, barrier1=True, barrier2=True):
    """Returns (C, counter). A is m x k and B is k x n, as lists of rows."""
    m, k = len(A), len(B)
    n = len(B[0]) if k else 0
    C = [[0] * n for _ in range(m)]
    cnt = Counter()
    for by in range(ceil_div(m, T)):
        for bx in range(ceil_div(n, T)):
            sh = {"A": [0] * (T * T), "B": [0] * (T * T)}
            gens = [tiled_kernel(tx, ty, bx, by, T, A, B, C, m, k, n, sh, cnt, barrier1, barrier2)
                    for ty in range(T) for tx in range(T)]
            _run_block(gens)
    return C, cnt


def naive_loads(m, k, n):
    """Global loads of the untiled kernel: each of the m n threads reads a row of A and a column of B."""
    return 2 * m * n * k


def tiled_loads(m, k, n, T):
    """Each element of A is loaded once per block column, each element of B once per block row."""
    return m * k * ceil_div(n, T) + k * n * ceil_div(m, T)


def matmul_reference(A, B):
    m, k = len(A), len(B)
    n = len(B[0]) if k else 0
    return [[sum(A[i][j] * B[j][c] for j in range(k)) for c in range(n)] for i in range(m)]
