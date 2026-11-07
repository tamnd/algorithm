# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brent-kung-adder/. The authors are listed in prov/XD1FWT.jsonl.

"""The Brent-Kung parallel-prefix adder, simulated gate by gate.

Bit lists are least significant bit first. Every signal is a pair (value,
arrival time), every gate has two inputs and unit delay, and the simulation
counts gates, prefix cells and the levels of cells that are not empty, so
that the tests can check the size and depth claims of the page.
"""

from dataclasses import dataclass

Wire = tuple[int, int]


@dataclass
class Stats:
    gates: int = 0
    cells: int = 0
    levels: int = 0


def _gate(op, x: Wire, y: Wire, st: Stats) -> Wire:
    st.gates += 1
    return op(x[0], y[0]), max(x[1], y[1]) + 1


def _and(x: Wire, y: Wire, st: Stats) -> Wire:
    return _gate(lambda u, v: u & v, x, y, st)


def _or(x: Wire, y: Wire, st: Stats) -> Wire:
    return _gate(lambda u, v: u | v, x, y, st)


def _xor(x: Wire, y: Wire, st: Stats) -> Wire:
    return _gate(lambda u, v: u ^ v, x, y, st)


def _combine(G, P, lo, i, j, st: Stats) -> None:
    """(G, P)[i] <- (G, P)[i] o (G, P)[j], where j is the position just below the block of i."""
    G[i] = _or(G[i], _and(P[i], G[j], st), st)
    if lo[j] > 0:  # the new block does not reach position 0, so its P is still needed
        P[i] = _and(P[i], P[j], st)
    lo[i] = lo[j]
    st.cells += 1


def brent_kung_add(a: list[int], b: list[int], c_in: int = 0, st: Stats | None = None) -> tuple[list[int], int]:
    """Add two n-bit lists; return the n + 1 result bits (carry out last) and the depth."""
    if st is None:
        st = Stats()
    n = len(a)
    if len(b) != n or n == 0:
        raise ValueError("the operands must have the same positive width")
    cin = (c_in & 1, 0)
    A = [(x & 1, 0) for x in a]
    B = [(x & 1, 0) for x in b]
    g = [_and(A[i], B[i], st) for i in range(n)]  # @line L1
    p = [_xor(A[i], B[i], st) for i in range(n)]  # @line L1
    g[0] = _or(g[0], _and(p[0], cin, st), st)  # @line L2
    G, P = list(g), list(p)  # @line L3
    lo = list(range(n))  # lo[i]: the lowest position of the block held by i
    d = 1  # @line L3
    while d < n:  # @line L4
        level = range(2 * d - 1, n, 2 * d)
        for i in level:  # @line L5
            _combine(G, P, lo, i, i - d, st)
        st.levels += len(level) > 0
        d *= 2  # @line L6
    d //= 4  # @line L7
    while d >= 1:  # @line L8
        level = range(3 * d - 1, n, 2 * d)
        for i in level:  # @line L9
            _combine(G, P, lo, i, i - d, st)
        st.levels += len(level) > 0
        d //= 2  # @line L10
    assert all(x == 0 for x in lo)
    c = [cin] + G  # @line L11
    s = [_xor(p[i], c[i], st) for i in range(n)]  # @line L12
    out = s + [c[n]]
    return [x[0] for x in out], max(x[1] for x in out)  # @line L13


def to_bits(x: int, n: int) -> list[int]:
    return [(x >> i) & 1 for i in range(n)]


def from_bits(bits: list[int]) -> int:
    return sum(bit << i for i, bit in enumerate(bits))


def add(x: int, y: int, n: int, c_in: int = 0) -> int:
    """x + y + c_in for 0 <= x, y < 2^n, through the circuit."""
    bits, _ = brent_kung_add(to_bits(x, n), to_bits(y, n), c_in)
    return from_bits(bits)
