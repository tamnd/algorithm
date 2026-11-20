# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lemke-howson-algorithm/. The authors are listed in prov/W47DAN.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from agtgame import from_bimatrix, is_nash
from lemke_howson_algorithm import all_lemke_howson, lemke_howson

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


def support_enumeration(A, B):
    """Independent check: equilibria from supports of equal size (all of them if nondegenerate)."""
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
                for j, q in zip(J, sy):
                    y[j] = q
                if all(sum(A[i][j] * y[j] for j in J) <= sy[k] for i in range(m)) and \
                        all(sum(x[i] * B[i][j] for i in I) <= sx[k] for j in range(n)):
                    out.append((tuple(x), tuple(y)))
    return out


def nondegenerate(A, B):
    """True if no strategy with support size s has more than s pure best responses (checked on vertices)."""
    m, n = len(A), len(A[0])
    for P, r, c in (([[B[i][j] for i in range(m)] for j in range(n)], m, n), (A, n, m)):
        # P[j][i]: payoff to the responder for response j against the mixer's strategy i.
        for s in range(1, r + 1):
            for I in combinations(range(r), s):
                for J in combinations(range(c), s):
                    sol = solve_square([[P[j][i] for i in I] + [-1] for j in J] + [[1] * s + [0]], [0] * s + [1])
                    if sol is None:
                        if s == 1:
                            continue
                        return False  # a singular system: treat as degenerate to be safe
                    z, u = sol[:s], sol[s]
                    if min(z) <= 0:
                        continue
                    pay = [sum(P[j][i] * zi for i, zi in zip(I, z)) for j in range(c)]
                    if max(pay) == u and sum(1 for v in pay if v == u) > s:
                        return False
    return True


def tup(eq):
    return tuple(eq[0]), tuple(eq[1])


def check(A, B, eq):
    assert is_nash(from_bimatrix(A, B), [eq[0], eq[1]])


def test_page_example_traces():
    A = [[3, 3], [2, 5], [0, 6]]
    B = [[3, 2], [2, 6], [3, 1]]
    paths = {
        0: ([(0, 3), (3, 0)], ((1, 0, 0), (1, 0))),
        1: ([(1, 4), (4, 2), (2, 3), (3, 1)], ((0, F(1, 3), F(2, 3)), (F(1, 3), F(2, 3)))),
        2: ([(2, 3), (3, 0), (0, 2)], ((1, 0, 0), (1, 0))),
        3: ([(3, 0), (0, 3)], ((1, 0, 0), (1, 0))),
        4: ([(4, 2), (2, 3), (3, 1), (1, 4)], ((0, F(1, 3), F(2, 3)), (F(1, 3), F(2, 3)))),
    }
    for k, (want_trace, want_eq) in paths.items():
        trace = []
        eq = lemke_howson(A, B, k, trace)
        assert trace == want_trace
        assert tup(eq) == want_eq
        check(A, B, eq)
    # The middle equilibrium exists but no path from the artificial equilibrium ends there.
    every = set(support_enumeration(A, B))
    reached = {tup(e) for e in all_lemke_howson(A, B)}
    assert every - reached == {((F(4, 5), F(1, 5), 0), (F(2, 3), F(1, 3)))}


def test_battle_of_the_sexes():
    A, B = [[2, 0], [0, 1]], [[1, 0], [0, 2]]
    for k, want in ((0, ((1, 0), (1, 0))), (2, ((1, 0), (1, 0))), (1, ((0, 1), (0, 1))), (3, ((0, 1), (0, 1)))):
        assert tup(lemke_howson(A, B, k)) == want


def test_zero_sum_games():
    for M in ([[1, -1], [-1, 1]], [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]):
        k = len(M)
        for lab in range(2 * k):
            eq = lemke_howson(M, [[-v for v in r] for r in M], lab)
            assert tup(eq) == (tuple([F(1, k)] * k), tuple([F(1, k)] * k))


def test_negative_payoffs_and_shift():
    # Shifting all payoffs does not change the equilibria or the path.
    A = [[-7, -2], [-3, -9]]
    B = [[-1, -8], [-6, -2]]
    for k in range(4):
        assert lemke_howson(A, B, k) == lemke_howson([[v + 20 for v in r] for r in A],
                                                     [[v + 20 for v in r] for r in B], k)


def test_random_nondegenerate_games():
    rng = random.Random(3301)
    done = 0
    while done < 60:
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        A = [[rng.randint(-30, 30) for _ in range(n)] for _ in range(m)]
        B = [[rng.randint(-30, 30) for _ in range(n)] for _ in range(m)]
        if not nondegenerate(A, B):
            continue
        done += 1
        every = set(support_enumeration(A, B))
        assert len(every) % 2 == 1
        for k in range(m + n):
            eq = lemke_howson(A, B, k)
            check(A, B, eq)
            assert tup(eq) in every


def test_degenerate_games_end_at_an_equilibrium():
    rng = random.Random(55)
    for _ in range(150):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        A = [[rng.randint(0, 2) for _ in range(n)] for _ in range(m)]
        B = [[rng.randint(0, 2) for _ in range(n)] for _ in range(m)]
        for k in range(m + n):
            check(A, B, lemke_howson(A, B, k))


def test_constant_game():
    # Every profile is an equilibrium; the lexicographic rule still gives a finite path.
    A = [[1, 1, 1], [1, 1, 1]]
    for k in range(5):
        check(A, A, lemke_howson(A, A, k))


def test_bad_label():
    try:
        lemke_howson([[1]], [[1]], 2)
    except ValueError:
        return
    raise AssertionError("expected ValueError")
