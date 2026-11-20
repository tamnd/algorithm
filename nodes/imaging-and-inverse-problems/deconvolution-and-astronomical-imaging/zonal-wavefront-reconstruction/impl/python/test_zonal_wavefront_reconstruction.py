# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zonal-wavefront-reconstruction/. The authors are listed in prov/4DD2FS.jsonl.

import math
import random
from fractions import Fraction as F

from imgla import adjoint_gap, solve, sym_eig
from zonal_wavefront_reconstruction import (
    GEOMETRIES,
    fried_forward,
    hudgin_forward,
    normal_matrix,
    null_space,
    project_out_null,
    reconstruct,
    residual_norm2,
    southwell_to_hudgin,
)


def rand_grid(rng, n1, n2):
    return [[rng.gauss(0, 1) for _ in range(n2)] for _ in range(n1)]


def max_diff(a, b):
    return max(abs(p - q) for ra, rb in zip(a, b) for p, q in zip(ra, rb))


def flat_s(s):
    return [v for part in s for row in part for v in row]


def test_adjoint_test_both_geometries():
    rng = random.Random(7)
    n = 6
    for geo, shapes in (("hudgin", ((n, n - 1), (n - 1, n))), ("fried", ((n - 1, n - 1), (n - 1, n - 1)))):
        fwd, adj = GEOMETRIES[geo]
        x = rand_grid(rng, n, n)
        y = tuple(rand_grid(rng, *sh) for sh in shapes)

        def a(v):
            return [flat_s(fwd(v))]

        def ah(w):
            vals = w[0]
            k = shapes[0][0] * shapes[0][1]
            dx = [vals[i * shapes[0][1]:(i + 1) * shapes[0][1]] for i in range(shapes[0][0])]
            rest = vals[k:]
            dy = [rest[i * shapes[1][1]:(i + 1) * shapes[1][1]] for i in range(shapes[1][0])]
            return adj((dx, dy), n)

        assert adjoint_gap(a, ah, x, [flat_s(y)]) < 1e-12


def test_two_by_two_loop_exact():
    # One loop of four Hudgin edges with the slope 1 on the top edge only.
    s = ([[F(1)], [F(0)]], [[F(0), F(0)]])
    phi = reconstruct(s, 2, "hudgin", tol=0)
    assert phi == [[F(-3, 8), F(3, 8)], [F(-1, 8), F(1, 8)]]
    # The fitted differences are (3/4, 1/4) along x and (1/4, -1/4) along y.
    dx, dy = hudgin_forward(phi)
    assert dx == [[F(3, 4)], [F(1, 4)]] and dy == [[F(1, 4), F(-1, 4)]]
    assert residual_norm2(phi, s, "hudgin") == F(1, 4)


def test_hudgin_exact_data_recovers_phase_up_to_piston():
    rng = random.Random(3)
    n = 8
    true = rand_grid(rng, n, n)
    got = reconstruct(hudgin_forward(true), n, "hudgin", tol=1e-13)
    assert max_diff(got, project_out_null(true, "hudgin")) < 1e-9


def test_fried_exact_data_loses_piston_and_waffle():
    rng = random.Random(4)
    n = 7
    true = rand_grid(rng, n, n)
    waffle = null_space("fried", n)[1]
    with_waffle = [[t + 0.8 * w + 2.0 for t, w in zip(rt, rw)] for rt, rw in zip(true, waffle)]
    # The waffle and the piston give zero slopes.
    assert max(abs(v) for v in flat_s(fried_forward(waffle))) == 0
    got = reconstruct(fried_forward(with_waffle), n, "fried", tol=1e-13)
    assert max_diff(got, project_out_null(true, "fried")) < 1e-9


def test_null_space_dimensions_by_eigenvalues():
    for geo, dim in (("hudgin", 1), ("fried", 2)):
        for n in (3, 4, 5):
            w, _ = sym_eig(normal_matrix(geo, n))
            assert sum(1 for v in w if abs(v) < 1e-9) == dim


def test_hudgin_normal_matrix_is_neumann_laplacian():
    n = 4
    m = normal_matrix("hudgin", n)
    for i in range(n):
        for j in range(n):
            k = i * n + j
            nbrs = [(i + di, j + dj) for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1))
                    if 0 <= i + di < n and 0 <= j + dj < n]
            assert m[k][k] == len(nbrs)
            for a, b in nbrs:
                assert m[k][a * n + b] == -1
            assert sum(m[k]) == 0


def test_noisy_slopes_match_brute_force_min_norm():
    rng = random.Random(11)
    n = 5
    for geo in ("hudgin", "fried"):
        fwd, adj = GEOMETRIES[geo]
        true = rand_grid(rng, n, n)
        dx, dy = fwd(true)
        s = ([[v + rng.gauss(0, 0.1) for v in row] for row in dx],
             [[v + rng.gauss(0, 0.1) for v in row] for row in dy])
        got = reconstruct(s, n, geo, tol=1e-14)
        # Brute force: (G^T G + sum z z^T / |z|^2) phi = G^T s has the min norm solution.
        m = normal_matrix(geo, n)
        for z in null_space(geo, n):
            zf = [v for row in z for v in row]
            zz = sum(v * v for v in zf)
            m = [[m[r][c] + zf[r] * zf[c] / zz for c in range(n * n)] for r in range(n * n)]
        b = [v for row in adj(s, n) for v in row]
        ref = solve(m, b)
        assert max(abs(g - r) for g, r in zip([v for row in got for v in row], ref)) < 1e-8
        # The residual is orthogonal to the range: G^T (G phi - s) = 0.
        g = fwd(got)
        res = tuple([[p - q for p, q in zip(ra, rb)] for ra, rb in zip(a, b2)] for a, b2 in zip(g, s))
        assert max(abs(v) for row in adj(res, n) for v in row) < 1e-8


def test_southwell_is_exact_for_quadratic_wavefronts():
    n, h = 6, 0.25
    xs = [-0.625 + h * j for j in range(n)]
    # Defocus plus astigmatism plus tilt: phi = 2 (x^2 + y^2) + 0.5 x y + 0.3 x.
    def phi(x, y):
        return 2 * (x * x + y * y) + 0.5 * x * y + 0.3 * x
    true = [[phi(xs[j], xs[i]) for j in range(n)] for i in range(n)]
    sx = [[4 * xs[j] + 0.5 * xs[i] + 0.3 for j in range(n)] for i in range(n)]
    sy = [[4 * xs[i] + 0.5 * xs[j] for j in range(n)] for i in range(n)]
    got = reconstruct(southwell_to_hudgin(sx, sy, h), n, "hudgin", tol=1e-14)
    assert max_diff(got, project_out_null(true, "hudgin")) < 1e-10


def test_cg_stops_early_with_tolerance_and_is_close():
    rng = random.Random(5)
    n = 8
    true = rand_grid(rng, n, n)
    s = hudgin_forward(true)
    loose = reconstruct(s, n, "hudgin", tol=1e-3)
    ref = project_out_null(true, "hudgin")
    err = math.sqrt(sum((p - q) ** 2 for rp, rq in zip(loose, ref) for p, q in zip(rp, rq)))
    nrm = math.sqrt(sum(q * q for rq in ref for q in rq))
    assert err < 0.05 * nrm
