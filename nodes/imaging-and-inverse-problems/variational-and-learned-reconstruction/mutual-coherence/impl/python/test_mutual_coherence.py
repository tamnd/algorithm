# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mutual-coherence/. The authors are listed in prov/1VF7YK.jsonl.

import cmath
import math
import random

from mutual_coherence import (
    coherence,
    max_sparsity_for_uniqueness,
    restricted_isometry_constant,
    spark,
    welch_bound,
)


def hadamard(m):
    h = [[1.0]]
    while len(h) < m:
        h = [row + row for row in h] + [row + [-v for v in row] for row in h]
    return h


def identity_hadamard(m):
    h = hadamard(m)
    r = math.sqrt(m)
    return [[1.0 if i == j else 0.0 for j in range(m)] + [v / r for v in h[i]] for i in range(m)]


def gauss_unit(rng, m, n):
    a = [[rng.gauss(0.0, 1.0) for _ in range(n)] for _ in range(m)]
    for j in range(n):
        nrm = math.sqrt(sum(a[i][j] ** 2 for i in range(m)))
        for i in range(m):
            a[i][j] /= nrm
    return a


def test_identity_and_hadamard():
    # [I | H/2] in R^4: every identity column meets every Hadamard column with |<.,.>| = 1/2.
    a = identity_hadamard(4)
    mu, i, j = coherence(a)
    assert abs(mu - 0.5) <= 1e-15
    assert i < 4 <= j
    assert max_sparsity_for_uniqueness(mu) == 1
    # The spark is 4, above the bound 1 + 1/mu = 3: (h1 + h2) / 2 = e1 + e3.
    assert spark(a) == 4


def test_identity_and_unitary_dft():
    m = 4
    f = [[cmath.exp(-2j * math.pi * r * c / m) / math.sqrt(m) for c in range(m)] for r in range(m)]
    a = [[complex(1.0 if i == j else 0.0) for j in range(m)] + f[i] for i in range(m)]
    mu, _, _ = coherence(a)
    assert abs(mu - 1.0 / math.sqrt(m)) <= 1e-15


def test_simplex_frame_meets_the_welch_bound():
    # Three unit vectors at 120 degrees in the plane, and m + 1 vertices of a regular simplex in R^m.
    a = [[math.cos(2 * math.pi * k / 3) for k in range(3)], [math.sin(2 * math.pi * k / 3) for k in range(3)]]
    mu, _, _ = coherence(a)
    assert abs(mu - 0.5) <= 1e-15
    assert abs(welch_bound(2, 3) - 0.5) <= 1e-15
    for m in range(2, 6):
        # The centered standard basis of R^(m+1) spans an m-dimensional space;
        # the coherence does not depend on the coordinates chosen in it.
        cols = [[(1.0 if i == k else 0.0) - 1.0 / (m + 1) for i in range(m + 1)] for k in range(m + 1)]
        a = [[cols[k][i] for k in range(m + 1)] for i in range(m + 1)]
        mu, _, _ = coherence(a)
        assert abs(mu - 1.0 / m) <= 1e-14
        assert abs(welch_bound(m, m + 1) - 1.0 / m) <= 1e-15


def test_welch_bound_holds_on_random_matrices():
    rng = random.Random(1)
    for m in range(2, 7):
        for n in (m + 1, 2 * m, 3 * m):
            a = gauss_unit(rng, m, n)
            assert coherence(a)[0] >= welch_bound(m, n) - 1e-15


def test_gershgorin_bound_and_spark_bound():
    rng = random.Random(2)
    for _ in range(4):
        a = gauss_unit(rng, 5, 8)
        mu, _, _ = coherence(a)
        assert abs(restricted_isometry_constant(a, 2) - mu) <= 1e-12
        for s in (2, 3):
            assert restricted_isometry_constant(a, s) <= (s - 1) * mu + 1e-12
        assert spark(a) >= 1.0 + 1.0 / mu
    a = identity_hadamard(8)
    mu, _, _ = coherence(a)
    assert abs(mu - 1.0 / math.sqrt(8)) <= 1e-15
    for s in (2, 3):
        assert restricted_isometry_constant(a, s) <= (s - 1) * mu + 1e-12
