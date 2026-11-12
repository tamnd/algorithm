# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radam/. The authors are listed in prov/KMW02T.jsonl.

import math
import random
from fractions import Fraction

from radam import first_rectified_step, radam, rectification, rho, rho_inf, sma_length_from_center_of_mass


def test_rho_t_equals_the_center_of_mass_length_exactly() -> None:
    for b in (Fraction(999, 1000), Fraction(99, 100), Fraction(9, 10), Fraction(1, 2)):
        for t in range(1, 40):
            assert rho(b, t) == sma_length_from_center_of_mass(b, t)


def test_rho_inf_and_rho_1() -> None:
    assert rho_inf(Fraction(999, 1000)) == 1999
    assert rho_inf(Fraction(99, 100)) == 199
    assert rho_inf(Fraction(3, 5)) == 4
    for b in (Fraction(999, 1000), Fraction(9, 10), Fraction(1, 3)):
        assert rho(b, 1) == 1


def test_rho_t_increases_to_rho_inf() -> None:
    b = Fraction(99, 100)
    vals = [rho(b, t) for t in range(1, 300)]
    assert all(a < c for a, c in zip(vals, vals[1:]))
    assert all(r < rho_inf(b) for r in vals)
    assert 199 - rho(0.99, 2000) < 1e-5


def test_threshold_steps() -> None:
    # rho_4 = 3.9975 and rho_5 = 4.996 for beta2 = 0.999.
    assert first_rectified_step(0.999, 4) == 5
    assert first_rectified_step(0.999, 5) == 6
    # rho_inf <= 4 when beta2 <= 0.6: RAdam never leaves the momentum branch.
    assert first_rectified_step(0.6, 4) is None


def test_rectification_term_is_in_0_1_and_tends_to_1() -> None:
    rs = [rectification(0.999, t) for t in range(5, 20001, 5)]
    assert all(0 < r < 1 for r in rs)
    assert all(a < c for a, c in zip(rs, rs[1:]))
    assert 1 - rs[-1] < 1e-6
    assert math.isclose(rectification(0.999, 5), 0.0173, abs_tol=1e-4)


def test_first_steps_are_momentum_sgd_then_rectified_adam() -> None:
    rng = random.Random(3)
    gs = [[rng.gauss(0, 1), rng.gauss(0, 1)] for _ in range(8)]
    lr, b1, b2 = 0.01, 0.9, 0.999
    path, branch = radam(lambda x, t: gs[t - 1], [0.5, -0.5], 8, lr=lr, beta1=b1, beta2=b2)
    assert branch == ["sgdm"] * 4 + ["adaptive"] * 4
    x, m, v = [0.5, -0.5], [0.0, 0.0], [0.0, 0.0]
    for t in range(1, 9):
        g = gs[t - 1]
        m = [b1 * a + (1 - b1) * c for a, c in zip(m, g)]
        v = [b2 * a + (1 - b2) * c * c for a, c in zip(v, g)]
        m_hat = [a / (1 - b1 ** t) for a in m]
        if t <= 4:
            x = [a - lr * c for a, c in zip(x, m_hat)]
        else:
            v_hat = [a / (1 - b2 ** t) for a in v]
            r = rectification(b2, t)
            x = [a - lr * r * c / math.sqrt(e) for a, c, e in zip(x, m_hat, v_hat)]
        assert all(math.isclose(a, c, rel_tol=1e-12) for a, c in zip(x, path[t]))


def test_small_beta2_is_momentum_sgd_throughout() -> None:
    path, branch = radam(lambda x, t: [1.0], [0.0], 50, lr=0.1, beta2=0.6)
    assert set(branch) == {"sgdm"}
    assert math.isclose(path[-1][0], -5.0, rel_tol=1e-12)


def test_rectified_variance_is_close_to_the_limit() -> None:
    # psi_t = sqrt((1 - beta2^t) / v_t) for N(0, 1) gradients. Its variance is
    # far larger early on; r_t^2 Var[psi_t] stays near the limit
    # rho_inf / (2 (rho_inf - 2)(rho_inf - 4)).
    rng = random.Random(1)
    b2 = 0.999
    target = rho_inf(b2) / (2 * (rho_inf(b2) - 2) * (rho_inf(b2) - 4))
    for t in (10, 20, 50):
        xs = []
        for _ in range(3000):
            v = 0.0
            for _ in range(t):
                g = rng.gauss(0, 1)
                v = b2 * v + (1 - b2) * g * g
            xs.append(math.sqrt((1 - b2 ** t) / v))
        mu = sum(xs) / len(xs)
        var = sum((a - mu) ** 2 for a in xs) / (len(xs) - 1)
        assert var > 30 * target
        assert 0.5 * target < var * rectification(b2, t) ** 2 < 2 * target


def test_converges_on_a_quadratic() -> None:
    grad = lambda x, t: [2 * (x[0] - 1), 20 * (x[1] + 2)]
    x = radam(grad, [0.0, 0.0], 5000, lr=0.05, eps=1e-8)[0][-1]
    assert abs(x[0] - 1) < 1e-2 and abs(x[1] + 2) < 1e-2
