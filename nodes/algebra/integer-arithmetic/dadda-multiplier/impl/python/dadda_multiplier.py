# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dadda-multiplier/. The authors are listed in prov/Q7R1ED.jsonl.

"""A gate-level model of the Dadda multiplier.

Each wire is a pair (bit, arrival time). An AND gate, a half adder and a full
adder each have delay 1 on all outputs. The partial product bits are kept in
columns by weight; Dadda's rule reduces the columns in stages to the heights
of the sequence 2, 3, 4, 6, 9, 13, ... and a ripple-carry adder adds the last
two rows.
"""

from dataclasses import dataclass

Wire = tuple[int, int]


@dataclass
class Counts:
    """The number of cells of each kind that the circuit uses."""

    and_gates: int = 0
    full_adders: int = 0
    half_adders: int = 0
    final_adder_width: int = 0
    stages: int = 0
    reduction_depth: int = 0


def dadda_heights(limit: int) -> list[int]:
    """Return the Dadda sequence 2, 3, 4, 6, 9, ... of the values below limit."""
    seq = [2]
    while seq[-1] * 3 // 2 < limit:
        seq.append(seq[-1] * 3 // 2)
    return [d for d in seq if d < limit]


def _full(x: Wire, y: Wire, z: Wire) -> tuple[Wire, Wire]:
    t = max(x[1], y[1], z[1]) + 1
    total = x[0] + y[0] + z[0]
    return (total & 1, t), (total >> 1, t)


def _half(x: Wire, y: Wire) -> tuple[Wire, Wire]:
    t = max(x[1], y[1]) + 1
    total = x[0] + y[0]
    return (total & 1, t), (total >> 1, t)


def dadda_multiply(a: list[int], b: list[int]) -> tuple[list[int], Counts, int]:
    """Multiply two n-bit unsigned numbers given as bit lists, low bit first.

    Precondition: len(a) == len(b) == n >= 1 and every entry is 0 or 1.
    Returns the 2n product bits (low first), the cell counts and the depth
    (the arrival time of the last product bit). The final adder is a ripple
    carry adder, so the depth is that of the ripple; counts.reduction_depth
    is the arrival time of the last bit of the two rows before it.
    """
    n = len(a)
    if n < 1 or len(b) != n:
        raise ValueError("operands must have the same length n >= 1")
    counts = Counts()
    width = 2 * n
    cols: list[list[Wire]] = [[] for _ in range(width + 1)]
    for i in range(n):  # @line L1
        for j in range(n):
            cols[i + j].append((a[i] & b[j], 1))
            counts.and_gates += 1
    targets = dadda_heights(n)  # @line L2
    for d in reversed(targets):  # @line L3
        if max(len(c) for c in cols) <= d:
            continue
        counts.stages += 1
        new_cols: list[list[Wire]] = [[] for _ in range(width + 1)]
        for k in range(width):  # @line L4
            bits = cols[k]
            excess = len(bits) + len(new_cols[k]) - d
            nf, nh = (excess // 2, excess % 2) if excess > 0 else (0, 0)
            if 3 * nf + 2 * nh > len(bits):
                raise AssertionError("Dadda rule ran out of bits")
            pos = 0
            for _ in range(nf):  # @line L5
                s, c = _full(bits[pos], bits[pos + 1], bits[pos + 2])
                pos += 3
                new_cols[k].append(s)
                new_cols[k + 1].append(c)
                counts.full_adders += 1
            for _ in range(nh):  # @line L6
                s, c = _half(bits[pos], bits[pos + 1])
                pos += 2
                new_cols[k].append(s)
                new_cols[k + 1].append(c)
                counts.half_adders += 1
            new_cols[k].extend(bits[pos:])  # @line L7
        if new_cols[width]:
            raise AssertionError("a carry left the product width")
        cols = new_cols
    counts.reduction_depth = max((w[1] for c in cols for w in c), default=0)
    out: list[int] = []  # @line L8
    depth = 0
    carry: Wire | None = None
    first = None
    for k in range(width):
        live = list(cols[k]) + ([carry] if carry is not None else [])
        if len(live) >= 2 and first is None:
            first = k
        if len(live) == 0:
            out.append(0)
            carry = None
            continue
        if len(live) == 1:
            out.append(live[0][0])
            depth = max(depth, live[0][1])
            carry = None
            continue
        if len(live) == 2:
            s, carry = _half(live[0], live[1])
        else:
            s, carry = _full(live[0], live[1], live[2])
        out.append(s[0])
        depth = max(depth, s[1])
    if carry is not None and carry[0]:
        raise AssertionError("product overflowed 2n bits")
    last = max((k for k in range(width) if len(cols[k]) == 2), default=-1)
    counts.final_adder_width = 0 if first is None else last - first + 1
    return out, counts, depth  # @line L9


def to_bits(x: int, n: int) -> list[int]:
    """The n low bits of x, least significant first."""
    return [(x >> i) & 1 for i in range(n)]


def from_bits(bits: list[int]) -> int:
    """The value of a bit list, least significant first."""
    return sum(bit << i for i, bit in enumerate(bits))


def stage_count(n: int) -> int:
    """The number of reduction stages: the Dadda heights below n."""
    return len(dadda_heights(n)) if n > 2 else 0
