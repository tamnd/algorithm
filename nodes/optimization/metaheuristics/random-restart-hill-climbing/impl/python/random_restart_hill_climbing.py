# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-restart-hill-climbing/. The authors are listed in prov/JWD170.jsonl.

import random
from collections.abc import Callable, Iterable
from typing import TypeVar

S = TypeVar("S")


def hill_climbing(x: S, f: Callable[[S], float], neighbors: Callable[[S], Iterable[S]]) -> tuple[S, float]:
    """Best-improvement hill climbing: return a local minimum reached from x and its value."""
    fx = f(x)
    while True:
        y_star, f_star = None, fx
        for y in neighbors(x):
            fy = f(y)
            if fy < f_star:
                y_star, f_star = y, fy
        if y_star is None:
            return x, fx
        x, fx = y_star, f_star


def random_restart_hill_climbing(
    random_start: Callable[[random.Random], S],
    f: Callable[[S], float],
    neighbors: Callable[[S], Iterable[S]],
    runs: int,
    rng: random.Random,
    target: float | None = None,
) -> tuple[S, float, list[tuple[S, S, float]]]:
    """Run hill climbing from `runs` independent random starts and keep the best end.

    Returns (best, f(best), log), where log has one (start, end, f(end))
    entry per run. If target is given, stop after the first run whose end
    has f <= target. Precondition: runs >= 1. Cost: the sum of the costs
    of the runs of hill climbing.
    """
    if runs < 1:
        raise ValueError("runs must be at least 1")
    best, f_best = None, 0.0  # @line L1
    log: list[tuple[S, S, float]] = []
    for _ in range(runs):  # @line L2
        x0 = random_start(rng)  # @line L3
        x, fx = hill_climbing(x0, f, neighbors)  # @line L4
        log.append((x0, x, fx))
        if best is None or fx < f_best:  # @line L5
            best, f_best = x, fx
        if target is not None and f_best <= target:  # @line L6
            break
    return best, f_best, log  # @line L7


def random_bits(n: int) -> Callable[[random.Random], tuple[int, ...]]:
    """A start generator: a uniform random 0-1 tuple of length n."""
    return lambda rng: tuple(rng.randint(0, 1) for _ in range(n))


def flip_neighbors(x: tuple[int, ...]) -> Iterable[tuple[int, ...]]:
    """The flip neighborhood of a 0-1 tuple, in index order."""
    for i in range(len(x)):
        yield x[:i] + (1 - x[i],) + x[i + 1 :]


def uncut_weight(edges: list[tuple[int, int, int]], x: tuple[int, ...]) -> int:
    """Max-Cut as minimization: the weight of the edges with both ends on one side."""
    return sum(w for u, v, w in edges if x[u] == x[v])
