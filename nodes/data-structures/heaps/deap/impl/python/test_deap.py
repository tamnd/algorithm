# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deap/. The authors are listed in prov/5CWRB5.jsonl.

import random

import pytest

from deap import Deap


START = [5, 45, 10, 8, 25, 40, 15, 19, 9, 30, 20]


def test_example() -> None:
    d = Deap(START)
    assert d.keys() == START
    d.check_invariant()
    d.insert(4)
    assert d.keys() == [4, 45, 5, 8, 25, 40, 15, 10, 9, 30, 20, 19]
    d.insert(50)
    assert d.keys() == [4, 50, 5, 8, 25, 45, 15, 10, 9, 30, 20, 19, 40]
    assert d.extract_min() == 4
    assert d.keys() == [5, 50, 10, 8, 40, 45, 15, 19, 9, 30, 20, 25]
    assert d.extract_max() == 50
    assert d.keys() == [5, 45, 10, 8, 40, 30, 15, 19, 9, 25, 20]
    d.check_invariant()


def test_partners() -> None:
    assert [Deap.is_max_node(i) for i in range(2, 16)] == [
        False, True, False, False, True, True,
        False, False, False, False, True, True, True, True,
    ]
    assert Deap.min_partner(13) == 9
    assert Deap.min_partner(7) == 5
    d = Deap(range(12))
    assert d.n == 13
    assert d.max_partner(9) == 13
    assert d.max_partner(10) == 7
    assert d.max_partner(4) == 6


def test_edges() -> None:
    d: Deap[int] = Deap()
    for f in (d.find_min, d.find_max, d.extract_min, d.extract_max):
        with pytest.raises(IndexError):
            f()
    d.insert(3)
    assert (d.find_min(), d.find_max()) == (3, 3)
    assert d.extract_max() == 3
    d.insert(3)
    assert d.extract_min() == 3
    d = Deap([2, 7])
    assert d.extract_min() == 2
    assert d.find_max() == 7
    d = Deap([2, 7, 5])
    assert d.extract_max() == 7
    assert d.extract_max() == 5
    assert d.extract_min() == 2
    assert len(d) == 0


def test_random_against_model() -> None:
    rng = random.Random(77)
    for _ in range(600):
        d: Deap[int] = Deap()
        model: list[int] = []
        for _ in range(rng.randrange(1, 50)):
            op = rng.randrange(3)
            if op == 0 or not model:
                x = rng.randrange(25)
                d.insert(x)
                model.append(x)
            elif op == 1:
                m = min(model)
                model.remove(m)
                assert d.extract_min() == m
            else:
                m = max(model)
                model.remove(m)
                assert d.extract_max() == m
            d.check_invariant()
            assert sorted(d.keys()) == sorted(model)
            if model:
                assert d.find_min() == min(model)
                assert d.find_max() == max(model)
