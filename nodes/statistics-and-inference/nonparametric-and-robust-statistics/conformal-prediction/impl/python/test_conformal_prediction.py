# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conformal-prediction/. The authors are listed in prov/83RAAM.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from conformal_prediction import (
    conformal_p_value,
    full_conformal_least_squares,
    full_conformal_set,
    in_set,
    least_squares_affine_residuals,
    least_squares_scores,
    level,
    mean_scores,
    nearest_neighbour_scores,
    smoothed_p_value,
)

ALPHAS = (Fraction(1, 20), Fraction(1, 10), Fraction(1, 5), Fraction(1, 4), Fraction(1, 2), Fraction(5, 6))


def exact_coverage(bag, scores, alpha):
    """P(Y_new is in the set) when the order of the bag is uniformly random: enumerate every
    ordering, use the first n points as data and the last one as the new point."""
    hits = total = 0
    for perm in itertools.permutations(bag):
        data, (x_new, y_new) = list(perm[:-1]), perm[-1]
        hits += bool(full_conformal_set(data, x_new, [y_new], scores, alpha))
        total += 1
    return Fraction(hits, total)


def exact_smoothed_coverage(bag, scores, alpha):
    """The same, for the smoothed p-value, averaged exactly over u uniform on [0, 1]."""
    total = Fraction(0)
    perms = list(itertools.permutations(bag))
    for perm in perms:
        r = scores(list(perm))
        greater = sum(1 for v in r if v > r[-1])
        equal = sum(1 for v in r if v == r[-1])
        # P(greater + u equal > alpha m) for u uniform on [0, 1]
        threshold = (alpha * len(r) - greater) / equal
        total += min(max(1 - threshold, Fraction(0)), Fraction(1))
    return total / len(perms)


BAG = [(Fraction(1), Fraction(3)), (Fraction(2), Fraction(7, 2)), (Fraction(3), Fraction(6)),
       (Fraction(4), Fraction(5)), (Fraction(5), Fraction(9)), (Fraction(6), Fraction(8))]


def test_exact_coverage_with_distinct_scores():
    r = least_squares_scores(BAG)
    assert len(set(r)) == len(r)
    m = len(BAG)
    for alpha in ALPHAS:
        # with distinct scores the coverage is exactly ceil((1 - alpha)(n + 1))/(n + 1)
        expected = Fraction(math.ceil((1 - alpha) * m), m)
        assert exact_coverage(BAG, least_squares_scores, alpha) == expected
        assert 1 - alpha <= expected < 1 - alpha + Fraction(1, m)


def test_ties_give_at_least_one_minus_alpha_and_smoothing_gives_exactly():
    # y values symmetric about their mean: the scores |y - mean| come in tied pairs
    bag = [(0, Fraction(v)) for v in (-3, -1, 1, 3, 0, 0)]
    m = len(bag)
    for alpha in ALPHAS:
        cov = exact_coverage(bag, mean_scores, alpha)
        assert cov >= 1 - alpha
        assert exact_smoothed_coverage(bag, mean_scores, alpha) == 1 - alpha
    assert exact_coverage(bag, mean_scores, Fraction(1, 2)) > Fraction(math.ceil(Fraction(1, 2) * m), m)


def test_classification_with_nearest_neighbour_scores():
    bag = [(Fraction(0), "a"), (Fraction(1), "a"), (Fraction(3), "a"),
           (Fraction(6), "b"), (Fraction(7), "b"), (Fraction(9), "b")]
    for alpha in ALPHAS:
        assert exact_coverage(bag, nearest_neighbour_scores, alpha) >= 1 - alpha
        assert exact_smoothed_coverage(bag, nearest_neighbour_scores, alpha) == 1 - alpha
    data = bag[:5]
    assert full_conformal_set(data, Fraction(1, 2), ["a", "b"], nearest_neighbour_scores, 0.2) == ["a"]
    assert full_conformal_set(data, Fraction(8), ["a", "b"], nearest_neighbour_scores, 0.2) == ["b"]


def test_exact_least_squares_set_against_the_candidate_loop():
    rng = random.Random(3)
    for trial in range(12):
        n = rng.randint(4, 7)
        data = [(Fraction(rng.randint(0, 20), 2), Fraction(rng.randint(-40, 40), 4)) for _ in range(n)]
        if len({x for x, _ in data}) < 2:
            continue
        x_new = Fraction(rng.randint(-10, 30), 2)
        alpha = rng.choice(ALPHAS)
        sets = full_conformal_least_squares(data, x_new, alpha)
        a, b = least_squares_affine_residuals(data, x_new)
        # the affine form gives the same residuals as a refit
        for y in (Fraction(-7), Fraction(0), Fraction(13, 3)):
            direct = least_squares_scores(list(data) + [(x_new, y)])
            assert direct == [abs(ai + bi * y) for ai, bi in zip(a, b)]
        # brute force: a dense grid, every finite end, and points just inside and outside each end
        cands = [Fraction(k, 8) for k in range(-200, 201)]
        for lo, hi in sets:
            for e in (lo, hi):
                if e is not None:
                    cands += [e, e - Fraction(1, 10**6), e + Fraction(1, 10**6)]
        accepted = set(full_conformal_set(data, x_new, cands, least_squares_scores, alpha))
        for y in cands:
            assert (y in accepted) == in_set(sets, y), (trial, y)


def test_worked_example():
    data = [(1, "2.9"), (2, "5.5"), (3, "4.6"), (4, "5.1"), (5, "5.1"),
            (6, "5.4"), (7, "6.2"), (8, "6.0"), (9, "5.8"), (10, "6.1")]
    data = [(Fraction(x), Fraction(y)) for x, y in data]
    [(lo, hi)] = full_conformal_least_squares(data, Fraction(11, 2), 0.2)
    assert round(float(lo), 3) == 4.032 and round(float(hi), 3) == 6.380
    [(lo, hi)] = full_conformal_least_squares(data, Fraction(11, 2), 0.1)
    assert round(float(lo), 3) == 3.913 and round(float(hi), 3) == 6.783
    [(lo, hi)] = full_conformal_least_squares(data, Fraction(20), 0.1)
    assert round(float(lo), 3) == -5.698 and round(float(hi), 3) == 19.011


def simulate(n, alpha, trials, seed, make_point):
    rng = random.Random(seed)
    out = []
    for _ in range(trials):
        bag = [make_point(rng) for _ in range(n + 1)]
        out.append((bag[-1][0], conformal_p_value(least_squares_scores(bag)) > level(alpha)))
    return out


def test_marginal_coverage_with_heavy_tails_is_measured():
    def cauchy_point(rng):
        x = rng.uniform(0, 10)
        return x, 1 + 0.5 * x + math.tan(math.pi * (rng.random() - 0.5))

    trials = 3000
    hits = sum(ok for _, ok in simulate(19, 0.1, trials, 5, cauchy_point))
    assert abs(hits / trials - 0.9) < 4 * math.sqrt(0.09 / trials)


def test_coverage_is_not_conditional_on_x():
    def spread_point(rng):
        x = rng.uniform(-1, 1)
        return x, x + rng.gauss(0, 0.1 + abs(x))

    res = simulate(39, 0.1, 4000, 9, spread_point)
    inner = [ok for x, ok in res if abs(x) < 0.25]
    outer = [ok for x, ok in res if abs(x) > 0.75]
    assert sum(inner) / len(inner) > 0.97
    assert sum(outer) / len(outer) < 0.82
    assert abs(sum(ok for _, ok in res) / len(res) - 0.9) < 0.02


def test_p_values_and_errors():
    assert conformal_p_value([3, 1, 2, 2]) == Fraction(3, 4)
    assert smoothed_p_value([3, 1, 2, 2], Fraction(1, 2)) == Fraction(1, 2)
    with pytest.raises(ValueError):
        full_conformal_set([(0, 1)], 0, [1], mean_scores, 1.0)
    with pytest.raises(ValueError):
        full_conformal_least_squares([(1, 1), (1, 2)], 1, 0.1)
