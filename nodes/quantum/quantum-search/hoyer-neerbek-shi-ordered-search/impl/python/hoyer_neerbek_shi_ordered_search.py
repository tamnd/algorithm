# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hoyer-neerbek-shi-ordered-search/. The authors are listed in prov/M3Z7WG.jsonl.
"""The exact quantum ordered search algorithm of Høyer, Neerbek and Shi (2001).

Input: a monotone bit string x_0 <= x_1 <= ... <= x_{m-1} with x_{m-1} = 1, given by an
oracle. Output: f(x), the smallest index i with x_i = 1. The algorithm is exact: the final
state of the leaf register is the basis state |f(x)>.

The simulation keeps the exact amplitudes of the vertex and color registers. A layout
cuts the m positions (padded to an even number with x_i = 1) into blocks. A block of
height h is a complete binary tree with 2**h leaves. With 2**s colors, its root and its
depth 1 vertices carry p = 2**(s+1-h) pebbles each, and a vertex at depth j >= 2 carries
2**(j-1) * p pebbles. All vertices at one depth of one block carry the same set of
colors. The pebbles meet the conditions of HNS: on each root-to-leaf path every color
occurs once, and a vertex carries at least as many pebbles as all its ancestors together.
"""

import math
from functools import lru_cache

from qsim import TOL

Layout = tuple  # (s, blocks, colors); see layout()


def layout(m: int, s: int):
    """Blocks and color sets for m positions and 2**s colors.

    blocks: list of (start, h). colors[b][j]: the colors on depth j of block b.
    Returns (blocks, colors, load) where load[c] = number of vertices with color c.
    """
    big = m + (m & 1)
    full = 1 << (s + 1)
    heights = [s + 1] * (big // full)
    rest = big % full
    for h in range(s, 0, -1):
        if rest >> h & 1:
            heights.append(h)
    blocks, colors = [], []
    load = [0] * (1 << s)
    start = 0
    for h in heights:
        p = 1 << (s + 1 - h)
        sizes = [p] + [p << (j - 1) for j in range(1, h)]
        order = sorted(range(1 << s), key=lambda c: (load[c], c))
        sets = [None] * h
        pos = 0
        for j in range(h - 1, -1, -1):  # least loaded colors go to the deepest level
            sets[j] = order[pos:pos + sizes[j]]
            pos += sizes[j]
            for c in sets[j]:
                load[c] += 1 << j
        blocks.append((start, h))
        colors.append(sets)
        start += 1 << h
    return blocks, colors, load


MAX_S = 4  # at most 2**4 = 16 colors; the load ratio is 1/3 + 1/(6 * 4**s) per level


@lru_cache(maxsize=None)
def plan(m: int) -> tuple[int, int]:
    """(queries, s): the exact query count of this implementation and the best s."""
    if m == 1:
        return 0, -1
    best = None
    s = 0
    while s <= MAX_S and (1 << (s + 1)) <= m + (m & 1):
        sub = max(layout(m, s)[2])
        cost = 1 + plan(sub)[0]
        if best is None or cost < best[0]:
            best = (cost, s)
        s += 1
    return best


def queries(m: int) -> int:
    return plan(m)[0]


class Oracle:
    """Bit oracle for a monotone string; positions past the end read as 1."""

    def __init__(self, x: list[int]):
        if any(a > b for a, b in zip(x, x[1:])) or x[-1] != 1:
            raise ValueError("x must be monotone with last bit 1")
        self.x = x

    def bit(self, i: int) -> int:
        return 1 if i >= len(self.x) else self.x[i]


def _rightmost_leaf(start: int, h: int, j: int, k: int) -> int:
    return start + (k + 1) * (1 << (h - j)) - 1


def run(m: int, bit) -> tuple[list[float], int]:
    """Run HNS on m positions; bit(i) reads x_i (x_i = 1 for i >= m - 1).

    Returns (amplitudes of the leaf register on positions 0..m-1, queries used).
    """
    if m == 1:  # @line L1
        return [1.0], 0
    s = plan(m)[1]  # @line L2
    blocks, colors, load = layout(m, s)
    nc = 1 << s  # @line L3 (the color register holds 2**s colors)
    # vertex list per color, left to right: (block, depth, index)
    vc = [[] for _ in range(nc)]
    for b, (start, h) in enumerate(blocks):
        for j in range(h):
            for c in colors[b][j]:
                vc[c].extend((b, j, k) for k in range(1 << j))
    # step 2: one ordered search of size |V_c| per color, run in parallel
    joint = {}
    used = 0
    for c in range(nc):  # @line L4
        verts = vc[c]

        def ybit(i, verts=verts):
            if i >= len(verts):  # padding position of the subproblem
                return 1
            b, j, k = verts[i]
            start, h = blocks[b]
            return bit(_rightmost_leaf(start, h, j, k))

        amp, q = run(len(verts), ybit)  # @line L5
        used = max(used, q)
        for i, a in enumerate(amp):
            if a != 0:
                joint[(verts[i], c)] = joint.get((verts[i], c), 0.0) + a / math.sqrt(nc)  # @line L6
    # step 3: undo the coloring U1, |v>|c> -> |v>|0> on the span of its image
    vert = {}
    for (v, c), a in joint.items():
        b, j, _ = v
        p = len(colors[b][j])
        vert[v] = vert.get(v, 0.0) + a / math.sqrt(p)  # @line L7
    # step 4: one query O'_x, then U2 (a Haar wavelet basis on each block)
    used += 1  # @line L8
    big = m + (m & 1)
    leaves = [0.0] * big
    for (b, j, k), a in vert.items():  # @line L9
        start, h = blocks[b]
        lo = start + k * (1 << (h - j))
        half = 1 << (h - j - 1)
        xb = bit(_rightmost_leaf(start, h, j, k) - half)  # rightmost leaf of the left child
        w = a * 2 ** (-(h - j - 1) / 2)
        if j == 0:  # parent not pebbled: bit query, then Phi_right or Phi_left
            rng = range(lo, lo + half) if xb else range(lo + half, lo + 2 * half)
            for leaf in rng:
                leaves[leaf] += w
        else:  # phase query, then (Phi_right - Phi_left)/sqrt(2)
            sign = -1.0 if xb else 1.0
            for leaf in range(lo, lo + half):
                leaves[leaf] -= sign * w / math.sqrt(2)
            for leaf in range(lo + half, lo + 2 * half):
                leaves[leaf] += sign * w / math.sqrt(2)
    if any(abs(a) > TOL for a in leaves[m:]):
        raise AssertionError("amplitude on a padding leaf")
    return leaves[:m], used


def ordered_search(x: list[int]) -> tuple[int, int, list[float]]:
    """Return (f(x), queries, final leaf amplitudes) for a monotone string x."""
    o = Oracle(x)
    amp, q = run(len(x), o.bit)
    best = max(range(len(x)), key=lambda i: abs(amp[i]))  # @line L10
    return best, q, amp


def u2_block(h: int) -> list[list[float]]:
    """The matrix of U2 on one block of height h.

    Columns: (root, bit 0), (root, bit 1), then the other internal vertices in
    breadth-first order. Rows: the 2**h leaves. Phi_u has entry 2**(-d/2) on each leaf
    at distance d below u.
    """
    n = 1 << h
    cols = []
    half = n >> 1
    phi_r = [0.0] * half + [2 ** (-(h - 1) / 2)] * half
    phi_l = [2 ** (-(h - 1) / 2)] * half + [0.0] * half
    cols.append(phi_r)
    cols.append(phi_l)
    for j in range(1, h):
        width = n >> j
        for k in range(1 << j):
            col = [0.0] * n
            lo = k * width
            amp = 2 ** (-(h - j - 1) / 2) / math.sqrt(2)
            for leaf in range(lo, lo + width // 2):
                col[leaf] = -amp
            for leaf in range(lo + width // 2, lo + width):
                col[leaf] = amp
            cols.append(col)
    return [[cols[c][r] for c in range(n)] for r in range(n)]
