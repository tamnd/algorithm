# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-bipartite-matching-binding/. The authors are listed in prov/6HS42N.jsonl.

import itertools
import random

from weighted_bipartite_matching_binding import (connections, hungarian_max, is_valid, matching_bind,
                                                 max_live, pair_weight)

# The counterexample of the page: values a, b, c, d as (birth, death, unit, ports).
COUNTER = [(0, 0, 0, frozenset({0, 2})), (1, 1, 1, frozenset({2})),
           (1, 3, 0, frozenset({0, 1})), (2, 2, 0, frozenset({0, 1}))]


def random_values(rng: random.Random, n: int) -> list:
    """n values with lifetimes in a short horizon, 2 units and 3 ports."""
    horizon = rng.randint(2, 5)
    out = []
    for _ in range(n):
        b = rng.randrange(horizon)
        e = rng.randrange(b, horizon)
        ports = frozenset(rng.sample(range(3), rng.randint(1, 2)))
        out.append((b, e, rng.randrange(2), ports))
    return out


def conflict(x, y) -> bool:
    return not (x[1] < y[0] or y[1] < x[0])


def all_bindings(values: list, k: int):
    """Every map of the values to registers 0, ..., k - 1 with no two conflicting values together."""
    n = len(values)

    def rec(i: int, where: list[int], used: int):
        if i == n:
            yield list(where)
            return
        for r in range(min(used + 1, k)):
            if all(not (where[j] == r and conflict(values[j], values[i])) for j in range(i)):
                where.append(r)
                yield from rec(i + 1, where, max(used, r + 1))
                where.pop()

    yield from rec(0, [], 0)


def least_registers(values: list) -> int:
    """The least number of registers, by trying k = 1, 2, ... with every binding."""
    k = 0
    while True:
        if next(all_bindings(values, k), None) is not None:
            return k
        k += 1


def best_matching_weight(weight: list[list[int]]) -> int:
    """The largest weight of a matching that places every row, over all injective maps."""
    n = len(weight)
    m = len(weight[0]) if n else 0
    return max(sum(weight[a][c] for a, c in enumerate(cols))
               for cols in itertools.permutations(range(m), n))


def test_counterexample():
    trace: list = []
    where = matching_bind(COUNTER, trace)
    assert where == [0, 1, 0, 1]
    assert connections(COUNTER, where) == 9
    assert trace[1] == (1, [1, 2], [0, 1], [[1, 0], [2, 0]], [1, 0])
    best = min(connections(COUNTER, w) for w in all_bindings(COUNTER, 2))
    assert best == 8
    assert connections(COUNTER, [0, 0, 1, 0]) == 8


def test_hungarian_against_all_injective_maps():
    rng = random.Random(5)
    for _ in range(600):
        n = rng.randint(1, 4)
        m = rng.randint(n, 5)
        w = [[rng.randint(0, 4) for _ in range(m)] for _ in range(n)]
        cols = hungarian_max(w)
        assert len(set(cols)) == n
        assert sum(w[a][c] for a, c in enumerate(cols)) == best_matching_weight(w)


def test_each_step_is_optimal_for_its_step():
    rng = random.Random(6)
    for _ in range(500):
        values = random_values(rng, rng.randint(1, 7))
        trace: list = []
        where = matching_bind(values, trace)
        srcs: dict[int, set] = {}
        ports: dict[int, set] = {}
        for t, new, free, w, cols in trace:
            for a, k in enumerate(new):
                for c, r in enumerate(free):
                    assert w[a][c] == pair_weight(values[k], srcs.get(r, set()), ports.get(r, set()))
            assert sum(w[a][c] for a, c in enumerate(cols)) == best_matching_weight(w)
            for a, k in enumerate(new):
                r = free[cols[a]]
                assert where[k] == r
                srcs.setdefault(r, set()).add(values[k][2])
                ports.setdefault(r, set()).update(values[k][3])


def test_register_count_and_measured_cost():
    rng = random.Random(8)
    gaps: dict[int, int] = {}
    for _ in range(500):
        values = random_values(rng, rng.randint(1, 6))
        where = matching_bind(values, None)
        assert is_valid(values, where)
        k = len(set(where))
        assert k == max_live(values) == least_registers(values)
        best = min(connections(values, w) for w in all_bindings(values, k))
        gap = connections(values, where) - best
        assert gap >= 0
        gaps[gap] = gaps.get(gap, 0) + 1
    assert gaps == {0: 479, 1: 16, 2: 5}
