# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newmark-beta-method/. The authors are listed in prov/DKETH0.jsonl.

import math
from fractions import Fraction as Fr

import scimat
from newmark_beta_method import (
    amplification_matrix,
    critical_omega_dt,
    newmark,
    newmark_nonlinear,
    spectral_radius_2x2,
)


def free_sdof(omega, dt, nsteps, beta, gamma, d0=1.0, v0=0.0):
    return newmark([[1.0]], [[0.0]], [[omega * omega]], lambda t: [0.0], [d0], [v0], dt, nsteps, beta, gamma)


def test_first_step_exact_fractions():
    # m = k = 1, d0 = 1, v0 = 0, dt = 1/2, average acceleration: d1 = 15/17, v1 = -8/17.
    ds, vs, accs = newmark([[Fr(1)]], [[Fr(0)]], [[Fr(1)]], lambda t: [Fr(0)], [Fr(1)], [Fr(0)], Fr(1, 2), 1, Fr(1, 4), Fr(1, 2))
    assert accs[0] == [Fr(-1)]
    assert ds[1] == [Fr(15, 17)]
    assert vs[1] == [Fr(-8, 17)]
    assert accs[1] == [Fr(-15, 17)]


def test_average_acceleration_conserves_energy_exactly():
    # For an undamped linear system, (1/2)(v.Mv + d.Kd) is the same at every step, for any dt.
    M = [[Fr(2), Fr(0)], [Fr(0), Fr(1)]]
    K = [[Fr(6), Fr(-2)], [Fr(-2), Fr(4)]]
    C = [[Fr(0)] * 2 for _ in range(2)]
    ds, vs, _ = newmark(M, C, K, lambda t: [Fr(0), Fr(0)], [Fr(1), Fr(0)], [Fr(0), Fr(1)], Fr(3), 12, Fr(1, 4), Fr(1, 2))

    def energy(d, v):
        return (scimat.dot(v, scimat.matvec(M, v)) + scimat.dot(d, scimat.matvec(K, d))) / 2

    e0 = energy(ds[0], vs[0])
    assert all(energy(d, v) == e0 for d, v in zip(ds, vs))


def test_trapezoidal_phase_is_two_arctan():
    # The eigenvalues of the average acceleration step have modulus 1 and argument 2 atan(omega dt / 2).
    for w in (0.1, 0.7, 2.0, 10.0, 100.0):
        a = amplification_matrix(w, 0.25, 0.5)
        det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
        tr = a[0][0] + a[1][1]
        assert abs(det - 1) < 1e-12
        assert abs(tr / 2 - math.cos(2 * math.atan(w / 2))) < 1e-12


def errors_at_T(beta, gamma, steps_list, T=2.0):
    errs = []
    for ns in steps_list:
        ds, vs, _ = free_sdof(1.0, T / ns, ns, beta, gamma)
        errs.append(math.hypot(ds[-1][0] - math.cos(T), vs[-1][0] + math.sin(T)))
    return errs


def test_second_order_for_gamma_half():
    for beta in (0.25, 1 / 6, 1 / 12, 0.0):
        p = scimat.observed_order(errors_at_T(beta, 0.5, [40, 80, 160, 320]))
        assert all(abs(q - 2) < 0.2 for q in p), (beta, p)


def test_first_order_for_gamma_above_half():
    gamma = 0.6
    beta = (gamma + 0.5) ** 2 / 4
    p = scimat.observed_order(errors_at_T(beta, gamma, [80, 160, 320, 640]))
    assert all(abs(q - 1) < 0.2 for q in p), p


def test_central_difference_limit_two():
    assert critical_omega_dt(0.0, 0.5) == 2
    assert spectral_radius_2x2(amplification_matrix(1.99, 0.0, 0.5)) <= 1 + 1e-12
    assert spectral_radius_2x2(amplification_matrix(2.01, 0.0, 0.5)) > 1.05


def test_linear_acceleration_limit():
    wc = critical_omega_dt(1 / 6, 0.5)
    assert abs(wc - math.sqrt(12)) < 1e-12
    assert spectral_radius_2x2(amplification_matrix(wc * 0.999, 1 / 6, 0.5)) <= 1 + 1e-9
    assert spectral_radius_2x2(amplification_matrix(wc * 1.01, 1 / 6, 0.5)) > 1


def test_unconditional_stability_region():
    for gamma in (0.5, 0.55, 0.7, 1.0):
        beta = gamma / 2
        for w in (0.5, 5.0, 50.0, 5e3):
            # near omega dt = infinity the step matrix is close to a Jordan block, so allow rounding
            assert spectral_radius_2x2(amplification_matrix(w, beta, gamma)) <= 1 + 1e-9
    assert critical_omega_dt(0.25, 0.5) == math.inf


def test_dissipation_with_gamma_above_half():
    gamma = 0.6
    beta = (gamma + 0.5) ** 2 / 4
    rho = spectral_radius_2x2(amplification_matrix(1e6, beta, gamma))
    assert rho < 0.9
    assert spectral_radius_2x2(amplification_matrix(1e6, 0.25, 0.5)) > 1 - 1e-9


def test_two_dof_against_modal_solution():
    # M = I, K = [[2, -1], [-1, 2]]: modes (1, 1) with omega = 1 and (1, -1) with omega = sqrt(3).
    K = [[2.0, -1.0], [-1.0, 2.0]]
    I2 = [[1.0, 0.0], [0.0, 1.0]]
    Z = [[0.0, 0.0], [0.0, 0.0]]
    T = 3.0
    w2 = math.sqrt(3.0)

    def exact(t):
        q1, q2 = math.cos(t), 0.5 * math.cos(w2 * t)
        return [q1 + q2, q1 - q2]

    errs = []
    for ns in (60, 120, 240):
        ds, _, _ = newmark(I2, Z, K, lambda t: [0.0, 0.0], exact(0.0), [0.0, 0.0], T / ns, ns)
        errs.append(max(abs(x - y) for x, y in zip(ds[-1], exact(T))))
    p = scimat.observed_order(errs)
    assert all(abs(q - 2) < 0.2 for q in p), p


def test_forced_damped_oscillator():
    # a + 0.2 v + d = cos(t) from rest; compare with the exact solution.
    xi, T = 0.1, 4.0

    def exact(t):
        # particular solution (0.2 sin t) / 0.04 = 5 sin t; homogeneous part fixes d(0) = 0, v(0) = 0.
        wd = math.sqrt(1 - xi * xi)
        A = 0.0
        B = -5.0 / wd
        return 5 * math.sin(t) + math.exp(-xi * t) * (A * math.cos(wd * t) + B * math.sin(wd * t))

    errs = []
    for ns in (50, 100, 200):
        ds, _, _ = newmark([[1.0]], [[0.2]], [[1.0]], lambda t: [math.cos(t)], [0.0], [0.0], T / ns, ns)
        errs.append(abs(ds[-1][0] - exact(T)))
    p = scimat.observed_order(errs)
    assert all(abs(q - 2) < 0.2 for q in p), p


def rk4_duffing(d, v, T, ns):
    h = T / ns

    def f(x, y):
        return y, -x - x ** 3

    for _ in range(ns):
        k1 = f(d, v)
        k2 = f(d + h / 2 * k1[0], v + h / 2 * k1[1])
        k3 = f(d + h / 2 * k2[0], v + h / 2 * k2[1])
        k4 = f(d + h * k3[0], v + h * k3[1])
        d += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        v += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    return d, v


def test_nonlinear_duffing_against_rk4():
    # a + d + d^3 = 0, d(0) = 1, v(0) = 0; RK4 with 4000 steps is the reference.
    T = 3.0
    dref, _ = rk4_duffing(1.0, 0.0, T, 4000)
    errs = []
    for ns in (50, 100, 200):
        ds, _, _, its = newmark_nonlinear(
            [[1.0]], [[0.0]], lambda d: [d[0] + d[0] ** 3], lambda d: [[1 + 3 * d[0] ** 2]], lambda t: [0.0], [1.0], [0.0], T / ns, ns
        )
        assert max(its) <= 8
        errs.append(abs(ds[-1][0] - dref))
    p = scimat.observed_order(errs)
    assert all(abs(q - 2) < 0.2 for q in p), p


def test_nonlinear_energy_is_not_exact():
    # The trapezoidal rule does not conserve the energy of a nonlinear spring exactly.
    ds, vs, _, _ = newmark_nonlinear(
        [[1.0]], [[0.0]], lambda d: [d[0] + d[0] ** 3], lambda d: [[1 + 3 * d[0] ** 2]], lambda t: [0.0], [1.0], [0.0], 0.5, 40
    )
    e = [v[0] ** 2 / 2 + d[0] ** 2 / 2 + d[0] ** 4 / 4 for d, v in zip(ds, vs)]
    assert max(abs(x - e[0]) for x in e) > 1e-4
