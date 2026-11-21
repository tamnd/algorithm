# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/d-bar-method/. The authors are listed in prov/Q00HZV.jsonl.

import cmath
import math
import random

from d_bar_method import (
    cauchy_transform,
    d_bar,
    gamma0_reference,
    k_grid,
    layered_dn_eigenvalues,
    radial_dn_eigenvalues,
    t_exp_radial,
)


def _bump(amp, a=0.6):
    # A smooth radial conductivity that is exactly 1 for r >= a, as the method assumes near the boundary.
    def gamma(r):
        q = r / a
        return 1 + amp * math.exp(1 - 1 / (1 - q * q)) if q < 1 else 1.0
    return gamma


def test_dn_eigenvalues():
    lams = layered_dn_eigenvalues(0.5, 2.0, 1.0, 2)
    assert abs(lams[0] - 13 / 11) < 1e-14
    assert abs(lams[1] - 98 / 47) < 1e-14
    assert radial_dn_eigenvalues(lambda r: 3.0, 4) == [3.0, 6.0, 9.0, 12.0]
    step = radial_dn_eigenvalues(lambda r: 2.0 if r < 0.5 else 1.0, 6)
    for a, b in zip(step, layered_dn_eigenvalues(0.5, 2.0, 1.0, 6)):
        assert abs(a - b) < 1e-3
    # A higher conductivity inside gives lambda_n > n, and the excess decays like rho^(2n).
    smooth = radial_dn_eigenvalues(_bump(0.5), 8)
    excess = [lam - n for n, lam in enumerate(smooth, start=1)]
    assert all(e > 0 for e in excess)
    assert all(b < a for a, b in zip(excess, excess[1:]))


def test_t_exp_series_matches_boundary_integral():
    # t^exp(k) = int e^{i conj(k) conj(z)} (Lambda_gamma - Lambda_1) e^{i k z} ds(z) on |z| = 1,
    # with the DN maps applied mode by mode to samples of e^{i k z}.
    lams = layered_dn_eigenvalues(0.5, 2.0, 1.0, 40)
    N, M = 128, 40
    phis = [2 * math.pi * p / N for p in range(N)]
    for k in (0.7 + 0.2j, -1.5 + 1.1j, 2.5j):
        f = [cmath.exp(1j * k * cmath.exp(1j * p)) for p in phis]
        coef = {m: sum(v * cmath.exp(-1j * m * p) for v, p in zip(f, phis)) / N for m in range(-M, M + 1)}
        g = [sum(c * (lams[abs(m) - 1] - abs(m)) * cmath.exp(1j * m * p) for m, c in coef.items() if m)
             for p in phis]
        direct = sum(cmath.exp(1j * (k * cmath.exp(1j * p)).conjugate()) * gv for p, gv in zip(phis, g))
        direct *= 2 * math.pi / N
        assert abs(direct - t_exp_radial(lams, k)) < 1e-9
        assert abs(direct.imag) < 1e-9


def test_cauchy_transform_of_gaussian():
    # (1/pi) int e^{-|w|^2} / (z - w) dA(w) = (1 - e^{-|z|^2}) / z, the bounded solution of dbar u = e^{-|z|^2}.
    errs = []
    for h in (0.3, 0.15):
        grid = k_grid(4.5, h)
        vals = [math.exp(-abs(k) ** 2) for k in grid]
        targets = [min(grid, key=lambda k: abs(k - z)) for z in (0.3 + 0.15j, 0.75 - 0.45j, -1.2 + 0.6j)]
        inv = [[(1 / (z - kp) if z != kp else 0j) for kp in grid] for z in targets]
        got = cauchy_transform(grid, h, vals, inv)
        errs.append(max(abs(u - (1 - math.exp(-abs(z) ** 2)) / z) for u, z in zip(got, targets)))
    assert errs[1] < 5e-3
    assert errs[1] < 0.6 * errs[0]


def test_constant_conductivity_is_exact():
    lams = [float(n) for n in range(1, 20)]
    assert all(t_exp_radial(lams, k) == 0 for k in (0.5, 2 + 1j, 3j))
    for gz in d_bar(lams, [0j, 0.3 + 0.4j, -0.7], 2.0, 0.4):
        assert abs(gz - 1) < 1e-14


def test_fixed_point_residual_and_center_value():
    lams = layered_dn_eigenvalues(0.5, 1.5, 1.0, 40)
    for z in (0j, 0.4 - 0.2j):
        gz, mu, grid, w = d_bar(lams, [z], 3.0, 0.3, return_mu=True)[0]
        assert grid[0] == 0
        cm = [wi * m.conjugate() for wi, m in zip(w, mu)]
        for k, m in zip(grid, mu):
            s = sum(wi / (k - kp) for wi, kp in zip(cm, grid) if kp != k)
            assert abs(m - 1 - s) < 1e-10
        if z == 0:
            # Radial real t: the grid is symmetric under conjugation, so mu(0, 0) is real,
            # and gamma(0) has the closed form of the reference.
            assert abs(mu[0].imag) < 1e-12
            ref = gamma0_reference(lams, 3.0)
            assert abs(gz - ref) < 5e-3 * ref


def test_smooth_conductivity_rotation_and_accuracy():
    gamma = _bump(0.2)
    lams = radial_dn_eigenvalues(gamma, 30)
    zs = [0j, 0.2, 0.2j, 0.4, -0.4j, 0.8]
    got = d_bar(lams, zs, 3.0, 0.3)
    # Radial data give a radial reconstruction: the grid is symmetric under rotation by 90 degrees.
    assert abs(got[1] - got[2]) < 1e-10
    assert abs(got[3] - got[4]) < 1e-10
    for z, gz in zip(zs, got):
        assert abs(gz - gamma(abs(z))) < 0.05
    # A small cutoff smooths the peak; from R = 3 to R = 8 the center value stays near the true 1.2.
    assert gamma0_reference(lams, 2.0) < 1.1
    assert all(abs(gamma0_reference(lams, R) - 1.2) < 0.05 for R in (3.0, 4.0, 5.0, 6.0, 8.0))


def test_noise_limits_the_cutoff():
    lams = radial_dn_eigenvalues(_bump(0.5), 30)
    rng = random.Random(3)
    noisy = [lam + rng.gauss(0, 3e-3) for lam in lams]
    # The noise enters t^exp(k) with the weights |k|^(2n) / (n!)^2, which grow fast with |k|:
    # a small cutoff R hides it, a large one amplifies it.
    assert abs(gamma0_reference(noisy, 2.0) - gamma0_reference(lams, 2.0)) < 0.05
    assert abs(gamma0_reference(noisy, 5.0) - gamma0_reference(lams, 5.0)) > 0.8
