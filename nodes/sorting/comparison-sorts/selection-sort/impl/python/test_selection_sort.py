# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selection-sort/. The authors are listed in prov/6ADSAW.jsonl.

import random

from selection_sort import selection_sort


def test_example() -> None:
    a = [29, 10, 14, 37, 13, 5, 22]
    selection_sort(a)
    assert a == [5, 10, 13, 14, 22, 29, 37]


def test_edges_and_extremes() -> None:
    cases = (
        [],
        [7],
        [4, 4, 4, 4],
        [2, 1],
        [1, 2, 3, 4],
        [4, 3, 2, 1],
        [-(2**63), 2**63 - 1, 0, -1, 1],
    )
    for values in cases:
        a = list(values)
        selection_sort(a)
        assert a == sorted(values)


class Item:
    def __init__(self, key: int, label: str) -> None:
        self.key = key
        self.label = label

    def __lt__(self, other: "Item") -> bool:
        return self.key < other.key


def _select_last_minimum(a: list[Item]) -> None:
    """Sort a with <= at line L4, the wrong variant of the pitfall. Only for this test."""
    n = len(a)
    for i in range(0, n - 1):
        min_index = i
        for j in range(i + 1, n):
            if a[j].key <= a[min_index].key:
                min_index = j
        a[i], a[min_index] = a[min_index], a[i]


def test_equal_items_can_change_order() -> None:
    a = [Item(2, "a"), Item(2, "b"), Item(1, "c")]
    selection_sort(a)
    assert [(item.key, item.label) for item in a] == [
        (1, "c"),
        (2, "b"),
        (2, "a"),
    ]


def test_first_minimum_is_kept_and_last_minimum_reverses() -> None:
    first = [Item(2, "a"), Item(1, "b"), Item(1, "c")]
    selection_sort(first)
    assert [(item.key, item.label) for item in first] == [
        (1, "b"),
        (1, "c"),
        (2, "a"),
    ]

    last = [Item(2, "a"), Item(1, "b"), Item(1, "c")]
    _select_last_minimum(last)
    assert [(item.key, item.label) for item in last] == [
        (1, "c"),
        (1, "b"),
        (2, "a"),
    ]


def test_random_against_brute_force() -> None:
    rng = random.Random(2150)
    for _ in range(500):
        values = [rng.randint(-50, 50) for _ in range(rng.randint(0, 30))]
        expected = sorted(values)
        a = list(values)
        selection_sort(a)
        assert a == expected
