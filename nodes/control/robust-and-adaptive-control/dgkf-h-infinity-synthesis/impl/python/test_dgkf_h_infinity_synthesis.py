# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dgkf-h-infinity-synthesis/. The authors are listed in prov/DM08Z2.jsonl.

import math
import random

import ctlmat as cm
from dgkf_h_infinity_synthesis import (
    central_controller,
    closed_loop,
    dgkf_synthesis,
    freq_gain,
    gamma_feasible,
    is_hurwitz,
    matrix_sign,
    optimal_gamma,
    riccati,
    spectral_radius,
)


def scalar_plant(a):
    # x' = a x + w1 + u, z = (x, u), y = x + w2
    return {"A": [[a]], "B1": [[1, 0]], "B2": [[1]], "C1": [[1], [0]],
            "C2": [[1]], "D12": [[0], [1]], "D21": [[0, 1]]}


# Second-order plant with an unstable pole at s = 1.
PLANT2 = {"A": [[0, 1], [2, -1]], "B1": [[1, 0, 0], [0, 1, 0]],
          "B2": [[0], [1]], "C1": [[1, 0], [0, 1], [0, 0]],
          "C2": [[1, 0]], "D12": [[0], [0], [1]], "D21": [[0, 0, 1]]}

FREQS = [10 ** (e / 40) for e in range(-160, 161)]


def peak(sys):
    return max(freq_gain(sys, w) for w in FREQS + [0.0])


def test_ctlmat_self_test():
    assert cm._self_test()


def test_normalizations_of_the_examples():
    for p in (scalar_plant(0), PLANT2):
        d12, c1, b1, d21 = p["D12"], p["C1"], p["B1"], p["D21"]
        m = len(d12[0])
        assert cm.mul(cm.transpose(d12), c1) == cm.zeros(m, len(c1[0]))
        assert cm.mul(cm.transpose(d12), d12) == cm.eye(m)
        assert cm.mul(b1, cm.transpose(d21)) == cm.zeros(len(b1), len(d21))
        assert cm.mul(d21, cm.transpose(d21)) == cm.eye(len(d21))


def test_matrix_sign_of_a_diagonalizable_matrix():
    h = [[1.0, 2.0], [0.0, -3.0]]
    s = matrix_sign(h)
    # sign(H) = V diag(1, -1) V^-1 with V = [[1, 1], [0, -2]].
    want = [[1.0, 1.0], [0.0, -1.0]]
    assert max(abs(s[i][j] - want[i][j]) for i in range(2) for j in range(2)) < 1e-12
    assert matrix_sign([[0.0, 1.0], [-1.0, 0.0]]) is None


def test_riccati_against_the_scalar_formula():
    # a^T x + x a + x r x + q = 0 with r < 0 has the stabilizing root below.
    for a, r, q in ((0.0, -1.0, 1.0), (1.0, -0.5, 2.0), (-2.0, -3.0, 0.5)):
        x = riccati([[a]], [[r]], [[q]])[0][0]
        want = (-a - math.sqrt(a * a - r * q)) / r
        assert abs(x - want) < 1e-10 * (1 + abs(want))
        assert a + r * x < 0


def test_riccati_residual_and_closed_loop_on_plant2():
    g = 8.0
    ok, x, y = gamma_feasible(PLANT2, g)
    assert ok
    a = [[float(v) for v in row] for row in PLANT2["A"]]
    b1, b2, c1 = PLANT2["B1"], PLANT2["B2"], PLANT2["C1"]
    r = cm.sub(cm.scale(1 / g ** 2, cm.mul(b1, cm.transpose(b1))), cm.mul(b2, cm.transpose(b2)))
    res = cm.add(cm.add(cm.mul(cm.transpose(a), x), cm.mul(x, a)),
                 cm.add(cm.mul(cm.mul(x, r), x), cm.mul(cm.transpose(c1), c1)))
    assert max(abs(v) for row in res for v in row) < 1e-9
    assert cm.is_symmetric(x, 1e-12) and cm.is_pos_def(x)
    assert cm.is_pos_def(y)
    assert is_hurwitz(cm.add(a, cm.mul(r, x)))
    assert spectral_radius(cm.mul(x, y)) < g * g


def test_optimal_gamma_matches_the_closed_form():
    # For the scalar plant the three conditions give gamma_opt = a + sqrt(a^2 + 2).
    for a in (-1, 0, 1, 2):
        g = optimal_gamma(scalar_plant(a), rtol=1e-7)
        assert abs(g - (a + math.sqrt(a * a + 2))) < 1e-6 * g


def test_conditions_fail_below_and_hold_above_the_optimum():
    for p in (scalar_plant(1), PLANT2):
        g = optimal_gamma(p)
        assert not gamma_feasible(p, 0.99 * g)[0]
        assert gamma_feasible(p, 1.01 * g)[0]


def test_central_controller_meets_the_bound():
    for p in (scalar_plant(-1), scalar_plant(0), scalar_plant(2), PLANT2):
        gopt, g, k = dgkf_synthesis(p)
        cl = closed_loop(p, k)
        assert is_hurwitz(cl[0])
        pk = peak(cl)
        assert pk < g
        assert pk >= gopt * (1 - 1e-4)


def test_central_controller_at_a_loose_level():
    g = 3 * optimal_gamma(PLANT2)
    cl = closed_loop(PLANT2, central_controller(PLANT2, g))
    assert is_hurwitz(cl[0])
    assert peak(cl) < g


def _peak_scalar(a, k1, k0, p):
    # Closed loop of the scalar plant with K(s) = (k1 s + k0) / (s + p),
    # written with D = s - a - K so that s = a gives no division by zero.
    # The largest singular value of the 2 by 2 matrix comes from its
    # Frobenius norm and its determinant.
    best = 0.0
    for w in FREQS + [0.0]:
        s = 1j * w
        k = (k1 * s + k0) / (s + p)
        dd = s - a - k
        t = [[1 / dd, k / dd], [k / dd, k * (s - a) / dd]]
        f = sum(abs(v) ** 2 for row in t for v in row)
        dt = abs(t[0][0] * t[1][1] - t[0][1] * t[1][0])
        best = max(best, math.sqrt((f + math.sqrt(max(f * f - 4 * dt * dt, 0.0))) / 2))
    return best


def test_no_first_order_controller_beats_the_optimum():
    rng = random.Random(7)
    for a in (0, 1):
        p = scalar_plant(a)
        gopt = a + math.sqrt(a * a + 2)
        found = 0
        best = math.inf
        for _ in range(150):
            k1 = rng.uniform(-3, 1)
            k0 = rng.uniform(-8, 1)
            pole = rng.uniform(0.01, 10)
            k = ([[-pole]], [[1]], [[k0 - k1 * pole]], [[k1]])
            cl = closed_loop(p, k)
            if not is_hurwitz(cl[0]):
                continue
            found += 1
            best = min(best, _peak_scalar(a, k1, k0, pole))
        assert found > 20
        assert best >= gopt * (1 - 1e-3)
        assert best < 2 * gopt


def test_both_sweeps_agree():
    p = scalar_plant(1)
    k = ([[-2.0]], [[1.0]], [[-3.0 + 2.0 * 0.5]], [[-0.5]])
    cl = closed_loop(p, k)
    assert is_hurwitz(cl[0])
    assert abs(peak(cl) - _peak_scalar(1, -0.5, -3.0, 2.0)) < 1e-9
