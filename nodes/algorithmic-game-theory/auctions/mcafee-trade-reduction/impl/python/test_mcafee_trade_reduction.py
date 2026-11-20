# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mcafee-trade-reduction/. The authors are listed in prov/AMA27A.jsonl.

import itertools
import random
from fractions import Fraction

from mcafee_trade_reduction import buyer_utility, mcafee_trade_reduction, seller_utility


def optimal_gain(bids, asks):
    """Largest gain from trade, by brute force over equal-size sets of traders."""
    best = 0
    for t in range(min(len(bids), len(asks)) + 1):
        for bs in itertools.combinations(range(len(bids)), t):
            for ss in itertools.combinations(range(len(asks)), t):
                best = max(best, sum(bids[i] for i in bs) - sum(asks[j] for j in ss))
    return best


def gain(bids, asks):
    buyers, sellers, _, _ = mcafee_trade_reduction(bids, asks)
    return sum(bids[i] for i in buyers) - sum(asks[j] for j in sellers)


def test_example() -> None:
    # k = 2 and p0 = (2 + 9) / 2 = 11/2 lies in [3, 8]: both pairs trade.
    assert mcafee_trade_reduction([10, 8, 2], [1, 3, 9]) == ([0, 1], [0, 1], Fraction(11, 2), Fraction(11, 2))
    # k = 2 and p0 = (4 + 9) / 2 = 13/2 is not in [3, 5]: one pair trades.
    assert mcafee_trade_reduction([10, 4, 5], [9, 1, 3]) == ([0], [1], 5, 3)
    # Without a third trader on a side the reduction branch is used.
    assert mcafee_trade_reduction([10, 8], [1, 3, 9]) == ([0], [0], 8, 3)


def test_edges() -> None:
    assert mcafee_trade_reduction([], []) == ([], [], 0, 0)
    assert mcafee_trade_reduction([5], []) == ([], [], 0, 0)
    assert mcafee_trade_reduction([2], [3]) == ([], [], 0, 0)
    assert mcafee_trade_reduction([5], [1]) == ([], [], 5, 1)
    assert mcafee_trade_reduction([4, 4], [4, 4]) == ([0], [0], 4, 4)
    assert mcafee_trade_reduction([4, 4, 4], [4, 4, 4]) == ([0, 1], [0, 1], 4, 4)
    assert mcafee_trade_reduction([10, 5, 6], [7, 1, 3]) == ([0, 2], [1, 2], 6, 6)
    assert mcafee_trade_reduction([6, 6, 1], [1, 2, 5]) == ([0, 1], [0, 1], 3, 3)


def test_budget_balance_and_trade_loss() -> None:
    rng = random.Random(1)
    for _ in range(3000):
        bids = [rng.randrange(0, 10) for _ in range(rng.randrange(0, 5))]
        asks = [rng.randrange(0, 10) for _ in range(rng.randrange(0, 5))]
        buyers, sellers, pb, ps = mcafee_trade_reduction(bids, asks)
        assert len(buyers) == len(sellers)
        assert pb >= ps
        assert all(bids[i] >= pb for i in buyers)
        assert all(asks[j] <= ps for j in sellers)
        b = sorted(bids, reverse=True)
        s = sorted(asks)
        k = sum(1 for t in range(min(len(b), len(s))) if b[t] >= s[t])
        opt = optimal_gain(bids, asks)
        assert opt == sum(b[t] - s[t] for t in range(k))
        assert len(buyers) in (k, max(k - 1, 0))
        g = gain(bids, asks)
        assert g >= opt - (b[k - 1] - s[k - 1] if k else 0)
        assert k * g >= (k - 1) * opt


def test_truthful_is_dominant() -> None:
    for nb, ns, top in ((1, 2, 5), (2, 1, 5), (2, 2, 5), (3, 2, 4), (2, 3, 4), (3, 3, 3)):
        grid = range(0, top)
        for bids in itertools.product(grid, repeat=nb):
            for asks in itertools.product(grid, repeat=ns):
                bids, asks = list(bids), list(asks)
                for i in range(nb):
                    u_true = buyer_utility(bids[i], bids, asks, i)
                    assert u_true >= 0
                    for lie in grid:
                        other = bids[:i] + [lie] + bids[i + 1:]
                        assert u_true >= buyer_utility(bids[i], other, asks, i)
                for j in range(ns):
                    u_true = seller_utility(asks[j], bids, asks, j)
                    assert u_true >= 0
                    for lie in grid:
                        other = asks[:j] + [lie] + asks[j + 1:]
                        assert u_true >= seller_utility(asks[j], bids, other, j)


INF = float("inf")


def buyer_threshold(others, asks):
    """The critical bid of a new buyer, by the case analysis of the proof."""
    c = [INF] + sorted(others, reverse=True)
    s = [None] + sorted(asks)

    def cc(t):
        return c[t] if t < len(c) else None

    def ss(t):
        return s[t] if t < len(s) else None

    h = 0
    while cc(h + 1) is not None and ss(h + 1) is not None and c[h + 1] >= s[h + 1]:
        h += 1
    if ss(1) is None:
        return INF
    if ss(h + 1) is not None and c[h] >= s[h + 1]:
        if cc(h + 1) is not None and ss(h + 2) is not None:
            p = Fraction(c[h + 1] + s[h + 2], 2)
            if s[h + 1] <= p <= c[h]:
                return p
        return c[h]
    if ss(h + 1) is not None:
        p = Fraction(c[h] + s[h + 1], 2)
        if c[h - 1] >= p:
            return p
    return c[h - 1]


def test_buyer_threshold() -> None:
    rng = random.Random(3)
    grid = [Fraction(t, 2) for t in range(0, 17)]
    for _ in range(400):
        others = [rng.randrange(0, 8) for _ in range(rng.randrange(0, 4))]
        asks = [rng.randrange(0, 8) for _ in range(rng.randrange(0, 4))]
        theta = buyer_threshold(others, asks)
        for b in grid:
            bids = others + [b]
            buyers, _, price, _ = mcafee_trade_reduction(bids, asks)
            i = len(others)
            if b > theta:
                assert i in buyers and price == theta
            elif b < theta:
                assert i not in buyers
            elif i in buyers:
                assert price == theta


def test_truthful_with_half_steps() -> None:
    # The price p0 can be a half integer, so test lies on a finer grid too.
    rng = random.Random(2)
    grid = [Fraction(t, 2) for t in range(0, 13)]
    for _ in range(300):
        bids = [rng.choice(grid) for _ in range(3)]
        asks = [rng.choice(grid) for _ in range(3)]
        for i in range(3):
            u_true = buyer_utility(bids[i], bids, asks, i)
            for lie in grid:
                assert u_true >= buyer_utility(bids[i], bids[:i] + [lie] + bids[i + 1:], asks, i)
        for j in range(3):
            u_true = seller_utility(asks[j], bids, asks, j)
            for lie in grid:
                assert u_true >= seller_utility(asks[j], bids, asks[:j] + [lie] + asks[j + 1:], j)
