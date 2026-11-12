# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bidirectional-path-tracing/. The authors are listed in prov/RKAS24.jsonl.

"""Bidirectional path tracing against exact answers of the rendering equation.

A sample joins paths of at most K edges, which carry the light of at most
K - 1 reflections, so the reference is the Neumann series cut after K - 1
terms, computed with Fraction. A test passes when each pixel is within 4
standard errors of the exact value.
"""

import math
import random
from fractions import Fraction as Fr

from bidirectional_path_tracing import (
    Scene,
    Sphere,
    camera_subpath,
    connections,
    light_subpath,
    mis_weight,
    render,
    strategy_pdfs,
    throughput,
)

Z = 4.0


def solve(a, b):
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                g = m[r][c] / m[c][c]
                m[r] = [x - g * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def exact(albedo, form, emit, bounces=None):
    n = len(emit)
    t = [[albedo[i] * form[i][j] for j in range(n)] for i in range(n)]
    if bounces is None:
        return solve([[(1 if i == j else 0) - t[i][j] for j in range(n)] for i in range(n)], emit)
    term, total = emit[:], emit[:]
    for _ in range(bounces):
        term = [sum(t[i][j] * term[j] for j in range(n)) for i in range(n)]
        total = [x + y for x, y in zip(total, term)]
    return total


def zoned(cuts, emit, albedo):
    s = Sphere(1.0, True, tuple(map(float, cuts)), tuple(map(float, emit)), tuple(map(float, albedo)))
    area = [(cuts[j + 1] - cuts[j]) / 2 for j in range(len(emit))]
    return Scene([s], 0.0, list(map(float, cuts))), [area[:] for _ in emit]


def concentric(e_out, a_out, e_in, a_in):
    """Outer sphere R = 2, inner sphere r = 3/5, camera at distance 1 from the center."""
    q = Fr(9, 100)
    outer = Sphere(2.0, True, (-1.0, 1.0), (float(e_out),), (float(a_out),))
    inner = Sphere(0.6, False, (-1.0, 1.0), (float(e_in),), (float(a_in),))
    return Scene([outer, inner], -1.0, [-1.0, 0.8, 1.0]), [[1 - q, q], [Fr(1), Fr(0)]]


def check(est, ref):
    for (mean, se), r in zip(est, ref):
        assert abs(mean - float(r)) <= Z * se + 1e-12, (mean, se, float(r))


def test_mis_weights_sum_to_one() -> None:
    scene, _ = concentric(Fr(0), Fr(4, 5), Fr(1), Fr(1, 2))
    rng = random.Random(1)
    seen = 0
    for _ in range(300):
        light, cam = light_subpath(scene, rng, 3), camera_subpath(scene, rng, 4)
        for s, t, x in connections(scene, light, cam, 3):
            if throughput(scene, x)[1] == 0:
                continue
            pdfs = strategy_pdfs(scene, x)
            for h in ("balance", "power"):
                assert abs(sum(mis_weight(pdfs, i, h) for i in range(len(pdfs))) - 1) < 1e-12
            seen += 1
    assert seen > 100


def test_furnace() -> None:
    # Uniform emission 1 and albedo 1/2: paths of at most 3 edges give 1 + 1/2 + 1/4.
    scene, _ = zoned([Fr(-1), Fr(1)], [Fr(1)], [Fr(1, 2)])
    check(render(scene, 2000, random.Random(2), 3), [Fr(7, 4)])


def test_zoned_sphere_against_truncated_linear_system() -> None:
    cuts = [Fr(-1), Fr(-1, 2), Fr(0), Fr(1, 2), Fr(1)]
    emit, albedo = [Fr(0), Fr(0), Fr(0), Fr(4)], [Fr(1, 2), Fr(1, 4), Fr(3, 4), Fr(1, 2)]
    scene, form = zoned(cuts, emit, albedo)
    for h, seed in (("power", 3), ("balance", 4)):
        check(render(scene, 2000, random.Random(seed), 3, h), exact(albedo, form, emit, 2))


def test_concentric_spheres_with_occlusion() -> None:
    for e_out, a_out, e_in, a_in, seed in ((Fr(0), Fr(4, 5), Fr(1), Fr(1, 2), 5), (Fr(1), Fr(1, 2), Fr(0), Fr(3, 4), 6)):
        scene, form = concentric(e_out, a_out, e_in, a_in)
        check(render(scene, 2000, random.Random(seed), 3), exact([a_out, a_in], form, [e_out, e_in], 2))


def test_each_strategy_alone_is_unbiased_for_its_path_length() -> None:
    scene, form = concentric(Fr(0), Fr(4, 5), Fr(1), Fr(1, 2))
    a, e = [Fr(4, 5), Fr(1, 2)], [Fr(0), Fr(1)]
    for k, seed in ((1, 7), (2, 8)):
        ref = [x - y for x, y in zip(exact(a, form, e, k - 1), exact(a, form, e, k - 2) if k > 1 else [0, 0])]
        for s in range(k + 1):
            check(render(scene, 2500, random.Random(seed + 10 * s), k, only=(s, k + 1 - s)), ref)


def test_camera_only_strategy_matches_path_tracing_weight() -> None:
    # Strategy s = 0 is path tracing with a uniform pinhole: f / p0 = (4 pi / Omega_j) E rho_1 .. rho_{k-1}.
    scene, _ = concentric(Fr(0), Fr(4, 5), Fr(1), Fr(1, 2))
    rng = random.Random(9)
    seen = 0
    for _ in range(400):
        light, cam = light_subpath(scene, rng, 3), camera_subpath(scene, rng, 4)
        for s, t, x in connections(scene, light, cam, 3):
            j, f = throughput(scene, x)
            if f == 0 or s != 0:
                continue
            omega = 2 * math.pi * (scene.pixel_cuts[j + 1] - scene.pixel_cuts[j])
            rho = math.prod(v.albedo for v in x[1:-1])
            c = f / strategy_pdfs(scene, x)[0]
            assert abs(c - 4 * math.pi / omega * x[0].emit * rho) < 1e-9 * c
            seen += 1
    assert seen > 50


def test_depth_one_is_the_visible_emission() -> None:
    scene, form = zoned([Fr(-1), Fr(0), Fr(1)], [Fr(0), Fr(2)], [Fr(3, 4), Fr(1, 4)])
    check(render(scene, 1500, random.Random(11), 1), [Fr(0), Fr(2)])
