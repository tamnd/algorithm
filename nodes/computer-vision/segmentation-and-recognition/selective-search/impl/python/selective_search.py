# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selective-search/. The authors are listed in prov/RBM5RD.jsonl.
"""Selective search: hierarchical grouping of an over-segmentation into box proposals.

The input is an image (a list of rows; a pixel is an int in 0..255 or a tuple
of such ints, one per channel) and an initial label map of the same size,
where each label is one region. The paper starts from the segmentation of
Felzenszwalb and Huttenlocher; this file only has equal_value_regions, the
4-connected components of equal pixels, as a simple stand-in. Regions are
neighbors when two of their pixels are 4-connected.

The similarity is a_c s_colour + a_s s_size + a_f s_fill with the colour
histograms of the paper (25 bins per channel, L1 normalized, histogram
intersection). The texture similarity of the paper (Gaussian derivatives in
8 orientations) is left out. All similarities are exact Fractions, so ties
are exact and broken by the smaller pair of region ids. A box is
(x1, y1, x2, y2) with x2 = last column + 1. Standard library only.
"""

import heapq
from collections import deque
from fractions import Fraction

BINS = 25


def channels(pixel):
    return pixel if isinstance(pixel, tuple) else (pixel,)


def equal_value_regions(image):
    """Label map of the 4-connected components of equal pixel values, labels 0, 1, ..."""
    h, w = len(image), len(image[0])
    labels = [[-1] * w for _ in range(h)]
    nxt = 0
    for r in range(h):
        for c in range(w):
            if labels[r][c] >= 0:
                continue
            labels[r][c] = nxt
            queue = deque([(r, c)])
            while queue:
                y, x = queue.popleft()
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < h and 0 <= xx < w and labels[yy][xx] < 0 and image[yy][xx] == image[y][x]:
                        labels[yy][xx] = nxt
                        queue.append((yy, xx))
            nxt += 1
    return labels


class Region:
    __slots__ = ("size", "box", "hist", "nbrs")

    def __init__(self, size, box, hist, nbrs):
        self.size, self.box, self.hist, self.nbrs = size, box, hist, nbrs


def initial_regions(image, labels):
    """Size, box, normalized colour histogram, neighbors and member set of each initial region."""
    h, w = len(image), len(image[0])
    nch = len(channels(image[0][0]))
    counts, boxes, sizes, nbrs = {}, {}, {}, {}
    for r in range(h):
        for c in range(w):
            k = labels[r][c]
            if k not in sizes:
                sizes[k], boxes[k], counts[k], nbrs[k] = 0, [c, r, c + 1, r + 1], [0] * (BINS * nch), set()
    for r in range(h):
        for c in range(w):
            k = labels[r][c]
            sizes[k] += 1
            b = boxes[k]
            b[0], b[1], b[2], b[3] = min(b[0], c), min(b[1], r), max(b[2], c + 1), max(b[3], r + 1)
            for ch, v in enumerate(channels(image[r][c])):
                counts[k][ch * BINS + v * BINS // 256] += 1
            for rr, cc in ((r + 1, c), (r, c + 1)):
                if rr < h and cc < w and labels[rr][cc] != k:
                    nbrs[k].add(labels[rr][cc])
                    nbrs[labels[rr][cc]].add(k)
    regions = {}
    for k in sizes:
        total = sizes[k] * nch
        regions[k] = Region(sizes[k], tuple(boxes[k]), [Fraction(n, total) for n in counts[k]],
                            set(nbrs[k]))
    return regions


def box_union(a, b):
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


def box_area(b):
    return (b[2] - b[0]) * (b[3] - b[1])


def similarity(ri, rj, im_size, weights):
    """a_c s_colour + a_s s_size + a_f s_fill of two regions (weights in {0, 1} in the paper)."""
    ac, a_s, af = weights
    s = Fraction(0)
    if ac:
        s += ac * sum(min(p, q) for p, q in zip(ri.hist, rj.hist))
    if a_s:
        s += a_s * (1 - Fraction(ri.size + rj.size, im_size))
    if af:
        s += af * (1 - Fraction(box_area(box_union(ri.box, rj.box)) - ri.size - rj.size, im_size))
    return s


def merge(ri, rj, i, j):
    """The union region; the histogram is the size-weighted mean of the two."""
    size = ri.size + rj.size
    hist = [(ri.size * p + rj.size * q) / size for p, q in zip(ri.hist, rj.hist)]
    return Region(size, box_union(ri.box, rj.box), hist, (ri.nbrs | rj.nbrs) - {i, j})


def selective_search(image, labels, weights=(1, 1, 1)):
    """One grouping strategy. Returns (boxes, merges): the boxes of all regions in creation order
    (initial regions by label, then each merged region) and the list of merged pairs (i, j, t)."""
    im_size = len(image) * len(image[0])
    regions = initial_regions(image, labels)  # @line L1
    heap = []
    for i in regions:  # @line L2
        for j in regions[i].nbrs:
            if i < j:
                heapq.heappush(heap, (-similarity(regions[i], regions[j], im_size, weights), i, j))
    boxes = [regions[k].box for k in sorted(regions)]  # @line L3
    alive = set(regions)
    merges = []
    nxt = max(regions) + 1
    while heap:  # @line L4
        neg_s, i, j = heapq.heappop(heap)  # @line L5
        if i not in alive or j not in alive:
            continue  # a stale pair: lazy deletion stands for line L7
        t = nxt
        nxt += 1
        rt = merge(regions[i], regions[j], i, j)  # @line L6
        alive -= {i, j}  # @line L7
        for k in rt.nbrs:
            regions[k].nbrs -= {i, j}
            regions[k].nbrs.add(t)
            heapq.heappush(heap, (-similarity(regions[k], rt, im_size, weights), k, t))  # @line L8
        regions[t] = rt  # @line L9
        alive.add(t)
        boxes.append(rt.box)
        merges.append((i, j, t))
    return boxes, merges  # @line L10


def selective_search_scan(image, labels, weights=(1, 1, 1)):
    """The same grouping with a full scan for the best pair at each step; a slow reference."""
    im_size = len(image) * len(image[0])
    regions = initial_regions(image, labels)
    pairs = {(i, j): similarity(regions[i], regions[j], im_size, weights)
             for i in regions for j in regions[i].nbrs if i < j}
    boxes = [regions[k].box for k in sorted(regions)]
    merges = []
    nxt = max(regions) + 1
    while pairs:
        i, j = min(pairs, key=lambda p: (-pairs[p], p))
        t = nxt
        nxt += 1
        rt = merge(regions[i], regions[j], i, j)
        pairs = {p: v for p, v in pairs.items() if i not in p and j not in p}
        for k in rt.nbrs:
            regions[k].nbrs -= {i, j}
            regions[k].nbrs.add(t)
            pairs[(k, t)] = similarity(regions[k], rt, im_size, weights)
        regions[t] = rt
        boxes.append(rt.box)
        merges.append((i, j, t))
    return boxes, merges


def hierarchy_ranks(boxes, merges, n_initial):
    """Position of each box in its hierarchy: 1 for the last region made, larger lower down.

    The paper gives the region at the top of the hierarchy position 1. Here a
    region made later gets a smaller number; initial regions come last.
    """
    order = list(range(n_initial + len(merges) - 1, -1, -1))
    return [(pos + 1, boxes[k]) for pos, k in enumerate(order)]


def rank_proposals(strategy_outputs, rng):
    """Combine strategies: score = RND * position, sort by score, drop duplicate boxes."""
    scored = []
    for ranked in strategy_outputs:
        for pos, box in ranked:
            scored.append((rng.random() * pos, box))
    scored.sort(key=lambda x: x[0])
    seen, out = set(), []
    for _, box in scored:
        if box not in seen:
            seen.add(box)
            out.append(box)
    return out
