# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flute/. The authors are listed in prov/Q78Z3D.jsonl.

from functools import lru_cache
from itertools import permutations
from typing import Sequence

Point = tuple[int, int]
Edge = tuple[int, int]  # indices into the point list
Vec = tuple[int, ...]

TABLE_DEGREE = 4  # FLUTE ships tables up to degree 9; this code builds them up to 4


def pareto(items: dict[Vec, frozenset]) -> dict[Vec, frozenset]:
    """Keep the vectors that no other vector is at most in every coordinate."""
    vecs = sorted(items, key=sum)
    keep: list[Vec] = []
    for a in vecs:
        if not any(all(x <= y for x, y in zip(b, a)) for b in keep):
            keep.append(a)
    return {a: items[a] for a in keep}


@lru_cache(maxsize=None)
def powv_table(pi: tuple[int, ...]) -> tuple[tuple[Vec, frozenset], ...]:
    """Wirelength vectors for the position sequence pi, with Steiner nodes for each.

    Pin i has x rank i and y rank pi[i]. A vector (a_1..a_{d-1}, b_1..b_{d-1})
    stands for the length sum a_i h_i + sum b_j v_j, where h_i and v_j are the
    gaps between consecutive x and y values. For every choice of gaps >= 0, the
    least of these sums is the length of a rectilinear Steiner minimal tree.
    Built by a Dreyfus-Wagner recursion over the d x d grid with vector costs.
    """
    d = len(pi)
    nodes = [(i, j) for i in range(d) for j in range(d)]
    term = [(i, pi[i]) for i in range(d)]

    def box(u: tuple[int, int], v: tuple[int, int]) -> Vec:
        vec = [0] * (2 * (d - 1))
        for k in range(min(u[0], v[0]), max(u[0], v[0])):
            vec[k] = 1
        for k in range(min(u[1], v[1]), max(u[1], v[1])):
            vec[d - 1 + k] = 1
        return tuple(vec)

    def add(a: Vec, b: Vec) -> Vec:
        return tuple(x + y for x, y in zip(a, b))

    full = (1 << d) - 1
    F: dict[tuple[int, tuple[int, int]], dict[Vec, frozenset]] = {}
    for k in range(d):
        for v in nodes:
            F[(1 << k, v)] = {box(term[k], v): frozenset()}
    for mask in sorted(range(1, full + 1), key=lambda m: bin(m).count("1")):
        if bin(mask).count("1") < 2:
            continue
        low = mask & -mask
        G: dict[tuple[int, int], dict[Vec, frozenset]] = {}
        for u in nodes:
            acc: dict[Vec, frozenset] = {}
            sub = (mask - 1) & mask
            while sub:
                if sub & low:
                    for a, sa in F[(sub, u)].items():
                        for b, sb in F[(mask ^ sub, u)].items():
                            c = add(a, b)
                            if c not in acc:
                                acc[c] = sa | sb | {u}
                sub = (sub - 1) & mask
            G[u] = pareto(acc)
        for v in nodes:
            acc = {}
            for u in nodes:
                bu = box(u, v)
                for a, sa in G[u].items():
                    c = add(a, bu)
                    if c not in acc:
                        acc[c] = sa
            F[(mask, v)] = pareto(acc)
    last = d - 1
    ans = F[(full ^ (1 << last), term[last])] if d > 1 else {(): frozenset()}
    tset = set(term)
    return tuple((vec, frozenset(s for s in st if s not in tset)) for vec, st in ans.items())


def all_tables(d: int) -> dict[tuple[int, ...], tuple[tuple[Vec, frozenset], ...]]:
    """The whole lookup table for degree d, one entry per position sequence."""
    return {pi: powv_table(pi) for pi in permutations(range(d))}


def l1(p: Point, q: Point) -> int:
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def mst_edges(pts: Sequence[Point]) -> list[Edge]:
    """Prim's algorithm on the complete L1 graph, O(k^2) for k points."""
    k = len(pts)
    if k == 0:
        return []
    best = [(l1(pts[0], p), 0) for p in pts]
    used = [False] * k
    used[0] = True
    out = []
    for _ in range(k - 1):
        j = min((i for i in range(k) if not used[i]), key=lambda i: best[i][0])
        used[j] = True
        out.append((best[j][1], j))
        for i in range(k):
            if not used[i] and l1(pts[j], pts[i]) < best[i][0]:
                best[i] = (l1(pts[j], pts[i]), j)
    return out


def lookup(pins: Sequence[Point]) -> tuple[int, list[Point]]:
    """Table lookup for a net of degree at most TABLE_DEGREE: (length, Steiner points)."""
    d = len(pins)
    if d <= 1:
        return 0, []
    by_x = sorted(range(d), key=lambda i: (pins[i][0], pins[i][1]))
    by_y = sorted(range(d), key=lambda i: (pins[i][1], pins[i][0]))
    yrank = {p: r for r, p in enumerate(by_y)}
    pi = tuple(yrank[i] for i in by_x)
    xs = [pins[i][0] for i in by_x]
    ys = [pins[i][1] for i in by_y]
    gaps = [xs[k + 1] - xs[k] for k in range(d - 1)] + [ys[k + 1] - ys[k] for k in range(d - 1)]  # @line L2
    best = None
    for vec, st in powv_table(pi):
        w = sum(a * g for a, g in zip(vec, gaps))  # @line L3
        if best is None or w < best[0]:
            best = (w, st)
    w, st = best
    pinset = set(pins)
    return w, sorted({(xs[i], ys[j]) for i, j in st} - pinset)


def flute(pins: Sequence[Point]) -> tuple[int, list[Point], list[Edge]]:
    """Rectilinear Steiner tree of the pins in the style of FLUTE.

    Returns (length, points, edges): points are the pins followed by Steiner
    points, and edges join point indices. For at most TABLE_DEGREE pins the
    length is the optimum. Larger nets are split at a pin of median x rank or
    median y rank, recursively, and the shorter result is kept.
    """
    pins = list(pins)
    d = len(pins)
    if d <= TABLE_DEGREE:  # @line L1
        w, st = lookup(pins)
        pts = pins + st
        edges = mst_edges(pts)  # @line L4
        return sum(l1(pts[a], pts[b]) for a, b in edges), pts, edges
    best = None  # @line L5
    for axis in (0, 1):  # @line L6
        order = sorted(range(d), key=lambda i: (pins[i][axis], pins[i][1 - axis]))
        r = d // 2
        left = [pins[i] for i in order[: r + 1]]  # @line L7
        right = [pins[i] for i in order[r:]]
        wl, pl, el = flute(left)  # @line L8
        wr, pr, er = flute(right)
        if best is None or wl + wr < best[0]:
            best = (wl + wr, (order, r, pl, el, pr, er))
    total, (order, r, pl, el, pr, er) = best
    # Join the two trees at the shared pin order[r]; pins keep their input indices.
    idx_left = order[: r + 1] + [d + k for k in range(len(pl) - r - 1)]
    nl = len(pl) - r - 1
    idx_right = order[r:] + [d + nl + k for k in range(len(pr) - (d - r))]
    pts = pins + pl[r + 1:] + pr[d - r:]
    edges = [(idx_left[a], idx_left[b]) for a, b in el] + [(idx_right[a], idx_right[b]) for a, b in er]
    return total, pts, edges  # @line L9
