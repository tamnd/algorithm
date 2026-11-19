# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plda-scoring/. The authors are listed in prov/MHT9KM.jsonl.

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from plda_scoring import (
    cholesky,
    inverse,
    log_gauss,
    logdet,
    mat_mul,
    prepare,
    prince_elder_to_two_cov,
    score,
    score_multi,
)


def random_spd(rng, d, scale=1.0):
    R = [[rng.gauss(0.0, 1.0) for _ in range(d)] for _ in range(d)]
    S = mat_mul(R, [list(c) for c in zip(*R)])
    for i in range(d):
        S[i][i] += 0.5 * d
    return [[scale * v for v in row] for row in S]


def block(rows_of_blocks):
    out = []
    for brow in rows_of_blocks:
        for r in range(len(brow[0])):
            out.append([v for blk in brow for v in blk[r]])
    return out


def zeros(d):
    return [[0.0] * d for _ in range(d)]


def joint_llr(enroll, test, m, B, W):
    """Brute force: joint Gaussian of all embeddings under one speaker, against the test from a new speaker."""
    A = [[b + w for b, w in zip(rb, rw)] for rb, rw in zip(B, W)]
    xs = list(enroll) + [test]
    k = len(xs)
    big = block([[A if i == j else B for j in range(k)] for i in range(k)])
    flat = [v for x in xs for v in x]
    mean = [v for _ in range(k) for v in m]
    same = log_gauss(flat, mean, big)
    k1 = len(enroll)
    big1 = block([[A if i == j else B for j in range(k1)] for i in range(k1)])
    flat1 = [v for x in enroll for v in x]
    mean1 = [v for _ in range(k1) for v in m]
    enroll_only = log_gauss(flat1, mean1, big1)
    return same - enroll_only - log_gauss(test, m, A)


def test_closed_form_matches_joint_gaussian():
    rng = random.Random(1)
    for d in (1, 2, 3):
        B = random_spd(rng, d)
        W = random_spd(rng, d, 0.5)
        m = [rng.uniform(-1.0, 1.0) for _ in range(d)]
        prep = prepare(B, W)
        for _ in range(5):
            x1 = [rng.gauss(0.0, 2.0) for _ in range(d)]
            x2 = [rng.gauss(0.0, 2.0) for _ in range(d)]
            assert score(x1, x2, m, prep) == pytest.approx(joint_llr([x1], x2, m, B, W), abs=1e-9)


def test_symmetry_and_signs():
    rng = random.Random(2)
    d = 3
    B = random_spd(rng, d)
    W = random_spd(rng, d)
    Q, P, c = prepare(B, W)
    m = [0.0] * d
    x1 = [0.3, -1.2, 0.7]
    x2 = [1.1, 0.4, -0.5]
    assert score(x1, x2, m, (Q, P, c)) == pytest.approx(score(x2, x1, m, (Q, P, c)), abs=1e-12)
    for i in range(d):
        for j in range(d):
            assert P[i][j] == pytest.approx(P[j][i], abs=1e-12)
    # Q is negative definite, so -Q has a Cholesky factor.
    cholesky([[-v for v in row] for row in Q])
    assert c > 0.0


def test_multi_enrollment_matches_joint_gaussian():
    rng = random.Random(3)
    d = 2
    B = random_spd(rng, d)
    W = random_spd(rng, d, 0.7)
    m = [0.5, -0.5]
    for n in (1, 2, 4):
        enroll = [[rng.gauss(0.0, 1.5) for _ in range(d)] for _ in range(n)]
        test = [rng.gauss(0.0, 1.5) for _ in range(d)]
        assert score_multi(enroll, test, m, B, W) == pytest.approx(joint_llr(enroll, test, m, B, W), abs=1e-9)


def test_one_enrollment_equals_closed_form():
    rng = random.Random(4)
    d = 3
    B = random_spd(rng, d)
    W = random_spd(rng, d)
    m = [0.1, 0.2, 0.3]
    prep = prepare(B, W)
    x1 = [1.0, -0.5, 0.25]
    x2 = [0.75, -0.25, 0.5]
    assert score_multi([x1], x2, m, B, W) == pytest.approx(score(x1, x2, m, prep), abs=1e-9)


def test_tiny_between_covariance_gives_zero():
    B = [[1e-9, 0.0], [0.0, 1e-9]]
    W = [[1.0, 0.2], [0.2, 1.5]]
    prep = prepare(B, W)
    assert abs(score([3.0, -2.0], [-1.0, 4.0], [0.0, 0.0], prep)) < 1e-6


def test_page_example():
    prep = prepare([[3.0]], [[1.0]])
    Q, P, c = prep
    assert Q[0][0] == pytest.approx(-9.0 / 28.0, abs=1e-12)
    assert P[0][0] == pytest.approx(3.0 / 7.0, abs=1e-12)
    assert c == pytest.approx(0.5 * math.log(16.0 / 7.0), abs=1e-12)
    expected = {(1.0, 1.0): 0.520482, (1.0, -1.0): -0.336661, (0.0, 0.0): 0.413339,
                (2.0, 2.0): 0.841911, (3.0, 0.0): -1.033089}
    for (a, b), v in expected.items():
        assert score([a], [b], [0.0], prep) == pytest.approx(v, abs=1e-6)


def test_prince_elder_map():
    F = [[1.0], [2.0]]
    G = [[0.5], [0.0]]
    Sigma = [0.1, 0.3]
    B, W = prince_elder_to_two_cov(F, G, Sigma)
    assert B == [[1.0, 2.0], [2.0, 4.0]]
    assert W[0][0] == pytest.approx(0.35)
    assert W[0][1] == pytest.approx(0.0)
    assert W[1][1] == pytest.approx(0.3)
    # B is singular here (rank one), which the closed form allows because A and the Schur complement stay definite.
    prep = prepare(B, W)
    x1, x2 = [0.4, 1.1], [0.6, 0.9]
    assert score(x1, x2, [0.0, 0.0], prep) == pytest.approx(joint_llr([x1], x2, [0.0, 0.0], B, W), abs=1e-9)


def test_linear_algebra_helpers():
    S = [[4.0, 2.0], [2.0, 3.0]]
    assert logdet(S) == pytest.approx(math.log(8.0), abs=1e-12)
    Si = inverse(S)
    prod = mat_mul(S, Si)
    for i in range(2):
        for j in range(2):
            assert prod[i][j] == pytest.approx(1.0 if i == j else 0.0, abs=1e-12)
    with pytest.raises(ValueError):
        cholesky([[1.0, 2.0], [2.0, 1.0]])
    with pytest.raises(ValueError):
        score_multi([], [0.0], [0.0], [[1.0]], [[1.0]])
