# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/genetic-principal-components/. The authors are listed in prov/HDK5SD.jsonl.

import math
import random

import pytest

from genetic_principal_components import (covariance, eigenstrat_statistic, jacobi_eigen, normalize,
                                          principal_components, residualize, top_eigenvectors)


def simulate(rng, sizes, m, spread=0.15):
    """Genotypes of len(sizes) populations that drift apart from one ancestral frequency per site."""
    g, labels = [], []
    anc = [rng.uniform(0.1, 0.9) for _ in range(m)]
    freqs = [[min(0.99, max(0.01, a + rng.gauss(0.0, spread))) for a in anc] for _ in sizes]
    for k, size in enumerate(sizes):
        for _ in range(size):
            g.append([(rng.random() < f) + (rng.random() < f) for f in freqs[k]])
            labels.append(k)
    return g, labels


def matvec(x, v):
    return [sum(a * b for a, b in zip(row, v)) for row in x]


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def test_normalize_by_hand():
    g = [[0, 2, 1], [1, 2, 1], [2, 2, 0], [1, 2, 0]]
    mat, kept = normalize(g)
    assert kept == [0, 2]  # site 1 is monomorphic
    # site 0: mu = 1, p = 0.5, s = 0.5
    assert [row[0] for row in mat] == pytest.approx([-2.0, 0.0, 2.0, 0.0])
    # site 2: mu = 0.5, p = 0.25, s = sqrt(0.1875)
    s = math.sqrt(0.1875)
    assert [row[1] for row in mat] == pytest.approx([0.5 / s, 0.5 / s, -0.5 / s, -0.5 / s])
    for c in range(2):
        assert sum(row[c] for row in mat) == pytest.approx(0.0, abs=1e-12)


def test_covariance_rows_sum_to_zero():
    rng = random.Random(3)
    g, _ = simulate(rng, [6, 6], 40)
    x = covariance(normalize(g)[0])
    n = len(x)
    for a in range(n):
        assert sum(x[a]) == pytest.approx(0.0, abs=1e-10)
        for b in range(n):
            assert x[a][b] == x[b][a]


def test_jacobi_reconstructs_matrix():
    rng = random.Random(5)
    n = 7
    b = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
    a = [[sum(b[i][t] * b[j][t] for t in range(n)) for j in range(n)] for i in range(n)]
    vals, vecs = jacobi_eigen(a)
    assert vals == sorted(vals, reverse=True)
    for c in range(n):
        v = [vecs[r][c] for r in range(n)]
        av = matvec(a, v)
        assert av == pytest.approx([vals[c] * t for t in v], abs=1e-9)
        for d in range(n):
            w = [vecs[r][d] for r in range(n)]
            assert dot(v, w) == pytest.approx(1.0 if c == d else 0.0, abs=1e-10)
    assert sum(vals) == pytest.approx(sum(a[i][i] for i in range(n)))


def test_planted_spectrum():
    rng = random.Random(11)
    n = 10
    spectrum = [9.0, 4.0, 2.0, 1.0, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
    raw = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
    q = []
    for v in raw:  # Gram-Schmidt to a random orthonormal basis
        w = list(v)
        for u in q:
            c = dot(u, w)
            w = [a - c * b for a, b in zip(w, u)]
        nrm = math.sqrt(dot(w, w))
        q.append([a / nrm for a in w])
    x = [[sum(spectrum[t] * q[t][i] * q[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
    vals, vecs = top_eigenvectors(x, 3, random.Random(1))
    assert vals == pytest.approx(spectrum[:3], abs=1e-9)
    for c in range(3):
        assert abs(dot(vecs[c], q[c])) == pytest.approx(1.0, abs=1e-8)


def test_against_jacobi_on_genotypes():
    rng = random.Random(7)
    g, _ = simulate(rng, [8, 8, 8], 120)
    mat, kept = normalize(g)
    x = covariance(mat)
    vals, vecs = top_eigenvectors(x, 2, random.Random(2))
    ref_vals, ref_vecs = jacobi_eigen(x)
    n = len(x)
    assert vals == pytest.approx(ref_vals[:2], rel=1e-8)
    for c in range(2):
        ref = [ref_vecs[r][c] for r in range(n)]
        assert abs(dot(vecs[c], ref)) == pytest.approx(1.0, abs=1e-6)
        assert matvec(x, vecs[c]) == pytest.approx([vals[c] * t for t in vecs[c]], abs=1e-7)
        assert sum(vecs[c]) == pytest.approx(0.0, abs=1e-7)  # orthogonal to the all-ones vector
    assert dot(vecs[0], vecs[1]) == pytest.approx(0.0, abs=1e-8)
    # The trace is the mean over sites of the squared column norms, and the smallest eigenvalue is 0.
    assert sum(ref_vals) == pytest.approx(sum(x[i][i] for i in range(n)))
    assert ref_vals[-1] == pytest.approx(0.0, abs=1e-9)


def test_first_axis_separates_two_populations():
    rng = random.Random(13)
    g, labels = simulate(rng, [10, 10], 300)
    vals, vecs, kept = principal_components(g, 2, random.Random(4))
    pc1 = vecs[0]
    side = [v > 0 for v in pc1]
    agree = sum(s == (lab == 1) for s, lab in zip(side, labels))
    assert agree in (0, len(labels))
    assert vals[0] > 1.5 * vals[1]


def test_three_populations_need_two_axes():
    rng = random.Random(17)
    g, labels = simulate(rng, [8, 8, 8], 300)
    vals, vecs, _ = principal_components(g, 3, random.Random(6))
    centers = []
    for k in range(3):
        idx = [i for i, lab in enumerate(labels) if lab == k]
        centers.append([sum(vecs[c][i] for i in idx) / len(idx) for c in range(2)])
    # Every individual is closest to the center of its own population in the plane of PC1 and PC2.
    for i, lab in enumerate(labels):
        pt = [vecs[0][i], vecs[1][i]]
        dist = [sum((a - b) ** 2 for a, b in zip(pt, ctr)) for ctr in centers]
        assert min(range(3), key=lambda k: dist[k]) == lab
    assert vals[1] > 1.5 * vals[2]


def test_eigenstrat_removes_stratification():
    rng = random.Random(19)
    g, labels = simulate(rng, [15, 15], 300, spread=0.2)
    vals, vecs, kept = principal_components(g, 1, random.Random(8))
    # A phenotype that depends only on the population, not on any site.
    pheno = [lab + rng.gauss(0.0, 0.3) for lab in labels]
    # The site with the largest frequency difference between the populations.
    def diff(j):
        a = sum(g[i][j] for i in range(15)) / 30
        b = sum(g[i][j] for i in range(15, 30)) / 30
        return abs(a - b)
    j = max(range(len(g[0])), key=diff)
    geno = [float(row[j]) for row in g]
    raw = eigenstrat_statistic(geno, pheno, [])
    adjusted = eigenstrat_statistic(geno, pheno, vecs[:1])
    assert raw > 10.0
    assert adjusted < 3.84


def test_statistic_without_axes_is_correlation():
    rng = random.Random(23)
    y = [rng.gauss(0, 1) for _ in range(25)]
    x = [rng.choice((0.0, 1.0, 2.0)) for _ in range(25)]
    mx, my = sum(x) / 25, sum(y) / 25
    r = sum((a - mx) * (b - my) for a, b in zip(x, y))
    r /= math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
    assert eigenstrat_statistic(x, y, []) == pytest.approx(24 * r * r)
    res = residualize(y, [])
    assert sum(res) == pytest.approx(0.0, abs=1e-12)


def test_seed_and_errors():
    rng = random.Random(29)
    g, _ = simulate(rng, [5, 5], 50)
    a = principal_components(g, 2, random.Random(1))
    b = principal_components(g, 2, random.Random(1))
    assert a == b
    x = covariance(normalize(g)[0])
    with pytest.raises(ValueError):
        top_eigenvectors(x, 0, random.Random(1))
    with pytest.raises(ValueError):
        covariance(normalize([[0, 0], [0, 0]])[0])
