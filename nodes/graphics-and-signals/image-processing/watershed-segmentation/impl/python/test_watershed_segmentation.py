# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/watershed-segmentation/. The authors are listed in prov/P0M4PZ.jsonl.

import random
from collections import deque

import pytest

from watershed_segmentation import WSHED, neighbors, regional_minima, watershed_from_markers, watershed_immersion

# The 3 by 3 example of Roerdink and Meijster (their Fig. 3), 4-connected.
EXAMPLE = [
    [3, 2, 2],
    [3, 1, 1],
    [0, 1, 0],
]


def geodesic_distances(inside, sources, w, h, connectivity):
    """BFS distances inside the set `inside` from the set `sources`."""
    dist = {p: 0 for p in sources}
    q = deque(sources)
    while q:
        x, y = q.popleft()
        for p in neighbors(x, y, w, h, connectivity):
            if p in inside and p not in dist:
                dist[p] = dist[(x, y)] + 1
                q.append(p)
    return dist


def immersion_brute_force(f, connectivity, every_integer_level=True):
    """Definition 3.2 of Roerdink and Meijster, level by level, from scratch.

    The recursion runs over every integer from the minimum to the maximum, as
    the definition says, or only over the gray values that occur in the image
    if every_integer_level is false. The distance to each basin is a separate
    BFS inside the whole threshold set, and pixels reached by no basin must
    form new regional minima.
    """
    h, w = len(f), len(f[0])
    lo = min(min(r) for r in f)
    hi = max(max(r) for r in f)
    basin = {}  # pixel -> label
    count = 0
    values = range(lo, hi + 1) if every_integer_level else sorted({v for r in f for v in r})
    for level in values:
        inside = {(x, y) for y in range(h) for x in range(w) if f[y][x] <= level}
        labels = sorted(set(basin.values()))
        dists = {i: geodesic_distances(inside, [p for p, l in basin.items() if l == i], w, h, connectivity) for i in labels}
        new_basin = {}
        unreached = []
        for p in sorted(inside, key=lambda p: (p[1], p[0])):
            ds = [(dists[i][p], i) for i in labels if p in dists[i]]
            if not ds:
                unreached.append(p)
                continue
            best = min(d for d, _ in ds)
            winners = [i for d, i in ds if d == best]
            if len(winners) == 1:
                new_basin[p] = winners[0]
        for p, l in basin.items():
            assert new_basin.get(p) == l, "a basin pixel must stay in its basin"
        # Connected components of unreached pixels are new regional minima.
        left = set(unreached)
        for p in unreached:
            if p in left:
                count += 1
                comp = geodesic_distances(left, [p], w, h, connectivity)
                for c in comp:
                    assert f[c[1]][c[0]] == level
                    new_basin[c] = count
                    left.discard(c)
        basin = new_basin
    return [[basin.get((x, y), WSHED) for x in range(w)] for y in range(h)]


def canonical(lab):
    """Renumber positive labels by first appearance in raster order."""
    names = {}
    out = []
    for row in lab:
        out.append([v if v <= 0 else names.setdefault(v, len(names) + 1) for v in row])
    return out


def random_image(rng, h, w, top):
    return [[rng.randint(0, top) for _ in range(w)] for _ in range(h)]


def test_example_of_roerdink_and_meijster():
    lab = watershed_immersion(EXAMPLE, 4)
    a, b, W = 1, 2, WSHED
    assert lab == [[b, b, b], [W, b, b], [a, W, b]]
    assert lab == immersion_brute_force(EXAMPLE, 4)
    # Under 8-connectivity the two minima are joined through the centre.
    assert canonical(watershed_immersion(EXAMPLE, 8)) == canonical(immersion_brute_force(EXAMPLE, 8))


@pytest.mark.parametrize("connectivity", [4, 8])
def test_against_brute_force_immersion(connectivity):
    rng = random.Random(1991 + connectivity)
    for _ in range(400):
        h, w = rng.randint(1, 6), rng.randint(1, 6)
        f = random_image(rng, h, w, rng.choice([1, 2, 3, 5, 9]))
        assert canonical(watershed_immersion(f, connectivity)) == canonical(immersion_brute_force(f, connectivity))


@pytest.mark.parametrize("connectivity", [4, 8])
def test_plateaus_and_gaps_in_levels(connectivity):
    rng = random.Random(2000 + connectivity)
    for _ in range(150):
        h, w = rng.randint(2, 7), rng.randint(2, 7)
        # Few distinct values far apart: wide plateaus and empty levels.
        f = [[rng.choice([0, 4, 9]) for _ in range(w)] for _ in range(h)]
        assert canonical(watershed_immersion(f, connectivity)) == canonical(immersion_brute_force(f, connectivity))


@pytest.mark.parametrize("connectivity", [4, 8])
def test_basins_contain_one_minimum_each(connectivity):
    rng = random.Random(41 + connectivity)
    for _ in range(200):
        f = random_image(rng, rng.randint(1, 7), rng.randint(1, 7), 6)
        lab = watershed_immersion(f, connectivity)
        mins = regional_minima(f, connectivity)
        h, w = len(f), len(f[0])
        seen = {}
        for y in range(h):
            for x in range(w):
                if mins[y][x]:
                    assert lab[y][x] > 0
                    seen.setdefault(lab[y][x], set()).add(mins[y][x])
        basins = {v for row in lab for v in row if v > 0}
        assert basins == set(seen)
        assert all(len(s) == 1 for s in seen.values())


def bottleneck(f, sources, w, h, connectivity):
    """The least possible highest value on a path from the sources, for every pixel."""
    best = {}
    heap = [(f[y][x], x, y) for x, y in sources]
    import heapq

    heapq.heapify(heap)
    while heap:
        b, x, y = heapq.heappop(heap)
        if (x, y) in best:
            continue
        best[(x, y)] = b
        for nx, ny in neighbors(x, y, w, h, connectivity):
            if (nx, ny) not in best:
                heapq.heappush(heap, (max(b, f[ny][nx]), nx, ny))
    return best


@pytest.mark.parametrize("connectivity", [4, 8])
def test_markers_flood_by_lowest_pass(connectivity):
    rng = random.Random(1994 + connectivity)
    for _ in range(200):
        h, w = rng.randint(1, 6), rng.randint(1, 7)
        f = random_image(rng, h, w, 9)
        pixels = [(x, y) for y in range(h) for x in range(w)]
        rng.shuffle(pixels)
        k = rng.randint(1, min(4, h * w))
        markers = [[0] * w for _ in range(h)]
        for i, (x, y) in enumerate(pixels[:k]):
            markers[y][x] = i + 1
        lab = watershed_from_markers(f, markers, connectivity)
        b = {i + 1: bottleneck(f, [p], w, h, connectivity) for i, p in enumerate(pixels[:k])}
        for y in range(h):
            for x in range(w):
                l = lab[y][x]
                assert l > 0
                assert b[l][(x, y)] == min(b[i][(x, y)] for i in b)
        # Each label is one connected region around its marker.
        for i, p in enumerate(pixels[:k]):
            inside = {(x, y) for y in range(h) for x in range(w) if lab[y][x] == i + 1}
            assert set(geodesic_distances(inside, [p], w, h, connectivity)) == inside


def test_empty_levels_change_the_literal_recursion():
    # IZ is not idempotent: running it again on the same threshold set with the
    # grown basins can move a tie pixel into a basin. The literal recursion over
    # every integer repeats IZ at the empty levels 3 to 8.
    f = [[0, 1, 0], [2, 2, 9]]
    W = WSHED
    assert watershed_immersion(f, 4) == [[1, W, 2], [1, 1, W]]
    assert immersion_brute_force(f, 4) == [[1, W, 2], [1, 1, W]]
    assert immersion_brute_force(f, 4, every_integer_level=False) == [[1, W, 2], [1, 1, 2]]
    g = [[0, 1, 0], [2, 2, 3]]  # no empty level
    assert watershed_immersion(g, 4) == [[1, W, 2], [1, 1, 2]]


def test_basins_can_touch_without_a_line():
    assert watershed_immersion([[0, 1, 1, 0]], 4) == [[1, 1, 2, 2]]
    assert watershed_immersion([[0, 1, 0]], 4) == [[1, WSHED, 2]]


def test_markers_on_example():
    markers = [[0, 0, 0], [0, 0, 0], [1, 0, 2]]
    # Both markers reach the pixels of value 1 and 2 at the same key; the
    # earlier entry in the queue wins.
    assert watershed_from_markers(EXAMPLE, markers, 4) == [[1, 1, 2], [1, 1, 2], [1, 1, 2]]


def test_bad_connectivity():
    with pytest.raises(ValueError):
        watershed_immersion([[0, 1]], 6)
