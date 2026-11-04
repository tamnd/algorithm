# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/three-sum-two-pointer-scan/. The authors are listed in prov/V2066X.jsonl.

import itertools
import random

from three_sum_two_pointer_scan import three_sum_two_pointer_scan


def brute(values: list[int], t: int) -> list[tuple[int, int, int]]:
    found = set()
    for i, j, k in itertools.combinations(range(len(values)), 3):
        if values[i] + values[j] + values[k] == t:
            found.add(tuple(sorted((values[i], values[j], values[k]))))
    return sorted(found)


def test_example() -> None:
    assert three_sum_two_pointer_scan([-1, 0, 1, 2, -1, -4]) == [(-1, -1, 2), (-1, 0, 1)]


def test_edges() -> None:
    assert three_sum_two_pointer_scan([]) == []
    assert three_sum_two_pointer_scan([0, 0]) == []
    assert three_sum_two_pointer_scan([0, 0, 0]) == [(0, 0, 0)]
    assert three_sum_two_pointer_scan([0, 0, 0, 0, 0]) == [(0, 0, 0)]
    assert three_sum_two_pointer_scan([1, 1, 1], 3) == [(1, 1, 1)]
    assert three_sum_two_pointer_scan([1, 2, 4]) == []
    assert three_sum_two_pointer_scan([-2, 0, 0, 2, 2]) == [(-2, 0, 2)]
    big = 2**61
    assert three_sum_two_pointer_scan([-2 * big, big, big]) == [(-2 * big, big, big)]


def test_input_not_changed() -> None:
    a = [3, -1, -2, 0]
    three_sum_two_pointer_scan(a)
    assert a == [3, -1, -2, 0]


def test_against_brute_force() -> None:
    rng = random.Random(7031)
    for _ in range(1500):
        n = rng.randrange(0, 11)
        a = [rng.randrange(-6, 7) for _ in range(n)]
        t = rng.randrange(-5, 6)
        assert three_sum_two_pointer_scan(a, t) == brute(a, t)
