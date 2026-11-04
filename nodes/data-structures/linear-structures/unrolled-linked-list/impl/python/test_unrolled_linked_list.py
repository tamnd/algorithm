# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unrolled-linked-list/. The authors are listed in prov/YWD1E5.jsonl.

import random

import pytest

from unrolled_linked_list import UnrolledLinkedList


def test_example() -> None:
    xs: UnrolledLinkedList[int] = UnrolledLinkedList(4)
    for x in (10, 20, 30, 40):
        xs.append(x)
    assert xs.blocks() == [4]
    xs.insert(1, 15)
    assert xs.blocks() == [3, 2]  # split
    xs.insert(5, 50)
    xs.insert(6, 60)
    assert xs.to_list() == [10, 15, 20, 30, 40, 50, 60]
    assert xs.get(3) == 30 and xs.get(5) == 50
    assert xs.delete(0) == 10
    assert xs.blocks() == [2, 4]
    assert xs.delete(0) == 15
    assert xs.blocks() == [2, 3]  # borrow
    assert xs.to_list() == [20, 30, 40, 50, 60]
    assert xs.delete(3) == 50
    assert xs.delete(2) == 40
    assert xs.blocks() == [3]  # merge
    assert xs.to_list() == [20, 30, 60]
    xs.check_invariant()


def test_edges() -> None:
    xs: UnrolledLinkedList[int] = UnrolledLinkedList(2)
    assert xs.to_list() == [] and len(xs) == 0
    with pytest.raises(IndexError):
        xs.get(0)
    with pytest.raises(IndexError):
        xs.delete(0)
    with pytest.raises(IndexError):
        xs.insert(1, 5)
    with pytest.raises(ValueError):
        UnrolledLinkedList(1)
    xs.insert(0, 7)
    assert xs.delete(0) == 7
    assert xs.head is None and xs.blocks() == []
    for x in range(9):
        xs.insert(0, x)
        xs.check_invariant()
    assert xs.to_list() == list(range(8, -1, -1))
    xs.set(4, 99)
    assert xs.get(4) == 99


def test_block_count_bound() -> None:
    b = 8
    xs: UnrolledLinkedList[int] = UnrolledLinkedList(b)
    rng = random.Random(5)
    for _ in range(2000):
        xs.insert(rng.randint(0, len(xs)), 1)
    for _ in range(1500):
        xs.delete(rng.randrange(len(xs)))
    xs.check_invariant()
    k = len(xs.blocks())
    assert k <= max(1, len(xs) // (b // 2))


def test_random_against_list() -> None:
    rng = random.Random(8128)
    for _ in range(500):
        b = rng.randint(2, 7)
        xs: UnrolledLinkedList[int] = UnrolledLinkedList(b)
        model: list[int] = []
        for _ in range(rng.randint(0, 80)):
            op = rng.randrange(4)
            if op <= 1:
                i = rng.randint(0, len(model))
                v = rng.randint(-10**18, 10**18)
                xs.insert(i, v)
                model.insert(i, v)
            elif op == 2 and model:
                i = rng.randrange(len(model))
                assert xs.delete(i) == model.pop(i)
            elif model:
                i = rng.randrange(len(model))
                assert xs.get(i) == model[i]
            xs.check_invariant()
            assert len(xs) == len(model)
        assert xs.to_list() == model
