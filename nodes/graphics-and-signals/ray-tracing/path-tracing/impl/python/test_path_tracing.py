# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/path-tracing/. The authors are listed in prov/PCC896.jsonl.

"""Path tracing against exact answers of the rendering equation.

In a closed sphere with Lambertian zones, a cosine sampled ray from any
point of the wall lands uniformly by area on the wall, so the radiance is
constant on each zone and the zone radiances solve a small linear system.
Two concentric spheres with constant materials are also exact by symmetry.
The reference solves these systems with Fraction. Each Monte Carlo test
passes when the estimate is within 4 standard errors of the exact value.
"""

import math
import random
from fractions import Fraction as Fr

from path_tracing import Scene, Sphere, path_trace, render

Z = 4.0  # the statistical bound, in standard errors


def solve(a: list[list[Fr]], b: list[Fr]) -> list[Fr]:
    """Gaussian elimination with exact rational arithmetic."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def transport(albedo: list[Fr], form: list[list[Fr]]) -> list[list[Fr]]:
    return [[albedo[i] * form[i][j] for j in range(len(albedo))] for i in range(len(albedo))]


def exact(albedo: list[Fr], form: list[list[Fr]], emit: list[Fr]) -> list[Fr]:
    """The solution of L = E + diag(albedo) F L."""
    t = transport(albedo, form)
    n = len(emit)
    a = [[(1 if i == j else 0) - t[i][j] for j in range(n)] for i in range(n)]
    return solve(a, emit)


def truncated(albedo: list[Fr], form: list[list[Fr]], emit: list[Fr], bounces: int) -> list[Fr]:
    """The Neumann series E + T E + ... + T^bounces E."""
    t = transport(albedo, form)
    term, total = emit[:], emit[:]
    for _ in range(bounces):
        term = [sum(t[i][j] * term[j] for j in range(len(term))) for i in range(len(term))]
        total = [x + y for x, y in zip(total, term)]
    return total


def zoned(cuts: list[Fr], emit: list[Fr], albedo: list[Fr]) -> tuple[Scene, list[list[Fr]]]:
    """A unit sphere seen from its center; pixel j sees zone j exactly."""
    s = Sphere(1.0, True, tuple(map(float, cuts)), tuple(map(float, emit)), tuple(map(float, albedo)))
    area = [(cuts[j + 1] - cuts[j]) / 2 for j in range(len(emit))]
    return Scene([s], 0.0, list(map(float, cuts))), [area[:] for _ in emit]


def concentric(e_out: Fr, a_out: Fr, e_in: Fr, a_in: Fr) -> tuple[Scene, list[list[Fr]]]:
    """Outer sphere of radius 2 (index 0), inner sphere of radius 3/5 (index 1).

    The camera is at distance 1 from the center, so the inner sphere fills the
    cone of directions with cos >= 4/5 about +z: pixel 0 sees only the outer
    sphere and pixel 1 only the inner sphere.
    """
    q = Fr(9, 100)  # (r / R)^2, the form factor from the outer sphere to the inner one
    outer = Sphere(2.0, True, (-1.0, 1.0), (float(e_out),), (float(a_out),))
    inner = Sphere(0.6, False, (-1.0, 1.0), (float(e_in),), (float(a_in),))
    return Scene([outer, inner], -1.0, [-1.0, 0.8, 1.0]), [[1 - q, q], [Fr(1), Fr(0)]]


def check(est: list[tuple[float, float]], ref: list[Fr]) -> None:
    for (mean, se), r in zip(est, ref):
        assert abs(mean - float(r)) <= Z * se + 1e-12, (mean, se, float(r))


def test_furnace_geometric_series() -> None:
    # Emission 1 and albedo 1/2 everywhere: L = 1 + 1/2 + 1/4 + ... = 2.
    scene, _ = zoned([Fr(-1), Fr(1)], [Fr(1)], [Fr(1, 2)])
    rng = random.Random(1)
    n = 4000
    vals = [path_trace(scene, scene.camera, scene.sample_pixel(0, rng), rng) for _ in range(n)]
    # With survival probability equal to the albedo, each estimate counts the
    # vertices of the path, a geometric variable with mean 2 and variance 2.
    assert all(v == int(v) and v >= 1 for v in vals)
    mean = sum(vals) / n
    assert abs(mean - 2.0) <= Z * math.sqrt(2.0 / n)


def test_zoned_sphere_against_linear_system() -> None:
    cuts = [Fr(-1), Fr(-1, 2), Fr(0), Fr(1, 2), Fr(1)]
    emit = [Fr(0), Fr(0), Fr(0), Fr(4)]
    albedo = [Fr(1, 2), Fr(1, 4), Fr(3, 4), Fr(1, 2)]
    scene, form = zoned(cuts, emit, albedo)
    ref = exact(albedo, form, emit)
    check(render(scene, 3000, random.Random(2)), ref)


def test_zoned_sphere_closed_form() -> None:
    # The incident radiance is C = sum(a E) / (1 - sum(a rho)) everywhere.
    cuts = [Fr(-1), Fr(-1, 2), Fr(0), Fr(1, 2), Fr(1)]
    emit = [Fr(0), Fr(0), Fr(0), Fr(4)]
    albedo = [Fr(1, 2), Fr(1, 4), Fr(3, 4), Fr(1, 2)]
    _, form = zoned(cuts, emit, albedo)
    a = form[0]
    c = sum(x * e for x, e in zip(a, emit)) / (1 - sum(x * r for x, r in zip(a, albedo)))
    assert exact(albedo, form, emit) == [e + r * c for e, r in zip(emit, albedo)]
    assert c == 2


def test_concentric_spheres_with_occlusion() -> None:
    for e_out, a_out, e_in, a_in, seed in ((Fr(0), Fr(4, 5), Fr(1), Fr(1, 2), 3), (Fr(1), Fr(1, 2), Fr(0), Fr(3, 4), 4)):
        scene, form = concentric(e_out, a_out, e_in, a_in)
        ref = exact([a_out, a_in], form, [e_out, e_in])
        check(render(scene, 3000, random.Random(seed)), ref)


def test_depth_limit_matches_truncated_series() -> None:
    cuts = [Fr(-1), Fr(0), Fr(1)]
    emit, albedo = [Fr(0), Fr(2)], [Fr(3, 4), Fr(1, 4)]
    scene, form = zoned(cuts, emit, albedo)
    for bounces in (0, 1, 3):
        ref = truncated(albedo, form, emit, bounces)
        check(render(scene, 2000, random.Random(10 + bounces), max_depth=bounces), ref)
    # With no bounces the estimate is the emission of the zone that is seen.
    assert [m for m, _ in render(scene, 10, random.Random(0), max_depth=0)] == [0.0, 2.0]


def test_roulette_start_depth_keeps_the_mean() -> None:
    scene, form = concentric(Fr(0), Fr(4, 5), Fr(1), Fr(1, 2))
    ref = exact([Fr(4, 5), Fr(1, 2)], form, [Fr(0), Fr(1)])
    check(render(scene, 3000, random.Random(5), rr_depth=3), ref)
