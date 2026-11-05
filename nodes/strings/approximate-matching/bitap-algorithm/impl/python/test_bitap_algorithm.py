# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bitap-algorithm/. The authors are listed in prov/F82Z8Y.jsonl.

import random

import pytest
from bitap_algorithm import bitap_mismatches, field_width, mismatch_fields


def brute(pattern: str, text: str, k: int) -> list[int]:
    m = len(pattern)
    return [
        i for i in range(len(text) - m + 1)
        if sum(a != b for a, b in zip(pattern, text[i:i + m])) <= k
    ]


def test_examples() -> None:
    assert bitap_mismatches("abc", "abxabcbc", 1) == [0, 3, 5]
    assert bitap_mismatches("abc", "abxabcbc", 0) == [3]
    assert bitap_mismatches("ACGTA", "ACGAAACGTTACCTA", 1) == [0, 5, 10]
    rows = mismatch_fields("abc", "abxabcbc", 1)
    assert [r[2] for r in rows[2:]] == [1, None, None, 0, None, 1]


def test_field_width() -> None:
    assert [field_width(k) for k in range(8)] == [1, 2, 3, 3, 4, 4, 4, 4]
    for k in range(100):
        b = field_width(k)
        assert 2 ** (b - 1) >= k + 1 > 2 ** (b - 2) or b == 1


def test_edges() -> None:
    assert bitap_mismatches("", "", 0) == [0]
    assert bitap_mismatches("", "abc", 0) == [0, 1, 2, 3]
    assert bitap_mismatches("a", "", 3) == []
    assert bitap_mismatches("abc", "ab", 3) == []
    assert bitap_mismatches("ab", "xyz", 2) == [0, 1]
    assert bitap_mismatches("ab", "xyz", 1) == []
    with pytest.raises(ValueError):
        bitap_mismatches("a", "a", -1)


def test_random_against_brute_force() -> None:
    rng = random.Random(1992)
    for alphabet in ("ab", "acgt"):
        for _ in range(1500):
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 9)))
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 25)))
            k = rng.randint(0, 10)
            assert bitap_mismatches(p, t, k) == brute(p, t, k), (p, t, k)


def test_text_characters_outside_the_pattern() -> None:
    rng = random.Random(7)
    for _ in range(500):
        p = "".join(rng.choice("ab") for _ in range(rng.randint(1, 6)))
        t = "".join(rng.choice("abxy") for _ in range(rng.randint(0, 20)))
        k = rng.randint(0, 3)
        assert bitap_mismatches(p, t, k) == brute(p, t, k)
