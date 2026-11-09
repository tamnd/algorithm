# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/late-acceptance-hill-climbing/. The authors are listed in prov/ZRSAWH.jsonl.

import math
import random
from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

S = TypeVar("S")


@dataclass
class Step(Generic[S]):
    """The record of iteration I: the candidate, the test and the state after it."""

    v: int  # the slot of the history list that was used
    f_candidate: float
    c_before: float  # C[v] before the update
    accepted: bool
    x: S
    fx: float


def late_acceptance_hill_climbing(
    x0: S,
    f: Callable[[S], float],
    random_neighbor: Callable[[S, random.Random], S],
    length: int,
    iterations: int,
    rng: random.Random,
) -> tuple[S, float, list[Step[S]]]:
    """Minimize f by late acceptance hill climbing (Burke and Bykov).

    A candidate y is accepted if f(y) <= C[I mod length] or f(y) <= f(x),
    where C[I mod length] is the cost of the current solution `length`
    iterations ago (f(x0) at the start). Returns (best, f(best), log).
    Cost: one evaluation of f and one random neighbor per iteration,
    plus O(length) space for the history list.
    """
    if length < 1 or iterations < 0:
        raise ValueError("length must be at least 1 and iterations non-negative")
    x, fx = x0, f(x0)  # @line L1
    best, f_best = x, fx
    c = [fx] * length  # @line L2
    log: list[Step[S]] = []
    for i in range(iterations):  # @line L3
        y = random_neighbor(x, rng)  # @line L4
        fy = f(y)
        v = i % length  # @line L5
        c_before = c[v]
        accepted = fy <= c[v] or fy <= fx  # @line L6
        if accepted:
            x, fx = y, fy
        c[v] = fx  # @line L7
        if fx < f_best:  # @line L8
            best, f_best = x, fx
        log.append(Step(v, fy, c_before, accepted, x, fx))
    return best, f_best, log  # @line L9


def random_two_opt(tour: tuple[int, ...], rng: random.Random) -> tuple[int, ...]:
    """A uniform random 2-opt neighbor: reverse tour[i..j], 1 <= i < j <= n - 1, (i, j) != (1, n - 1).

    Needs n >= 4, so that the neighborhood is not empty.
    """
    n = len(tour)
    while True:
        i, j = sorted(rng.sample(range(1, n), 2))
        if not (i == 1 and j == n - 1):
            return tour[:i] + tour[i : j + 1][::-1] + tour[j + 1 :]


def distance_matrix(points: list[tuple[int, int]]) -> list[list[int]]:
    """Euclidean distances rounded to the nearest integer."""
    return [[round(math.dist(p, q)) for q in points] for p in points]


def tour_length(d: list[list[int]], tour: tuple[int, ...]) -> int:
    """The length of the closed tour under the distance matrix d."""
    return sum(d[tour[k]][tour[(k + 1) % len(tour)]] for k in range(len(tour)))
