# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/label-cover/. The authors are listed in prov/N3TWC8.jsonl.

import random
from fractions import Fraction
from itertools import product

from label_cover import (
    clause_variable_game,
    majority_labeling,
    max_sat_fraction,
    repeat,
    satisfied,
    value,
    value_all_labelings,
)


def random_game(rng: random.Random, nu: int, nw: int, su: int, sw: int, m: int):
    edges = []
    for _ in range(m):
        edges.append((rng.randrange(nu), rng.randrange(nw), tuple(rng.randrange(sw) for _ in range(su))))
    return nu, nw, su, sw, edges


def random_formula(rng: random.Random, n: int, m: int):
    out = []
    for _ in range(m):
        vs = rng.sample(range(1, n + 1), 3)
        out.append(tuple(v if rng.random() < 0.5 else -v for v in vs))
    return out


def test_all_eight_clauses() -> None:
    clauses = [tuple(s * v for s, v in zip(signs, (1, 2, 3))) for signs in product((1, -1), repeat=3)]
    game = clause_variable_game(3, clauses)
    assert len(game[4]) == 24
    assert max_sat_fraction(3, clauses) == Fraction(7, 8)
    assert value(game) == Fraction(23, 24)


def test_satisfiable_formula_has_value_one() -> None:
    clauses = [(1, 2, 3), (-1, 2, -3), (-2, 3, 4)]
    assert value(clause_variable_game(4, clauses)) == 1


def test_clause_variable_identity() -> None:
    rng = random.Random(3)
    for _ in range(150):
        n = rng.randint(3, 6)
        clauses = random_formula(rng, n, rng.randint(1, 9))
        game = clause_variable_game(n, clauses)
        assert value(game) == 1 - (1 - max_sat_fraction(n, clauses)) / 3


def test_value_matches_full_search() -> None:
    rng = random.Random(5)
    for _ in range(60):
        game = random_game(rng, 3, 3, 3, 2, rng.randint(1, 7))
        assert value(game) == value_all_labelings(game)


def test_majority_reaches_one_over_right_alphabet() -> None:
    rng = random.Random(7)
    for _ in range(200):
        sw = rng.randint(2, 4)
        game = random_game(rng, rng.randint(1, 4), rng.randint(1, 4), rng.randint(1, 4), sw, rng.randint(1, 12))
        left, right = majority_labeling(game)
        assert satisfied(game, left, right) * sw >= len(game[4])


def test_parallel_repetition_bounds() -> None:
    rng = random.Random(11)
    for _ in range(25):
        game = random_game(rng, 2, 2, 3, 2, rng.randint(2, 4))
        g2 = repeat(game, 2)
        assert g2[0] == 4 and g2[1] == 4 and g2[2] == 9 and g2[3] == 4
        assert len(g2[4]) == len(game[4]) ** 2
        v, v2 = value(game), value(g2)
        assert v * v <= v2 <= v
        if v == 1:
            assert v2 == 1
