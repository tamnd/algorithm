# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variable-neighborhood-search/. The authors are listed in prov/WPXWMK.jsonl.

import itertools
import random
from collections.abc import Callable, Iterable
from typing import TypeVar

S = TypeVar("S")


def variable_neighborhood_search(
    x0: S,
    f: Callable[[S], float],
    shake: Callable[[S, int, random.Random], S],
    local_search: Callable[[S], S],
    k_max: int,
    iterations: int,
    rng: random.Random,
) -> tuple[S, float, list[tuple[int, S, float, bool]]]:
    """Minimize f by general variable neighborhood search (Mladenovic and Hansen).

    Each iteration shakes the current solution in the k-th neighborhood,
    runs the local search, and moves if the result is strictly better: then
    k returns to 1, otherwise k grows by 1 and wraps from k_max to 1.
    Returns (x, f(x), log) with one (k, local optimum, value, moved) entry
    per iteration. Cost: `iterations` + 1 runs of the local search.
    """
    if k_max < 1 or iterations < 0:
        raise ValueError("k_max must be at least 1 and iterations non-negative")
    x = local_search(x0)  # @line L1
    fx = f(x)
    k = 1  # @line L2
    log: list[tuple[int, S, float, bool]] = []
    for _ in range(iterations):  # @line L3
        y = shake(x, k, rng)  # @line L4
        z = local_search(y)  # @line L5
        fz = f(z)
        moved = fz < fx  # @line L6
        log.append((k, z, fz, moved))
        if moved:
            x, fx, k = z, fz, 1
        else:
            k = k + 1 if k < k_max else 1  # @line L7
    return x, fx, log  # @line L8


def variable_neighborhood_descent(
    f: Callable[[S], float], neighborhoods: list[Callable[[S], Iterable[S]]]
) -> Callable[[S], S]:
    """VND: best improvement in N_1; if none, try N_2, and so on; after a move, go back to N_1.

    The result is a local minimum of every neighborhood in the list.
    """

    def run(x: S) -> S:
        fx, k = f(x), 0
        while k < len(neighborhoods):
            y = min(neighborhoods[k](x), key=f, default=None)
            if y is not None and f(y) < fx:
                x, fx, k = y, f(y), 0
            else:
                k += 1
        return x

    return run


def flip_neighbors(x: tuple[int, ...]) -> Iterable[tuple[int, ...]]:
    """All strings at Hamming distance 1, in index order."""
    for i in range(len(x)):
        yield x[:i] + (1 - x[i],) + x[i + 1 :]


def two_flip_neighbors(x: tuple[int, ...]) -> Iterable[tuple[int, ...]]:
    """All strings at Hamming distance 2, in lexicographic order of the pair of indices."""
    for i, j in itertools.combinations(range(len(x)), 2):
        y = list(x)
        y[i], y[j] = 1 - y[i], 1 - y[j]
        yield tuple(y)


def shake_flips(x: tuple[int, ...], k: int, rng: random.Random) -> tuple[int, ...]:
    """A uniform random string at Hamming distance min(k, n) from x."""
    y = list(x)
    for i in rng.sample(range(len(x)), min(k, len(x))):
        y[i] = 1 - y[i]
    return tuple(y)


def uncut_weight(edges: list[tuple[int, int, int]], x: tuple[int, ...]) -> int:
    """Max-Cut as minimization: the weight of the edges with both ends on one side."""
    return sum(w for u, v, w in edges if x[u] == x[v])
