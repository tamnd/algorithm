# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/split-conformal-prediction/. The authors are listed in prov/6A6QRB.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from split_conformal_prediction import (
    INF,
    calibration_rank,
    conformal_quantile,
    conformalized_quantile_regression,
    fit_binned_quantile,
    fit_line,
    split_conformal,
)

ALPHAS = (Fraction(1, 20), Fraction(1, 10), Fraction(1, 6), Fraction(1, 5), Fraction(1, 3), Fraction(1, 2))

TRAIN = [(Fraction(0), Fraction(1)), (Fraction(2), Fraction(2)), (Fraction(4), Fraction(4)), (Fraction(6), Fraction(4))]


def exact_coverage(train, rest, alpha):
    """P(Y_new in the interval) when the n2 calibration points and the new point are in a
    uniformly random order: enumerate every ordering of them, with the training part fixed."""
    hits = total = 0
    for perm in itertools.permutations(rest):
        calib, (x_new, y_new) = list(perm[:-1]), perm[-1]
        res = split_conformal(train + calib, len(train), fit_line, alpha)
        lo, hi = res.interval(x_new)
        hits += lo <= y_new <= hi
        total += 1
    return Fraction(hits, total)


def test_exact_coverage_by_exchangeability():
    rest = [(Fraction(1), Fraction(3)), (Fraction(3), Fraction(1)), (Fraction(5), Fraction(7)),
            (Fraction(7), Fraction(2)), (Fraction(2), Fraction(5, 2)), (Fraction(8), Fraction(9))]
    mu = fit_line(TRAIN)
    scores = [abs(y - mu(x)) for x, y in rest]
    assert len(set(scores)) == len(scores)
    n2 = len(rest) - 1
    for alpha in ALPHAS:
        k = calibration_rank(n2, alpha)
        cov = exact_coverage(TRAIN, rest, alpha)
        assert cov == (Fraction(k, n2 + 1) if k <= n2 else 1)
        # Lei et al. bounds: 1 - alpha <= coverage <= 1 - alpha + 1/(n2 + 1)
        assert 1 - alpha <= cov <= 1 - alpha + Fraction(1, n2 + 1)


def test_ties_keep_the_lower_bound():
    # residuals +-1, +-1, 2, -2 give tied scores: coverage can only go up
    mu = fit_line(TRAIN)
    rest = [(Fraction(x), mu(Fraction(x)) + s) for x, s in ((1, 1), (3, -1), (5, 1), (7, 2), (2, -2), (8, 1))]
    scores = [abs(y - mu(x)) for x, y in rest]
    assert len(set(scores)) == 2
    n2 = len(rest) - 1
    raised = False
    for alpha in ALPHAS:
        k = calibration_rank(n2, alpha)
        cov = exact_coverage(TRAIN, rest, alpha)
        assert cov >= 1 - alpha
        raised |= cov > Fraction(min(k, n2 + 1), n2 + 1)
    assert raised


def test_rank_and_bounds_arithmetic():
    for n2 in range(1, 60):
        for alpha in ALPHAS + (Fraction(1, 100), Fraction(9, 10)):
            k = calibration_rank(n2, alpha)
            if k <= n2:
                assert 1 - alpha <= Fraction(k, n2 + 1) < 1 - alpha + Fraction(1, n2 + 1)
            else:
                assert alpha < Fraction(1, n2 + 1)
    # with n/2 calibration points the upper slack 1/(n2 + 1) is Lei et al.'s 2/(n + 2)
    for n in range(2, 200, 2):
        assert Fraction(1, n // 2 + 1) == Fraction(2, n + 2)
    assert calibration_rank(19, 0.1) == 18 and calibration_rank(20, 0.1) == 19
    assert conformal_quantile([5, 1, 4, 2, 3], 0.1) == INF
    assert conformal_quantile([5, 1, 4, 2, 3], 0.5) == 3


def test_q_is_the_kth_smallest_score_and_infinite_when_k_exceeds_n2():
    rng = random.Random(1)
    pts = [(x, 2 * x + rng.gauss(0, 1)) for x in (rng.uniform(0, 5) for _ in range(30))]
    res = split_conformal(pts, 20, fit_line, 0.2, random.Random(4))
    assert res.n2 == 10 and res.k == 9
    order = list(range(30))
    random.Random(4).shuffle(order)
    mu = fit_line([pts[i] for i in order[:20]])
    scores = sorted(abs(pts[i][1] - mu(pts[i][0])) for i in order[20:])
    assert res.q == scores[8]
    assert split_conformal(pts, 26, fit_line, 0.1, random.Random(4)).q == INF
    with pytest.raises(ValueError):
        split_conformal(pts, 30, fit_line, 0.1)
    with pytest.raises(ValueError):
        split_conformal(pts, 10, fit_line, 0.0)


def gen(rng, n, noise):
    out = []
    for _ in range(n):
        x = rng.uniform(0, 10)
        out.append((x, 1 + 0.5 * x + noise(rng)))
    return out


def test_marginal_coverage_is_measured():
    def cauchy(rng):
        return math.tan(math.pi * (rng.random() - 0.5))

    rng = random.Random(4)
    trials, hits = 3000, 0
    for _ in range(trials):
        pts = gen(rng, 41, cauchy)
        lo, hi = split_conformal(pts[:40], 20, fit_line, 0.1, rng).interval(pts[-1][0])
        hits += lo <= pts[-1][1] <= hi
    expected = 19 / 21  # k/(n2 + 1) with n2 = 20
    assert abs(hits / trials - expected) < 4 * math.sqrt(expected * (1 - expected) / trials)


def test_cqr_adapts_to_the_spread_measured():
    rng = random.Random(7)
    split_outer = cqr_outer = outer = 0
    split_all = cqr_all = 0
    trials = 1200
    for _ in range(trials):
        pts = []
        for _ in range(401):
            x = rng.uniform(-1, 1)
            pts.append((x, x + rng.gauss(0, 0.1 + abs(x))))
        data, (xn, yn) = pts[:400], pts[-1]
        lo, hi = split_conformal(data, 200, fit_line, 0.1, rng).interval(xn)
        a, b = conformalized_quantile_regression(data, 200, fit_binned_quantile, 0.1, rng)(xn)
        s, c = lo <= yn <= hi, a <= yn <= b
        split_all += s
        cqr_all += c
        if abs(xn) > 0.75:
            outer += 1
            split_outer += s
            cqr_outer += c
    assert abs(split_all / trials - 0.9) < 0.04 and abs(cqr_all / trials - 0.9) < 0.04
    assert split_outer / outer < 0.82 < cqr_outer / outer
