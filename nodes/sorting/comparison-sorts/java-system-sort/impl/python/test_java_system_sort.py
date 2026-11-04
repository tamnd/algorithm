# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/java-system-sort/. The authors are listed in prov/YQKT8T.jsonl.

import random

import java_system_sort as js
from java_system_sort import java_system_sort


class Key:
    def __init__(self, k: int, tag: int) -> None:
        self.k, self.tag = k, tag

    def __lt__(self, other: "Key") -> bool:
        return self.k < other.k


def test_example_objects() -> None:
    a = [str(x) for x in [3, 4, 5, 6, 0, 1, 9, 8, 7, 2]]
    java_system_sort(a)
    assert a == [str(x) for x in range(10)]


def test_example_primitives() -> None:
    a = [(37 * i) % 101 for i in range(101)]
    java_system_sort(a)
    assert a == list(range(101))


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1, 1], [3, 2, 1], [2**63 - 1, -(2**63)], ["b", "a"], [1.5, -2.0, 0.0]):
        b = list(a)
        java_system_sort(b)
        assert b == sorted(a)


def test_objects_are_stable() -> None:
    rng = random.Random(7)
    for n in (10, 100, 1000):
        a = [Key(rng.randint(0, 9), i) for i in range(n)]
        java_system_sort(a)
        assert all(
            a[i].k < a[i + 1].k or (a[i].k == a[i + 1].k and a[i].tag < a[i + 1].tag) for i in range(n - 1)
        )


def test_heapsort_fallback() -> None:
    rng = random.Random(3)
    a = [rng.randint(0, 50) for _ in range(500)]
    b = list(a)
    js._sort_primitive(b, 0, len(b) - 1, 1)
    assert b == sorted(a)


def test_runs_and_patterns() -> None:
    n = 2000
    for a in (
        list(range(n)),
        list(range(n, 0, -1)),
        [i % 17 for i in range(n)],
        [0] * n,
        list(range(n // 2)) + list(range(n // 2)),
    ):
        b = [str(x).zfill(5) for x in a]
        c = list(a)
        java_system_sort(b)
        java_system_sort(c)
        assert b == sorted(b) and c == sorted(a)


def test_random_against_sorted() -> None:
    rng = random.Random(1997)
    for t in range(600):
        n = rng.randint(0, 400)
        a = [rng.randint(-50, 50) for _ in range(n)]
        if t % 2:
            a = [str(x) for x in a]
        b = list(a)
        java_system_sort(b)
        assert b == sorted(a)
