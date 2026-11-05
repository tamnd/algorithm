# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lyndon-array/. The authors are listed in prov/KRWVSH.jsonl.

import itertools
import random
from typing import List

from lyndon_array import LyndonArray, inverse_suffix_array


def is_lyndon(w: str) -> bool:
    return len(w) > 0 and all(w < w[i:] + w[:i] for i in range(1, len(w)))


def brute_lam(s: str) -> List[int]:
    n = len(s)
    return [max(m for m in range(1, n - i + 1) if is_lyndon(s[i : i + m])) for i in range(n)]


def brute_factors(s: str) -> List[int]:
    # Greedy longest Lyndon prefix, which is the Lyndon factorization.
    out, i = [], 0
    while i < len(s):
        out.append(i)
        i += max(m for m in range(1, len(s) - i + 1) if is_lyndon(s[i : i + m]))
    return out


def test_example() -> None:
    s = "abaabaabb"
    assert inverse_suffix_array(s) == [2, 6, 0, 3, 7, 1, 4, 8, 5]
    a = LyndonArray(s)
    a.check_invariant()
    assert a.lam == [2, 1, 7, 2, 1, 4, 3, 1, 1]
    assert a.query(2) == 7
    assert a.factors(0) == [0, 2]
    assert a.factors(3) == [3, 5]


def test_edges() -> None:
    assert LyndonArray("").lam == []
    assert LyndonArray("a").lam == [1]
    assert LyndonArray("aa").lam == [1, 1]
    assert LyndonArray("aba").lam == [2, 1, 1]
    assert LyndonArray("ab").lam == [2, 1]
    assert LyndonArray([2, 1, 3]).lam == [1, 2, 1]


def test_exhaustive_small() -> None:
    for sigma in (1, 2, 3):
        for n in range(0, 10 if sigma < 3 else 7):
            for t in itertools.product("abc"[:sigma], repeat=n):
                s = "".join(t)
                a = LyndonArray(s)
                assert a.lam == brute_lam(s), s


def test_random() -> None:
    rng = random.Random(2003)
    for _ in range(600):
        sigma = rng.choice((1, 2, 3))
        n = rng.randint(0, 30)
        s = "".join(rng.choice("abc"[:sigma]) for _ in range(n))
        a = LyndonArray(s)
        a.check_invariant()
        assert a.lam == brute_lam(s), s
        i = rng.randint(0, n)
        assert a.factors(i) == [i + f for f in brute_factors(s[i:])], (s, i)
