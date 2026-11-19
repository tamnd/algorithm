# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vits/. The authors are listed in prov/HW04HE.jsonl.

import itertools
import math
import random

import pytest

from vits import durations, gaussian_log_likelihoods, monotonic_alignment_search


def all_alignments(n, T):
    """Every monotonic alignment of T frames to n tokens, from the cut points."""
    for cuts in itertools.combinations(range(1, T), n - 1):
        bounds = (0,) + cuts + (T,)
        a = []
        for i in range(n):
            a.extend([i] * (bounds[i + 1] - bounds[i]))
        yield a


def brute_force(v):
    """The best alignment by (score, reversed alignment), the tie rule of the code."""
    n, T = len(v), len(v[0])
    best = None
    for a in all_alignments(n, T):
        s = sum(v[a[j]][j] for j in range(T))
        key = (s, tuple(reversed(a)))
        if best is None or key > best[0]:
            best = (key, a)
    return best[1], best[0][0]


def test_count_is_binomial():
    for n in range(1, 6):
        for T in range(n, 9):
            assert sum(1 for _ in all_alignments(n, T)) == math.comb(T - 1, n - 1)
    assert sum(1 for _ in all_alignments(3, 6)) == 10


def test_matches_brute_force_float():
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randint(1, 5)
        T = rng.randint(n, 9)
        v = [[rng.gauss(0.0, 1.0) for _ in range(T)] for _ in range(n)]
        a, s = monotonic_alignment_search(v)
        b, t = brute_force(v)
        assert a == b
        assert math.isclose(s, t, rel_tol=1e-12, abs_tol=1e-12)


def test_matches_brute_force_with_ties():
    # Small integer scores make many ties; the sums are exact in floating point.
    rng = random.Random(11)
    for _ in range(300):
        n = rng.randint(1, 4)
        T = rng.randint(n, 8)
        v = [[float(rng.randint(-2, 1)) for _ in range(T)] for _ in range(n)]
        a, s = monotonic_alignment_search(v)
        b, t = brute_force(v)
        assert s == t
        assert a == b


def test_alignment_is_monotonic_and_onto():
    rng = random.Random(3)
    for _ in range(50):
        n = rng.randint(1, 6)
        T = rng.randint(n, 30)
        v = [[rng.uniform(-5, 0) for _ in range(T)] for _ in range(n)]
        a, s = monotonic_alignment_search(v)
        assert a[0] == 0 and a[-1] == n - 1
        assert all(a[j + 1] - a[j] in (0, 1) for j in range(T - 1))
        assert sum(durations(a, n)) == T and min(durations(a, n)) >= 1
        assert math.isclose(s, sum(v[a[j]][j] for j in range(T)))


def test_page_example():
    v = [
        [-1.0, -1.0, -4.0, -6.0, -6.0, -9.0],
        [-5.0, -2.0, -1.0, -1.0, -5.0, -5.0],
        [-9.0, -7.0, -5.0, -2.0, -1.0, -1.0],
    ]
    a, s = monotonic_alignment_search(v)
    assert a == [0, 0, 1, 1, 2, 2]
    assert s == -6.0
    assert durations(a, 3) == [2, 2, 2]


def test_gaussian_scores_recover_segments():
    # Three tokens with well separated means; the frames come in runs of 2, 3 and 4.
    mu = [[0.0, 0.0], [3.0, 0.0], [0.0, 3.0]]
    sigma = [[0.5, 0.5]] * 3
    rng = random.Random(5)
    z = []
    for i, length in enumerate([2, 3, 4]):
        for _ in range(length):
            z.append([mu[i][0] + rng.gauss(0, 0.1), mu[i][1] + rng.gauss(0, 0.1)])
    v = gaussian_log_likelihoods(mu, sigma, z)
    a, _ = monotonic_alignment_search(v)
    assert durations(a, 3) == [2, 3, 4]
    expected = -math.log(2 * math.pi * 0.25) - (0.0 ** 2 + 0.0 ** 2) / 0.5
    assert math.isclose(gaussian_log_likelihoods([[0.0, 0.0]], [[0.5, 0.5]], [[0.0, 0.0]])[0][0], expected)


def test_large_input_runs():
    rng = random.Random(9)
    n, T = 40, 400
    v = [[rng.uniform(-3, 0) for _ in range(T)] for _ in range(n)]
    a, _ = monotonic_alignment_search(v)
    assert len(a) == T and a[-1] == n - 1


def test_errors():
    with pytest.raises(ValueError):
        monotonic_alignment_search([])
    with pytest.raises(ValueError):
        monotonic_alignment_search([[0.0], [0.0]])
    with pytest.raises(ValueError):
        monotonic_alignment_search([[0.0, 1.0], [0.0]])
    a, s = monotonic_alignment_search([[2.0, 3.0]])
    assert a == [0, 0] and s == 5.0
