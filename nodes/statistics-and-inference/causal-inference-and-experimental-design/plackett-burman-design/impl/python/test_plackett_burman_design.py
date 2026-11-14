# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plackett-burman-design/. The authors are listed in prov/9V49FC.jsonl.

import random
from fractions import Fraction
from itertools import combinations, product

import pytest

from plackett_burman_design import (
    PB12_GENERATOR, cyclic_design, is_hadamard, main_effects, paley_design, sylvester_design,
    with_mean_column,
)


def test_pb12() -> None:
    d = cyclic_design(PB12_GENERATOR)
    assert len(d) == 12 and len(d[0]) == 11
    assert is_hadamard(with_mean_column(d))
    assert all(sum(col) == 0 for col in zip(*d))  # six + and six - in every column
    assert d == paley_design(11)  # the PB12 row is the quadratic residues of 11, plus 0


def test_paley_designs() -> None:
    for q in (3, 7, 11, 19, 23, 31, 43):
        d = paley_design(q)
        assert len(d) == q + 1 and is_hadamard(with_mean_column(d))
    assert "".join("+" if v > 0 else "-" for v in paley_design(19)[0]) == "++--++++-+-+----++-"


def test_sylvester_designs() -> None:
    for m in range(1, 6):
        assert is_hadamard(with_mean_column(sylvester_design(m)))


def test_strength_two_projection() -> None:
    # every pair of columns shows (+,+), (+,-), (-,+), (-,-) three times each in N = 12
    d = cyclic_design(PB12_GENERATOR)
    for a, b in combinations(range(11), 2):
        pairs = [(r[a], r[b]) for r in d]
        assert all(pairs.count(p) == 3 for p in product((1, -1), repeat=2))


def test_partial_aliasing_of_pb12() -> None:
    d = cyclic_design(PB12_GENERATOR)
    coefs = set()
    for i in range(11):
        for a, b in combinations([j for j in range(11) if j != i], 2):
            coefs.add(Fraction(sum(r[i] * r[a] * r[b] for r in d), 12))
    assert coefs == {Fraction(1, 3), Fraction(-1, 3)}
    # in the 2^(7-4) design of 8 runs the aliasing is complete: column a times column b is
    # the column with label a xor b, so the coefficient is 1 for that column and 0 otherwise
    s = sylvester_design(3)
    for i in range(7):
        for a, b in combinations([j for j in range(7) if j != i], 2):
            coef = Fraction(sum(r[i] * r[a] * r[b] for r in s), 8)
            assert coef == (1 if (i + 1) == ((a + 1) ^ (b + 1)) else 0)


def test_main_effects_unbiased_without_interactions() -> None:
    rng = random.Random(1)
    d = cyclic_design(PB12_GENERATOR)
    beta = [rng.uniform(-3.0, 3.0) for _ in range(11)]
    y = [10.0 + sum(b * x for b, x in zip(beta, r)) for r in d]
    assert all(abs(e - 2.0 * b) < 1e-12 for e, b in zip(main_effects(d, y), beta))


def test_no_hadamard_matrix_of_order_six() -> None:
    # A normalized Hadamard matrix of order 6 would need 5 rows that start with +1, have
    # three +1 entries (orthogonal to the first row) and are pairwise orthogonal.
    cands = [v for v in product((1, -1), repeat=6) if v[0] == 1 and sum(v) == 0]
    ortho = lambda u, w: sum(a * b for a, b in zip(u, w)) == 0
    assert not any(ortho(u, w) for u, w in combinations(cands, 2))


def test_example_interaction_spread_or_concentrated() -> None:
    # y = 50 + 5 x_A + 3 x_D + 4 x_A x_D, no noise
    d = cyclic_design(PB12_GENERATOR)
    y = [50 + 5 * r[0] + 3 * r[3] + 4 * r[0] * r[3] for r in d]
    assert y == [62, 62, 44, 48, 48, 48, 44, 46, 44, 62, 46, 46]
    est = [Fraction(2 * sum(r[j] * v for r, v in zip(d, y)), 12) for j in range(11)]
    assert est[0] == 10 and est[3] == 6
    assert [est[j] for j in range(11) if j not in (0, 3)] == [Fraction(s * 8, 3) for s in (-1, 1, 1, 1, -1, -1, -1, -1, -1)]
    # the 8-run 2^(7-4) design: column labels 1..7, and A x B is the column labelled 1 xor 2 = 3
    s = sylvester_design(3)
    y8 = [50 + 5 * r[0] + 3 * r[1] + 4 * r[0] * r[1] for r in s]
    est8 = [Fraction(2 * sum(r[j] * v for r, v in zip(s, y8)), 8) for j in range(7)]
    assert est8 == [10, 6, 8, 0, 0, 0, 0]


def test_three_column_projection_of_pb12() -> None:
    # any 3 columns hold a full 2^3 plus a half fraction: four patterns once, four twice
    d = cyclic_design(PB12_GENERATOR)
    for t in combinations(range(11), 3):
        pats = [tuple(r[i] for i in t) for r in d]
        assert sorted(pats.count(p) for p in product((1, -1), repeat=3)) == [1, 1, 1, 1, 2, 2, 2, 2]


def test_hadamard_order_argument() -> None:
    # three normalized rows: the column patterns of rows 2 and 3 each occur n/4 times
    for h in (with_mean_column(cyclic_design(PB12_GENERATOR)), with_mean_column(paley_design(19))):
        n = len(h)
        cols = list(zip(*h))
        norm = [[v * c[0] for v in c] for c in cols]  # make the first row all +1
        for i, j in combinations(range(1, n), 2):
            pats = [(c[i], c[j]) for c in norm]
            assert all(pats.count(p) == n // 4 for p in product((1, -1), repeat=2))


def test_errors() -> None:
    with pytest.raises(ValueError):
        paley_design(13)
