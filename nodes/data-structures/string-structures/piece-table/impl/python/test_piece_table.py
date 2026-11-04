# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/piece-table/. The authors are listed in prov/A8HMV8.jsonl.

import random

import pytest

from piece_table import ADD, ORIGINAL, PieceTable


def test_example() -> None:
    t = PieceTable("the fox jumps")
    t.insert(4, "quick ")
    assert t.pieces == [(ORIGINAL, 0, 4), (ADD, 0, 6), (ORIGINAL, 4, 9)]
    t.insert(10, "brown ")
    assert t.pieces == [(ORIGINAL, 0, 4), (ADD, 0, 12), (ORIGINAL, 4, 9)]
    assert t.text() == "the quick brown fox jumps"
    t.delete(4, 6)
    assert t.pieces == [(ORIGINAL, 0, 4), (ADD, 6, 6), (ORIGINAL, 4, 9)]
    assert t.text() == "the brown fox jumps"
    t.delete(10, 4)
    assert t.pieces == [(ORIGINAL, 0, 4), (ADD, 6, 6), (ORIGINAL, 8, 5)]
    assert t.text() == "the brown jumps"
    assert "".join(t.add) == "quick brown "
    assert t.original == "the fox jumps"
    t.check_invariant()


def test_edges() -> None:
    t = PieceTable()
    assert t.text() == "" and len(t) == 0
    t.insert(0, "")
    t.insert(0, "abc")
    t.insert(3, "def")
    assert t.pieces == [(ADD, 0, 6)]
    t.insert(0, "x")
    t.delete(0, 7)
    assert t.text() == "" and t.pieces == []
    t.check_invariant()
    with pytest.raises(IndexError):
        t.insert(1, "a")
    with pytest.raises(IndexError):
        t.delete(0, 1)
    with pytest.raises(IndexError):
        t.char_at(0)


def test_random_against_string() -> None:
    rng = random.Random(4242)
    for _ in range(500):
        model = "".join(rng.choice("abc") for _ in range(rng.randint(0, 10)))
        t = PieceTable(model)
        for _ in range(rng.randint(0, 30)):
            if rng.random() < 0.55 or not model:
                i = rng.randint(0, len(model))
                s = "".join(rng.choice("xyz") for _ in range(rng.randint(0, 4)))
                t.insert(i, s)
                model = model[:i] + s + model[i:]
            else:
                i = rng.randint(0, len(model) - 1)
                d = rng.randint(0, len(model) - i)
                t.delete(i, d)
                model = model[:i] + model[i + d :]
            t.check_invariant()
        assert t.text() == model and len(t) == len(model)
        if model:
            i = rng.randrange(len(model))
            assert t.char_at(i) == model[i]
            j = rng.randint(i, len(model))
            assert t.substring(i, j) == model[i:j]
