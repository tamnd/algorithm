# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-alpha-method/. The authors are listed in prov/1NTWAK.jsonl.

import math
from fractions import Fraction as Fr

import scimat
from generalized_alpha_method import (
    amplification_matrix,
    chung_hulbert,
    damping_ratio_and_period_error,
    eigenvalues_3x3,
    generalized_alpha,
    hht,
    spectral_radius,
    wbz,
)


def free_sdof(omega, T, ns, params):
    return generalized_alpha([[1.0]], [[0.0]], [[omega * omega]], lambda t: [0.0], [1.0], [0.0], T / ns, ns, params=params)


def errors_free(params, steps, T=2.0):
    out = []
    for ns in steps:
        ds, vs, _ = free_sdof(1.0, T, ns, params)
        out.append(math.hypot(ds[-1][0] - math.cos(T), vs[-1][0] + math.sin(T)))
    return out


def test_parameters_from_rho_inf():
    am, af, beta, gamma = chung_hulbert(Fr(1, 2))
    assert (am, af, beta, gamma) == (Fr(0), Fr(1, 3), Fr(4, 9), Fr(5, 6))
    am, af, beta, gamma = chung_hulbert(Fr(1))
    assert (am, af, beta, gamma) == (Fr(1, 2), Fr(1, 2), Fr(1, 4), Fr(1, 2))


def test_rho_one_is_the_trapezoidal_rule():
    # With rho_inf = 1 the step equals the average acceleration Newmark step, exactly.
    M = [[Fr(2), Fr(0)], [Fr(0), Fr(1)]]
    K = [[Fr(6), Fr(-2)], [Fr(-2), Fr(4)]]
    C = [[Fr(0)] * 2 for _ in range(2)]
    ds, vs, accs = generalized_alpha(M, C, K, lambda t: [Fr(0), Fr(0)], [Fr(1), Fr(0)], [Fr(0), Fr(1)], Fr(1, 2), 6, rho_inf=Fr(1))
    e0 = (scimat.dot(vs[0], scimat.matvec(M, vs[0])) + scimat.dot(ds[0], scimat.matvec(K, ds[0]))) / 2
    for d, v, a in zip(ds, vs, accs):
        # the equation of motion holds at every step and the energy is exact
        assert scimat.add(scimat.matvec(M, a), scimat.matvec(K, d)) == [0, 0]
        assert (scimat.dot(v, scimat.matvec(M, v)) + scimat.dot(d, scimat.matvec(K, d))) / 2 == e0


def test_high_frequency_limit_is_rho_inf():
    for r in (0.0, 0.3, 0.5, 0.8, 0.95):
        p = chung_hulbert(r)
        rho = spectral_radius(1e6, p)
        assert abs(rho - r) < 2e-3, (r, rho)
        # the three roots meet at -rho_inf
        for z in eigenvalues_3x3(amplification_matrix(1e6, p)):
            assert abs(z + r) < 5e-3


def test_unconditional_stability():
    for r in (0.0, 0.3, 0.6, 0.9, 1.0):
        p = chung_hulbert(r)
        for k in range(-8, 13):
            w = 10 ** (k / 4)
            # near omega dt = infinity and rho_inf = 1 the roots form a near Jordan block, so allow rounding
            assert spectral_radius(w, p) <= 1 + 1e-6, (r, w)


def test_second_order_for_all_rho():
    for r in (0.0, 0.5, 0.9):
        p = scimat.observed_order(errors_free(chung_hulbert(r), [40, 80, 160, 320]))
        assert all(abs(q - 2) < 0.2 for q in p), (r, p)


def test_hht_and_wbz_second_order_and_limit():
    for params, r in ((hht(0.1), 9 / 11), (hht(1 / 3), 0.5), (wbz(0.5), 0.5)):
        p = scimat.observed_order(errors_free(params, [40, 80, 160, 320]))
        assert all(abs(q - 2) < 0.2 for q in p), p
        assert abs(spectral_radius(1e7, params) - r) < 1e-3


def test_less_low_frequency_damping_than_newmark():
    # Same rho_inf = 9/11: Newmark with gamma = 0.6 damps the resolved modes far more.
    newmark = (0.0, 0.0, 1.1 ** 2 / 4, 0.6)
    ch = chung_hulbert(9 / 11)
    for w in (0.1, 0.3, 1.0):
        xn, _ = damping_ratio_and_period_error(w, newmark)
        xc, _ = damping_ratio_and_period_error(w, ch)
        xh, _ = damping_ratio_and_period_error(w, hht(0.1))
        assert 0 <= xc < xh < xn
    p = scimat.observed_order(errors_free(newmark, [80, 160, 320, 640]))
    assert all(abs(q - 1) < 0.2 for q in p)


def test_damping_ratio_is_third_order_in_omega_dt():
    p = chung_hulbert(0.5)
    x = [damping_ratio_and_period_error(w, p)[0] for w in (0.2, 0.1, 0.05)]
    orders = scimat.observed_order(x)
    assert all(abs(q - 3) < 0.3 for q in orders), orders


def test_forced_damped_two_dof():
    # M = I, C = 0.1 K, K = [[2, -1], [-1, 2]], F = (sin t, 0), against a fine reference run.
    K = [[2.0, -1.0], [-1.0, 2.0]]
    C = scimat.scale(0.1, K)
    I2 = scimat.eye(2)

    def F(t):
        return [math.sin(t), 0.0]

    T = 3.0
    ref, _, _ = generalized_alpha(I2, C, K, F, [0.0, 0.0], [0.0, 0.0], T / 5120, 5120, rho_inf=0.6)
    errs = []
    for ns in (40, 80, 160):
        ds, _, _ = generalized_alpha(I2, C, K, F, [0.0, 0.0], [0.0, 0.0], T / ns, ns, rho_inf=0.6)
        errs.append(max(abs(x - y) for x, y in zip(ds[-1], ref[-1])))
    p = scimat.observed_order(errs)
    assert all(abs(q - 2) < 0.25 for q in p), p


def test_load_at_the_shifted_time():
    # a + 0.2 v + d = cos t from rest. The load at t_(n+1-af) gives order 2; the load at t_(n+1) only order 1.
    xi, T = 0.1, 4.0
    wd = math.sqrt(1 - xi * xi)

    def exact(t):
        return 5 * math.sin(t) - 5 / wd * math.exp(-xi * t) * math.sin(wd * t)

    params = chung_hulbert(0.5)
    af = params[1]
    for late, order in ((False, 2), (True, 1)):
        errs = []
        for ns in (50, 100, 200, 400):
            dt = T / ns
            F = (lambda t, dt=dt: [math.cos(t + af * dt)]) if late else (lambda t: [math.cos(t)])
            ds, _, _ = generalized_alpha([[1.0]], [[0.2]], [[1.0]], F, [0.0], [0.0], dt, ns, params=params)
            errs.append(abs(ds[-1][0] - exact(T)))
        p = scimat.observed_order(errs)
        assert abs(p[-1] - order) < 0.1, (late, p)


def test_stiff_mode_is_damped():
    # A stiff spring (omega = 1000) next to a soft one; after 20 large steps the stiff mode is gone.
    M = scimat.eye(2)
    K = [[1.0, 0.0], [0.0, 1e6]]
    Z = scimat.zeros(2)
    ds, _, _ = generalized_alpha(M, Z, K, lambda t: [0.0, 0.0], [1.0, 1.0], [0.0, 0.0], 0.1, 20, rho_inf=0.0)
    assert abs(ds[-1][1]) < 1e-12
    assert abs(ds[-1][0] - math.cos(2.0)) < 1e-2
    ds, _, _ = generalized_alpha(M, Z, K, lambda t: [0.0, 0.0], [1.0, 1.0], [0.0, 0.0], 0.1, 20, rho_inf=1.0)
    assert abs(ds[-1][1]) > 0.5
