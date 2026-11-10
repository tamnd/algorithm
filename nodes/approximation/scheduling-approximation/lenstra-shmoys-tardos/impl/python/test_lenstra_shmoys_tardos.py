# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lenstra-shmoys-tardos/. The authors are listed in prov/0P56MZ.jsonl.

import itertools
import random
from fractions import Fraction

from lenstra_shmoys_tardos import INF, least_feasible_T, lenstra_shmoys_tardos, lp_vertex, round_vertex


def loads(p, sigma):
    out = [0] * len(p)
    for j, i in enumerate(sigma):
        assert p[i][j] is not INF
        out[i] += p[i][j]
    return out


def brute_opt(p):
    """Least makespan by depth-first search with pruning."""
    m, n = len(p), len(p[0])
    best = [sum(min(p[i][j] for i in range(m) if p[i][j] is not INF) for j in range(n)) + 1]
    load = [0] * m

    def go(j):
        if j == n:
            best[0] = min(best[0], max(load))
            return
        for i in range(m):
            if p[i][j] is not INF and load[i] + p[i][j] < best[0]:
                load[i] += p[i][j]
                go(j + 1)
                load[i] -= p[i][j]

    go(0)
    return best[0]


def check_vertex(p, T, x):
    m, n = len(p), len(p[0])
    for j in range(n):
        assert sum(v for (i, jj), v in x.items() if jj == j) == 1
    for i in range(m):
        assert sum(p[i][j] * v for (ii, j), v in x.items() if ii == i) <= T
    for (i, j), v in x.items():
        assert v > 0 and p[i][j] is not INF and p[i][j] <= T
    # every connected component of the support has at most as many edges as nodes
    parent = {}

    def find(u):
        while parent.setdefault(u, u) != u:
            u = parent[u]
        return u

    for i, j in x:
        a, b = find(("m", i)), find(("j", j))
        if a != b:
            parent[a] = b
    nodes, edges = {}, {}
    for i, j in x:
        r = find(("j", j))
        edges[r] = edges.get(r, 0) + 1
    for u in list(parent):
        r = find(u)
        nodes[r] = nodes.get(r, 0) + 1
    for r, e in edges.items():
        assert e <= nodes[r]


def random_instance(rng, n, m, pinf):
    p = [[rng.randint(1, 9) if rng.random() > pinf else INF for _ in range(n)] for _ in range(m)]
    for j in range(n):
        if all(p[i][j] is INF for i in range(m)):
            p[rng.randrange(m)][j] = rng.randint(1, 9)
    return p


def test_small_example():
    p = [[2, 3, 4, 6], [3, 3, 2, 8], [5, 1, 4, 4]]
    sigma, T = lenstra_shmoys_tardos(p)
    assert lp_vertex(p, T - 1) is None and lp_vertex(p, T) is not None
    assert max(loads(p, sigma)) <= 2 * T
    assert T <= brute_opt(p)


def test_random_against_brute_force():
    rng = random.Random(1990)
    for _ in range(120):
        n, m = rng.randint(1, 6), rng.randint(1, 3)
        p = random_instance(rng, n, m, rng.choice([0.0, 0.3]))
        opt = brute_opt(p)
        T = least_feasible_T(p)
        assert T <= opt
        assert T == 0 or lp_vertex(p, T - 1) is None
        x = lp_vertex(p, T)
        check_vertex(p, T, x)
        sigma = round_vertex(x, n, m)
        frac = max((p[i][j] for (i, j), v in x.items() if v != 1), default=0)
        assert max(loads(p, sigma)) <= T + frac <= 2 * T <= 2 * opt


def test_identical_machines_lp_value():
    """For p_ij = p_j the LP is feasible exactly when max p_j <= T and sum p_j <= m T."""
    rng = random.Random(4)
    for _ in range(60):
        n, m = rng.randint(1, 5), rng.randint(1, 3)
        q = [rng.randint(1, 9) for _ in range(n)]
        p = [list(q) for _ in range(m)]
        want = max(max(q), -(-sum(q) // m))
        assert least_feasible_T(p) == want


def test_integrality_gap_instance():
    """One job of time m on every machine and a private job of time m - 1 on each machine."""
    for m in range(2, 5):
        p = [[m] + [m - 1 if k == i else INF for k in range(m)] for i in range(m)]
        sigma, T = lenstra_shmoys_tardos(p)
        assert T == m
        assert brute_opt(p) == 2 * m - 1
        assert max(loads(p, sigma)) <= 2 * m


def three_dm_instance(q, triples):
    """The reduction of Lenstra, Shmoys and Tardos: makespan 2 iff a perfect matching exists."""
    jobs = []
    for b in range(q):
        jobs.append([1 if t[1] == b else INF for t in triples])
    for c in range(q):
        jobs.append([1 if t[2] == c else INF for t in triples])
    for a in range(q):
        ta = sum(1 for t in triples if t[0] == a)
        for _ in range(ta - 1):
            jobs.append([2 if t[0] == a else INF for t in triples])
    return [[jobs[j][i] for j in range(len(jobs))] for i in range(len(triples))]


def has_perfect_matching(q, triples):
    for pick in itertools.combinations(triples, q):
        if all(len({t[k] for t in pick}) == q for k in range(3)):
            return True
    return False


def test_three_dm_reduction():
    rng = random.Random(7)
    seen = set()
    for _ in range(150):
        q = rng.randint(1, 3)
        allt = list(itertools.product(range(q), repeat=3))
        triples = rng.sample(allt, rng.randint(1, min(len(allt), q + 3)))
        if any(not any(t[k] == e for t in triples) for k in range(3) for e in range(q)):
            continue
        p = three_dm_instance(q, triples)
        opt = brute_opt(p)
        match = has_perfect_matching(q, triples)
        assert (opt == 2) == match
        assert opt >= 2
        seen.add(match)
        sigma, T = lenstra_shmoys_tardos(p)
        assert max(loads(p, sigma)) <= 2 * T <= 2 * opt
    assert seen == {True, False}


def test_edges():
    assert lenstra_shmoys_tardos([[5]]) == ([0], 5)
    assert lenstra_shmoys_tardos([[]]) == ([], 0)
    sigma, T = lenstra_shmoys_tardos([[1, INF], [INF, 1]])
    assert sigma == [0, 1] and T == 1
    x = lp_vertex([[Fraction(3)]], 2)
    assert x is None
