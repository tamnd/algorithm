# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/principal-component-analysis/. The authors are listed in prov/45RF44.jsonl.

import math
import random

from principal_component_analysis import jacobi_eigen, pca, reconstruct

EXAMPLE = [
    [13, 11, 9], [9, 15, 7], [5, 7, 17], [1, 11, 15],
    [7, -1, -3], [3, 3, -5], [-1, -5, 5], [-5, -1, 3],
]
TOL = 1e-8


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def same_up_to_sign(a: list[float], b: list[float]) -> bool:
    return all(abs(x - y) < 1e-7 for x, y in zip(a, b)) or all(abs(x + y) < 1e-7 for x, y in zip(a, b))


def covariance(x: list[list[float]]) -> list[list[float]]:
    n, d = len(x), len(x[0])
    mu = [sum(r[j] for r in x) / n for j in range(d)]
    return [[sum((r[a] - mu[a]) * (r[b] - mu[b]) for r in x) / n for b in range(d)] for a in range(d)]


def power_deflation(c: list[list[float]], k: int, rng: random.Random) -> list[tuple[float, list[float]]]:
    """An independent oracle: power iteration with Hotelling deflation."""
    d = len(c)
    a = [row[:] for row in c]
    out = []
    for _ in range(k):
        v = [rng.gauss(0, 1) for _ in range(d)]
        for _ in range(3000):
            w = [dot(row, v) for row in a]
            nw = math.sqrt(dot(w, w)) or 1.0
            v = [x / nw for x in w]
        lam = dot(v, [dot(row, v) for row in a])
        out.append((lam, v))
        a = [[a[i][j] - lam * v[i] * v[j] for j in range(d)] for i in range(d)]
    return out


def test_worked_example() -> None:
    x = [[float(t) for t in r] for r in EXAMPLE]
    assert covariance(x) == [[29, 22, 4], [22, 44, 26], [4, 26, 53]]
    res = pca(x, 2)
    assert res.mean == [4, 5, 6]
    assert all(abs(a - b) < TOL for a, b in zip(res.eigenvalues, [81, 36, 9]))
    assert same_up_to_sign(res.components[0], [1 / 3, 2 / 3, 2 / 3])
    assert same_up_to_sign(res.components[1], [2 / 3, 1 / 3, -2 / 3])
    assert all(abs(abs(z[0]) - 9) < 1e-7 and abs(abs(z[1]) - 6) < 1e-7 for z in res.scores)
    err = sum(sum((a - b) ** 2 for a, b in zip(r, h)) for r, h in zip(x, reconstruct(res))) / 8
    assert abs(err - 9) < TOL


def test_jacobi_against_definition_and_power_method() -> None:
    rng = random.Random(3)
    for _ in range(100):
        d = rng.randint(1, 6)
        b = [[rng.uniform(-2, 2) for _ in range(d)] for _ in range(d)]
        c = [[dot(b[i], b[j]) for j in range(d)] for i in range(d)]
        vals, vecs = jacobi_eigen(c)
        assert all(vals[i] >= vals[i + 1] - TOL for i in range(d - 1))
        for lam, v in zip(vals, vecs):
            cv = [dot(row, v) for row in c]
            assert all(abs(cv[i] - lam * v[i]) < 1e-7 for i in range(d))
        assert abs(sum(vals) - sum(c[i][i] for i in range(d))) < 1e-8
    c = [[4.0, 1.0, 0.5], [1.0, 3.0, 0.2], [0.5, 0.2, 1.0]]
    vals, vecs = jacobi_eigen(c)
    for (lam, v), lam2, v2 in zip(power_deflation(c, 3, random.Random(5)), vals, vecs):
        assert abs(lam - lam2) < 1e-7 and same_up_to_sign(v, v2)


def test_orthonormal_and_variance_identity() -> None:
    rng = random.Random(17)
    for _ in range(100):
        n, d = rng.randint(2, 12), rng.randint(1, 5)
        k = rng.randint(0, d)
        x = [[rng.gauss(0, 1 + j) for j in range(d)] for _ in range(n)]
        res = pca(x, k)
        for i in range(k):
            for j in range(k):
                assert abs(dot(res.components[i], res.components[j]) - (i == j)) < 1e-9
        for j in range(k):
            col = [z[j] for z in res.scores]
            assert abs(sum(col)) < 1e-8
            assert abs(dot(col, col) / n - res.eigenvalues[j]) < 1e-8
            for l in range(j):
                assert abs(dot(col, [z[l] for z in res.scores]) / n) < 1e-8
        total = sum(covariance(x)[j][j] for j in range(d))
        assert abs(sum(res.eigenvalues) - total) < 1e-8
        assert all(lam > -1e-9 for lam in res.eigenvalues)


def test_two_views_agree() -> None:
    """Max variance = trace - min error, and no orthonormal W does better."""
    rng = random.Random(23)
    for _ in range(100):
        n, d = rng.randint(3, 10), rng.randint(2, 5)
        k = rng.randint(1, d - 1)
        x = [[rng.gauss(0, 1) * (j + 1) + rng.gauss(0, 0.3) for j in range(d)] for _ in range(n)]
        res = pca(x, k)
        total = sum(res.eigenvalues)
        err = sum(sum((a - b) ** 2 for a, b in zip(r, h)) for r, h in zip(x, reconstruct(res))) / n
        kept = sum(res.eigenvalues[:k])
        assert abs(err - (total - kept)) < 1e-8
        assert abs(err - sum(res.eigenvalues[k:])) < 1e-8
        c = covariance(x)
        for _ in range(20):  # random orthonormal k-frames by Gram-Schmidt
            frame: list[list[float]] = []
            while len(frame) < k:
                v = [rng.gauss(0, 1) for _ in range(d)]
                for f in frame:
                    p = dot(v, f)
                    v = [a - p * b for a, b in zip(v, f)]
                nv = math.sqrt(dot(v, v))
                if nv > 1e-6:
                    frame.append([a / nv for a in v])
            captured = sum(dot(f, [dot(row, f) for row in c]) for f in frame)
            assert captured <= kept + 1e-9


def test_two_dimensional_brute_force_direction() -> None:
    rng = random.Random(29)
    for _ in range(50):
        x = [[rng.gauss(0, 2), 0.0] for _ in range(15)]
        x = [[a, 0.5 * a + rng.gauss(0, 1)] for a, _ in x]
        c = covariance(x)
        best = max(
            (c[0][0] * math.cos(t) ** 2 + 2 * c[0][1] * math.cos(t) * math.sin(t) + c[1][1] * math.sin(t) ** 2, t)
            for t in [math.pi * i / 20000 for i in range(20000)]
        )
        assert abs(pca(x, 1).eigenvalues[0] - best[0]) < 1e-6


def test_edges() -> None:
    res = pca([[2.0, 3.0]], 1)
    assert res.eigenvalues == [0.0, 0.0] and res.scores == [[0.0]]
    res = pca([[1.0, 1.0], [3.0, 3.0]], 2)
    assert abs(res.eigenvalues[0] - 2.0) < TOL and abs(res.eigenvalues[1]) < TOL
    assert pca([[1.0], [2.0], [3.0]], 0).scores == [[], [], []]
