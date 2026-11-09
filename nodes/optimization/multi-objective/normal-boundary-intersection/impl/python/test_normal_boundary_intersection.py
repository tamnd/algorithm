# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/normal-boundary-intersection/. The authors are listed in prov/QJW02J.jsonl.

import random
from fractions import Fraction as Fr
from itertools import combinations
from math import comb

from normal_boundary_intersection import lp_min, nbi, simplex_grid


def solve_square(M, rhs):
    k = len(M)
    aug = [list(M[i]) + [rhs[i]] for i in range(k)]
    for col in range(k):
        piv = next((i for i in range(col, k) if aug[i][col] != 0), -1)
        if piv < 0:
            return None
        aug[col], aug[piv] = aug[piv], aug[col]
        pv = aug[col][col]
        aug[col] = [x / pv for x in aug[col]]
        for i in range(k):
            if i != col and aug[i][col] != 0:
                f = aug[i][col]
                aug[i] = [x - f * y for x, y in zip(aug[i], aug[col])]
    return [aug[i][k] for i in range(k)]


def poly_vertices(A, b):
    n = len(A[0])
    out = set()
    for sub in combinations(range(len(A)), n):
        x = solve_square([[Fr(v) for v in A[i]] for i in sub], [Fr(b[i]) for i in sub])
        if x is not None and all(sum(Fr(a) * y for a, y in zip(A[i], x)) >= b[i] for i in range(len(A))):
            out.add(tuple(x))
    return sorted(out)


def front_vertices_2d(A, b, C):
    """Vertices of the upper image for p = 2, sorted by y1: the images of the
    vertices of X that no other image or segment between images dominates."""
    S = sorted({tuple(sum(Fr(c) * x for c, x in zip(row, v)) for row in C) for v in poly_vertices(A, b)})
    # Lower-left convex chain: keep the points that are not dominated, then
    # remove those above the chain (a convex hull scan).
    nd = [s for s in S if not any(q != s and q[0] <= s[0] and q[1] <= s[1] for q in S)]
    hull = []
    for s in nd:
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = hull[-2], hull[-1]
            if (x2 - x1) * (s[1] - y1) - (y2 - y1) * (s[0] - x1) <= 0:
                hull.pop()
            else:
                break
        hull.append(s)
    return hull


def dominated_gap(A, b, C, y):
    """max sum(s) s.t. C x + s = y, A x >= b, s >= 0; positive iff y is dominated."""
    n, p = len(A[0]), len(C)
    Az = [list(row) + [0] * p for row in A] + [[0] * n + [int(i == j) for j in range(p)] for i in range(p)]
    bz = list(b) + [0] * p
    E = [list(C[i]) + [int(i == j) for j in range(p)] for i in range(p)]
    st, val, _ = lp_min(Az, bz, E, list(y), [0] * n + [-1] * p)
    assert st == "optimal"
    return -val


def random_molp(rng, p):
    n = rng.randint(2, 3)
    A, b = [], []
    for j in range(n):
        e = [int(i == j) for i in range(n)]
        A += [e, [-x for x in e]]
        b += [0, -rng.randint(2, 4)]
    for _ in range(rng.randint(1, 3)):
        A.append([rng.randint(-2, 3) for _ in range(n)])
        b.append(rng.randint(-4, 4))
    C = [[rng.randint(-2, 3) for _ in range(n)] for _ in range(p)]
    return A, b, C


def test_grid() -> None:
    for p in range(1, 5):
        for H in range(1, 6):
            g = simplex_grid(p, H)
            assert len(g) == len(set(g)) == comb(H + p - 1, p - 1)
            assert all(sum(beta) == 1 and min(beta) >= 0 for beta in g)


def test_example() -> None:
    # minimize (x1, x2) over x >= 0, x1 + 2 x2 >= 4, 3 x1 + x2 >= 6.
    A = [[1, 0], [0, 1], [1, 2], [3, 1]]
    b = [0, 0, 4, 6]
    Fstar, Phi, pts = nbi(A, b, [[1, 0], [0, 1]], 4)
    assert Fstar == [0, 0] and Phi == [[0, 4], [6, 0]]
    assert [t for _, t, _ in pts] == [0, Fr(1, 12), Fr(1, 6), Fr(1, 8), 0]
    assert [y for _, _, y in pts] == [(0, 6), (Fr(2, 3), 4), (Fr(4, 3), 2), (Fr(5, 2), Fr(3, 4)), (4, 0)]


def test_two_objectives_against_segment_intersection() -> None:
    rng = random.Random(1998)
    done = 0
    while done < 40:
        A, b, C = random_molp(rng, 2)
        if not poly_vertices(A, b):
            continue
        done += 1
        Fstar, Phi, pts = nbi(A, b, C, 5)
        chain = front_vertices_2d(A, b, C)
        assert Fstar == [chain[0][0], chain[-1][1]]
        normal = [-sum(row) for row in Phi]
        for beta, t, y in pts:
            q = [Fstar[i] + sum(Phi[i][j] * beta[j] for j in range(2)) for i in range(2)]
            if len(chain) == 1:
                assert y == chain[0]
                continue
            hits = set()
            for P, Q in zip(chain, chain[1:]):
                # q + t n = P + s (Q - P)
                sol = solve_square([[normal[0], P[0] - Q[0]], [normal[1], P[1] - Q[1]]], [P[0] - q[0], P[1] - q[1]])
                if sol is not None and 0 <= sol[1] <= 1:
                    hits.add(sol[0])
            assert hits == {t}, (A, b, C, beta)
            assert t >= 0
            assert y == tuple(q[i] + t * normal[i] for i in range(2))
            assert dominated_gap(A, b, C, y) == 0  # Pareto optimal for p = 2


def test_three_objectives_can_give_dominated_points() -> None:
    # X is the tetrahedron with the vertices (0,2,2), (2,0,2), (2,2,0), (1,1,1).
    A = [[1, 1, 0], [1, 0, 1], [0, 1, 1], [-1, -1, -1]]
    b = [2, 2, 2, -4]
    C = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    Fstar, Phi, pts = nbi(A, b, C, 2)
    assert Fstar == [0, 0, 0]
    ys = [y for _, _, y in pts]
    assert ys == [(0, 2, 2), (1, 1, 2), (1, 2, 1), (2, 0, 2), (2, 1, 1), (2, 2, 0)]
    assert [dominated_gap(A, b, C, y) for y in ys] == [0, 1, 1, 0, 1, 0]
    # A finer grid has the centre of the simplex, whose normal line hits (1,1,1).
    _, _, pts = nbi(A, b, C, 3)
    centre = [(t, y) for beta, t, y in pts if beta == (Fr(1, 3),) * 3]
    assert centre == [(Fr(1, 12), (1, 1, 1))]


def test_points_lie_on_their_normal_lines() -> None:
    rng = random.Random(7)
    done = 0
    while done < 20:
        A, b, C = random_molp(rng, 3)
        if not poly_vertices(A, b):
            continue
        done += 1
        Fstar, Phi, pts = nbi(A, b, C, 3)
        normal = [-sum(row) for row in Phi]
        for j in range(3):  # the anchors are Pareto optimal
            beta = tuple(Fr(int(i == j)) for i in range(3))
            y = next(y for bb, _, y in pts if bb == beta)
            assert dominated_gap(A, b, C, y) == 0
            assert y[j] == Fstar[j]
        for beta, t, y in pts:
            assert t >= 0
            assert y == tuple(Fstar[i] + sum(Phi[i][j] * beta[j] for j in range(3)) + t * normal[i] for i in range(3))
