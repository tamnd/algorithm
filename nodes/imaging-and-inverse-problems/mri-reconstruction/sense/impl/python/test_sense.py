# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sense/. The authors are listed in prov/7VT2V0.jsonl.

import cmath
import math
import random

import pytest

from imgkit import MODIFIED_SHEPP_LOGAN, ellipse_phantom, pixel_centers
from imgla import adjoint_gap, cholesky, matvec, solve
from sense import encode, encode_adjoint, g_factor, sense, unitary_idft2


def ring_maps(n, c=4):
    """Smooth synthetic coil maps: Gaussian profiles of coils on a ring of radius 1.2, with a phase."""
    xs, ys = pixel_centers(n)
    maps = []
    for k in range(c):
        ang = math.radians(20.0 + 360.0 * k / c)
        cx, cy = 1.2 * math.cos(ang), 1.2 * math.sin(ang)
        phase0 = 0.9 * k
        maps.append([
            [
                math.exp(-((x - cx) ** 2 + (y - cy) ** 2) / 1.2)
                * cmath.exp(1j * (phase0 + 0.4 * x - 0.3 * y))
                for x in xs
            ]
            for y in ys
        ])
    return maps


def phantom(n):
    xs, _ = pixel_centers(n)
    img = ellipse_phantom(n, MODIFIED_SHEPP_LOGAN)
    return [[v * cmath.exp(0.3j * x) for v, x in zip(row, xs)] for row in img]


def rel_err(a, b):
    num = sum(abs(u - v) ** 2 for ra, rb in zip(a, b) for u, v in zip(ra, rb))
    den = sum(abs(v) ** 2 for rb in b for v in rb)
    return math.sqrt(num / den)


@pytest.mark.parametrize("r", [2, 4])
def test_exact_without_noise(r):
    n = 32
    maps, x = ring_maps(n), phantom(n)
    y = encode(x, maps, r)
    assert rel_err(sense(y, maps, r), x) < 1e-9


def test_skipped_rows_are_not_read():
    n, r = 16, 2
    maps, x = ring_maps(n), phantom(n)
    y = encode(x, maps, r)
    rng = random.Random(3)
    for yk in y:
        for kappa in range(1, n, 2):
            yk[kappa] = [complex(rng.gauss(0, 9), rng.gauss(0, 9)) for _ in range(n)]
    assert rel_err(sense(y, maps, r), x) < 1e-9


def test_correlated_noise_covariance_keeps_exactness():
    n, r = 16, 2
    maps, x = ring_maps(n), phantom(n)
    psi = [[1.0, 0.3, 0.1j, 0.0], [0.3, 1.5, 0.2, 0.0], [-0.1j, 0.2, 0.8, 0.1], [0.0, 0.0, 0.1, 1.2]]
    y = encode(x, maps, r)
    assert rel_err(sense(y, maps, r, psi=psi), x) < 1e-9


def test_encoding_adjoint():
    n, r = 16, 2
    maps = ring_maps(n)
    rng = random.Random(5)
    x = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)] for _ in range(n)]
    y = [[[complex(rng.gauss(0, 1), rng.gauss(0, 1)) if kappa % r == 0 else 0j for _ in range(n)]
          for kappa in range(n)] for _ in maps]
    def flat(arrs):
        return [v for a in arrs for row in a for v in row]

    def unflat(v):
        return [[[v[(k * n + i) * n + j] for j in range(n)] for i in range(n)] for k in range(len(maps))]

    gap = adjoint_gap(
        lambda v: flat(encode(v, maps, r)),
        lambda w: encode_adjoint(unflat(w), maps, r),
        x,
        flat(y),
    )
    assert gap < 1e-10


def test_matches_dense_least_squares_with_noise():
    n, r = 8, 2
    maps = ring_maps(n)
    rng = random.Random(7)
    x = phantom(n)
    y = encode(x, maps, r)
    for yk in y:
        for kappa in range(0, n, r):
            yk[kappa] = [v + complex(rng.gauss(0, 0.05), rng.gauss(0, 0.05)) for v in yk[kappa]]
    # dense normal equations of the full model
    cols = []
    for idx in range(n * n):
        e = [[0j] * n for _ in range(n)]
        e[idx // n][idx % n] = 1.0
        cols.append([v for yk in encode(e, maps, r) for row in yk for v in row])
    data = [v for yk in y for row in yk for v in row]
    gram = [[sum(a.conjugate() * b for a, b in zip(cp, cq)) for cq in cols] for cp in cols]
    rhs = [sum(a.conjugate() * b for a, b in zip(cp, data)) for cp in cols]
    xs = solve(gram, rhs)
    out = sense(y, maps, r)
    assert max(abs(out[i][j] - xs[i * n + j]) for i in range(n) for j in range(n)) < 1e-9


def test_g_factor_is_at_least_one_and_one_without_acceleration():
    n = 16
    maps = ring_maps(n)
    g1 = g_factor(maps, 1)
    assert all(abs(v - 1.0) < 1e-12 for row in g1 for v in row)
    for r in (2, 4):
        g = g_factor(maps, r)
        assert min(v for row in g for v in row) >= 1.0 - 1e-12
    assert max(v for row in g_factor(maps, 4) for v in row) > max(v for row in g_factor(maps, 2) for v in row)


def test_g_factor_two_coil_hand_example():
    a = 0.5
    maps = [[[1.0, 1.0], [a, a]], [[a, a], [1.0, 1.0]]]
    g = g_factor(maps, 2)
    assert abs(g[0][0] - (1 + a * a) / (1 - a * a)) < 1e-12


def test_noise_variance_matches_theory():
    # Linear method: reconstruct pure k-space noise. Coil noise covariance psi at each sample.
    n, r, trials = 8, 2, 300
    maps = ring_maps(n)
    psi = [[1.0, 0.2, 0.0, 0.1], [0.2, 1.0, 0.2, 0.0], [0.0, 0.2, 1.0, 0.2], [0.1, 0.0, 0.2, 1.0]]
    low = cholesky(psi)
    rng = random.Random(11)
    s = 1.0 / math.sqrt(2.0)
    acc = {1: [[0.0] * n for _ in range(n)], r: [[0.0] * n for _ in range(n)]}
    for _ in range(trials):
        w = [[[complex(rng.gauss(0, s), rng.gauss(0, s)) for _ in range(n)] for _ in range(n)] for _ in maps]
        e = [[[0j] * n for _ in range(n)] for _ in maps]
        for kappa in range(n):
            for l in range(n):
                v = matvec(low, [wk[kappa][l] for wk in w])
                for k in range(len(maps)):
                    e[k][kappa][l] = v[k]
        for rr in (1, r):
            out = sense(e, maps, rr, psi=psi)
            for i in range(n):
                for j in range(n):
                    acc[rr][i][j] += abs(out[i][j]) ** 2 / trials
    # theory: variance R [(E^H Psi^-1 E)^-1]_pp, and var_R / var_1 = R g^2
    g = g_factor(maps, r, psi)
    ratio_emp = sum(acc[r][i][j] for i in range(n) for j in range(n)) / sum(
        acc[1][i][j] * r * g[i][j] ** 2 for i in range(n) for j in range(n))
    assert abs(ratio_emp - 1.0) < 0.08
    # full sampling: the variance is 1 / (s^H Psi^-1 s)
    pred = 0.0
    for i in range(n):
        for j in range(n):
            sv = [mp[i][j] for mp in maps]
            pred += 1.0 / sum(a.conjugate() * b for a, b in zip(sv, solve(psi, sv))).real
    emp = sum(acc[1][i][j] for i in range(n) for j in range(n))
    assert abs(emp / pred - 1.0) < 0.08


def test_r_larger_than_c_is_refused():
    maps = ring_maps(8, c=2)
    y = [[[0j] * 8 for _ in range(8)] for _ in maps]
    with pytest.raises(ValueError):
        sense(y, maps, 4)


def test_full_sampling_is_coil_combination():
    n = 8
    maps, x = ring_maps(n), phantom(n)
    y = encode(x, maps, 1)
    imgs = [unitary_idft2(yk) for yk in y]
    out = sense(y, maps, 1)
    for i in range(n):
        for j in range(n):
            sv = [mp[i][j] for mp in maps]
            est = sum(a.conjugate() * im[i][j] for a, im in zip(sv, imgs)) / sum(abs(a) ** 2 for a in sv)
            assert abs(out[i][j] - est) < 1e-12
