# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chamfer-distance/. The authors are listed in prov/HJGGJE.jsonl.

import heapq
import random
from fractions import Fraction

from chamfer_distance import chamfer


def features(image):
    return [(x, y) for y in range(len(image)) for x in range(len(image[0])) if image[y][x]]


def random_image(rng, w, h, p):
    return [[1 if rng.random() < p else 0 for _ in range(w)] for _ in range(h)]


def closed_form(image, a, b):
    """For each pixel, the minimum over the features of a (M - m) + b m."""
    h, w = len(image), len(image[0])
    feats = features(image)
    if not feats:
        return [[None] * w for _ in range(h)]
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            best = None
            for (u, v) in feats:
                big, small = max(abs(x - u), abs(y - v)), min(abs(x - u), abs(y - v))
                c = a * (big - small) + b * small
                best = c if best is None else min(best, c)
            row.append(best)
        out.append(row)
    return out


def dijkstra(image, a, b):
    """Shortest paths from all features in the 8-neighbor grid graph inside the image."""
    h, w = len(image), len(image[0])
    dist = [[None] * w for _ in range(h)]
    heap = [(0, x, y) for (x, y) in features(image)]
    heapq.heapify(heap)
    while heap:
        d, x, y = heapq.heappop(heap)
        if dist[y][x] is not None:
            continue
        dist[y][x] = d
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                u, v = x + dx, y + dy
                if 0 <= u < w and 0 <= v < h and dist[v][u] is None:
                    heapq.heappush(heap, (d + (b if dx and dy else a), u, v))
    return dist


def exact_squared(image):
    """All pairs: the exact squared Euclidean distance to the nearest feature."""
    h, w = len(image), len(image[0])
    feats = features(image)
    return [[min((x - u) ** 2 + (y - v) ** 2 for (u, v) in feats) for x in range(w)]
            for y in range(h)]


def test_example():
    image = [[0] * 7 for _ in range(5)]
    image[1][1] = 1
    image[3][5] = 1
    assert chamfer(image) == [
        [4, 3, 4, 7, 10, 9, 10],
        [3, 0, 3, 6, 7, 6, 7],
        [4, 3, 4, 7, 4, 3, 4],
        [7, 6, 7, 6, 3, 0, 3],
        [10, 9, 10, 7, 4, 3, 4],
    ]


def test_edges():
    assert chamfer([]) == []
    assert chamfer([[0, 0], [0, 0]]) == [[None, None], [None, None]]
    assert chamfer([[1]]) == [[0]]
    assert chamfer([[1, 0, 0, 0]]) == [[0, 3, 6, 9]]
    assert chamfer([[0], [0], [1]]) == [[6], [3], [0]]


def test_equals_closed_form():
    rng = random.Random(6801)
    for _ in range(400):
        a = rng.randint(1, 6)
        b = rng.randint(a, 2 * a)
        w, h = rng.randint(1, 9), rng.randint(1, 9)
        image = random_image(rng, w, h, rng.choice([0.03, 0.1, 0.3]))
        assert chamfer(image, a, b) == closed_form(image, a, b)


def test_equals_shortest_paths():
    rng = random.Random(6802)
    for _ in range(400):
        a = rng.randint(1, 6)
        b = rng.randint(a, 2 * a)
        w, h = rng.randint(1, 9), rng.randint(1, 9)
        image = random_image(rng, w, h, rng.choice([0.03, 0.1, 0.3]))
        assert chamfer(image, a, b) == dijkstra(image, a, b)


def test_city_block_and_chessboard():
    rng = random.Random(6803)
    for _ in range(200):
        w, h = rng.randint(1, 8), rng.randint(1, 8)
        image = random_image(rng, w, h, 0.15)
        feats = features(image)
        if not feats:
            continue
        l1 = [[min(abs(x - u) + abs(y - v) for (u, v) in feats) for x in range(w)] for y in range(h)]
        linf = [[min(max(abs(x - u), abs(y - v)) for (u, v) in feats) for x in range(w)]
                for y in range(h)]
        assert chamfer(image, 1, 2) == l1
        assert chamfer(image, 1, 1) == linf


def test_three_four_error_bound():
    # 8 E <= c^2 <= 10 E, so c / 3 lies between (2 sqrt 2 / 3) e and (sqrt 10 / 3) e.
    rng = random.Random(6804)
    lo, hi = Fraction(10), Fraction(0)
    for _ in range(300):
        w, h = rng.randint(1, 10), rng.randint(1, 10)
        image = random_image(rng, w, h, rng.choice([0.02, 0.1]))
        if not features(image):
            continue
        c = chamfer(image)
        e = exact_squared(image)
        for y in range(h):
            for x in range(w):
                if e[y][x] == 0:
                    assert c[y][x] == 0
                    continue
                assert 8 * e[y][x] <= c[y][x] ** 2 <= 10 * e[y][x]
                r = Fraction(c[y][x] ** 2, 9 * e[y][x])
                lo, hi = min(lo, r), max(hi, r)
    assert lo == Fraction(8, 9)
    assert hi == Fraction(10, 9)


def test_three_four_extremes():
    image = [[0] * 4 for _ in range(2)]
    image[0][0] = 1
    c = chamfer(image)
    assert c[1][1] == 4 and c[1][1] ** 2 == 8 * 2  # the diagonal: 4 / 3 against sqrt 2
    assert c[1][3] == 10 and c[1][3] ** 2 == 10 * 10  # the knight-like (3, 1): 10 / 3 against sqrt 10
    assert c[0][3] == 9  # along an axis the scaled result is exact


def test_measured_error_on_one_feature():
    # One feature in the corner of a 40 by 40 grid: the largest relative errors of c / 3.
    n = 40
    image = [[0] * n for _ in range(n)]
    image[0][0] = 1
    c = chamfer(image)
    ratios = [Fraction(c[y][x] ** 2, 9 * (x * x + y * y)) for y in range(n) for x in range(n) if x or y]
    assert min(ratios) == Fraction(8, 9)
    assert max(ratios) == Fraction(10, 9)
