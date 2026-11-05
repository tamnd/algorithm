# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/booth-algorithm/. The authors are listed in prov/PTQRP5.jsonl.

import itertools
import random

from booth_algorithm import least_rotation


def brute(s: str) -> int:
    n = len(s)
    if n == 0:
        return 0
    rots = [s[q:] + s[:q] for q in range(n)]
    best = min(rots)
    return rots.index(best)


def test_example() -> None:
    assert least_rotation("cabaab") == 3


def test_edges() -> None:
    cases = {"": 0, "a": 0, "aa": 0, "ab": 0, "ba": 1, "aba": 2, "abab": 0, "bbba": 3, "aaaa": 0}
    for s, k in cases.items():
        assert least_rotation(s) == k


def test_lists() -> None:
    assert least_rotation([3, 1, 2, 1, 1]) == 3
    assert least_rotation([5]) == 0


def test_exhaustive_small() -> None:
    for sigma in (1, 2, 3):
        letters = "abc"[:sigma]
        for n in range(1, 8):
            for w in itertools.product(letters, repeat=n):
                s = "".join(w)
                assert least_rotation(s) == brute(s), s


def test_random() -> None:
    rng = random.Random(20240611)
    for _ in range(1500):
        sigma = rng.choice((1, 2, 3))
        n = rng.randint(0, 40)
        s = "".join(rng.choice("abc"[:sigma]) for _ in range(n))
        if rng.random() < 0.3 and n > 0:
            r = rng.randint(1, 4)
            s = (s[: rng.randint(1, n)]) * r
        assert least_rotation(s) == brute(s), s
