# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stack-allocation/. The authors are listed in prov/2NC7TG.jsonl.

import random

import pytest

from stack_allocation import StackAllocator, StackOrderError


def test_worked_example() -> None:
    s = StackAllocator(0, 100)
    assert s.enter(16) == 0  # frame of f
    assert s.alloca(10) == 16
    assert s.enter(24) == 26  # f calls g
    assert s.alloca(30) == 50
    with pytest.raises(StackOrderError):
        s.free(16)  # not the last block
    s.leave()  # g returns: frees 26 .. 79
    assert s.top == 26
    assert s.alloc(80) is None  # 26 + 80 > 100
    assert s.alloc(20) == 26
    s.free(26)
    s.leave()
    assert s.top == 0 and s.blocks == []


def test_errors() -> None:
    s = StackAllocator(0, 10)
    with pytest.raises(StackOrderError):
        s.alloca(1)
    with pytest.raises(StackOrderError):
        s.free(0)
    with pytest.raises(StackOrderError):
        s.release((5, 0))
    s.alloc(4)
    m = s.mark()
    s.free(0)
    s.alloc(6)
    with pytest.raises(StackOrderError):
        s.release(m)  # the block under the mark was freed


def test_random_against_model() -> None:
    rng = random.Random(1999)
    for _ in range(100):
        limit = rng.randrange(0, 300)
        s = StackAllocator(0, limit)
        model: list[tuple[int, int]] = []  # (start, size), a plain stack
        marks: list[tuple[tuple[int, int], int]] = []  # (mark, number of blocks)
        for _ in range(200):
            r = rng.random()
            if r < 0.45:
                n = rng.randrange(0, 40)
                p = s.alloc(n)
                top = model[-1][0] + model[-1][1] if model else 0
                if top + n > limit:
                    assert p is None
                else:
                    assert p == top
                    model.append((p, n))
            elif r < 0.75 and model:
                if rng.random() < 0.2 and len(model) > 1 and model[-2][0] != model[-1][0]:
                    with pytest.raises(StackOrderError):
                        s.free(model[-2][0])
                p, _ = model.pop()
                s.free(p)
            elif r < 0.9:
                marks.append((s.mark(), len(model)))
            elif marks:
                m, k = marks.pop()
                s.release(m)
                del model[k:]
            # a mark dies when a block below it is freed
            while marks and marks[-1][1] > len(model):
                marks.pop()
            # the live blocks are disjoint and packed from the base
            top = 0
            for p, n in model:
                assert p == top
                top += n
            assert s.top == top and s.blocks == [p for p, _ in model]
