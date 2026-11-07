# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-lanczos-algorithm/. The authors are listed in prov/ZXGZZS.jsonl.

"""Montgomery's block Lanczos algorithm over GF(2).

A block of s vectors of length n is a list of n integers; bit c of entry r is the
entry in row r and column c. An s x s matrix is a list of s integers (its rows).
The sparse matrix B is a list of rows, each a list of the column indices of its ones.
"""

import random
from typing import Sequence

SparseRows = Sequence[Sequence[int]]


def b_times(b: SparseRows, v: Sequence[int]) -> list[int]:
    """B V for a sparse m x n matrix B and an n x s block V."""
    out = []
    for row in b:
        acc = 0
        for j in row:
            acc ^= v[j]
        out.append(acc)
    return out


def bt_times(b: SparseRows, u: Sequence[int], n: int) -> list[int]:
    """B^T U for a sparse m x n matrix B and an m x s block U."""
    out = [0] * n
    for k, row in enumerate(b):
        x = u[k]
        if x:
            for j in row:
                out[j] ^= x
    return out


def inner(v: Sequence[int], w: Sequence[int], s: int) -> list[int]:
    """V^T W, an s x s matrix, for two blocks with the same number of rows."""
    res = [0] * s
    for x, y in zip(v, w):
        while x:
            low = x & -x
            res[low.bit_length() - 1] ^= y
            x ^= low
    return res


def times_small(v: Sequence[int], m: Sequence[int]) -> list[int]:
    """V M for a block V and an s x s matrix M (also M1 M2 for two s x s matrices)."""
    out = []
    for x in v:
        acc = 0
        while x:
            low = x & -x
            acc ^= m[low.bit_length() - 1]
            x ^= low
        out.append(acc)
    return out


def add(m1: Sequence[int], m2: Sequence[int]) -> list[int]:
    return [x ^ y for x, y in zip(m1, m2)]


def select(t: Sequence[int], prev_mask: int, s: int) -> tuple[list[int], int] | None:
    """Montgomery's choice of S_i and W_i^inv = S (S^T T S)^{-1} S^T from T = V^T A V.

    The columns not in the previous selection are taken first. Returns (winv, mask),
    or None if the step breaks down.
    """
    full = (1 << s) - 1
    order = [c for c in range(s) if not prev_mask >> c & 1] + [c for c in range(s) if prev_mask >> c & 1]
    m = [t[c] | (1 << (s + c)) for c in range(s)]  # row c of [T | I], the identity in bits s..2s-1
    mask = 0
    for idx, c in enumerate(order):
        k = next((order[q] for q in range(idx, s) if m[order[q]] >> c & 1), None)
        if k is not None:
            m[c], m[k] = m[k], m[c]
            mask |= 1 << c
            for r in range(s):
                if r != c and m[r] >> c & 1:
                    m[r] ^= m[c]
        else:
            k = next((order[q] for q in range(idx, s) if m[order[q]] >> (s + c) & 1), None)
            if k is None:
                return None
            m[c], m[k] = m[k], m[c]
            for r in range(s):
                if r != c and m[r] >> (s + c) & 1:
                    m[r] ^= m[c]
            m[c] = 0
    if (mask | prev_mask) != full:
        return None
    return [(m[c] >> s) & full for c in range(s)], mask


def block_lanczos_kernel(b: SparseRows, n: int, s: int = 16, seed: int = 0,
                         tries: int = 3, trace: list | None = None) -> list[list[int]]:
    """Independent nonzero vectors x in GF(2)^n with B x = 0, for a sparse m x n matrix B.

    Runs block Lanczos on A = B^T B with block width s. Every returned vector is checked;
    the list may be empty if all tries break down or find nothing. If trace is a list,
    each iteration appends (V_i, mask of S_i) to it, for testing.
    Cost: about n / (s - 0.76) iterations, each with one product by B and one by B^T on
    an n x s block, and O(n s) word operations.
    """
    rng = random.Random(seed)
    full = (1 << s) - 1
    for _ in range(tries):
        if trace is not None:
            trace.clear()
        found = _one_run(b, n, s, rng, full, trace)
        if found:
            return found
    return []


def _one_run(b: SparseRows, n: int, s: int, rng: random.Random, full: int,
             trace: list | None) -> list[list[int]]:
    if n == 0:
        return []
    y = [rng.getrandbits(s) for _ in range(n)]  # @line L1
    v = bt_times(b, b_times(b, y), n)  # V_0 = A Y
    v0 = v
    x = [0] * n
    zero_block = [0] * n
    zero_small = [0] * s
    v1 = v2 = zero_block  # V_{i-1}, V_{i-2}
    winv1 = winv2 = zero_small
    t1 = t2_1 = zero_small  # T and T2 of step i-1
    mask1 = full
    for _ in range(n + 10):  # @line L2
        av = bt_times(b, b_times(b, v), n)  # @line L3
        t = inner(v, av, s)
        t2 = inner(av, av, s)
        if not any(t):  # @line L4
            break
        sel = select(t, mask1, s)  # @line L5
        if sel is None:
            break  # breakdown: finish with the current block, the final step checks everything
        winv, mask = sel
        if trace is not None:
            trace.append((v, mask))
        x = add(x, times_small(v, times_small(winv, inner(v, v0, s))))  # @line L6
        ident = [1 << c for c in range(s)]
        t2m = [r & mask for r in t2]
        d = add(ident, times_small(winv, add(t2m, t)))  # @line L7
        e = times_small(winv1, [r & mask for r in t])
        f = times_small(times_small(winv2, add(ident, times_small(t1, winv1))),
                        [r & mask for r in add([r & mask1 for r in t2_1], t1)])
        new = add(add([r & mask for r in av], times_small(v, d)), add(times_small(v1, e), times_small(v2, f)))  # @line L8
        v2, v1, v = v1, v, new
        winv2, winv1 = winv1, winv
        t1, t2_1, mask1 = t, t2, mask
    # @line L9
    z = [(xi ^ yi) | (vi << s) for xi, yi, vi in zip(x, y, v)]  # columns: X + Y, then V_m
    bz = b_times(b, z)
    cols = 2 * s
    zc = [_column(z, c) for c in range(cols)]
    bzc = [_column(bz, c) for c in range(cols)]
    basis: dict[int, tuple[int, int]] = {}
    kernel = []
    for c in range(cols):  # @line L10
        img, pre = bzc[c], zc[c]
        while img:
            top = img.bit_length() - 1
            if top not in basis:
                break
            bi, bp = basis[top]
            img, pre = img ^ bi, pre ^ bp
        if img:
            basis[img.bit_length() - 1] = (img, pre)
        elif pre:
            kernel.append(pre)
    out: dict[int, int] = {}
    for vec in kernel:
        while vec:
            top = vec.bit_length() - 1
            if top not in out:
                out[top] = vec
                break
            vec ^= out[top]
    return [[vec >> r & 1 for r in range(n)] for vec in out.values()]  # @line L11


def _column(block: Sequence[int], c: int) -> int:
    """Column c of a block as an integer with bit r for row r."""
    col = 0
    for r, x in enumerate(block):
        if x >> c & 1:
            col |= 1 << r
    return col
