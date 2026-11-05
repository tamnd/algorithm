# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hits-algorithm/. The authors are listed in prov/AJD47V.jsonl.

import math
import random

from hits_algorithm import hits_algorithm


def jacobi_eigen(m: list[list[float]]) -> tuple[list[float], list[list[float]]]:
    """Eigenvalues and eigenvectors (as columns) of a small symmetric matrix, by cyclic Jacobi rotations."""
    n = len(m)
    a = [row[:] for row in m]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(100):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-22:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-30:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    return [a[i][i] for i in range(n)], v


def close(x: list[float], y: list[float], tol: float = 1e-7) -> bool:
    return all(abs(p - q) <= tol for p, q in zip(x, y))


def test_example() -> None:
    arcs = [(0, 2), (0, 3), (1, 2), (1, 3), (1, 4), (4, 3)]
    a, h = hits_algorithm(5, arcs)
    assert close([round(x, 3) for x in a], [0, 0, 0.591, 0.737, 0.328], 1e-9)
    assert close([round(x, 3) for x in h], [0.591, 0.737, 0, 0, 0.328], 1e-9)


def test_edges() -> None:
    assert hits_algorithm(0, []) == ([], [])
    assert hits_algorithm(3, []) == ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
    a, h = hits_algorithm(2, [(0, 1)])
    assert close(a, [0, 1]) and close(h, [1, 0])
    a, h = hits_algorithm(1, [(0, 0)])
    assert close(a, [1]) and close(h, [1])
    # a star into node 0: one authority, equal hubs
    a, h = hits_algorithm(4, [(1, 0), (2, 0), (3, 0)])
    assert close(a, [1, 0, 0, 0]) and close(h, [0] + [1 / math.sqrt(3)] * 3)


def test_repeated_top_eigenvalue_follows_in_degrees() -> None:
    # two separate arcs: lambda_1 = 1 twice; the limit is the projection of the in-degree vector
    a, h = hits_algorithm(4, [(0, 1), (2, 3)])
    s = 1 / math.sqrt(2)
    assert close(a, [0, s, 0, s]) and close(h, [s, 0, s, 0])


def test_random_against_eigenvectors() -> None:
    rng = random.Random(4127)
    checked = 0
    for _ in range(600):
        n = rng.randint(1, 7)
        arcs = [(u, v) for u in range(n) for v in range(n) if rng.random() < 0.3]
        a, h = hits_algorithm(n, arcs)
        if not arcs:
            assert a == [0.0] * n
            continue
        A = [[0.0] * n for _ in range(n)]
        for u, v in arcs:
            A[u][v] += 1.0
        M = [[sum(A[k][i] * A[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
        vals, vecs = jacobi_eigen(M)
        order = sorted(range(n), key=lambda i: -vals[i])
        lam1 = vals[order[0]]
        # a is a unit eigenvector for the largest eigenvalue, with no negative entry
        Ma = [sum(M[i][j] * a[j] for j in range(n)) for i in range(n)]
        assert close(Ma, [lam1 * x for x in a], 1e-6)
        assert abs(math.sqrt(sum(x * x for x in a)) - 1) < 1e-9
        assert min(a) >= -1e-12 and min(h) >= -1e-12
        # h is A a scaled to norm 1
        Aa = [sum(A[i][j] * a[j] for j in range(n)) for i in range(n)]
        s = math.sqrt(sum(x * x for x in Aa))
        assert close(h, [x / s for x in Aa], 1e-6)
        if n == 1 or vals[order[1]] < lam1 - 1e-3:
            w = [vecs[i][order[0]] for i in range(n)]
            if sum(w) < 0:
                w = [-x for x in w]
            assert close(a, w, 1e-6)
            checked += 1
    assert checked > 300
