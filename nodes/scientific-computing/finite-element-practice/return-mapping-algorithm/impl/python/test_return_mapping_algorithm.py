# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/return-mapping-algorithm/. The authors are listed in prov/PD9SMC.jsonl.

import math
import random
from fractions import Fraction as Fr

from return_mapping_algorithm import (
    bar_newton,
    dev,
    radial_return,
    return_map_1d,
    tnorm,
    yield_value,
    zero_state,
)

E, SY, KI, HK = 200.0, 0.25, 10.0, 5.0
KAPPA, MU = 160.0, 80.0


def test_1d_exact_fractions():
    # E = 100, sy = 1, K = 10, H = 0: strain 0.03 from the virgin state.
    sig, (ep, al, q), tan = return_map_1d(Fr(3, 100), (Fr(0), Fr(0), Fr(0)), Fr(100), Fr(1), Fr(10), Fr(0))
    assert sig == Fr(1) + Fr(10) * al
    assert ep == al == Fr(2, 110)
    assert sig == Fr(13, 11)
    assert tan == Fr(1000, 110)


def test_1d_elastic_step_unchanged():
    state = (0.001, 0.001, 0.0)
    sig, new, tan = return_map_1d(0.002, state, E, SY, KI, HK)
    assert new == state and tan == E and sig == E * 0.001


def test_1d_monotone_loading_is_exact_for_any_step():
    # Bilinear exact response: sigma = sy + Et (eps - eps_y) after first yield.
    et = E * (KI + HK) / (E + KI + HK)
    eps_y = SY / E
    for nsteps in (1, 3, 50):
        state = (0.0, 0.0, 0.0)
        for k in range(1, nsteps + 1):
            eps = 0.01 * k / nsteps
            sig, state, _ = return_map_1d(eps, state, E, SY, KI, HK)
        assert abs(sig - (SY + et * (0.01 - eps_y))) < 1e-12


def test_1d_bauschinger_with_kinematic_hardening():
    # Pure kinematic hardening: the elastic range keeps its width 2 sy and moves with the back stress.
    state = (0.0, 0.0, 0.0)
    sig_max, state, _ = return_map_1d(0.01, state, E, SY, 0.0, HK)
    # unload elastically until the reverse yield stress sig_max - 2 sy
    eps = 0.01 - (2 * SY - 1e-9) / E
    sig, st2, tan = return_map_1d(eps, state, E, SY, 0.0, HK)
    assert st2 == state and tan == E
    sig, st3, tan = return_map_1d(eps - 1e-4, state, E, SY, 0.0, HK)
    assert st3 != state
    assert abs(sig - (sig_max - 2 * SY)) < 1e-3


def random_sym(rng, scale):
    a = [[rng.uniform(-scale, scale) for _ in range(3)] for _ in range(3)]
    return [[(a[i][j] + a[j][i]) / 2 for j in range(3)] for i in range(3)]


def test_3d_consistency_and_normality():
    rng = random.Random(1)
    for _ in range(20):
        state = zero_state()
        eps = random_sym(rng, 0.01)
        sig, new, _, dgam = radial_return(eps, state, KAPPA, MU, SY, KI, HK)
        assert dgam > 0
        # the new stress is on the new yield surface
        assert abs(yield_value(sig, new, SY, KI)) < 1e-12
        # the plastic strain increment is deviatoric and parallel to dev(sigma) - beta
        dep = new[0]
        assert abs(dep[0][0] + dep[1][1] + dep[2][2]) < 1e-14
        s = dev(sig)
        xi = [[s[i][j] - new[2][i][j] for j in range(3)] for i in range(3)]
        nx, nd = tnorm(xi), tnorm(dep)
        assert all(abs(xi[i][j] / nx - dep[i][j] / nd) < 1e-12 for i in range(3) for j in range(3))
        # the pressure is elastic
        assert abs((sig[0][0] + sig[1][1] + sig[2][2]) / 3 - KAPPA * (eps[0][0] + eps[1][1] + eps[2][2])) < 1e-12


def test_3d_elastic_steps_unchanged():
    rng = random.Random(2)
    state = zero_state()
    for _ in range(10):
        eps = random_sym(rng, 1e-4)
        sig, new, _, dgam = radial_return(eps, state, KAPPA, MU, SY, KI, HK)
        assert dgam == 0 and new is state
        assert yield_value(sig, state, SY, KI) <= 0


def test_3d_consistent_tangent_against_finite_differences():
    rng = random.Random(3)
    base_state = zero_state()
    # a plastic start state
    _, base_state, _, _ = radial_return(random_sym(rng, 0.005), base_state, KAPPA, MU, SY, KI, HK)
    eps = random_sym(rng, 0.01)
    sig, _, c, dgam = radial_return(eps, base_state, KAPPA, MU, SY, KI, HK)
    assert dgam > 0
    h = 1e-7
    worst = 0.0
    for k in range(3):
        for l in range(k, 3):
            ep = [row[:] for row in eps]
            em = [row[:] for row in eps]
            # a symmetric perturbation: add h to the (k, l) and (l, k) entries
            for (a, b) in {(k, l), (l, k)}:
                ep[a][b] += h
                em[a][b] -= h
            sp, _, _, _ = radial_return(ep, base_state, KAPPA, MU, SY, KI, HK)
            sm, _, _, _ = radial_return(em, base_state, KAPPA, MU, SY, KI, HK)
            for i in range(3):
                for j in range(3):
                    fd = (sp[i][j] - sm[i][j]) / (2 * h)
                    an = c[3 * i + j][3 * k + l] + (c[3 * i + j][3 * l + k] if k != l else 0)
                    worst = max(worst, abs(fd - an))
    assert worst < 1e-5 * (KAPPA + MU)


def test_3d_proportional_path_is_step_independent():
    # A proportional deviatoric strain path keeps n fixed; then one step equals many steps.
    e0 = [[0.004, 0.001, 0.0], [0.001, -0.003, 0.002], [0.0, 0.002, -0.001]]
    finals = []
    for nsteps in (1, 7, 40):
        state = zero_state()
        for k in range(1, nsteps + 1):
            eps = [[e0[i][j] * k / nsteps for j in range(3)] for i in range(3)]
            sig, state, _, _ = radial_return(eps, state, KAPPA, MU, SY, KI, HK)
        finals.append(sig)
    for s in finals[1:]:
        assert max(abs(s[i][j] - finals[0][i][j]) for i in range(3) for j in range(3)) < 1e-12


def test_3d_nonproportional_path_first_order():
    # Tension then shear: backward Euler is exact for the discrete equations, but the
    # stress after a nonproportional path depends on the step, with an O(dt) error.
    def run(nsteps):
        state = zero_state()
        for k in range(1, nsteps + 1):
            t = k / nsteps
            eps = [[0.004, 0.006 * t, 0.0], [0.006 * t, -0.002, 0.0], [0.0, 0.0, -0.002]]
            sig, state, _, _ = radial_return(eps, state, KAPPA, MU, SY, KI, HK)
        return sig

    ref = run(20480)
    errs = []
    for ns in (20, 40, 80, 160):
        s = run(ns)
        errs.append(max(abs(s[i][j] - ref[i][j]) for i in range(3) for j in range(3)))
    orders = [math.log2(errs[i] / errs[i + 1]) for i in range(len(errs) - 1)]
    assert all(abs(q - 1) < 0.2 for q in orders), orders


def test_bar_newton_quadratic_with_consistent_tangent():
    areas = [1.0, 0.8, 1.2, 1.0]
    lengths = [1.0, 1.0, 1.0, 1.0]
    sig_c, it_c = bar_newton(areas, lengths, 0.02, E, SY, KI, HK, consistent=True)
    sig_e, it_e = bar_newton(areas, lengths, 0.02, E, SY, KI, HK, consistent=False, maxit=2000)
    forces = [s * a for s, a in zip(sig_c, areas)]
    assert max(forces) - min(forces) < 1e-9
    assert all(abs(x - y) < 1e-8 for x, y in zip(sig_c, sig_e))
    # the response is piecewise linear: once every element is on the right branch,
    # Newton with the consistent tangent is exact in one more step
    assert it_c <= 3
    # the elastic tangent gives a linear rate with factor about 1 - Et / E
    assert it_e > 100
