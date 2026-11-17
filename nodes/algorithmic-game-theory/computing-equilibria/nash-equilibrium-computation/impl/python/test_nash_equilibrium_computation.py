# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nash-equilibrium-computation/. The authors are listed in prov/EYAA2N.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from nash_equilibrium_computation import is_equilibrium, payoffs, support_enumeration

H = Fraction(1, 2)


def pure_equilibria(a, b):
    """Independent oracle: all pure profiles where no player gains by a switch."""
    m, n = len(a), len(a[0])
    out = set()
    for i, j in itertools.product(range(m), range(n)):
        if all(a[k][j] <= a[i][j] for k in range(m)) and all(b[i][k] <= b[i][j] for k in range(n)):
            out.add((i, j))
    return out


def two_by_two_oracle(a, b):
    """Independent oracle for nondegenerate 2 by 2 games: pure ones plus the interior one."""
    eqs = set()
    for i, j in pure_equilibria(a, b):
        x = tuple(Fraction(int(k == i)) for k in range(2))
        y = tuple(Fraction(int(k == j)) for k in range(2))
        eqs.add((x, y))
    # Row indifference: q a00 + (1-q) a01 = q a10 + (1-q) a11.
    dq = (a[0][0] - a[0][1]) - (a[1][0] - a[1][1])
    dp = (b[0][0] - b[1][0]) - (b[0][1] - b[1][1])
    if dq != 0 and dp != 0:
        q = Fraction(a[1][1] - a[0][1], dq)
        p = Fraction(b[1][1] - b[1][0], dp)
        if 0 < q < 1 and 0 < p < 1:
            eqs.add(((p, 1 - p), (q, 1 - q)))
    return eqs


def nondegenerate(a, b):
    """Generic test: no pure strategy has two pure best responses, and the 2 by 2 subgames are regular."""
    m, n = len(a), len(a[0])
    for j in range(n):
        col = [a[i][j] for i in range(m)]
        if col.count(max(col)) > 1:
            return False
    for i in range(m):
        if b[i].count(max(b[i])) > 1:
            return False
    return True


def test_battle_of_the_sexes():
    a = [[2, 0], [0, 1]]
    b = [[1, 0], [0, 2]]
    eqs = support_enumeration(a, b)
    third, two = Fraction(1, 3), Fraction(2, 3)
    assert eqs == [((1, 0), (1, 0)), ((0, 1), (0, 1)), ((two, third), (third, two))]
    assert payoffs(a, b, *eqs[2]) == (two, two)


def test_matching_pennies_and_rps():
    a = [[1, -1], [-1, 1]]
    b = [[-1, 1], [1, -1]]
    assert support_enumeration(a, b) == [((H, H), (H, H))]
    r = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
    t = Fraction(1, 3)
    assert support_enumeration(r, [[-v for v in row] for row in r]) == [((t, t, t), (t, t, t))]


def test_prisoners_dilemma():
    a = [[3, 0], [5, 1]]
    b = [[3, 5], [0, 1]]
    assert support_enumeration(a, b) == [((0, 1), (0, 1))]
    assert not is_equilibrium(a, b, (1, 0), (1, 0))


def test_chicken():
    a = [[0, 7], [2, 6]]
    b = [[0, 2], [7, 6]]
    eqs = support_enumeration(a, b)
    t = Fraction(1, 3)
    assert ((t, 2 * t), (t, 2 * t)) in eqs and len(eqs) == 3
    assert payoffs(a, b, (t, 2 * t), (t, 2 * t)) == (Fraction(14, 3), Fraction(14, 3))


def test_one_by_one_and_rectangular():
    assert support_enumeration([[4]], [[-2]]) == [((1,), (1,))]
    eqs = support_enumeration([[1, 2, 3]], [[3, 1, 2]])
    assert eqs == [((1,), (1, 0, 0))]


def test_bad_shape():
    with pytest.raises(ValueError):
        support_enumeration([[1, 2]], [[1]])


def test_is_equilibrium_rejects_non_distributions():
    a = [[1, 0], [0, 1]]
    assert not is_equilibrium(a, a, (H, H), (1, 1))
    assert not is_equilibrium(a, a, (2, -1), (1, 0))


def test_random_two_by_two_against_closed_form():
    rng = random.Random(1950)
    tested = 0
    while tested < 500:
        a = [[rng.randint(-6, 6) for _ in range(2)] for _ in range(2)]
        b = [[rng.randint(-6, 6) for _ in range(2)] for _ in range(2)]
        if not nondegenerate(a, b):
            continue
        tested += 1
        eqs = support_enumeration(a, b)
        assert set(eqs) == two_by_two_oracle(a, b)
        assert len(eqs) % 2 == 1


def test_random_three_by_three_nondegenerate():
    rng = random.Random(1951)
    tested = 0
    while tested < 200:
        a = [[rng.randint(-9, 9) for _ in range(3)] for _ in range(3)]
        b = [[rng.randint(-9, 9) for _ in range(3)] for _ in range(3)]
        if not nondegenerate(a, b):
            continue
        tested += 1
        eqs = support_enumeration(a, b)
        assert eqs, "Nash's theorem: at least one equilibrium"
        for x, y in eqs:
            assert is_equilibrium(a, b, x, y)
        pure = {(x.index(1), y.index(1)) for x, y in eqs if 1 in x and 1 in y}
        assert pure == pure_equilibria(a, b)
        assert len(set(eqs)) == len(eqs)
        # Nondegenerate games have an odd number of equilibria.
        assert len(eqs) % 2 == 1


def test_random_zero_sum_same_value():
    rng = random.Random(1928)
    for _ in range(150):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        a = [[rng.randint(-5, 5) for _ in range(n)] for _ in range(m)]
        b = [[-v for v in row] for row in a]
        eqs = support_enumeration(a, b)
        # Random integer zero-sum games can be degenerate, so the list may be partial,
        # but on these sizes it is never empty, and all equilibria share the value.
        assert eqs
        values = {payoffs(a, b, x, y)[0] for x, y in eqs}
        assert len(values) == 1
        for x, y in eqs:
            assert is_equilibrium(a, b, x, y)
