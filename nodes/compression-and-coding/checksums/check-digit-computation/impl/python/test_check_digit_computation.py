# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/check-digit-computation/. The authors are listed in prov/CAQC35.jsonl.

import random

import pytest

from check_digit_computation import (
    chinese_id_check,
    gs1_check,
    gs1_valid,
    iban_check_digits,
    iban_valid,
    isbn10_check,
    isbn10_valid,
    mod11_2_check,
    mod11_2_valid,
    mod97,
    mod97_10_check,
)


def test_published_examples() -> None:
    # Wikipedia, "ISBN", check digit examples: ISBN-10 0-306-40615-2 and ISBN-13 978-0-306-40615-7.
    assert isbn10_check("030640615") == "2" and isbn10_valid("0-306-40615-2")
    assert gs1_check("978030640615") == "7" and gs1_valid("978-0-306-40615-7")
    # Wikipedia, "International Article Number": EAN-13 4006381333931.
    assert gs1_check("400638133393") == "1" and gs1_valid("4006381333931")
    # Wikipedia, "Universal Product Code": UPC-A 036000291452.
    assert gs1_check("03600029145") == "2" and gs1_valid("036000291452")
    # Wikipedia, "International Bank Account Number": GB82 WEST 1234 5698 7654 32.
    assert iban_valid("GB82 WEST 1234 5698 7654 32")
    assert iban_check_digits("GB", "WEST12345698765432") == "82"
    assert not iban_valid("GB82 WEST 1234 5698 7654 23")
    # ORCID support, "Structure of the ORCID Identifier": MOD 11-2 examples.
    assert mod11_2_valid("0000-0002-1825-0097")
    assert mod11_2_valid("0000-0001-5109-3700")
    assert mod11_2_valid("0000-0002-1694-233X")
    assert mod11_2_check("000000021825009") == "7"
    # Wikipedia, "Resident Identity Card" (China), check code examples.
    assert chinese_id_check("63280119790817003") == "6"
    assert chinese_id_check("34262219840209049") == "X"


def test_chinese_id_is_mod11_2() -> None:
    assert [pow(2, 17 - i, 11) for i in range(17)] == [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    rng = random.Random(13101)
    for _ in range(1000):
        p = "".join(rng.choice("0123456789") for _ in range(17))
        assert chinese_id_check(p) == mod11_2_check(p)


def oracle_weighted(payload: str, weights: list[int], m: int, target: int) -> int:
    """Brute force: the check value c in 0..m-1 with sum(w_i d_i) + c = target mod m."""
    s = sum(w * int(x) for w, x in zip(weights, payload))
    return next(c for c in range(m) if (s + c - target) % m == 0)


def test_random_against_brute_force() -> None:
    rng = random.Random(13102)
    for _ in range(1000):
        p9 = "".join(rng.choice("0123456789") for _ in range(9))
        c = oracle_weighted(p9, list(range(10, 1, -1)), 11, 0)
        assert isbn10_check(p9) == ("X" if c == 10 else str(c))
        p12 = "".join(rng.choice("0123456789") for _ in range(12))
        assert gs1_check(p12) == str(oracle_weighted(p12, [1, 3] * 6, 10, 0))
        n = rng.randrange(1, 20)
        p = "".join(rng.choice("0123456789") for _ in range(n))
        c = oracle_weighted(p, [pow(2, n - i, 11) for i in range(n)], 11, 1)
        assert mod11_2_check(p) == ("X" if c == 10 else str(c))
        q = "".join(rng.choice("0123456789") for _ in range(rng.randrange(1, 40)))
        assert int(q + mod97_10_check(q)) % 97 == 1
        assert mod97(q) == int(q) % 97


def test_edges() -> None:
    assert isbn10_check("000000000") == "0"
    assert mod97_10_check("0") == "98"
    with pytest.raises(ValueError):
        isbn10_check("12345678")
    with pytest.raises(ValueError):
        gs1_check("12a")
    assert not isbn10_valid("030640615X")
    assert not mod11_2_valid("X")


# ------------------------------------------------------------ exhaustive error counts


def count_errors(check, n: int, check_len: int = 1) -> tuple[int, int, int, int, int]:
    """Over all payloads of n digits: missed single errors, missed adjacent and all transpositions, and totals."""
    single = adj = adj_total = alltr = alltr_total = 0
    for x in range(10**n):
        p = f"{x:0{n}d}"
        w = p + check(p)

        def valid(s: str) -> bool:
            return s[:n].isdigit() and check(s[:n]) == s[n:]

        for i in range(len(w)):
            for v in "0123456789":
                if v != w[i]:
                    single += valid(w[:i] + v + w[i + 1 :])
        for i in range(len(w)):
            for j in range(i + 1, len(w)):
                if w[i] != w[j]:
                    e = list(w)
                    e[i], e[j] = e[j], e[i]
                    missed = valid("".join(e))
                    alltr_total += 1
                    alltr += missed
                    if j == i + 1:
                        adj_total += 1
                        adj += missed
    return single, adj, adj_total, alltr, alltr_total


def isbn_like(p: str) -> str:
    """The ISBN-10 rule on a shorter payload: weights len+1, ..., 2 and 1 for the check, mod 11."""
    n = len(p)
    c = (11 - sum((n + 1 - i) * int(x) for i, x in enumerate(p)) % 11) % 11
    return "X" if c == 10 else str(c)


def test_mod11_distinct_weights_catch_all_transpositions() -> None:
    # 10000 codewords of 5 characters, 909 of them end in X.
    assert count_errors(isbn_like, 4) == (0, 0, 36091, 0, 90364)
    assert count_errors(mod11_2_check, 4) == (0, 0, 36091, 0, 90364)


def test_gs1_misses_adjacent_digits_that_differ_by_5() -> None:
    single, adj, adj_total, alltr, alltr_total = count_errors(gs1_check, 4)
    assert (single, adj, adj_total) == (0, 4000, 36000)
    assert (alltr, alltr_total) == (42000, 90000)  # every swap of two places with equal weight is missed
    for a in range(10):
        for b in range(10):
            missed = (3 * a + b - (3 * b + a)) % 10 == 0
            assert missed == (a == b or abs(a - b) == 5)


def test_mod97_10_catches_singles_and_transpositions() -> None:
    # 1000 codewords of 5 digits: 3 payload digits and 2 check digits.
    assert count_errors(mod97_10_check, 3, 2) == (0, 0, 3618, 0, 9016)


def test_full_length_isbn10_every_error_of_random_codewords() -> None:
    rng = random.Random(13103)
    for _ in range(300):
        p = "".join(rng.choice("0123456789") for _ in range(9))
        w = p + isbn10_check(p)
        for i in range(10):
            for v in "0123456789X":
                if v != w[i]:
                    assert not isbn10_valid(w[:i] + v + w[i + 1 :])
        for i in range(10):
            for j in range(i + 1, 10):
                if w[i] != w[j]:
                    e = list(w)
                    e[i], e[j] = e[j], e[i]
                    assert not isbn10_valid("".join(e))
