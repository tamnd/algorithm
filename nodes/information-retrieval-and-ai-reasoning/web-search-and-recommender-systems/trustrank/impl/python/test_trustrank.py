# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trustrank/. The authors are listed in prov/Y8VX0X.jsonl.

import random
from fractions import Fraction

import pytest

from trustrank import biased_pagerank, clean_links, inverse_pagerank, seed_vector, select_seeds, trustrank, trustrank_exact

ALPHA = Fraction(17, 20)

# The example graph of the page: good pages 0 to 3, spam pages 4 to 6.
N = 7
E = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6), (6, 4), (5, 4), (4, 0)]
GOOD = {0, 1, 2, 3}


def random_graph(rng: random.Random, n: int) -> list[tuple[int, int]]:
    return [(q, p) for q in range(n) for p in range(n) if rng.random() < 0.3]


def reachable(n: int, edges: list[tuple[int, int]], start: list[int]) -> set[int]:
    adj: dict[int, list[int]] = {}
    for q, p in clean_links(n, edges):
        adj.setdefault(q, []).append(p)
    seen, stack = set(start), list(start)
    while stack:
        q = stack.pop()
        for p in adj.get(q, []):
            if p not in seen:
                seen.add(p)
                stack.append(p)
    return seen


def test_example() -> None:
    inv = inverse_pagerank(N, E)
    assert sorted(range(N), key=lambda p: (-inv[p], p))[:3] == [4, 2, 1]
    t, seeds = trustrank(N, E, lambda p: p in GOOD, 3)
    assert seeds == [2, 1]
    exact = trustrank_exact(N, E, seeds)
    want = [0.2088, 0.2524, 0.2896, 0.1231, 0.0786, 0.0334, 0.0142]
    assert all(abs(float(x) - w) < 5e-5 for x, w in zip(exact, want))
    assert sum(exact) == 1
    assert sum(abs(a - float(b)) for a, b in zip(t, exact)) <= 2 * 0.85**20
    # Every good page has more trust than every spam page.
    assert min(exact[p] for p in GOOD) > max(exact[p] for p in range(N) if p not in GOOD)


def test_example_rounds_exact() -> None:
    d = seed_vector(N, [2, 1], exact=True)
    t1 = biased_pagerank(N, E, d, ALPHA, 1)
    assert t1 == [Fraction(17, 80), Fraction(3, 40), Fraction(1, 2), Fraction(17, 80), 0, 0, 0]


def test_fixed_point_is_exact() -> None:
    rng = random.Random(7)
    for _ in range(40):
        n = rng.randrange(1, 8)
        edges = random_graph(rng, n)
        seeds = sorted(rng.sample(range(n), rng.randrange(1, n + 1)))
        t = trustrank_exact(n, edges, seeds)
        d = seed_vector(n, seeds, exact=True)
        # t = alpha T t + (1 - alpha) d holds exactly.
        arcs = clean_links(n, edges)
        out = [0] * n
        for q, _ in arcs:
            out[q] += 1
        rhs = [(1 - ALPHA) * d[p] for p in range(n)]
        for q, p in arcs:
            rhs[p] += ALPHA * t[q] / out[q]
        assert rhs == t


def test_iteration_error_bound() -> None:
    # The L1 error after M rounds is at most alpha^M times |d - t*|, which is at most 2 alpha^M.
    rng = random.Random(11)
    for _ in range(40):
        n = rng.randrange(1, 9)
        edges = random_graph(rng, n)
        seeds = sorted(rng.sample(range(n), rng.randrange(1, n + 1)))
        exact = [float(x) for x in trustrank_exact(n, edges, seeds)]
        d = seed_vector(n, seeds)
        for m in (0, 1, 5, 20, 200):
            t = biased_pagerank(n, edges, d, 0.85, m)
            err = sum(abs(a - b) for a, b in zip(t, exact))
            assert err <= 2 * 0.85**m + 1e-12
        assert err <= 1e-9


def test_unreachable_pages_get_zero_and_trust_leaks() -> None:
    rng = random.Random(3)
    for _ in range(60):
        n = rng.randrange(1, 9)
        edges = random_graph(rng, n)
        seeds = sorted(rng.sample(range(n), rng.randrange(1, n + 1)))
        t = trustrank_exact(n, edges, seeds)
        reach = reachable(n, edges, seeds)
        assert all((t[p] > 0) == (p in reach) for p in range(n))
        out = {q for q, _ in clean_links(n, edges)}
        dangling_in_reach = any(p not in out for p in reach)
        assert (sum(t) < 1) == dangling_in_reach
        assert sum(t) <= 1


def test_dampening_and_leak_bound() -> None:
    # A page at link distance k from the seeds has trust at most alpha^k. A set S with no
    # seed holds at most alpha / (1 - alpha) times the trust that its in-links bring from outside.
    rng = random.Random(5)
    for _ in range(60):
        n = rng.randrange(2, 9)
        edges = random_graph(rng, n)
        seeds = sorted(rng.sample(range(n), rng.randrange(1, n)))
        t = trustrank_exact(n, edges, seeds)
        arcs = clean_links(n, edges)
        dist = {s: 0 for s in seeds}
        layer = list(seeds)
        while layer:
            nxt = []
            for q, p in arcs:
                if q in layer and p not in dist:
                    dist[p] = dist[q] + 1
                    nxt.append(p)
            layer = nxt
        for p, k in dist.items():
            assert t[p] <= ALPHA**k
        out = [0] * n
        for q, _ in arcs:
            out[q] += 1
        rest = [p for p in range(n) if p not in seeds]
        s = set(rng.sample(rest, rng.randrange(1, len(rest) + 1)))
        inflow = sum(t[q] / out[q] for q, p in arcs if p in s and q not in s)
        assert sum(t[p] for p in s) <= ALPHA / (1 - ALPHA) * inflow


def test_isolated_spam_farm_gets_no_trust() -> None:
    # A farm of k pages that all point to a target and back, with no link from a good page.
    for k in (1, 5, 30):
        n = 3 + 1 + k
        edges = [(0, 1), (1, 2), (2, 0), (3, 0)]
        edges += [(3, 4 + i) for i in range(k)] + [(4 + i, 3) for i in range(k)]
        t = trustrank_exact(n, edges, [0])
        assert all(t[p] == 0 for p in range(3, n))
        assert t[0] + t[1] + t[2] == 1


def test_links_are_cleaned() -> None:
    assert clean_links(3, [(0, 1), (0, 1), (1, 1), (2, 0)]) == [(0, 1), (2, 0)]
    with pytest.raises(ValueError):
        clean_links(2, [(0, 2)])
    a = trustrank_exact(3, [(0, 1), (0, 1), (1, 1), (1, 2), (2, 0)], [0])
    b = trustrank_exact(3, [(0, 1), (1, 2), (2, 0)], [0])
    assert a == b


def test_seed_selection() -> None:
    assert select_seeds([0.5, 0.5, 0.9, 0.1], lambda p: p != 2, 3) == [0, 1]
    assert select_seeds([0.5, 0.5, 0.9, 0.1], lambda p: True, 0) == []
    with pytest.raises(ValueError):
        trustrank(N, E, lambda p: False, 3)


def test_inverse_pagerank_is_pagerank_of_reversed_graph() -> None:
    rev = [(p, q) for q, p in E]
    assert inverse_pagerank(N, E, ALPHA, 6) == biased_pagerank(N, rev, [Fraction(1, N)] * N, ALPHA, 6)
