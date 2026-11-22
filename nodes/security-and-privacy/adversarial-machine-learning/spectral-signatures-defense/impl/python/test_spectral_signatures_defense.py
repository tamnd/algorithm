# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-signatures-defense/. The authors are listed in prov/DEFG9T.jsonl.

"""Tests of the spectral signatures filter on seeded synthetic features, against a Jacobi eigensolver."""

import math
import random

from spectral_signatures_defense import covariance_sum, spectral_filter, spectral_scores, top_eigenvector


def jacobi_eigen(a: list[list[float]]) -> tuple[list[float], list[list[float]]]:
    """Eigenvalues and eigenvectors (as columns) of a symmetric matrix by cyclic Jacobi rotations."""
    d = len(a)
    a = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]
    for _ in range(100):
        off = math.fsum(a[p][q] ** 2 for p in range(d) for q in range(d) if p != q)
        if off < 1e-30 * (1.0 + math.fsum(a[p][p] ** 2 for p in range(d))):
            break
        for p in range(d):
            for q in range(p + 1, d):
                if a[p][q] == 0.0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(d):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(d):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(d):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    return [a[i][i] for i in range(d)], v


def top_by_jacobi(c: list[list[float]]) -> tuple[float, float, list[float]]:
    vals, vecs = jacobi_eigen(c)
    order = sorted(range(len(vals)), key=lambda i: vals[i], reverse=True)
    second = vals[order[1]] if len(vals) > 1 else 0.0
    return vals[order[0]], second, [vecs[k][order[0]] for k in range(len(vals))]


EXAMPLE = [[-2.0, 0.0], [-1.0, 1.0], [-1.0, -1.0], [-1.0, 2.0], [-1.0, -2.0], [0.0, 0.0], [3.0, 0.0], [3.0, 0.0]]


def test_example_of_the_page() -> None:
    assert covariance_sum(EXAMPLE, [0.0, 0.0]) == [[26.0, 0.0], [0.0, 10.0]]
    assert [round(s, 12) for s in spectral_scores(EXAMPLE)] == [4.0, 1.0, 1.0, 1.0, 1.0, 0.0, 9.0, 9.0]
    kept, removed = spectral_filter(EXAMPLE, 0.25)
    assert removed == [0, 6, 7] and kept == [1, 2, 3, 4, 5]
    rows = [[float(i % 7), float(i % 5)] for i in range(60)]
    assert 1.5 * 0.3 * 60 < 27 and len(spectral_filter(rows, 0.3)[1]) == 27


def test_a_start_column_orthogonal_to_the_top_eigenvector() -> None:
    # The third column has the largest norm but is an eigenvector of the smaller eigenvalue 0.9.
    c = [[0.5, 0.5, 0.0], [0.5, 0.5, 0.0], [0.0, 0.0, 0.9]]
    v = top_eigenvector(c)
    assert abs(abs(v[0]) - math.sqrt(0.5)) < 1e-12 and abs(v[0] - v[1]) < 1e-12 and abs(v[2]) < 1e-12
    assert top_eigenvector([[0.0, 0.0], [0.0, 0.0]]) == [1.0, 0.0]


def test_scores_match_a_jacobi_eigensolver() -> None:
    rng = random.Random(5101)
    done = 0
    while done < 500:
        n, d = rng.randint(2, 12), rng.randint(1, 5)
        stretch = [rng.uniform(0.2, 3.0) for _ in range(d)]
        rows = [[rng.gauss(0.0, 1.0) * stretch[j] for j in range(d)] for _ in range(n)]
        mu = [sum(r[j] for r in rows) / n for j in range(d)]
        c = covariance_sum(rows, mu)
        top, second, v = top_by_jacobi(c)
        if top <= 1e-9 or second > 0.95 * top:
            continue  # the top direction is not well separated; the scores are not unique
        done += 1
        expect = [sum((r[j] - mu[j]) * v[j] for j in range(d)) ** 2 for r in rows]
        got = spectral_scores(rows)
        scale = 1.0 + max(expect)
        assert all(abs(a - b) <= 1e-9 * scale for a, b in zip(got, expect))
        u = top_eigenvector(c)
        assert abs(math.sqrt(sum(a * a for a in u)) - 1.0) < 1e-12
        assert abs(abs(sum(a * b for a, b in zip(u, v))) - 1.0) < 1e-9


def test_filter_removes_exactly_the_largest_scores() -> None:
    rng = random.Random(5102)
    for _ in range(500):
        n, d = rng.randint(1, 15), rng.randint(1, 4)
        rows = [[float(rng.randint(-3, 3)) for _ in range(d)] for _ in range(n)]
        eps = rng.choice([0.0, 0.05, 0.1, 0.2, 0.5, 1.0])
        kept, removed = spectral_filter(rows, eps)
        assert sorted(kept + removed) == list(range(n))
        assert len(removed) == min(n, math.floor(1.5 * eps * n + 1e-9))
        tau = spectral_scores(rows)
        if kept and removed:
            assert min(tau[i] for i in removed) >= max(tau[i] for i in kept)


def test_population_lemma_top_direction_follows_the_mean_shift() -> None:
    """<v, Delta>^2 >= ||Delta||^2 - sigma^2 / (eps (1 - eps)) for the top eigenvector v of the mixture covariance."""
    rng = random.Random(5103)
    for _ in range(500):
        d = rng.randint(1, 6)
        eps = rng.uniform(0.01, 0.5)
        sigma2 = rng.uniform(0.1, 2.0)

        def psd_below() -> list[list[float]]:
            a = [[rng.gauss(0.0, 1.0) for _ in range(d)] for _ in range(d)]
            m = [[sum(a[i][k] * a[j][k] for k in range(d)) for j in range(d)] for i in range(d)]
            top = max(jacobi_eigen(m)[0])
            f = rng.uniform(0.0, 1.0) * sigma2 / top
            return [[f * x for x in row] for row in m]

        cd, cw = psd_below(), psd_below()
        delta = [rng.gauss(0.0, 1.0) * rng.uniform(0.1, 5.0) for _ in range(d)]
        cov = [
            [(1 - eps) * cd[i][j] + eps * cw[i][j] + eps * (1 - eps) * delta[i] * delta[j] for j in range(d)]
            for i in range(d)
        ]
        _, _, v = top_by_jacobi(cov)
        proj2 = sum(a * b for a, b in zip(v, delta)) ** 2
        assert proj2 >= sum(a * a for a in delta) - sigma2 / (eps * (1 - eps)) - 1e-9


def test_planted_poison_is_removed() -> None:
    """A measurement on synthetic features: n = 200, eps = 0.05, ||Delta||^2 = 6 / eps as in Lemma 3.1 of Tran et al."""
    rng = random.Random(5104)
    for trial in range(5):
        n, d, eps = 200, 8, 0.05
        bad = round(eps * n)
        direction = [rng.gauss(0.0, 1.0) for _ in range(d)]
        norm = math.sqrt(sum(a * a for a in direction))
        delta = [a / norm * math.sqrt(6.0 / eps) for a in direction]
        rows = [[rng.gauss(0.0, 1.0) for _ in range(d)] for _ in range(n - bad)]
        rows += [[delta[j] + rng.gauss(0.0, 1.0) for j in range(d)] for _ in range(bad)]
        _, removed = spectral_filter(rows, eps)
        caught = sum(1 for i in removed if i >= n - bad)
        assert len(removed) == 15 and caught == bad, trial
