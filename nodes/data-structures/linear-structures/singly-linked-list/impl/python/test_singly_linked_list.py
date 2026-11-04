# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/singly-linked-list/. The authors are listed in prov/QXYA7A.jsonl.

import random

import pytest

from singly_linked_list import SinglyLinkedList


def test_example() -> None:
    lst: SinglyLinkedList[int] = SinglyLinkedList()
    lst.push_front(3)
    lst.push_back(7)
    lst.push_front(1)
    lst.push_back(9)
    assert list(lst) == [1, 3, 7, 9]
    node = lst.search(7)
    assert node is not None and node.key == 7
    lst.insert_after(node, 4)
    assert list(lst) == [1, 3, 7, 4, 9]
    assert lst.delete(3)
    assert list(lst) == [1, 7, 4, 9]
    assert lst.pop_front() == 1
    assert lst.delete(9)
    assert list(lst) == [7, 4]
    assert lst.tail is not None and lst.tail.key == 4
    assert not lst.delete(5)
    lst.check_invariant()


def test_edges() -> None:
    lst: SinglyLinkedList[int] = SinglyLinkedList()
    assert lst.is_empty() and len(lst) == 0
    assert lst.search(1) is None
    assert not lst.delete(1)
    with pytest.raises(IndexError):
        lst.pop_front()
    lst.push_back(5)
    assert lst.head is lst.tail
    assert lst.pop_front() == 5
    assert lst.head is None and lst.tail is None
    lst.check_invariant()
    # delete the only node: tail must become None
    lst.push_front(2)
    assert lst.delete(2)
    assert lst.tail is None
    lst.check_invariant()
    # duplicates: delete removes only the first one
    for k in (4, 4, 4):
        lst.push_back(k)
    assert lst.delete(4)
    assert list(lst) == [4, 4]
    # insert after the tail moves the tail
    t = lst.tail
    assert t is not None
    lst.insert_after(t, 6)
    assert lst.tail is not None and lst.tail.key == 6
    lst.push_back(8)
    assert list(lst) == [4, 4, 6, 8]
    lst.check_invariant()


def test_random_against_list() -> None:
    rng = random.Random(4127)
    for _ in range(600):
        lst: SinglyLinkedList[int] = SinglyLinkedList()
        model: list[int] = []
        for _ in range(rng.randint(0, 40)):
            op = rng.randrange(6)
            k = rng.randint(0, 6)
            if op == 0:
                lst.push_front(k)
                model.insert(0, k)
            elif op == 1:
                lst.push_back(k)
                model.append(k)
            elif op == 2:
                if model:
                    assert lst.pop_front() == model.pop(0)
            elif op == 3:
                node = lst.search(k)
                assert (node is not None) == (k in model)
                if node is not None:
                    lst.insert_after(node, k + 10)
                    model.insert(model.index(k) + 1, k + 10)
            elif op == 4:
                found = k in model
                assert lst.delete(k) == found
                if found:
                    model.remove(k)
            else:
                assert len(lst) == len(model)
            lst.check_invariant()
            assert list(lst) == model
