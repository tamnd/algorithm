# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wallace-tree-multiplier/. The authors are listed in prov/N0JM8H.jsonl.

"""A Wallace tree multiplier, simulated gate by gate.

Every signal is a pair (value, depth). The partial product bits are reduced
column by column, level by level, with full adders and half adders until every
column holds at most two bits, and a Kogge-Stone prefix adder adds the two
remaining rows. A Stats object counts the gates, the adders and the levels and
records the column heights after each level.
"""


class Stats:
    def __init__(self) -> None:
        self.gates = 0
        self.full_adders = 0
        self.half_adders = 0
        self.levels = 0
        self.heights: list[list[int]] = []


def _and(x, y, st):
    st.gates += 1
    return x[0] & y[0], max(x[1], y[1]) + 1


def _or(x, y, st):
    st.gates += 1
    return x[0] | y[0], max(x[1], y[1]) + 1


def _xor(x, y, st):
    st.gates += 1
    return x[0] ^ y[0], max(x[1], y[1]) + 1


def full_adder(x, y, z, st):
    """Three bits of one column in; a sum bit for the column and a carry bit for the next."""
    st.full_adders += 1
    p = _xor(x, y, st)
    s = _xor(p, z, st)
    c = _or(_and(x, y, st), _and(p, z, st), st)
    return s, c


def half_adder(x, y, st):
    st.half_adders += 1
    return _xor(x, y, st), _and(x, y, st)


def _prefix_add(X: list, Y: list, st: Stats) -> list:
    """Kogge-Stone addition of two rows of signals of equal length; returns len + 1 signals."""
    n = len(X)
    g = [_and(X[i], Y[i], st) for i in range(n)]
    p = [_xor(X[i], Y[i], st) for i in range(n)]
    G, P = list(g), list(p)
    d = 1
    while d < n:
        nG, nP = list(G), list(P)
        for i in range(d, n):
            nG[i] = _or(G[i], _and(P[i], G[i - d], st), st)
            nP[i] = _and(P[i], P[i - d], st)
        G, P = nG, nP
        d *= 2
    zero = (0, 0)
    c = [zero] + G
    return [_xor(p[i], c[i], st) for i in range(n)] + [c[n]]


def wallace_multiply(a: list[int], b: list[int], st: Stats | None = None) -> tuple[list[int], int]:
    """Multiply two bit lists (least significant first); return the product bits and the depth."""
    if st is None:
        st = Stats()
    n, m = len(a), len(b)
    if n == 0 or m == 0:
        return [0], 0
    A = [(x & 1, 0) for x in a]
    B = [(x & 1, 0) for x in b]
    width = n + m
    cols: list[list] = [[] for _ in range(width + 1)]
    for i in range(n):  # @line L1: the n m partial product bits, a_i AND b_j in column i + j
        for j in range(m):
            cols[i + j].append(_and(A[i], B[j], st))
    st.heights.append([len(c) for c in cols[:width]])
    while max(len(c) for c in cols) > 2:  # @line L2: one level of the tree
        new: list[list] = [[] for _ in range(width + 1)]
        for k in range(width):  # @line L3: all columns in parallel
            bits = cols[k]
            t = 0
            while len(bits) - t >= 3:  # @line L4: groups of three
                s, c = full_adder(bits[t], bits[t + 1], bits[t + 2], st)  # @line L5
                new[k].append(s)
                new[k + 1].append(c)
                t += 3
            if len(bits) - t == 2:  # @line L6: a pair goes to a half adder, a single bit passes
                s, c = half_adder(bits[t], bits[t + 1], st)
                new[k].append(s)
                new[k + 1].append(c)
            elif len(bits) - t == 1:
                new[k].append(bits[t])
        cols = new
        st.levels += 1
        st.heights.append([len(c) for c in cols[:width]])
    zero = (0, 0)
    X = [cols[k][0] if len(cols[k]) > 0 else zero for k in range(width)]  # @line L7: the two rows
    Y = [cols[k][1] if len(cols[k]) > 1 else zero for k in range(width)]
    out = _prefix_add(X, Y, st)[:width]  # @line L8: one carry-propagate addition
    return [x[0] for x in out], max(x[1] for x in out)


def tree_levels(k: int) -> int:
    """The number of levels of carry-save reduction that k rows need: the least j
    with d_j >= k, where d_0 = 2 and d_{j+1} = floor(3 d_j / 2)."""
    d, j = 2, 0
    while d < k:
        d = 3 * d // 2
        j += 1
    return j


def to_bits(x: int, n: int) -> list[int]:
    return [(x >> i) & 1 for i in range(n)]


def from_bits(s: list[int]) -> int:
    return sum(bit << i for i, bit in enumerate(s))


def multiply_limbs(a: list[int], b: list[int], w: int = 8) -> list[int]:
    """Multiply two limb arrays in radix 2**w with one Wallace tree of their full width."""
    if not a or not b:
        return [0] * (len(a) + len(b))
    abits = [(a[i // w] >> (i % w)) & 1 for i in range(len(a) * w)]
    bbits = [(b[i // w] >> (i % w)) & 1 for i in range(len(b) * w)]
    s, _ = wallace_multiply(abits, bbits)
    out = [0] * (len(a) + len(b))
    for i, bit in enumerate(s):
        out[i // w] |= bit << (i % w)
    return out


def multiply_signed(x: int, y: int, n: int) -> int:
    """Two's complement n-bit operands: multiply the magnitudes and fix the sign."""
    lo, hi = -(1 << (n - 1)), (1 << (n - 1)) - 1
    if not (lo <= x <= hi and lo <= y <= hi):
        raise ValueError("operand out of range")
    s, _ = wallace_multiply(to_bits(abs(x), n), to_bits(abs(y), n))
    p = from_bits(s)
    return -p if (x < 0) != (y < 0) else p
