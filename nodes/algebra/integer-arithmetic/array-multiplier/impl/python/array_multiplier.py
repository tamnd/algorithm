# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/array-multiplier/. The authors are listed in prov/4XX4WG.jsonl.

"""A gate-level model of the carry-save array multiplier.

Each wire is a pair (bit, arrival time), or None for a wire that is the
constant 0 by construction. An AND gate has delay 1, and a full adder or a
half adder has delay 1 on both outputs. A cell with three live inputs is a
full adder, with two it is a half adder, and with one it is a plain wire.
"""

from dataclasses import dataclass

Wire = tuple[int, int] | None


@dataclass
class Counts:
    """The number of cells of each kind that the circuit uses."""

    and_gates: int = 0
    full_adders: int = 0
    half_adders: int = 0


def _cell(x: Wire, y: Wire, z: Wire, counts: Counts) -> tuple[Wire, Wire]:
    """Add up to three bits of one weight; return (sum, carry)."""
    live = [w for w in (x, y, z) if w is not None]
    if not live:
        return None, None
    if len(live) == 1:
        return live[0], None
    if len(live) == 2:
        counts.half_adders += 1
    else:
        counts.full_adders += 1
    total = sum(w[0] for w in live)
    t = max(w[1] for w in live) + 1
    return (total & 1, t), (total >> 1, t)


def array_multiply(a: list[int], b: list[int]) -> tuple[list[int], Counts, int]:
    """Multiply two n-bit unsigned numbers given as bit lists, low bit first.

    Precondition: len(a) == len(b) == n >= 1 and every entry is 0 or 1.
    Returns the 2n product bits (low first), the cell counts and the depth
    (the arrival time of the last product bit). Cost: n^2 AND gates and
    n(n - 1) adder cells for n >= 2, simulated in Theta(n^2) steps.
    """
    n = len(a)
    if n < 1 or len(b) != n:
        raise ValueError("operands must have the same length n >= 1")
    counts = Counts()
    pp: list[list[Wire]] = []
    for j in range(n):  # @line L1
        pp.append([(a[i] & b[j], 1) for i in range(n)])
        counts.and_gates += n
    s: list[Wire] = list(pp[0])  # @line L2
    c: list[Wire] = [None] * n
    p: list[Wire] = [None] * (2 * n)
    for j in range(1, n):  # @line L3
        p[j - 1] = s[0]  # @line L4
        new_s: list[Wire] = []
        new_c: list[Wire] = []
        for i in range(n):  # @line L5
            upper = s[i + 1] if i + 1 < n else None
            si, ci = _cell(pp[j][i], upper, c[i], counts)
            new_s.append(si)
            new_c.append(ci)
        s, c = new_s, new_c  # @line L6
    p[n - 1] = s[0]  # @line L7
    carry: Wire = None  # @line L8
    for i in range(1, n):  # @line L9
        p[n - 1 + i], carry = _cell(s[i], c[i - 1], carry, counts)  # @line L10
    p[2 * n - 1] = carry  # @line L11
    bits = [w[0] if w is not None else 0 for w in p]
    depth = max((w[1] for w in p if w is not None), default=0)
    return bits, counts, depth


def to_bits(x: int, n: int) -> list[int]:
    """The n low bits of x >= 0, low bit first."""
    return [(x >> i) & 1 for i in range(n)]


def from_bits(bits: list[int]) -> int:
    """The value of a bit list, low bit first."""
    return sum(bit << i for i, bit in enumerate(bits))


def multiply(x: int, y: int, n: int) -> int:
    """x * y for 0 <= x, y < 2^n, computed by the array multiplier."""
    bits, _, _ = array_multiply(to_bits(x, n), to_bits(y, n))
    return from_bits(bits)
