# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/force-directed-layout/. The authors are listed in prov/MAJJEY.jsonl.

import math


def force_directed_layout(
    n: int,
    edges: list[tuple[int, int]],
    pos: list[tuple[float, float]],
    k: float = 1.0,
    t0: float = 0.1,
    rounds: int = 100,
) -> list[tuple[float, float]]:
    """Fruchterman-Reingold layout in the plane, from the start positions pos.

    Every pair of vertices repels with force k^2 / d, every edge attracts its
    ends with force d^2 / k, and each vertex moves along its total force by at
    most the temperature, which falls linearly from t0 to 0 over the rounds.
    Two vertices at the same point are pushed apart along the x axis, the lower
    index to the left. The graph is undirected; self-loops and repeated edges
    are ignored. There is no frame, so components drift apart.
    Time O(n^2 + m) per round, extra space O(n).
    """
    edge_set = sorted({(min(u, v), max(u, v)) for u, v in edges if u != v})
    x = [float(p[0]) for p in pos]
    y = [float(p[1]) for p in pos]
    t = t0  # @line L1
    for r in range(1, rounds + 1):  # @line L2
        dx = [0.0] * n  # @line L3
        dy = [0.0] * n
        for u in range(n):  # @line L4
            for v in range(u + 1, n):
                ex, ey = x[v] - x[u], y[v] - y[u]
                d = math.hypot(ex, ey)
                if d == 0.0:
                    ex, ey, d = 1.0, 0.0, 1.0
                    f = k * k / 1e-9
                else:
                    f = k * k / d
                dx[v] += ex / d * f
                dy[v] += ey / d * f
                dx[u] -= ex / d * f
                dy[u] -= ey / d * f
        for u, v in edge_set:  # @line L5
            ex, ey = x[v] - x[u], y[v] - y[u]
            d = math.hypot(ex, ey)
            f = d * d / k
            if d > 0.0:
                dx[v] -= ex / d * f
                dy[v] -= ey / d * f
                dx[u] += ex / d * f
                dy[u] += ey / d * f
        for v in range(n):  # @line L6
            length = math.hypot(dx[v], dy[v])
            if length > 0.0:
                step = min(length, t)
                x[v] += dx[v] / length * step
                y[v] += dy[v] / length * step
        t = t0 * (1 - r / rounds)  # @line L7
    return list(zip(x, y))  # @line L8
