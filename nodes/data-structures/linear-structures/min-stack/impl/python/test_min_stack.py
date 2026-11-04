# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/min-stack/. The authors are listed in prov/PR4H8X.jsonl.

import random

import pytest

from min_stack import LeanMinStack, MinStack


def test_page_example() -> None:
    s: MinStack[int] = MinStack()
    mins = []
    for x in [5, 3, 7, 3, 2]:
        s.push(x)
        mins.append(s.min())
    assert mins == [5, 3, 3, 3, 2]
    assert s.s == [(5, 5), (3, 3), (7, 3), (3, 3), (2, 2)]
    out = []
    for _ in range(4):
        out.append((s.pop(), s.min()))
    assert out == [(2, 3), (3, 3), (7, 3), (3, 5)]
    assert s.top() == 5


def test_edges() -> None:
    s: MinStack[int] = MinStack()
    for f in (s.pop, s.top, s.min):
        with pytest.raises(IndexError):
            f()
    s.push(4)
    s.push(4)
    s.pop()
    assert s.min() == 4  # a duplicate of the minimum
    s.push(-(2**63))
    s.push(2**63 - 1)
    assert s.min() == -(2**63)


def test_lean_variant_with_duplicates() -> None:
    s: LeanMinStack[int] = LeanMinStack()
    for x in [2, 1, 1]:
        s.push(x)
    s.pop()
    assert s.min() == 1  # with < instead of <= this would be 2


def test_random_against_model() -> None:
    rng = random.Random(155)
    for _ in range(500):
        s: MinStack[int] = MinStack()
        t: LeanMinStack[int] = LeanMinStack()
        model: list[int] = []
        for _ in range(50):
            if model and rng.random() < 0.45:
                want = model.pop()
                assert s.pop() == want
                assert t.pop() == want
            else:
                x = rng.randint(0, 6)
                s.push(x)
                t.push(x)
                model.append(x)
            s.check_invariant()
            if model:
                assert s.min() == min(model) == t.min()
                assert s.top() == model[-1]
            assert len(s) == len(model)
