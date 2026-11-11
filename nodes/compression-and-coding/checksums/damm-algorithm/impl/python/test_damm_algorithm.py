# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/damm-algorithm/. The authors are listed in prov/B1H68B.jsonl.

import random

import pytest

from damm_algorithm import Q, check_digit, interim, is_valid


def test_known_example() -> None:
    # 572: interim digits 0 -> 9 -> 7 -> 4, so the check digit is 4 (Wikipedia, "Damm algorithm").
    c, trail = 0, []
    for d in (5, 7, 2):
        c = Q[c][d]
        trail.append(c)
    assert trail == [9, 7, 4]
    assert check_digit("572") == "4"
    assert is_valid("5724")
    assert not is_valid("5742")


def test_latin_square() -> None:
    e = list(range(10))
    assert all(sorted(row) == e for row in Q)
    assert all(sorted(Q[r][c] for r in e) == e for c in e)


def test_zero_diagonal() -> None:
    assert all(Q[x][x] == 0 for x in range(10))


def test_weakly_totally_anti_symmetric() -> None:
    # (c * x) * y = (c * y) * x implies x = y, for all c, x, y.
    for c in range(10):
        for x in range(10):
            for y in range(10):
                if Q[Q[c][x]][y] == Q[Q[c][y]][x]:
                    assert x == y


def test_edges() -> None:
    assert check_digit("0") == "0" and is_valid("00") and is_valid("0")
    # Leading zeros do not change the interim digit: Q[0][0] = 0.
    assert check_digit("00572") == check_digit("572")
    with pytest.raises(ValueError):
        interim("")


def test_random_round_trip() -> None:
    rng = random.Random(12101)
    for _ in range(1000):
        p = "".join(rng.choice("0123456789") for _ in range(rng.randrange(1, 30)))
        assert is_valid(p + check_digit(p))
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
    assert twin == 3520  # of 36000
    assert jump == 2498  # of 27000
    assert jtwin == 3122  # of 27000
