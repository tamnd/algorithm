# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/suffix-array/. The authors are listed in prov/R5YHHT.jsonl.

import random

from suffix_array import SuffixArray


def naive_sa(s: str) -> list[int]:
    return sorted(range(len(s)), key=lambda i: s[i:])


def naive_occ(s: str, p: str) -> list[int]:
    return [i for i in range(len(s) - len(p) + 1) if s[i:i + len(p)] == p]


def test_example() -> None:
    a = SuffixArray("banana")
    a.check_invariant()
    assert a.sa == [5, 3, 1, 0, 4, 2]
    assert a.rank == [3, 2, 5, 1, 4, 0]
    assert a.range("ana") == (1, 3)
    assert a.locate("ana") == [1, 3]
    assert a.count("na") == 2
    assert a.range("nab") == (5, 5)
    assert a.count("c") == 0
    assert a.range("") == (0, 6)


def test_edges() -> None:
    a = SuffixArray("")
    a.check_invariant()
    assert a.sa == [] and a.locate("a") == []
    assert SuffixArray("x").sa == [0]
    assert SuffixArray("aaaa").sa == [3, 2, 1, 0]
    assert SuffixArray("abab").sa == [2, 0, 3, 1]
    assert SuffixArray("mississippi").sa == [10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    assert SuffixArray([3, 1, 2, 1]).sa == [3, 1, 2, 0]


def test_long_periodic() -> None:
    for s in ("a" * 300, "ab" * 150, "aab" * 100):
        a = SuffixArray(s)
        assert a.sa == naive_sa(s)


def test_random_against_naive() -> None:
    rng = random.Random(9071)
    for trial in range(800):
        sigma = "abcd"[: rng.choice([1, 2, 4])]
        n = rng.randint(0, 20)
        s = "".join(rng.choice(sigma) for _ in range(n))
        if trial % 40 == 0:
            s = rng.choice(["a" * n, "ab" * (n // 2), ""])
        a = SuffixArray(s)
        assert a.sa == naive_sa(s)
        a.check_invariant()
        for _ in range(6):
            p = "".join(rng.choice(sigma) for _ in range(rng.randint(1, 4)))
            if s and rng.random() < 0.5:
                i = rng.randrange(len(s))
                p = s[i:rng.randint(i + 1, len(s))]
            assert a.locate(p) == naive_occ(s, p)
            assert a.count(p) == len(naive_occ(s, p))
