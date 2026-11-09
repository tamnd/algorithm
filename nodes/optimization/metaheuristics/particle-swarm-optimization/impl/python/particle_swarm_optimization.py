# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/particle-swarm-optimization/. The authors are listed in prov/F6H8KV.jsonl.

import math
import random
from collections.abc import Callable, Sequence

Vector = list[float]


def particle_swarm_optimization(
    f: Callable[[Sequence[float]], float],
    lower: Sequence[float],
    upper: Sequence[float],
    n_particles: int,
    w: float,
    c1: float,
    c2: float,
    iterations: int,
    rng: random.Random,
    on_move: Callable[..., None] | None = None,
) -> tuple[Vector, float, list[float], list[Vector]]:
    """Minimize f with the global-best particle swarm with inertia weight w.

    Positions start uniformly in the box [lower, upper] and velocities at 0.
    The best point g is updated as soon as a particle improves on it.
    Positions are not clipped to the box. Returns (g, f(g), history,
    personal bests), where history[t] is f(g) after iteration t.
    on_move(i, x_old, v_old, p, g, r1, r2, v_new, x_new) is called for each
    move, for tests. Precondition: n_particles >= 1 and lower[d] <= upper[d].
    Cost: O(iterations * n_particles * (n + c)) time for dimension n and
    evaluation cost c, and O(n_particles * n) space.
    """
    n = len(lower)
    xs = [[rng.uniform(lower[d], upper[d]) for d in range(n)] for _ in range(n_particles)]  # @line L1
    vs = [[0.0] * n for _ in range(n_particles)]
    ps = [list(x) for x in xs]
    fp = [f(x) for x in xs]
    best = min(range(n_particles), key=lambda i: fp[i])  # @line L2
    g, fg = list(ps[best]), fp[best]
    history = [fg]
    for _ in range(iterations):  # @line L3
        for i in range(n_particles):  # @line L4
            x, v, p = xs[i], vs[i], ps[i]
            x_old, v_old, g_old = list(x), list(v), list(g)
            r1 = [rng.random() for _ in range(n)]  # @line L5
            r2 = [rng.random() for _ in range(n)]
            for d in range(n):
                v[d] = w * v[d] + c1 * r1[d] * (p[d] - x[d]) + c2 * r2[d] * (g[d] - x[d])  # @line L6
                x[d] = x[d] + v[d]  # @line L7
            if on_move is not None:
                on_move(i, x_old, v_old, list(p), g_old, r1, r2, list(v), list(x))
            fx = f(x)
            if fx < fp[i]:  # @line L8
                ps[i], fp[i] = list(x), fx
                if fx < fg:  # @line L9
                    g, fg = list(x), fx
        history.append(fg)
    return g, fg, history, ps  # @line L10


def constriction_coefficient(phi: float) -> float:
    """Clerc and Kennedy's chi = 2 / |2 - phi - sqrt(phi^2 - 4 phi)| for phi > 4."""
    return 2.0 / abs(2.0 - phi - math.sqrt(phi * phi - 4.0 * phi))


def order1_stable(w: float, c1: float, c2: float) -> bool:
    """The mean of a stagnant particle converges iff |w| < 1 and 0 < c1 + c2 < 4 (1 + w)."""
    return abs(w) < 1 and 0 < c1 + c2 < 4 * (1 + w)


def order2_stable_equal(w: float, c: float) -> bool:
    """Poli's second-order region for c1 = c2 = c / 2: |w| < 1 and 0 < c < 24 (1 - w^2) / (7 - 5 w)."""
    return abs(w) < 1 and 0 < c < 24 * (1 - w * w) / (7 - 5 * w)


def sphere(x: Sequence[float]) -> float:
    """The sum of squares; its minimum 0 is at the origin."""
    return sum(t * t for t in x)
