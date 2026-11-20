# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/uniform-price-auction/. The authors are listed in prov/6TRC5Q.jsonl.

import itertools
import random
from fractions import Fraction

from uniform_price_auction import (
    HIGHEST_LOSING,
    LOWEST_WINNING,
    uniform_price_auction,
    utility,
)


def nonincreasing_vectors(grid, length):
    for v in itertools.product(grid, repeat=length):
        if all(v[j] >= v[j + 1] for j in range(length - 1)):
            yield list(v)


def best_total(bids, k):
    """Largest sum of accepted bids, by brute force over unit counts."""
    best = 0
    for counts in itertools.product(*[range(len(row) + 1) for row in bids]):
        if sum(counts) <= k:
            best = max(best, sum(sum(row[:c]) for row, c in zip(bids, counts)))
    return best


def test_example() -> None:
    bids = [[10, 10], [6]]
    assert uniform_price_auction(bids, 2) == ([2, 0], 6, [12, 0])
    assert uniform_price_auction(bids, 2, LOWEST_WINNING) == ([2, 0], 10, [20, 0])
    assert uniform_price_auction([[10, 0], [6]], 2) == ([1, 1], 0, [0, 0])
    assert uniform_price_auction([[7], [5], [3], [3]], 2) == ([1, 1, 0, 0], 3, [3, 3, 0, 0])


def test_edges() -> None:
    assert uniform_price_auction([], 3) == ([], 0, [])
    assert uniform_price_auction([[4]], 0) == ([0], 4, [0])
    assert uniform_price_auction([[4]], 0, LOWEST_WINNING) == ([0], 0, [0])
    assert uniform_price_auction([[4, 1]], 5) == ([2], 0, [0])
    assert uniform_price_auction([[4, 1]], 5, LOWEST_WINNING) == ([2], 1, [2])
    assert uniform_price_auction([[5], [5], [5]], 2) == ([1, 1, 0], 5, [5, 5, 0])
    half = Fraction(1, 2)
    assert uniform_price_auction([[half], [Fraction(1, 3)]], 1) == ([1, 0], Fraction(1, 3), [Fraction(1, 3), 0])
    try:
        uniform_price_auction([[1, 2]], 1)
    except ValueError:
        pass
    else:
        raise AssertionError("an increasing bid list must be rejected")


def test_allocation_and_clearing_price() -> None:
    rng = random.Random(1)
    for _ in range(1500):
        n = rng.randrange(0, 4)
        bids = [sorted((rng.randrange(0, 8) for _ in range(rng.randrange(0, 4))), reverse=True) for _ in range(n)]
        k = rng.randrange(0, 6)
        for rule in (HIGHEST_LOSING, LOWEST_WINNING):
            units, price, payments = uniform_price_auction(bids, k, rule)
            total = sum(len(row) for row in bids)
            assert sum(units) == min(k, total)
            assert sum(sum(row[:u]) for row, u in zip(bids, units)) == best_total(bids, k)
            assert payments == [u * price for u in units]
            # Every winning bid is at least the price, and every losing bid is
            # at most the price (when a unit is sold or the rule uses losers).
            for row, u in zip(bids, units):
                assert all(b >= price for b in row[:u])
                if rule == HIGHEST_LOSING or sum(units) > 0:
                    assert all(b <= price for b in row[u:])


def test_unit_demand_truthful_is_dominant() -> None:
    grid = range(0, 5)
    for k in (1, 2):
        for others in itertools.product(grid, repeat=2):
            for i in range(3):
                for value in grid:
                    truthful = [[b] for b in others[:i]] + [[value]] + [[b] for b in others[i:]]
                    u_true = utility([value], truthful, i, k)
                    assert u_true >= 0
                    for lie in grid:
                        bids = [[b] for b in others[:i]] + [[lie]] + [[b] for b in others[i:]]
                        assert u_true >= utility([value], bids, i, k)


def test_lowest_winning_price_is_not_truthful() -> None:
    # One unit, values 5 and 3: the winner pays its own bid, so shading helps.
    assert utility([5], [[5], [3]], 0, 1, LOWEST_WINNING) == 0
    assert utility([5], [[4], [3]], 0, 1, LOWEST_WINNING) == 1


def test_demand_reduction() -> None:
    values_a, values_b = [10, 10], [6]
    truthful = utility(values_a, [values_a, values_b], 0, 2)
    reduced = utility(values_a, [[10, 0], values_b], 0, 2)
    assert (truthful, reduced) == (8, 10)
    # The reduced profile is a Nash equilibrium over a grid of bids.
    grid = range(0, 13)
    profile = [[10, 0], [6]]
    u_a = utility(values_a, profile, 0, 2)
    u_b = utility(values_b, profile, 1, 2)
    for lie in nonincreasing_vectors(grid, 2):
        assert utility(values_a, [lie, [6]], 0, 2) <= u_a
    for lie in grid:
        assert utility(values_b, [[10, 0], [lie]], 1, 2) <= u_b
    # The equilibrium allocation is not efficient: welfare 16 against 20.
    units, _, _ = uniform_price_auction(profile, 2)
    welfare = sum(values_a[:units[0]]) + sum(values_b[:units[1]])
    assert (welfare, best_total([values_a, values_b], 2)) == (16, 20)


def test_multi_unit_bidders_gain_only_by_lowering_bids() -> None:
    # With two units of demand, a profitable lie exists in some profiles, and
    # in each profile some best lie bids no more than the value on each unit.
    grid = range(0, 5)
    found = False
    for values in nonincreasing_vectors(grid, 2):
        for other in nonincreasing_vectors(grid, 2):
            for k in (1, 2, 3):
                u_true = utility(values, [values, other], 0, k)
                best = max(utility(values, [lie, other], 0, k) for lie in nonincreasing_vectors(grid, 2))
                shaded = max(
                    utility(values, [lie, other], 0, k)
                    for lie in nonincreasing_vectors(grid, 2)
                    if lie[0] <= values[0] and lie[1] <= values[1]
                )
                assert shaded == best
                found = found or best > u_true
    assert found
