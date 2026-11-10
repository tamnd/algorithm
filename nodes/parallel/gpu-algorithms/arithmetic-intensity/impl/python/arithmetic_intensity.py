# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arithmetic-intensity/.
"""Arithmetic intensity I = W / Q in FLOP per byte, as exact fractions.

The closed forms count W (FLOP, a multiply-add is 2) and Q (bytes that cross the memory link).
The trace_* functions walk the loops of each kernel and count the same quantities one access at a
time, under the cache assumption named in each function, so the tests can compare the two.
"""

from fractions import Fraction as F


def intensity(w, q):
    return F(w, q)


# Closed forms; s is the size of one element in bytes (4 for FP32, 8 for FP64).

def vector_add(n, s=4):
    return 1 * n, 3 * s * n  # c[i] = a[i] + b[i]


def dot_product(n, s=4):
    return 2 * n, 2 * s * n + s  # n multiply-adds, read x and y, write one result


def matvec(n, s=4, x_cached=True):
    """y = A x for an n x n matrix. With x_cached, x is read from memory once."""
    reads_x = n if x_cached else n * n
    return 2 * n * n, s * (n * n + reads_x + n)


def naive_matmul(n, s=4):
    """One thread per output, every operand read from memory, no cache."""
    return 2 * n**3, s * (2 * n**3 + n * n)


def tiled_matmul(n, t, s=4):
    """Shared-memory tiles of t x t; each block loads 2 t n words and writes t t words."""
    assert n % t == 0
    blocks = (n // t) ** 2
    return 2 * n**3, s * (blocks * 2 * t * n + n * n)


def ideal_matmul(n, s=4):
    """Every word of A, B and C crosses the link once: the compulsory traffic."""
    return 2 * n**3, s * 3 * n * n


def unfused_add_mul(n, s=4):
    """d = a + b, then e = d * c, as two kernels: d is stored and loaded again."""
    return 2 * n, s * (3 * n + 3 * n)


def fused_add_mul(n, s=4):
    """e = (a + b) * c in one kernel: d stays in a register."""
    return 2 * n, s * 4 * n


def csr_spmv(nnz, rows, value=8, index=4, x_bytes_per_nnz=8):
    """y = A x in CSR: per nonzero a value, a column index and an x read; row pointers and y."""
    return 2 * nnz, nnz * (value + index + x_bytes_per_nnz) + (rows + 1) * index + rows * value


# Traces: walk the loops and count.

def trace_vector_add(n, s=4):
    w = q = 0
    for _ in range(n):
        q += 2 * s  # load a[i], b[i]
        w += 1
        q += s  # store c[i]
    return w, q


def trace_dot_product(n, s=4):
    w = q = 0
    for _ in range(n):
        q += 2 * s
        w += 2
    return w, q + s


def trace_matvec(n, s=4, x_cached=True):
    w = q = 0
    seen_x = set()
    for i in range(n):
        for j in range(n):
            q += s  # A[i][j]
            if not x_cached or j not in seen_x:
                q += s  # x[j]
                seen_x.add(j)
            w += 2
        q += s  # y[i]
    return w, q


def trace_tiled_matmul(n, t, s=4):
    w = q = 0
    for by in range(n // t):
        for bx in range(n // t):
            for phase in range(n // t):
                q += 2 * t * t * s  # the block loads one tile of A and one tile of B
                w += t * t * t * 2  # t*t threads each do t multiply-adds from shared memory
            q += t * t * s  # store the t x t outputs
    return w, q
