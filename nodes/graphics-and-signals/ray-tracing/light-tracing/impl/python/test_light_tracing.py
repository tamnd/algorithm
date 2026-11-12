# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/light-tracing/. The authors are listed in prov/R3PDJC.jsonl.

"""Light tracing against exact answers of the rendering equation.

The scenes are a closed sphere with Lambertian zones, where the radiance is
constant on each zone, and two concentric spheres, exact by symmetry. The
reference solves the linear system with Fraction. A test passes when each
pixel is within 4 standard errors of the exact value.
"""

import random
from fractions import Fraction as Fr

from light_tracing import Scene, Sphere, connect, light_trace, trace_particle

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


def test_furnace() -> None:
    scene, _ = zoned([Fr(-1), Fr(1)], [Fr(1)], [Fr(1, 2)])
    check(light_trace(scene, 3000, random.Random(1)), [Fr(2)])


def test_zoned_sphere_against_linear_system() -> None:
    cuts = [Fr(-1), Fr(-1, 2), Fr(0), Fr(1, 2), Fr(1)]
    emit, albedo = [Fr(0), Fr(0), Fr(0), Fr(4)], [Fr(1, 2), Fr(1, 4), Fr(3, 4), Fr(1, 2)]
    scene, form = zoned(cuts, emit, albedo)
    check(light_trace(scene, 6000, random.Random(2)), exact(albedo, form, emit))


def test_concentric_spheres_with_occlusion() -> None:
    for e_out, a_out, e_in, a_in, seed in ((Fr(0), Fr(4, 5), Fr(1), Fr(1, 2), 3), (Fr(1), Fr(1, 2), Fr(0), Fr(3, 4), 4)):
        scene, form = concentric(e_out, a_out, e_in, a_in)
        check(light_trace(scene, 6000, random.Random(seed)), exact([a_out, a_in], form, [e_out, e_in]))


def test_depth_limit_matches_truncated_series() -> None:
    scene, form = concentric(Fr(0), Fr(4, 5), Fr(1), Fr(1, 2))
    for b in (0, 1, 2):
        ref = exact([Fr(4, 5), Fr(1, 2)], form, [Fr(0), Fr(1)], b)
        check(light_trace(scene, 4000, random.Random(10 + b), max_depth=b), ref)


def test_emitter_seen_directly() -> None:
    # With no bounces, the image is the emission that the camera sees. In the
    # zoned sphere every light point is visible and G We / pA is constant, so
    # each particle gives the exact pixel value.
    scene, _ = zoned([Fr(-1), Fr(0), Fr(1)], [Fr(0), Fr(2)], [Fr(1, 2), Fr(1, 2)])
    rng = random.Random(5)
    for _ in range(50):
        assert abs(trace_particle(scene, rng, max_depth=0)[1] - 2.0) < 1e-9


def test_hidden_points_do_not_connect() -> None:
    scene, _ = concentric(Fr(1), Fr(1, 2), Fr(0), Fr(3, 4))
    # the point of the outer sphere straight behind the inner one
    assert connect(scene, (0.0, 0.0, 2.0), (0.0, 0.0, -1.0)) is None
    assert connect(scene, (0.0, 0.0, -2.0), (0.0, 0.0, 1.0)) is not None
