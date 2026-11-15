# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/indirect-method-optimal-control/. The authors are listed in prov/NBHETY.jsonl.

import math
import random

import pytest

import ctlmat as cm
import ctlsim as cs
from indirect_method_optimal_control import (
    fd_jacobian,
    integrate,
    shooting_residual,
    single_shooting,
)


def test_helper_self_tests():
    assert cm._self_test()
    assert cs._self_test()


# Scalar LQ problem: x' = u, cost int_0^T u^2 dt + x(T)^2.
# H = u^2 + lam u, u = -lam/2, lam' = 0, lam(T) = 2 x(T), so lam = 2 x0 / (1 + T).
def scalar_canon(t, z):
    return [-z[1] / 2, 0.0]


def scalar_residual(zT, T):
    return [zT[1] - 2 * zT[0]]


def test_scalar_lq_example():
    s, k = single_shooting(scalar_canon, [1.0], scalar_residual, [0.0], T=1.0)
    assert abs(s[0] - 1.0) < 1e-9
    assert k <= 3


def test_scalar_lq_random():
    rng = random.Random(11)
    for _ in range(10):
        x0 = rng.uniform(-3, 3)
        T = rng.uniform(0.2, 4)
        s, _ = single_shooting(scalar_canon, [x0], scalar_residual, [rng.uniform(-5, 5)], T=T, N=50)
        assert abs(s[0] - 2 * x0 / (1 + T)) < 1e-9


# Double integrator LQ: x1' = x2, x2' = u, cost int_0^T (x^T x + u^2) dt, free end.
# u = -lam2/2, lam' = -2 x - A^T lam, lam(T) = 0; the Riccati solution gives lam(0) = 2 P(0) x0.
A2 = [[0, 1], [0, 0]]


def di_canon(t, z):
    return [z[1], -z[3] / 2, -2 * z[0], -2 * z[1] - z[2]]


def riccati_p0(T, steps=600):
    """P(0) from -P' = A^T P + P A + Q - P B B^T P, P(T) = 0, in reversed time."""
    def rhs(t, p, u):
        P = cm.unvec(p, 2)
        PB = [[P[0][1]], [P[1][1]]]
        D = cm.add(cm.add(cm.mul(cm.transpose(A2), P), cm.mul(P, A2)),
                   cm.sub(cm.eye(2), cm.mul(PB, cm.transpose(PB))))
        return cm.vec(D)
    _, ps, _ = cs.simulate(rhs, [0.0] * 4, 0.0, T, T / steps)
    return cm.unvec(ps[-1], 2)


def test_double_integrator_matches_riccati():
    rng = random.Random(5)
    T = 3.0
    P0 = riccati_p0(T)
    for _ in range(3):
        x0 = [rng.uniform(-2, 2), rng.uniform(-2, 2)]
        s, _ = single_shooting(di_canon, x0, lambda zT, TT: [zT[2], zT[3]], [0.0, 0.0], T=T, N=300)
        want = [2 * v for v in cm.matvec(P0, x0)]
        assert max(abs(a - b) for a, b in zip(s, want)) < 1e-8


# Nonlinear: x' = sin x + u, cost int_0^2 (x^2 + u^2) dt, x(0) = 1, free end.
# H = x^2 + u^2 + lam (sin x + u), u = -lam/2, lam' = -2 x - lam cos x, lam(2) = 0.
def nl_canon(t, z):
    x, lam = z
    return [math.sin(x) - lam / 2, -2 * x - lam * math.cos(x)]


def nl_solution():
    return single_shooting(nl_canon, [1.0], lambda zT, T: [zT[1]], [0.0], T=2.0, N=400)


def test_nonlinear_converges_and_h_is_constant():
    s, k = nl_solution()
    assert abs(s[0] - 4.15956) < 1e-4
    zs = integrate(nl_canon, [1.0] + s, 2.0, 400)
    assert abs(zs[-1][1]) <= 1e-10
    hs = [x * x - lam * lam / 4 + lam * math.sin(x) for x, lam in zs]
    assert max(hs) - min(hs) < 1e-8


def test_nonlinear_cost_is_stationary_and_does_not_drop():
    s, _ = nl_solution()
    rng = random.Random(7)
    co = [rng.uniform(-1, 1) for _ in range(4)]

    def phi(t):
        return co[0] + sum(co[j] * math.sin(j * math.pi * t / 2) for j in range(1, 4))

    def cost(e):
        # Integrate the optimal pair (x*, lam*) next to the perturbed state x
        # and its cost, so the optimal input -lam*/2 is known at every RK4 stage.
        def f(t, w, u):
            xs, ls, x, _ = w
            uu = -ls / 2 + e * phi(t)
            return [math.sin(xs) - ls / 2, -2 * xs - ls * math.cos(xs), math.sin(x) + uu, x * x + uu * uu]
        _, ws, _ = cs.simulate(f, [1.0, s[0], 1.0, 0.0], 0.0, 2.0, 2.0 / 400)
        return ws[-1][3]

    j0 = cost(0.0)
    for e in (0.3, 0.1, -0.1, 0.03):
        assert cost(e) > j0
    e = 1e-3
    assert abs((cost(e) - cost(-e)) / (2 * e)) < 1e-4


# Free final time: x' = u, cost int_0^T (1 + u^2) dt, x(0) = 1, x(T) = 0.
# Unknowns (lam(0), T), residual (x(T), H(T)) with H = 1 - lam^2 / 4. Answer (2, 1).
def test_free_final_time():
    s, _ = single_shooting(scalar_canon, [1.0], lambda zT, T: [zT[0], 1 - zT[1] ** 2 / 4],
                           [1.5, 0.7], free_time=True, N=50)
    assert abs(s[0] - 2) < 1e-9
    assert abs(s[1] - 1) < 1e-9


def test_free_final_time_wrong_sign_guess():
    # Newton heads for lam = -2, which needs T = -1, so the time goes negative.
    with pytest.raises(ValueError):
        single_shooting(scalar_canon, [1.0], lambda zT, T: [zT[0], 1 - zT[1] ** 2 / 4],
                        [-1.0, 0.7], free_time=True, N=50)


# x' = x + u, cost int (x^2 + u^2): the canonical matrix M has M^2 = 2 I, so the
# shooting derivative d lam(T) / d lam(0) is cosh(sqrt2 T) - sinh(sqrt2 T) / sqrt2.
def unstable_canon(t, z):
    return [z[0] - z[1] / 2, -2 * z[0] - z[1]]


def test_shooting_sensitivity_grows_exponentially():
    m = math.sqrt(2)
    for T in (1.0, 5.0, 10.0):
        def phi(v):
            return shooting_residual(unstable_canon, [1.0], lambda zT, TT: [zT[1]], v, T=T, N=int(200 * T))
        J = fd_jacobian(phi, [0.0])
        want = math.cosh(m * T) - math.sinh(m * T) / m
        assert abs(J[0][0] - want) < 1e-5 * want
    assert want > 2e5


def test_long_horizon_approaches_riccati_and_long_one_fails():
    s, _ = single_shooting(unstable_canon, [1.0], lambda zT, TT: [zT[1]], [0.0], T=10.0, N=1000)
    assert abs(s[0] - 2 * (1 + math.sqrt(2))) < 1e-5
    with pytest.raises(RuntimeError):
        single_shooting(unstable_canon, [1.0], lambda zT, TT: [zT[1]], [0.0], T=20.0, N=1000, maxit=4)


def test_maxit_and_bad_input():
    with pytest.raises(RuntimeError):
        single_shooting(nl_canon, [1.0], lambda zT, T: [zT[1]], [0.0], T=2.0, maxit=0)
    with pytest.raises(ValueError):
        single_shooting(scalar_canon, [1.0], scalar_residual, [0.0, 1.0], T=1.0)
    with pytest.raises(ValueError):
        single_shooting(scalar_canon, [1.0], scalar_residual, [0.0])
    with pytest.raises(ValueError):
        integrate(scalar_canon, [1.0, 0.0], -1.0, 10)
