# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/threshold-implementation/. The authors are listed in prov/2V6QRX.jsonl.
"""A threshold implementation of the AND of two bits with three shares.

This is a small abstract model of a masked gate, not of a device. Shares
are bits in tuples. To model glitches, a probe on the output of a
component function is extended to all the inputs of that function: the
function ``component_inputs`` returns those inputs, and the tests compare
their distributions over all input sharings. Random bits come from the
caller or from a seeded ``random.Random``.
"""

import itertools
import random

Shares = tuple[int, ...]


def sharings(v: int, n: int) -> list[Shares]:
    """All n-share Boolean sharings of the bit v, that is 2^(n-1) tuples."""
    return [s for s in itertools.product((0, 1), repeat=n) if sum(s) % 2 == v]


def ti_and(x: Shares, y: Shares, r: tuple[int, int] | None = None) -> Shares:
    """Three output shares of x AND y from three shares of x and of y.

    Component i does not read share i of x or y (non-completeness). If r
    is given, the bits (r1, r2, r1 xor r2) are added to make the output
    sharing uniform. Cost: Theta(1); 9 AND gates and 2 random bits.
    """
    x1, x2, x3 = x
    y1, y2, y3 = y
    z1 = (x2 & y2) ^ (x2 & y3) ^ (x3 & y2)  # @line L1
    z2 = (x3 & y3) ^ (x1 & y3) ^ (x3 & y1)  # @line L2
    z3 = (x1 & y1) ^ (x1 & y2) ^ (x2 & y1)  # @line L3
    if r is not None:  # @line L4
        z1, z2, z3 = z1 ^ r[0], z2 ^ r[1], z3 ^ r[0] ^ r[1]
    out = (z1, z2, z3)  # @line L5
    return out  # @line L6


def component_inputs(x: Shares, y: Shares, r: tuple[int, int] | None = None) -> list[tuple[int, ...]]:
    """What a glitch-extended probe on each output share of ti_and can see."""
    x1, x2, x3 = x
    y1, y2, y3 = y
    rr = () if r is None else r
    return [
        (x2, x3, y2, y3) + rr[:1],
        (x1, x3, y1, y3) + rr[1:2],
        (x1, x2, y1, y2) + rr,
    ]


def two_share_and(a: Shares, b: Shares, r: int) -> tuple[Shares, list[tuple[int, ...]]]:
    """A first-order AND with two shares and one random bit, computed without a register.

    It is correct, and each output share alone is uniform, but each
    component reads both shares of b, so a glitch can combine them.
    Returns the output shares and the inputs of each component.
    """
    a1, a2 = a
    b1, b2 = b
    c1 = (a1 & b1) ^ (a1 & b2) ^ r
    c2 = (a2 & b1) ^ (a2 & b2) ^ r
    return (c1, c2), [(a1, b1, b2, r), (a2, b1, b2, r)]


def masked_and(rng: random.Random, x: int, y: int) -> Shares:
    """Share the bits x and y uniformly, apply ti_and with fresh bits, and return the shares."""
    def share(v: int) -> Shares:
        s1, s2 = rng.randrange(2), rng.randrange(2)
        return (s1, s2, v ^ s1 ^ s2)

    return ti_and(share(x), share(y), (rng.randrange(2), rng.randrange(2)))
