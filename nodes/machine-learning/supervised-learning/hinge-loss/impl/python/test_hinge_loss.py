# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hinge-loss/. The authors are listed in prov/12NTY4.jsonl.

import random

from hinge_loss import (conditional_risk, crammer_singer, crammer_singer_subgradient, dot, hinge,
                        hinge_subgradient, squared_hinge, squared_hinge_derivative, weston_watkins,
                        weston_watkins_subgradient)


def test_worked_values() -> None:
    assert [hinge(1, m) for m in (-2, -1, 0, 0.5, 1, 2)] == [3, 2, 1, 0.5, 0, 0]
    assert squared_hinge(1, 0.5) == 0.25
    assert squared_hinge(-1, 0.5) == 2.25
    f = [1.0, 0.5, 0.8]
    assert abs(weston_watkins(f, 0) - 1.3) < 1e-12
    assert abs(crammer_singer(f, 0) - 0.8) < 1e-12
    assert abs(weston_watkins([3.2, 5.1, -1.7], 0) - 2.9) < 1e-12
    assert abs(crammer_singer([3.2, 5.1, -1.7], 0) - 2.9) < 1e-12
    assert crammer_singer([3.0, 1.0, 0.5], 0) == 0.0


def test_subgradient_inequality() -> None:
    r = random.Random(2)
    for _ in range(2000):
        d = r.randint(1, 4)
        x = [r.uniform(-2, 2) for _ in range(d)]
        y = r.choice((-1, 1))
        w = [r.uniform(-2, 2) for _ in range(d)]
        g = hinge_subgradient(w, x, y)
        v = [r.uniform(-2, 2) for _ in range(d)]
        lhs = hinge(y, dot(v, x))
        rhs = hinge(y, dot(w, x)) + dot(g, [a - b for a, b in zip(v, w)])
        assert lhs >= rhs - 1e-12


def test_kink_subgradients_are_valid() -> None:
    r = random.Random(12)
    x = [1.0, 2.0]
    w = [1.0, 0.0]  # y w.x = 1 for y = +1
    for c in (0.0, 0.3, 1.0):
        g = hinge_subgradient(w, x, 1, c)
        for _ in range(300):
            v = [r.uniform(-3, 3), r.uniform(-3, 3)]
            assert hinge(1, dot(v, x)) >= hinge(1, dot(w, x)) + dot(g, [a - b for a, b in zip(v, w)]) - 1e-12


def test_squared_hinge_derivative() -> None:
    r = random.Random(4)
    h = 1e-6
    for _ in range(500):
        f = r.uniform(-3, 3)
        y = r.choice((-1, 1))
        fd = (squared_hinge(y, f + h) - squared_hinge(y, f - h)) / (2 * h)
        assert abs(fd - squared_hinge_derivative(y, f)) < 1e-5


def test_conditional_risk_minimizer_is_sign_of_2eta_minus_1() -> None:
    grid = [i / 100 for i in range(-300, 301)]
    for k in range(0, 101):
        eta = k / 100
        best = min(conditional_risk(eta, a) for a in grid)
        argmins = [a for a in grid if conditional_risk(eta, a) <= best + 1e-12]
        if eta > 0.5:
            assert argmins == [1.0] or (eta == 1 and min(argmins) == 1.0)
        elif eta < 0.5:
            assert argmins == [-1.0] or (eta == 0 and max(argmins) == -1.0)
        else:
            assert min(argmins) == -1.0 and max(argmins) == 1.0
        assert abs(best - 2 * min(eta, 1 - eta)) < 1e-12


def test_multiclass_relations() -> None:
    r = random.Random(7)
    for _ in range(2000):
        k = r.randint(2, 6)
        f = [r.uniform(-3, 3) for _ in range(k)]
        y = r.randrange(k)
        cs, ww = crammer_singer(f, y), weston_watkins(f, y)
        assert cs <= ww + 1e-12
        assert ww <= (k - 1) * cs + 1e-12
        if k == 2:
            assert abs(cs - hinge(1, f[y] - f[1 - y])) < 1e-12
            assert abs(ww - cs) < 1e-12


def test_multiclass_subgradients() -> None:
    r = random.Random(9)
    for _ in range(1000):
        k = r.randint(2, 5)
        f = [r.uniform(-2, 2) for _ in range(k)]
        y = r.randrange(k)
        g1, g2 = crammer_singer_subgradient(f, y), weston_watkins_subgradient(f, y)
        for _ in range(5):
            v = [r.uniform(-2, 2) for _ in range(k)]
            dv = [a - b for a, b in zip(v, f)]
            assert crammer_singer(v, y) >= crammer_singer(f, y) + dot(g1, dv) - 1e-12
            assert weston_watkins(v, y) >= weston_watkins(f, y) + dot(g2, dv) - 1e-12
