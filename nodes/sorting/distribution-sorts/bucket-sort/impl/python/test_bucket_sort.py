# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bucket-sort/. The authors are listed in prov/HHT9WC.jsonl.

import math
import random

from bucket_sort import bucket_index, bucket_sort


def sort_copy(a: list) -> list:
    b = list(a)
    bucket_sort(b)
    return b


def test_example() -> None:
    a = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
    beta = bucket_index(a, 10)
    assert [beta(x) for x in a] == [7, 1, 3, 2, 7, 9, 2, 1, 2, 6]
    assert sort_copy(a) == [0.12, 0.17, 0.21, 0.23, 0.26, 0.39, 0.68, 0.72, 0.78, 0.94]


def test_edges() -> None:
    assert sort_copy([]) == []
    assert sort_copy([0.5]) == [0.5]
    assert sort_copy([0.3, 0.3, 0.3]) == [0.3, 0.3, 0.3]
    top = math.nextafter(1.0, 0.0)
    assert sort_copy([top, 0.0, top]) == [0.0, top, top]
    big = [2**63 - 1, -(2**63), 0, -1, 1, 2**63 - 1]
    assert sort_copy(big) == sorted(big)
    assert sort_copy(["pear", "", "apple", "ab", "a", "fig"]) == ["", "a", "ab", "apple", "fig", "pear"]
    assert sort_copy([2.5, -1.0, 7.25]) == [-1.0, 2.5, 7.25]


def test_rounding_at_the_top() -> None:
    lo, hi = -4.286139999468759, 1.3086794732495628
    x = math.nextafter(hi, lo)
    a = [lo, x] + [lo + (hi - lo) * i / 917 for i in range(917)]
    assert sort_copy(a) == sorted(a)


def test_one_bucket_worst_case() -> None:
    a = [0.5 + i * 1e-9 for i in range(200, 0, -1)]
    assert sort_copy(a) == sorted(a)


def test_stable() -> None:
    class Key(float):
        pass

    a = [Key(0.25), Key(0.25), Key(0.1)]
    ids = [id(x) for x in a]
    b = list(a)
    bucket_sort(b)
    assert [id(x) for x in b] == [ids[2], ids[0], ids[1]]


def test_random_against_sorted() -> None:
    rng = random.Random(9050)
    for _ in range(600):
        kind = rng.randrange(3)
        m = rng.randint(0, 60)
        if kind == 0:
            a: list = [rng.random() ** rng.choice([1, 3]) for _ in range(m)]
        elif kind == 1:
            a = [rng.randint(-50, 50) for _ in range(m)]
        else:
            a = ["".join(rng.choice("abc") for _ in range(rng.randint(0, 6))) for _ in range(m)]
        assert sort_copy(a) == sorted(a)
