# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-partitioning/. The authors are listed in prov/VACAVK.jsonl.

import math
import random
from fractions import Fraction
from itertools import combinations

from spectral_partitioning import cut_weight, fiedler_vector, laplacian, spectral_partitioning

TOL = 1e-6  # tolerance for eigenvalue comparisons (the solver stops at residual 1e-10)


def jacobi_eigenvalues(a: list[list[float]]) -> list[float]:
    """All eigenvalues of a symmetric matrix by cyclic Jacobi rotations (the reference)."""
    n = len(a)
    a = [row[:] for row in a]
    for _ in range(100):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-22:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = (1 if theta >= 0 else -1) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = c * akp - s * akq
                    a[k][q] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = c * apk - s * aqk
                    a[q][k] = s * apk + c * aqk
    return sorted(a[i][i] for i in range(n))


def exact_cut(edges, side) -> Fraction:
    return sum((Fraction(w) for u, v, w in edges if side[u] != side[v]), Fraction(0))


def min_bisection(n, edges) -> Fraction:
    best = None
    for s in combinations(range(n), n // 2):
        side = [1] * n
        for v in s:
            side[v] = 0
        c = exact_cut(edges, side)
        best = c if best is None or c < best else best
    return best


def min_ratio_cut(n, edges) -> Fraction:
    best = None
    for mask in range(1, (1 << n) - 1):
        if mask & 1 == 0:
            continue
        side = [0 if mask >> v & 1 else 1 for v in range(n)]
        a = side.count(0)
        r = exact_cut(edges, side) / (a * (n - a))
        best = r if best is None or r < best else best
    return best


def random_graph(rng: random.Random, n: int, p: float) -> list[tuple[int, int, int]]:
    return [(u, v, rng.randint(1, 3)) for u, v in combinations(range(n), 2) if rng.random() < p]


def two_triangles():
    a, b, c, d, e, f = range(6)
    return [(a, b, 1), (a, c, 1), (b, c, 1), (d, e, 1), (d, f, 1), (e, f, 1), (c, d, 1), (b, e, 1)]


def test_page_example():
    edges = two_triangles()
    lam, x, res = fiedler_vector(6, edges, random.Random(1))
    assert res <= 1e-10 and abs(lam - 1.0) < TOL
    side = spectral_partitioning(6, edges, random.Random(1))
    assert side[0] == side[1] == side[2] != side[3] == side[4] == side[5]
    assert exact_cut(edges, side) == 2 == min_bisection(6, edges)
    side = spectral_partitioning(6, edges, random.Random(1), mode="ratio")
    assert exact_cut(edges, side) / 9 == Fraction(2, 9) == min_ratio_cut(6, edges)


def test_path_and_cycle_eigenvalues():
    for n in range(2, 10):
        path = [(i, i + 1, 1) for i in range(n - 1)]
        lam, _, _ = fiedler_vector(n, path, random.Random(n))
        assert abs(lam - 2 * (1 - math.cos(math.pi / n))) < TOL
        side = spectral_partitioning(n, path, random.Random(n))
        assert cut_weight(path, side) == 1  # a path splits at its middle edge
    for n in range(3, 10):
        cyc = [(i, (i + 1) % n, 1) for i in range(n)]
        lam, _, _ = fiedler_vector(n, cyc, random.Random(n))
        assert abs(lam - 2 * (1 - math.cos(2 * math.pi / n))) < TOL


def test_disconnected_graph_has_zero_lambda2():
    edges = [(0, 1, 1), (1, 2, 1), (0, 2, 1), (3, 4, 1), (4, 5, 1), (3, 5, 1)]
    lam, _, _ = fiedler_vector(6, edges, random.Random(3))
    assert abs(lam) < TOL
    side = spectral_partitioning(6, edges, random.Random(3))
    assert exact_cut(edges, side) == 0


def test_small_cases():
    assert spectral_partitioning(2, [(0, 1, 1)], random.Random(0)) in ([0, 1], [1, 0])
    side = spectral_partitioning(3, [], random.Random(0))
    assert side.count(0) == 1


def roach(k: int) -> tuple[int, list[tuple[int, int, int]]]:
    """Guattery and Miller's roach graph: two paths of 2k vertices, rungs on the first k."""
    edges = []
    for i in range(2 * k - 1):
        edges.append((i, i + 1, 1))
        edges.append((2 * k + i, 2 * k + i + 1, 1))
    edges += [(i, 2 * k + i, 1) for i in range(k)]
    return 4 * k, edges


def test_roach_graph_defeats_the_median_split():
    for k in (3, 4):
        n, edges = roach(k)
        side = spectral_partitioning(n, edges, random.Random(1))
        assert exact_cut(edges, side) == k  # the rungs: upper path against lower path
        assert min_bisection(n, edges) == 2  # cut both paths in the middle
        side = spectral_partitioning(n, edges, random.Random(1), mode="ratio")
        assert exact_cut(edges, side) == 1  # the sweep cuts off one antenna


def test_random_graphs_against_brute_force():
    rng = random.Random(2026)
    for trial in range(120):
        n = rng.randint(3, 10)
        edges = random_graph(rng, n, rng.choice([0.3, 0.5, 0.8]))
        if not edges:
            continue
        lam, x, res = fiedler_vector(n, edges, random.Random(trial))
        ref = jacobi_eigenvalues(laplacian(n, edges))
        assert abs(ref[0]) < TOL
        if res <= 1e-10:
            assert abs(lam - ref[1]) < TOL
        assert lam >= ref[1] - TOL  # a unit vector orthogonal to 1 has Rayleigh quotient >= lambda2
        assert abs(sum(x)) < 1e-9 and abs(sum(t * t for t in x) - 1) < 1e-9
        # Bisection: balanced, cut computed right, never below the optimum,
        # and the optimum is at least n lambda2 / 4.
        side = spectral_partitioning(n, edges, random.Random(trial))
        assert side.count(0) == n // 2
        c = exact_cut(edges, side)
        assert abs(float(c) - cut_weight(edges, side)) < 1e-9
        best = min_bisection(n, edges)
        assert c >= best
        if n % 2 == 0:
            assert float(best) >= n * ref[1] / 4 - TOL
        # Ratio cut sweep: never below the optimum, and the optimum is at
        # least lambda2 / n (Hagen and Kahng).
        side = spectral_partitioning(n, edges, random.Random(trial), mode="ratio")
        a = side.count(0)
        assert 0 < a < n
        r = exact_cut(edges, side) / (a * (n - a))
        best_r = min_ratio_cut(n, edges)
        assert r >= best_r
        assert float(best_r) >= ref[1] / n - TOL
