# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/basis-pursuit/. The authors are listed in prov/M3TQK5.jsonl.

import itertools
import random
from fractions import Fraction as F

import pytest

from basis_pursuit import basis_pursuit, linprog_eq


# ---- small exact linear algebra for the references ----

def matvec(A, x):
    return [sum((F(a) * b for a, b in zip(row, x)), F(0)) for row in A]


def det(M):
    T = [[F(v) for v in row] for row in M]
    n, d = len(T), F(1)
    for c in range(n):
        p = next((r for r in range(c, n) if T[r][c] != 0), None)
        if p is None:
            return F(0)
        if p != c:
            T[c], T[p] = T[p], T[c]
            d = -d
        d *= T[c][c]
        for r in range(c + 1, n):
            f = T[r][c] / T[c][c]
            T[r] = [a - f * e for a, e in zip(T[r], T[c])]
    return d


def solve_square(M, b):
    n = len(M)
    T = [[F(v) for v in M[i]] + [F(b[i])] for i in range(n)]
    for c in range(n):
        p = next((r for r in range(c, n) if T[r][c] != 0), None)
        if p is None:
            return None
        T[c], T[p] = T[p], T[c]
        for r in range(n):
            if r != c and T[r][c] != 0:
                f = T[r][c] / T[c][c]
                T[r] = [a - f * e for a, e in zip(T[r], T[c])]
    return [T[i][n] / T[i][i] for i in range(n)]


def gram(A, S):
    return [[sum(F(A[i][a]) * A[i][b] for i in range(len(A))) for b in S] for a in S]


def solutions_on_supports(A, y, kmax):
    """Every x with A x = y whose support is a set S, |S| <= kmax, of independent columns."""
    n = len(A[0])
    out = []
    for k in range(kmax + 1):
        for S in itertools.combinations(range(n), k):
            G = gram(A, S)
            if k and det(G) == 0:
                continue
            z = solve_square(G, [sum(F(A[i][a]) * y[i] for i in range(len(A))) for a in S]) if k else []
            x = [F(0)] * n
            for j, v in zip(S, z):
                x[j] = v
            if matvec(A, x) == [F(v) for v in y]:
                out.append(x)
    return out


def l1(x):
    return sum(abs(v) for v in x)


def is_psd(M):
    """Exact test: a symmetric matrix is positive semidefinite iff every principal minor is >= 0."""
    n = len(M)
    return all(det([[M[i][j] for j in S] for i in S]) >= 0 for k in range(1, n + 1) for S in itertools.combinations(range(n), k))


def rip_at_most(G, k, t):
    """Brute force over all supports of size k: is delta_k <= t, given the Gram matrix G = A^T A?"""
    n = len(G)
    for S in itertools.combinations(range(n), k):
        GS = [[G[i][j] for j in S] for i in S]
        upper = [[(1 + t) * (a == b) - GS[a][b] for b in range(k)] for a in range(k)]
        lower = [[GS[a][b] - (1 - t) * (a == b) for b in range(k)] for a in range(k)]
        if not (is_psd(upper) and is_psd(lower)):
            return False
    return True


def rip_constant(G, k, steps=40):
    """delta_k to within 2^-steps by bisection on the exact test above. Returns (low, high)."""
    lo, hi = F(0), F(max(1, max(G[i][i] for i in range(len(G)))))
    if rip_at_most(G, k, lo):
        return lo, lo
    for _ in range(steps):
        mid = (lo + hi) / 2
        if rip_at_most(G, k, mid):
            hi = mid
        else:
            lo = mid
    return lo, hi


def hadamard(n):
    H = [[1]]
    while len(H) < n:
        H = [r + r for r in H] + [r + [-v for v in r] for r in H]
    return H


def identity_plus_hadamard(n):
    """[I | H/sqrt(n)] with n = 16: unit-norm columns and coherence 1/4, all exact."""
    H = hadamard(n)
    q = F(1, 4) if n == 16 else None
    return [[F(int(i == j)) for j in range(n)] + [q * H[i][j] for j in range(n)] for i in range(n)]


TETRA = [[1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]]  # columns have norm sqrt(3)
TETRA_GRAM = [[F(sum(TETRA[i][a] * TETRA[i][b] for i in range(3)), 3) for b in range(4)] for a in range(4)]


# ---- tests ----

def test_linprog_small() -> None:
    # minimize -z0 - z1 subject to z0 + z1 + z2 = 4, z0 - z1 + z3 = 2
    z, val = linprog_eq([-1, -1, 0, 0], [[1, 1, 1, 0], [1, -1, 0, 1]], [4, 2])
    assert val == -4 and z[0] + z[1] == 4
    assert linprog_eq([1, 1], [[1, 1], [1, 1]], [1, 2]) is None
    z, val = linprog_eq([1, 2], [[1, 1], [2, 2]], [3, 6])  # redundant row
    assert z == [3, 0] and val == 3


def test_matches_vertex_enumeration() -> None:
    # The LP optimum is attained at a vertex, and the vertices are the solutions on independent supports.
    rng = random.Random(1)
    for _ in range(60):
        m, n = rng.choice([(2, 3), (2, 4), (3, 4), (3, 5), (3, 6)])
        A = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(m)]
        y = [rng.randint(-4, 4) for _ in range(m)]
        cands = solutions_on_supports(A, y, m)
        x = basis_pursuit(A, y)
        if not cands:
            assert x is None
            continue
        assert x is not None and matvec(A, x) == [F(v) for v in y]
        assert l1(x) == min(l1(c) for c in cands)


def test_tetrahedron_rip_exact() -> None:
    # delta_1 = 0, delta_2 = mu = 1/3, delta_3 = 2/3, delta_4 = 1, checked over all supports.
    for k, d in [(1, F(0)), (2, F(1, 3)), (3, F(2, 3)), (4, F(1))]:
        assert rip_at_most(TETRA_GRAM, k, d)
        if d > 0:
            assert not rip_at_most(TETRA_GRAM, k, d - F(1, 1000))


def test_tetrahedron_recovers_every_1_sparse_vector() -> None:
    # delta_2 = 1/3 < sqrt(2) - 1, because (1/3 + 1)^2 = 16/9 < 2, so every 1-sparse x is recovered.
    assert (F(1, 3) + 1) ** 2 < 2
    for j in range(4):
        for v in (-3, -1, 2, 5):
            x0 = [F(0)] * 4
            x0[j] = F(v)
            assert basis_pursuit(TETRA, matvec(TETRA, x0)) == x0


def test_two_column_rip_equals_coherence() -> None:
    # For unit-norm columns the 2x2 Gram blocks are [[1, g], [g, 1]], so delta_2 = mu exactly.
    units = [(F(1), F(0), F(0)), (F(1, 3), F(2, 3), F(2, 3)), (F(2, 7), F(3, 7), F(-6, 7)), (F(4, 9), F(-4, 9), F(7, 9)), (F(0), F(3, 5), F(4, 5))]
    A = [[u[i] for u in units] for i in range(3)]
    G = gram(A, range(5))
    mu = max(abs(G[i][j]) for i in range(5) for j in range(i + 1, 5))
    assert rip_at_most(G, 2, mu) and not rip_at_most(G, 2, mu - F(1, 10**6))


def test_random_small_rip_is_large() -> None:
    # Tiny random matrices: delta_4 is far above sqrt(2) - 1, so the RIP theorem says nothing for s = 2.
    rng = random.Random(3)
    for _ in range(3):
        A = [[F(rng.choice((-1, 1)), 2) for _ in range(6)] for _ in range(4)]  # columns of norm 1
        lo, hi = rip_constant(gram(A, range(6)), 4, 20)
        assert lo > F(1, 2)


def sparsest(A, y, smax):
    """Brute force l0: the solutions of A x = y with the fewest nonzeros, up to smax."""
    for k in range(smax + 1):
        sols = [x for x in solutions_on_supports(A, y, k) if sum(1 for v in x if v != 0) == k]
        if sols:
            return sols
    return []


def test_recovery_matches_l0_brute_force() -> None:
    # [I | H/4] has coherence 1/4 < 1/(2s - 1) for s = 2, so BP must return the unique sparsest solution.
    A = identity_plus_hadamard(16)
    rng = random.Random(5)
    for _ in range(4):
        S = rng.sample(range(32), 2)
        x0 = [F(0)] * 32
        for j in S:
            x0[j] = F(rng.choice([-3, -2, -1, 1, 2, 3]))
        y = matvec(A, x0)
        assert basis_pursuit(A, y) == x0
        assert sparsest(A, y, 2) == [x0]


def test_omp_fails_bp_succeeds() -> None:
    # Columns e1, e2, e3 and w = (6, 6, 7)/11, all of norm 1. x0 = e1 + e2.
    w = (F(6, 11), F(6, 11), F(7, 11))
    A = [[1, 0, 0, w[0]], [0, 1, 0, w[1]], [0, 0, 1, w[2]]]
    x0 = [F(1), F(1), F(0), F(0)]
    y = matvec(A, x0)
    assert basis_pursuit(A, y) == x0
    best = min(l1(c) for c in solutions_on_supports(A, y, 3))
    assert {tuple(c) for c in solutions_on_supports(A, y, 3) if l1(c) == best} == {tuple(x0)}  # unique minimiser
    # OMP picks w first, since <w, y>^2 = 144/121 > 1, and then e3. It ends with an exact fit on the wrong support.
    alt = [F(0), F(0), F(-7, 6), F(11, 6)]
    assert matvec(A, alt) == y and l1(alt) == 3


def test_bp_fails_omp_succeeds() -> None:
    # The reverse also happens: here the unique l1 minimiser is not the 2-sparse x0.
    A = [[F(7, 9), F(-3, 7), F(1, 9), F(8, 9)], [F(4, 9), F(2, 7), F(8, 9), F(1, 9)], [F(4, 9), F(6, 7), F(4, 9), F(-4, 9)]]
    x0 = [F(2), F(-1), F(0), F(0)]
    y = matvec(A, x0)
    x = basis_pursuit(A, y)
    assert x == [F(181, 140), F(0), F(-3, 28), F(39, 35)]
    assert l1(x) == F(88, 35) < l1(x0)
    best = min(l1(c) for c in solutions_on_supports(A, y, 3))
    assert {tuple(c) for c in solutions_on_supports(A, y, 3) if l1(c) == best} == {tuple(x)}


def test_infeasible() -> None:
    assert basis_pursuit([[1, 1], [1, 1]], [1, 2]) is None
