# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sequential-posted-pricing/. The authors are listed in prov/MES401.jsonl.

"""Sequential posted pricing for one item, with prices from the ex ante relaxation.

A distribution is a list of (value, probability) pairs with distinct values and positive
probabilities that sum to 1, as ints or Fractions. Every computation is exact.

The plan solves the ex ante relaxation: maximize the sum of the concave hulls of the bidders'
revenue curves subject to a total sale probability of at most 1. Each bidder then gets a price
lottery whose sale probability and expected revenue match its share of the relaxation. The
mechanism draws all prices, offers them in decreasing order, and sells to the first bidder who
accepts. Its expected revenue is at least 1 - (1 - 1/n)^n >= 1 - 1/e times the relaxation, which
is at least the optimal revenue.
"""

from fractions import Fraction
from itertools import product
from typing import Sequence

Dist = Sequence[tuple]
NO_OFFER = None  # a price of "infinity": the bidder is not offered the item


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


def hull_vertices(dist: Dist):
    """Return the vertices (q, revenue, price) of the concave hull of the revenue curve.

    The first vertex is (0, 0, NO_OFFER). A vertex with price s has q = Pr[v >= s].
    """
    values, probs = normalize(dist)
    pts = [(Fraction(0), Fraction(0), NO_OFFER)]
    q = Fraction(0)
    for s, f in zip(reversed(values), reversed(probs)):
        q += f
        pts.append((q, s * q, s))
    hull = []
    for p in pts:
        while len(hull) >= 2:
            (x1, y1, _), (x2, y2, _) = hull[-2], hull[-1]
            if (y2 - y1) * (p[0] - x1) <= (p[1] - y1) * (x2 - x1):
                hull.pop()
            else:
                break
        hull.append(p)
    return hull


def sale_probability(dist: Dist, price) -> Fraction:
    """Return Pr[v >= price], or 0 for NO_OFFER."""
    if price is NO_OFFER:
        return Fraction(0)
    return sum((Fraction(p) for v, p in dist if Fraction(v) >= price), Fraction(0))


def plan(dists: Sequence[Dist]):
    """Solve the ex ante relaxation and return (relaxation value, lotteries).

    lotteries[i] is a list of (price, probability) pairs; the price may be NO_OFFER.
    """
    hulls = [hull_vertices(d) for d in dists]  # @line L1
    segments = []
    for i, h in enumerate(hulls):
        for k in range(1, len(h)):
            dq, dr = h[k][0] - h[k - 1][0], h[k][1] - h[k - 1][1]
            if dr > 0:
                segments.append((dr / dq, i, k))
    segments.sort(key=lambda t: (-t[0], t[1], t[2]))  # @line L2
    cap = Fraction(1)
    q = [Fraction(0)] * len(dists)
    value = Fraction(0)
    for slope, i, k in segments:  # @line L3
        if cap == 0:
            break
        h = hulls[i]
        take = min(cap, h[k][0] - h[k - 1][0])  # @line L4
        q[i] += take
        value += slope * take
        cap -= take
    lotteries = []
    for i, h in enumerate(hulls):  # @line L5
        k = next(k for k in range(len(h)) if h[k][0] >= q[i])
        if h[k][0] == q[i]:
            lotteries.append([(h[k][2], Fraction(1))])
        else:
            # q[i] lies strictly inside the segment from vertex k - 1 to vertex k
            lam = (h[k][0] - q[i]) / (h[k][0] - h[k - 1][0])
            lotteries.append([(h[k - 1][2], lam), (h[k][2], 1 - lam)])
    return value, lotteries


def offer_order(prices):
    """Return the bidders in decreasing order of price (lower index first on ties), skipping NO_OFFER."""
    live = [i for i, p in enumerate(prices) if p is not NO_OFFER]
    return sorted(live, key=lambda i: (-prices[i], i))


def run(prices, values):
    """Offer the posted prices in decreasing order. Return (buyer, price), or (None, 0)."""
    for i in offer_order(prices):  # @line L7
        if Fraction(values[i]) >= prices[i]:  # @line L8
            return i, prices[i]
    return None, Fraction(0)  # @line L9


def draw_prices(lotteries, rng):
    """Draw one price per bidder from its lottery with a random.Random instance."""
    prices = []
    for lot in lotteries:  # @line L6
        u = Fraction(rng.random())
        acc = Fraction(0)
        chosen = lot[-1][0]
        for price, prob in lot:
            acc += prob
            if u < acc:
                chosen = price
                break
        prices.append(chosen)
    return prices


def expected_revenue(dists: Sequence[Dist], lotteries) -> Fraction:
    """Return the exact expected revenue of the sequential posted pricing with these lotteries."""
    total = Fraction(0)
    for combo in product(*lotteries):
        weight = Fraction(1)
        for _, prob in combo:
            weight *= prob
        prices = [price for price, _ in combo]
        unsold = Fraction(1)
        for i in offer_order(prices):
            a = sale_probability(dists[i], prices[i])
            total += weight * unsold * a * prices[i]
            unsold *= 1 - a
    return total


def sequential_posted_pricing(dists: Sequence[Dist], values, rng):
    """Plan, draw the prices and run the mechanism once. Return (buyer, price)."""
    _, lotteries = plan(dists)
    return run(draw_prices(lotteries, rng), values)
