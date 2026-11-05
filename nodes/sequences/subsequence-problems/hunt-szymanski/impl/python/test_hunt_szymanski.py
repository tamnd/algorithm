# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hunt-szymanski/. The authors are listed in prov/EEQDBV.jsonl.

import random

from hunt_szymanski import hunt_szymanski, hunt_szymanski_trace, match_lists


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
    assert match_lists(x, y)[0] == [6, 4]
    assert sum(len(lst) for lst in match_lists(x, y)) == 12
    rows = hunt_szymanski_trace(x, y)
    assert rows == [[4], [1, 5], [1, 3], [1, 3, 5], [1, 2, 5], [1, 2, 4, 6], [1, 2, 4, 5]]
    assert "".join(hunt_szymanski(x, y)) == "BDAB"


def test_dna() -> None:
    s1 = "ACCGGTCGAGTGCGCGGAAGCCGGCCGAA"
    s2 = "GTCGTTCGGAATGCCGTTGCTCTGTAAA"
    assert "".join(hunt_szymanski(s1, s2)) == "GTCGTCGGAAGCCGGCCGAA"


def test_edges() -> None:
    assert hunt_szymanski("", "") == []
    assert hunt_szymanski("A", "") == []
    assert hunt_szymanski("ABC", "DEF") == []
    assert hunt_szymanski("AAAA", "AA") == ["A", "A"]
    assert hunt_szymanski("ABCD", "ABCD") == list("ABCD")
    assert hunt_szymanski([1, 2, 3], [3, 2, 1]) in ([1], [2], [3])


def test_random_against_table() -> None:
    rng = random.Random(1977)
    for _ in range(600):
        x = "".join(rng.choice("ABCD"[: rng.randint(1, 4)]) for _ in range(rng.randrange(15)))
        y = "".join(rng.choice("ABCD") for _ in range(rng.randrange(15)))
        z = hunt_szymanski(x, y)
        assert len(z) == table_lcs_length(x, y)
        assert is_subsequence(z, list(x)) and is_subsequence(z, list(y))
