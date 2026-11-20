# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/all-pay-auction/. The authors are listed in prov/HC5JY0.jsonl.

import random
from fractions import Fraction

from all_pay_auction import all_pay_auction, equilibrium_bid, interim_utility


def test_example() -> None:
    assert all_pay_auction([10, 7, 3]) == (0, [10, 7, 3])
    assert all_pay_auction([3, 7, 10]) == (2, [3, 7, 10])


def test_edges() -> None:
    assert all_pay_auction([]) == (None, [])
    assert all_pay_auction([5]) == (0, [5])
    assert all_pay_auction([7, 7, 3]) == (0, [7, 7, 3])
    assert all_pay_auction([3, 7, 7]) == (1, [3, 7, 7])
    assert all_pay_auction([0, 0]) == (0, [0, 0])


def test_against_reference() -> None:
    rng = random.Random(1)
    for _ in range(2000):
        bids = [rng.randrange(0, 6) for _ in range(rng.randrange(1, 7))]
        top = max(bids)
        assert all_pay_auction(bids) == (bids.index(top), bids)


def test_equilibrium_values() -> None:
    assert equilibrium_bid(Fraction(1, 2), 2) == Fraction(1, 8)
    assert equilibrium_bid(Fraction(1), 3) == Fraction(2, 3)
    # Two bidders: the bid v^2/2 is the expected Vickrey payment of type v.
    for k in range(11):
        v = Fraction(k, 10)
        assert equilibrium_bid(v, 2) == v * v / 2


def test_equilibrium_is_best_response() -> None:
    # Bids above equilibrium_bid(1) win for sure and cost more than equilibrium_bid(1),
    # so every relevant bid is equilibrium_bid(t) for some t in [0, 1].
    grid = [Fraction(k, 60) for k in range(61)]
    for n in (2, 3, 4):
        for v in [Fraction(k, 12) for k in range(13)]:
            best = interim_utility(v, v, n)
            assert best >= 0
            for t in grid:
                if t != v:
                    assert interim_utility(v, t, n) < best


def test_expected_utility_by_simulation() -> None:
    rng = random.Random(2)
    n, v, t = 3, Fraction(3, 4), Fraction(9, 10)
    trials, total = 20000, 0.0
    b0 = float(equilibrium_bid(t, n))
    for _ in range(trials):
        bids = [b0] + [float(equilibrium_bid(Fraction(rng.random()), n)) for _ in range(n - 1)]
        w, pay = all_pay_auction(bids)
        total += (float(v) if w == 0 else 0.0) - pay[0]
    # Utilities lie in [-1, 1]; Hoeffding gives deviation above 0.03 with probability below 1e-3.
    assert abs(total / trials - float(interim_utility(v, t, n))) < 0.03


def test_revenue_uniform() -> None:
    rng = random.Random(3)
    for n in (2, 3):
        trials, total = 20000, 0.0
        for _ in range(trials):
            bids = [(n - 1) * rng.random() ** n / n for _ in range(n)]
            _, pay = all_pay_auction(bids)
            total += sum(pay)
        # Revenue is in [0, n - 1]; with n <= 3 Hoeffding gives deviation above 0.03 with
        # probability at most 2 exp(-2 * 20000 * 0.03^2 / 4) < 1e-3.
        assert abs(total / trials - (n - 1) / (n + 1)) < 0.03


def test_complete_information_equilibrium() -> None:
    # Values v1 >= v2 known to both. Bidder 1 bids uniform on [0, v2]; bidder 2 bids 0
    # with probability 1 - v2/v1 and otherwise uniform on [0, v2].
    for v1, v2 in [(Fraction(10), Fraction(6)), (Fraction(5), Fraction(5)), (Fraction(3), Fraction(1, 2))]:
        def cdf1(b):
            return min(b / v2, Fraction(1))

        def cdf2(b):
            return min(1 - v2 / v1 + b / v1, Fraction(1))

        grid = [v2 * Fraction(k, 20) for k in range(1, 31)]
        for b in grid:
            u1 = v1 * cdf2(b) - b
            u2 = v2 * cdf1(b) - b
            if b <= v2:
                assert u1 == v1 - v2
                assert u2 == 0
            else:
                assert u1 < v1 - v2
                assert u2 < 0
