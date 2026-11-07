# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/carry-skip-adder/. The authors are listed in prov/FWJCMW.jsonl.

"""The carry-skip (carry-bypass) adder, simulated gate by gate.

Bit lists are least significant bit first. Every signal is a triple
(value, settle time, depth). The depth is the topological one: one more than
the deepest input. The settle time follows controlling values: an AND gate
whose output is 0 settles one unit after its earliest 0 input, an OR gate
whose output is 1 one unit after its earliest 1 input, and otherwise a gate
settles one unit after its latest input. The settle time depends on the data;
its maximum over all inputs is the delay of the adder.
"""

from dataclasses import dataclass

Wire = tuple[int, int, int]


@dataclass
class Stats:
    gates: int = 0


def _and(x: Wire, y: Wire, st: Stats) -> Wire:
    st.gates += 1
    d = max(x[2], y[2]) + 1
    if x[0] and y[0]:
        return 1, max(x[1], y[1]) + 1, d
    return 0, min(w[1] for w in (x, y) if w[0] == 0) + 1, d


def _or(x: Wire, y: Wire, st: Stats) -> Wire:
    st.gates += 1
    d = max(x[2], y[2]) + 1
    if x[0] or y[0]:
        return 1, min(w[1] for w in (x, y) if w[0] == 1) + 1, d
    return 0, max(x[1], y[1]) + 1, d


def _xor(x: Wire, y: Wire, st: Stats) -> Wire:
    st.gates += 1
    return x[0] ^ y[0], max(x[1], y[1]) + 1, max(x[2], y[2]) + 1


def _not(x: Wire, st: Stats) -> Wire:
    st.gates += 1
    return 1 - x[0], x[1] + 1, x[2] + 1


def _and_tree(ws: list[Wire], st: Stats) -> Wire:
    while len(ws) > 1:
        nxt = [_and(ws[i], ws[i + 1], st) for i in range(0, len(ws) - 1, 2)]
        if len(ws) % 2:
            nxt.append(ws[-1])
        ws = nxt
    return ws[0]


def carry_skip_add(a: list[int], b: list[int], c_in: int, sizes: list[int], st: Stats | None = None):
    """Add two n-bit lists with ripple blocks of the given sizes, low block first.

    Returns (n + 1 result bits with the carry out last, delay, depth): the
    settle time of the slowest output on this input, and the depth of the circuit.
    """
    if st is None:
        st = Stats()
    n = len(a)
    if len(b) != n or n == 0 or sum(sizes) != n or min(sizes) < 1:
        raise ValueError("bad widths or block sizes")
    A = [(x & 1, 0, 0) for x in a]
    B = [(x & 1, 0, 0) for x in b]
    g = [_and(A[i], B[i], st) for i in range(n)]  # @line L1
    p = [_xor(A[i], B[i], st) for i in range(n)]  # @line L1
    starts = [sum(sizes[:j]) for j in range(len(sizes))]
    big_p = [None] + [_and_tree(p[lo:lo + k], st) for lo, k in zip(starts[1:], sizes[1:])]  # @line L2
    c: Wire = (c_in & 1, 0, 0)  # @line L3
    s: list[Wire] = []
    for j, (lo, k) in enumerate(zip(starts, sizes)):  # @line L4
        x = c  # @line L5
        for i in range(lo, lo + k):  # @line L6
            s.append(_xor(p[i], c, st))  # @line L6
            c = _or(g[i], _and(p[i], c, st), st)  # @line L6
        if j >= 1:  # @line L7
            c = _or(_and(big_p[j], x, st), _and(_not(big_p[j], st), c, st), st)  # @line L7
    out = s + [c]
    return [w[0] for w in out], max(w[1] for w in out), max(w[2] for w in out)  # @line L8


def uniform_sizes(n: int, k: int) -> list[int]:
    return [k] * (n // k) + ([n % k] if n % k else [])


def worst_input(n: int) -> tuple[int, int, int]:
    """Operands (a, b, c_in) of the slowest case found: the carry-in 1 is
    killed at position 0, and the carry 0 that leaves position 0 must then
    pass every position, because all other positions propagate."""
    return (1 << n) - 2, 0, 1


def delay_bound(sizes: list[int]) -> int:
    """The upper bound on the delay proved on the page, for these block sizes.

    T is the time by which the carry into the next block has settled.
    """
    best = 2 * sizes[0]
    t = 2 * sizes[0] + 1
    for k in sizes[1:]:
        best = max(best, t + 2 * k - 1)
        t = max(t + 2, 2 * k + 3)
    return max(best, t)


def depth_formula(n: int, blocks: int) -> int:
    """The depth of the circuit: the ripple path through all n positions,
    plus two gates for each skip multiplexer on it."""
    return 2 * n + 2 * blocks - 1


def to_bits(x: int, n: int) -> list[int]:
    return [(x >> i) & 1 for i in range(n)]


def from_bits(bits: list[int]) -> int:
    return sum(bit << i for i, bit in enumerate(bits))


def add(x: int, y: int, n: int, c_in: int = 0, sizes: list[int] | None = None) -> int:
    """x + y + c_in for 0 <= x, y < 2^n, through the circuit."""
    if sizes is None:
        sizes = uniform_sizes(n, max(1, round((n / 2) ** 0.5)))
    bits, _, _ = carry_skip_add(to_bits(x, n), to_bits(y, n), c_in, sizes)
    return from_bits(bits)
