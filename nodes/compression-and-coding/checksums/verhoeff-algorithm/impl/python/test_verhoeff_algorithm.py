# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/verhoeff-algorithm/. The authors are listed in prov/ZV0WXF.jsonl.

import itertools
import random

import pytest

from verhoeff_algorithm import D, INV, P, check_digit, is_valid


def test_known_example() -> None:
    # 236 gets check digit 3, and 2363 is valid (Wikipedia, "Verhoeff algorithm", Examples).
    assert check_digit("236") == "3"
    assert is_valid("2363")
    assert not is_valid("2364")


def test_group_axioms() -> None:
    e = range(10)
    assert all(D[0][a] == a == D[a][0] for a in e)  # identity 0
    assert all(sorted(D[a]) == list(e) for a in e)  # closure, rows are permutations
    assert all(D[D[a][b]][c] == D[a][D[b][c]] for a, b, c in itertools.product(e, e, e))  # associativity
    assert all(D[a][INV[a]] == 0 == D[INV[a]][a] for a in e)  # inverses
    assert any(D[a][b] != D[b][a] for a in e for b in e)  # not commutative


def test_dihedral_structure() -> None:
    # 1 generates the rotations {0..4}; 5 is a reflection with 5 r 5 = r^-1.
    r = 1
    powers = [0]
    for _ in range(4):
        powers.append(D[powers[-1]][r])
    assert sorted(powers) == [0, 1, 2, 3, 4] and D[powers[-1]][r] == 0
    assert D[5][5] == 0
    assert D[D[5][1]][5] == INV[1]


def test_permutation_powers() -> None:
    for i in range(1, 8):
        assert P[i] == [P[1][x] for x in P[i - 1]]
    assert [P[1][x] for x in P[7]] == P[0]  # order 8
    # The property Verhoeff needs: a * p(b) != b * p(a) whenever a != b.
    assert all(D[a][P[1][b]] != D[b][P[1][a]] for a in range(10) for b in range(10) if a != b)


def test_edges() -> None:
    # Unlike Luhn and Damm, a leading zero changes the result: P[1] moves 0 to 1.
    assert check_digit("0") == "4" and is_valid("04") and not is_valid("00")
    assert is_valid("0")
    assert check_digit("0236") != check_digit("236")
    for bad in ("", "x1", "-1"):
        with pytest.raises(ValueError):
            check_digit(bad)


def test_random_round_trip() -> None:
    rng = random.Random(11101)
    for _ in range(1000):
        p = "".join(rng.choice("0123456789") for _ in range(rng.randrange(1, 30)))
        c = check_digit(p)
        assert is_valid(p + c)
        assert sum(is_valid(p + d) for d in "0123456789") == 1


def all_codewords() -> list[str]:
    return [p + check_digit(p) for p in (f"{x:04d}" for x in range(10000))]


def test_exhaustive_error_counts() -> None:
    single = adj = twin = jump = jtwin = 0
    for w in all_codewords():
        for i in range(5):
            single += sum(is_valid(w[:i] + v + w[i + 1 :]) for v in "0123456789" if v != w[i])
        for i in range(4):
            if w[i] != w[i + 1]:
                adj += is_valid(w[:i] + w[i + 1] + w[i] + w[i + 2 :])
            else:
                twin += sum(is_valid(w[:i] + v + v + w[i + 2 :]) for v in "0123456789" if v != w[i])
        for i in range(3):
            if w[i] != w[i + 2]:
                jump += is_valid(w[:i] + w[i + 2] + w[i + 1] + w[i] + w[i + 3 :])
            else:
                jtwin += sum(is_valid(w[:i] + v + w[i + 1] + v + w[i + 3 :]) for v in "0123456789" if v != w[i])
    assert single == 0  # of 450000
    assert adj == 0  # of 36000
    assert twin == 1600  # of 36000
    assert jump == 1560  # of 27000
    assert jtwin == 1560  # of 27000
