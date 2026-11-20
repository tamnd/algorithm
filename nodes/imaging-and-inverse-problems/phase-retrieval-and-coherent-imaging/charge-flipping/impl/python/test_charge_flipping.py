# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/charge-flipping/. The authors are listed in prov/3DN6XM.jsonl.

import cmath
import math
import random

from charge_flipping import charge_flipping, flip, r_factor, random_start
from imgkit import dft2, idft2


def structure(n1, n2, natoms, seed):
    """Point atoms of weight 1 or 2 on distinct grid points, zero elsewhere."""
    rng = random.Random(seed)
    rho = [[0.0] * n2 for _ in range(n1)]
    for i, j in rng.sample([(i, j) for i in range(n1) for j in range(n2)], natoms):
        rho[i][j] = rng.choice((1.0, 1.0, 2.0))
    return rho


def data(rho, observe_origin=False):
    f = dft2(rho)
    n1, n2 = len(rho), len(rho[0])
    amp = [[abs(v) for v in row] for row in f]
    obs = [[True] * n2 for _ in range(n1)]
    obs[0][0] = observe_origin
    return f, amp, obs


def match_error(rho, true):
    """Relative error after the best shift and inversion, with the mean set to that of true."""
    n1, n2 = len(rho), len(rho[0])
    shift = (sum(map(sum, true)) - sum(map(sum, rho))) / (n1 * n2)
    best = math.inf
    for inv in (1, -1):
        for si in range(n1):
            for sj in range(n2):
                e = sum(
                    (rho[(inv * i + si) % n1][(inv * j + sj) % n2] + shift - true[i][j]) ** 2
                    for i in range(n1)
                    for j in range(n2)
                )
                best = min(best, e)
    return math.sqrt(best / sum(v * v for row in true for v in row))


def max_diff(a, b):
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def test_flip_with_zero_threshold_is_the_reflector():
    rng = random.Random(1)
    rho = [[rng.gauss(0, 1) for _ in range(6)] for _ in range(5)]
    g = flip(rho, 0.0)
    for rr, rg in zip(rho, g):
        for v, w in zip(rr, rg):
            assert w == abs(v)
            assert abs(w - (2 * max(v, 0.0) - v)) < 1e-15


def test_random_start_obeys_friedel_and_gives_a_real_density():
    true = structure(8, 16, 6, 2)
    _, amp, obs = data(true)
    f = random_start(amp, obs, 3)
    for k in range(8):
        for l in range(16):
            assert abs(f[k][l] - f[-k % 8][-l % 16].conjugate()) < 1e-12
            assert abs(abs(f[k][l]) - (amp[k][l] if obs[k][l] else 0.0)) < 1e-12
    assert max(abs(v.imag) for row in idft2(f) for v in row) < 1e-12


def test_atomic_density_is_a_fixed_point():
    true = structure(8, 8, 5, 4)
    f, amp, obs = data(true)
    for delta in (0.0, 0.3, 0.9):
        rho, r = charge_flipping(amp, obs, delta, 5, start=f)
        assert max_diff(rho, true) < 1e-12
        assert r < 1e-13


def test_one_cycle_matches_direct_sums():
    true = structure(4, 4, 3, 5)
    _, amp, obs = data(true)
    start = random_start(amp, obs, 6)
    delta = 0.25
    n = 4
    f = [list(row) for row in start]
    for _ in range(3):
        rho = [
            [sum(f[k][l] * cmath.exp(2j * math.pi * (k * i + l * j) / n) for k in range(n) for l in range(n)).real / 16 for j in range(n)]
            for i in range(n)
        ]
        g = [[v if v > delta else -v for v in row] for row in rho]
        gs = [
            [sum(g[i][j] * cmath.exp(-2j * math.pi * (k * i + l * j) / n) for i in range(n) for j in range(n)) for l in range(n)]
            for k in range(n)
        ]
        f = [[amp[k][l] * gs[k][l] / abs(gs[k][l]) if obs[k][l] else (gs[k][l] if (k, l) == (0, 0) else 0j) for l in range(n)] for k in range(n)]
    want = [[v.real for v in row] for row in idft2(f)]
    got, _ = charge_flipping(amp, obs, delta, 3, start=start)
    assert max_diff(got, want) < 1e-10


def test_translation_and_inversion_equivariance():
    true = structure(8, 8, 5, 7)
    _, amp, obs = data(true)
    start = random_start(amp, obs, 8)
    base, _ = charge_flipping(amp, obs, 0.2, 15, start=start)
    t1, t2 = 3, 5
    moved = [[start[k][l] * cmath.exp(-2j * math.pi * (k * t1 + l * t2) / 8) for l in range(8)] for k in range(8)]
    out, _ = charge_flipping(amp, obs, 0.2, 15, start=moved)
    assert max_diff(out, [[base[(i - t1) % 8][(j - t2) % 8] for j in range(8)] for i in range(8)]) < 1e-9
    inverted = [[v.conjugate() for v in row] for row in start]
    out, _ = charge_flipping(amp, obs, 0.2, 15, start=inverted)
    assert max_diff(out, [[base[-i % 8][-j % 8] for j in range(8)] for i in range(8)]) < 1e-9


def test_solves_a_small_2d_structure():
    true = structure(16, 16, 8, 1)
    _, amp, obs = data(true)
    rho10, r10 = charge_flipping(amp, obs, 0.2, 10, seed=1)
    rho, r = charge_flipping(amp, obs, 0.2, 150, seed=1)
    assert r10 > 0.3 and match_error(rho10, true) > 0.5
    assert r < 0.01
    assert match_error(rho, true) < 0.25


def test_r_factor_is_zero_at_the_truth():
    true = structure(8, 8, 4, 9)
    f, amp, obs = data(true)
    assert r_factor(amp, obs, f) < 1e-15


def test_low_r_does_not_prove_a_solution_in_1d():
    # With a small threshold in 1D, the iteration finds a dense density with the
    # right moduli: a low R, a wrong structure.
    true = structure(1, 64, 6, 1)
    _, amp, obs = data(true)
    rho, r = charge_flipping(amp, obs, 0.1, 200, seed=0)
    assert r < 1e-3
    assert match_error(rho, true) > 0.5
