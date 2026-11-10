# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shmoys-tardos-gap/. The authors are listed in prov/6ZNFNM.jsonl.

import random
from fractions import Fraction
from itertools import product

from shmoys_tardos_gap import lp_min, min_cost_job_matching, shmoys_tardos_gap


def brute(p, c, t):
    """Least cost of an assignment with every load at most t, or None."""
    m, n = len(p), len(p[0])
    best = None
    for a in product(range(m), repeat=n):
        loads = [0] * m
        for j, i in enumerate(a):
            loads[i] += p[i][j]
        if max(loads) <= t:
            cost = sum(c[i][j] for j, i in enumerate(a))
            if best is None or cost < best:
                best = cost
    return best


def is_pseudo_forest(m, n, x):
    """Each component of the support graph (machines and jobs) has at most as many edges as vertices."""
    parent = list(range(m + n))

    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u

    edges = [(i, m + j) for i in range(m) for j in range(n) if x[i][j] > 0]
    for u, v in edges:
        parent[find(u)] = find(v)
    nv, ne = {}, {}
    for u in range(m + n):
        nv[find(u)] = nv.get(find(u), 0) + 1
    for u, v in edges:
        ne[find(u)] = ne.get(find(u), 0) + 1
    return all(ne.get(r, 0) <= nv[r] for r in nv)


def check(p, c, t, use_brute=True):
    m, n = len(p), len(p[0])
    opt = brute(p, c, t) if use_brute else None
    res = shmoys_tardos_gap(p, c, t)
    if res is None:
        assert opt is None
        return None
    assign, lp, x = res
    for j in range(n):
        assert sum(x[i][j] for i in range(m)) == 1
    for i in range(m):
        assert sum(p[i][j] * x[i][j] for j in range(n)) <= t
    assert is_pseudo_forest(m, n, x)
    if opt is not None:
        assert lp <= opt
    cost = sum(c[assign[j]][j] for j in range(n))
    assert cost <= lp
    for i in range(m):
        load = sum(p[i][j] for j in range(n) if assign[j] == i)
        pmax = max([p[i][j] for j in range(n) if x[i][j] > 0], default=0)
        assert load <= t + pmax <= 2 * t
        for j in range(n):
            if assign[j] == i:
                assert x[i][j] > 0 and p[i][j] <= t
    return assign, lp, cost


def test_page_example():
    p = [[2, 1, 2, 4], [3, 2, 4, 2]]
    c = [[0, 1, 4, 4], [3, 1, 1, 0]]
    assign, lp, cost = check(p, c, 4)
    assert lp == Fraction(7, 2) and cost == 2 and assign == [0, 0, 1, 1]
    h = Fraction(1, 2)
    assert shmoys_tardos_gap(p, c, 4)[2] == [[1, 1, h, 0], [0, 0, h, 1]]
    assert brute(p, c, 4) == 5 and brute(p, c, 8) == 2


def test_lp_min_small():
    val, x = lp_min([1, 1], [([1, 2], ">=", 2), ([3, 1], ">=", 3)])
    assert val == Fraction(7, 5) and x == [Fraction(4, 5), Fraction(3, 5)]
    assert lp_min([1], [([1], "<=", -1)]) is None


def test_matching_small():
    edges = [(0, 0, 5), (0, 1, 1), (1, 1, 1), (1, 2, 4), (2, 0, 1)]
    s = min_cost_job_matching(3, 3, edges)
    assert sorted(s) == [0, 1, 2] and s == [1, 2, 0]
    assert min_cost_job_matching(2, 1, [(0, 0, 1), (1, 0, 1)]) is None


def test_random_against_brute_force():
    rng = random.Random(1993)
    feasible = 0
    for _ in range(600):
        m, n = rng.randint(1, 3), rng.randint(1, 5)
        p = [[rng.randint(1, 6) for _ in range(n)] for _ in range(m)]
        c = [[rng.randint(0, 6) for _ in range(n)] for _ in range(m)]
        t = rng.randint(2, 12)
        if check(p, c, t) is not None:
            feasible += 1
    assert feasible > 250


def test_matching_against_brute_force():
    rng = random.Random(7)
    for _ in range(300):
        nj, ns = rng.randint(1, 4), rng.randint(1, 5)
        edges = [(j, s, rng.randint(0, 9)) for j in range(nj) for s in range(ns) if rng.random() < 0.6]
        w = {(j, s): cost for j, s, cost in edges}
        best = None
        for a in product(range(ns), repeat=nj):
            if len(set(a)) == nj and all((j, a[j]) in w for j in range(nj)):
                v = sum(w[(j, a[j])] for j in range(nj))
                best = v if best is None or v < best else best
        got = min_cost_job_matching(nj, ns, edges)
        if best is None:
            assert got is None
        else:
            assert len(set(got)) == nj and sum(w[(j, got[j])] for j in range(nj)) == best


def test_tight_family_makespan_two_t():
    # one job of length k on every machine, and k - 1 unit jobs fixed to each machine
    for k in (2, 3, 4):
        n = 1 + k * (k - 1)
        big = 10 ** 6
        p = [[k] + [1 if (j - 1) // (k - 1) == i else big for j in range(1, n)] for i in range(k)]
        c = [[0] * n for _ in range(k)]
        assign, lp, cost = check(p, c, k, use_brute=False)
        loads = [sum(p[i][j] for j in range(n) if assign[j] == i) for i in range(k)]
        # each integral schedule puts the long job on top of k - 1 unit jobs
        assert max(loads) == 2 * k - 1
