# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-refinement/. The authors are listed in prov/H90MTM.jsonl.

import random
from fractions import Fraction as F

from k_refinement import (
    derivative,
    distinct,
    elevate,
    elevate_bezier,
    eval_piece,
    evaluate,
    find_span,
    h_then_p,
    insert_knot,
    jumps,
    k_refine,
    solve_exact,
)


def cox_de_boor(t, i, p, u):
    """N_{i,p}(u) by the recursion, half-open spans, closed at the right end."""
    if p == 0:
        if t[i] <= u < t[i + 1]:
            return F(1)
        last = max(k for k in range(len(t) - 1) if t[k] < t[k + 1])
        return F(int(i == last and u == t[-1]))
    s = F(0)
    if t[i + p] > t[i]:
        s += (u - t[i]) / (t[i + p] - t[i]) * cox_de_boor(t, i, p - 1, u)
    if t[i + p + 1] > t[i + 1]:
        s += (t[i + p + 1] - u) / (t[i + p + 1] - t[i + 1]) * cox_de_boor(t, i + 1, p - 1, u)
    return s


def curve_by_basis(t, p, P, u):
    u = F(u)
    vals = [cox_de_boor(t, i, p, u) for i in range(len(P))]
    return tuple(sum(v * q[c] for v, q in zip(vals, P)) for c in range(len(P[0])))


def random_curve(rng, p):
    inner = sorted(F(rng.randint(1, 11), 12) for _ in range(rng.randint(0, 4)))
    t = [F(0)] * (p + 1)
    for x in inner:
        if t.count(x) < p:
            t.append(x)
    t += [F(1)] * (p + 1)
    t.sort()
    n = len(t) - p - 1
    P = [(F(rng.randint(-9, 9)), F(rng.randint(-9, 9))) for _ in range(n)]
    return t, P


def params(rng, t, count=25):
    us = [F(rng.randint(0, 600), 600) for _ in range(count)]
    return us + [x for x, _ in distinct(t)]


def test_de_boor_matches_cox_de_boor():
    rng = random.Random(1)
    for p in (1, 2, 3):
        t, P = random_curve(rng, p)
        for u in params(rng, t, 10):
            assert evaluate(t, p, P, u) == curve_by_basis(t, p, P, u)


def test_knot_insertion_keeps_curve():
    rng = random.Random(2)
    for p in (1, 2, 3):
        for _ in range(5):
            t, P = random_curve(rng, p)
            x = F(rng.randint(1, 23), 24)
            t2, Q = insert_knot(t, p, P, x)
            assert len(Q) == len(P) + 1
            for u in params(rng, t2):
                assert evaluate(t2, p, Q, u) == evaluate(t, p, P, u)


def test_elevate_bezier_matches_bernstein_identity():
    Q = [(F(0), F(0)), (F(1), F(3)), (F(4), F(-2))]
    R = elevate_bezier(Q)
    assert R == [(F(0), F(0)), (F(2, 3), F(2)), (F(2), F(4, 3)), (F(4), F(-2))]
    t2, t3 = [F(0)] * 3 + [F(1)] * 3, [F(0)] * 4 + [F(1)] * 4
    for k in range(11):
        u = F(k, 10)
        assert evaluate(t3, 3, R, u) == evaluate(t2, 2, Q, u)


def test_elevation_keeps_curve_and_continuity():
    rng = random.Random(3)
    for p in (1, 2, 3):
        for _ in range(4):
            t, P = random_curve(rng, p)
            t2, P2 = elevate(t, p, P)
            assert [(x, m + 1) for x, m in distinct(t)] == distinct(t2)
            for u in params(rng, t2):
                assert evaluate(t2, p + 1, P2, u) == evaluate(t, p, P, u)


def test_elevation_against_collocation():
    """The elevated coefficients are unique, so a direct solve must give them."""
    rng = random.Random(4)
    for p in (1, 2, 3):
        t, P = random_curve(rng, p)
        t2, P2 = elevate(t, p, P)
        q = p + 1
        n = len(t2) - q - 1
        gre = [sum(t2[i + 1 : i + q + 1]) / q for i in range(n)]
        A = [[cox_de_boor(t2, j, q, u) for j in range(n)] for u in gre]
        B = [evaluate(t, p, P, u) for u in gre]
        assert solve_exact(A, B) == P2


def test_k_refinement_keeps_curve_and_gives_c_p_minus_1():
    rng = random.Random(5)
    for p in (1, 2):
        for r in (1, 2):
            t, P = random_curve(rng, p)
            old = {x for x, _ in distinct(t)}
            X = sorted({F(rng.randint(1, 47), 48) for _ in range(3)} - old)
            t2, q, P2 = k_refine(t, p, P, r, X)
            assert q == p + r
            for u in params(rng, t2):
                assert evaluate(t2, q, P2, u) == evaluate(t, p, P, u)
            mult = dict(distinct(t2))
            for x in X:
                assert mult[x] == 1
                J = jumps(t2, q, P2, x, list(range(q + 1)))
                assert all(v == 0 for j in J[:q] for v in j)  # C^(q-1)
            for x, m in distinct(t)[1:-1]:
                assert mult[x] == m + r


def test_other_order_is_a_bigger_less_smooth_space():
    rng = random.Random(6)
    for p in (1, 2):
        for r in (1, 2):
            t, P = random_curve(rng, p)
            old = {x for x, _ in distinct(t)}
            X = sorted({F(rng.randint(1, 47), 48) for _ in range(3)} - old)
            tk, qk, Pk = k_refine(t, p, P, r, X)
            th, qh, Ph = h_then_p(t, p, P, r, X)
            assert qk == qh
            assert len(Ph) - len(Pk) == r * len(X)
            for x in X:
                assert dict(distinct(th))[x] == r + 1  # only C^(p-1) there
            for u in params(rng, th):
                assert evaluate(th, qh, Ph, u) == evaluate(tk, qk, Pk, u)


def test_small_example_counts():
    t = [F(0), F(0), F(1), F(1)]
    P = [(F(0),), (F(1),)]
    tk, qk, Pk = k_refine(t, 1, P, 1, [F(1, 2)])
    th, qh, Ph = h_then_p(t, 1, P, 1, [F(1, 2)])
    assert tk == [0, 0, 0, F(1, 2), 1, 1, 1] and len(Pk) == 4
    assert th == [0, 0, 0, F(1, 2), F(1, 2), 1, 1, 1] and len(Ph) == 5
    for n_el in (1, 2, 4, 8):
        X = [F(i, n_el) for i in range(1, n_el)]
        for q in (2, 3, 4):
            assert len(k_refine(t, 1, P, q - 1, X)[2]) == n_el + q
            assert len(h_then_p(t, 1, P, q - 1, X)[2]) == q * n_el + 1


def test_derivative_and_spans():
    t = [F(0)] * 3 + [F(1, 2)] + [F(1)] * 3
    P = [(F(0),), (F(1),), (F(3),), (F(2),)]
    assert find_span(t, 2, F(1)) == 3
    td, pd, D = derivative(t, 2, P)
    h = F(1, 1000)
    for u in (F(1, 4), F(3, 4)):
        k = find_span(t, 2, u)
        num = (eval_piece(t, 2, P, k, u + h)[0] - eval_piece(t, 2, P, k, u - h)[0]) / (2 * h)
        assert num == evaluate(td, pd, D, u)[0]  # exact for a quadratic piece
