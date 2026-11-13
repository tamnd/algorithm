# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/octree-color-quantization/. The authors are listed in prov/XZM37W.jsonl.

import random
from collections import Counter
from fractions import Fraction as F

from octree_color_quantization import OctreeQuantizer, octree_quantize, squared_distance, total_error


def partitions(items, k):
    """All partitions of the list items into at most k nonempty groups."""
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for p in partitions(rest, k):
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1 :]
        if len(p) < k:
            yield [[first]] + p


def best_error(colors, k):
    """The least total squared error of any palette of at most k colors, by trying every partition."""
    count = Counter(colors)
    best = None
    for p in partitions(list(count), k):
        e = 0
        for group in p:
            pixels = [c for c in group for _ in range(count[c])]
            m = [F(sum(c[a] for c in pixels), len(pixels)) for a in range(3)]
            e += sum(squared_distance(c, m) for c in pixels)
        best = e if best is None else min(best, e)
    return best


def random_image(rng, n, top):
    return [tuple(rng.randrange(top) for _ in range(3)) for _ in range(n)]


def count_nodes(node):
    return 1 + sum(count_nodes(c) for c in node.children if c is not None)


def test_counts_and_sums_are_kept_and_the_tree_stays_small() -> None:
    rng = random.Random(8)
    for _ in range(20):
        k = rng.randrange(1, 30)
        tree = OctreeQuantizer(k)
        colors = random_image(rng, 400, 256)
        for c in colors:
            tree.insert(c)
            assert tree.leaves <= k
            assert count_nodes(tree.root) <= k * (tree.depth + 1)
        leaves = tree.leaf_nodes()
        assert len(leaves) == tree.leaves
        assert sum(n.count for n in leaves) == len(colors)
        for a in range(3):
            assert sum(n.sums[a] for n in leaves) == sum(c[a] for c in colors)


def test_palette_has_at_most_k_colors_and_can_have_fewer() -> None:
    rng = random.Random(8)
    for _ in range(100):
        colors = random_image(rng, rng.randrange(1, 80), rng.choice([4, 32, 256]))
        k = rng.randrange(1, 20)
        pal, index, _ = octree_quantize(colors, k)
        assert 1 <= len(pal) <= k
        assert len(index) == len(colors)
    # three colors that differ in the top bit, k = 2: the root merges all three
    pal, index, tree = octree_quantize([(0, 0, 0), (255, 0, 0), (0, 255, 0)], 2)
    assert pal == [(85, 85, 0)] and index == [0, 0, 0]
    assert tree.merges == 22
    # 5000 random colors and k = 16 give 15 palette colors
    pal, _, _ = octree_quantize(random_image(random.Random(8), 5000, 256), 16)
    assert len(pal) == 15


def test_few_colors_are_kept_exactly() -> None:
    rng = random.Random(8)
    for _ in range(50):
        distinct = list({tuple(rng.randrange(256) for _ in range(3)) for _ in range(rng.randrange(1, 12))})
        colors = [rng.choice(distinct) for _ in range(60)]
        pal, index, _ = octree_quantize(colors, 12)
        assert sorted(pal) == sorted(distinct)
        assert total_error(colors, pal, index) == 0


def test_each_pixel_maps_to_the_mean_of_its_own_cell() -> None:
    rng = random.Random(8)
    colors = random_image(rng, 2000, 256)
    pal, index, tree = octree_quantize(colors, 20)
    for c, j in zip(colors, index):
        node = tree.root
        while not node.leaf:
            node = node.children[(((c[0] >> (7 - node.level)) & 1) << 2) | (((c[1] >> (7 - node.level)) & 1) << 1) | ((c[2] >> (7 - node.level)) & 1)]
        shift = tree.depth - node.level
        for a in range(3):
            # the mean lies in the same cube of side 2^shift as the pixel
            assert pal[j][a] // 2**shift == c[a] >> shift


def test_against_the_exhaustive_best_palette() -> None:
    colors = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (100, 0, 0)]
    pal, index, _ = octree_quantize(colors, 2)
    assert total_error(colors, pal, index) == best_error(colors, 2) == 5
    three = [(0, 0, 0), (255, 0, 0), (0, 255, 0)]
    pal, index, _ = octree_quantize(three, 2)
    assert total_error(three, pal, index) == 86700 and best_error(three, 2) == F(65025, 2)
    # 127 and 128 are neighbors but differ in the top binary digit, so the root keeps them apart
    split = [(0, 0, 0), (127, 0, 0), (128, 0, 0)]
    pal, index, _ = octree_quantize(split, 2)
    assert pal == [(F(127, 2), 0, 0), (128, 0, 0)]
    assert total_error(split, pal, index) == F(16129, 2) and best_error(split, 2) == F(1, 2)
    rng = random.Random(8)
    worse = 0
    for _ in range(200):
        colors = random_image(rng, rng.randrange(3, 9), 16)
        k = rng.randrange(2, 4)
        pal, index, _ = octree_quantize(colors, k)
        e, b = total_error(colors, pal, index), best_error(colors, k)
        assert e >= b
        worse += e > b
    assert worse == 166
