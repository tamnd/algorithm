# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-scheduling/. The authors are listed in prov/7BR0CN.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from greedy_scheduling import greedy_schedule, work_and_span


# ------------------------------------------------------------ DAG builders for the tests


class Builder:
    """Series-parallel parts as (sources, sinks) over a growing edge list."""

    def __init__(self) -> None:
        self.n = 0
        self.edges: list[tuple[int, int]] = []

    def strand(self) -> tuple[list[int], list[int]]:
        self.n += 1
        return [self.n - 1], [self.n - 1]

    def series(self, *parts):
        acc = parts[0]
        for b in parts[1:]:
            self.edges += [(u, v) for u in acc[1] for v in b[0]]
            acc = (acc[0], b[1])
        return acc

    def parallel(self, *parts):
        return [v for p in parts for v in p[0]], [v for p in parts for v in p[1]]

    def chain(self, k: int):
        return self.series(*[self.strand() for _ in range(k)])


def sum_dag(n: int) -> tuple[int, list]:
    b = Builder()

    def go(m):
        if m == 1:
            return b.strand()
        return b.series(b.strand(), b.parallel(go((m + 1) // 2), go(m // 2)), b.strand())

    go(n)
    return b.n, b.edges


def fib_dag(n: int) -> tuple[int, list]:
    b = Builder()

    def go(m):
        if m <= 1:
            return b.strand()
        return b.series(b.strand(), b.parallel(go(m - 1), go(m - 2)), b.strand())

    go(n)
    return b.n, b.edges


def merge_sort_dag(n: int) -> tuple[int, list]:
    """Merge sort with parallel calls and a serial merge (a chain of m strands)."""
    b = Builder()

    def go(m):
        if m == 1:
            return b.strand()
        return b.series(b.strand(), b.parallel(go((m + 1) // 2), go(m // 2)), b.chain(m))

    go(n)
    return b.n, b.edges


def random_sp_dag(rng: random.Random, size: int) -> tuple[int, list]:
    b = Builder()

    def go(s):
        if s <= 1 or rng.random() < 0.2:
            return b.chain(rng.randrange(1, 3))
        k = min(rng.randrange(2, 4), s)
        cuts = sorted(rng.sample(range(1, s), k - 1))
        sizes = [y - x for x, y in zip([0] + cuts, cuts + [s])]
        parts = [go(z) for z in sizes]
        return b.series(*parts) if rng.random() < 0.5 else b.parallel(*parts)

    go(size)
    return b.n, b.edges


def random_dag(rng: random.Random, n: int, prob: float) -> tuple[int, list]:
    perm = list(range(n))
    rng.shuffle(perm)
    edges = [(perm[i], perm[j]) for i in range(n) for j in range(i + 1, n) if rng.random() < prob]
    return n, edges


# ------------------------------------------------------------ oracles


def check_valid(n: int, edges: list, p: int, steps: list[list[int]]) -> None:
    when = {}
    for t, run in enumerate(steps):
        assert 1 <= len(run) <= p
        for v in run:
            assert v not in when
            when[v] = t
    assert sorted(when) == list(range(n))
    for u, v in edges:
        assert when[u] < when[v]


def check_greedy(n: int, edges: list, p: int, steps: list[list[int]]) -> None:
    """At each step, either p strands run or every ready strand runs."""
    preds = [set() for _ in range(n)]
    for u, v in edges:
        preds[v].add(u)
    done: set[int] = set()
    for run in steps:
        ready = {v for v in range(n) if v not in done and preds[v] <= done}
        assert set(run) <= ready
        assert len(run) == min(p, len(ready))
        done |= set(run)


def optimal_length(n: int, edges: list, p: int, greedy_only: bool = False) -> int:
    """Shortest schedule by breadth-first search over the sets of finished strands."""
    pred_mask = [0] * n
    for u, v in edges:
        pred_mask[v] |= 1 << u
    full = (1 << n) - 1
    frontier, seen, t = {0}, {0}, 0
    while full not in frontier:
        t += 1
        nxt = set()
        for done in frontier:
            ready = [v for v in range(n) if not done >> v & 1 and pred_mask[v] & done == pred_mask[v]]
            sizes = [min(p, len(ready))] if greedy_only else range(1, min(p, len(ready)) + 1)
            for k in sizes:
                for sub in itertools.combinations(ready, k):
                    m = done
                    for v in sub:
                        m |= 1 << v
                    if m not in seen:
                        seen.add(m)
                        nxt.add(m)
        frontier = nxt
    return t


def check_bounds(n: int, edges: list, p: int, steps: list[list[int]]) -> None:
    w, s = work_and_span(n, edges)
    tp = len(steps)
    assert tp >= s and p * tp >= w  # span law and work law
    assert p * tp <= (w - s) + p * s  # T_p <= (W - S)/p + S
    assert tp <= Fraction(w, p) + s  # T_p <= W/p + S


# ------------------------------------------------------------ tests


def test_example_of_the_page() -> None:
    # Fork-join sum of 4 numbers, 10 strands: W = 10, S = 5.
    n, edges = sum_dag(4)
    assert work_and_span(n, edges) == (10, 5)
    steps = greedy_schedule(n, edges, 2)
    check_valid(n, edges, 2, steps)
    check_greedy(n, edges, 2, steps)
    assert len(steps) == 6
    assert optimal_length(n, edges, 2) == 6


def test_edges_cases() -> None:
    assert greedy_schedule(0, [], 3) == []
    assert greedy_schedule(1, [], 3) == [[0]]
    with pytest.raises(ValueError):
        greedy_schedule(2, [], 0)
    with pytest.raises(ValueError):
        greedy_schedule(2, [(0, 1), (1, 0)], 2)
    n, edges = fib_dag(6)
    w, s = work_and_span(n, edges)
    assert len(greedy_schedule(n, edges, 1)) == w
    assert len(greedy_schedule(n, edges, n)) == s


def test_fork_join_programs() -> None:
    rng = random.Random(4)
    dags = [sum_dag(k) for k in (1, 2, 3, 7, 16, 33)]
    dags += [fib_dag(k) for k in (0, 1, 2, 5, 9)]
    dags += [merge_sort_dag(k) for k in (1, 2, 5, 8, 13)]
    for n, edges in dags:
        for p in (1, 2, 3, 4, 8, 64):
            for trial in range(5):
                steps = greedy_schedule(n, edges, p, rng=rng if trial else None)
                check_valid(n, edges, p, steps)
                check_greedy(n, edges, p, steps)
                check_bounds(n, edges, p, steps)


def test_random_dags_large() -> None:
    rng = random.Random(8)
    for _ in range(300):
        if rng.random() < 0.5:
            n, edges = random_sp_dag(rng, rng.randrange(1, 60))
        else:
            n, edges = random_dag(rng, rng.randrange(0, 60), rng.choice([0.02, 0.1, 0.3]))
        p = rng.randrange(1, 9)
        steps = greedy_schedule(n, edges, p, rng=rng)
        check_valid(n, edges, p, steps)
        check_greedy(n, edges, p, steps)
        check_bounds(n, edges, p, steps)


def test_factor_two_against_brute_force() -> None:
    rng = random.Random(1)
    for _ in range(500):
        if rng.random() < 0.5:
            n, edges = random_sp_dag(rng, rng.randrange(1, 7))
            if n > 9:
                continue
        else:
            n, edges = random_dag(rng, rng.randrange(1, 9), rng.choice([0.1, 0.25, 0.5]))
        p = rng.randrange(1, 4)
        t_opt = optimal_length(n, edges, p)
        w, s = work_and_span(n, edges)
        assert t_opt >= max(-(-w // p), s)
        assert optimal_length(n, edges, p, greedy_only=True) == t_opt
        for _ in range(3):
            steps = greedy_schedule(n, edges, p, rng=rng)
            tp = len(steps)
            check_valid(n, edges, p, steps)
            check_bounds(n, edges, p, steps)
            assert tp <= 2 * t_opt
            assert p * tp <= (2 * p - 1) * t_opt  # T_p <= (2 - 1/p) T_opt


def test_bad_tie_breaking_is_nearly_twice_optimal() -> None:
    # A chain of k strands and p*k independent strands; the independent ones go first.
    for p in (2, 3, 4):
        for k in (1, 2, 4, 8):
            n = k + p * k
            edges = [(i, i + 1) for i in range(k - 1)]
            bad = greedy_schedule(n, edges, p, priority=lambda v: (v < k, v))
            good = greedy_schedule(n, edges, p, priority=lambda v: (v >= k, v))
            w, s = work_and_span(n, edges)
            assert len(bad) == 2 * k == (w - s) // p + s
            assert len(good) == k + -(-k // p)
            if n <= 12:
                assert optimal_length(n, edges, p) == len(good)
