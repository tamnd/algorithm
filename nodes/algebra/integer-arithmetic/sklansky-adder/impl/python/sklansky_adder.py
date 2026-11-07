# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sklansky-adder/. The authors are listed in prov/JA4QR9.jsonl.

"""The Sklansky (divide-and-conquer) parallel-prefix adder, simulated gate by gate.

Bit lists are least significant bit first. Every signal is a pair (value,
depth), and a Stats object counts gates, prefix cells and the fan-out of every
prefix signal, so that the size, depth and fan-out of the circuit can be checked.
"""

from collections import Counter


class Stats:
    def __init__(self) -> None:
        self.gates = 0
        self.cells = 0
        self.fanout: Counter = Counter()  # uses of the pair held at a position, keyed by (position, version)
        self.max_recursion = 0


def _gate(op, x: tuple[int, int], y: tuple[int, int], st: Stats) -> tuple[int, int]:
    st.gates += 1
    return op(x[0], y[0]), max(x[1], y[1]) + 1


def _and(x, y, st):
    return _gate(lambda u, v: u & v, x, y, st)


def _or(x, y, st):
    return _gate(lambda u, v: u | v, x, y, st)


def _xor(x, y, st):
    return _gate(lambda u, v: u ^ v, x, y, st)


def _prefix(G: list, P: list, version: list[int], lo: int, hi: int, st: Stats, depth: int) -> None:
    """After the call, (G[i], P[i]) is the pair of the block lo..i for lo <= i < hi."""
    st.max_recursion = max(st.max_recursion, depth)
    if hi - lo <= 1:  # @line L7
        return
    mid = lo + (hi - lo + 1) // 2  # @line L8: the low half has ceil(size / 2) positions
    _prefix(G, P, version, lo, mid, st, depth + 1)  # @line L9: the two halves, in parallel
    _prefix(G, P, version, mid, hi, st, depth + 1)
    gl, pl = G[mid - 1], P[mid - 1]
    for i in range(mid, hi):  # @line L10: combine every high position with the top of the low half
        st.fanout[(mid - 1, version[mid - 1])] += 1
        G[i] = _or(G[i], _and(P[i], gl, st), st)
        P[i] = _and(P[i], pl, st)
        version[i] += 1
        st.cells += 1


def sklansky_add(a: list[int], b: list[int], c_in: int = 0, st: Stats | None = None) -> tuple[list[int], int]:
    """Add two n-bit lists; return the n + 1 sum bits (carry out last) and the depth."""
    if st is None:
        st = Stats()
    n = len(a)
    if len(b) != n:
        raise ValueError("the operands must have the same width")
    cin = (c_in & 1, 0)
    if n == 0:
        return [cin[0]], 0
    A = [(x & 1, 0) for x in a]
    B = [(x & 1, 0) for x in b]
    g = [_and(A[i], B[i], st) for i in range(n)]  # @line L1: generate and propagate bits
    p = [_xor(A[i], B[i], st) for i in range(n)]
    g[0] = _or(g[0], _and(p[0], cin, st), st)  # @line L2: fold the carry in
    G, P = list(g), list(p)
    _prefix(G, P, [0] * n, 0, n, st, 0)  # @line L3
    c = [cin] + G  # @line L4: c[i + 1] = G[i]
    s = [_xor(p[i], c[i], st) for i in range(n)]  # @line L5
    out = s + [c[n]]
    return [x[0] for x in out], max(x[1] for x in out)  # @line L6


def prefix_blocks(n: int) -> list[list[tuple[int, int]]]:
    """The block lo..i held by each position after each level, for the example table."""
    levels = []
    size = 1
    while size < n:
        size *= 2
        levels.append([((i // size) * size, i) for i in range(n)])
    return levels


def to_bits(x: int, n: int) -> list[int]:
    return [(x >> i) & 1 for i in range(n)]


def from_bits(s: list[int]) -> int:
    return sum(bit << i for i, bit in enumerate(s))


def add_limbs(a: list[int], b: list[int], w: int = 8, c_in: int = 0) -> list[int]:
    """Add two limb arrays in radix 2**w with one Sklansky adder of their full width."""
    n = max(len(a), len(b))
    a = list(a) + [0] * (n - len(a))
    b = list(b) + [0] * (n - len(b))
    abits = [(a[i // w] >> (i % w)) & 1 for i in range(n * w)]
    bbits = [(b[i // w] >> (i % w)) & 1 for i in range(n * w)]
    s, _ = sklansky_add(abits, bbits, c_in)
    out = [0] * (n + 1)
    for i, bit in enumerate(s):
        out[i // w] |= bit << (i % w)
    return out
