# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kriging/. The authors are listed in prov/ZHD0F7.jsonl.
import math
import random
from fractions import Fraction as F

import pytest

from kriging import Kriging, exponential_cov, gaussian_cov, matern32_cov


def cauchy_sq(r2):
    """Cauchy covariance 1 / (1 + r^2), positive definite in every dimension; exact on Fractions."""
    return 1 / (1 + r2)


def cauchy(r):
    return 1.0 / (1.0 + r * r)


def solve_exact(A, b):
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [a - f * b2 for a, b2 in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def sq(p, q):
    return sum((a - b) ** 2 for a, b in zip(p, q))


def oracle(pts, ys, x, mean=None):
    n = len(pts)
    K = [[cauchy_sq(sq(p, q)) for q in pts] for p in pts]
    k = [cauchy_sq(sq(x, p)) for p in pts]
    c0 = F(1)
    if mean is None:
        A = [K[i] + [F(1)] for i in range(n)] + [[F(1)] * n + [F(0)]]
        sol = solve_exact(A, k + [F(1)])
        lam, mu = sol[:n], sol[n]
        return sum(l * y for l, y in zip(lam, ys)), c0 - sum(l * v for l, v in zip(lam, k)) - mu, lam
    lam = solve_exact(K, k)
    pred = mean + sum(l * (y - mean) for l, y in zip(lam, ys))
    return pred, c0 - sum(l * v for l, v in zip(lam, k)), lam


def rand_point(rng, d):
    return tuple(F(rng.randint(-40, 40), 10) for _ in range(d))


def test_against_exact_oracle():
    rng = random.Random(1963)
    cases = 0
    for trial in range(260):
        d = rng.randint(1, 3)
        n = rng.randint(1, 7)
        pts = []
        while len(pts) < n:
            p = rand_point(rng, d)
            if p not in pts:
                pts.append(p)
        ys = [F(rng.randint(-30, 30), 7) for _ in range(n)]
        mean = None if trial % 2 == 0 else F(rng.randint(-5, 5), 3)
        kr = Kriging([tuple(float(c) for c in p) for p in pts], [float(v) for v in ys], cauchy,
                     mean=None if mean is None else float(mean))
        for _ in range(2):
            x = rand_point(rng, d)
            pred, var, lam = oracle(pts, ys, x, mean)
            xf = tuple(float(c) for c in x)
            assert abs(kr.predict(xf) - float(pred)) <= 1e-8 * (1 + abs(float(pred)))
            assert abs(kr.variance(xf) - max(float(var), 0.0)) <= 1e-8
            for u, v in zip(kr.weights(xf), lam):
                assert abs(u - float(v)) <= 1e-8 * (1 + abs(float(v)))
            cases += 1
    assert cases >= 500


def test_interpolation_and_unbiasedness():
    rng = random.Random(1951)
    for trial in range(150):
        n = rng.randint(1, 9)
        xs = sorted(rng.sample(range(0, 100), n))
        xs = [v / 25 for v in xs]
        rng.shuffle(xs)  # order does not matter
        ys = [rng.uniform(-2, 2) for _ in xs]
        cov = (matern32_cov(1.0, 0.8), exponential_cov(2.0, 1.0), cauchy)[trial % 3]
        kr = Kriging(xs, ys, cov)
        for x, y in zip(xs, ys):
            # points can be 0.04 apart, so K is ill conditioned; allow for it
            assert abs(kr.predict(x) - y) <= 1e-7 * (1 + abs(y))
            assert kr.variance(x) <= 1e-7
        t = rng.uniform(-1, 5)
        lam = kr.weights(t)
        assert abs(sum(lam) - 1) <= 1e-7  # ordinary kriging weights sum to 1
        assert kr.variance(t) >= 0
        c = rng.uniform(-3, 3)
        kc = Kriging(xs, [c] * n, cov)
        assert abs(kc.predict(t) - c) <= 1e-7 * (1 + abs(c))  # constants reproduced


def test_variance_bounds():
    # Simple kriging variance lies in [0, C(0)]; it decreases when data are added.
    rng = random.Random(1941)
    for _ in range(100):
        n = rng.randint(2, 8)
        xs = [rng.uniform(0, 4) for _ in range(n)]
        ys = [rng.uniform(-1, 1) for _ in range(n)]
        cov = matern32_cov(1.5, 0.7)
        full = Kriging(xs, ys, cov, mean=0.0)
        part = Kriging(xs[:-1], ys[:-1], cov, mean=0.0)
        t = rng.uniform(-1, 5)
        assert 0 <= full.variance(t) <= part.variance(t) + 1e-12 <= 1.5 + 1e-12


def test_page_example():
    kr = Kriging([0, 1, 3, 4], [1, 2, 0, 0.5], gaussian_cov(1.0, 1.5))
    assert abs(kr.beta - 0.850289) < 1e-6
    assert abs(kr.predict(2) - 1.127761) < 1e-6
    assert abs(math.sqrt(kr.variance(2)) - 0.437081) < 1e-6
    w = kr.weights(2)
    assert abs(w[0] + 0.2555) < 1e-4 and abs(w[1] - 0.7555) < 1e-4
    assert abs(kr.predict(50) - kr.beta) < 1e-12
    assert abs(kr.variance(50) - 1.431946) < 1e-6
    ks = Kriging([0, 1, 3, 4], [1, 2, 0, 0.5], gaussian_cov(1.0, 1.5), mean=0.0)
    assert abs(ks.predict(2) - 0.983038) < 1e-6


def test_edges_and_conditioning():
    kr = Kriging([2.0], [5.0], exponential_cov())
    assert kr.predict(-3.0) == 5.0
    # one point, ordinary kriging: variance 2 (C(0) - C(r))
    assert abs(kr.variance(3.0) - 2 * (1 - math.exp(-1.0))) < 1e-12
    with pytest.raises(ValueError):
        Kriging([0.0, 1.0, 1.0], [0.0, 1.0, 2.0], exponential_cov())
    # with a nugget, repeated points are allowed and their values are averaged
    kn = Kriging([0.0, 1.0, 1.0], [0.0, 1.0, 3.0], exponential_cov(), nugget=0.1)
    assert 1.0 < kn.predict(1.0) < 3.0
    # Gaussian covariance on dense points breaks down (ill conditioning)
    xs = [i / 40 for i in range(41)]
    with pytest.raises(ValueError):
        Kriging(xs, [math.sin(v) for v in xs], gaussian_cov(1.0, 0.3))
    with pytest.raises(ValueError):
        Kriging([], [], exponential_cov())
