# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/glauber-dynamics/. The authors are listed in prov/G0ENPS.jsonl.

import random
from fractions import Fraction
from typing import Callable, Sequence


def allowed_colors(adj: Sequence[Sequence[int]], q: int, x: Sequence[int], v: int) -> list[int]:
    """The colors in 0..q-1 that no neighbor of v has in the coloring x."""
    used = {x[w] for w in adj[v]}
    return [c for c in range(q) if c not in used]


def glauber_coloring_step(adj: Sequence[Sequence[int]], q: int, x: list[int], rng: random.Random) -> list[int]:
    """One heat-bath step for proper q-colorings, in place.

    Pick a uniform vertex v, then give v a uniform color among the colors
    that its neighbors do not use. This is a draw from the uniform
    distribution on proper colorings, conditioned on the colors off v.
    Needs q > max degree, so that the list is never empty.
    """
    v = rng.randrange(len(adj))  # @line L2
    a = allowed_colors(adj, q, x, v)  # @line L3
    if not a:
        raise ValueError("q must be larger than the degree of each vertex")
    x[v] = a[rng.randrange(len(a))]  # @line L4
    return x


def glauber_coloring(
    adj: Sequence[Sequence[int]], q: int, x: list[int], steps: int, rng: random.Random
) -> list[int]:
    """Run steps heat-bath steps from the coloring x, in place, and return x.

    Each step costs O(deg(v) + q) time. With q > 2 * max degree, the
    distribution after t steps is within total variation eps of uniform
    for t >= (q - D) / (q - 2D) * n * ln(n / eps), D the max degree.
    """
    for _ in range(steps):  # @line L1
        glauber_coloring_step(adj, q, x, rng)
    return x


def is_proper(adj: Sequence[Sequence[int]], x: Sequence[int]) -> bool:
    return all(x[v] != x[w] for v in range(len(adj)) for w in adj[v])


def greedy_coloring(adj: Sequence[Sequence[int]], q: int) -> list[int]:
    """A proper coloring to start from: color the vertices in order, smallest free color."""
    x = [-1] * len(adj)
    for v in range(len(adj)):
        used = {x[w] for w in adj[v] if x[w] >= 0}
        x[v] = min(c for c in range(q) if c not in used)
    return x


def heat_bath_law(
    x: Sequence[int], v: int, values: Sequence[int], weight: Callable[[Sequence[int]], Fraction]
) -> list[tuple[int, Fraction]]:
    """The law of the new value at site v: pi conditioned on the other sites.

    weight(y) is pi(y) up to a constant factor. The result lists each value
    s with probability weight(x with x[v] = s) / sum over s'. Exact when the
    weights are Fractions.
    """
    y = list(x)
    ws = []
    for s in values:
        y[v] = s
        ws.append(weight(y))
    total = sum(ws)
    if total == 0:
        raise ValueError("all values at this site have weight 0")
    return [(s, w / total) for s, w in zip(values, ws)]


def glauber_step(
    x: list[int],
    values: Sequence[int],
    weight: Callable[[Sequence[int]], float],
    rng: random.Random,
) -> list[int]:
    """One step of Glauber dynamics for a general distribution, in place.

    Pick a uniform site v, then draw x[v] from heat_bath_law. Uses
    rng.random(), so it is exact only up to floating point.
    """
    v = rng.randrange(len(x))
    law = heat_bath_law(x, v, values, weight)
    r = rng.random()
    acc = 0.0
    for s, p in law:
        acc += float(p)
        if r < acc:
            x[v] = s
            return x
    x[v] = law[-1][0]
    return x
