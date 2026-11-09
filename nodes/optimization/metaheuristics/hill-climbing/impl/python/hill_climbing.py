# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hill-climbing/. The authors are listed in prov/NDHC1V.jsonl.

from collections.abc import Callable, Iterable
from typing import TypeVar

S = TypeVar("S")


def hill_climbing(
    x0: S,
    f: Callable[[S], float],
    neighbors: Callable[[S], Iterable[S]],
    rule: str = "best",
) -> tuple[S, float, list[S]]:
    """Minimize f by hill climbing from x0 and return (x, f(x), path).

    rule is "best" (steepest descent: move to a best neighbor, the first
    one in the order of neighbors(x) on a tie) or "first" (first
    improvement: move to the first neighbor that is better).
    Precondition: f takes finitely many values on the solutions reachable
    from x0, so the search stops. path lists x0 and each solution moved to;
    its last item is x, a local minimum: no y in neighbors(x) has f(y) < f(x).
    Cost: each step evaluates f at most |neighbors(x)| times.
    """
    if rule not in ("best", "first"):
        raise ValueError("rule must be 'best' or 'first'")
    x = x0  # @line L1
    fx = f(x)
    path = [x]
    while True:  # @line L2
        y_star, f_star = None, fx  # @line L3
        for y in neighbors(x):  # @line L4
            fy = f(y)
            if fy < f_star:  # @line L5
                y_star, f_star = y, fy  # @line L6
                if rule == "first":  # @line L7
                    break
        if y_star is None:  # @line L8
            return x, fx, path
        x, fx = y_star, f_star  # @line L9
        path.append(x)


def flip_neighbors(x: tuple[int, ...]) -> Iterable[tuple[int, ...]]:
    """The flip neighborhood of a 0-1 tuple: change one position, in index order."""
    for i in range(len(x)):
        yield x[:i] + (1 - x[i],) + x[i + 1 :]


def uncut_weight(edges: list[tuple[int, int, int]], x: tuple[int, ...]) -> int:
    """Max-Cut as minimization: the weight of the edges with both ends on one side."""
    return sum(w for u, v, w in edges if x[u] == x[v])


def two_opt_neighbors(tour: tuple[int, ...]) -> Iterable[tuple[int, ...]]:
    """The 2-opt neighborhood of a tour: reverse tour[i..j] for 1 <= i < j <= n - 1, (i, j) != (1, n - 1)."""
    n = len(tour)
    for i in range(1, n - 1):
        for j in range(i + 1, n):
            if i == 1 and j == n - 1:
                continue  # reversing all but city tour[0] gives the same cycle
            yield tour[:i] + tour[i : j + 1][::-1] + tour[j + 1 :]


def tour_length(d: list[list[int]], tour: tuple[int, ...]) -> int:
    """The length of the closed tour under the distance matrix d."""
    return sum(d[tour[k]][tour[(k + 1) % len(tour)]] for k in range(len(tour)))
