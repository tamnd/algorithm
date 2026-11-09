# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/benson-algorithm/. The authors are listed in prov/V38187.jsonl.

import random
from fractions import Fraction as Fr
from itertools import combinations

from benson_algorithm import benson, simplex_max, solve_square


def poly_vertices(A, b):
    """Vertices of {x : A x >= b} by brute force over n-subsets of rows."""
    n = len(A[0])
    out = set()
    for sub in combinations(range(len(A)), n):
        x = solve_square([[Fr(v) for v in A[i]] for i in sub], [Fr(b[i]) for i in sub])
        if x is not None and all(sum(Fr(a) * y for a, y in zip(A[i], x)) >= b[i] for i in range(len(A))):
            out.add(tuple(x))
    return sorted(out)


def in_upper_hull(s, Q):
    """Is s in conv(Q) + R^p_+? Brute force over the basic solutions of
    lam >= 0, sum(lam) = 1, sum(lam_q q) + slack = s, slack >= 0."""
    p, k = len(s), len(Q)
    cols = [list(q) + [Fr(1)] for q in Q]  # columns for lam
    cols += [[Fr(int(i == j)) for i in range(p)] + [Fr(0)] for j in range(p)]  # slacks
    rhs = list(s) + [Fr(1)]
    for basis in combinations(range(k + p), p + 1):
        M = [[cols[j][i] for j in basis] for i in range(p + 1)]
        w = solve_square(M, rhs)
        if w is not None and all(x >= 0 for x in w):
            return True
    return False


def oracle_vertices(A, b, C):
    """Vertices of conv(C[vertices of X]) + R^p_+."""
    S = sorted({tuple(sum(Fr(c) * x for c, x in zip(row, v)) for row in C) for v in poly_vertices(A, b)})
    return sorted(s for s in S if not in_upper_hull(s, [q for q in S if q != s])), S


def box(n, lo, hi):
    A, b = [], []
    for j in range(n):
        e = [int(i == j) for i in range(n)]
        A += [e, [-x for x in e]]
        b += [lo, -hi]
    return A, b


def test_example() -> None:
    # minimize (x1, x2) over x >= 0, x1 + 2 x2 >= 4, 3 x1 + x2 >= 6.
    A = [[1, 0], [0, 1], [1, 2], [3, 1]]
    b = [0, 0, 4, 6]
    V, cuts = benson(A, b, [[1, 0], [0, 1]])
    assert V == [(0, 6), (Fr(8, 5), Fr(6, 5)), (4, 0)]
    for h, beta in cuts:
        assert all(sum(a * y for a, y in zip(h, v)) >= beta for v in V)


def test_simplex_against_vertices() -> None:
    rng = random.Random(11)
    for _ in range(150):
        n = rng.randint(1, 3)
        A, b = box(n, 0, rng.randint(1, 6))
        for _ in range(rng.randint(0, 3)):
            A.append([rng.randint(-3, 3) for _ in range(n)])
            b.append(rng.randint(-6, 2))
        c = [rng.randint(-5, 5) for _ in range(n)]
        verts = poly_vertices(A, b)
        # max c^T x subject to A x >= b, as  x = x1 - x2, A x1 - A x2 - s = b.
        m = len(A)
        M = [A[i] + [-x for x in A[i]] + [-int(k == i) for k in range(m)] for i in range(m)]
        st, val, w = simplex_max(M, b, c + [-x for x in c] + [0] * m)
        if not verts:
            assert st == "infeasible"
            continue
        assert st == "optimal"
        assert val == max(sum(ci * x for ci, x in zip(c, v)) for v in verts)
        assert all(x >= 0 for x in w)


def test_unbounded_and_infeasible() -> None:
    assert simplex_max([[1, -1]], [1], [1, 0])[0] == "unbounded"
    assert simplex_max([[1, 1]], [-1], [1, 0])[0] == "infeasible"


def random_molp(rng):
    n = rng.randint(2, 3)
    p = rng.randint(2, 3)
    A, b = box(n, 0, rng.randint(2, 5))
    for _ in range(rng.randint(0, 3)):
        A.append([rng.randint(-3, 3) for _ in range(n)])
        b.append(rng.randint(-8, 3))
    C = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(p)]
    return A, b, C


def test_random_against_oracle() -> None:
    rng = random.Random(1998)
    done = 0
    while done < 30:
        A, b, C = random_molp(rng)
        if not poly_vertices(A, b):
            continue
        done += 1
        V, cuts = benson(A, b, C)
        expect, S = oracle_vertices(A, b, C)
        assert V == expect, (A, b, C)
        # Every cut is valid for the image points and supports the upper image.
        for h, beta in cuts:
            vals = [sum(a * y for a, y in zip(h, s)) for s in S]
            assert min(vals) == beta
            assert all(x >= 0 for x in h) and sum(h) == 1


def test_weighted_sums_attained_at_vertices() -> None:
    # min u^T y over the upper image equals min u^T C x over X, and is
    # attained at a vertex, for every u > 0.
    rng = random.Random(3)
    done = 0
    while done < 15:
        A, b, C = random_molp(rng)
        if not poly_vertices(A, b):
            continue
        done += 1
        V, _ = benson(A, b, C)
        _, S = oracle_vertices(A, b, C)
        for _ in range(5):
            u = [Fr(rng.randint(1, 9)) for _ in range(len(C))]
            best = min(sum(a * y for a, y in zip(u, s)) for s in S)
            assert min(sum(a * y for a, y in zip(u, v)) for v in V) == best
