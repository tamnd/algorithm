# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bezier-extraction/. The authors are listed in prov/5HN7GF.jsonl.

import random
from fractions import Fraction as F

from bezier_extraction import bezier_points, elements, extract, local_basis, rational_local_basis


def cox_de_boor(t, i, p, u):
    """N_{i,p}(u) by the recursion, on half-open spans."""
    if p == 0:
        return F(int(t[i] <= u < t[i + 1]))
    s = F(0)
    if t[i + p] > t[i]:
        s += (u - t[i]) / (t[i + p] - t[i]) * cox_de_boor(t, i, p - 1, u)
    if t[i + p + 1] > t[i + 1]:
        s += (t[i + p + 1] - u) / (t[i + p + 1] - t[i + 1]) * cox_de_boor(t, i + 1, p - 1, u)
    return s


def random_knots(rng, p):
    U = [F(0)] * (p + 1)
    for x in range(1, rng.randint(2, 6)):
        U += [F(x)] * rng.randint(1, p)
    end = U[-1] + 1
    return U + [end] * (p + 1)


def insert(t, p, P, x):
    """Boehm insertion on coefficient vectors (dicts), used as the reference."""
    k = max(i for i in range(len(t) - 1) if t[i] <= x < t[i + 1])
    Q = []
    for i in range(len(P) + 1):
        if i <= k - p:
            Q.append(P[i])
        elif i > k:
            Q.append(P[i - 1])
        else:
            a = (x - t[i]) / (t[i + p] - t[i])
            Q.append({j: (1 - a) * P[i - 1].get(j, 0) + a * P[i].get(j, 0) for j in set(P[i]) | set(P[i - 1])})
    return t[: k + 1] + [x] + t[k + 1 :], Q


def global_extraction(U, p):
    """Reference: insert every interior knot up to multiplicity p over the whole basis."""
    n = len(U) - p - 1
    t, Q = list(U), [{i: F(1)} for i in range(n)]
    for x in sorted(set(U))[1:-1]:
        while t.count(x) < p:
            t, Q = insert(t, p, Q, x)
    out = []
    for e, (k, _, _) in enumerate(elements(U)):
        rows = range(k - p, k + 1)
        out.append([[Q[e * p + j].get(i, F(0)) for j in range(p + 1)] for i in rows])
    return out


def test_paper_example():
    C = extract([0, 0, 0, 0, 1, 2, 3, 4, 4, 4, 4], 3)
    assert len(C) == 4
    assert C[0] == [[1, 0, 0, 0], [0, 1, F(1, 2), F(1, 4)], [0, 0, F(1, 2), F(7, 12)], [0, 0, 0, F(1, 6)]]
    assert C[1] == [[F(1, 4), 0, 0, 0], [F(7, 12), F(2, 3), F(1, 3), F(1, 6)], [F(1, 6), F(1, 3), F(2, 3), F(2, 3)], [0, 0, 0, F(1, 6)]]
    assert C[3] == [list(reversed(r)) for r in reversed(C[0])]


def test_against_cox_de_boor():
    rng = random.Random(7)
    for p in (1, 2, 3, 4):
        for _ in range(3):
            U = random_knots(rng, p)
            C = extract(U, p)
            spans = elements(U)
            assert len(C) == len(spans)
            for Ce, (k, lo, hi) in zip(C, spans):
                for s in [F(0), F(1, 3), F(1, 2), F(5, 7), F(rng.randint(1, 99), 100)]:
                    u = lo + s * (hi - lo)
                    want = [cox_de_boor(U, i, p, u) for i in range(k - p, k + 1)]
                    assert local_basis(Ce, p, s) == want


def test_against_global_knot_insertion():
    rng = random.Random(8)
    for p in (1, 2, 3, 4):
        for _ in range(3):
            U = random_knots(rng, p)
            assert extract(U, p) == global_extraction(U, p)


def test_columns_sum_to_one_and_entries_nonnegative():
    rng = random.Random(9)
    for p in (2, 3, 5):
        U = random_knots(rng, p)
        for Ce in extract(U, p):
            for j in range(p + 1):
                assert sum(Ce[a][j] for a in range(p + 1)) == 1
            assert all(x >= 0 for row in Ce for x in row)


def test_bezier_points_give_the_curve():
    rng = random.Random(10)
    p = 3
    U = random_knots(rng, p)
    n = len(U) - p - 1
    P = [(F(rng.randint(-5, 5)), F(rng.randint(-5, 5))) for _ in range(n)]
    for Ce, (k, lo, hi) in zip(extract(U, p), elements(U)):
        Bz = bezier_points(Ce, P[k - p : k + 1])
        for s in (F(0), F(1, 4), F(2, 3)):
            u = lo + s * (hi - lo)
            want = tuple(sum(cox_de_boor(U, i, p, u) * P[i][c] for i in range(n)) for c in range(2))
            # de Casteljau on the Bezier points
            pts = [list(q) for q in Bz]
            for r in range(1, p + 1):
                pts = [[(1 - s) * x + s * y for x, y in zip(pts[j], pts[j + 1])] for j in range(p + 1 - r)]
            assert tuple(pts[0]) == want


def test_rational_basis():
    p = 2
    U = [0, 0, 0, 1, 2, 2, 2]
    w = [F(1), F(1, 2), F(2), F(1)]
    for Ce, (k, lo, hi) in zip(extract(U, p), elements(U)):
        for s in (F(0), F(1, 5), F(1, 2), F(1)):
            u = lo + s * (hi - lo)
            N = [cox_de_boor(U, i, p, u) if u < 2 else F(int(i == 3)) for i in range(4)]
            W = sum(wi * ni for wi, ni in zip(w, N))
            want = [w[i] * N[i] / W for i in range(k - p, k + 1)]
            if u < 2:
                assert rational_local_basis(Ce, w[k - p : k + 1], p, s) == want
            assert sum(rational_local_basis(Ce, w[k - p : k + 1], p, s)) == 1
