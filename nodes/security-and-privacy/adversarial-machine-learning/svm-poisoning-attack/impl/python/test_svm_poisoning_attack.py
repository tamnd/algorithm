# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/svm-poisoning-attack/. The authors are listed in prov/VZRNHS.jsonl.

"""Tests of the SVM poisoning attack on seeded synthetic blobs: a duality certificate, finite differences, a measurement."""

import math
import random

from svm_poisoning_attack import dot, error_rate, hinge_total, kkt_violation, poison, poison_gradient, train_svm


def blobs(rng: random.Random, per_class: int, d: int, shift: float, sigma: float) -> tuple[list[list[float]], list[int]]:
    xs, ys = [], []
    for i in range(2 * per_class):
        y = 1 if i % 2 == 0 else -1
        xs.append([(y * shift if j == 0 else 0.0) + rng.gauss(0.0, sigma) for j in range(d)])
        ys.append(y)
    return xs, ys


def primal(xs, ys, w, b, c) -> float:
    return 0.5 * dot(w, w) + c * math.fsum(max(0.0, 1.0 - y * (dot(w, x) + b)) for x, y in zip(xs, ys))


def dual(alpha, w) -> float:
    return math.fsum(alpha) - 0.5 * dot(w, w)


def test_svm_solution_has_zero_duality_gap() -> None:
    """Weak duality: D(alpha) <= P* <= P(w, b) for feasible alpha, so a zero gap certifies the optimum."""
    rng = random.Random(6201)
    for _ in range(500):
        n, d = rng.randint(2, 10), rng.randint(1, 3)
        xs = [[rng.uniform(-2.0, 2.0) for _ in range(d)] for _ in range(n)]
        ys = [1, -1] + [rng.choice([1, -1]) for _ in range(n - 2)]
        c = rng.choice([0.1, 1.0, 10.0])
        m = train_svm(xs, ys, c)
        assert all(-1e-12 <= a <= c + 1e-12 for a in m.alpha)
        assert abs(math.fsum(a * y for a, y in zip(m.alpha, ys))) < 1e-9
        w = [math.fsum(m.alpha[i] * ys[i] * xs[i][j] for i in range(n)) for j in range(d)]
        assert all(abs(a - b) < 1e-12 for a, b in zip(w, m.w))
        p, q = primal(xs, ys, m.w, m.b, c), dual(m.alpha, m.w)
        assert p - q <= 1e-7 * (1.0 + abs(p)), (p, q)
        assert kkt_violation(xs, ys, m, c) < 1e-6


def test_gradient_matches_finite_differences() -> None:
    rng = random.Random(6202)
    checked = nonzero = 0
    for _ in range(60):
        d = rng.randint(2, 5)
        xs, ys = blobs(rng, 6, d, 1.5, math.sqrt(0.6))
        val = list(zip(*blobs(rng, 10, d, 1.5, math.sqrt(0.6))))
        k = rng.randrange(len(xs) // 2) * 2 + 1  # a point of class -1
        xc = [a + rng.gauss(0.0, 0.3) for a in xs[k]]
        allx, ally = xs + [xc], ys + [1]
        m = train_svm(allx, ally, 1.0)
        if len(allx) - 1 in m.margin or not m.margin:
            continue
        try:
            g = poison_gradient(allx, ally, m, 1.0, val)
        except ValueError:
            continue
        h = 1e-5
        ok = True
        fd = []
        for j in range(d):
            vals = []
            for sgn in (1.0, -1.0):
                moved = list(xc)
                moved[j] += sgn * h
                mm = train_svm(xs + [moved], ally, 1.0)
                same_sets = mm.margin == m.margin and mm.error == m.error
                same_val = all((1 - y * (dot(mm.w, x) + mm.b) > 0) == (1 - y * (dot(m.w, x) + m.b) > 0) for x, y in val)
                ok = ok and same_sets and same_val
                vals.append(hinge_total(mm, val))
            fd.append((vals[0] - vals[1]) / (2 * h))
        if not ok:
            continue
        checked += 1
        nonzero += max(abs(a) for a in g) > 1e-6
        assert all(abs(a - b) <= 1e-5 * (1.0 + abs(b)) for a, b in zip(g, fd)), (g, fd)
    assert checked >= 30 and nonzero >= 15, (checked, nonzero)


EX_X = [[-2.0, 0.0], [2.0, 0.0], [-2.0, 1.0], [2.0, 1.0]]
EX_Y = [-1, 1, -1, 1]
EX_VAL = [([-1.0, 0.0], -1), ([1.0, 0.0], 1), ([-1.0, 1.0], -1), ([1.0, 1.0], 1)]


def test_example_of_the_page() -> None:
    clean = train_svm(EX_X, EX_Y, 0.1)
    assert abs(clean.w[0] - 0.5) < 1e-12 and abs(clean.w[1]) < 1e-12 and abs(clean.b) < 1e-12
    assert abs(hinge_total(clean, EX_VAL) - 2.0) < 1e-12 and error_rate(clean, EX_VAL) == 0.0
    for a in (-2.0, -2.5, -3.0, -5.0):
        m = train_svm(EX_X + [[a, 0.5]], EX_Y + [1], 0.1)
        assert m.margin == [1, 3] and m.error == [0, 2, 4]
        assert abs(m.w[0] - (0.6 + 0.1 * a)) < 1e-12 and abs(m.w[1]) < 1e-12 and abs(m.b - (-0.2 - 0.2 * a)) < 1e-12
        assert abs(hinge_total(m, EX_VAL) - (2.4 - 0.4 * (a + 2.0))) < 1e-12
        g = poison_gradient(EX_X + [[a, 0.5]], EX_Y + [1], m, 0.1, EX_VAL)
        assert abs(g[0] + 0.4) < 1e-12 and abs(g[1]) < 1e-12
        assert error_rate(m, EX_VAL) == (0.5 if a < -8.0 / 3.0 else 0.0)
    xc, losses = poison(EX_X, EX_Y, EX_VAL, 0.1, [-2.0, 0.5], 1, 0.5, -5.0, 5.0, 20, 1e-9)
    assert xc == [-5.0, 0.5] and [round(t, 9) for t in losses] == [2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.6]


def test_flat_region_when_the_margin_set_has_d_plus_one_points() -> None:
    """With a linear kernel and |S| = d + 1, the margin equations fix w and b, so the gradient is zero."""
    rng = random.Random(6203)
    xs, ys = blobs(rng, 25, 2, 1.5, math.sqrt(0.6))
    val = list(zip(*blobs(rng, 250, 2, 1.5, math.sqrt(0.6))))
    m = train_svm(xs + [xs[1]], ys + [1], 1.0)
    assert len(m.margin) == 3
    g = poison_gradient(xs + [xs[1]], ys + [1], m, 1.0, val)
    assert max(abs(a) for a in g) < 1e-10


def test_one_point_raises_the_validation_error() -> None:
    """A measurement: the means (+-1.5, 0, ...) and covariance 0.6 I of Biggio et al., but d = 8 and 15 points per class, C = 1."""
    gains = []
    for seed in (6204, 6205, 6206, 6207):
        rng = random.Random(seed)
        xs, ys = blobs(rng, 15, 8, 1.5, math.sqrt(0.6))
        val = list(zip(*blobs(rng, 200, 8, 1.5, math.sqrt(0.6))))
        clean = train_svm(xs, ys, 1.0)
        # Clone a point of class -1 and flip its label.
        xc, losses = poison(xs, ys, val, 1.0, xs[1], 1, 0.5, -5.0, 5.0, 60, 1e-6)
        attacked = train_svm(xs + [xc], ys + [1], 1.0)
        assert losses[-1] > losses[0]
        assert all(-5.0 <= a <= 5.0 for a in xc)
        gains.append(error_rate(attacked, val) - error_rate(clean, val))
    assert min(gains) > 0.0 and sum(gains) / len(gains) >= 0.05
