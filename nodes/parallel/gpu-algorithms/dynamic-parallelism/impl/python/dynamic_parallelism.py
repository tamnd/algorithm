# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-parallelism/. The authors are listed in prov/271465.jsonl.
"""Models of programs that use CUDA dynamic parallelism.

Each function runs sequentially in Python and records the child launches that
the CUDA version would make: the number of launches, the depth of nesting and
the launches per level.  No CUDA code is run.
"""
from collections import Counter


class Stats:
    def __init__(self):
        self.launches = 0                # device-side child launches
        self.per_level = Counter()       # launches made at each nesting level (the host launch is level 0)
        self.max_depth = 0
        self.evaluations = 0             # pixel evaluations (adaptive grid)

    def launch(self, depth):
        self.launches += 1
        self.per_level[depth] += 1
        self.max_depth = max(self.max_depth, depth)


def cdp_quicksort(a, rng, cutoff=32, pivot_rule="random"):
    """Quicksort in which each partition step launches one child grid per side.

    A side with at most `cutoff` items is sorted inside the current grid,
    as the CUDA samples do with a simple sort at the bottom of the recursion.
    pivot_rule is "random" (uses rng) or "first".
    """
    a = list(a)
    st = Stats()

    def grid(lo, hi, depth):                           # one grid works on a[lo:hi]
        if hi - lo <= cutoff:
            a[lo:hi] = sorted(a[lo:hi])
            return
        pivot = a[rng.randrange(lo, hi)] if pivot_rule == "random" else a[lo]
        left = [v for v in a[lo:hi] if v < pivot]
        mid = [v for v in a[lo:hi] if v == pivot]
        right = [v for v in a[lo:hi] if v > pivot]
        a[lo:hi] = left + mid + right
        m1, m2 = lo + len(left), lo + len(left) + len(mid)
        for l2, h2 in ((lo, m1), (m2, hi)):
            if h2 - l2 > 1:
                st.launch(depth + 1)                    # child<<<...>>>(a, l2, h2)
                grid(l2, h2, depth + 1)

    grid(0, len(a), 0)
    return a, st


def adaptive_fill(f, size, min_size, max_depth, split=2):
    """Mariani-Silver style refinement of a size x size image of values f(x, y).

    A region whose border has one value is filled with it.  Otherwise, if it is
    large enough and not too deep, it is split into split x split children, each
    a child launch.  Else every pixel is evaluated.  Exact for any f that is
    monotone in x and in y, because then the extreme values lie on the border.
    """
    img = [[None] * size for _ in range(size)]
    st = Stats()

    def ev(x, y):
        st.evaluations += 1
        return f(x, y)

    def region(x0, y0, s, depth):
        border = set()
        cells = {(x0 + i, y0) for i in range(s)} | {(x0 + i, y0 + s - 1) for i in range(s)}
        cells |= {(x0, y0 + i) for i in range(s)} | {(x0 + s - 1, y0 + i) for i in range(s)}
        for (x, y) in sorted(cells):                   # each border pixel once
            v = ev(x, y)
            img[y][x] = v
            border.add(v)
        if len(border) == 1:
            v = border.pop()
            for y in range(y0, y0 + s):
                for x in range(x0, x0 + s):
                    img[y][x] = v
            return
        if depth < max_depth and s // split >= min_size:
            c = s // split
            for j in range(split):
                for i in range(split):
                    st.launch(depth + 1)
                    region(x0 + i * c, y0 + j * c, c, depth + 1)
            return
        for y in range(y0 + 1, y0 + s - 1):
            for x in range(x0 + 1, x0 + s - 1):
                img[y][x] = ev(x, y)

    region(0, 0, size, 0)
    return img, st


def launch_cost(launches, per_launch):
    """A first model: each device launch adds a fixed cost; the cost depends on the GPU."""
    return launches * per_launch
