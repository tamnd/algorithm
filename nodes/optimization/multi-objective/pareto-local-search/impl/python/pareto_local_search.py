# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pareto-local-search/. The authors are listed in prov/X6FC7X.jsonl.

"""Pareto local search (Paquete, Chiarandini and Stuetzle 2004).

All objectives are minimized. The archive holds solutions with mutually
non-dominated images. Each archived solution is visited once: all its
neighbours are offered to the archive, and a neighbour enters when no member
weakly dominates its image. The search stops when every member is visited.
The member to visit is the oldest unvisited one, so a run is deterministic.
"""

from typing import Callable, Hashable, Iterable, Sequence

Vector = Sequence[float]


def dominates(a: Vector, b: Vector) -> bool:
    """Return True when a dominates b (minimization)."""
    strict = False
    for u, v in zip(a, b):
        if u > v:
            return False
        if u < v:
            strict = True
    return strict


def weakly_dominates(a: Vector, b: Vector) -> bool:
    return all(u <= v for u, v in zip(a, b))


def pareto_local_search(
    start: Hashable,
    f: Callable[[Hashable], Vector],
    neighbours: Callable[[Hashable], Iterable[Hashable]],
    on_visit: Callable[[Hashable, list], None] | None = None,
) -> list:
    """Return the final archive as a list of (solution, image) pairs."""
    archive = [[start, tuple(f(start)), False]]  # @line L1
    while True:
        cur = next((e for e in archive if not e[2]), None)
        if cur is None:  # @line L2
            break
        x = cur[0]  # @line L3
        for xn in neighbours(x):  # @line L4
            yn = tuple(f(xn))
            if any(weakly_dominates(e[1], yn) for e in archive):  # @line L5
                continue
            archive[:] = [e for e in archive if not dominates(yn, e[1])]  # @line L6
            archive.append([xn, yn, False])
        cur[2] = True  # @line L7
        if on_visit is not None:
            on_visit(x, [(e[0], e[1]) for e in archive])
    return [(e[0], e[1]) for e in archive]  # @line L8
