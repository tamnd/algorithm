# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dimer-method/. The authors are listed in prov/JXAQP4.jsonl.
import math
import random

import pytest

from dimer_method import curvature, dimer_method, muller_brown, rotate

C_MIN = [-0.05001, 0.46669]
S1 = (-0.82200, 0.62431, -40.6648)
S2 = (0.21249, 0.29299, -72.2489)


def quadratic(p):
    # V = (3 x^2 + 2 x y - y^2) / 2, Hessian [[3, 1], [1, -1]], eigenvalues 1 +- sqrt(5).
    x, y = p
    return 0.5 * (3.0 * x * x + 2.0 * x * y - y * y), [3.0 * x + y, x - y]


def hessian_fd(potential, p, e=1e-5):
    h = [[0.0, 0.0], [0.0, 0.0]]
    for j in range(2):
        q1 = list(p)
        q2 = list(p)
        q1[j] += e
        q2[j] -= e
        g1 = potential(q1)[1]
        g2 = potential(q2)[1]
        for i in range(2):
            h[i][j] = (g1[i] - g2[i]) / (2.0 * e)
    return h


def eig2(h):
    t = h[0][0] + h[1][1]
    d = h[0][0] * h[1][1] - h[0][1] * h[1][0]
    s = math.sqrt(t * t / 4.0 - d)
    return t / 2.0 - s, t / 2.0 + s


def test_curvature_is_the_rayleigh_quotient_for_a_quadratic():
    p = [0.3, 0.2]
    g0 = quadratic(p)[1]
    c, _ = curvature(quadratic, p, [1.0, 0.0], 1e-3, g0)
    assert c == pytest.approx(3.0, abs=1e-9)
    n = [1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0)]
    c, _ = curvature(quadratic, p, n, 1e-3, g0)
    assert c == pytest.approx((3.0 + 2.0 - 1.0) / 2.0, abs=1e-9)


def test_one_rotation_finds_the_lowest_mode_of_a_quadratic():
    p = [0.3, 0.2]
    n, c, c0, f_rot = rotate(quadratic, p, [1.0, 0.0], 1e-3, quadratic(p)[1])
    lam = 1.0 - math.sqrt(5.0)
    assert c0 == pytest.approx(3.0, abs=1e-9)
    assert c == pytest.approx(lam, abs=1e-9)
    # n is an eigenvector: H n = lam n.
    hn = [3.0 * n[0] + n[1], n[0] - n[1]]
    assert hn == pytest.approx([lam * n[0], lam * n[1]], abs=1e-8)


def test_translation_converges_to_the_saddle_of_a_quadratic():
    r, n, c, it, ok = dimer_method(quadratic, [0.3, 0.2], [1.0, 0.0], 1e-3, 0.2, 1e-10)
    assert ok and it < 200
    assert r == pytest.approx([0.0, 0.0], abs=1e-9)
    assert c == pytest.approx(1.0 - math.sqrt(5.0), abs=1e-9)


def test_searches_from_muller_brown_minimum_c_find_both_saddles():
    rng = random.Random(1)
    found = {"S1": 0, "S2": 0}
    for _ in range(20):
        r0 = [C_MIN[0] + rng.gauss(0.0, 0.05), C_MIN[1] + rng.gauss(0.0, 0.05)]
        a = rng.uniform(0.0, 2.0 * math.pi)
        r, n, c, it, ok = dimer_method(muller_brown, r0, [math.cos(a), math.sin(a)], 1e-4, 1e-3, 1e-6)
        assert ok and it < 500
        name = "S1" if r[0] < -0.4 else "S2"
        s = S1 if name == "S1" else S2
        found[name] += 1
        assert r == pytest.approx(list(s[:2]), abs=1e-5)
        assert muller_brown(r)[0] == pytest.approx(s[2], abs=1e-4)
        # A first-order saddle: one negative eigenvalue, and c is it.
        lo, hi = eig2(hessian_fd(muller_brown, r))
        assert lo < 0.0 < hi
        assert c == pytest.approx(lo, rel=1e-3)
    assert found == {"S1": 6, "S2": 14}
