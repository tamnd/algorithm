# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/equal-error-rate/. The authors are listed in prov/QFSA7K.jsonl.

import math
import os
import random
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from equal_error_rate import eer_nearest, eer_rocch, min_dcf, operating_points, rocch

TAR = [0.9, 0.8, 0.6, 0.45, 0.3]
NON = [0.7, 0.5, 0.4, 0.35, 0.1]


def test_page_example():
    pts = [(pf, pm) for _, pf, pm in operating_points(TAR, NON)]
    assert pts == [(F(1), F(0)), (F(4, 5), F(0)), (F(4, 5), F(1, 5)), (F(3, 5), F(1, 5)), (F(2, 5), F(1, 5)),
                   (F(2, 5), F(2, 5)), (F(1, 5), F(2, 5)), (F(1, 5), F(3, 5)), (F(0), F(3, 5)), (F(0), F(4, 5)),
                   (F(0), F(1))]
    assert rocch(TAR, NON) == [(F(0), F(3, 5)), (F(2, 5), F(1, 5)), (F(4, 5), F(0))]
    assert eer_rocch(TAR, NON) == F(3, 10)
    assert eer_nearest(TAR, NON) == F(2, 5)
    assert min_dcf(TAR, NON, F(1, 2)) == F(3, 10)


def test_conventions_differ_on_a_tie():
    tar = [0.9, 0.8, 0.7, 0.4]
    non = [0.75, 0.5, 0.3, 0.2, 0.1, 0.05]
    assert eer_rocch(tar, non) == F(1, 5)
    assert eer_nearest(tar, non) == F(7, 24)


def test_extremes():
    assert eer_rocch([2.0, 3.0], [0.0, 1.0]) == 0
    assert eer_rocch([0.5], [0.5]) == F(1, 2)
    rng = random.Random(5)
    tar = [rng.uniform(0.0, 1.0) for _ in range(30)]
    non = [rng.uniform(2.0, 3.0) for _ in range(40)]
    # Reversed scores: the hull is the chance line, so the hull EER is 1/2.
    assert eer_rocch(tar, non) == F(1, 2)
    assert eer_nearest(tar, non) > F(1, 2)
    with pytest.raises(ValueError):
        eer_rocch([], [1.0])


def test_rocch_eer_is_max_of_min_dcf():
    rng = random.Random(7)
    for _ in range(20):
        tar = [round(rng.gauss(1.0, 1.0), 2) for _ in range(rng.randint(1, 15))]
        non = [round(rng.gauss(0.0, 1.0), 2) for _ in range(rng.randint(1, 15))]
        eer = eer_rocch(tar, non)
        for k in range(0, 41):
            assert min_dcf(tar, non, F(k, 40)) <= eer
        hull = rocch(tar, non)
        if len(hull) == 1:
            assert eer == 0
            continue
        for (f1, m1), (f2, m2) in zip(hull, hull[1:]):
            if m1 >= f1 and m2 <= f2:
                p = (f2 - f1) / ((f2 - f1) + (m1 - m2))
                assert min_dcf(tar, non, p) == eer
                break


def test_invariant_under_monotone_maps():
    rng = random.Random(11)
    tar = [rng.gauss(1.0, 1.0) for _ in range(25)]
    non = [rng.gauss(0.0, 1.0) for _ in range(35)]
    e = eer_rocch(tar, non)
    assert eer_rocch([3.0 * s + 1.0 for s in tar], [3.0 * s + 1.0 for s in non]) == e
    assert eer_rocch([math.exp(s) for s in tar], [math.exp(s) for s in non]) == e
    assert eer_nearest([math.exp(s) for s in tar], [math.exp(s) for s in non]) == eer_nearest(tar, non)


def test_hull_never_above_steps():
    rng = random.Random(13)
    tar = [rng.gauss(0.8, 1.0) for _ in range(20)]
    non = [rng.gauss(0.0, 1.0) for _ in range(20)]
    assert eer_rocch(tar, non) <= eer_nearest(tar, non) + F(1, 20)
    hull = rocch(tar, non)
    for _, pf, pm in operating_points(tar, non):
        # Every operating point lies on or above the hull.
        for (f1, m1), (f2, m2) in zip(hull, hull[1:]):
            if f1 <= pf <= f2:
                assert pm >= m1 + (m2 - m1) * (pf - f1) / (f2 - f1)


def test_gaussian_scores():
    rng = random.Random(17)
    tar = [rng.gauss(2.0, 1.0) for _ in range(3000)]
    non = [rng.gauss(0.0, 1.0) for _ in range(3000)]
    # Equal variances and d' = 2 give the EER Phi(-1) = 0.158655.
    phi = 0.5 * math.erfc(1.0 / math.sqrt(2.0))
    assert abs(float(eer_rocch(tar, non)) - phi) < 0.02
    assert abs(float(eer_nearest(tar, non)) - phi) < 0.02
