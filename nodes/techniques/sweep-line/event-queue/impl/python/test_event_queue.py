# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/event-queue/. The authors are listed in prov/324RJK.jsonl.

import random

import pytest

from event_queue import EventQueue


def test_example() -> None:
    # Segments a: (0,0)-(10,10), b: (0,10)-(10,0), c: (1,5)-(3,5), as on the page.
    q: EventQueue[tuple[int, int], str] = EventQueue()
    q.insert((0, 0), "a")
    q.insert((0, 10), "b")
    q.insert((1, 5), "c")
    q.insert((10, 10))
    q.insert((10, 0))
    q.insert((3, 5))
    q.check_invariant()
    assert len(q) == 6
    assert q.pop_min() == ((0, 0), ["a"])
    assert q.pop_min() == ((0, 10), ["b"])
    q.insert((5, 5))  # a and b are neighbors and cross at (5, 5)
    assert len(q) == 5
    assert q.pop_min() == ((1, 5), ["c"])
    assert q.pop_min() == ((3, 5), [])
    assert q.contains((5, 5))
    q.insert((5, 5))  # a and b are neighbors again: the same event
    assert len(q) == 3
    q.check_invariant()
    popped = []
    while not q.is_empty():
        popped.append(q.pop_min())
    assert popped == [((5, 5), []), ((10, 0), []), ((10, 10), [])]


def test_merge_payloads() -> None:
    q: EventQueue[tuple[int, int], str] = EventQueue()
    q.insert((4, 4), "s1 ends")
    q.insert((2, 9), "x")
    q.insert((4, 4), "s3 starts")
    q.insert((4, 4))
    assert len(q) == 2
    assert q.pop_min() == ((2, 9), ["x"])
    assert q.pop_min() == ((4, 4), ["s1 ends", "s3 starts"])
    assert q.is_empty()


def test_empty_and_one() -> None:
    q: EventQueue[tuple[int, int], int] = EventQueue()
    assert q.is_empty() and len(q) == 0
    assert not q.contains((0, 0))
    with pytest.raises(IndexError):
        q.pop_min()
    q.insert((-(2**63), 2**63 - 1), 7)
    q.check_invariant()
    assert q.pop_min() == ((-(2**63), 2**63 - 1), [7])
    assert q.is_empty()


def test_lexicographic_order() -> None:
    q: EventQueue[tuple[int, int], int] = EventQueue()
    for p in [(1, 5), (1, -3), (0, 100), (1, 0)]:
        q.insert(p, 0)
    assert [q.pop_min()[0] for _ in range(4)] == [(0, 100), (1, -3), (1, 0), (1, 5)]


def test_random_against_model() -> None:
    rng = random.Random(324)
    for _ in range(600):
        q: EventQueue[tuple[int, int], int] = EventQueue()
        model: dict[tuple[int, int], list[int]] = {}
        for step in range(rng.randrange(1, 60)):
            op = rng.random()
            if op < 0.6:
                p = (rng.randrange(5), rng.randrange(5))
                a = rng.choice([None, step])
                q.insert(p, a)
                model.setdefault(p, [])
                if a is not None:
                    model[p].append(a)
            elif model:
                p = min(model)
                assert q.pop_min() == (p, model.pop(p))
            else:
                assert q.is_empty()
            q.check_invariant()
            assert len(q) == len(model)
            assert q.is_empty() == (not model)
            probe = (rng.randrange(5), rng.randrange(5))
            assert q.contains(probe) == (probe in model)
