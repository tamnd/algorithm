# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cg-sense/. The authors are listed in prov/CCN5EK.jsonl.

import cmath
import math
import random

from cg_sense import cartesian_ops, cg_sense, nudft_ops, radial_density, radial_points
from imgkit import MODIFIED_SHEPP_LOGAN, ellipse_phantom, pixel_centers
from imgla import adjoint_gap, solve


def ring_maps(n, c=4):
    """Smooth synthetic coil maps: Gaussian profiles of coils on a ring of radius 1.2, with a phase."""
    xs, ys = pixel_centers(n)
    maps = []
    for k in range(c):
        ang = math.radians(20.0 + 360.0 * k / c)
        cx, cy = 1.2 * math.cos(ang), 1.2 * math.sin(ang)
        maps.append([
            [
                math.exp(-((x - cx) ** 2 + (y - cy) ** 2) / 1.2) * cmath.exp(1j * (0.9 * k + 0.4 * x - 0.3 * y))
                for x in xs
            ]
            for y in ys
        ])
    return maps


def phantom_vec(n):
    xs, _ = pixel_centers(n)
    img = ellipse_phantom(n, MODIFIED_SHEPP_LOGAN)
    return [v * cmath.exp(0.3j * x) for row in img for v, x in zip(row, xs)]


def rel(a, b):
    return math.sqrt(sum(abs(u - v) ** 2 for u, v in zip(a, b)) / sum(abs(v) ** 2 for v in b))


def dense_solution(apply_e, apply_eh, size, y, weights):
    """The solution of E^H D E x = E^H D y by Gaussian elimination."""
    cols = []
    for q in range(size):
        e = [0j] * size
        e[q] = 1.0
        cols.append(apply_eh([w * v for w, v in zip(weights, apply_e(e))]))
    a = [[cols[q][p] for q in range(size)] for p in range(size)]
    return solve(a, apply_eh([w * v for w, v in zip(weights, y)])), a


def test_adjoint_cartesian_and_nudft():
    rng = random.Random(1)
    n = 8
    maps = ring_maps(n)
    mask = [[rng.random() < 0.5 for _ in range(n)] for _ in range(n)]
    pts = radial_points(6, 8)
    for e, eh in (cartesian_ops(maps, mask), nudft_ops(maps, pts)):
        x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n * n)]
        y = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(len(e(x)))]
        assert adjoint_gap(e, eh, x, y) < 1e-10


def unfold_r2(y_img, maps, n):
    """Per-pixel SENSE for R = 2 (rows kappa even kept), written out for the comparison."""
    from imgkit import idft2
    m = n // 2
    folded = []
    for yk in y_img:
        sub = [yk[kappa] for kappa in range(0, n, 2)]
        folded.append([[v * n for v in row] for row in idft2(sub)])
    out = [0j] * (n * n)
    for i in range(m):
        for j in range(n):
            e = [[mp[i][j], mp[i + m][j]] for mp in maps]
            gram = [[sum(e[k][p].conjugate() * e[k][q] for k in range(len(maps))) for q in range(2)] for p in range(2)]
            rhs = [sum(e[k][p].conjugate() * folded[k][i][j] for k in range(len(maps))) for p in range(2)]
            v = solve(gram, rhs)
            out[i * n + j], out[(i + m) * n + j] = v[0], v[1]
    return out


def test_uniform_cartesian_equals_sense_with_noise():
    n = 32
    maps = ring_maps(n)
    mask = [[kappa % 2 == 0] * n for kappa in range(n)]
    e, eh = cartesian_ops(maps, mask)
    rng = random.Random(4)
    y = [v + complex(rng.gauss(0, 0.002), rng.gauss(0, 0.002)) for v in e(phantom_vec(n))]
    x = cg_sense(y, e, eh, n * n, 45, tol=1e-12)
    # put the samples back on the grid for the direct SENSE unfolding
    per = n * n // 2
    y_img = []
    for k in range(len(maps)):
        arr = [[0j] * n for _ in range(n)]
        t = 0
        for kappa in range(n):
            for l in range(n):
                if mask[kappa][l]:
                    arr[kappa][l] = y[k * per + t]
                    t += 1
        y_img.append(arr)
    assert rel(x, unfold_r2(y_img, maps, n)) < 1e-8


def test_noiseless_variable_density_mask_converges_to_the_object():
    n = 32
    maps = ring_maps(n)
    rng = random.Random(9)
    keep = [abs(kappa if kappa < n // 2 else kappa - n) < 4 or rng.random() < 0.6 for kappa in range(n)]
    mask = [[keep[kappa]] * n for kappa in range(n)]
    e, eh = cartesian_ops(maps, mask)
    x0 = phantom_vec(n)
    errs = []
    cg_sense(e(x0), e, eh, n * n, 30, callback=lambda t, x: errs.append(rel(x, x0)))
    assert errs[-1] < 1e-6
    assert errs[-1] < errs[4] < errs[0]


def test_radial_matches_dense_least_squares_with_and_without_density():
    n = 8
    maps = ring_maps(n)
    pts = radial_points(8, 8)
    e, eh = nudft_ops(maps, pts)
    rng = random.Random(2)
    y = [v + complex(rng.gauss(0, 0.01), rng.gauss(0, 0.01)) for v in e(phantom_vec(n))]
    dens = radial_density(pts) * len(maps)
    for w in (None, dens):
        ref, _ = dense_solution(e, eh, n * n, y, w or [1.0] * len(y))
        x = cg_sense(y, e, eh, n * n, 64, weights=w, tol=1e-13)
        assert rel(x, ref) < 1e-8


def test_energy_norm_error_does_not_increase():
    n = 8
    maps = ring_maps(n)
    pts = radial_points(8, 8)
    e, eh = nudft_ops(maps, pts)
    rng = random.Random(6)
    y = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(len(pts) * len(maps))]
    ones = [1.0] * len(y)
    xs, a = dense_solution(e, eh, n * n, y, ones)

    def energy(x):
        d = [u - v for u, v in zip(x, xs)]
        ad = [sum(a[p][q] * d[q] for q in range(n * n)) for p in range(n * n)]
        return sum(u.conjugate() * v for u, v in zip(d, ad)).real

    vals = [energy([0j] * (n * n))]
    cg_sense(y, e, eh, n * n, 64, callback=lambda t, x: vals.append(energy(x)))
    assert all(b <= a_ * (1 + 1e-9) + 1e-12 for a_, b in zip(vals, vals[1:]))
    assert vals[-1] < 1e-12 * vals[0]


def test_noiseless_radial_reaches_the_object():
    n = 8
    maps = ring_maps(n)
    pts = radial_points(8, 8)
    e, eh = nudft_ops(maps, pts)
    x0 = phantom_vec(n)
    dens = radial_density(pts) * len(maps)
    for w in (None, dens):
        assert rel(cg_sense(e(x0), e, eh, n * n, 64, weights=w, tol=1e-13), x0) < 1e-6
