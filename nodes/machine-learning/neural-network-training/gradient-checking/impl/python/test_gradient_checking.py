# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gradient-checking/. The authors are listed in prov/3WZDG5.jsonl.

import math
import random

from gradient_checking import EPS, check_gradient, default_step, numerical_gradient, relative_error

F = lambda t: math.sin(t[0]) * math.exp(t[0])
X = 0.7
D = (math.cos(X) + math.sin(X)) * math.exp(X)


def err(h, scheme):
    return abs(numerical_gradient(F, [X], h, scheme)[0] - D)


def test_forward_difference_is_first_order():
    # halving h halves the error while truncation dominates: ratio about 2
    for h in (1e-2, 1e-3, 1e-4):
        ratio = err(h, "forward") / err(h / 2, "forward")
        assert 1.9 < ratio < 2.1, (h, ratio)
    # and the error is close to (h / 2) |f''(x)|
    f2 = 2 * math.cos(X) * math.exp(X)
    assert math.isclose(err(1e-4, "forward"), 0.5e-4 * f2, rel_tol=1e-3)


def test_central_difference_is_second_order():
    # halving h divides the error by about 4
    for h in (1e-1, 1e-2, 1e-3):
        ratio = err(h, "central") / err(h / 2, "central")
        assert 3.9 < ratio < 4.1, (h, ratio)
    f3 = 2 * (math.cos(X) - math.sin(X)) * math.exp(X)
    assert math.isclose(err(1e-3, "central"), 1e-6 / 6 * abs(f3), rel_tol=1e-3)


def test_default_steps_balance_rounding_and_truncation():
    assert math.isclose(default_step("central"), EPS ** (1 / 3))
    assert math.isclose(default_step("forward"), EPS ** 0.5)
    c = err(None, "central")
    fw = err(None, "forward")
    assert c < 1e-10 and fw < 1e-7 and c < fw
    # a far larger or far smaller step is worse
    assert c < err(1e-3, "central") and c < err(1e-10, "central")
    assert c < err(1e-12, "central")


def test_correct_gradient_passes_and_bug_is_caught():
    rng = random.Random(5)
    A = [[rng.uniform(-1, 1) for _ in range(4)] for _ in range(4)]

    def f(t):  # log-sum-exp of A t
        z = [sum(a * v for a, v in zip(row, t)) for row in A]
        m = max(z)
        return m + math.log(sum(math.exp(v - m) for v in z))

    def grad(t, bug=False):
        z = [sum(a * v for a, v in zip(row, t)) for row in A]
        m = max(z)
        e = [math.exp(v - m) for v in z]
        p = [v / sum(e) for v in e]
        if bug:
            p = e  # forgot to normalize the softmax
        return [sum(p[i] * A[i][j] for i in range(4)) for j in range(4)]

    for _ in range(20):
        t = [rng.uniform(-2, 2) for _ in range(4)]
        ok, worst, _ = check_gradient(f, grad, t, tol=1e-7)
        assert ok, worst
        ok, worst, _ = check_gradient(f, lambda s: grad(s, True), t, tol=1e-7)
        assert not ok and worst > 1e-3


def test_relu_kink_gives_false_alarm():
    relu = lambda t: max(t[0], 0.0)
    drelu = lambda t: [1.0 if t[0] > 0 else 0.0]
    # the kink at 0 is inside [t - h, t + h]: the check fails on a correct gradient
    ok, worst, _ = check_gradient(relu, drelu, [1e-7], tol=1e-4, h=1e-5)
    assert not ok and math.isclose(worst, 0.495, rel_tol=1e-6)
    # the same gradient passes when the kink is farther than h
    ok, worst, _ = check_gradient(relu, drelu, [1e-3], tol=1e-4, h=1e-5)
    assert ok and worst < 1e-9


def test_relative_error():
    assert relative_error(0.0, 0.0) == 0.0
    assert relative_error(1.0, 1.0) == 0.0
    assert math.isclose(relative_error(1.0, 1.1), 0.1 / 1.1)
    assert relative_error(1e-20, -1e-20) == 2.0
