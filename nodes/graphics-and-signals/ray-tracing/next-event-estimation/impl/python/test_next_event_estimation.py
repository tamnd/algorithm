# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/next-event-estimation/. The authors are listed in prov/WJBAKB.jsonl.

"""Next event estimation against exact answers of the rendering equation.

In a closed sphere with Lambertian zones, the radiance is constant on each
zone and solves a small linear system; two concentric spheres are exact by
symmetry. The reference solves these systems with Fraction. A Monte Carlo
test passes when the estimate is within 4 standard errors of the exact value.
"""

import math
import random
from fractions import Fraction as Fr

from next_event_estimation import Scene, Sphere, direct_light, render, sample_cosine

Z = 4.0


def solve(a: list[list[Fr]], b: list[Fr]) -> list[Fr]:
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


def exact(albedo: list[Fr], form: list[list[Fr]], emit: list[Fr], bounces: int | None = None) -> list[Fr]:
    n = len(emit)
    t = [[albedo[i] * form[i][j] for j in range(n)] for i in range(n)]
    if bounces is None:
        return solve([[(1 if i == j else 0) - t[i][j] for j in range(n)] for i in range(n)], emit)
    term, total = emit[:], emit[:]
    for _ in range(bounces):
        term = [sum(t[i][j] * term[j] for j in range(n)) for i in range(n)]
        total = [x + y for x, y in zip(total, term)]
    return total


def zoned(cuts: list[Fr], emit: list[Fr], albedo: list[Fr]) -> tuple[Scene, list[list[Fr]]]:
    s = Sphere(1.0, True, tuple(map(float, cuts)), tuple(map(float, emit)), tuple(map(float, albedo)))
    area = [(cuts[j + 1] - cuts[j]) / 2 for j in range(len(emit))]
    return Scene([s], 0.0, list(map(float, cuts))), [area[:] for _ in emit]


def concentric(e_out: Fr, a_out: Fr, e_in: Fr, a_in: Fr) -> tuple[Scene, list[list[Fr]]]:
    """Outer sphere R = 2, inner sphere r = 3/5, camera at distance 1 from the center.

    Pixel 0 (z < 4/5) sees the outer sphere and pixel 1 the inner one.
    """
    q = Fr(9, 100)
    outer = Sphere(2.0, True, (-1.0, 1.0), (float(e_out),), (float(a_out),))
    inner = Sphere(0.6, False, (-1.0, 1.0), (float(e_in),), (float(a_in),))
    return Scene([outer, inner], -1.0, [-1.0, 0.8, 1.0]), [[1 - q, q], [Fr(1), Fr(0)]]


def check(est: list[tuple[float, float]], ref: list[Fr]) -> None:
    for (mean, se), r in zip(est, ref):
        assert abs(mean - float(r)) <= Z * se + 1e-12, (mean, se, float(r))


SMALL = ([Fr(-1), Fr(0), Fr(9, 10), Fr(1)], [Fr(0), Fr(0), Fr(20)], [Fr(3, 4), Fr(1, 2), Fr(0)])


def plain_trace(scene: Scene, d, rng: random.Random) -> float:
    """Path tracing without light sampling, as a baseline for the variance."""
    total, beta, o = 0.0, 1.0, scene.camera
    while True:
        hit = scene.intersect(o, d)
        total += beta * hit.emit
        q = min(0.95, hit.albedo)
        if q == 0 or rng.random() >= q:
            return total
        beta *= hit.albedo / q
        o, d = hit.point, sample_cosine(hit.normal, rng)


def test_furnace() -> None:
    scene, form = zoned([Fr(-1), Fr(1)], [Fr(1)], [Fr(1, 2)])
    check(render(scene, 3000, random.Random(1)), [Fr(2)])


def test_zoned_sphere_against_linear_system() -> None:
    cuts = [Fr(-1), Fr(-1, 2), Fr(0), Fr(1, 2), Fr(1)]
    emit, albedo = [Fr(0), Fr(0), Fr(0), Fr(4)], [Fr(1, 2), Fr(1, 4), Fr(3, 4), Fr(1, 2)]
    scene, form = zoned(cuts, emit, albedo)
    ref = exact(albedo, form, emit)
    assert ref == [Fr(1), Fr(1, 2), Fr(3, 2), Fr(5)]
    check(render(scene, 2000, random.Random(2)), ref)


def test_small_light() -> None:
    cuts, emit, albedo = SMALL
    scene, form = zoned(cuts, emit, albedo)
    check(render(scene, 2000, random.Random(3)), exact(albedo, form, emit))


def test_concentric_spheres_with_occlusion() -> None:
    for e_out, a_out, e_in, a_in, seed in ((Fr(0), Fr(4, 5), Fr(1), Fr(1, 2), 4), (Fr(1), Fr(1, 2), Fr(0), Fr(3, 4), 5)):
        scene, form = concentric(e_out, a_out, e_in, a_in)
        check(render(scene, 2000, random.Random(seed)), exact([a_out, a_in], form, [e_out, e_in]))


def test_depth_limit_matches_truncated_series() -> None:
    scene, form = concentric(Fr(0), Fr(4, 5), Fr(1), Fr(1, 2))
    for bounces in (0, 1, 2):
        ref = exact([Fr(4, 5), Fr(1, 2)], form, [Fr(0), Fr(1)], bounces)
        check(render(scene, 2000, random.Random(20 + bounces), max_depth=bounces), ref)


def test_direct_light_is_unbiased_for_one_bounce() -> None:
    # From any wall point of the zoned sphere, the reflected direct light is
    # albedo times sum(a_j E_j); for the small light this is rho * 20 * 1/20.
    cuts, emit, albedo = SMALL
    scene, _ = zoned(cuts, emit, albedo)
    rng = random.Random(6)
    hit = scene.intersect((0.0, 0.0, 0.0), (0.6, 0.0, -0.8))
    # Inside a sphere every light point is visible and G / pA is constant, so
    # each sample gives the exact value: the estimator has zero variance.
    vals = [direct_light(scene, hit, rng) for _ in range(1000)]
    assert all(abs(v - 0.75) < 1e-12 for v in vals)
    # Between the concentric spheres, half of the inner light is hidden.
    scene, _ = concentric(Fr(0), Fr(4, 5), Fr(1), Fr(1, 2))
    hit = scene.intersect(scene.camera, (0.0, 0.0, -1.0))
    vals = [direct_light(scene, hit, rng) for _ in range(4000)]
    mean = sum(vals) / len(vals)
    sd = math.sqrt(sum((v - mean) ** 2 for v in vals) / (len(vals) - 1))
    assert abs(mean - 0.8 * 0.09) <= Z * sd / math.sqrt(len(vals))
    assert sd > 0.01


def test_lower_variance_than_plain_path_tracing() -> None:
    cuts, emit, albedo = SMALL
    scene, _ = zoned(cuts, emit, albedo)
    n = 1500
    rng = random.Random(7)
    plain = [plain_trace(scene, scene.sample_pixel(0, rng), rng) for _ in range(n)]
    nee = render(scene, n, random.Random(8))[0]
    m = sum(plain) / n
    sd_plain = math.sqrt(sum((v - m) ** 2 for v in plain) / (n - 1))
    assert nee[1] * math.sqrt(n) < sd_plain / 2
