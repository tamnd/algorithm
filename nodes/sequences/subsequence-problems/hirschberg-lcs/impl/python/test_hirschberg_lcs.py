# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hirschberg-lcs/. The authors are listed in prov/S3GJKS.jsonl.

import random

from hirschberg_lcs import hirschberg, lcs_row


def is_subsequence(z: list, x: list) -> bool:
    it = iter(x)
    return all(any(a == b for b in it) for a in z)


def table_lcs_length(x: str, y: str) -> int:
    c = [[0] * (len(y) + 1) for _ in range(len(x) + 1)]
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            if x[i - 1] == y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
            else:
                c[i][j] = max(c[i - 1][j], c[i][j - 1])
    return c[len(x)][len(y)]


def test_example() -> None:
    x, y = "ABCBDAB", "BDCABA"
    assert lcs_row(x[:3], y) == [0, 1, 1, 2, 2, 2, 2]
    assert lcs_row(x[3:][::-1], y[::-1]) == [0, 1, 2, 2, 2, 3, 4]
    assert "".join(hirschberg(x, y)) == "BCBA"


def test_dna() -> None:
    s1 = "ACCGGTCGAGTGCGCGGAAGCCGGCCGAA"
    s2 = "GTCGTTCGGAATGCCGTTGCTCTGTAAA"
    assert "".join(hirschberg(s1, s2)) == "GTCGTCGGAAGCCGGCCGAA"


def test_edges() -> None:
    assert hirschberg("", "") == []
    assert hirschberg("A", "") == []
    assert hirschberg("", "A") == []
    assert hirschberg("A", "BAB") == ["A"]
    assert hirschberg("ABC", "DEF") == []
    assert hirschberg("ABCD", "ABCD") == list("ABCD")
    assert hirschberg([1, 2, 3], [3, 2, 1]) in ([1], [2], [3])


def test_random_against_table() -> None:
    rng = random.Random(1975)
    for _ in range(500):
        x = "".join(rng.choice("ABC") for _ in range(rng.randrange(14)))
        y = "".join(rng.choice("ABC") for _ in range(rng.randrange(14)))
        z = hirschberg(x, y)
        assert len(z) == table_lcs_length(x, y) == lcs_row(x, y)[len(y)]
        assert is_subsequence(z, list(x)) and is_subsequence(z, list(y))
