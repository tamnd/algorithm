# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lin-kernighan/. The authors are listed in prov/TAC0AY.jsonl.

from typing import Sequence

EPS = 1e-12


def tour_cost(cost: Sequence[Sequence[float]], tour: Sequence[int]) -> float:
    n = len(tour)
    if n < 2:
        return 0.0
    return sum(cost[tour[i]][tour[(i + 1) % n]] for i in range(n))


def nearest_lists(cost: Sequence[Sequence[float]], k: int) -> list[list[int]]:
    """The k nearest other cities of each city: the candidate lists."""
    n = len(cost)
    return [sorted((j for j in range(n) if j != i), key=lambda j: (cost[i][j], j))[:k] for i in range(n)]


def _edge(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def lk_search(
    cost: Sequence[Sequence[float]],
    path: list[int],
    candidates: Sequence[Sequence[int]],
    breadth: Sequence[int] = (5, 3),
    max_depth: int = 50,
    trace: list | None = None,
) -> tuple[float, list[int]] | None:
    """One variable-depth search from the Hamiltonian path that the removal of one tour edge leaves.

    path[0] = t1 is fixed and path[-1] is the free end. A step adds an edge from the free end y to a
    candidate z and removes the edge from z to its path neighbor w on the side of y, so w becomes
    the free end. The gain criterion keeps the partial gain positive; an added edge is never
    removed and a removed edge is never added again. Return (gain, tour) for the best closed tour
    with a positive gain, or None. If trace is a list, each tried step is appended to it.
    """
    t1 = path[0]
    removed = {_edge(path[0], path[-1])}
    added: set[tuple[int, int]] = set()
    best: tuple[float, list[int]] | None = None

    def step(p: list[int], gain: float, depth: int) -> bool:
        nonlocal best
        y = p[-1]
        where = {city: i for i, city in enumerate(p)}
        options = []
        for z in candidates[y]:
            i = where[z]
            if i >= len(p) - 2:  # z = y or z is the path neighbor of y
                continue
            w = p[i + 1]
            g = gain - cost[y][z]  # @line L4
            if g <= EPS or _edge(y, z) in removed or _edge(z, w) in added:
                continue
            options.append((cost[z][w] - cost[y][z], i, z, w, g))  # look ahead to the removed edge
        options.sort(reverse=True)
        width = breadth[depth] if depth < len(breadth) else 1
        for _, i, z, w, g in options[:width]:
            new_path = p[: i + 1] + p[i + 1 :][::-1]  # @line L5
            new_gain = g + cost[z][w]
            close = new_gain - cost[w][t1]  # @line L6
            if trace is not None:  # (depth, y, z, w, partial gain, gain of the closed tour)
                trace.append((depth, y, z, w, new_gain, close))
            if close > EPS and (best is None or close > best[0] + EPS):
                best = (close, new_path)
            added.add(_edge(y, z))
            removed.add(_edge(z, w))
            if depth + 1 < max_depth and (best is None or new_gain > best[0] + EPS):  # @line L7
                step(new_path, new_gain, depth + 1)
            added.discard(_edge(y, z))
            removed.discard(_edge(z, w))
            if best is not None:  # stop the backtracking at the first improvement
                return True
        return False

    step(path, cost[path[0]][path[-1]], 0)
    return best


def lin_kernighan(
    cost: Sequence[Sequence[float]],
    tour: Sequence[int],
    candidates: Sequence[Sequence[int]] | None = None,
    breadth: Sequence[int] = (5, 3),
) -> tuple[list[int], int]:
    """Repeat Lin-Kernighan searches from every city and both of its tour edges until none gains."""
    t = list(tour)
    n = len(t)
    if n < 4:
        return t, 0
    if candidates is None:
        candidates = nearest_lists(cost, min(8, n - 1))
    improvements = 0
    improved = True
    while improved:  # @line L1
        improved = False
        for start in range(n):
            for direction in (1, -1):  # @line L2
                i = t.index(start)
                ring = t[i:] + t[:i]
                if direction == 1:  # remove the edge from start to its successor
                    path = ring[:1] + ring[1:][::-1]
                else:  # remove the edge from start to its predecessor
                    path = ring
                found = lk_search(cost, path, candidates, breadth)  # @line L3
                if found is not None:  # @line L8
                    t = found[1]
                    improvements += 1
                    improved = True
                    break
            if improved:
                break
    return t, improvements  # @line L9
