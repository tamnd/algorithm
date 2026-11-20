# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stackelberg-commitment-algorithm/. The authors are listed in prov/3741KV.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from agtlp import lp_max
from stackelberg_commitment_algorithm import best_for_column, follower_response, optimal_commitment

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


def leader_payoff(A, x, j):
    return sum(F(x[i]) * A[i][j] for i in range(len(A)))


def brute_force(A, B):
    """Best leader payoff over the vertices of all regions {x in simplex : j is a best response}."""
    m, n = len(A), len(A[0])
    best = None
    for j in range(n):
        # Constraints: x_i >= 0 and (B[:, j] - B[:, k]) . x >= 0; a vertex makes m - 1 of them tight.
        cons = [[int(t == i) for t in range(m)] for i in range(m)]
        cons += [[B[i][j] - B[i][k] for i in range(m)] for k in range(n) if k != j]
        for S in combinations(range(len(cons)), m - 1):
            x = solve_square([cons[s] for s in S] + [[1] * m], [0] * (m - 1) + [1])
            if x is None or any(sum(F(c[i]) * x[i] for i in range(m)) < 0 for c in cons):
                continue
            v = leader_payoff(A, x, j)
            if best is None or v > best:
                best = v
    return best


def support_enumeration(A, B):
    m, n = len(A), len(A[0])
    out = []
    for k in range(1, min(m, n) + 1):
        for I in combinations(range(m), k):
            for J in combinations(range(n), k):
                sy = solve_square([[A[i][j] for j in J] + [-1] for i in I] + [[1] * k + [0]], [0] * k + [1])
                sx = solve_square([[B[i][j] for i in I] + [-1] for j in J] + [[1] * k + [0]], [0] * k + [1])
                if sy is None or sx is None or min(sy[:k]) < 0 or min(sx[:k]) < 0:
                    continue
                x, y = [F(0)] * m, [F(0)] * n
                for i, p in zip(I, sx):
                    x[i] = p
                for j, p in zip(J, sy):
                    y[j] = p
                if all(sum(A[i][j] * y[j] for j in J) <= sy[k] for i in range(m)) and \
                        all(sum(x[i] * B[i][j] for i in I) <= sx[k] for j in range(n)):
                    out.append((x, y, sy[k]))
    return out


def random_game(rng, m, n, lo=-9, hi=9):
    return ([[rng.randint(lo, hi) for _ in range(n)] for _ in range(m)],
            [[rng.randint(lo, hi) for _ in range(n)] for _ in range(m)])


def check(A, B, value, x, j):
    m, n = len(A), len(A[0])
    assert all(v >= 0 for v in x) and sum(x) == 1
    pay = [sum(x[i] * B[i][k] for i in range(m)) for k in range(n)]
    assert pay[j] == max(pay)
    assert leader_payoff(A, x, j) == value
    assert leader_payoff(A, x, follower_response(A, B, x)) == value


def test_page_example():
    A = [[1, 3], [0, 2]]
    B = [[1, 0], [0, 1]]
    assert best_for_column(A, B, 0) == (1, [1, 0])
    assert best_for_column(A, B, 1) == (F(5, 2), [F(1, 2), F(1, 2)])
    value, x, j = optimal_commitment(A, B)
    assert (value, x, j) == (F(5, 2), [F(1, 2), F(1, 2)], 1)
    check(A, B, value, x, j)
    # The only Nash equilibrium gives the leader 1, and committing to a pure strategy gives 2.
    assert [e[2] for e in support_enumeration(A, B)] == [1]
    assert max(leader_payoff(A, [int(t == i) for t in range(2)],
                             follower_response(A, B, [int(t == i) for t in range(2)])) for i in range(2)) == 2


def test_infeasible_column():
    # Column 1 is strictly dominated for the follower, so its LP is infeasible.
    A = [[0, 9], [1, 9]]
    B = [[1, 0], [1, 0]]
    assert best_for_column(A, B, 1) is None
    assert optimal_commitment(A, B) == (1, [0, 1], 0)


def test_random_games_against_vertex_enumeration():
    rng = random.Random(5150)
    for _ in range(150):
        A, B = random_game(rng, rng.randint(1, 4), rng.randint(1, 4))
        value, x, j = optimal_commitment(A, B)
        check(A, B, value, x, j)
        assert value == brute_force(A, B)


def test_commitment_beats_every_nash_and_pure_commitment():
    rng = random.Random(77)
    for _ in range(100):
        m, n = rng.randint(1, 3), rng.randint(1, 3)
        A, B = random_game(rng, m, n)
        value, _, _ = optimal_commitment(A, B)
        eqs = support_enumeration(A, B)
        assert eqs
        for x, y, _ in eqs:
            assert value >= sum(x[i] * A[i][k] * y[k] for i in range(m) for k in range(n))
        for i in range(m):
            e = [int(t == i) for t in range(m)]
            assert value >= leader_payoff(A, e, follower_response(A, B, e))


def test_zero_sum_value_is_the_minimax_value():
    rng = random.Random(404)
    for _ in range(100):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        A = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(m)]
        B = [[-v for v in row] for row in A]
        value, _, _ = optimal_commitment(A, B)
        # maximize v+ - v- subject to v+ - v- <= sum_i x_i A[i][k] for every k, sum x = 1.
        c = [1, -1] + [0] * m
        A_ub = [[1, -1] + [-A[i][k] for i in range(m)] for k in range(n)]
        status, _, minimax, _ = lp_max(c, A_ub, [0] * n, [[0, 0] + [1] * m], [1])
        assert status == "optimal" and value == minimax


def test_ties_are_broken_for_the_leader():
    # The follower is indifferent between the columns at every x; the leader gets the larger column.
    A = [[1, 4], [2, 0]]
    B = [[5, 5], [5, 5]]
    value, x, j = optimal_commitment(A, B)
    assert (value, x, j) == (4, [1, 0], 1)
