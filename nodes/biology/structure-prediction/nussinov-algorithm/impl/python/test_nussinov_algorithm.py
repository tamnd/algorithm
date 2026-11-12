# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nussinov-algorithm/. The authors are listed in prov/6XRW3C.jsonl.

import random
from typing import Iterator

from nussinov_algorithm import can_pair, is_secondary_structure, nussinov, nussinov_table, to_dot_bracket


def all_structures(s: str, m: int = 3) -> Iterator[list[tuple[int, int]]]:
    """Every secondary structure of s, by brute force over the partner of the first base.

    The recursion depth is at most the length of s, which is small in these tests.
    """

    def rec(i: int, j: int) -> Iterator[list[tuple[int, int]]]:
        if j - i < 1:
            yield []
            return
        for rest in rec(i + 1, j):  # base i unpaired
            yield rest
        for k in range(i + m + 1, j + 1):  # base i pairs with k
            if can_pair(s[i], s[k]):
                for inner in rec(i + 1, k - 1):
                    for outer in rec(k + 1, j):
                        yield [(i, k)] + inner + outer

    yield from rec(0, len(s) - 1)


def test_example() -> None:
    best, st = nussinov("GGGAAAUCC")
    assert best == 3
    assert to_dot_bracket(9, st) == "(((...)))"


def test_worked_example() -> None:
    s = "GCAAAGCAAAGC"
    N = nussinov_table(s)
    assert N[1][10] == 2 and N[1][5] == 1 and N[0][4] == 0
    best, st = nussinov(s)
    assert best == 3
    assert to_dot_bracket(12, st) == "((...)(...))"


def test_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randint(0, 12)
        s = "".join(rng.choice("ACGU") for _ in range(n))
        structs = list(all_structures(s))
        assert all(is_secondary_structure(s, t) for t in structs)
        assert len({tuple(sorted(t)) for t in structs}) == len(structs)
        best, st = nussinov(s)
        assert best == max(len(t) for t in structs)
        assert is_secondary_structure(s, st) and len(st) == best


def test_other_hairpin_minimum() -> None:
    rng = random.Random(11)
    for m in (0, 1, 2):
        for _ in range(100):
            s = "".join(rng.choice("ACGU") for _ in range(rng.randint(1, 10)))
            brute = max(len(t) for t in all_structures(s, m))
            best, st = nussinov(s, m)
            assert best == brute
            assert is_secondary_structure(s, st, m)


def test_table_monotone() -> None:
    s = "GGGGAAAACCCCUUUUAAAAGGGG"
    N = nussinov_table(s)
    n = len(s)
    for i in range(n):
        for j in range(i + 1, n):
            assert N[i][j] >= N[i][j - 1]
            assert N[i][j] >= N[i + 1][j]
            assert N[i][j] <= N[i][j - 1] + 1
