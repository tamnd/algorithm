# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/doubly-linked-list/. The authors are listed in prov/B9V487.jsonl.

import random

import pytest

from doubly_linked_list import DoublyLinkedList


def test_page_example() -> None:
    L: DoublyLinkedList[int] = DoublyLinkedList()
    n1 = L.push_back(1)
    n2 = L.push_back(2)
    L.push_back(3)
    n5 = L.insert_after(n1, 5)
    assert list(L) == [1, 5, 2, 3]
    assert L.delete(n2) == 2
    assert list(L) == [1, 5, 3]
    L.push_front(9)
    assert L.pop_back() == 3
    assert list(L) == [9, 1, 5]
    assert L.search(5) is n5
    assert L.search(4) is None
    assert L.nil.next.key == 9 and L.nil.prev is n5
    L.check_invariant()


def test_empty() -> None:
    L: DoublyLinkedList[int] = DoublyLinkedList()
    L.check_invariant()
    assert len(L) == 0 and list(L) == []
    assert L.search(1) is None
    with pytest.raises(IndexError):
        L.pop_front()
    with pytest.raises(IndexError):
        L.pop_back()
    with pytest.raises(IndexError):
        L.delete(L.nil)


def test_single_item() -> None:
    L: DoublyLinkedList[str] = DoublyLinkedList()
    v = L.push_front("a")
    L.check_invariant()
    assert L.delete(v) == "a"
    L.check_invariant()
    assert list(L) == []
    L.push_back("b")
    assert L.pop_front() == "b"
    L.check_invariant()


def test_insert_before_and_duplicates() -> None:
    L: DoublyLinkedList[int] = DoublyLinkedList()
    a = L.push_back(7)
    L.insert_before(a, 7)
    first = L.search(7)
    assert first is not a and first is L.nil.next
    L.check_invariant()


def test_random_against_list() -> None:
    rng = random.Random(20261104)
    for _ in range(600):
        L: DoublyLinkedList[int] = DoublyLinkedList()
        model: list[int] = []
        nodes: list = []
        for _ in range(rng.randrange(1, 40)):
            op = rng.randrange(7)
            x = rng.randrange(10)
            if op == 0:
                nodes.insert(0, L.push_front(x)); model.insert(0, x)
            elif op == 1:
                nodes.append(L.push_back(x)); model.append(x)
            elif op == 2 and model:
                i = rng.randrange(len(model))
                nodes.insert(i + 1, L.insert_after(nodes[i], x)); model.insert(i + 1, x)
            elif op == 3 and model:
                i = rng.randrange(len(model))
                nodes.insert(i, L.insert_before(nodes[i], x)); model.insert(i, x)
            elif op == 4 and model:
                i = rng.randrange(len(model))
                assert L.delete(nodes.pop(i)) == model.pop(i)
            elif op == 5 and model:
                assert L.pop_front() == model.pop(0); nodes.pop(0)
            elif op == 6 and model:
                assert L.pop_back() == model.pop(); nodes.pop()
            L.check_invariant()
            assert list(L) == model and len(L) == len(model)
            got = L.search(x)
            if x in model:
                assert got is nodes[model.index(x)]
            else:
                assert got is None
