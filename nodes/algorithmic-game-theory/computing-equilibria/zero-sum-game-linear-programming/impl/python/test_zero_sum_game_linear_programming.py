# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zero-sum-game-linear-programming/. The authors are listed in prov/6NAYNS.jsonl.
"""Tests of the page algorithm and of the shared helper agtlp."""

import random
from fractions import Fraction
from itertools import combinations

from agtgame import from_bimatrix, is_nash
from agtlp import lp_max, lp_min
from zero_sum_game_linear_programming import column_player_lp, guarantees, zero_sum_lp

F = Fraction


# Exact linear algebra for the brute force checks.

def _det(K):
    K = [list(row) for row in K]
    r = len(K)
    d = F(1)
    for col in range(r):
        p = next((k for k in range(col, r) if K[k][col] != 0), None)
        if p is None:
            return F(0)
        if p != col:
            K[col], K[p] = K[p], K[col]
            d = -d
        d *= K[col][col]
        for k in range(col + 1, r):
            f = K[k][col] / K[col][col]
            if f:
                K[k] = [a - f * b for a, b in zip(K[k], K[col])]
    return d


def _solve_square(K, b):
    """Return the unique solution of K z = b, or None if K is singular."""
    r = len(K)
    rows = [list(K[k]) + [b[k]] for k in range(r)]
    for col in range(r):
        p = next((k for k in range(col, r) if rows[k][col] != 0), None)
        if p is None:
            return None
        rows[col], rows[p] = rows[p], rows[col]
        pv = rows[col][col]
        rows[col] = [v / pv for v in rows[col]]
        for k in range(r):
            f = rows[k][col]
            if k != col and f:
                rows[k] = [a - f * c for a, c in zip(rows[k], rows[col])]
    return [rows[k][-1] for k in range(r)]


def _reduce(rows, rhs):
    """Drop dependent rows of rows z = rhs. Return (rows, rhs), or None if inconsistent."""
    keep_r, keep_b = [], []
    work = []
    for row, b in zip(rows, rhs):
        v = list(row) + [b]
        for piv, w in work:
            if v[piv]:
                f = v[piv] / w[piv]
                v = [a - f * c for a, c in zip(v, w)]
        piv = next((j for j in range(len(row)) if v[j] != 0), None)
        if piv is None:
            if v[-1] != 0:
                return None
            continue
        work.append((piv, v))
        keep_r.append(list(row))
        keep_b.append(b)
    return keep_r, keep_b


def _vertices(rows, rhs, ncols):
    """Yield every basic feasible solution of rows z = rhs, z >= 0."""
    red = _reduce(rows, rhs)
    if red is None:
        return
    rows, rhs = red
    r = len(rows)
    if r == 0:
        yield [F(0)] * ncols
        return
    for cols in combinations(range(ncols), r):
        K = [[rows[i][j] for j in cols] for i in range(r)]
        z = _solve_square(K, rhs)
        if z is not None and all(v >= 0 for v in z):
            full = [F(0)] * ncols
            for j, v in zip(cols, z):
                full[j] = v
            yield full


def brute_lp_max(c, A_ub, b_ub, A_eq, b_eq):
    """Return (status, value) by enumeration of all bases of the primal and the dual."""
    n, m1, m2 = len(c), len(A_ub), len(A_eq)
    A_ub = [[F(v) for v in row] for row in A_ub]
    A_eq = [[F(v) for v in row] for row in A_eq]
    b_ub, b_eq = [F(v) for v in b_ub], [F(v) for v in b_eq]
    rows = [list(A_ub[i]) + [F(int(k == i)) for k in range(m1)] for i in range(m1)]
    rows += [list(A_eq[i]) + [F(0)] * m1 for i in range(m2)]
    best = None
    for z in _vertices(rows, list(b_ub) + list(b_eq), n + m1):
        val = sum((F(c[j]) * z[j] for j in range(n)), F(0))
        if best is None or val > best:
            best = val
    if best is None:
        return "infeasible", None
    # Dual: A_ub^T u + A_eq^T (p - q) - t = c with u, p, q, t >= 0.
    drows = []
    for j in range(n):
        drows.append([F(A_ub[i][j]) for i in range(m1)] + [F(A_eq[i][j]) for i in range(m2)]
                     + [-F(A_eq[i][j]) for i in range(m2)] + [F(-int(k == j)) for k in range(n)])
    if next(_vertices(drows, [F(v) for v in c], m1 + 2 * m2 + n), None) is None:
        return "unbounded", None
    return "optimal", best


def check_certificate(c, A_ub, b_ub, A_eq, b_eq, x, value, dual, maximize=True):
    n, m1, m2 = len(c), len(A_ub), len(A_eq)
    A = [list(map(F, r)) for r in A_ub] + [list(map(F, r)) for r in A_eq]
    b = [F(v) for v in b_ub] + [F(v) for v in b_eq]
    assert len(x) == n and len(dual) == m1 + m2
    assert all(v >= 0 for v in x)
    ax = [sum((A[i][j] * x[j] for j in range(n)), F(0)) for i in range(m1 + m2)]
    assert all(ax[i] <= b[i] for i in range(m1))
    assert all(ax[i] == b[i] for i in range(m1, m1 + m2))
    assert sum((F(c[j]) * x[j] for j in range(n)), F(0)) == value
    # Strong duality.
    assert sum((b[i] * dual[i] for i in range(m1 + m2)), F(0)) == value
    aty = [sum((A[i][j] * dual[i] for i in range(m1 + m2)), F(0)) for j in range(n)]
    for i in range(m1):
        assert dual[i] >= 0 if maximize else dual[i] <= 0
        assert dual[i] * (b[i] - ax[i]) == 0  # complementary slackness
    for j in range(n):
        assert aty[j] >= c[j] if maximize else aty[j] <= c[j]
        assert x[j] * (aty[j] - c[j]) == 0  # complementary slackness


def random_lp(rng):
    n = rng.randint(1, 3)
    m1 = rng.randint(0, 3)
    m2 = rng.randint(0, 2)
    c = [rng.randint(-3, 3) for _ in range(n)]
    A_ub = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(m1)]
    b_ub = [rng.randint(-2, 4) for _ in range(m1)]
    A_eq = [[rng.randint(-2, 2) for _ in range(n)] for _ in range(m2)]
    b_eq = [rng.randint(-2, 3) for _ in range(m2)]
    if m2 and rng.random() < 0.2:  # a redundant equation
        A_eq.append([2 * v for v in A_eq[0]])
        b_eq.append(2 * b_eq[0])
    if m1 and rng.random() < 0.3:  # zero right sides make degenerate vertices
        b_ub = [0 if rng.random() < 0.6 else v for v in b_ub]
    return c, A_ub, b_ub, A_eq, b_eq


def test_helper_against_brute_force():
    rng = random.Random(7101)
    seen = set()
    for _ in range(1500):
        c, A_ub, b_ub, A_eq, b_eq = random_lp(rng)
        status, x, value, dual = lp_max(c, A_ub, b_ub, A_eq, b_eq)
        want, best = brute_lp_max(c, A_ub, b_ub, A_eq, b_eq)
        assert status == want
        seen.add(status)
        if status == "optimal":
            assert value == best
            check_certificate(c, A_ub, b_ub, A_eq, b_eq, x, value, dual)
        else:
            assert x is None and value is None and dual is None
        # lp_min of c is minus lp_max of -c.
        s2, x2, v2, d2 = lp_min([-v for v in c], A_ub, b_ub, A_eq, b_eq)
        assert s2 == status
        if s2 == "optimal":
            assert v2 == -value
            check_certificate([-v for v in c], A_ub, b_ub, A_eq, b_eq, x2, v2, d2, maximize=False)
    assert seen == {"optimal", "infeasible", "unbounded"}


def test_helper_beale_cycling_example():
    # Beale's example makes the simplex method cycle under the largest coefficient rule.
    c = [F(-3, 4), 20, F(-1, 2), 6]
    A_ub = [[F(1, 4), -8, -1, 9], [F(1, 2), -12, F(-1, 2), 3], [0, 0, 1, 0]]
    b_ub = [0, 0, 1]
    status, x, value, dual = lp_min(c, A_ub, b_ub)
    assert status == "optimal" and value == F(-5, 4)
    assert x == [1, 0, 1, 0]
    check_certificate(c, A_ub, b_ub, [], [], x, value, dual, maximize=False)
    assert brute_lp_max([-v for v in c], A_ub, b_ub, [], []) == ("optimal", F(5, 4))


def test_helper_small_cases():
    assert lp_max([1], [], [])[0] == "unbounded"
    assert lp_max([-1], [], []) == ("optimal", [0], 0, [])
    assert lp_max([1, 1], [[1, 0]], [-1])[0] == "infeasible"
    assert lp_max([1, 0], [[1, -1]], [1])[0] == "unbounded"
    assert lp_max([1, 1], [], [], [[1, 1], [2, 2]], [1, 2])[2] == 1
    assert lp_max([1, 1], [], [], [[1, 1], [1, 1]], [1, 2])[0] == "infeasible"
    s, x, v, d = lp_max([3, 2], [[1, 1], [1, 3]], [4, 6])
    assert (s, x, v) == ("optimal", [4, 0], 12)
    check_certificate([3, 2], [[1, 1], [1, 3]], [4, 6], [], [], x, v, d)
    s, x, v, d = lp_min([1, 1], [[-1, -2], [-3, -1]], [-4, -6])
    assert (s, x, v) == ("optimal", [F(8, 5), F(6, 5)], F(14, 5))
    assert all(isinstance(t, Fraction) for t in x + d)


# The page algorithm.

def shapley_snow_value(M):
    """Return the value of the matrix game M by brute force over its square submatrices.

    For a square submatrix K with s = 1^T adj(K) 1 != 0, the candidates are v = det(K) / s,
    x = 1^T adj(K) / s and y = adj(K) 1 / s. Shapley and Snow (1950) show that some K gives
    optimal strategies. Each candidate is checked against every row and column.
    """
    k = 1 - min(min(row) for row in M)
    Mp = [[F(v) + k for v in row] for row in M]
    m, n = len(M), len(M[0])
    for r in range(1, min(m, n) + 1):
        for I in combinations(range(m), r):
            for J in combinations(range(n), r):
                K = [[Mp[i][j] for j in J] for i in I]
                d = _det(K)
                if d == 0:
                    continue
                # adj(K) = det(K) K^{-1}, so x and y solve K^T x = 1 and K y = 1, rescaled.
                xs = _solve_square([[K[a][b] for a in range(r)] for b in range(r)], [F(1)] * r)
                ys = _solve_square(K, [F(1)] * r)
                s = sum(xs)
                if s == 0:
                    continue
                v = 1 / s
                x = [F(0)] * m
                y = [F(0)] * n
                for a, i in enumerate(I):
                    x[i] = xs[a] * v
                for b, j in enumerate(J):
                    y[j] = ys[b] * v
                if min(x) < 0 or min(y) < 0:
                    continue
                lo, hi = guarantees(Mp, x, y)
                if lo == hi == v:
                    return v - k
    raise AssertionError("Shapley-Snow found no kernel")


def check_solution(M, value, x, y):
    Mf = [[F(v) for v in row] for row in M]
    assert all(t >= 0 for t in x) and sum(x) == 1
    assert all(t >= 0 for t in y) and sum(y) == 1
    lo, hi = guarantees(Mf, x, y)
    assert lo == value == hi
    # A Nash equilibrium of the bimatrix game (M, -M), checked by pure deviations.
    assert is_nash(from_bimatrix(Mf, [[-v for v in row] for row in Mf]), [x, y])


def test_matching_pennies_and_rps():
    for M in ([[1, -1], [-1, 1]], [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]):
        value, x, y = zero_sum_lp(M)
        k = len(M)
        assert value == 0
        assert x == [F(1, k)] * k and y == [F(1, k)] * k
        check_solution(M, value, x, y)


def test_page_example():
    M = [[3, -1], [-2, 1]]
    value, x, y = zero_sum_lp(M)
    assert value == F(1, 7)
    assert x == [F(3, 7), F(4, 7)]
    assert y == [F(2, 7), F(5, 7)]
    check_solution(M, value, x, y)


def test_saddle_point_and_dominated_rows():
    M = [[4, 2, 3], [1, 0, 5], [3, 1, 2]]
    value, x, y = zero_sum_lp(M)
    assert value == 2 and x == [1, 0, 0] and y == [0, 1, 0]
    check_solution(M, value, x, y)


def test_random_games_against_shapley_snow():
    rng = random.Random(2028)
    for _ in range(150):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        M = [[rng.randint(-5, 5) for _ in range(n)] for _ in range(m)]
        value, x, y = zero_sum_lp(M)
        check_solution(M, value, x, y)
        assert value == shapley_snow_value(M)
        w, y2 = column_player_lp(M)
        assert w == value
        check_solution(M, value, x, y2)
