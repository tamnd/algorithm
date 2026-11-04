# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/circular-linked-list/. The authors are listed in prov/N4ZP5Y.jsonl.

import random

import pytest

from circular_linked_list import CircularLinkedList, josephus


def test_page_example() -> None:
    L: CircularLinkedList[int] = CircularLinkedList()
    for x in (1, 2, 3):
        L.push_back(x)
    L.push_front(0)
    assert list(L) == [0, 1, 2, 3] and L.last.key == 3
    L.rotate()
    assert list(L) == [1, 2, 3, 0] and L.last.key == 0
    assert L.pop_front() == 1
    L.rotate()
    assert list(L) == [3, 0, 2] and L.last.key == 2
    assert L.pop_front() == 3
    assert list(L) == [0, 2]
    L.check_invariant()


def test_josephus_example() -> None:
    assert josephus(7, 3) == [3, 6, 2, 7, 5, 1, 4]
    assert josephus(1, 5) == [1]
    assert josephus(5, 1) == [1, 2, 3, 4, 5]


def test_empty_and_single() -> None:
    L: CircularLinkedList[str] = CircularLinkedList()
    L.check_invariant()
    with pytest.raises(IndexError):
        L.pop_front()
    with pytest.raises(IndexError):
        L.rotate()
    L.push_back("a")
    assert L.last is not None and L.last.next is L.last
    L.rotate()
    assert list(L) == ["a"]
    assert L.pop_front() == "a"
    assert L.last is None
    L.check_invariant()


def test_random_against_list() -> None:
    rng = random.Random(4242)
    for _ in range(600):
        L: CircularLinkedList[int] = CircularLinkedList()
        model: list[int] = []
        for _ in range(rng.randrange(1, 40)):
            op = rng.randrange(4)
            x = rng.randrange(100)
            if op == 0:
                L.push_front(x); model.insert(0, x)
            elif op == 1:
                L.push_back(x); model.append(x)
            elif op == 2 and model:
                assert L.pop_front() == model.pop(0)
            elif op == 3 and model:
                L.rotate(); model.append(model.pop(0))
            L.check_invariant()
            assert list(L) == model
            if model:
                assert L.front() == model[0]


def test_josephus_random_against_list() -> None:
    rng = random.Random(7)
    for _ in range(500):
        n, k = rng.randrange(1, 15), rng.randrange(1, 6)
        people, i, order = list(range(1, n + 1)), 0, []
        while people:
            i = (i + k - 1) % len(people)
            order.append(people.pop(i))
        assert josephus(n, k) == order
