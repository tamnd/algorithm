# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-search/. The authors are listed in prov/GDCGR7.jsonl.

import random

from linear_search import linear_search


def test_example() -> None:
    a = [7, 3, 9, 3, 1, 8]
    assert linear_search(a, 3) == 1
    assert linear_search(a, 7) == 0
    assert linear_search(a, 8) == 5
    assert linear_search(a, 5) == -1


def test_edges() -> None:
    assert linear_search([], 1) == -1
    assert linear_search([4], 4) == 0
    assert linear_search([4], 5) == -1
    assert linear_search([2, 2, 2], 2) == 0
    assert linear_search(["b", "a"], "a") == 1


def test_no_order_needed() -> None:
    # Items without an order: only == is used.
    a = [{1}, {2, 3}, {4}]
    assert linear_search(a, {3, 2}) == 1


def test_number_of_tests() -> None:
    class Counted:
        tests = 0

        def __init__(self, v: int) -> None:
            self.v = v

        def __eq__(self, other: object) -> bool:
            Counted.tests += 1
            return isinstance(other, Counted) and self.v == other.v

    a = [Counted(v) for v in [7, 3, 9, 3, 1, 8]]
    Counted.tests = 0
    assert linear_search(a, Counted(1)) == 4
    assert Counted.tests == 5
    Counted.tests = 0
    assert linear_search(a, Counted(5)) == -1
    assert Counted.tests == 6


def test_random_against_list_index() -> None:
    rng = random.Random(4417)
    for _ in range(2000):
        a = [rng.randint(-10, 10) for _ in range(rng.randint(0, 25))]
        x = rng.randint(-12, 12)
        want = a.index(x) if x in a else -1
        assert linear_search(a, x) == want
