# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prophet-inequality/. The authors are listed in prov/WRNK0C.jsonl.

import itertools
import random
from fractions import Fraction as F

from prophet_inequality import (
    expected_max,
    guarantee,
    half_mean_threshold,
    optimal_value,
    stop_probability,
    threshold_value,
)

EXAMPLE = [
    [(F(0), F(1, 2)), (F(4), F(1, 2))],
    [(F(1), F(2, 3)), (F(6), F(1, 3))],
    [(F(0), F(3, 4)), (F(12), F(1, 4))],
]


def outcomes(dists):
    for combo in itertools.product(*dists):
        prob = F(1)
        for _, p in combo:
            prob *= p
        yield [x for x, _ in combo], prob


def brute_max(dists):
    return sum((max(xs) * p for xs, p in outcomes(dists)), F(0))


def brute_threshold(dists, tau):
    total = F(0)
    for xs, p in outcomes(dists):
        total += p * next((x for x in xs if x >= tau), F(0))
    return total


def brute_optimal(dists):
    """Best rule of the form 'stop at X_i when X_i is in S_i', over all sets S_i."""
    best = F(0)
    choices = [list(itertools.product((False, True), repeat=len(d))) for d in dists]
    for rule in itertools.product(*choices):
        total = F(0)
        for combo in itertools.product(*[range(len(d)) for d in dists]):
            prob, gain = F(1), F(0)
            for i, k in enumerate(combo):
                prob *= dists[i][k][1]
            for i, k in enumerate(combo):
                if rule[i][k]:
                    gain = dists[i][k][0]
                    break
            total += prob * gain
        best = max(best, total)
    return best


def random_dist(rng, size):
    values = rng.sample(range(0, 20), size)
    weights = [rng.randrange(1, 6) for _ in range(size)]
    s = sum(weights)
    return [(F(v, rng.randrange(1, 4)), F(w, s)) for v, w in zip(values, weights)]


def test_worked_example():
    assert expected_max(EXAMPLE) == F(23, 4)
    assert optimal_value(EXAMPLE) == 4
    tau = half_mean_threshold(EXAMPLE)
    assert tau == F(23, 8)
    assert threshold_value(EXAMPLE, tau) == 4
    assert stop_probability(EXAMPLE, tau) == F(3, 4)
    assert stop_probability(EXAMPLE, F(6)) == F(1, 2)
    assert threshold_value(EXAMPLE, F(6)) == 4
    assert threshold_value(EXAMPLE, F(12)) == 3


def test_tight_example():
    for k in (2, 10, 100, 1000):
        eps = F(1, k)
        dists = [[(F(1), F(1))], [(F(0), 1 - eps), (1 / eps, eps)]]
        assert expected_max(dists) == 2 - eps
        assert optimal_value(dists) == 1
        assert threshold_value(dists, half_mean_threshold(dists)) == 1
        assert optimal_value(dists) / expected_max(dists) == 1 / (2 - eps)


def test_random_instances_against_brute_force():
    rng = random.Random(2012)
    for trial in range(600):
        n = rng.randrange(1, 4)
        dists = [random_dist(rng, rng.randrange(1, 4)) for _ in range(n)]
        emax = expected_max(dists)
        assert emax == brute_max(dists)
        opt = optimal_value(dists)
        assert opt <= emax
        tau = half_mean_threshold(dists)
        kw = threshold_value(dists, tau)
        assert kw == brute_threshold(dists, tau)
        assert 2 * kw >= emax
        assert kw <= opt
        cuts = {x for d in dists for x, _ in d} | {tau, F(0), emax}
        for t in cuts:
            v = threshold_value(dists, t)
            assert v == brute_threshold(dists, t)
            assert v >= guarantee(dists, t)
            assert v <= opt
            if stop_probability(dists, t) == F(1, 2):
                assert 2 * v >= emax
        if trial < 150:
            assert opt == brute_optimal(dists)


def test_order_does_not_matter_for_the_bound():
    rng = random.Random(5)
    for _ in range(200):
        dists = [random_dist(rng, rng.randrange(1, 4)) for _ in range(rng.randrange(2, 5))]
        for order in (dists, dists[::-1]):
            assert 2 * threshold_value(order, half_mean_threshold(order)) >= expected_max(order)


def test_monte_carlo():
    rng = random.Random(9)
    trials, total = 40000, 0.0
    tau = half_mean_threshold(EXAMPLE)
    for _ in range(trials):
        for d in EXAMPLE:
            x = rng.choices([x for x, _ in d], [float(p) for _, p in d])[0]
            if x >= tau:
                total += float(x)
                break
    assert abs(total / trials - 4.0) < 0.1
