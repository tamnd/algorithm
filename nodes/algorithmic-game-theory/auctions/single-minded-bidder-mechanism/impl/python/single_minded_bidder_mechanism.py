# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/single-minded-bidder-mechanism/. The authors are listed in prov/Z6TN8C.jsonl.

from fractions import Fraction
from typing import Sequence, Union

Number = Union[int, Fraction]
Bid = tuple[frozenset, Number]
# A payment c * sqrt(r) is stored as the pair (c, r), with c a Fraction and r
# a square-free positive integer, so that every payment is exact.
Payment = tuple[Fraction, int]


def _order(bids: Sequence[Bid]) -> list[int]:
    """Bidders by v / sqrt(|S|), highest first, compared exactly as v^2 / |S|."""
    for bundle, value in bids:
        if not bundle:
            raise ValueError("every bundle must be nonempty")
        if value < 0:
            raise ValueError("values must be nonnegative")
    return sorted(range(len(bids)), key=lambda i: (-Fraction(bids[i][1]) ** 2 / len(bids[i][0]), i))


def _greedy(bids: Sequence[Bid], order: Sequence[int], skip: int = -1) -> list[int]:
    winners: list[int] = []
    used: set = set()
    for i in order:  # @line L3
        if i == skip:
            continue
        if used.isdisjoint(bids[i][0]):  # @line L4
            winners.append(i)  # @line L4
            used |= bids[i][0]  # @line L4
    return winners


def _surd(c: Fraction, r: int) -> Payment:
    """Write c * sqrt(r) with a square-free radicand."""
    f = 1
    d = 2
    while d * d <= r:
        while r % (d * d) == 0:
            r //= d * d
            f *= d
        d += 1
    return Fraction(c) * f, r


def single_minded_mechanism(bids: Sequence[Bid]) -> tuple[list[int], list[Payment]]:
    """The truthful greedy mechanism of Lehmann, O'Callaghan and Shoham.

    bids[i] = (S_i, v_i): bidder i asks for the nonempty bundle S_i (a
    frozenset of items) and reports the value v_i. Bidders are taken in the
    order of v_i / sqrt(|S_i|), highest first, ties to the smaller index, and
    a bidder wins if its bundle is disjoint from the bundles already won.
    A winner i pays v_j * sqrt(|S_i| / |S_j|), where j is the first bidder
    that wins in the same greedy run without i and whose bundle meets S_i,
    and 0 if there is no such j. Return (winners in greedy order, payments),
    with payments[i] = (c, r) meaning c * sqrt(r); losers pay (0, 1).
    """
    order = _order(bids)  # @line L1
    winners = _greedy(bids, order)  # @line L2
    payments: list[Payment] = [(Fraction(0), 1)] * len(bids)
    for i in winners:  # @line L5
        bundle = bids[i][0]
        blocker = None
        for j in _greedy(bids, order, skip=i):  # @line L6
            if not bundle.isdisjoint(bids[j][0]):  # @line L6
                blocker = j  # @line L6
                break
        if blocker is not None:  # @line L7
            size_j = len(bids[blocker][0])
            payments[i] = _surd(Fraction(bids[blocker][1]) / size_j, len(bundle) * size_j)  # @line L7
    return winners, payments  # @line L8


def payment_float(p: Payment) -> float:
    """The payment c * sqrt(r) as a float, for display only."""
    return float(p[0]) * p[1] ** 0.5


def sign_surd(a: Number, b: Number = 0, x: int = 0, c: Number = 0, y: int = 0) -> int:
    """Exact sign of a + b * sqrt(x) + c * sqrt(y) for rationals a, b, c and x, y >= 0."""

    def sgn(t) -> int:
        return (t > 0) - (t < 0)

    def two(a, b, x) -> int:
        # sign of a + b * sqrt(x)
        sa, sb = sgn(a), sgn(b) if x else 0
        if sb == 0 or sa == sb:
            return sa or sb
        if sa == 0:
            return sb
        d = sgn(a * a - b * b * x)
        return sa if d > 0 else (sb if d < 0 else 0)

    first = two(a, b, x)
    sc = sgn(c) if y else 0
    if sc == 0 or first == sc:
        return first or sc
    if first == 0:
        return sc
    # Signs differ: compare (a + b sqrt x)^2 with c^2 y.
    d = two(a * a + b * b * x - c * c * y, 2 * a * b, x)
    return first if d > 0 else (sc if d < 0 else 0)
