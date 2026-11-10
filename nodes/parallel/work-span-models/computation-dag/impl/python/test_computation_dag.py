# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/computation-dag/. The authors are listed in prov/54BC6D.jsonl.

import math
import random
from collections import Counter
from functools import lru_cache

import pytest

from computation_dag import (
    ComputationDag,
    ForkJoinTracer,
    Part,
    chain,
    p_fib,
    p_sum,
    parallel,
    series,
    sp_fib,
    sp_merge_sort_serial_merge,
    sp_p_merge,
    sp_p_merge_sort,
    sp_sum,
    strand,
)


def clg(n: int) -> int:
    return (n - 1).bit_length()  # ceil(lg n) for n >= 1


def fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def brute_span(dag: ComputationDag) -> int:
    """Longest path by plain recursion over all paths (small graphs only)."""
    n = dag.num_strands()

    def longest_from(u: int) -> int:
        return 1 + max((longest_from(v) for v in dag.succ[u]), default=0)

    return max((longest_from(u) for u in range(n)), default=0)


# ------------------------------------------------------------ the data structure


def test_empty_and_single() -> None:
    d = ComputationDag()
    assert d.work_and_span() == (0, 0)
    assert d.critical_path() == []
    d.add_strand()
    assert d.work_and_span() == (1, 1)
    assert d.critical_path() == [0]


def test_chain_and_antichain() -> None:
    d = ComputationDag()
    vs = [d.add_strand() for _ in range(6)]
    for u, v in zip(vs, vs[1:]):
        d.add_edge(u, v)
    assert d.work_and_span() == (6, 6)
    e = ComputationDag()
    for _ in range(6):
        e.add_strand()
    assert e.work_and_span() == (6, 1)


def test_cycle_is_rejected() -> None:
    d = ComputationDag()
    a, b, c = d.add_strand(), d.add_strand(), d.add_strand()
    d.add_edge(a, b)
    d.add_edge(b, c)
    d.add_edge(c, a)
    with pytest.raises(ValueError):
        d.work_and_span()
    with pytest.raises(ValueError):
        d.add_edge(a, a)
    with pytest.raises(ValueError):
        d.add_edge(a, b, "fork")


def test_repeated_edge_is_ignored() -> None:
    d = ComputationDag()
    a, b = d.add_strand(), d.add_strand()
    d.add_edge(a, b)
    d.add_edge(a, b)
    assert d.num_edges() == 1
    d.check_invariant()


def test_random_dags_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(500):
        n = rng.randrange(0, 11)
        d = ComputationDag()
        for _ in range(n):
            d.add_strand()
        perm = list(range(n))
        rng.shuffle(perm)  # edges go forward in a hidden random order
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < 0.3:
                    d.add_edge(perm[i], perm[j], rng.choice(["continuation", "spawn", "call", "return"]))
        d.check_invariant()
        w, s = d.work_and_span()
        assert w == n
        assert s == brute_span(d)
        path = d.critical_path()
        assert len(path) == s
        for u, v in zip(path, path[1:]):
            assert v in d.succ[u]
        order = d.topological_order()
        pos = {v: i for i, v in enumerate(order)}
        assert all(pos[u] < pos[v] for (u, v) in d.kind)


# ------------------------------------------------------------ the CLRS tracer


def test_p_fib_4_matches_clrs_figure() -> None:
    t = ForkJoinTracer()
    assert t.run(p_fib, 4) == 3
    t.dag.check_invariant()
    assert t.dag.work_and_span() == (17, 8)
    kinds = Counter(t.dag.kind.values())
    assert kinds == {"spawn": 4, "call": 4, "continuation": 4, "return": 8}


@lru_cache(maxsize=None)
def pfib_ws(n: int) -> tuple[int, int]:
    """Work and span of P-FIB(n) from its structure: a -> (fib(n-1) || u' -> fib(n-2)) -> w."""
    if n <= 1:
        return 1, 1
    w1, s1 = pfib_ws(n - 1)
    w2, s2 = pfib_ws(n - 2)
    return w1 + w2 + 3, 2 + max(s1, 1 + s2)


def test_p_fib_many_n() -> None:
    for n in range(0, 16):
        t = ForkJoinTracer()
        assert t.run(p_fib, n) == fib(n)
        w, s = t.dag.work_and_span()
        assert (w, s) == pfib_ws(n)
        assert w == 4 * fib(n + 1) - 3
        assert s == (2 * n if n >= 2 else 1)


def test_p_sum_tracer() -> None:
    rng = random.Random(3)
    for n in list(range(1, 40)) + [64, 100, 128]:
        a = [rng.randrange(-100, 100) for _ in range(n)]
        t = ForkJoinTracer()
        assert t.run(p_sum, a, 0, n) == sum(a)
        w, s = t.dag.work_and_span()
        assert w == 4 * n - 3
        assert s <= 3 * clg(n) + 1
        if n & (n - 1) == 0:
            assert s == 3 * clg(n) + 1


def test_tracer_serial_steps() -> None:
    def serial(t: ForkJoinTracer, k: int) -> None:
        for _ in range(k):
            t.step()

    for k in range(0, 10):
        t = ForkJoinTracer()
        t.run(serial, k)
        assert t.dag.work_and_span() == (k + 1, k + 1)


# ------------------------------------------------------------ series-parallel composition


def random_sp(dag: ComputationDag, rng: random.Random, size: int) -> Part:
    if size <= 1 or rng.random() < 0.15:
        return chain(dag, rng.randrange(1, 4))
    k = rng.randrange(2, 4)
    cuts = sorted(rng.sample(range(1, size), min(k - 1, size - 1)))
    sizes = [b - a for a, b in zip([0] + cuts, cuts + [size])]
    parts = [random_sp(dag, rng, s) for s in sizes]
    return series(dag, *parts) if rng.random() < 0.5 else parallel(dag, *parts)


def test_composition_rules_on_random_sp_dags() -> None:
    rng = random.Random(11)
    for _ in range(400):
        d = ComputationDag()
        p = random_sp(d, rng, rng.randrange(1, 30))
        d.check_invariant()
        assert d.work_and_span() == (p.work, p.span)
        if d.num_strands() <= 40:
            assert brute_span(d) == p.span


def test_series_and_parallel_of_two() -> None:
    rng = random.Random(5)
    for _ in range(200):
        d = ComputationDag()
        a = random_sp(d, rng, rng.randrange(1, 12))
        b = random_sp(d, rng, rng.randrange(1, 12))
        wa, sa, wb, sb = a.work, a.span, b.work, b.span
        both = parallel(d, series(d, a, b), strand(d))
        assert d.work_and_span() == (both.work, both.span) == (wa + wb + 1, max(sa + sb, 1))


def test_sp_sum_closed_form() -> None:
    for n in list(range(1, 200)) + [1000, 1024, 1025]:
        d = ComputationDag()
        p = sp_sum(d, n)
        assert d.work_and_span() == (p.work, p.span) == (3 * n - 2, 2 * clg(n) + 1)


def test_sp_fib_closed_form() -> None:
    for n in range(0, 20):
        d = ComputationDag()
        p = sp_fib(d, n)
        assert d.work_and_span() == (p.work, p.span)
        assert p.work == 3 * fib(n + 1) - 2
        assert p.span == (2 * n - 1 if n >= 1 else 1)


def test_merge_sort_with_serial_merge() -> None:
    for n in list(range(1, 130)) + [1000]:
        d = ComputationDag()
        p = sp_merge_sort_serial_merge(d, n)
        w, s = d.work_and_span()
        assert (w, s) == (p.work, p.span)
        c = clg(n)
        assert w == n * c - 2**c + 3 * n - 1
        if n & (n - 1) == 0:
            assert s == 2 * n + c - 1
        assert 2 * n - 1 <= s <= 2 * n + 2 * c + 1


def test_p_merge_is_correct_and_cheap() -> None:
    rng = random.Random(2)
    for _ in range(300):
        n1, n2 = rng.randrange(0, 60), rng.randrange(0, 60)
        x = sorted(rng.randrange(50) for _ in range(n1))
        y = sorted(rng.randrange(50) for _ in range(n2))
        t = x + y
        out = [None] * (n1 + n2)
        d = ComputationDag()
        p = sp_p_merge(d, t, 0, n1, n1, n1 + n2, out, 0)
        assert out == sorted(t)
        n = n1 + n2
        assert d.work_and_span() == (p.work, p.span)
        assert p.work <= 6 * n + 1
        assert p.span <= 3 * (math.log2(n + 1) ** 2) + 4 * math.log2(n + 1) + 2


def test_p_merge_sort() -> None:
    rng = random.Random(9)
    sizes = list(range(1, 40)) + [64, 100, 256, 500, 1024]
    for n in sizes:
        a = [rng.randrange(1000) for _ in range(n)]
        out = [None] * n
        d = ComputationDag()
        p = sp_p_merge_sort(d, a, 0, n, out, 0)
        assert out == sorted(a)
        w, s = d.work_and_span()
        assert (w, s) == (p.work, p.span)
        lg = math.log2(n) if n > 1 else 0.0
        assert w <= 7 * n * lg + 2 * n
        assert s <= 2 * lg**3 + 4 * lg**2 + 6 * lg + 2


# ------------------------------------------------------------ the recurrences with constants


def test_recurrence_polylog_span() -> None:
    # S(2^k) = S(2^(k-1)) + k^2, S(1) = 1 has S(2^k) = 1 + k(k+1)(2k+1)/6.
    s = 1
    for k in range(1, 64):
        s += k * k
        assert s == 1 + k * (k + 1) * (2 * k + 1) // 6
        assert k**3 / 3 <= s <= k**3 / 3 + k**2 + 1


def test_recurrence_three_quarters() -> None:
    # S(n) = S(floor(3n/4)) + ceil(lg n) + 1, S(1) = 1 is at most lg^2 n / (2 lg(4/3)) + 6 lg n + 3.
    c = 1 / (2 * math.log2(4 / 3))

    @lru_cache(maxsize=None)
    def s(n: int) -> int:
        return 1 if n <= 1 else s(3 * n // 4) + clg(n) + 1

    for n in list(range(1, 3000)) + [10**5, 10**6]:
        lg = math.log2(n)
        assert s(n) <= c * lg * lg + 6 * lg + 3


def test_recurrence_serial_merge_span() -> None:
    # S(n) = S(ceil(n/2)) + n + 1 with S(1) = 1 is Theta(n): 2n - 1 <= S(n) <= 2n + 2 ceil(lg n) + 1.
    @lru_cache(maxsize=None)
    def s(n: int) -> int:
        return 1 if n == 1 else s((n + 1) // 2) + n + 1

    for n in range(1, 5000):
        assert 2 * n - 1 <= s(n) <= 2 * n + 2 * clg(n) + 1
