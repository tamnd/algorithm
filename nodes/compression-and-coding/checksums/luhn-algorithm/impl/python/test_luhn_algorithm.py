# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/luhn-algorithm/. The authors are listed in prov/BC0D59.jsonl.

import random

import pytest

from luhn_algorithm import DOUBLE, check_digit, is_valid


def oracle_valid(number: str) -> bool:
    """Independent form: double every second digit from the right and add the digits of the products."""
    total = 0
    for i, ch in enumerate(reversed(number)):
        v = int(ch) * (2 if i % 2 else 1)
        total += sum(int(c) for c in str(v))
    return total % 10 == 0


def test_known_example() -> None:
    # 7992739871 with check digit 3 (Wikipedia, "Luhn algorithm", Example).
    assert check_digit("7992739871") == "3"
    assert is_valid("79927398713")
    assert not is_valid("79927398710")
    assert is_valid("4111111111111111")  # a common card test number


def test_double_table() -> None:
    assert DOUBLE == [sum(int(c) for c in str(2 * x)) for x in range(10)]
    assert sorted(DOUBLE) == list(range(10))  # D is a permutation of the digits


def test_edges() -> None:
    assert check_digit("0") == "0" and is_valid("0") and is_valid("00")
    assert is_valid("18") and check_digit("1") == "8"
    for bad in ("", "12a", "1 2", "١"):
        with pytest.raises(ValueError):
            is_valid(bad)


def test_random_against_oracle() -> None:
    rng = random.Random(10101)
    for _ in range(1000):
        p = "".join(rng.choice("0123456789") for _ in range(rng.randrange(1, 25)))
        w = p + check_digit(p)
        assert is_valid(w) and oracle_valid(w)
        r = "".join(rng.choice("0123456789") for _ in range(rng.randrange(1, 25)))
        assert is_valid(r) == oracle_valid(r)


def all_codewords() -> list[str]:
    return [p + check_digit(p) for p in (f"{x:04d}" for x in range(10000))]


def test_all_single_digit_errors_detected() -> None:
    missed = total = 0
    for w in all_codewords():
        for i in range(5):
            for v in "0123456789":
                if v != w[i]:
                    total += 1
                    missed += is_valid(w[:i] + v + w[i + 1 :])
    assert (missed, total) == (0, 450000)


def test_adjacent_transpositions_only_09_90_missed() -> None:
    missed = total = 0
    for w in all_codewords():
        for i in range(4):
            if w[i] != w[i + 1]:
                total += 1
                if is_valid(w[:i] + w[i + 1] + w[i] + w[i + 2 :]):
                    missed += 1
                    assert {w[i], w[i + 1]} == {"0", "9"}
    assert (missed, total) == (800, 36000)


def test_other_error_classes_exact_counts() -> None:
    twin = jump = 0
    twin_pairs = set()
    for w in all_codewords():
        for i in range(4):
            if w[i] == w[i + 1]:
                for v in "0123456789":
                    if v != w[i] and is_valid(w[:i] + v + v + w[i + 2 :]):
                        twin += 1
                        twin_pairs.add(frozenset((w[i], v)))
        for i in range(3):
            if w[i] != w[i + 2]:
                jump += is_valid(w[:i] + w[i + 2] + w[i + 1] + w[i] + w[i + 3 :])
    assert twin == 2400  # of 36000
    assert twin_pairs == {frozenset("25"), frozenset("36"), frozenset("47")}
    assert jump == 27000  # of 27000: every jump transposition abc -> cba is missed
