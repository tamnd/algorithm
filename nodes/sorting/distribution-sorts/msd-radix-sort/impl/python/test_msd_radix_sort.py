# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/msd-radix-sort/. The authors are listed in prov/5YMPGZ.jsonl.

import random

from msd_radix_sort import msd_radix_sort


def test_example() -> None:
    a = ["she", "sells", "sea", "shells", "by", "the", "sea", "shore"]
    assert msd_radix_sort(a) == ["by", "sea", "sea", "sells", "she", "shells", "shore", "the"]


def test_edges() -> None:
    assert msd_radix_sort([]) == []
    assert msd_radix_sort(["x"]) == ["x"]
    assert msd_radix_sort(["", "a", ""]) == ["", "", "a"]
    assert msd_radix_sort(["ab", "a", "abc", "a"]) == ["a", "a", "ab", "abc"]
    assert msd_radix_sort(["b", "a"], r=128) == ["a", "b"]


def test_long_common_prefix() -> None:
    p = "q" * 5000
    a = [p + "b", p, p + "a", p]
    assert msd_radix_sort(a) == sorted(a)


def test_random_against_sorted() -> None:
    rng = random.Random(3301)
    for _ in range(600):
        a = ["".join(rng.choice("abc") for _ in range(rng.randint(0, 6))) for _ in range(rng.randint(0, 30))]
        assert msd_radix_sort(list(a)) == sorted(a)
