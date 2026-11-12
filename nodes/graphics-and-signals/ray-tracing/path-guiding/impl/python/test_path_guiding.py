# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/path-guiding/. The authors are listed in prov/XGS21H.jsonl.

"""Path guiding against exact answers of the rendering equation.

Every training iteration renders an unbiased image, so each image must be
within 4 standard errors of the exact value. Paths cut after k reflections
are compared with the Neumann series cut after k terms, computed with
Fraction. Other tests check the parts: the direction map, the density and
the sampling of the quadtree, the split of the spatial tree, and that the
guide moves its samples to the light.
"""

import functools
import math
import random
from fractions import Fraction as Fr

from path_guiding import (
    Guide,
    QuadTree,
    Scene,
    Sphere,
    dot,
    from_square,
    sample_cosine,
    scale,
    to_square,
    train_and_render,
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


def check(est, ref):
    for (mean, se), r in zip(est, ref):
        assert abs(mean - float(r)) <= Z * se + 1e-12, (mean, se, float(r))


CUTS = [Fr(-1), Fr(0), Fr(9, 10), Fr(1)]
EMIT = [Fr(0), Fr(0), Fr(20)]


@functools.lru_cache(maxsize=None)
def floor_run():
    """Direct light only, a camera pixel on the floor; trained for six iterations."""
    s = Sphere(1.0, True, tuple(map(float, CUTS)), tuple(map(float, EMIT)), (0.25, 0.25, 0.0))
    scene = Scene([s], 0.0, [-1.0, -0.8, 0.9, 1.0])
    images, guide = train_and_render(scene, 200, 6, random.Random(5), max_records=2000, path_depth=1)
    return scene, images, guide


def test_map_has_constant_jacobian() -> None:
    rng = random.Random(1)
    h = 1e-6
    for _ in range(200):
        u, v = 0.05 + 0.9 * rng.random(), h + rng.random() * (1 - 2 * h)
        d = from_square(u, v)
        assert abs(dot(d, d) - 1) < 1e-12
        back = to_square(d)
        assert abs(back[0] - u) < 1e-12 and abs(back[1] - v) < 1e-9
        a0, a1, b0, b1 = from_square(u - h, v), from_square(u + h, v), from_square(u, v - h), from_square(u, v + h)
        du = [(a1[k] - a0[k]) / (2 * h) for k in range(3)]
        dv = [(b1[k] - b0[k]) / (2 * h) for k in range(3)]
        cross = (du[1] * dv[2] - du[2] * dv[1], du[2] * dv[0] - du[0] * dv[2], du[0] * dv[1] - du[1] * dv[0])
        assert abs(math.sqrt(dot(cross, cross)) - 4 * math.pi) < 1e-5


def leaves(tree):
    stack = [(0, 0.0, 0.0, 1.0)]
    while stack:
        n, u0, v0, size = stack.pop()
        if tree.child[n] < 0:
            yield n, u0, v0, size
            continue
        half = size / 2
        for c in range(4):
            stack.append((tree.child[n] + c, u0 + half * (c // 2), v0 + half * (c % 2), half))


def test_quadtree_density_is_normalized_and_matches_sampling() -> None:
    rng = random.Random(2)
    old = QuadTree()
    for _ in range(3000):
        old.record(rng.random() ** 3, rng.random(), 1.0)
    tree = old.refined(0.01, 6)
    assert len(tree.child) > 1
    for _ in range(5000):
        tree.record(rng.random() ** 3, 0.5 * rng.random(), rng.random())
    total = sum(tree.pdf(u0 + size / 2, v0 + size / 2) * size * size for _, u0, v0, size in leaves(tree))
    assert abs(total - 1) < 1e-9
    n = 20000
    counts = [0] * 4
    first = tree.child[0]
    for _ in range(n):
        u, v = tree.sample(rng)
        assert tree.pdf(u, v) > 0
        counts[2 * int(u >= 0.5) + int(v >= 0.5)] += 1
    for c in range(4):
        p = tree.energy[first + c] / tree.energy[0]
        assert abs(counts[c] - n * p) <= Z * math.sqrt(n * p * (1 - p)) + 1e-9


def test_spatial_tree_splits_busy_cells() -> None:
    rng = random.Random(3)
    g = Guide()
    for _ in range(100):
        z, phi = 2 * rng.random() - 1, 2 * math.pi * rng.random()
        r = math.sqrt(1 - z * z)
        g.record(0, from_square(rng.random(), rng.random()), 1.0)
        assert g.cell_of((r * math.cos(phi), r * math.sin(phi), z)) == 0
    new = g.refined(0.01, 4, 10)  # 100 > 10 records: 100, 50, 25, 12, 6, so four levels
    shape = g.tree[0].refined(0.01, 4).child
    found = [n for n in range(len(new.child)) if new.child[n] < 0]
    assert len(found) == 16
    for n in found:
        assert new.depth[n] == 4 and new.tree[n].child == shape and new.tree[n].energy[0] == 0
    for _ in range(200):
        z, phi = 2 * rng.random() - 1, 2 * math.pi * rng.random()
        r = math.sqrt(1 - z * z)
        assert new.child[new.cell_of((r * math.cos(phi), r * math.sin(phi), z))] < 0


def test_direct_light_is_unbiased_in_every_iteration() -> None:
    _, form = zoned(CUTS, EMIT, [Fr(1, 4), Fr(1, 4), Fr(0)])
    ref = exact([Fr(1, 4), Fr(1, 4), Fr(0)], form, EMIT, 1)
    assert ref == [Fr(1, 4), Fr(1, 4), Fr(20)]
    _, images, _ = floor_run()
    for image in images:
        check(image, ref)


def test_guide_moves_samples_to_the_light() -> None:
    scene, _, guide = floor_run()
    rng = random.Random(4)
    x = (0.3, 0.1, -math.sqrt(1 - 0.1))
    n, cell = scale(x, -1), guide.cell_of(x)
    m = 4000
    by_guide = sum(scene.intersect(x, w).emit > 0 for w in (guide.sample(cell, rng) for _ in range(m))
                   if dot(n, w) > 0)
    by_cosine = sum(scene.intersect(x, sample_cosine(n, rng)).emit > 0 for _ in range(m))
    assert by_guide > 4 * by_cosine


def test_two_bounces_on_zoned_sphere() -> None:
    cuts, emit = [Fr(-1), Fr(-1, 2), Fr(0), Fr(1, 2), Fr(1)], [Fr(0), Fr(0), Fr(0), Fr(4)]
    albedo = [Fr(1, 2), Fr(1, 4), Fr(3, 4), Fr(1, 2)]
    scene, form = zoned(cuts, emit, albedo)
    ref = exact(albedo, form, emit, 2)
    assert ref == [Fr(3, 4), Fr(3, 8), Fr(9, 8), Fr(19, 4)]
    images, _ = train_and_render(scene, 150, 4, random.Random(6), max_records=1000, path_depth=2)
    for image in images:
        check(image, ref)


def test_russian_roulette_full_solution() -> None:
    albedo = [Fr(3, 4), Fr(1, 2), Fr(0)]
    scene, form = zoned(CUTS, EMIT, albedo)
    ref = exact(albedo, form, EMIT)
    assert ref == [Fr(15, 8), Fr(5, 4), Fr(20)]
    images, _ = train_and_render(scene, 150, 4, random.Random(7), max_records=1000)
    for image in images:
        check(image, ref)
