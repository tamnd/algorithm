# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selective-search/. The authors are listed in prov/RBM5RD.jsonl.

import random
from fractions import Fraction

from selective_search import (
    BINS,
    equal_value_regions,
    hierarchy_ranks,
    initial_regions,
    rank_proposals,
    selective_search,
    selective_search_scan,
    similarity,
)

IMG = [[200, 205, 210, 205, 210, 215],
       [200, 205, 210, 205, 210, 215],
       [20, 30, 100, 105, 30, 40],
       [20, 30, 100, 110, 30, 40]]
LAB = [[0, 0, 0, 1, 1, 1],
       [0, 0, 0, 1, 1, 1],
       [2, 2, 3, 3, 4, 4],
       [2, 2, 3, 3, 4, 4]]


def random_case(rng, h, w, levels, colour=False):
    coarse = [[rng.randrange(levels) for _ in range(w)] for _ in range(h)]
    labels = equal_value_regions(coarse)
    if colour:
        img = [[tuple(rng.randrange(256) for _ in range(3)) for _ in range(w)] for _ in range(h)]
    else:
        img = [[rng.randrange(256) for _ in range(w)] for _ in range(h)]
    return img, labels


def components(labels):
    """The number of connected parts of the region adjacency graph."""
    h, w = len(labels), len(labels[0])
    parent = {}

    def find(x):
        while parent.setdefault(x, x) != x:
            x = parent[x]
        return x

    for r in range(h):
        for c in range(w):
            find(labels[r][c])
            for rr, cc in ((r + 1, c), (r, c + 1)):
                if rr < h and cc < w:
                    a, b = find(labels[r][c]), find(labels[rr][cc])
                    if a != b:
                        parent[a] = b
    return len({find(x) for x in parent})


def test_page_example():
    r = initial_regions(IMG, LAB)
    assert r[0].hist[19] == Fraction(1, 3) and r[0].hist[20] == Fraction(2, 3)
    assert similarity(r[0], r[1], 24, (1, 0, 0)) == Fraction(2, 3)
    assert similarity(r[0], r[1], 24, (1, 1, 1)) == Fraction(13, 6)
    assert similarity(r[2], r[3], 24, (1, 1, 1)) == Fraction(5, 3)
    boxes, merges = selective_search(IMG, LAB)
    assert merges == [(0, 1, 5), (2, 3, 6), (4, 6, 7), (5, 7, 8)]
    assert boxes[5:] == [(0, 0, 6, 2), (0, 2, 4, 4), (0, 2, 6, 4), (0, 0, 6, 4)]
    # Size alone merges the small regions first.
    assert selective_search(IMG, LAB, (0, 1, 0))[1] == [(2, 3, 5), (1, 4, 6), (0, 5, 7), (6, 7, 8)]


def test_equal_value_regions():
    assert equal_value_regions([[1, 1, 2], [3, 1, 2]]) == [[0, 0, 1], [2, 0, 1]]


def test_heap_matches_full_scan():
    rng = random.Random(1)
    for k in range(16):
        img, labels = random_case(rng, rng.randint(2, 7), rng.randint(2, 7), 3, colour=k % 8 == 0)
        for weights in [(1, 1, 1), (1, 0, 0), (0, 0, 1)]:
            assert selective_search(img, labels, weights) == selective_search_scan(img, labels, weights)


def test_hierarchy_shape_and_boxes():
    rng = random.Random(2)
    for _ in range(25):
        img, labels = random_case(rng, rng.randint(2, 8), rng.randint(2, 8), 3)
        n = 1 + max(max(row) for row in labels)
        boxes, merges = selective_search(img, labels)
        assert len(merges) == n - components(labels)
        assert len(boxes) == n + len(merges)
        members = {k: {k} for k in range(n)}
        for i, j, t in merges:
            assert i in members and j in members
            members[t] = members.pop(i) | members.pop(j)
            cells = [(r, c) for r in range(len(labels)) for c in range(len(labels[0])) if labels[r][c] in members[t]]
            box = (min(c for _, c in cells), min(r for r, _ in cells),
                   max(c for _, c in cells) + 1, max(r for r, _ in cells) + 1)
            assert boxes[t] == box


def test_propagated_histogram_is_exact():
    rng = random.Random(3)
    for _ in range(20):
        img, labels = random_case(rng, 6, 7, 3)
        regions = initial_regions(img, labels)
        im = 42
        ids = sorted(regions)
        a, b = ids[0], next(iter(regions[ids[0]].nbrs))
        from selective_search import merge
        rt = merge(regions[a], regions[b], a, b)
        counts = [0] * BINS
        size = 0
        for r in range(6):
            for c in range(7):
                if labels[r][c] in (a, b):
                    counts[img[r][c] * BINS // 256] += 1
                    size += 1
        assert rt.hist == [Fraction(k, size) for k in counts]
        assert sum(rt.hist) == 1
        assert 0 <= similarity(regions[a], regions[b], im, (1, 0, 0)) <= 1


def test_similarity_ranges():
    rng = random.Random(4)
    for _ in range(10):
        img, labels = random_case(rng, 6, 6, 3, colour=True)
        regions = initial_regions(img, labels)
        for i in regions:
            for j in regions[i].nbrs:
                for weights in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
                    s = similarity(regions[i], regions[j], 36, weights)
                    assert 0 <= s <= 1


def test_ranking_combines_and_dedups():
    boxes, merges = selective_search(IMG, LAB)
    ranked = hierarchy_ranks(boxes, merges, 5)
    assert ranked[0] == (1, (0, 0, 6, 4))
    other = hierarchy_ranks(*selective_search(IMG, LAB, (0, 1, 0)), 5)
    out = rank_proposals([ranked, other], random.Random(5))
    all_boxes = {b for _, b in ranked} | {b for _, b in other}
    assert len(out) == len(all_boxes) and set(out) == all_boxes
    assert out == rank_proposals([ranked, other], random.Random(5))
