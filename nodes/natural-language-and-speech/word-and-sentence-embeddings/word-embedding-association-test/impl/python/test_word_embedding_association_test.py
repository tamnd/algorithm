# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/word-embedding-association-test/. The authors are listed in prov/R1EFZ2.jsonl.

import math
import random
from itertools import permutations

import pytest

from word_embedding_association_test import (
    association,
    effect_size,
    sampled_p_value,
    weat,
    weat_statistic,
)

A = [[1.0, 0.0]]
B = [[0.0, 1.0]]
X = [[4.0, 1.0], [3.0, 2.0], [1.0, 3.0]]
Y = [[2.0, 3.0], [1.0, 4.0], [0.0, 1.0]]


def rand_vec(rng, d):
    return [rng.gauss(0.0, 1.0) for _ in range(d)]


def planted(rng, n, d, direction, shift):
    return [[x + shift * u for x, u in zip(rand_vec(rng, d), direction)] for _ in range(n)]


def test_association_hand_values():
    assert association([4.0, 1.0], A, B) == pytest.approx(3 / math.sqrt(17))
    assert association([1.0, 1.0], A, B) == pytest.approx(0.0)
    assert association([0.0, 1.0], A, B) == pytest.approx(-1.0)
    two = [[1.0, 0.0], [0.0, 2.0]]
    # The mean over A of the cosines with (1, 1) is 1 / sqrt(2), and B gives -1 / sqrt(2).
    assert association([1.0, 1.0], two, [[-1.0, 0.0]]) == pytest.approx(math.sqrt(2))


def test_page_example():
    stat, d, p = weat(X, Y, A, B)
    assert stat == pytest.approx(2.3775, abs=1e-4)
    assert d == pytest.approx(1.3182, abs=1e-4)
    assert p == pytest.approx(1 / 20)
    assert weat(X, Y, A, B, strict=False)[2] == pytest.approx(2 / 20)
    assert effect_size(X, Y, A, B, ddof=1) == pytest.approx(1.2034, abs=1e-4)
    assert weat_statistic(X, Y, A, B) == pytest.approx(stat, abs=1e-12)
    assert effect_size(X, Y, A, B) == pytest.approx(d, abs=1e-12)


def test_exact_p_value_equals_the_fraction_over_all_permutations():
    rng = random.Random(1)
    for _ in range(5):
        Xs = [rand_vec(rng, 4) for _ in range(3)]
        Ys = [rand_vec(rng, 4) for _ in range(3)]
        As = [rand_vec(rng, 4) for _ in range(2)]
        Bs = [rand_vec(rng, 4) for _ in range(3)]
        words = Xs + Ys
        obs = weat_statistic(Xs, Ys, As, Bs)
        greater = 0
        total = 0
        for perm in permutations(range(6)):
            xi = [words[k] for k in perm[:3]]
            yi = [words[k] for k in perm[3:]]
            if weat_statistic(xi, yi, As, Bs) > obs + 1e-12:
                greater += 1
            total += 1
        assert total == 720
        assert weat(Xs, Ys, As, Bs)[2] == pytest.approx(greater / total)


def test_sampled_p_value_is_close_to_the_exact_one():
    rng = random.Random(2)
    direction = [1.0, 0.0, 0.0, 0.0]
    Xs = planted(rng, 5, 4, direction, 0.4)
    Ys = planted(rng, 5, 4, direction, -0.4)
    As = planted(rng, 4, 4, direction, 1.0)
    Bs = planted(rng, 4, 4, direction, -1.0)
    exact = weat(Xs, Ys, As, Bs)[2]
    est = sampled_p_value(Xs, Ys, As, Bs, 4000, random.Random(3))
    assert abs(est - exact) < 0.03


def test_effect_size_is_at_most_two():
    rng = random.Random(4)
    for _ in range(200):
        n = rng.randint(2, 5)
        Xs = [rand_vec(rng, 3) for _ in range(n)]
        Ys = [rand_vec(rng, 3) for _ in range(n)]
        As = [rand_vec(rng, 3) for _ in range(2)]
        Bs = [rand_vec(rng, 3) for _ in range(2)]
        assert abs(effect_size(Xs, Ys, As, Bs)) <= 2 + 1e-12
        assert abs(effect_size(Xs, Ys, As, Bs, ddof=1)) <= 2 + 1e-12


def test_effect_size_reaches_two_when_each_set_is_constant():
    Xs = [[1.0, 0.0], [2.0, 0.0], [5.0, 0.0]]
    Ys = [[0.0, 1.0], [0.0, 3.0], [0.0, 0.5]]
    assert effect_size(Xs, Ys, A, B) == pytest.approx(2.0)
    assert effect_size(Ys, Xs, A, B) == pytest.approx(-2.0)


def test_swaps_negate_the_statistic_and_the_effect_size():
    rng = random.Random(5)
    Xs = [rand_vec(rng, 3) for _ in range(4)]
    Ys = [rand_vec(rng, 3) for _ in range(4)]
    As = [rand_vec(rng, 3) for _ in range(3)]
    Bs = [rand_vec(rng, 3) for _ in range(3)]
    s, d, p = weat(Xs, Ys, As, Bs)
    s2, d2, p2 = weat(Ys, Xs, As, Bs)
    s3, d3, _ = weat(Xs, Ys, Bs, As)
    assert s2 == pytest.approx(-s) and s3 == pytest.approx(-s)
    assert d2 == pytest.approx(-d) and d3 == pytest.approx(-d)
    # The partition values are symmetric about 0, so p2 is the share of values
    # below s, and p + p2 + (the share of values equal to s) = 1.
    ties = weat(Xs, Ys, As, Bs, strict=False)[2] - p
    assert p + p2 + ties == pytest.approx(1.0)


def test_smallest_p_value():
    Xs = [[1.0, 0.0], [1.0, 0.1], [1.0, 0.2], [1.0, 0.3]]
    Ys = [[0.0, 1.0], [0.1, 1.0], [0.2, 1.0], [0.3, 1.0]]
    assert weat(Xs, Ys, A, B)[2] == 0.0
    assert weat(Xs, Ys, A, B, strict=False)[2] == pytest.approx(1 / 70)


def test_planted_bias_gives_a_small_p_value_and_none_gives_a_large_one():
    rng = random.Random(6)
    direction = [1.0, 0.0, 0.0, 0.0, 0.0]
    As = planted(rng, 4, 5, direction, 2.0)
    Bs = planted(rng, 4, 5, direction, -2.0)
    Xs = planted(rng, 6, 5, direction, 1.5)
    Ys = planted(rng, 6, 5, direction, -1.5)
    _, d, p = weat(Xs, Ys, As, Bs)
    assert d > 1.0 and p < 0.01
    flat = [rand_vec(rng, 5) for _ in range(12)]
    p_null = [weat(flat[:6], flat[6:], As, Bs)[2], weat(flat[6:], flat[:6], As, Bs)[2]]
    assert max(p_null) > 0.05


def test_bad_input():
    with pytest.raises(ValueError):
        weat([[1.0, 0.0]], [], A, B)
    with pytest.raises(ValueError):
        association([1.0, 0.0], [], B)
    with pytest.raises(ValueError):
        effect_size([[1.0, 0.0]], [[2.0, 0.0]], A, B)
    with pytest.raises(ValueError):
        sampled_p_value(X, Y, A, B, 0)
