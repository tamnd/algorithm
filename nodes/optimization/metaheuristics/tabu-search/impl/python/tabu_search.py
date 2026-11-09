# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tabu-search/. The authors are listed in prov/4KBPCC.jsonl.

from collections import deque
from collections.abc import Callable, Hashable, Iterable
from dataclasses import dataclass
from typing import Generic, TypeVar

S = TypeVar("S")


@dataclass
class Step(Generic[S]):
    """The record of one iteration: the move made and the state after it."""

    attribute: Hashable
    x: S
    fx: float
    aspirated: bool  # the move was tabu and the aspiration criterion allowed it
    tabu_list: list[Hashable]
    f_best: float


def tabu_search(
    x0: S,
    f: Callable[[S], float],
    moves: Callable[[S], Iterable[tuple[Hashable, S]]],
    tenure: int,
    iterations: int,
) -> tuple[S, float, list[Step[S]]]:
    """Minimize f by tabu search with a recency-based tabu list and aspiration by objective.

    moves(x) yields (attribute, y) for each feasible neighbor y of x. The
    tabu list holds the attributes of the last `tenure` moves; a move whose
    attribute is in the list is tabu, unless f(y) < f(best) (aspiration by
    objective). Each iteration moves to an allowed neighbor of least f (the
    first one on a tie), even when it is worse than x. The search stops
    after `iterations` moves, or earlier if no move is allowed.
    Returns (best, f(best), log). Cost: one evaluation of f per neighbor
    per iteration, plus O(tenure) for the tabu tests.
    """
    if tenure < 0 or iterations < 0:
        raise ValueError("tenure and iterations must be non-negative")
    x, fx = x0, f(x0)  # @line L1
    best, f_best = x, fx
    tabu: deque[Hashable] = deque()
    log: list[Step[S]] = []
    for _ in range(iterations):  # @line L2
        chosen = None  # @line L3
        for a, y in moves(x):  # @line L4
            fy = f(y)
            if a in tabu and not fy < f_best:  # @line L5
                continue
            if chosen is None or fy < chosen[2]:  # @line L6
                chosen = (a, y, fy, a in tabu)
        if chosen is None:  # @line L7
            break
        a, x, fx, aspirated = chosen  # @line L8
        tabu.append(a)  # @line L9
        if len(tabu) > tenure:
            tabu.popleft()
        if fx < f_best:  # @line L10
            best, f_best = x, fx
        log.append(Step(a, x, fx, aspirated, list(tabu), f_best))
    return best, f_best, log  # @line L11


def knapsack_moves(
    weights: list[int], capacity: int
) -> Callable[[tuple[int, ...]], Iterable[tuple[Hashable, tuple[int, ...]]]]:
    """Flip moves of the 0-1 knapsack: add or remove item i, keeping the weight at most capacity.

    The attribute of a move is the item index i.
    """

    def moves(x: tuple[int, ...]) -> Iterable[tuple[Hashable, tuple[int, ...]]]:
        load = sum(w for w, b in zip(weights, x) if b)
        for i in range(len(x)):
            if x[i] or load + weights[i] <= capacity:
                yield i, x[:i] + (1 - x[i],) + x[i + 1 :]

    return moves


def knapsack_objective(values: list[int]) -> Callable[[tuple[int, ...]], int]:
    """The knapsack as minimization: f(x) = -(total value of the chosen items)."""
    return lambda x: -sum(v for v, b in zip(values, x) if b)
