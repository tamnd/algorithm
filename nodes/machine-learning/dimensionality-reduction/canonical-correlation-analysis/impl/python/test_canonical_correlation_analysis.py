# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/canonical-correlation-analysis/. The authors are listed in prov/2S7QFD.jsonl.

import math
import random

import pytest

from canonical_correlation_analysis import cca, centre, correlation, cross_cov


def paired_data(rng: random.Random, n: int, p: int, q: int, shared: int = 2) -> tuple[list, list]:
    """X and Y share `shared` latent signals, with different noise and mixing."""
    mx = [[rng.uniform(-1, 1) for _ in range(shared + p)] for _ in range(p)]
    my = [[rng.uniform(-1, 1) for _ in range(shared + q)] for _ in range(q)]
    xs, ys = [], []
    for _ in range(n):
        z = [rng.gauss(0, 1) for _ in range(shared)]
        ex = z + [rng.gauss(0, 1) for _ in range(p)]
        ey = z + [rng.gauss(0, 1) for _ in range(q)]
        xs.append([sum(a * b for a, b in zip(row, ex)) for row in mx])
        ys.append([sum(a * b for a, b in zip(row, ey)) for row in my])
    return xs, ys


def test_brute_force_first_pair_2d() -> None:
    rng = random.Random(1)
    for _ in range(3):
        xs, ys = paired_data(rng, 60, 2, 2)
        rho, a_dirs, b_dirs = cca(xs, ys)
        assert correlation(xs, ys, a_dirs[0], b_dirs[0]) == pytest.approx(rho[0], abs=1e-10)
        xc, yc = centre(xs), centre(ys)
        cxx, cyy, cxy = cross_cov(xc, xc), cross_cov(yc, yc), cross_cov(xc, yc)

        def form(u, m, v):
            return sum(u[i] * m[i][j] * v[j] for i in range(2) for j in range(2))

        angles = [math.pi * i / 600 for i in range(600)]
        units = [(math.cos(t), math.sin(t)) for t in angles]
        sx = [math.sqrt(form(a, cxx, a)) for a in units]
        sy = [math.sqrt(form(b, cyy, b)) for b in units]
        best = max(abs(form(a, cxy, b)) / (sx[i] * sy[j])
                   for i, a in enumerate(units) for j, b in enumerate(units))
        assert abs(correlation(xs, ys, units[0], units[1])) <= best
        assert rho[0] >= best - 1e-10
        assert rho[0] - best < 1e-3


def test_one_dimensional_case_is_absolute_correlation() -> None:
    rng = random.Random(2)
    xs, ys = paired_data(rng, 40, 1, 1)
    rho, _, _ = cca(xs, ys)
    assert rho[0] == pytest.approx(abs(correlation(xs, ys, [1.0], [1.0])), abs=1e-12)


def test_canonical_variates_are_uncorrelated() -> None:
    rng = random.Random(3)
    xs, ys = paired_data(rng, 80, 3, 4, shared=3)
    rho, a_dirs, b_dirs = cca(xs, ys)
    assert len(rho) == 3 and rho == sorted(rho, reverse=True) and rho[0] <= 1.0
    for i in range(3):
        for j in range(3):
            c_ab = correlation(xs, ys, a_dirs[i], b_dirs[j])
            assert c_ab == pytest.approx(rho[i] if i == j else 0.0, abs=1e-9)
            if i != j:
                assert correlation(xs, xs, a_dirs[i], a_dirs[j]) == pytest.approx(0.0, abs=1e-9)
                assert correlation(ys, ys, b_dirs[i], b_dirs[j]) == pytest.approx(0.0, abs=1e-9)


def test_invariance_under_linear_maps() -> None:
    rng = random.Random(4)
    xs, ys = paired_data(rng, 50, 3, 2)
    rho, _, _ = cca(xs, ys)
    g = [[2.0, 1.0, 0.0], [0.0, 1.0, -3.0], [1.0, 0.0, 1.0]]
    xs2 = [[sum(g[i][j] * x[j] for j in range(3)) + 5.0 for i in range(3)] for x in xs]
    rho2, _, _ = cca(xs2, ys)
    assert rho2 == pytest.approx(rho, abs=1e-9)
    rho3, _, _ = cca(ys, xs)
    assert rho3 == pytest.approx(rho, abs=1e-9)


def test_population_example_by_hand() -> None:
    # A model with the covariances of the page example: Var x = Var y = 1 per
    # coordinate, cov(x1, x2) = 0.6, cov(x1, y) = (0.5, 0.2), cov(x2, y) = 0.
    # Check the closed form rho_1 = sqrt(29) / 8 and a_1 proportional to (1, -0.6)
    # on a large sample.
    rng = random.Random(5)
    alpha = 0.6 / math.sqrt(0.71)
    beta = math.sqrt(1 - alpha * alpha)
    xs, ys = [], []
    for _ in range(20000):
        y1, y2, e, f = (rng.gauss(0, 1) for _ in range(4))
        xs.append([0.5 * y1 + 0.2 * y2 + math.sqrt(0.71) * e, alpha * e + beta * f])
        ys.append([y1, y2])
    rho, a_dirs, _ = cca(xs, ys)
    assert rho[0] == pytest.approx(math.sqrt(29) / 8, abs=0.02)
    assert rho[1] < 0.05
    a = a_dirs[0]
    assert a[1] / a[0] == pytest.approx(-0.6, abs=0.06)


def test_cca_with_class_indicators_gives_fisher_lda() -> None:
    # rho^2 = lambda / (1 + lambda), where lambda is a Fisher eigenvalue of (S_B, S_W).
    rng = random.Random(7)
    xs, labels = [], []
    for c, centre_c in enumerate([(0.0, 0.0), (2.0, 1.0), (0.5, 3.0)]):
        for _ in range(15):
            xs.append([centre_c[0] + rng.gauss(0, 1), centre_c[1] + 0.5 * rng.gauss(0, 1)])
            labels.append(c)
    ind = [[1.0 if c == 1 else 0.0, 1.0 if c == 2 else 0.0] for c in labels]
    rho, _, _ = cca(xs, ind)
    n = len(xs)
    mu = [sum(x[j] for x in xs) / n for j in range(2)]
    s_w = [[0.0, 0.0], [0.0, 0.0]]
    s_b = [[0.0, 0.0], [0.0, 0.0]]
    for c in range(3):
        pts = [x for x, y in zip(xs, labels) if y == c]
        m = [sum(p[j] for p in pts) / len(pts) for j in range(2)]
        for i in range(2):
            for j in range(2):
                s_w[i][j] += sum((p[i] - m[i]) * (p[j] - m[j]) for p in pts)
                s_b[i][j] += len(pts) * (m[i] - mu[i]) * (m[j] - mu[j])
    # Generalized eigenvalues of a 2 x 2 pencil: det(S_B - lam S_W) = 0.
    a2 = s_w[0][0] * s_w[1][1] - s_w[0][1] ** 2
    a1 = -(s_b[0][0] * s_w[1][1] + s_b[1][1] * s_w[0][0] - 2 * s_b[0][1] * s_w[0][1])
    a0 = s_b[0][0] * s_b[1][1] - s_b[0][1] ** 2
    disc = math.sqrt(a1 * a1 - 4 * a2 * a0)
    lams = sorted([(-a1 + disc) / (2 * a2), (-a1 - disc) / (2 * a2)], reverse=True)
    assert [r * r for r in rho] == pytest.approx([lam / (1 + lam) for lam in lams], abs=1e-10)


def test_small_n_overfits_and_ridge_fixes_singularity() -> None:
    rng = random.Random(6)
    xs = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(5)]
    ys = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(5)]
    rho, _, _ = cca(xs, ys)
    # Centred columns live in a 4-dimensional space and 3 + 3 > 4, so two correlations are 1.
    assert rho[0] == pytest.approx(1.0, abs=1e-8) and rho[1] == pytest.approx(1.0, abs=1e-8)
    xs4 = [[rng.gauss(0, 1) for _ in range(6)] for _ in range(5)]
    with pytest.raises(ValueError):
        cca(xs4, ys)
    rho_r, a_r, b_r = cca(xs4, ys, kx=0.5, ky=0.5)
    assert all(0.0 <= r < 1.0 for r in rho_r)
    xc = centre(xs4)
    cxx = cross_cov(xc, xc)
    a = a_r[0]
    norm = sum(a[i] * (cxx[i][j] + (0.5 if i == j else 0.0)) * a[j] for i in range(6) for j in range(6))
    assert norm == pytest.approx(1.0, abs=1e-9)
