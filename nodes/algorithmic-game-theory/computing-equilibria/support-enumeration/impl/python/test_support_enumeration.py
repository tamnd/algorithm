# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/support-enumeration/. The authors are listed in prov/GHTYAP.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from agtgame import from_bimatrix, is_nash
from support_enumeration import is_nondegenerate, solve_square, support_enumeration

F = Fraction


def vertex_enumeration(A, B):
    """All extreme equilibria, from the vertices of the two best response polytopes.

    P = {x >= 0 : B'^T x <= 1} and Q = {y >= 0 : A' y <= 1}, with A', B' > 0. A vertex pair
    (x, y) other than (0, 0) whose labels cover all of rows and columns is an equilibrium.
    """
    m, n = len(A), len(A[0])
    shift = 1 - min(min(min(r) for r in A), min(min(r) for r in B))
    Ap = [[F(v) + shift for v in r] for r in A]
    Bp = [[F(v) + shift for v in r] for r in B]

    def vertices(cons, dim):
        # cons: list of (label, coefficients, rhs) for coefficients . z <= rhs.
        out = []
        for tight in combinations(range(len(cons)), dim):
            z = solve_square([cons[t][1] for t in tight], [cons[t][2] for t in tight])
            if z is None:
                continue
            if all(sum((c * v for c, v in zip(co, z)), F(0)) <= r for _, co, r in cons):
                labels = {lab for lab, co, r in cons if sum((c * v for c, v in zip(co, z)), F(0)) == r}
                if (z, labels) not in out:
                    out.append((z, labels))
        return out

    cp = [(i, [F(-int(k == i)) for k in range(m)], F(0)) for i in range(m)]
    cp += [(m + j, [Bp[i][j] for i in range(m)], F(1)) for j in range(n)]
    cq = [(i, Ap[i], F(1)) for i in range(m)]
    cq += [(m + j, [F(-int(k == j)) for k in range(n)], F(0)) for j in range(n)]
    eqs = []
    for x, lx in vertices(cp, m):
        for y, ly in vertices(cq, n):
            if any(x) and any(y) and lx | ly == set(range(m + n)):
                e = ([v / sum(x) for v in x], [v / sum(y) for v in y])
                if e not in eqs:
                    eqs.append(e)
    return eqs


def check_equilibria(A, B, eqs):
    game = from_bimatrix(A, B)
    for x, y in eqs:
        assert is_nash(game, [x, y])


def as_set(eqs):
    return {(tuple(x), tuple(y)) for x, y in eqs}


def test_battle_of_the_sexes():
    A, B = [[2, 0], [0, 1]], [[1, 0], [0, 2]]
    eqs = support_enumeration(A, B)
    assert as_set(eqs) == {((1, 0), (1, 0)), ((0, 1), (0, 1)), ((F(2, 3), F(1, 3)), (F(1, 3), F(2, 3)))}
    check_equilibria(A, B, eqs)
    x, y = eqs[2]
    assert sum(x[i] * y[j] * A[i][j] for i in range(2) for j in range(2)) == F(2, 3)


def test_zero_sum_check_values():
    MP = [[1, -1], [-1, 1]]
    RPS = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
    for M in (MP, RPS):
        k = len(M)
        eqs = support_enumeration(M, [[-v for v in r] for r in M])
        assert eqs == [([F(1, k)] * k, [F(1, k)] * k)]


def test_chicken():
    A = [[0, 7], [2, 6]]  # strategy 0 is dare, 1 is chicken
    B = [[0, 2], [7, 6]]
    eqs = as_set(support_enumeration(A, B))
    assert eqs == {((1, 0), (0, 1)), ((0, 1), (1, 0)), ((F(1, 3), F(2, 3)), (F(1, 3), F(2, 3)))}


def test_page_example():
    A = [[3, 3], [2, 5], [0, 6]]
    B = [[3, 2], [2, 6], [3, 1]]
    assert is_nondegenerate(A, B)
    eqs = support_enumeration(A, B)
    assert as_set(eqs) == {((1, 0, 0), (1, 0)), ((F(4, 5), F(1, 5), 0), (F(2, 3), F(1, 3))),
                           ((0, F(1, 3), F(2, 3)), (F(1, 3), F(2, 3)))}
    assert as_set(eqs) == as_set(vertex_enumeration(A, B))


def test_coordination_game_has_one_equilibrium_per_support():
    for n in range(1, 5):
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        eqs = support_enumeration(I, I)
        assert len(eqs) == 2 ** n - 1
        for x, y in eqs:
            k = sum(1 for v in x if v)
            assert x == y and all(v in (0, F(1, k)) for v in x)


def test_random_nondegenerate_games():
    rng = random.Random(4417)
    done = 0
    while done < 60:
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        A = [[rng.randint(-50, 50) for _ in range(n)] for _ in range(m)]
        B = [[rng.randint(-50, 50) for _ in range(n)] for _ in range(m)]
        if not is_nondegenerate(A, B):
            continue
        done += 1
        eqs = support_enumeration(A, B)
        check_equilibria(A, B, eqs)
        assert len(eqs) % 2 == 1  # a nondegenerate game has an odd number of equilibria
        assert as_set(eqs) == as_set(vertex_enumeration(A, B))
        for x, y in eqs:  # supports of equal size
            assert sum(1 for v in x if v) == sum(1 for v in y if v)


def test_degenerate_game_misses_an_extreme_equilibrium():
    # Against row 0 both columns are best responses, so the game is degenerate.
    A = [[1, 0], [0, 1]]
    B = [[1, 1], [0, 3]]
    assert not is_nondegenerate(A, B)
    eqs = support_enumeration(A, B)
    check_equilibria(A, B, eqs)
    allv = as_set(vertex_enumeration(A, B))
    assert as_set(eqs) <= allv
    assert ((1, 0), (F(1, 2), F(1, 2))) in allv - as_set(eqs)


def test_random_degenerate_games_give_only_equilibria():
    rng = random.Random(90)
    for _ in range(80):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        A = [[rng.randint(0, 2) for _ in range(n)] for _ in range(m)]
        B = [[rng.randint(0, 2) for _ in range(n)] for _ in range(m)]
        eqs = support_enumeration(A, B)
        check_equilibria(A, B, eqs)
        assert as_set(eqs) <= as_set(vertex_enumeration(A, B))
