# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-array/. The authors are listed in prov/9C8NGV.jsonl.

import random

import pytest

from dynamic_array import DynamicArray


def phi(n: int, cap: int) -> float:
    return 2 * n - cap if 2 * n >= cap else cap / 2 - n


def test_page_example() -> None:
    d: DynamicArray[int] = DynamicArray()
    rows = []
    for x in [1, 2, 3, 4, 5]:
        c0 = d.copies
        d.append(x)
        rows.append((d.n, d.cap, d.copies - c0))
    for want in [5, 4, 3, 2, 1]:
        c0 = d.copies
        assert d.pop() == want
        rows.append((d.n, d.cap, d.copies - c0))
    assert rows == [
        (1, 1, 0), (2, 2, 1), (3, 4, 2), (4, 4, 0), (5, 8, 4),
        (4, 8, 0), (3, 8, 0), (2, 4, 2), (1, 2, 1), (0, 2, 0),
    ]
    assert d.copies == 10


def test_edges() -> None:
    d: DynamicArray[int] = DynamicArray()
    with pytest.raises(IndexError):
        d.pop()
    with pytest.raises(IndexError):
        d.get(0)
    d.append(7)
    d.set(0, 8)
    assert d.get(0) == 8 and d.cap == 1
    assert d.pop() == 8 and d.cap == 1


def test_no_thrashing_at_boundary() -> None:
    d: DynamicArray[int] = DynamicArray()
    for x in range(64):
        d.append(x)
    assert d.cap == 64
    c0 = d.copies
    for _ in range(100):
        d.append(0)
        d.pop()
    assert d.copies - c0 == 64  # only the first append resizes


def test_amortized_bound() -> None:
    rng = random.Random(77)
    d: DynamicArray[int] = DynamicArray()
    total = 0
    m = 0
    for _ in range(5000):
        before = phi(d.n, d.cap)
        c0 = d.copies
        if d.n and rng.random() < 0.45:
            d.pop()
            bound = 2
        else:
            d.append(1)
            bound = 3
        cost = 1 + d.copies - c0
        assert cost + phi(d.n, d.cap) - before <= bound
        total += cost
        m += 1
    assert total <= 3 * m + 0.5


def test_random_against_list() -> None:
    rng = random.Random(9821)
    for _ in range(500):
        d: DynamicArray[int] = DynamicArray()
        model: list[int] = []
        for _ in range(60):
            op = rng.randrange(3)
            if op == 0:
                x = rng.randint(0, 9)
                d.append(x)
                model.append(x)
            elif op == 1 and model:
                assert d.pop() == model.pop()
            elif model:
                i = rng.randrange(len(model))
                assert d.get(i) == model[i]
            d.check_invariant()
            assert list(d) == model
