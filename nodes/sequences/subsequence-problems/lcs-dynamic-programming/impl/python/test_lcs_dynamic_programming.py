# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lcs-dynamic-programming/. The authors are listed in prov/31FDB1.jsonl.

import itertools
import random

from lcs_dynamic_programming import lcs, lcs_length, lcs_table


def is_subsequence(z: list, x: list) -> bool:
    it = iter(x)
    return all(any(a == b for b in it) for a in z)


def brute_lcs_length(x: str, y: str) -> int:
    for k in range(min(len(x), len(y)), 0, -1):
        for idx in itertools.combinations(range(len(x)), k):
            if is_subsequence([x[i] for i in idx], list(y)):
                return k
    return 0


def test_example() -> None:
    x, y = "ABCBDAB", "BDCABA"
    assert "".join(lcs(x, y)) == "BCBA"
    assert lcs_table(x, y)[7][6] == 4
    assert lcs_table(x, y)[4] == [0, 1, 1, 2, 2, 3, 3]
    assert lcs_length(x, y) == 4


def test_dna() -> None:
    s1 = "ACCGGTCGAGTGCGCGGAAGCCGGCCGAA"
    s2 = "GTCGTTCGGAATGCCGTTGCTCTGTAAA"
    assert "".join(lcs(s1, s2)) == "GTCGTCGGAAGCCGGCCGAA"


def test_edges() -> None:
    assert lcs("", "") == []
    assert lcs("ABC", "") == []
    assert lcs("", "ABC") == []
    assert lcs("ABC", "DEF") == []
    assert lcs("ABC", "ABC") == list("ABC")
    assert lcs([1, 2, 3], [3, 2, 1]) in ([1], [2], [3])
    assert lcs_length("AAAA", "AA") == 2


def test_random_against_brute_force() -> None:
    rng = random.Random(14)
    for _ in range(400):
        x = "".join(rng.choice("ABC") for _ in range(rng.randrange(9)))
        y = "".join(rng.choice("ABC") for _ in range(rng.randrange(9)))
        z = lcs(x, y)
        k = brute_lcs_length(x, y)
        assert len(z) == k == lcs_length(x, y) == lcs_table(x, y)[len(x)][len(y)]
        assert is_subsequence(z, list(x)) and is_subsequence(z, list(y))
