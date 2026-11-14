# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sat-based-fpga-routing/. The authors are listed in prov/1K07JP.jsonl.

"""SAT-based detailed routing for an island-style FPGA, after Nam, Sakallah and Rutenbar.

The global routing is fixed. Each net is a route tree over channel segments:
a list of segments and a list of edges (s, s2, kind), where s and s2 meet at a
switch block and kind names the two sides of the switch block that the edge
joins, such as "WN" for west to north or "EW" for east to west. Every
channel segment has W tracks 0..W-1. The switch pattern is a function
pattern(kind, t, W) that returns the set of tracks of s2 that a switch joins
to track t of s.

A legal detailed routing gives each net one track on each segment of its
route, such that two nets that share a segment use different tracks there, and
the two tracks of every edge are joined by a switch.
"""

import itertools

from small_dpll import solve


def disjoint_pattern(kind: str, t: int, w: int) -> set[int]:
    """Track t meets only track t (the subset switch block)."""
    return {t}


def twisted_pattern(kind: str, t: int, w: int) -> set[int]:
    """Like the disjoint pattern, but the turn between the west and north sides joins track t to track w - 1 - t."""
    return {w - 1 - t} if kind in ("WN", "NW") else {t}


def encode(nets, w: int, pattern):
    """Return (number of variables, clauses, var) where var[(n, s, t)] is the variable of net n on track t of s."""
    var: dict[tuple[int, int, int], int] = {}
    for n, (segs, _) in enumerate(nets):  # @line L1
        for s in segs:
            for t in range(w):
                var[(n, s, t)] = len(var) + 1
    clauses: list[list[int]] = []
    for n, (segs, _) in enumerate(nets):
        for s in segs:
            clauses.append([var[(n, s, t)] for t in range(w)])  # @line L2
            for t, u in itertools.combinations(range(w), 2):
                clauses.append([-var[(n, s, t)], -var[(n, s, u)]])  # @line L3
    users: dict[int, list[int]] = {}
    for n, (segs, _) in enumerate(nets):
        for s in segs:
            users.setdefault(s, []).append(n)
    for s, ns in users.items():
        for n, m in itertools.combinations(ns, 2):
            for t in range(w):
                clauses.append([-var[(n, s, t)], -var[(m, s, t)]])  # @line L4
    for n, (segs, edges) in enumerate(nets):
        for s, s2, kind in edges:
            for t in range(w):
                clauses.append([-var[(n, s, t)]] + [var[(n, s2, u)] for u in sorted(pattern(kind, t, w))])  # @line L5
    return len(var), clauses, var


def sat_route(nets, w: int, pattern):
    """Return {(net, segment): track} for a legal detailed routing, or None if none exists at width w."""
    if w < 1:
        return None if any(segs for segs, _ in nets) else {}
    n_vars, clauses, var = encode(nets, w, pattern)
    model = solve(n_vars, clauses)  # @line L6
    if model is None:
        return None  # @line L7
    return {(n, s): t for (n, s, t), v in var.items() if model[v]}  # @line L8


def is_legal(nets, w: int, pattern, tracks) -> bool:
    for n, (segs, edges) in enumerate(nets):
        for s in segs:
            if not (0 <= tracks.get((n, s), -1) < w):
                return False
        for s, s2, kind in edges:
            if tracks[(n, s2)] not in pattern(kind, tracks[(n, s)], w):
                return False
    used: set[tuple[int, int]] = set()
    for n, (segs, _) in enumerate(nets):
        for s in segs:
            if (s, tracks[(n, s)]) in used:
                return False
            used.add((s, tracks[(n, s)]))
    return True


def exhaustive_route(nets, w: int, pattern):
    """Reference: try every assignment of tracks to the (net, segment) pairs."""
    keys = [(n, s) for n, (segs, _) in enumerate(nets) for s in segs]
    for choice in itertools.product(range(w), repeat=len(keys)):
        tracks = dict(zip(keys, choice))
        if is_legal(nets, w, pattern, tracks):
            return tracks
    return None


def min_width(nets, pattern, w_max: int):
    """Least w in 1..w_max at which the global routing has a legal detailed routing, or None."""
    for w in range(1, w_max + 1):
        if sat_route(nets, w, pattern) is not None:
            return w
    return None
