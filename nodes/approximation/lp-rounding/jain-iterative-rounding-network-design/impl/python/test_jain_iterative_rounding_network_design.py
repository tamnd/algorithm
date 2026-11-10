# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jain-iterative-rounding-network-design/. The authors are listed in prov/GSS56Z.jsonl.

import random
from fractions import Fraction
from itertools import combinations

import pytest

from jain_iterative_rounding_network_design import crosses, jain_iterative_rounding, lp_min, requirement


def meets(n, edges, sub, f):
    return all(sum(1 for e in sub if crosses(s, edges[e][0], edges[e][1])) >= need for s, need in f.items())


def brute_opt(n, edges, r):
    f = requirement(n, r)
    best = None
    for k in range(len(edges) + 1):
        for sub in combinations(range(len(edges)), k):
            cost = sum(edges[e][2] for e in sub)
            if (best is None or cost < best) and meets(n, edges, sub, f):
                best = cost
    return best


def rank(rows):
    m = [list(map(Fraction, r)) for r in rows]
    rk, col = 0, 0
    width = len(m[0]) if m else 0
    while rk < len(m) and col < width:
        p = next((i for i in range(rk, len(m)) if m[i][col] != 0), None)
        if p is None:
            col += 1
            continue
        m[rk], m[p] = m[p], m[rk]
        for i in range(len(m)):
            if i != rk and m[i][col] != 0:
                q = m[i][col] / m[rk][col]
                m[i] = [a - q * b for a, b in zip(m[i], m[rk])]
        rk, col = rk + 1, col + 1
    return rk


def cut_rows(n, edges, f):
    return [([1 if crosses(s, u, v) else 0 for u, v, _ in edges], need) for s, need in f.items() if need > 0]


def assert_vertex(n, edges, f, x):
    """The constraints that are tight at x have full rank |E|, so x is a vertex."""
    tight = [a for a, need in cut_rows(n, edges, f) if sum(ai * xi for ai, xi in zip(a, x)) == need]
    for k in range(len(edges)):
        if x[k] == 0 or x[k] == 1:
            tight.append([1 if q == k else 0 for q in range(len(edges))])
    assert rank(tight) == len(edges)


def check(n, edges, r):
    opt = brute_opt(n, edges, r)
    if opt is None:
        with pytest.raises(ValueError):
            jain_iterative_rounding(n, edges, r)
        return None
    chosen, rounds = jain_iterative_rounding(n, edges, r)
    assert len(set(chosen)) == len(chosen)
    assert meets(n, edges, chosen, requirement(n, r))
    alg = sum(edges[e][2] for e in chosen)
    lp = rounds[0][0] if rounds else 0
    assert lp <= opt and alg <= 2 * lp
    for (v, x), nxt in zip(rounds, rounds[1:] + [(Fraction(0), None)]):
        heavy = [e for e in x if x[e] >= Fraction(1, 2)]
        assert heavy  # Jain's theorem: a vertex has an edge with x_e >= 1/2
        assert nxt[0] <= v - sum(edges[e][2] * x[e] for e in heavy)
    return chosen, rounds, alg, opt


def random_instance(rng, n, max_edges):
    pool = list(combinations(range(n), 2))
    edges = [(u, v, rng.randint(1, 6)) for u, v in pool if rng.random() < 0.6]
    edges += [(u, v, rng.randint(1, 6)) for u, v in rng.sample(pool, 1)]  # one parallel edge
    edges = edges[:max_edges]
    r = {}
    for u, v in combinations(range(n), 2):
        if rng.random() < 0.4:
            r[(u, v)] = rng.randint(1, 2)
    return edges, r


def test_page_example():
    # vertices 0 .. 4; r = 1 for (0, 1) and (0, 2), r = 2 for (0, 3)
    edges = [(0, 1, 1), (1, 2, 1), (2, 0, 1), (2, 3, 2), (3, 4, 2), (4, 0, 2), (1, 3, 4)]
    r = {(0, 1): 1, (0, 2): 1, (0, 3): 2}
    chosen, rounds, alg, opt = check(5, edges, r)
    assert (alg, opt) == (12, 8)
    assert len(rounds) == 1 and rounds[0][0] == Fraction(15, 2)
    h = Fraction(1, 2)
    assert rounds[0][1] == {0: h, 1: 0, 2: 1, 3: 1, 4: h, 5: h, 6: h}
    assert sorted(chosen) == [0, 2, 3, 4, 5, 6]


def test_random_against_brute_force():
    rng = random.Random(2001)
    for _ in range(70):
        n = rng.randint(2, 5)
        edges, r = random_instance(rng, n, 7)
        check(n, edges, r)


def test_vertex_lemma_with_random_costs():
    rng = random.Random(42)
    hits = 0
    for _ in range(60):
        n = rng.randint(3, 5)
        edges, r = random_instance(rng, n, 7)
        f = requirement(n, r)
        rows = [(a, ">=", need) for a, need in cut_rows(n, edges, f)]
        rows += [([1 if q == k else 0 for q in range(len(edges))], "<=", 1) for k in range(len(edges))]
        cost = [rng.randint(0, 9) for _ in edges]
        sol = lp_min(cost, rows)
        if sol is None or not any(f.values()):
            continue  # the lemma needs some positive requirement
        x = sol[1]
        assert_vertex(n, edges, f, x)
        assert max(x) >= Fraction(1, 2)
        hits += any(0 < v < 1 for v in x)
    assert hits > 5


def test_odd_cycle_ratio_two_against_lp():
    # a spanning tree requirement on an odd cycle: the LP vertex is 1/2 on every edge
    for k in (3, 5, 7):
        edges = [(i, (i + 1) % k, 1) for i in range(k)]
        r = {(0, i): 1 for i in range(1, k)}
        chosen, rounds = jain_iterative_rounding(k, edges, r)
        assert rounds[0][0] == Fraction(k, 2)
        assert all(v == Fraction(1, 2) for v in rounds[0][1].values())
        assert sum(edges[e][2] for e in chosen) == k == 2 * rounds[0][0]


def test_no_requirement():
    assert jain_iterative_rounding(3, [(0, 1, 1)], {}) == ([], [])
