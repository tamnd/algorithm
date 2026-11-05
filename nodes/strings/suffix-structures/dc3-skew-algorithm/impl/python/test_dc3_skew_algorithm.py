# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dc3-skew-algorithm/. The authors are listed in prov/M5ZHTB.jsonl.

import random

from dc3_skew_algorithm import dc3


def texts(seed: int, count: int = 900, maxn: int = 40) -> list:
    rng = random.Random(seed)
    out: list = ["", "a", "aa", "ab", "ba", "aaa", "aba"]
    for n in range(1, 25):
        out += ["a" * n, "ab" * n, "aab" * n, "abc" * n]
    for _ in range(count):
        sigma = rng.choice([1, 2, 4])
        out.append("".join(rng.choice("abcd"[:sigma]) for _ in range(rng.randrange(maxn + 1))))
    return out


def naive_sa(t) -> list[int]:
    return sorted(range(len(t)), key=lambda i: t[i:])


def test_examples() -> None:
    assert dc3("banana") == [5, 3, 1, 0, 4, 2]
    assert dc3("mississippi") == [10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    assert dc3("yabbadabbado") == naive_sa("yabbadabbado")
    assert dc3("") == []


def test_against_naive_sort() -> None:
    for t in texts(1):
        assert dc3(t) == naive_sa(t), t


def test_integer_alphabets() -> None:
    rng = random.Random(2)
    for _ in range(300):
        t = [rng.randrange(rng.choice([1, 2, 4, 100])) for _ in range(rng.randrange(60))]
        assert dc3(t) == naive_sa(t)


def test_long_texts() -> None:
    rng = random.Random(3)
    for t in ["a" * 3000, "ab" * 1500 + "a", "".join(rng.choice("ab") for _ in range(3000))]:
        assert dc3(t) == naive_sa(t)
