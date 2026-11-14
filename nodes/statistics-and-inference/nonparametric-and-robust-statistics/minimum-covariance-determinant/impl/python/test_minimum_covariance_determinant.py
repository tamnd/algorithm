# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-covariance-determinant/. The authors are listed in prov/KD8XYJ.jsonl.

import itertools
import math
import random
from fractions import Fraction as F

import pytest

from minimum_covariance_determinant import (
    c_step,
    closest,
    concentrate,
    consistency_factor,
    cov,
    det,
    default_h,
    exact_mcd,
    fast_mcd_raw,
    inverse,
    mahalanobis2,
    mcd,
    mean,
)

EXAMPLE = [(2, 1), (1, 3), (5, 4), (3, 2), (4, 1), (3, 4), (4, 6), (10, -1), (11, 2), (10, 10)]


def exact(points):
    return [tuple(F(v) for v in x) for x in points]


def random_data(rng, n, k):
    """n - k clean integer points near the origin and k far points, as Fractions."""
    clean = [(F(rng.randint(-5, 5)), F(rng.randint(-5, 5))) for _ in range(n - k)]
    far = [(F(rng.randint(8, 20)), F(rng.randint(-20, 20))) for _ in range(k)]
    return clean + far


def test_example_trace():
    pts = exact(EXAMPLE)
    h = 6
    j = [2, 6, 7]
    mu = mean(pts, j)
    idx = closest(pts, mu, cov(pts, j, mu), h)
    path = [idx]
    while True:
        new = c_step(pts, idx, h)
        if new == idx:
            break
        idx = new
        path.append(idx)
    assert path == [[2, 4, 5, 6, 7, 8], [2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6], [0, 2, 3, 4, 5, 6]]
    dets = [det(cov(pts, q)) for q in path]
    assert dets == [F(3397, 108), F(1909, 108), F(413, 108), F(85, 36)]
    assert exact_mcd(pts, h) == (F(85, 36), [0, 2, 3, 4, 5, 6])
    assert mean(pts, path[-1]) == [F(7, 2), F(3)]
    assert cov(pts, path[-1]) == [[F(11, 12), F(5, 6)], [F(5, 6), F(10, 3)]]


def test_example_stopping_points():
    pts = exact(EXAMPLE)
    h = 6
    ends = {}
    for j in itertools.combinations(range(10), 3):
        j = list(j)
        if det(cov(pts, j)) == 0:
            continue
        d, idx, _, _ = concentrate(pts, closest(pts, mean(pts, j), cov(pts, j), h), h)
        ends.setdefault((tuple(idx), d), []).append(j)
    assert sum(len(v) for v in ends.values()) == 119
    assert len(ends) == 8
    assert len(ends[((0, 2, 3, 4, 5, 6), F(85, 36))]) == 43
    assert [0, 1, 7] in ends[((0, 1, 3, 4, 5, 7), F(973, 108))]


def test_example_reweighted():
    r = mcd(EXAMPLE, h=6, starts=50)
    assert r["subset"] == [0, 2, 3, 4, 5, 6]
    assert r["outlier"] == [False] * 7 + [True] * 3
    assert r["location"] == pytest.approx([22 / 7, 3.0])
    raw_inv = inverse(r["raw_scatter"])
    assert mahalanobis2(EXAMPLE[1], r["raw_location"], raw_inv) == pytest.approx(3.43, abs=0.005)
    assert [round(v, 1) for v in r["distance2"][7:]] == [45.8, 43.7, 32.7]
    assert consistency_factor(0.6, 2) == pytest.approx(2.56977, abs=1e-5)


def test_fast_mcd_matches_full_enumeration():
    """p = 2 and n <= 12: every (p + 1)-subset as a start finds the exact MCD determinant."""
    rng = random.Random(1)
    checked = 0
    for _ in range(14):
        n = rng.randint(6, 12)
        pts = random_data(rng, n, rng.randint(0, (n - 1) // 2))
        h = default_h(n, 2)
        best, _ = exact_mcd(pts, h)
        if best == 0:
            continue
        checked += 1
        assert fast_mcd_raw(pts, h, starts=None)[0] == best
    assert checked >= 10


def test_random_starts_match_enumeration_on_most_sets():
    """Measured: 30 random starts find the exact optimum on most small sets, not on all."""
    rng = random.Random(2)
    hits = total = 0
    for t in range(12):
        n = rng.randint(6, 11)
        pts = random_data(rng, n, rng.randint(0, (n - 1) // 2))
        h = default_h(n, 2)
        best, _ = exact_mcd(pts, h)
        got = fast_mcd_raw(pts, h, starts=30, seed=t)[0]
        assert got >= best
        total += 1
        hits += got == best
    assert hits >= total - 2


def test_c_step_never_increases_determinant():
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(5, 12)
        pts = random_data(rng, n, rng.randint(0, n // 3))
        h = rng.randint(3, n)
        h1 = sorted(rng.sample(range(n), h))
        mu1, s1 = mean(pts, h1), cov(pts, h1)
        d1 = det(s1)
        if d1 == 0:
            continue
        h2 = c_step(pts, h1, h)
        mu2, s2 = mean(pts, h2), cov(pts, h2)
        d2 = det(s2)
        assert d2 <= d1
        # The two inequalities of the proof, exactly.
        s1_inv = inverse(s1)
        tr = sum(s1_inv[a][b] * s2[b][a] for a in range(2) for b in range(2))
        assert tr + mahalanobis2(mu2, mu1, s1_inv) <= 2
        assert d2 / d1 <= (tr / 2) ** 2
        if d2 == d1:
            assert mu2 == mu1 and s2 == s1


def test_optimum_is_a_c_step_fixed_point():
    rng = random.Random(4)
    for _ in range(6):
        n = rng.randint(6, 10)
        pts = random_data(rng, n, 2)
        h = default_h(n, 2)
        best, idx = exact_mcd(pts, h)
        if best == 0:
            continue
        new = c_step(pts, idx, h)
        assert det(cov(pts, new)) == best
        assert mean(pts, new) == mean(pts, idx)


def test_affine_equivariance():
    pts = exact(EXAMPLE)
    a = [[F(2), F(1)], [F(-1), F(3)]]
    b = [F(5), F(-7)]
    moved = [tuple(sum(a[i][j] * x[j] for j in range(2)) + b[i] for i in range(2)) for x in pts]
    d0, idx0, _, _ = fast_mcd_raw(pts, 6, starts=None)
    d1, idx1, _, _ = fast_mcd_raw(moved, 6, starts=None)
    assert idx1 == idx0
    assert d1 == det(a) ** 2 * d0


def test_consistency_factor_closed_form_for_two_dimensions():
    # For p = 2: chi2_{2, alpha} = -2 log(1 - alpha) and F_4(x) = 1 - exp(-x/2)(1 + x/2).
    for alpha in [0.5, 0.6, 0.75, 0.9, 0.975]:
        want = alpha / (1.0 - (1.0 - alpha) * (1.0 - math.log(1.0 - alpha)))
        assert consistency_factor(alpha, 2) == pytest.approx(want, rel=1e-10)
    assert consistency_factor(0.5, 2) == pytest.approx(3.2589, abs=1e-4)


def test_flags_outliers_where_the_mean_fails():
    """Measured: 80 normal points in 3 dimensions and 20 points shifted by 6 in every coordinate."""
    rng = random.Random(5)
    clean = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(80)]
    far = [[rng.gauss(6, 0.5) for _ in range(3)] for _ in range(20)]
    r = mcd(clean + far, starts=60, seed=1)
    assert all(r["outlier"][80:])
    assert sum(r["outlier"][:80]) <= 6
    err_mcd = math.sqrt(sum(v * v for v in r["location"]))
    sample_mean = [sum(x[j] for x in clean + far) / 100 for j in range(3)]
    err_mean = math.sqrt(sum(v * v for v in sample_mean))
    assert err_mean > 1.8
    assert err_mcd < 0.4


def test_consistency_on_clean_normal_data():
    """Measured: the corrected raw scatter has a determinant near 1; the reweighted scatter is near I."""
    rng = random.Random(6)
    pts = [[rng.gauss(0, 1), rng.gauss(0, 1)] for _ in range(600)]
    r = mcd(pts, starts=10, seed=0)
    assert abs(det(r["raw_scatter"]) - 1) < 0.2  # the raw shape is noisy: diagonal 1.32 and 0.68
    s = r["scatter"]
    assert abs(s[0][0] - 1) < 0.2 and abs(s[1][1] - 1) < 0.2 and abs(s[0][1]) < 0.15
    c = consistency_factor(default_h(600, 2) / 600, 2)
    assert det(r["raw_scatter"]) / c**2 < 0.15  # without the factor the scatter is far too small


def test_exact_fit_gives_zero_determinant():
    pts = exact([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (0, 7), (6, 1)])
    d, idx, _, _ = fast_mcd_raw(pts, 5, starts=None)
    assert d == 0
    assert all(pts[i][0] == pts[i][1] for i in idx)


def test_errors():
    with pytest.raises(ValueError):
        fast_mcd_raw(exact(EXAMPLE), h=2)
    with pytest.raises(ValueError):
        fast_mcd_raw(exact(EXAMPLE), h=11)
