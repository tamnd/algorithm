# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gap-buffer/. The authors are listed in prov/DCWD8D.jsonl.

import random

import pytest

from gap_buffer import GapBuffer


def test_page_example() -> None:
    B: GapBuffer[str] = GapBuffer(4)
    for c in "cat":
        B.insert(c)
    assert (B.g, B.e) == (3, 4)
    assert B.move_to(1) == 2 and (B.g, B.e) == (1, 2)
    B.insert("h")
    assert "".join(B) == "chat" and B.g == B.e == 2
    assert B.move_to(4) == 2
    B.insert("s")
    assert len(B.a) == 8 and (B.g, B.e) == (5, 8)
    B.insert("!")
    assert B.move_to(0) == 6 and (B.g, B.e) == (0, 2)
    assert B.delete_after() == "c"
    assert "".join(B) == "hats!" and B.get(4) == "!"
    B.check_invariant()


def test_edges() -> None:
    B: GapBuffer[int] = GapBuffer(0)
    assert len(B.a) == 1 and len(B) == 0
    with pytest.raises(IndexError):
        B.delete_before()
    with pytest.raises(IndexError):
        B.delete_after()
    with pytest.raises(IndexError):
        B.move_to(1)
    with pytest.raises(IndexError):
        B.get(0)
    B.insert(7)
    B.insert(8)
    assert list(B) == [7, 8]
    assert B.delete_before() == 8
    B.move_to(0)
    assert B.delete_after() == 7 and len(B) == 0
    B.check_invariant()


def test_random_against_list() -> None:
    rng = random.Random(1980)
    for _ in range(600):
        B: GapBuffer[int] = GapBuffer(rng.randrange(0, 4))
        model: list[int] = []
        cur = 0
        for _ in range(rng.randrange(1, 60)):
            op = rng.randrange(4)
            if op == 0:
                x = rng.randrange(100)
                B.insert(x); model.insert(cur, x); cur += 1
            elif op == 1:
                p = rng.randrange(len(model) + 1)
                assert B.move_to(p) == abs(p - cur)
                cur = p
            elif op == 2 and cur > 0:
                assert B.delete_before() == model.pop(cur - 1); cur -= 1
            elif op == 3 and cur < len(model):
                assert B.delete_after() == model.pop(cur)
            B.check_invariant()
            assert list(B) == model and B.cursor() == cur
