# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simultaneous-ascending-auction/. The authors are listed in prov/427AF8.jsonl.

import itertools
import random
from fractions import Fraction

from simultaneous_ascending_auction import all_bundles, demand, simultaneous_ascending_auction


def table(m, f):
    """Freeze a valuation into a dict so that it is cheap to call."""
    values = {s: f(s) for s in all_bundles(m)}
    return values.__getitem__


def unit_demand(w):
    return lambda s: max((w[j] for j in s), default=0)


def additive(w):
    return lambda s: sum(w[j] for j in s)


def oxs(rows):
    """Assign the items of s to distinct slots; each slot holds one item.
    These valuations (OXS) satisfy gross substitutes."""

    def v(s):
        items = sorted(s)
        best = 0
        for slots in itertools.product(range(len(rows) + 1), repeat=len(items)):
            used = [t for t in slots if t < len(rows)]
            if len(used) == len(set(used)):
                best = max(best, sum(rows[t][j] for t, j in zip(slots, items) if t < len(rows)))
        return best

    return v


def optimum(valuations, m):
    best = 0
    for owner in itertools.product(range(len(valuations) + 1), repeat=m):
        total = 0
        for i, v in enumerate(valuations):
            total += v(frozenset(j for j in range(m) if owner[j] == i))
        best = max(best, total)
    return best


def welfare(valuations, held):
    return sum(v(s) for v, s in zip(valuations, held))


def test_unit_demand_example() -> None:
    v1, v2 = unit_demand([5, 4]), unit_demand([3, 4])
    held, prices, rounds = simultaneous_ascending_auction([v1, v2], 2, 1)
    assert held == [frozenset({0}), frozenset({1})]
    assert prices == [1, 1] and rounds == 2


def test_exposure_example() -> None:
    # Bidder 0 wants items 0 and 1 together (value 10); bidder 1 wants item 0
    # (value 9) and bidder 2 wants item 1 (value 3).
    v = [lambda s: 10 if s >= {0, 1} else 0, lambda s: 9 if 0 in s else 0, lambda s: 3 if 1 in s else 0]
    held, prices, rounds = simultaneous_ascending_auction(v, 2, 1)
    assert held == [frozenset({1}), frozenset({0}), frozenset()]
    assert prices == [8, 3] and rounds == 9
    # Bidder 0 is stuck with item 1 at price 3 and value 0.
    assert v[0](held[0]) - prices[1] == -3
    assert welfare(v, held) == 9 and optimum(v, 2) == 12


def test_edges() -> None:
    assert simultaneous_ascending_auction([], 2, 1) == ([], [0, 0], 1)
    assert simultaneous_ascending_auction([additive([3])], 1, 1) == ([frozenset({0})], [1], 2)
    assert simultaneous_ascending_auction([additive([0, 0])], 2, 1) == ([frozenset()], [0, 0], 1)
    try:
        simultaneous_ascending_auction([additive([1])], 1, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("epsilon must be positive")


def random_gross_substitutes(rng, m):
    kind = rng.randrange(3)
    if kind == 0:
        return unit_demand([rng.randrange(0, 9) for _ in range(m)])
    if kind == 1:
        return additive([rng.randrange(0, 9) for _ in range(m)])
    return oxs([[rng.randrange(0, 9) for _ in range(m)] for _ in range(2)])


def test_gross_substitutes_end_in_near_equilibrium() -> None:
    rng = random.Random(1)
    bundles = {m: all_bundles(m) for m in (1, 2, 3)}
    for trial in range(120):
        m, n = rng.randrange(1, 4), rng.randrange(1, 4)
        epsilon = Fraction(1, rng.choice([1, 2, 3]))
        valuations = [table(m, random_gross_substitutes(rng, m)) for _ in range(n)]
        held, prices, rounds = simultaneous_ascending_auction(valuations, m, epsilon)
        top = max(v(frozenset(range(m))) for v in valuations)
        assert rounds <= m * top / epsilon + 1
        sold = set().union(*held)
        assert all(prices[j] == 0 for j in range(m) if j not in sold)
        for i, v in enumerate(valuations):
            personal = [prices[j] if j in held[i] else prices[j] + epsilon for j in range(m)]
            best = demand(v, personal, bundles[m], held[i])
            # Each bidder demands exactly what it holds at its personal prices.
            assert best == held[i]
            assert v(held[i]) - sum(prices[j] for j in held[i]) >= 0
        assert welfare(valuations, held) >= optimum(valuations, m) - m * epsilon


def test_small_increment_gets_close_to_optimum() -> None:
    rng = random.Random(2)
    for _ in range(20):
        valuations = [table(2, random_gross_substitutes(rng, 2)) for _ in range(3)]
        held, _, _ = simultaneous_ascending_auction(valuations, 2, Fraction(1, 10))
        assert welfare(valuations, held) >= optimum(valuations, 2) - Fraction(2, 10)
