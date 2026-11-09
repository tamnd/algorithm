# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pareto-ranking/. The authors are listed in prov/MN6FJG.jsonl.

"""Three Pareto rankings of a list of objective vectors (all objectives minimized).

- goldberg_rank: the front number from non-dominated sorting (NSGA, NSGA-II).
- fonseca_fleming_rank: one plus the number of points that dominate a point (MOGA).
- spea2_raw_fitness: the sum of the strengths of the points that dominate a point (SPEA2).

Lower is better for all three. Each costs O(p N^2) time.
"""

from typing import Callable, Sequence

Vector = Sequence[float]


def dominates(a: Vector, b: Vector) -> bool:
    """Return True when a dominates b (minimization)."""
    strict = False
    for x, y in zip(a, b):
        if x > y:
            return False
        if x < y:
            strict = True
    return strict


def dominance_lists(points: Sequence[Vector]) -> tuple[list[list[int]], list[list[int]]]:
    """Return (beats, beaten_by): beats[i] lists the j that i dominates, beaten_by[j] the i that dominate j."""
    n = len(points)
    beats: list[list[int]] = [[] for _ in range(n)]
    beaten_by: list[list[int]] = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if dominates(points[i], points[j]):
                beats[i].append(j)
                beaten_by[j].append(i)
            elif dominates(points[j], points[i]):
                beats[j].append(i)
                beaten_by[i].append(j)
    return beats, beaten_by


def _goldberg(beats: list[list[int]], beaten_by: list[list[int]]) -> list[int]:
    count = [len(b) for b in beaten_by]
    rank = [0] * len(beats)
    current = [i for i in range(len(beats)) if count[i] == 0]
    k = 1
    while current:
        nxt = []
        for i in current:
            rank[i] = k
            for j in beats[i]:
                count[j] -= 1
                if count[j] == 0:
                    nxt.append(j)
        current = nxt
        k += 1
    return rank


def _fonseca_fleming(beats: list[list[int]], beaten_by: list[list[int]]) -> list[int]:
    return [1 + len(b) for b in beaten_by]


def _spea2_raw(beats: list[list[int]], beaten_by: list[list[int]]) -> list[int]:
    strength = [len(b) for b in beats]
    return [sum(strength[j] for j in beaten_by[i]) for i in range(len(beats))]


RULES = {"goldberg": _goldberg, "fonseca-fleming": _fonseca_fleming, "spea2": _spea2_raw}


def goldberg_rank(points: Sequence[Vector]) -> list[int]:
    """Front number: 1 for the non-dominated points, k + 1 for the front after front k."""
    return _goldberg(*dominance_lists(points))


def fonseca_fleming_rank(points: Sequence[Vector]) -> list[int]:
    """MOGA rank: 1 + the number of points that dominate the point."""
    return _fonseca_fleming(*dominance_lists(points))


def spea2_raw_fitness(points: Sequence[Vector]) -> list[int]:
    """SPEA2 raw fitness R(i) = sum of S(j) over the j that dominate i, S(j) = |points j dominates|."""
    return _spea2_raw(*dominance_lists(points))


def pareto_rank_order(
    xs: Sequence[object],
    f: Callable[[object], Vector],
    rule: str = "goldberg",
    density: Callable[[list[Vector], int], float] | None = None,
) -> list[int]:
    """The template: return the indices of xs from best to worst.

    Sort by the rank of the chosen rule, then by larger density value
    (a larger value means a less crowded member), then by index.
    """
    ys = [tuple(f(x)) for x in xs]  # @line L1
    beats, beaten_by = dominance_lists(ys)  # @line L2
    r = RULES[rule](beats, beaten_by)  # @line L3
    d = [density(ys, i) if density else 0.0 for i in range(len(ys))]  # @line L4
    order = sorted(range(len(ys)), key=lambda i: (r[i], -d[i], i))  # @line L5
    return order  # @line L6
