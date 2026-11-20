# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/myerson-optimal-auction/. The authors are listed in prov/VMDH3M.jsonl.

"""Myerson's revenue-optimal auction for one item and independent private values.

A distribution is a list of (value, probability) pairs with distinct values and positive
probabilities that sum to 1. Values and probabilities are ints or Fractions, and every
computation is exact. Bidder i reports a value in the support of its own distribution.

The virtual value of a support point is the slope of the revenue curve R(q) = q * F^{-1}(1 - q)
in quantile space. The ironed virtual value is the slope of its concave hull. The auction gives
the item to the bidder with the largest nonnegative ironed virtual value (the lowest index on
ties) and charges the winner the smallest value in its support with which it still wins.
"""

from fractions import Fraction
from itertools import product
from typing import Callable, Sequence

Dist = Sequence[tuple]


def normalize(dist: Dist):
    """Return (values, probs) sorted by value, as Fractions, after checking the input."""
    pairs = sorted((Fraction(v), Fraction(p)) for v, p in dist)
    values = [v for v, _ in pairs]
    probs = [p for _, p in pairs]
    if not pairs or len(set(values)) != len(values):
        raise ValueError("the support must be nonempty with distinct values")
    if any(p <= 0 for p in probs) or sum(probs) != 1:
        raise ValueError("the probabilities must be positive and sum to 1")
    return values, probs


def revenue_curve(values, probs):
    """Return the points (q, R) of the revenue curve, from (0, 0) up to q = 1.

    Point j (j >= 1) belongs to the j-th highest value s, with q = Pr[v >= s] and R = s * q.
    """
    pts = [(Fraction(0), Fraction(0))]
    q = Fraction(0)
    for s, f in zip(reversed(values), reversed(probs)):
        q += f
        pts.append((q, s * q))
    return pts


def upper_hull(pts):
    """Return the indices of the vertices of the concave (upper) hull of points sorted by q."""
    hull = []
    for k, (x, y) in enumerate(pts):
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = pts[hull[-2]], pts[hull[-1]]
            # drop the middle point if it lies on or below the chord from hull[-2] to k
            if (y2 - y1) * (x - x1) <= (y - y1) * (x2 - x1):
                hull.pop()
            else:
                break
        hull.append(k)
    return hull


def virtual_values(dist: Dist):
    """Return the discrete virtual values phi(s_1), ..., phi(s_K) in increasing order of value."""
    values, probs = normalize(dist)
    pts = revenue_curve(values, probs)
    K = len(values)
    # the segment from point j - 1 to point j belongs to value index K - j
    slopes = [(pts[j][1] - pts[j - 1][1]) / (pts[j][0] - pts[j - 1][0]) for j in range(1, K + 1)]
    return list(reversed(slopes))


def ironed_virtual_values(dist: Dist):
    """Return the ironed virtual values in increasing order of value: slopes of the concave hull."""
    values, probs = normalize(dist)
    pts = revenue_curve(values, probs)
    K = len(values)
    hull = upper_hull(pts)
    slope = [None] * (K + 1)
    for a, b in zip(hull, hull[1:]):
        m = (pts[b][1] - pts[a][1]) / (pts[b][0] - pts[a][0])
        for j in range(a + 1, b + 1):
            slope[j] = m
    return list(reversed(slope[1:]))


class Auction:
    """Myerson's auction for a fixed list of bidder distributions."""

    def __init__(self, dists: Sequence[Dist]):
        if not dists:
            raise ValueError("there must be at least one bidder")
        self.supports = []
        self.ironed = []
        for d in dists:
            values, _ = normalize(d)
            self.supports.append(values)
            self.ironed.append(dict(zip(values, ironed_virtual_values(d))))  # @line L1

    def wins(self, i: int, c: Sequence[Fraction], ci: Fraction) -> bool:
        """True if bidder i wins with ironed virtual value ci against the others' values c."""
        if ci < 0:
            return False
        for j, cj in enumerate(c):
            if j == i or cj < 0:
                continue
            if cj > ci or (cj == ci and j < i):
                return False
        return True

    def run(self, bids: Sequence):
        """Return (winner, payments). The winner is None if the item is not sold."""
        n = len(self.supports)
        if len(bids) != n:
            raise ValueError("one bid per bidder is needed")
        bids = [Fraction(b) for b in bids]
        for i, b in enumerate(bids):
            if b not in self.ironed[i]:
                raise ValueError("a bid must lie in the bidder's support")
        c = [self.ironed[i][b] for i, b in enumerate(bids)]  # @line L2
        payments = [Fraction(0)] * n
        candidates = [i for i in range(n) if c[i] >= 0]  # @line L3
        if not candidates:
            return None, payments
        top = max(c[i] for i in candidates)
        w = min(i for i in candidates if c[i] == top)  # @line L4
        for s in self.supports[w]:  # @line L5
            if self.wins(w, c, self.ironed[w][s]):
                payments[w] = s
                break
        return w, payments  # @line L6


def myerson(dists: Sequence[Dist], bids: Sequence):
    """Run Myerson's auction once. Return (winner, payments)."""
    return Auction(dists).run(bids)


def profiles(dists: Sequence[Dist]):
    """Yield (bids, probability) over all value profiles of independent bidders."""
    supports = [list(zip(*normalize(d))) for d in dists]
    for combo in product(*supports):
        p = Fraction(1)
        for _, f in combo:
            p *= f
        yield [v for v, _ in combo], p


def expected_revenue(dists: Sequence[Dist]) -> Fraction:
    """Return the exact expected revenue of Myerson's auction, by enumeration of all profiles."""
    auction = Auction(dists)
    total = Fraction(0)
    for bids, p in profiles(dists):
        _, pay = auction.run(bids)
        total += p * sum(pay)
    return total


def expected_virtual_surplus(dists: Sequence[Dist]) -> Fraction:
    """Return E[max(0, max_i ironed phi_i(v_i))], the optimal revenue by Myerson's theorem."""
    ironed = [dict(zip(normalize(d)[0], ironed_virtual_values(d))) for d in dists]
    total = Fraction(0)
    for bids, p in profiles(dists):
        best = max([Fraction(0)] + [ironed[i][b] for i, b in enumerate(bids)])
        total += p * best
    return total


def myerson_regular(bids: Sequence, phis: Sequence[Callable], phi_invs: Sequence[Callable]):
    """Myerson's auction for regular continuous distributions.

    phis[i] is the virtual valuation of bidder i, a nondecreasing function, and phi_invs[i] is
    its inverse. The winner pays the smallest bid with which it still wins.
    """
    n = len(bids)
    c = [phis[i](bids[i]) for i in range(n)]
    payments = [0] * n
    candidates = [i for i in range(n) if c[i] >= 0]
    if not candidates:
        return None, payments
    top = max(c[i] for i in candidates)
    w = min(i for i in candidates if c[i] == top)
    rival = max([0] + [c[j] for j in range(n) if j != w])
    payments[w] = phi_invs[w](rival)
    return w, payments
