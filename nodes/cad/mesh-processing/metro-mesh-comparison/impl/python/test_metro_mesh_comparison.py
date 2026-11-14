# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/metro-mesh-comparison/. The authors are listed in prov/YBB4K3.jsonl.

import math
import random
from fractions import Fraction

from metro_mesh_comparison import (
    UniformGrid,
    brute_force_dist2,
    dist2_point_triangle,
    metro,
    monte_carlo_samples,
    one_sided,
    subdivision_samples,
)
from mp3geom import cross, dot, sub

SQUARE = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]
SQUARE_FACES = [(0, 1, 2), (0, 2, 3)]


def segment_dist2(p, a, b):
    ab, ap = sub(b, a), sub(p, a)
    t = min(max(Fraction(dot(ap, ab), dot(ab, ab)), 0), 1)
    d = tuple(x - (y + t * z) for x, y, z in zip(p, a, ab))
    return dot(d, d)


def reference_dist2(p, a, b, c):
    """Exact distance by another route: the plane if the foot is inside, else the three edges."""
    n = cross(sub(b, a), sub(c, a))
    nn = dot(n, n)
    s = Fraction(dot(n, sub(p, a)), nn)
    q = tuple(x - s * y for x, y in zip(p, n))
    inside = all(dot(cross(sub(v, u), sub(q, u)), n) >= 0 for u, v in ((a, b), (b, c), (c, a)))
    if inside:
        return s * s * nn
    return min(segment_dist2(p, a, b), segment_dist2(p, b, c), segment_dist2(p, c, a))


def random_mesh(rng, n_faces, size=6):
    points = [tuple(rng.randint(-size, size) for _ in range(3)) for _ in range(n_faces + 2)]
    faces = []
    while len(faces) < n_faces:
        f = tuple(rng.sample(range(len(points)), 3))
        a, b, c = (points[v] for v in f)
        if cross(sub(b, a), sub(c, a)) != (0, 0, 0):
            faces.append(f)
    return points, faces


def test_point_triangle_distance_is_exact() -> None:
    rng = random.Random(1998)
    for _ in range(3000):
        while True:
            a, b, c = (tuple(rng.randint(-5, 5) for _ in range(3)) for _ in range(3))
            if cross(sub(b, a), sub(c, a)) != (0, 0, 0):
                break
        p = tuple(Fraction(rng.randint(-40, 40), 4) for _ in range(3))
        assert dist2_point_triangle(p, a, b, c) == reference_dist2(p, a, b, c)
    # the corners, edge points and inner points of the triangle are at distance 0
    a, b, c = (0, 0, 0), (4, 0, 0), (0, 4, 0)
    for p in (a, b, c, (2, 0, 0), (2, 2, 0), (1, 1, 0)):
        assert dist2_point_triangle(p, a, b, c) == 0


def test_grid_equals_brute_force() -> None:
    rng = random.Random(7)
    for h in (1, 2, Fraction(5, 2)):
        points, faces = random_mesh(rng, 25)
        grid = UniformGrid(points, faces, h)
        for _ in range(120):
            p = tuple(Fraction(rng.randint(-60, 60), 5) for _ in range(3))
            assert grid.dist2(p) == brute_force_dist2(p, points, faces)


def test_parallel_squares() -> None:
    up = [(x, y, Fraction(1, 2)) for x, y, _ in SQUARE]
    ab, ba, sym = metro(SQUARE, SQUARE_FACES, up, SQUARE_FACES, k=4, n=200)
    for maximum, mean, rms in (ab, ba):
        assert maximum == mean == rms == 0.5
    assert sym == 0.5


def test_square_against_half_square() -> None:
    # The corner (1, 1, 0) of the square is sqrt(2)/2 from the triangle, and the triangle lies on the square.
    half = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
    ab, ba, sym = metro(SQUARE, SQUARE_FACES, half, [(0, 1, 2)], k=4, n=200)
    assert ab[0] == math.sqrt(2) / 2
    assert ba == (0.0, 0.0, 0.0)
    assert sym == math.sqrt(2) / 2


def test_tilted_plane_mean_and_rms() -> None:
    # B lies in the plane z = x / 2. A point (x, y, 0) of A is x / sqrt(5) from it, and its foot is inside B.
    tilted = [(0, 0, 0), (1, 0, Fraction(1, 2)), (1, 1, Fraction(1, 2)), (0, 1, 0)]
    samples = monte_carlo_samples(SQUARE, SQUARE_FACES, 3000, random.Random(17))
    maximum, mean, rms = one_sided(samples + subdivision_samples(SQUARE, SQUARE_FACES, 8), tilted, SQUARE_FACES)
    assert maximum == math.sqrt(Fraction(1, 5))       # exact sample at x = 1
    assert abs(mean - 1 / (2 * math.sqrt(5))) < 0.01  # the true mean; 0.01 is about 4 standard errors
    assert abs(rms - math.sqrt(1 / 15)) < 0.01


def test_refinement_sandwich() -> None:
    # sampled(k) <= sampled(2k) <= the true one-sided distance <= sampled(k) + the longest sub-triangle edge
    rng = random.Random(3)
    for _ in range(4):
        pa, fa = random_mesh(rng, 4)
        pb, fb = random_mesh(rng, 6)
        longest = max(math.sqrt(dot(sub(pa[f[i]], pa[f[(i + 1) % 3]]), sub(pa[f[i]], pa[f[(i + 1) % 3]]))) for f in fa for i in range(3))
        k = 3
        lo = one_sided(subdivision_samples(pa, fa, k), pb, fb)[0]
        hi = one_sided(subdivision_samples(pa, fa, 2 * k), pb, fb)[0]
        assert lo <= hi + 1e-12
        assert hi <= lo + longest / k + 1e-12


def test_float_fails_on_a_sliver() -> None:
    # A triangle of length 2 and width 1e-15: in doubles the region tests and the division lose all digits.
    a, b = (0.0, 0.0, 0.0), (1.0, 0.0, 0.0)
    c = (1.9875242733132161, 8.342347734145901e-16, 7.384876595764672e-16)
    p = (0.5196353826017766, 0.3307482815418452, -0.24314659152190998)
    exact = dist2_point_triangle(tuple(map(Fraction, p)), *(tuple(map(Fraction, v)) for v in (a, b, c)))
    assert exact == reference_dist2(tuple(map(Fraction, p)), *(tuple(map(Fraction, v)) for v in (a, b, c)))
    error = abs(math.sqrt(dist2_point_triangle(p, a, b, c)) - math.sqrt(exact))
    assert error > 0.02                       # measured 0.0251


def test_grid_and_brute_force_give_the_same_report() -> None:
    rng = random.Random(11)
    pa, fa = random_mesh(rng, 6)
    pb, fb = random_mesh(rng, 8)
    assert metro(pa, fa, pb, fb, k=3, n=100) == metro(pa, fa, pb, fb, k=3, n=100, h=2)
