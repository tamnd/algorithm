# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/carry-select-adder/. The authors are listed in prov/0D2Z2R.jsonl.

"""The carry-select adder, simulated gate by gate.

Bit lists are least significant bit first. Every signal is a pair (value,
arrival time); AND, OR and XOR gates have two inputs and unit delay. The
constant carries 0 and 1 of the two copies of each block are folded in, so
the gate count is that of a real circuit. The block sizes are a parameter.
"""

from dataclasses import dataclass

Wire = tuple[int, int]
ZERO: Wire = (0, 0)
ONE: Wire = (1, 0)


@dataclass
class Stats:
    gates: int = 0


def _and(x: Wire, y: Wire, st: Stats) -> Wire:
    st.gates += 1
    return x[0] & y[0], max(x[1], y[1]) + 1


def _or(x: Wire, y: Wire, st: Stats) -> Wire:
    st.gates += 1
    return x[0] | y[0], max(x[1], y[1]) + 1


def _xor(x: Wire, y: Wire, st: Stats) -> Wire:
    st.gates += 1
    return x[0] ^ y[0], max(x[1], y[1]) + 1


def _ripple(g: list[Wire], p: list[Wire], c: Wire | int, st: Stats) -> tuple[list[Wire], Wire]:
    """Ripple through one block; c is a wire, or the constant 0 or 1."""
    sums = []
    for gi, pi in zip(g, p):
        if c == 0:
            sums.append(pi)
            c = gi
        elif c == 1:
            sums.append(_xor(pi, ONE, st))
            c = _or(gi, pi, st)
        else:
            sums.append(_xor(pi, c, st))
            c = _or(gi, _and(pi, c, st), st)
    return sums, c


def carry_select_add(a: list[int], b: list[int], c_in: int, sizes: list[int], st: Stats | None = None):
    """Add two n-bit lists with blocks of the given sizes, low block first.

    Returns (n + 1 result bits with the carry out last, depth).
    """
    if st is None:
        st = Stats()
    n = len(a)
    if len(b) != n or n == 0 or sum(sizes) != n or min(sizes) < 1:
        raise ValueError("bad widths or block sizes")
    A = [(x & 1, 0) for x in a]
    B = [(x & 1, 0) for x in b]
    g = [_and(A[i], B[i], st) for i in range(n)]  # @line L1
    p = [_xor(A[i], B[i], st) for i in range(n)]  # @line L1
    k0 = sizes[0]
    s, carry = _ripple(g[:k0], p[:k0], (c_in & 1, 0), st)  # @line L2
    starts = [sum(sizes[:j]) for j in range(len(sizes))]
    pre = []
    for j in range(1, len(sizes)):  # @line L3
        lo, hi = starts[j], starts[j] + sizes[j]
        s0, c0 = _ripple(g[lo:hi], p[lo:hi], 0, st)  # @line L4
        s1, c1 = _ripple(g[lo:hi], p[lo:hi], 1, st)  # @line L4
        diff = [_xor(x, y, st) for x, y in zip(s0, s1)]
        pre.append((s0, diff, c0, c1))
    for s0, diff, c0, c1 in pre:  # @line L5
        cb = carry  # @line L6
        s += [_xor(x, _and(cb, d, st), st) for x, d in zip(s0, diff)]  # @line L7
        carry = _or(c0, _and(c1, cb, st), st)  # @line L8
    out = s + [carry]
    return [w[0] for w in out], max(w[1] for w in out)  # @line L9


def uniform_sizes(n: int, k: int) -> list[int]:
    """Blocks of size k, with a shorter last block if k does not divide n."""
    return [k] * (n // k) + ([n % k] if n % k else [])


def growing_sizes(n: int, k0: int = 1) -> list[int]:
    """Block sizes k0, k0, k0 + 1, k0 + 2, ..., the last block cut to fit.

    With these sizes the two results of each block are ready by the time its
    carry-in arrives, so each block adds only the two gates of its carry
    selection to the critical path.
    """
    sizes, total, k = [], 0, k0
    while total < n:
        take = min(k, n - total)
        sizes.append(take)
        total += take
        if len(sizes) >= 2:
            k += 1
    return sizes


def to_bits(x: int, n: int) -> list[int]:
    return [(x >> i) & 1 for i in range(n)]


def from_bits(bits: list[int]) -> int:
    return sum(bit << i for i, bit in enumerate(bits))


def add(x: int, y: int, n: int, c_in: int = 0, sizes: list[int] | None = None) -> int:
    """x + y + c_in for 0 <= x, y < 2^n, through the circuit."""
    if sizes is None:
        sizes = uniform_sizes(n, max(1, round(n ** 0.5)))
    bits, _ = carry_select_add(to_bits(x, n), to_bits(y, n), c_in, sizes)
    return from_bits(bits)
