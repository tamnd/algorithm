# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lowe-ratio-test/. The authors are listed in prov/GBD07V.jsonl.

import math
import random

import pytest

from lowe_ratio_test import nearest_two, ratio_test_match


def brute(A, B, r):
    out = []
    for i, a in enumerate(A):
        ds = sorted((math.dist(a, b), j) for j, b in enumerate(B))
        (d1, j), (d2, _) = ds[0], ds[1]
        if d1 < r * d2:
            out.append((i, j))
    return out


def test_worked_example():
    A = [(0.0, 0.0), (5.0, 5.0), (2.1, 0.0)]
    B = [(1.0, 0.0), (3.0, 0.0), (5.0, 4.0), (5.0, 6.2)]
    got = ratio_test_match(A, B, 0.8)
    assert [(i, j) for i, j, _, _ in got] == [(0, 0)]
    i, j, d1, d2 = got[0]
    assert abs(d1 - 1.0) < 1e-12 and abs(d2 - 3.0) < 1e-12
    # with a looser ratio the other queries pass too: 0.9 / 1.1 = 0.818 and 1 / 1.2 = 0.833
    assert [(i, j) for i, j, _, _ in ratio_test_match(A, B, 0.82)] == [(0, 0), (2, 1)]
    assert [(i, j) for i, j, _, _ in ratio_test_match(A, B, 0.85)] == [(0, 0), (1, 2), (2, 1)]


def test_many_small_inputs_against_sorting():
    rng = random.Random(1)
    for _ in range(600):
        d = rng.randint(1, 4)
        A = [tuple(rng.randint(0, 5) for _ in range(d)) for _ in range(rng.randint(0, 6))]
        B = [tuple(rng.randint(0, 5) for _ in range(d)) for _ in range(rng.randint(2, 7))]
        # with integer coordinates no distance ratio equals these r exactly, so rounding cannot decide
        r = rng.choice((0.61, 0.71, 0.83, 0.93, 1.0))
        got = ratio_test_match(A, B, r)
        want = brute(A, B, r)
        assert [i for i, _, _, _ in got] == [i for i, _ in want]
        for (i, j, d1, d2), (_, wj) in zip(got, want):
            assert math.dist(A[i], B[j]) == pytest.approx(math.dist(A[i], B[wj]))
            assert d1 < r * d2


def test_scale_of_all_descriptors_does_not_matter():
    rng = random.Random(2)
    A = [tuple(rng.random() for _ in range(8)) for _ in range(30)]
    B = [tuple(rng.random() for _ in range(8)) for _ in range(40)]
    base = [(i, j) for i, j, _, _ in ratio_test_match(A, B, 0.9)]
    for c in (0.25, 4.0, 1000.0):
        A2 = [tuple(c * x for x in a) for a in A]
        B2 = [tuple(c * x for x in b) for b in B]
        assert [(i, j) for i, j, _, _ in ratio_test_match(A2, B2, 0.9)] == base


def test_duplicate_of_the_nearest_is_rejected():
    A = [(0.0, 0.0)]
    B = [(1.0, 1.0), (1.0, 1.0), (9.0, 9.0)]
    assert nearest_two(A[0], B) == (0, 2.0, 2.0)
    assert ratio_test_match(A, B, 1.0) == []
    assert ratio_test_match(A, B[1:], 0.8) == [(0, 0, math.sqrt(2.0), math.sqrt(162.0))]


def test_kept_set_grows_with_the_ratio():
    rng = random.Random(3)
    A = [tuple(rng.random() for _ in range(4)) for _ in range(50)]
    B = [tuple(rng.random() for _ in range(4)) for _ in range(50)]
    prev = set()
    for r in (0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
        cur = {(i, j) for i, j, _, _ in ratio_test_match(A, B, r)}
        assert prev <= cur
        prev = cur


def test_bad_input():
    with pytest.raises(ValueError):
        ratio_test_match([(0.0,)], [(1.0,)], 0.8)
    with pytest.raises(ValueError):
        ratio_test_match([(0.0,)], [(1.0,), (2.0,)], 0.0)
    assert ratio_test_match([], [(1.0,), (2.0,)]) == []
