# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-search/. The authors are listed in prov/2B7QDX.jsonl.

import random

from binary_search import binary_search


def test_examples() -> None:
    a = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    assert binary_search(a, 23) == 5
    assert binary_search(a, 2) == 0
    assert binary_search(a, 91) == 9
    assert binary_search(a, 30) == -1
    assert binary_search(a, 1) == -1
    assert binary_search(a, 100) == -1


def test_empty_and_single() -> None:
    assert binary_search([], 1) == -1
    assert binary_search([7], 7) == 0
    assert binary_search([7], 3) == -1


def test_duplicates() -> None:
    a = [1, 3, 3, 3, 5]
    assert a[binary_search(a, 3)] == 3


def test_strings() -> None:
    assert binary_search(["ant", "bee", "cat"], "bee") == 1


def test_random_against_linear_scan() -> None:
    rng = random.Random(2150)
    for _ in range(2000):
        a = sorted(rng.randint(-20, 20) for _ in range(rng.randint(0, 30)))
        x = rng.randint(-25, 25)
        i = binary_search(a, x)
        if x in a:
            assert 0 <= i < len(a) and a[i] == x
        else:
            assert i == -1


def test_every_position_and_gap_small_sizes() -> None:
    # Exhaustive boundary test: every index and every gap, n = 0 .. 64.
    for n in range(65):
        a = list(range(0, 2 * n, 2))
        for i in range(n):
            assert binary_search(a, 2 * i) == i
        for g in range(-1, 2 * n + 1, 2):
            assert binary_search(a, g) == -1


def test_step_count_is_at_most_floor_lg_n_plus_one() -> None:
    class Key:
        compares = 0

        def __init__(self, v: int) -> None:
            self.v = v

        def __lt__(self, other: "Key") -> bool:
            Key.compares += 1
            return self.v < other.v

    for n in range(1, 130):
        a = [Key(2 * i) for i in range(n)]
        bound = 2 * n.bit_length()  # two two-way tests per step, floor(lg n) + 1 steps
        for v in range(-1, 2 * n + 1):
            Key.compares = 0
            binary_search(a, Key(v))
            assert Key.compares <= bound


def test_large_indices() -> None:
    a = range(0, 10**12, 3)  # a sorted sequence with about 3.3e11 items
    assert binary_search(a, 3 * 123456789012) == 123456789012
    assert binary_search(a, 3 * 123456789012 + 1) == -1
