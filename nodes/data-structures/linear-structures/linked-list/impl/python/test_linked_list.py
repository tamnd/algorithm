# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linked-list/. The authors are listed in prov/8R26VK.jsonl.

import random

import pytest

from linked_list import LinkedList


def test_page_example() -> None:
    a: LinkedList[int] = LinkedList()
    a.push_front(3)
    seven = a.push_front(7)
    assert list(a) == [7, 3]
    five = a.insert_after(seven, 5)
    assert list(a) == [7, 5, 3]
    assert a.search(5) is five
    assert a.search(4) is None
    assert a.delete_after(five) == 3
    assert list(a) == [7, 5]
    assert a.delete_front() == 7
    assert list(a) == [5]
    a.check_invariant()


def test_edges() -> None:
    a: LinkedList[int] = LinkedList()
    with pytest.raises(IndexError):
        a.delete_front()
    with pytest.raises(IndexError):
        a.node_at(0)
    v = a.push_front(1)
    with pytest.raises(IndexError):
        a.delete_after(v)  # the last node has no successor
    a.insert_after(v, 1)
    assert a.search(1) is v  # the first of two equal keys
    assert a.node_at(1).next is None
    assert a.delete_front() == 1
    assert a.delete_front() == 1
    assert a.head is None and len(a) == 0


def test_random_against_list() -> None:
    rng = random.Random(8261)
    for _ in range(500):
        a: LinkedList[int] = LinkedList()
        model: list[int] = []
        for _ in range(40):
            op = rng.randrange(4)
            x = rng.randint(0, 5)
            if op == 0:
                i = rng.randint(0, len(model))
                if i == 0:
                    a.push_front(x)
                else:
                    a.insert_after(a.node_at(i - 1), x)
                model.insert(i, x)
            elif op == 1 and model:
                i = rng.randrange(len(model))
                got = a.delete_front() if i == 0 else a.delete_after(a.node_at(i - 1))
                assert got == model.pop(i)
            elif op == 2 and model:
                i = rng.randrange(len(model))
                assert a.node_at(i).key == model[i]
            else:
                p = a.search(x)
                if x in model:
                    assert p is a.node_at(model.index(x))
                else:
                    assert p is None
            a.check_invariant()
            assert list(a) == model
