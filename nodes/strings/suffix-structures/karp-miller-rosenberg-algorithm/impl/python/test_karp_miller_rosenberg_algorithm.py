# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karp-miller-rosenberg-algorithm/. The authors are listed in prov/NP7V4M.jsonl.

import random

from karp_miller_rosenberg_algorithm import kmr, longest_repeat, substring_compare, suffix_array


def texts(seed: int, count: int = 600, maxn: int = 18) -> list[str]:
    rng = random.Random(seed)
    out = ["", "a", "aa", "ab", "ba"]
    for n in range(1, 14):
        out += ["a" * n, "ab" * n, "aab" * n]
    for _ in range(count):
        sigma = rng.choice([1, 2, 4])
        out.append("".join(rng.choice("abcd"[:sigma]) for _ in range(rng.randrange(maxn + 1))))
    return out


def naive_names(t: str, length: int) -> list[int]:
    factors = [t[i : i + length] for i in range(len(t) - length + 1)]
    rank = {f: r for r, f in enumerate(sorted(set(factors)))}
    return [rank[f] for f in factors]


def naive_longest_repeat(t: str) -> int:
    best = 0
    for i in range(len(t)):
        for j in range(i + 1, len(t)):
            k = 0
            while j + k < len(t) and t[i + k] == t[j + k]:
                k += 1
            best = max(best, k)
    return best


def test_examples() -> None:
    names = kmr("banana")
    assert names == [[1, 0, 2, 0, 2, 0], [1, 0, 2, 0, 2], [1, 0, 2]]
    assert suffix_array("banana") == [5, 3, 1, 0, 4, 2]
    assert suffix_array("mississippi") == [10, 7, 4, 1, 0, 9, 8, 6, 3, 5, 2]
    assert longest_repeat("mississippi") == (4, 1, 4)
    assert longest_repeat("abcd") == (0, -1, -1)


def test_names_against_brute_force() -> None:
    for t in texts(1):
        names = kmr(t)
        assert len(names) == (len(t).bit_length() if t else 0)
        for j, row in enumerate(names):
            assert row == naive_names(t, 2**j)


def test_suffix_array_against_brute_force() -> None:
    for t in texts(2):
        assert suffix_array(t) == sorted(range(len(t)), key=lambda i: t[i:])


def test_compare_and_repeat_against_brute_force() -> None:
    rng = random.Random(3)
    for t in texts(4):
        n = len(t)
        names = kmr(t)
        for _ in range(10):
            if n == 0:
                break
            length = rng.randint(0, n)
            p, q = rng.randint(0, n - length), rng.randint(0, n - length)
            a, b = t[p : p + length], t[q : q + length]
            assert substring_compare(names, p, q, length) == (a > b) - (a < b)
        length, p, q = longest_repeat(t)
        assert length == naive_longest_repeat(t)
        if length:
            assert p < q and t[p : p + length] == t[q : q + length]
