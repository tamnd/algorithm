# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/manber-myers-algorithm/. The authors are listed in prov/D2EGK8.jsonl.

import random

from manber_myers_algorithm import manber_myers


def naive_sa(s: str) -> list[int]:
    return sorted(range(len(s)), key=lambda i: s[i:])


def test_example() -> None:
    assert manber_myers("mississippi") == [10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    assert manber_myers("banana") == [5, 3, 1, 0, 4, 2]


def test_edges() -> None:
    assert manber_myers("") == []
    assert manber_myers("z") == [0]
    assert manber_myers("aaaaa") == [4, 3, 2, 1, 0]
    assert manber_myers("ababab") == [4, 2, 0, 5, 3, 1]
    assert manber_myers("ba") == [1, 0]
    assert manber_myers([5, 2, 5, 2, 9]) == [1, 3, 0, 2, 4]


def test_long_periodic() -> None:
    for s in ("a" * 513, "ab" * 300, "abaababaabaab" * 20):
        assert manber_myers(s) == naive_sa(s)


def test_random_against_naive() -> None:
    rng = random.Random(1990)
    for trial in range(1500):
        sigma = "acgt"[: rng.choice([1, 2, 4])]
        n = rng.randint(0, 40)
        s = "".join(rng.choice(sigma) for _ in range(n))
        if trial % 30 == 0:
            s = rng.choice(["a" * n, "ab" * (n // 2), ""])
        assert manber_myers(s) == naive_sa(s)
