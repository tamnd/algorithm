# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/calendar-queue/. The authors are listed in prov/CZJZK8.jsonl.

import heapq
import random

import pytest

from calendar_queue import CalendarQueue


def test_example() -> None:
    q: CalendarQueue[str] = CalendarQueue(4, 1.0, resize=False)
    for e, t in [("a", 0.3), ("b", 2.6), ("c", 1.2), ("d", 5.1), ("e", 3.9), ("f", 2.2)]:
        q.insert(e, t)
    assert [[x[0] for x in b] for b in q.buckets] == [[0.3], [1.2, 5.1], [2.2, 2.6], [3.9]]
    q.check_invariant()
    out = [q.extract_min() for _ in range(5)]
    assert out == [("a", 0.3), ("c", 1.2), ("f", 2.2), ("b", 2.6), ("e", 3.9)]
    assert q.v == 3
    q.insert("g", 40.0)
    assert q.extract_min() == ("d", 5.1)
    assert q.v == 5
    assert q.extract_min() == ("g", 40.0)
    assert q.v == 40
    q.check_invariant()


def test_edges() -> None:
    with pytest.raises(ValueError):
        CalendarQueue(0)
    with pytest.raises(ValueError):
        CalendarQueue(2, 0.0)
    q: CalendarQueue[int] = CalendarQueue()
    with pytest.raises(IndexError):
        q.extract_min()
    with pytest.raises(IndexError):
        q.peek_min()
    q.insert(1, -3.5)
    q.insert(2, -3.5)
    assert q.peek_min() == (1, -3.5)
    assert q.extract_min() == (1, -3.5)
    assert q.extract_min() == (2, -3.5)
    assert len(q) == 0


def test_insert_in_the_past() -> None:
    q: CalendarQueue[int] = CalendarQueue(4, 1.0, resize=False)
    q.insert(0, 10.0)
    assert q.extract_min() == (0, 10.0)
    q.insert(1, 12.0)
    q.insert(2, 3.0)
    q.check_invariant()
    assert q.extract_min() == (2, 3.0)
    assert q.extract_min() == (1, 12.0)


def test_hold_model_resizes() -> None:
    rng = random.Random(8)
    q: CalendarQueue[int] = CalendarQueue()
    ref: list[tuple[float, int]] = []
    for i in range(300):
        t = rng.expovariate(1.0)
        q.insert(i, t)
        heapq.heappush(ref, (t, i))
    assert q.resizes > 0
    for i in range(300, 3000):
        e, t = q.extract_min()
        assert (t, e) == heapq.heappop(ref)
        t2 = t + rng.expovariate(1.0)
        q.insert(i, t2)
        heapq.heappush(ref, (t2, i))
    q.check_invariant()
    while ref:
        e, t = q.extract_min()
        assert (t, e) == heapq.heappop(ref)
    assert len(q) == 0


def test_random_against_model() -> None:
    rng = random.Random(4)
    for _ in range(500):
        q: CalendarQueue[int] = CalendarQueue(rng.randrange(1, 5), rng.choice([0.5, 1.0, 3.0]), resize=rng.random() < 0.7)
        ref: list[tuple[float, int]] = []
        nxt = 0
        for _ in range(rng.randrange(1, 60)):
            if rng.random() < 0.55 or not ref:
                t = rng.choice([rng.uniform(-5, 50), float(rng.randrange(10))])
                q.insert(nxt, t)
                heapq.heappush(ref, (t, nxt))
                nxt += 1
            else:
                e, t = q.extract_min()
                assert (t, e) == heapq.heappop(ref)
            q.check_invariant()
            assert len(q) == len(ref)
