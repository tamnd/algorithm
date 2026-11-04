# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xor-linked-list/. The authors are listed in prov/GE847R.jsonl.

import random
from collections import deque

import pytest

from xor_linked_list import XorLinkedList


def test_example() -> None:
    xs: XorLinkedList[int] = XorLinkedList()
    assert xs.push_front(10) == 1
    assert xs.push_back(20) == 2
    assert xs.push_back(30) == 3
    assert xs.push_front(5) == 4
    assert xs.to_list() == [5, 10, 20, 30]
    assert [xs.np[a] for a in (4, 1, 2, 3)] == [1, 6, 2, 2]
    xs.check_invariant()
    assert xs.pop_front() == 5
    xs.reverse()
    assert xs.to_list() == [30, 20, 10]
    assert xs.pop_front() == 30
    assert xs.push_front(7) == 3  # the freed address 3 is reused
    assert xs.to_list() == [7, 20, 10]
    xs.check_invariant()


def test_edges() -> None:
    xs: XorLinkedList[int] = XorLinkedList()
    assert xs.to_list() == [] and len(xs) == 0
    with pytest.raises(IndexError):
        xs.pop_front()
    with pytest.raises(IndexError):
        xs.pop_back()
    xs.reverse()
    xs.check_invariant()
    xs.push_back(1)
    xs.reverse()
    assert xs.to_list() == [1]
    assert xs.pop_back() == 1
    assert xs.head == 0 and xs.tail == 0
    xs.check_invariant()


def test_insert_between() -> None:
    xs: XorLinkedList[str] = XorLinkedList()
    a = xs.push_back("a")
    c = xs.push_back("c")
    xs.insert_between(a, c, "b")
    assert xs.to_list() == ["a", "b", "c"]
    xs.check_invariant()
    xs.reverse()
    assert xs.to_list() == ["c", "b", "a"]
    xs.check_invariant()


def test_random_against_deque() -> None:
    rng = random.Random(4711)
    for _ in range(500):
        xs: XorLinkedList[int] = XorLinkedList()
        model: deque[int] = deque()
        for _ in range(rng.randint(0, 60)):
            op = rng.randrange(5)
            v = rng.randint(-10**18, 10**18)
            if op == 0:
                xs.push_front(v)
                model.appendleft(v)
            elif op == 1:
                xs.push_back(v)
                model.append(v)
            elif op == 2 and model:
                assert xs.pop_front() == model.popleft()
            elif op == 3 and model:
                assert xs.pop_back() == model.pop()
            elif op == 4:
                xs.reverse()
                model.reverse()
            xs.check_invariant()
            assert len(xs) == len(model)
        assert xs.to_list() == list(model)
