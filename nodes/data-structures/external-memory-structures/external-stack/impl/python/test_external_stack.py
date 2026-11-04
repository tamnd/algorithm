# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/external-stack/. The authors are listed in prov/A69Z23.jsonl.

import random

import pytest

from external_stack import ExternalStack


def test_example() -> None:
    s: ExternalStack[int] = ExternalStack(2)
    for x in range(1, 8):
        s.push(x)
        s.check_invariant()
    assert s.disk == [[1, 2], [3, 4]] and s.buf == [5, 6, 7]
    assert (s.reads, s.writes) == (0, 2)
    assert [s.pop() for _ in range(3)] == [7, 6, 5]
    assert s.reads == 0
    assert s.pop() == 4
    assert s.reads == 1 and s.buf == [3] and s.disk == [[1, 2]]
    s.push(8)
    assert s.top() == 8 and len(s) == 4
    assert [s.pop() for _ in range(4)] == [8, 3, 2, 1]
    assert (s.reads, s.writes) == (2, 2)
    s.check_invariant()


def test_edges() -> None:
    with pytest.raises(ValueError):
        ExternalStack(0)
    s: ExternalStack[str] = ExternalStack(1)
    with pytest.raises(IndexError):
        s.pop()
    s.push("a")
    assert s.pop() == "a" and len(s) == 0
    with pytest.raises(IndexError):
        s.top()


def test_no_thrashing() -> None:
    B = 8
    s: ExternalStack[int] = ExternalStack(B)
    for x in range(2 * B):
        s.push(x)
    before = s.reads + s.writes
    for _ in range(1000):
        s.push(0)
        s.pop()
        s.pop()
        s.push(0)
    assert s.reads + s.writes - before <= 1


def test_against_list() -> None:
    rng = random.Random(5)
    for _ in range(500):
        B = rng.randrange(1, 6)
        s: ExternalStack[int] = ExternalStack(B)
        model: list[int] = []
        n = rng.randrange(1, 200)
        p = rng.random()
        for _ in range(n):
            if model and rng.random() < p:
                assert s.pop() == model.pop()
            else:
                x = rng.randrange(1000)
                s.push(x)
                model.append(x)
            s.check_invariant()
            assert s.items() == model and len(s) == len(model)
        assert s.reads + s.writes <= n // B
