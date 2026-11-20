# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lemke-algorithm/. The authors are listed in prov/8FV1QP.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from agtgame import from_bimatrix, is_nash
from agtlp import lp_max
from lemke_algorithm import bimatrix_equilibrium, bimatrix_lcp, lemke

F = Fraction


def solve_square(K, b):
    r = len(K)
    rows = [[F(v) for v in K[k]] + [F(b[k])] for k in range(r)]
    for col in range(r):
        p = next((k for k in range(col, r) if rows[k][col] != 0), None)
        if p is None:
            return None
        rows[col], rows[p] = rows[p], rows[col]
        rows[col] = [v / rows[col][col] for v in rows[col]]
        for k in range(r):
            f = rows[k][col]
            if k != col and f != 0:
                rows[k] = [a - f * c for a, c in zip(rows[k], rows[col])]
    return [rows[k][-1] for k in range(r)]


def is_lcp_solution(M, q, z, w):
    n = len(q)
    return (all(v >= 0 for v in z) and all(v >= 0 for v in w)
            and all(w[i] == sum(F(M[i][j]) * z[j] for j in range(n)) + q[i] for i in range(n))
            and sum(a * b for a, b in zip(z, w)) == 0)


def brute_force(M, q):
    """All solutions found from the 2^n complementary bases with a nonsingular principal block."""
    n = len(q)
    out = []
    for k in range(n + 1):
        for S in combinations(range(n), k):
            z = [F(0)] * n
            if S:
                sol = solve_square([[M[i][j] for j in S] for i in S], [-q[i] for i in S])
                if sol is None:
                    continue
                for i, v in zip(S, sol):
                    z[i] = v
            w = [sum(F(M[i][j]) * z[j] for j in range(n)) + q[i] for i in range(n)]
            if is_lcp_solution(M, q, z, w) and z not in out:
                out.append(z)
    return out


def random_q(rng, n):
    return [F(rng.randint(-6, 6)) for _ in range(n)]


def test_trivial_and_page_example():
    assert lemke([[2, 1], [1, 2]], [1, 0]) == ("solution", [0, 0], [1, 0])
    trace = []
    status, z, w = lemke([[2, 1], [1, 2]], [-1, 1], trace=trace)
    assert status == "solution" and z == [F(1, 2), 0] and w == [0, F(3, 2)]
    assert trace == [(4, 0), (2, 4)]  # z0 enters for w_0, then z_0 enters and z0 leaves


def test_ray_when_infeasible():
    # w = -z - 1 >= 0 has no solution with z >= 0.
    assert lemke([[-1]], [-1])[0] == "ray"
    assert lemke([[0, 0], [0, 0]], [-1, 2])[0] == "ray"


def test_positive_definite_unique_solution():
    rng = random.Random(1201)
    for _ in range(120):
        n = rng.randint(1, 5)
        G = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)]
        S = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)]
        # M = G G^T + I plus a skew part: x^T M x > 0 for x != 0, so M is a P-matrix.
        M = [[sum(G[i][k] * G[j][k] for k in range(n)) + int(i == j) + S[i][j] - S[j][i]
              for j in range(n)] for i in range(n)]
        q = random_q(rng, n)
        status, z, w = lemke(M, q)
        assert status == "solution" and is_lcp_solution(M, q, z, w)
        assert brute_force(M, q) == [z]


def test_p_matrix_not_symmetric():
    # Strictly row diagonally dominant with a positive diagonal: a P-matrix.
    rng = random.Random(77)
    for _ in range(120):
        n = rng.randint(1, 5)
        M = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            M[i][i] = sum(abs(M[i][j]) for j in range(n) if j != i) + rng.randint(1, 3)
        q = random_q(rng, n)
        status, z, w = lemke(M, q)
        assert status == "solution" and is_lcp_solution(M, q, z, w)
        assert brute_force(M, q) == [z]


def test_positive_semidefinite_ray_means_infeasible():
    rng = random.Random(9)
    rays = sols = 0
    for _ in range(200):
        n = rng.randint(1, 4)
        r = rng.randint(1, n)
        G = [[rng.randint(-2, 2) for _ in range(r)] for _ in range(n)]
        M = [[sum(G[i][k] * G[j][k] for k in range(r)) for j in range(n)] for i in range(n)]
        q = random_q(rng, n)
        status, z, w = lemke(M, q)
        # Feasibility of z >= 0, M z + q >= 0, that is, -M z <= q.
        feasible = lp_max([0] * n, [[-v for v in row] for row in M], q)[0] == "optimal"
        if status == "solution":
            sols += 1
            assert is_lcp_solution(M, q, z, w)
        else:
            rays += 1
            assert not feasible and brute_force(M, q) == []
        assert (status == "solution") == feasible
    assert rays > 10 and sols > 10


def test_general_matrices_outputs_are_solutions():
    rng = random.Random(31)
    for _ in range(300):
        n = rng.randint(1, 4)
        M = [[rng.randint(-4, 4) for _ in range(n)] for _ in range(n)]
        q = random_q(rng, n)
        status, z, w = lemke(M, q)
        if status == "solution":
            assert is_lcp_solution(M, q, z, w)


def test_degenerate_q_ties():
    for n in range(1, 6):
        M = [[int(i == j) + int(j == (i + 1) % n) for j in range(n)] for i in range(n)]
        q = [F(-1)] * n
        status, z, w = lemke(M, q)
        assert status == "solution" and is_lcp_solution(M, q, z, w)


def support_enumeration(A, B):
    m, n = len(A), len(A[0])
    out = []
    for k in range(1, min(m, n) + 1):
        for I in combinations(range(m), k):
            for J in combinations(range(n), k):
                sy = solve_square([[A[i][j] for j in J] + [-1] for i in I] + [[1] * k + [0]], [0] * k + [1])
                sx = solve_square([[B[i][j] for i in I] + [-1] for j in J] + [[1] * k + [0]], [0] * k + [1])
                if sy is None or sx is None or min(sy[:k]) <= 0 or min(sx[:k]) <= 0:
                    continue
                x, y = [F(0)] * m, [F(0)] * n
                for i, p in zip(I, sx):
                    x[i] = p
                for j, p in zip(J, sy):
                    y[j] = p
                if all(sum(A[i][j] * y[j] for j in J) <= sy[k] for i in range(m)) and \
                        all(sum(x[i] * B[i][j] for i in I) <= sx[k] for j in range(n)):
                    out.append((tuple(x), tuple(y)))
    return out


def nondegenerate(A, B):
    m, n = len(A), len(A[0])
    for P, r, c in (([[B[i][j] for i in range(m)] for j in range(n)], m, n), (A, n, m)):
        for s in range(1, r + 1):
            for I in combinations(range(r), s):
                for J in combinations(range(c), s):
                    sol = solve_square([[P[j][i] for i in I] + [-1] for j in J] + [[1] * s + [0]], [0] * s + [1])
                    if sol is None:
                        if s == 1:
                            continue
                        return False
                    z, u = sol[:s], sol[s]
                    if min(z) <= 0:
                        continue
                    pay = [sum(P[j][i] * zi for i, zi in zip(I, z)) for j in range(c)]
                    if max(pay) == u and sum(1 for v in pay if v == u) > s:
                        return False
    return True


def test_bimatrix_games_against_support_enumeration():
    A = [[3, 3], [2, 5], [0, 6]]
    B = [[3, 2], [2, 6], [3, 1]]
    x, y = bimatrix_equilibrium(A, B)
    assert (tuple(x), tuple(y)) in support_enumeration(A, B)
    rng = random.Random(606)
    done = 0
    while done < 60:
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        A = [[rng.randint(-20, 20) for _ in range(n)] for _ in range(m)]
        B = [[rng.randint(-20, 20) for _ in range(n)] for _ in range(m)]
        if not nondegenerate(A, B):
            continue
        done += 1
        M, q = bimatrix_lcp(A, B)
        assert all(v > 0 for row in M for v in row) and q == [-1] * (m + n)
        x, y = bimatrix_equilibrium(A, B)
        assert is_nash(from_bimatrix(A, B), [x, y])
        assert (tuple(x), tuple(y)) in support_enumeration(A, B)


def test_plain_bimatrix_lcp_can_end_on_a_ray():
    # M = [[0, C], [D^T, 0]] with positive costs is copositive but not copositive-plus,
    # and Lemke's method with d = 1 can end on a secondary ray on it.
    A = [[1, 0, 0], [2, 0, 0]]
    B = [[0, 0, 2], [0, 1, 2]]
    m, n, c = 2, 3, 3
    M = [[0] * (m + n) for _ in range(m + n)]
    for i in range(m):
        for j in range(n):
            M[i][m + j] = c - A[i][j]
            M[m + j][i] = c - B[i][j]
    assert lemke(M, [-1] * (m + n))[0] == "ray"
    x, y = bimatrix_equilibrium(A, B)
    assert is_nash(from_bimatrix(A, B), [x, y])


def test_bimatrix_degenerate_games():
    rng = random.Random(8)
    for _ in range(100):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        A = [[rng.randint(0, 2) for _ in range(n)] for _ in range(m)]
        B = [[rng.randint(0, 2) for _ in range(n)] for _ in range(m)]
        x, y = bimatrix_equilibrium(A, B)
        assert is_nash(from_bimatrix(A, B), [x, y])


def test_bad_covering_vector():
    try:
        lemke([[1]], [-1], d=[0])
    except ValueError:
        return
    raise AssertionError("expected ValueError")
