# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/main-lorentz-algorithm/. The authors are listed in prov/W9BQDM.jsonl.

import itertools
import random

from main_lorentz_algorithm import is_square_free, main_lorentz, square_occurrences, z_function


def brute(s):
    n = len(s)
    return sorted(
        (i, m)
        for m in range(1, n // 2 + 1)
        for i in range(n - 2 * m + 1)
        if s[i:i + m] == s[i + m:i + 2 * m]
    )


def check(s):
    triples = main_lorentz(s)
    occ = [(i, m) for lo, hi, m in triples for i in range(lo, hi + 1)]
    assert len(occ) == len(set(occ)), s  # each square is reported once
    assert sorted(occ) == brute(s), s
    assert all(lo <= hi for lo, hi, _ in triples), s


def test_example() -> None:
    assert sorted(main_lorentz("abaabaa")) == [(0, 0, 3), (1, 1, 3), (2, 2, 1), (5, 5, 1)]
    assert square_occurrences("abaabaa") == [(0, 3), (1, 3), (2, 1), (5, 1)]


def test_z_function() -> None:
    assert z_function("aabxaab") == [7, 1, 0, 0, 3, 1, 0]
    assert z_function("") == []


def test_edge_cases() -> None:
    for s in ["", "a", "ab", "aa", "aaaa", "abcacb", "abacaba"]:
        check(s)
    assert is_square_free("abcacb") and is_square_free("") and is_square_free("abacaba")
    assert not is_square_free("aa")
    assert square_occurrences([1, 2, 1, 2]) == [(0, 2)]
    assert len(square_occurrences("a" * 10)) == 25  # sum over m of 10 - 2m + 1


def test_triples_count() -> None:
    # The number of triples is O(n log n) even when the squares are quadratic.
    for n in (16, 64, 256):
        t = main_lorentz("a" * n)
        assert len(t) <= 2 * n * max(1, n.bit_length())


def test_exhaustive_small() -> None:
    for sigma, top in ((1, 12), (2, 12), (3, 8)):
        for n in range(top + 1):
            for w in itertools.product("abc"[:sigma], repeat=n):
                check("".join(w))


def test_random() -> None:
    rng = random.Random(1984)
    for _ in range(600):
        sigma = rng.choice((1, 2, 3))
        n = rng.randint(0, 60)
        s = "".join(rng.choice("abc"[:sigma]) for _ in range(n))
        if rng.random() < 0.3 and n > 0:
            s = s[: rng.randint(1, n)] * rng.randint(2, 4)
        check(s)


if __name__ == "__main__":
    test_example()
    test_z_function()
    test_edge_cases()
    test_triples_count()
    test_exhaustive_small()
    test_random()
    print("ok")
