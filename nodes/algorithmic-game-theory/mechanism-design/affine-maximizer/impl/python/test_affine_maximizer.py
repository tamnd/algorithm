# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/affine-maximizer/. The authors are listed in prov/P44K0N.jsonl.

import random
from fractions import Fraction
from itertools import product

from affine_maximizer import affine_maximizer, utility

F = Fraction


def single_item(values, nobody="none"):
    """Bids for one item: outcome k means bidder k wins."""
    n = len(values)
    outcomes = list(range(n)) + [nobody]
    bids = [{o: (F(values[k]) if o == k else F(0)) for o in outcomes} for k in range(n)]
    return outcomes, bids


def test_weighted_example():
    outcomes, bids = single_item([10, 7])
    x, p = affine_maximizer(outcomes, bids, [1, 2])
    assert x == 1
    assert p == [F(0), F(5)]


def test_vickrey_with_reserve():
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randint(1, 4)
        values = [rng.randint(0, 20) for _ in range(n)]
        r = rng.randint(0, 20)
        outcomes, bids = single_item(values)
        x, p = affine_maximizer(outcomes, bids, [1] * n, {"none": r})
        top = max(values)
        if top >= r:
            w = values.index(top)
            assert x == w
            second = max([v for k, v in enumerate(values) if k != w], default=0)
            assert p[w] == max(second, r)
            assert all(p[k] == 0 for k in range(n) if k != w)
        else:
            assert x == "none"
            assert p == [0] * n


def test_unit_weights_give_clarke_payments():
    rng = random.Random(2)
    outcomes = ["a", "b", "c", "d"]
    for _ in range(100):
        n = rng.randint(1, 4)
        bids = [{o: F(rng.randint(0, 9)) for o in outcomes} for _ in range(n)]
        x, p = affine_maximizer(outcomes, bids, [1] * n)
        total = {o: sum(b[o] for b in bids) for o in outcomes}
        assert total[x] == max(total.values())
        for i in range(n):
            others_best = max(total[o] - bids[i][o] for o in outcomes)
            assert p[i] == others_best - (total[x] - bids[i][x])


def test_dsic_by_brute_force():
    rng = random.Random(3)
    outcomes = ["a", "b", "c"]
    grid = [dict(zip(outcomes, t)) for t in product([0, 1, 2], repeat=3)]
    for _ in range(25):
        n = rng.randint(2, 3)
        k = rng.randint(1, 3)
        rng_range = rng.sample(outcomes, k)
        weights = [F(rng.randint(1, 3), rng.randint(1, 2)) for _ in range(n)]
        constants = {o: F(rng.randint(-2, 2)) for o in outcomes}
        others = [rng.choice(grid) for _ in range(n)]
        for i in range(n):
            results = []
            for report in grid:
                bids = list(others)
                bids[i] = report
                x, p = affine_maximizer(rng_range, bids, weights, constants)
                results.append((x, p[i]))
            for t_index, true in enumerate(grid):
                honest = utility(true, *results[t_index])
                for x, pay in results:
                    assert honest >= utility(true, x, pay)


def test_individual_rationality_and_nonnegative_payments():
    rng = random.Random(4)
    outcomes = ["a", "b", "c", "d"]
    for _ in range(200):
        n = rng.randint(1, 4)
        k = rng.randint(1, 4)
        rng_range = rng.sample(outcomes, k)
        bids = [{o: F(rng.randint(0, 9)) for o in outcomes} for _ in range(n)]
        weights = [F(rng.randint(1, 4)) for _ in range(n)]
        constants = {o: F(rng.randint(-5, 5)) for o in outcomes}
        x, p = affine_maximizer(rng_range, bids, weights, constants)
        assert x in rng_range
        for i in range(n):
            assert p[i] >= 0
            assert utility(bids[i], x, p[i]) >= 0


def test_rejects_bad_input():
    outcomes, bids = single_item([3, 4])
    for weights in ([1, 0], [1, -1], [1]):
        try:
            affine_maximizer(outcomes, bids, weights)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    try:
        affine_maximizer([], bids, [1, 1])
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
