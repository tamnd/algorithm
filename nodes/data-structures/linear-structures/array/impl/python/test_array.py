# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/array/. The authors are listed in prov/43DJ9Z.jsonl.

import random

import pytest

from array import Array


def test_page_example() -> None:
    a: Array[int] = Array(8)
    steps = []
    for i, x in [(0, 5), (1, 8), (1, 3), (0, 9)]:
        before = a.moves
        a.insert(i, x)
        steps.append(a.moves - before)
    assert a.to_list() == [9, 5, 3, 8]
    assert steps == [0, 0, 1, 3]
    assert a.get(2) == 3
    a.set(3, 7)
    assert a.to_list() == [9, 5, 3, 7]
    before = a.moves
    assert a.delete(1) == 5
    assert a.moves - before == 2
    assert a.to_list() == [9, 3, 7]
    assert a.cells[3] == 7  # the stale copy stays beyond n
    assert a.search(7) == 2
    assert a.search(4) is None


def test_edges() -> None:
    a: Array[int] = Array(0)
    with pytest.raises(OverflowError):
        a.insert(0, 1)
    b: Array[int] = Array(2)
    with pytest.raises(IndexError):
        b.get(0)
    with pytest.raises(IndexError):
        b.insert(1, 1)  # index n + 1 is not allowed
    b.insert(0, 1)
    b.insert(1, 1)
    with pytest.raises(OverflowError):
        b.insert(0, 2)
    assert b.search(1) == 0  # the first index of an item that occurs twice
    assert b.delete(1) == 1
    assert b.delete(0) == 1
    assert len(b) == 0
    with pytest.raises(IndexError):
        b.delete(0)


def test_moves_count() -> None:
    a: Array[int] = Array(20)
    for k in range(10):
        a.insert(k, k)
    before = a.moves
    a.insert(0, -1)
    assert a.moves - before == 10
    before = a.moves
    a.delete(0)
    assert a.moves - before == 10


def test_random_against_list() -> None:
    rng = random.Random(4301)
    for _ in range(500):
        cap = rng.randint(0, 12)
        a: Array[int] = Array(cap)
        model: list[int] = []
        for _ in range(40):
            op = rng.randrange(4)
            if op == 0 and len(model) < cap:
                i = rng.randint(0, len(model))
                x = rng.randint(0, 5)
                a.insert(i, x)
                model.insert(i, x)
            elif op == 1 and model:
                i = rng.randrange(len(model))
                assert a.delete(i) == model.pop(i)
            elif op == 2 and model:
                i = rng.randrange(len(model))
                x = rng.randint(0, 5)
                a.set(i, x)
                model[i] = x
                assert a.get(i) == x
            else:
                x = rng.randint(0, 5)
                want = model.index(x) if x in model else None
                assert a.search(x) == want
            a.check_invariant()
            assert a.to_list() == model
