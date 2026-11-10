# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mitchell-guillotine-ptas/. The authors are listed in prov/XPPZ2J.jsonl.

"""The parts of Mitchell's guillotine scheme that can be checked on small inputs.

A network is a list of straight edges (p, q) between points in general position (no two points share an x or a y
value). The windows are the rectangles with sides on the lines through the points. For one fixed network, a dynamic
program over the windows finds the cut tree with the least total bridge length, which gives an m-guillotine network
that contains it. For a tour, doubling the bridges and shortcutting an Euler circuit gives a tour again. The full
scheme also minimizes over the network, with the boundary states counted by side_signature; that part is not run."""

from fractions import Fraction
from math import dist
from typing import Optional, Sequence

Point = tuple
Edge = tuple
Window = tuple


def general_position(points: Sequence[Point]) -> bool:
    return len({p[0] for p in points}) == len(points) == len({p[1] for p in points})


def crossings(edges: Sequence[Edge], w: Window, axis: str, c) -> list[tuple]:
    """The points where the edges meet the line x = c (axis "x") or y = c (axis "y") with the other coordinate
    strictly inside the window, in order. Each item is (coordinate along the line, indices of the edges there)."""
    lo, hi = (w[2], w[3]) if axis == "x" else (w[0], w[1])
    k = 0 if axis == "x" else 1
    found: dict = {}
    for i, (p, q) in enumerate(edges):
        a, b = p[k], q[k]
        if a == b or not min(a, b) <= c <= max(a, b):
            continue  # an edge on the line itself cannot occur in general position
        t = p[1 - k] + Fraction(c - a, b - a) * (q[1 - k] - p[1 - k])
        if lo < t < hi:
            found.setdefault(t, []).append(i)
    return sorted((t, tuple(ids)) for t, ids in found.items())


def m_span(parts: Sequence[tuple], m: int) -> Optional[tuple]:
    """From the m-th part to the m-th part from the other end; None if there are at most 2(m - 1) parts."""
    k = len(parts)
    if k <= 2 * (m - 1):
        return None
    return parts[m - 1][0], parts[k - m][0]


def windows_of(points: Sequence[Point]) -> tuple[list, list, list[tuple]]:
    xs, ys = sorted(p[0] for p in points), sorted(p[1] for p in points)
    ws = [(i0, i1, j0, j1) for i0 in range(len(xs)) for i1 in range(i0 + 1, len(xs))
          for j0 in range(len(ys)) for j1 in range(j0 + 1, len(ys))]
    ws.sort(key=lambda t: (t[1] - t[0]) + (t[3] - t[2]))
    return xs, ys, ws


def least_bridges(points: Sequence[Point], edges: Sequence[Edge], m: int,
                  stats: Optional[dict] = None) -> tuple[Fraction, list[tuple]]:
    """The least total bridge length over all cut trees whose cuts lie on the lines through the points, and the
    bridges (axis, c, lo, hi, window) of one best tree. A window with no point strictly inside is a leaf."""
    xs, ys, ws = windows_of(points)  # @line L1
    best: dict = {}
    transitions = 0
    for i0, i1, j0, j1 in ws:
        w = (xs[i0], xs[i1], ys[j0], ys[j1])
        if not any(w[0] < p[0] < w[1] and w[2] < p[1] < w[3] for p in points):
            best[(i0, i1, j0, j1)] = (0, None)
            continue
        options = []
        for axis, cuts in (("x", range(i0 + 1, i1)), ("y", range(j0 + 1, j1))):
            for c in cuts:
                transitions += 1
                if axis == "x":
                    a, b = (i0, c, j0, j1), (c, i1, j0, j1)
                    sp = m_span(crossings(edges, w, "x", xs[c]), m)
                else:
                    a, b = (i0, i1, j0, c), (i0, i1, c, j1)
                    sp = m_span(crossings(edges, w, "y", ys[c]), m)
                cost = 0 if sp is None else sp[1] - sp[0]
                options.append((cost + best[a][0] + best[b][0], axis, c))  # @line L3
        value, axis, c = min(options)
        best[(i0, i1, j0, j1)] = (value, (axis, c))
    root = (0, len(xs) - 1, 0, len(ys) - 1)
    bridges, todo = [], [root]
    while todo:
        key = todo.pop()
        if best[key][1] is None:
            continue
        i0, i1, j0, j1 = key
        w = (xs[i0], xs[i1], ys[j0], ys[j1])
        axis, c = best[key][1]
        line = xs[c] if axis == "x" else ys[c]
        sp = m_span(crossings(edges, w, axis, line), m)
        if sp is not None and sp[1] > sp[0]:
            bridges.append((axis, line, sp[0], sp[1], w))
        todo += [(i0, c, j0, j1), (c, i1, j0, j1)] if axis == "x" else [(i0, i1, j0, c), (i0, i1, c, j1)]
    if stats is not None:
        stats["windows"] = len(ws)
        stats["transitions"] = transitions
    return best[root][0], bridges


def side_signature(edges: Sequence[Edge], w: Window, side: str, m: int) -> tuple:
    """What the dynamic program stores about one side of a window: the edges of the first m and the last m parts on
    the side (the m-th ones carry the ends of the bridge), or all parts if there are at most 2(m - 1)."""
    x0, x1, y0, y1 = w
    axis, c = {"left": ("x", x0), "right": ("x", x1), "bottom": ("y", y0), "top": ("y", y1)}[side]
    ids = [frozenset(frozenset(edges[i]) for i in ids) for _, ids in crossings(edges, w, axis, c)]  # @line L2
    if len(ids) <= 2 * (m - 1):
        return ("all",) + tuple(ids)
    return ("span",) + tuple(ids[:m]) + tuple(ids[-m:])


def node(axis: str, c, t) -> Point:
    return (c, t) if axis == "x" else (t, c)


def with_bridges(points: Sequence[Point], edges: Sequence[Edge], bridges: Sequence[tuple],
                 copies: int) -> list[tuple]:
    """The multigraph of the network with each bridge added copies times. Edges are split where a bridge meets
    them, so every piece joins two nodes."""
    splits: dict = {i: {p, q} for i, (p, q) in enumerate(edges)}
    pieces = []
    for axis, c, lo, hi, w in bridges:
        on = [(t, ids) for t, ids in crossings(edges, w, axis, c) if lo <= t <= hi]
        for t, ids in on:
            for i in ids:
                splits[i].add(node(axis, c, t))
        for (t, _), (u, _) in zip(on, on[1:]):
            pieces += [(node(axis, c, t), node(axis, c, u))] * copies
    for i, (p, q) in enumerate(edges):
        cut = sorted(splits[i], key=lambda r: dist(p, r))
        pieces += list(zip(cut, cut[1:]))
    return pieces


def length(pieces: Sequence[tuple]) -> float:
    return sum(dist(p, q) for p, q in pieces)


def even_and_connected(pieces: Sequence[tuple]) -> bool:
    adj: dict = {}
    for p, q in pieces:
        adj.setdefault(p, []).append(q)
        adj.setdefault(q, []).append(p)
    if any(len(v) % 2 for v in adj.values()):
        return False
    start = next(iter(adj))
    seen, stack = {start}, [start]
    while stack:
        for q in adj[stack.pop()]:
            if q not in seen:
                seen.add(q)
                stack.append(q)
    return len(seen) == len(adj)


def euler_shortcut(points: Sequence[Point], pieces: Sequence[tuple]) -> list[int]:
    """Walk an Euler circuit (Hierholzer, without recursion) and keep the first visit of each input point."""
    adj: dict = {}
    for k, (p, q) in enumerate(pieces):
        adj.setdefault(p, []).append((q, k))
        adj.setdefault(q, []).append((p, k))
    used = [False] * len(pieces)
    stack, walk = [points[0]], []
    while stack:
        v = stack[-1]
        while adj[v] and used[adj[v][-1][1]]:
            adj[v].pop()
        if adj[v]:
            q, k = adj[v].pop()
            used[k] = True
            stack.append(q)
        else:
            walk.append(stack.pop())
    index = {p: i for i, p in enumerate(points)}
    order, seen = [], set()
    for v in walk:
        if v in index and v not in seen:
            seen.add(v)
            order.append(index[v])
    return order


def tour_edges(points: Sequence[Point], order: Sequence[int]) -> list[Edge]:
    return [(points[order[i]], points[order[(i + 1) % len(order)]]) for i in range(len(order))]


def tour_length(points: Sequence[Point], order: Sequence[int]) -> float:
    return sum(dist(p, q) for p, q in tour_edges(points, order))


def guillotine_tour(points: Sequence[Point], order: Sequence[int], m: int,
                    stats: Optional[dict] = None) -> tuple[list[int], float, Fraction]:
    """Make the tour m-guillotine with the least bridges, double them, and shortcut an Euler circuit. Returns the
    new order, the length of the graph and the bridge length."""
    edges = tour_edges(points, order)
    total, bridges = least_bridges(points, edges, m, stats)
    pieces = with_bridges(points, edges, bridges, 2)
    if not even_and_connected(pieces):  # @line L4
        raise AssertionError("doubled bridges keep the degrees even and the graph connected")
    return euler_shortcut(points, pieces), length(pieces), total  # @line L5
