# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/null-space-property/. The authors are listed in prov/PPTQNH.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from null_space_property import _rref, failure_certificate, has_nsp, nsp_constant, rank

HALF = Fraction(1, 2)


def matvec(a, x):
    return [sum(Fraction(p) * q for p, q in zip(row, x)) for row in a]


def l1(v):
    return sum(abs(x) for x in v)


def kernel_basis(a):
    red, pivots = _rref(a)
    n = len(a[0])
    basis = []
    for f in (c for c in range(n) if c not in pivots):
        v = [Fraction(0)] * n
        v[f] = Fraction(1)
        for i, c in enumerate(pivots):
            v[c] = -red[i][f]
        basis.append(v)
    return basis


def bp_solutions(a, y):
    """All basic solutions of A z = y (supports with independent columns), and the l1 minimum.

    l1 minimization is a linear program, and its minimum is reached at one of
    these basic solutions, so this is an exact brute force solver for tiny A.
    """
    n = len(a[0])
    r = rank(a)
    sols = []
    for t in range(0, r + 1):
        for cols in combinations(range(n), t):
            sub = [[row[j] for j in cols] + [yi] for row, yi in zip(a, y)]
            red, pivots = _rref(sub)
            if t in pivots or len(pivots) != t:
                continue  # inconsistent, or the columns are dependent
            z = [Fraction(0)] * n
            for i, c in enumerate(pivots):
                z[cols[c]] = red[i][t]
            sols.append(z)
    best = min(l1(z) for z in sols)
    return best, [z for z in sols if l1(z) == best]


def test_hand_example():
    a = [[1, 0, 1], [0, 1, 1]]
    theta1, v = nsp_constant(a, 1)
    assert theta1 == Fraction(1, 3)
    assert matvec(a, v) == [0, 0]
    assert has_nsp(a, 1)
    theta2, _ = nsp_constant(a, 2)
    assert theta2 == Fraction(2, 3)
    assert not has_nsp(a, 2)
    x, z = failure_certificate(a, 2)
    assert [abs(t) for t in x] == [1, 1, 0] and [abs(t) for t in z] == [0, 0, 1]
    assert matvec(a, x) == matvec(a, z)
    assert l1(z) < l1(x)


def test_boundary_and_injective_cases():
    # One row of ones: v = (1, -1, 0) has half its mass on one entry, so order 1 fails (not strictly).
    assert nsp_constant([[1, 1, 1]], 1)[0] == HALF
    assert not has_nsp([[1, 1, 1]], 1)
    # An injective matrix has no nonzero null vector.
    eye = [[1 if i == j else 0 for j in range(3)] for i in range(3)]
    assert nsp_constant(eye, 2) == (0, None)
    assert has_nsp(eye, 3)


def test_identity_and_hadamard():
    # [I | H/2] in R^4 has coherence 1/2 < 1/(2s - 1) for s = 1, so order 1 holds.
    # Order 2 fails: e1 + e3 - (h1 + h2)/2 = 0 has half its mass on two entries.
    h = [[1, 1, 1, 1], [1, -1, 1, -1], [1, 1, -1, -1], [1, -1, -1, 1]]
    a = [[Fraction(int(i == j)) for j in range(4)] + [Fraction(v, 2) for v in h[i]] for i in range(4)]
    theta1, _ = nsp_constant(a, 1)
    assert theta1 < HALF
    theta2, _ = nsp_constant(a, 2)
    assert theta2 >= HALF
    assert not has_nsp(a, 2)


def test_constant_bounds_random_null_vectors():
    rng = random.Random(1)
    for _ in range(6):
        a = [[rng.randint(-3, 3) for _ in range(6)] for _ in range(3)]
        basis = kernel_basis(a)
        for s in (1, 2):
            theta, v = nsp_constant(a, s)
            assert matvec(a, v) == [0, 0, 0]
            assert theta <= s * nsp_constant(a, 1)[0]
            for _ in range(100):
                coef = [Fraction(rng.randint(-9, 9), rng.randint(1, 9)) for _ in basis]
                w = [sum(c * b[i] for c, b in zip(coef, basis)) for i in range(6)]
                if l1(w) == 0:
                    continue
                top = sum(sorted((abs(t) for t in w), reverse=True)[:s])
                assert top / l1(w) <= theta


def test_property_decides_l1_recovery():
    # If the property of order s holds, l1 minimization returns every s-sparse
    # vector as its unique solution; if it fails, the certificate shows a
    # vector with the same measurements and no larger l1 norm.
    rng = random.Random(2)
    seen = {True: 0, False: 0}
    for _ in range(8):
        a = [[rng.randint(-3, 3) for _ in range(6)] for _ in range(4)]
        for s in (1, 2):
            ok = has_nsp(a, s)
            seen[ok] += 1
            if ok:
                for _ in range(6):
                    x = [Fraction(0)] * 6
                    for i in rng.sample(range(6), s):
                        x[i] = Fraction(rng.choice([-1, 1]) * rng.randint(1, 5))
                    best, argmins = bp_solutions(a, matvec(a, x))
                    assert best == l1(x)
                    assert argmins and all(z == x for z in argmins)
            else:
                x, z = failure_certificate(a, s)
                assert sum(1 for t in x if t != 0) <= s
                assert matvec(a, x) == matvec(a, z)
                assert z != x and l1(z) <= l1(x)
    assert seen[True] > 0 and seen[False] > 0
