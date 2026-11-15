# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/joint-spectral-radius/. The authors are listed in prov/5Q24WE.jsonl.

import math
import random

import pytest

from ctlmat import inv, matvec, mul, norm2
from joint_spectral_radius import jsr_bounds, products, spectral_radius

PHI = (1 + math.sqrt(5)) / 2
GOLDEN = [[[1, 1], [0, 1]], [[1, 0], [1, 1]]]
TOL = 1e-7  # polyroots is accurate to about 1e-8 for a double eigenvalue


def random_matrix(rng, n, scale=1.0):
    return [[rng.uniform(-scale, scale) for _ in range(n)] for _ in range(n)]


def test_golden_pair():
    lo, hi = jsr_bounds(GOLDEN, 1)
    assert abs(lo - 1.0) < TOL and abs(hi - PHI) < TOL
    lo, hi = jsr_bounds(GOLDEN, 2)
    assert abs(lo - PHI) < TOL and abs(hi - PHI) < TOL
    assert abs(spectral_radius(mul(GOLDEN[0], GOLDEN[1])) - PHI ** 2) < TOL
    # odd lengths alone give smaller lower bounds
    ps = products(GOLDEN, 3)
    assert abs(max(spectral_radius(p) for p in ps) ** (1 / 3) - 1.551134) < 1e-6


def test_switching_between_schur_matrices_can_diverge():
    a1 = [[0.5, 2.0], [0.0, 0.5]]
    a2 = [[0.5, 0.0], [2.0, 0.5]]
    assert spectral_radius(a1) < 1 and spectral_radius(a2) < 1
    lo, hi = jsr_bounds([a1, a2], 2)
    assert abs(lo - (0.5 + PHI)) < TOL
    assert abs(hi - (0.5 + PHI)) < TOL
    x = [1.0, 1.0]
    for _ in range(20):
        x = matvec(a2, matvec(a1, x))
    assert norm2(x) > 1e6


def test_single_matrix_gives_its_spectral_radius():
    rng = random.Random(11)
    for _ in range(20):
        a = random_matrix(rng, 3)
        rho = spectral_radius(a)
        lo, hi = jsr_bounds([a], 6)
        assert lo == pytest.approx(rho, rel=1e-6, abs=TOL)
        assert hi >= rho - TOL


def test_upper_triangular_sets():
    # For upper triangular matrices the JSR is the largest modulus of a diagonal entry.
    rng = random.Random(3)
    for _ in range(30):
        mats = []
        for _ in range(rng.randint(1, 3)):
            d1, d2, u = rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-3, 3)
            mats.append([[d1, u], [0.0, d2]])
        rho = max(max(abs(m[0][0]), abs(m[1][1])) for m in mats)
        lo, hi = jsr_bounds(mats, 4)
        assert lo == pytest.approx(rho, abs=TOL)
        assert hi >= rho - TOL


def test_bounds_sandwich_and_monotone():
    rng = random.Random(7)
    for _ in range(15):
        n = rng.randint(2, 3)
        mats = [random_matrix(rng, n) for _ in range(rng.randint(2, 3))]
        prev_lo, prev_hi = 0.0, math.inf
        for k in range(1, 5):
            lo, hi = jsr_bounds(mats, k)
            assert lo <= hi + TOL
            assert lo >= prev_lo and hi <= prev_hi
            prev_lo, prev_hi = lo, hi
        # every product of every length lies inside the interval
        for k in range(1, 6):
            for p in products(mats, k):
                assert spectral_radius(p) ** (1 / k) <= prev_hi + TOL


def test_similarity_and_scaling():
    rng = random.Random(19)
    for _ in range(10):
        mats = [random_matrix(rng, 2) for _ in range(2)]
        t = random_matrix(rng, 2)
        t[0][0] += 3.0
        t[1][1] += 3.0
        ti = inv(t)
        conj = [mul(ti, mul(a, t)) for a in mats]
        lo1, _ = jsr_bounds(mats, 4)
        lo2, _ = jsr_bounds(conj, 4)
        assert lo1 == pytest.approx(lo2, rel=1e-6, abs=TOL)
        c = rng.uniform(0.2, 3.0)
        scaled = [[[c * v for v in row] for row in a] for a in mats]
        lo3, hi3 = jsr_bounds(scaled, 3)
        lo4, hi4 = jsr_bounds(mats, 3)
        assert lo3 == pytest.approx(c * lo4, rel=1e-6, abs=TOL)
        assert hi3 == pytest.approx(c * hi4, rel=1e-9)


def test_upper_bound_below_one_gives_decay_under_any_switching():
    rng = random.Random(23)
    mats = [[[0.6, 0.5], [0.0, 0.6]], [[0.6, 0.0], [-0.5, 0.6]]]
    _, hi = jsr_bounds(mats, 5)
    assert hi < 0.81
    k = 5
    assert max(norm2(p) for p in products(mats, k)) <= hi ** k + 1e-12
    # ||P|| <= hi^k for every product of length k, so x decays at least like hi^k per block
    for _ in range(50):
        x = [rng.uniform(-1, 1), rng.uniform(-1, 1)]
        x0 = norm2(x)
        for _ in range(4):
            for _ in range(k):
                x = matvec(mats[rng.randrange(2)], x)
        assert norm2(x) <= hi ** (4 * k) * x0 + 1e-12


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        jsr_bounds([], 2)
    with pytest.raises(ValueError):
        jsr_bounds(GOLDEN, 0)
    with pytest.raises(ValueError):
        jsr_bounds([[[1, 0], [0, 1]], [[1]]], 2)
