# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/h-infinity-loop-shaping/. The authors are listed in prov/5JS87D.jsonl.

import math
import random

import ctlmat as cm
from h_infinity_loop_shaping import (
    controller,
    feedback_a,
    gamma_min,
    is_hurwitz,
    loop_shaping_design,
    series,
    stability_margin,
)

INTEGRATOR = ([[0]], [[1]], [[1]], [[0]])          # 1 / s
LAG = ([[-1]], [[1]], [[1]], [[0]])                # 1 / (s + 1)
MOTOR = ([[0, 1], [0, -1]], [[0], [1]], [[2, 0]], [[0]])   # 2 / (s (s + 1))
UNSTABLE = ([[1, 1], [0, -2]], [[0], [1]], [[1, 0]], [[0]])  # 1 / ((s - 1) (s + 2))
PLANTS = (INTEGRATOR, LAG, MOTOR, UNSTABLE)

FREQS = [10 ** (e / 40) for e in range(-160, 161)]


def static(k):
    return ([], [], [], [[k]])


def lyap(a, q):
    # Solve A P + P A^T + Q = 0 by the Kronecker form (I x A + A x I) vec P = -vec Q.
    n = len(a)
    big = cm.add(cm.kron(cm.eye(n), a), cm.kron(a, cm.eye(n)))
    return cm.unvec(cm.solve(big, [-v for v in cm.vec(q)]), n)


def test_ctlmat_self_test():
    assert cm._self_test()


def test_integrator_values():
    g, x, z = gamma_min(INTEGRATOR)
    assert abs(x[0][0] - 1) < 1e-12 and abs(z[0][0] - 1) < 1e-12
    assert abs(g - math.sqrt(2)) < 1e-12


def test_first_order_lag_values():
    g, x, z = gamma_min(LAG)
    r = math.sqrt(2) - 1
    assert abs(x[0][0] - r) < 1e-12 and abs(z[0][0] - r) < 1e-12
    assert abs(g - math.sqrt(4 - 2 * math.sqrt(2))) < 1e-12
    assert abs(1 / g - math.cos(math.pi / 8)) < 1e-12


def test_riccati_residuals():
    for gs in PLANTS:
        a, b, c, _ = (cm.scale(1.0, m) for m in gs)
        _, x, z = gamma_min(gs)
        bb = cm.mul(b, cm.transpose(b))
        cc = cm.mul(cm.transpose(c), c)
        rx = cm.add(cm.sub(cm.add(cm.mul(cm.transpose(a), x), cm.mul(x, a)), cm.mul(cm.mul(x, bb), x)), cc)
        rz = cm.add(cm.sub(cm.add(cm.mul(a, z), cm.mul(z, cm.transpose(a))), cm.mul(cm.mul(z, cc), z)), bb)
        assert max(abs(v) for row in rx + rz for v in row) < 1e-9
        assert cm.is_pos_def(x, -1e-12) and cm.is_pos_def(z, -1e-12)
        assert is_hurwitz(cm.sub(a, cm.mul(bb, x)))
        assert is_hurwitz(cm.sub(a, cm.mul(z, cc)))


def test_gamma_min_matches_the_hankel_norm():
    # Reference: eps_max^2 = 1 - ||[N M]||_H^2 for the normalized left
    # coprime factors [N M] = (A - Z C^T C, [B, -Z C^T], C, [0, I]),
    # with the Hankel norm from two Lyapunov equations.
    for gs in PLANTS:
        a, b, c, _ = (cm.scale(1.0, m) for m in gs)
        g, _, z = gamma_min(gs)
        ah = cm.sub(a, cm.mul(cm.mul(z, cm.transpose(c)), c))
        bh = cm.block([[b, cm.scale(-1.0, cm.mul(z, cm.transpose(c)))]])
        p = lyap(ah, cm.mul(bh, cm.transpose(bh)))
        q = lyap(cm.transpose(ah), cm.mul(cm.transpose(c), c))
        hankel2 = max(abs(v) for v in cm.polyroots(cm.charpoly(cm.mul(p, q))))
        assert abs((1 - hankel2) - 1 / g ** 2) < 1e-9


def test_central_controller_reaches_the_level():
    for gs in PLANTS:
        g0 = gamma_min(gs)[0]
        for f in (1.05, 1.1, 1.5):
            k = controller(gs, f * g0)
            assert is_hurwitz(feedback_a(gs, k))
            b = stability_margin(gs, k, FREQS)
            assert b >= 1 / (f * g0) - 1e-9
            assert b <= 1 / g0 + 1e-9


def test_static_gain_for_the_integrator_is_optimal():
    # For G = 1/s and C = 1, b(G, C) = 1/sqrt(2) = eps_max.
    b = stability_margin(INTEGRATOR, static(1.0), FREQS)
    assert abs(b - 1 / math.sqrt(2)) < 1e-9


def test_no_random_controller_beats_eps_max():
    # A coarse grid can only miss the peak, which makes the computed
    # margin larger, so the check below is on the safe side.
    coarse = [10 ** (e / 10) for e in range(-30, 31)] + [0.0]
    rng = random.Random(11)
    for gs in (LAG, UNSTABLE):
        eps = 1 / gamma_min(gs)[0]
        found = 0
        for _ in range(60):
            if rng.random() < 0.5:
                k = static(rng.uniform(-1, 6))
            else:
                pole = rng.uniform(0.1, 10)
                k = ([[-pole]], [[1.0]], [[rng.uniform(-5, 20)]], [[rng.uniform(-1, 5)]])
            if not is_hurwitz(feedback_a(gs, k)):
                continue
            found += 1
            assert stability_margin(gs, k, coarse) <= eps + 1e-9
        assert found > 15


def test_series_connection():
    w1 = ([[0]], [[1]], [[2]], [[1]])      # (s + 2) / s
    gs = series(w1, LAG)                    # (s + 2) / (s (s + 1))
    a, b, c, d = gs
    s = 0.7j
    m = [[s - a[i][j] if i == j else -a[i][j] for j in range(2)] for i in range(2)]
    val = cm.mul(c, cm.solve(m, [[complex(v) for v in row] for row in b]))[0][0] + d[0][0]
    assert abs(val - (s + 2) / (s * (s + 1))) < 1e-12


def test_full_design_with_an_integral_weight():
    w1 = ([[0]], [[1]], [[2]], [[1]])      # W1 = (s + 2) / s
    w2 = static(1.0)
    gmin, gamma, k = loop_shaping_design(LAG, w1, w2, 1.1)
    assert abs(gamma - 1.1 * gmin) < 1e-12
    assert is_hurwitz(feedback_a(LAG, k))
    # The weight puts an integrator in K: K has an eigenvalue at 0.
    assert min(abs(r) for r in cm.polyroots(cm.charpoly(k[0]))) < 1e-9
    gs = series(w1, LAG)
    ks = controller(gs, gamma)
    assert stability_margin(gs, ks, FREQS) >= 1 / gamma - 1e-9
