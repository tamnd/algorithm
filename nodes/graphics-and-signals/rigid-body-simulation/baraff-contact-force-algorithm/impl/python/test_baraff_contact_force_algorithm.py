# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baraff-contact-force-algorithm/. The authors are listed in prov/APAZTF.jsonl.

import itertools
import random
from fractions import Fraction as F

from baraff_contact_force_algorithm import box_contact_matrix, compute_forces, is_solution, matvec, solve


def random_matrix(rng, rows, cols):
    return [[F(rng.randint(-6, 6), rng.randint(1, 3)) for _ in range(cols)] for _ in range(rows)]


def gram(J):
    """J J^T: symmetric positive semidefinite, of rank rank(J)."""
    return [[sum(x * y for x, y in zip(ri, rj)) for rj in J] for ri in J]


def brute_force(A, b):
    """All solutions of the LCP over the 2^n choices of the support of f, for a nonsingular A."""
    n = len(b)
    out = []
    for size in range(n + 1):
        for S in itertools.combinations(range(n), size):
            f = [F(0)] * n
            if S:
                try:
                    x = solve([[A[i][j] for j in S] for i in S], [-b[i] for i in S])
                except ZeroDivisionError:
                    continue
                for i, xi in zip(S, x):
                    f[i] = xi
            a = [p + q for p, q in zip(matvec(A, f), b)]
            if is_solution(A, b, f, a):
                out.append(f)
    return out


def test_page_example_box_tips():
    A = box_contact_matrix(1, F(5, 12), [-1, 0, 1])
    alpha = F(-15) / F(5, 12)
    b = [F(-10) + alpha * x for x in (-1, 0, 1)]
    assert b == [26, -10, -46]
    trace = []
    f, a, C = compute_forces(A, b, trace)
    assert trace == [(1, 1, "d to C", 10), (2, 1, "C to NC", 10), (2, 2, "d to C", F(60, 17))]
    assert f == [0, 0, F(230, 17)]
    assert a == [F(120, 17), F(60, 17), 0]
    assert C == {2}


def test_positive_definite_matches_brute_force():
    rng = random.Random(1)
    for _ in range(80):
        n = rng.randint(1, 5)
        A = gram(random_matrix(rng, n, n + 1))
        b = [F(rng.randint(-12, 12), rng.randint(1, 3)) for _ in range(n)]
        try:
            solve(A, [F(1)] * n)
        except ZeroDivisionError:
            continue
        sols = {tuple(s) for s in brute_force(A, b)}
        f, a, _ = compute_forces(A, b)
        assert is_solution(A, b, f, a)
        assert sols == {tuple(f)}


def test_semidefinite_resting_box_has_zero_acceleration():
    rng = random.Random(3)
    for _ in range(40):
        m, I = F(rng.randint(1, 4)), F(rng.randint(1, 6), 4)
        xs = sorted({F(rng.randint(-8, 8), 4) for _ in range(rng.randint(3, 5))})
        if len(xs) < 3 or xs[0] >= 0 or xs[-1] <= 0:
            continue
        torque = F(rng.randint(-10, 10), 4)
        if not xs[0] * m * 10 < torque < xs[-1] * m * 10:
            torque = 0
        acc_y, alpha = F(-10), torque / I
        A = box_contact_matrix(m, I, xs)
        b = [acc_y + alpha * x for x in xs]
        f, a, _ = compute_forces(A, b)
        assert is_solution(A, b, f, a)
        assert acc_y + sum(f) / m == 0
        assert alpha + sum(fi * x for fi, x in zip(f, xs)) / I == 0


def test_semidefinite_all_solutions_share_the_accelerations():
    rng = random.Random(5)
    for _ in range(60):
        n = rng.randint(2, 6)
        J = random_matrix(rng, n, rng.randint(1, n - 1))
        A = gram(J)
        w = [F(rng.randint(-6, 6), 2) for _ in range(len(J[0]))]
        b = [sum(x * y for x, y in zip(row, w)) for row in J]  # b = J w lies in the column space of A
        f, a, _ = compute_forces(A, b)
        assert is_solution(A, b, f, a)
        perm = list(range(n))
        rng.shuffle(perm)
        Ap = [[A[i][j] for j in perm] for i in perm]
        bp = [b[i] for i in perm]
        fp, ap, _ = compute_forces(Ap, bp)
        assert is_solution(Ap, bp, fp, ap)
        assert [ap[perm.index(i)] for i in range(n)] == a


def test_each_drive_adds_one_processed_index():
    rng = random.Random(7)
    for _ in range(60):
        n = rng.randint(2, 7)
        A = gram(random_matrix(rng, n, n))
        b = [F(rng.randint(-12, 12), rng.randint(1, 3)) for _ in range(n)]
        trace = []
        try:
            f, a, _ = compute_forces(A, b, trace)
        except ZeroDivisionError:
            continue
        driven = [d for d, j, move, _ in trace if move == "d to C"]
        assert len(driven) == len(set(driven)) <= n
        assert all(s >= 0 for *_, s in trace)


def test_nonnegative_b_needs_no_force():
    A = box_contact_matrix(2, F(1, 3), [F(-1, 2), F(1, 2)])
    f, a, C = compute_forces(A, [F(3), F(0)])
    assert f == [0, 0] and a == [3, 0] and C == set()
