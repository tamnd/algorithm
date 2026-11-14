# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clock-skew-scheduling/. The authors are listed in prov/K3PCDZ.jsonl.

import random
from fractions import Fraction

from clock_skew_scheduling import constraint_edges, min_period


def simple_cycles(n, edges):
    """Every simple cycle of the multigraph, as a list of edge indices, each
    found once from its smallest node."""
    out = []
    adj = [[] for _ in range(n)]
    for k, (v, u, _, _) in enumerate(edges):
        adj[v].append((u, k))

    def dfs(start, v, seen, path):
        for u, k in adj[v]:
            if u == start:
                out.append(path + [k])
            elif u > start and u not in seen:
                seen.add(u)
                dfs(start, u, seen, path + [k])
                seen.discard(u)

    for s in range(n):
        dfs(s, s, {s}, [])
    return out


def exact_by_cycles(n, paths, ts, th):
    """The least period from the cycle condition: every cycle with k setup
    edges and constant part b needs k T + b >= 0."""
    edges = constraint_edges(n, paths, ts, th)
    best = None
    for cyc in simple_cycles(n, edges):
        k = sum(edges[e][2] for e in cyc)
        b = sum(edges[e][3] for e in cyc)
        if k == 0:
            if b < 0:
                return "infeasible"
        else:
            r = Fraction(-b, k)
            best = r if best is None or r > best else best
    return best


def negative_cycle_fw(n, paths, ts, th, T):
    """Independent test of a negative cycle at period T (Floyd-Warshall)."""
    INF = None
    d = [[INF] * n for _ in range(n)]
    for v, u, a, b in constraint_edges(n, paths, ts, th):
        w = a * T + b
        if d[v][u] is None or w < d[v][u]:
            d[v][u] = w
    for m in range(n):
        for i in range(n):
            if d[i][m] is None:
                continue
            for j in range(n):
                if d[m][j] is None:
                    continue
                w = d[i][m] + d[m][j]
                if d[i][j] is None or w < d[i][j]:
                    d[i][j] = w
    return any(d[i][i] is not None and d[i][i] < 0 for i in range(n))


def meets(paths, ts, th, T, c):
    return all(c[i] + dmax + ts <= c[j] + T and c[i] + dmin >= c[j] + th for i, j, dmax, dmin in paths)


def random_instance(rng, n, m):
    paths = []
    for _ in range(m):
        i, j = rng.randrange(n), rng.randrange(n)
        dmin = rng.randint(0, 6)
        paths.append((i, j, dmin + rng.randint(0, 6), dmin))
    return paths, rng.randint(0, 2), rng.randint(0, 2)


def test_against_cycle_enumeration(rng=random.Random(3141)):
    infeasible = 0
    for _ in range(400):
        n = rng.randint(1, 5)
        paths, ts, th = random_instance(rng, n, rng.randint(1, 7))
        want = exact_by_cycles(n, paths, ts, th)
        got = min_period(n, paths, ts, th)
        if want == "infeasible":
            assert got is None
            infeasible += 1
            continue
        T, c, _ = got
        assert T == want
        assert meets(paths, ts, th, T, c)
        assert min(c) == 0
        assert not negative_cycle_fw(n, paths, ts, th, T)
        assert negative_cycle_fw(n, paths, ts, th, T - Fraction(1, 1000))
    assert infeasible > 0


def test_grid_search_two_registers(rng=random.Random(27)):
    # with two registers a simple cycle has at most 2 setup edges, so the
    # optimum is a multiple of 1/2; search T and c_1 - c_0 on that grid
    for _ in range(60):
        paths, ts, th = random_instance(rng, 2, rng.randint(1, 4))
        got = min_period(2, paths, ts, th)
        bound = 2 * sum(dmax + ts + th + 1 for _, _, dmax, _ in paths)
        found = None
        for t2 in range(0, 2 * bound + 1):
            T = Fraction(t2, 2)
            for x2 in range(-2 * bound, 2 * bound + 1):
                if meets(paths, ts, th, T, [Fraction(0), Fraction(x2, 2)]):
                    found = T
                    break
            if found is not None:
                break
        if got is None:
            assert found is None
        else:
            assert got[0] == found


def test_zero_skew_period_is_an_upper_bound(rng=random.Random(5)):
    for _ in range(100):
        n = rng.randint(1, 5)
        paths, ts, th = random_instance(rng, n, rng.randint(1, 7))
        got = min_period(n, paths, ts, th)
        if got is None or any(dmin < th for _, _, _, dmin in paths):
            continue
        zero = max(dmax + ts for _, _, dmax, _ in paths)
        assert got[0] <= zero


def test_example_of_the_page():
    paths = [(0, 1, 9, 5), (1, 2, 3, 2), (2, 0, 4, 1), (0, 2, 6, 2)]
    T, c, rounds = min_period(3, paths, 1, 1)
    assert (T, c, rounds) == (Fraction(13, 2), [0, Fraction(7, 2), 1], 3)
    assert exact_by_cycles(3, paths, 1, 1) == T
    assert meets(paths, 1, 1, T, c)
    assert not meets(paths, 1, 1, Fraction(10) - Fraction(1, 100), [0, 0, 0])
    assert meets(paths, 1, 1, Fraction(10), [0, 0, 0])
