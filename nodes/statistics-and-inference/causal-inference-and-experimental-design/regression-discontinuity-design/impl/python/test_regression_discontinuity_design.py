# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/regression-discontinuity-design/. The authors are listed in prov/QMX934.jsonl.

import math
import random
from fractions import Fraction as Fr

import pytest

from regression_discontinuity_design import (
    local_weights,
    pooled_fit,
    rdd,
    rdd_fuzzy,
    triangular,
    wls,
)


def test_worked_example():
    x = [Fr(v, 2) for v in (-5, -3, -2, -1, 0, 1, 2, 3, 5)]
    y = [Fr(v) for v in (2, 1, 3, 2, 6, 5, 7, 6, 9)]
    r = rdd(x, y, 0, 2)
    assert r.left == (Fr(5, 2), Fr(2, 5)) and r.right == (Fr(57, 10), Fr(2, 5))
    assert r.tau == Fr(16, 5) and (r.n_left, r.n_right) == (3, 4)
    assert pooled_fit(x, y, 0, 2) == [Fr(5, 2), Fr(16, 5), Fr(2, 5), 0]


def random_case(rng):
    n = rng.randint(8, 20)
    x = [Fr(rng.randint(-20, 20), 4) for _ in range(n)]
    x += [Fr(-1), Fr(-2), Fr(0), Fr(1)]  # two distinct values on each side inside h >= 3
    y = [Fr(rng.randint(-9, 9)) for _ in x]
    return x, y, Fr(rng.randint(3, 6))


def test_local_linear_equals_direct_wls_exactly():
    """Closed-form side fits agree with solving the weighted normal equations, and the jump equals
    the coefficient of T in the pooled WLS with separate slopes."""
    rng = random.Random(1)
    for _ in range(60):
        x, y, h = random_case(rng)
        r = rdd(x, y, 0, h)
        for right, fit in ((False, r.left), (True, r.right)):
            rows, yy, ww = [], [], []
            for a, b in zip(x, y):
                w = triangular(a / h)
                if (a >= 0) == right and w > 0:
                    rows.append([Fr(1), a])
                    yy.append(b)
                    ww.append(w)
            assert tuple(wls(rows, yy, ww)) == fit
        assert pooled_fit(x, y, 0, h)[1] == r.tau


def test_local_weights_reproduce_lines():
    """sum l_i = 1 and sum l_i v_i = 0, so the intercept of an exact line is returned exactly."""
    rng = random.Random(2)
    for _ in range(60):
        v = [Fr(rng.randint(0, 30), 7) for _ in range(rng.randint(3, 10))] + [Fr(0), Fr(1, 3)]
        w = [triangular(a / 5) for a in v]
        lw = local_weights(v, w)
        assert sum(lw) == 1
        assert sum(a * b for a, b in zip(lw, v)) == 0


def test_sharp_design_recovers_the_jump_of_piecewise_lines():
    """Noise-free y = a + b v + T (tau + g v): any bandwidth returns tau exactly."""
    rng = random.Random(3)
    for _ in range(40):
        x, _, h = random_case(rng)
        a, b, g, tau = (Fr(rng.randint(-9, 9), rng.randint(1, 3)) for _ in range(4))
        y = [a + b * v + (tau + g * v if v >= 0 else 0) for v in x]
        r = rdd(x, y, 0, h)
        assert r.tau == tau and r.se == 0


def test_fuzzy_design_exact_ratio():
    """y = a + b v + tau d with d jumping at the cutoff: the ratio of jumps is tau exactly."""
    rng = random.Random(4)
    done = 0
    while done < 40:
        x, _, h = random_case(rng)
        d = [Fr(int(rng.random() < (0.8 if v >= 0 else 0.2))) for v in x]
        a, b, tau = (Fr(rng.randint(-9, 9), rng.randint(1, 3)) for _ in range(3))
        y = [a + b * v + tau * di for v, di in zip(x, d)]
        try:
            est, se, jy, jd = rdd_fuzzy(x, y, d, 0, h)
        except ZeroDivisionError:
            continue
        assert est == tau and jy == tau * jd
        done += 1


def simulate(rng, n, h, extra_curvature):
    x = [rng.uniform(-1, 1) for _ in range(n)]
    y = [
        0.5 + 0.8 * a + 0.6 * a * a + (1.0 + extra_curvature * a * a if a >= 0 else 0.0) + rng.gauss(0, 0.3)
        for a in x
    ]
    return rdd(x, y, 0.0, h)


def test_monte_carlo_bias_and_coverage():
    """x uniform on (-1, 1), true jump 1, noise sd 0.3, n = 1000, h = 0.4, r = 300 per design.
    Same curvature on both sides: mean within 4 SE of 1, coverage within 0.95 +- (4 SE + 0.02).
    Curvature larger by 4 on the right: the triangular-kernel boundary bias is -(h^2/20) 4 = -0.032,
    and the mean is within 4 SE + 0.01 of 0.968."""
    for extra, target, seed in ((0.0, 1.0, 2026), (2.0, 1.0 - 0.032, 7)):
        rng = random.Random(seed)
        est, cover = [], 0
        for _ in range(300):
            res = simulate(rng, 1000, 0.4, extra)
            est.append(res.tau)
            cover += abs(res.tau - 1) <= 1.96 * res.se
        m = sum(est) / 300
        sd = math.sqrt(sum((v - m) ** 2 for v in est) / 299)
        assert abs(m - target) < 4 * sd / math.sqrt(300) + (0.01 if extra else 0.0)
        if not extra:
            assert abs(cover / 300 - 0.95) < 4 * math.sqrt(0.95 * 0.05 / 300) + 0.02


def test_input_checks():
    with pytest.raises(ValueError):
        rdd([1, 2], [1], 0, 1)
    with pytest.raises(ValueError):
        rdd([-1, 1, 2], [1, 2, 3], 0, 0)
    with pytest.raises(ValueError):
        rdd([-0.5, 0.5, 0.7], [1, 2, 3], 0, 1)  # one point on the left
