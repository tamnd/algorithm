# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lyndon-based-runs-computation/. The authors are listed in prov/B8YJN8.jsonl.

import itertools
import random

from lyndon_based_runs_computation import LCE, lyndon_array, runs, suffix_array


def smallest_period(w):
    return next(p for p in range(1, len(w) + 1) if all(w[k] == w[k + p] for k in range(len(w) - p)))


def brute_runs(s):
    n = len(s)
    found = set()
    for i in range(n):
        for j in range(i + 1, n):
            w = s[i:j + 1]
            p = smallest_period(w)
            if len(w) >= 2 * p and (i == 0 or s[i - 1] != s[i - 1 + p]) and (j == n - 1 or s[j + 1] != s[j + 1 - p]):
                found.add((i, j, p))
    return sorted(found)


def is_lyndon(u):
    return all(u < u[k:] for k in range(1, len(u)))


def brute_lyndon_array(s):
    return [max(j - i for j in range(i + 1, len(s) + 1) if is_lyndon(s[i:j])) for i in range(len(s))]


def check(s):
    assert runs(s) == brute_runs(s), s
    if s:
        key = list(s)
        assert lyndon_array([ord(c) for c in key]) == brute_lyndon_array(s), s
        assert suffix_array([ord(c) for c in key]) == sorted(range(len(s)), key=lambda i: s[i:]), s


def test_example() -> None:
    assert runs("aabaabaa") == [(0, 1, 1), (0, 7, 3), (3, 4, 1), (6, 7, 1)]
    assert lyndon_array([0, 0, 1, 0, 0, 1, 0, 0]) == [3, 2, 1, 3, 2, 1, 1, 1]
    assert lyndon_array([1, 1, 0, 1, 1, 0, 1, 1]) == [1, 1, 3, 1, 1, 3, 1, 1]
    assert runs("mississippi") == [(1, 7, 3), (2, 3, 1), (5, 6, 1), (8, 9, 1)]


def test_edge_cases() -> None:
    assert runs("") == []
    assert runs("a") == []
    assert runs("ab") == []
    assert runs("aaaa") == [(0, 3, 1)]
    assert runs("abcacb") == []
    assert runs([3, 1, 3, 1, 3]) == [(0, 4, 2)]
    for s in ["abab", "abaababaab", "abacaba", "aabbaabb"]:
        check(s)


def test_lce() -> None:
    s = "abaababaab"
    key = [ord(c) for c in s]
    lce = LCE(key)
    for i in range(len(s) + 1):
        for j in range(len(s) + 1):
            k = 0
            while i + k < len(s) and j + k < len(s) and s[i + k] == s[j + k]:
                k += 1
            assert lce.query(i, j) == k


def test_fibonacci_word() -> None:
    a, b = "a", "ab"
    while len(b) < 300:
        a, b = b, b + a
    rs = runs(b)
    assert len(rs) < len(b)  # the runs theorem
    check(b[:89])


def test_exhaustive_small() -> None:
    for sigma, top in ((1, 10), (2, 11), (3, 7)):
        for n in range(top + 1):
            for w in itertools.product("abc"[:sigma], repeat=n):
                check("".join(w))


def test_random() -> None:
    rng = random.Random(2017)
    for _ in range(600):
        sigma = rng.choice((1, 2, 3))
        n = rng.randint(0, 40)
        s = "".join(rng.choice("abc"[:sigma]) for _ in range(n))
        if rng.random() < 0.3 and n > 0:
            s = s[: rng.randint(1, n)] * rng.randint(2, 4)
        check(s)


if __name__ == "__main__":
    test_example()
    test_edge_cases()
    test_lce()
    test_fibonacci_word()
    test_exhaustive_small()
    test_random()
    print("ok")
