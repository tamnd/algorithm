# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/connected-component-labeling/. The authors are listed in prov/FCV9GC.jsonl.

import random
from collections import deque

import pytest

from connected_component_labeling import (
    DisjointSet,
    component_sizes,
    count_holes,
    label,
    label_background,
)

EXAMPLE = [
    [1, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 1],
]

DIAMOND = [
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0],
]


def neighbors(connectivity):
    if connectivity == 4:
        return [(1, 0), (-1, 0), (0, 1), (0, -1)]
    return [(dx, dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if dx or dy]


def bfs_label(img, connectivity):
    """Reference: breadth first flood fill from each unlabeled pixel in raster order."""
    h = len(img)
    w = len(img[0]) if h else 0
    lab = [[0] * w for _ in range(h)]
    k = 0
    for y in range(h):
        for x in range(w):
            if img[y][x] and not lab[y][x]:
                k += 1
                lab[y][x] = k
                q = deque([(x, y)])
                while q:
                    cx, cy = q.popleft()
                    for dx, dy in neighbors(connectivity):
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < w and 0 <= ny < h and img[ny][nx] and not lab[ny][nx]:
                            lab[ny][nx] = k
                            q.append((nx, ny))
    return lab, k


def random_image(rng, h, w, density):
    return [[1 if rng.random() < density else 0 for _ in range(w)] for _ in range(h)]


def test_example():
    lab4, k4 = label(EXAMPLE, 4)
    lab8, k8 = label(EXAMPLE, 8)
    assert k4 == 2 and k8 == 1
    top = [[1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 0], [1, 1, 1, 1, 1, 0]]
    assert lab4 == top + [[0, 0, 0, 0, 0, 2]]
    assert lab8 == top + [[0, 0, 0, 0, 0, 1]]
    assert component_sizes(lab4, k4) == [0, 11, 1]
    assert component_sizes(lab8, k8) == [0, 12]


@pytest.mark.parametrize("connectivity", [4, 8])
def test_against_bfs(connectivity):
    rng = random.Random(1966 + connectivity)
    for _ in range(600):
        h = rng.randrange(0, 9)
        w = rng.randrange(1, 9)
        img = random_image(rng, h, w, rng.choice([0.2, 0.45, 0.6, 0.8]))
        assert label(img, connectivity) == bfs_label(img, connectivity)


@pytest.mark.parametrize("connectivity", [4, 8])
def test_spirals_and_u_shapes(connectivity):
    # A U shape and a staircase force merges of labels made far apart.
    u = [[1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1], [1, 1, 1, 1, 1]]
    stairs = [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 1]]
    w_shape = [[1, 0, 1, 0, 1, 0, 1], [1, 1, 1, 1, 1, 1, 1]]
    for img in (u, stairs, w_shape):
        assert label(img, connectivity) == bfs_label(img, connectivity)


def test_diagonal_ring_and_jordan_property():
    # 4-connected foreground: four separate pixels, yet the center is cut off.
    assert label(DIAMOND, 4)[1] == 4
    assert count_holes(DIAMOND, 4) == 1
    # 8 with 8: one closed ring, yet the center leaks out through the corners.
    assert label(DIAMOND, 8)[1] == 1
    assert count_holes(DIAMOND, 8) == 0
    # The consistent pairs: (8, 4) gives one ring and one hole; (4, 8) gives
    # four pixels and no hole.
    assert (label(DIAMOND, 8)[1], count_holes(DIAMOND, 4)) == (1, 1)
    assert (label(DIAMOND, 4)[1], count_holes(DIAMOND, 8)) == (4, 0)


def euler_from_quads(img, connectivity):
    """Euler number from counts of 2 by 2 patterns of the zero padded image."""
    h = len(img)
    w = len(img[0]) if h else 0
    pad = [[0] * (w + 2)] + [[0] + [1 if v else 0 for v in row] + [0] for row in img] + [[0] * (w + 2)]
    q1 = q3 = qd = 0
    for y in range(h + 1):
        for x in range(w + 1):
            a, b = pad[y][x], pad[y][x + 1]
            c, d = pad[y + 1][x], pad[y + 1][x + 1]
            s = a + b + c + d
            if s == 1:
                q1 += 1
            elif s == 3:
                q3 += 1
            elif s == 2 and a == d:
                qd += 1
    if connectivity == 4:
        num = q1 - q3 + 2 * qd
    else:
        num = q1 - q3 - 2 * qd
    assert num % 4 == 0
    return num // 4


def test_objects_minus_holes_is_euler_number_for_dual_pairs():
    rng = random.Random(1970)
    for _ in range(400):
        img = random_image(rng, rng.randrange(1, 8), rng.randrange(1, 8), rng.choice([0.3, 0.5, 0.7]))
        assert label(img, 8)[1] - count_holes(img, 4) == euler_from_quads(img, 8)
        assert label(img, 4)[1] - count_holes(img, 8) == euler_from_quads(img, 4)


def test_background_labels_partition_the_zeros():
    rng = random.Random(3)
    for _ in range(100):
        img = random_image(rng, 6, 7, 0.5)
        lab, k = label_background(img, 4)
        inv = [[0 if v else 1 for v in row] for row in img]
        assert (lab, k) == bfs_label(inv, 4)


def test_disjoint_set():
    ds = DisjointSet()
    xs = [ds.make_set() for _ in range(10)]
    for a, b in [(1, 2), (3, 4), (2, 4), (7, 8)]:
        ds.union(xs[a], xs[b])
    roots = {ds.find(x) for x in xs}
    assert len(roots) == 6
    assert ds.find(xs[1]) == ds.find(xs[3])


def test_bad_connectivity():
    with pytest.raises(ValueError):
        label([[1]], 6)
