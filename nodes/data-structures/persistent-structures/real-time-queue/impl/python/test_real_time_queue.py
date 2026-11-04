# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/real-time-queue/. The authors are listed in prov/X9W66J.jsonl.

import random

import pytest

import real_time_queue as rtq
from real_time_queue import RealTimeQueue


def _state(q):  # type: ignore[no-untyped-def]
    return (q._lenf, q._lenr, q._lens)


def test_example() -> None:
    q0: RealTimeQueue[int] = RealTimeQueue()
    q1 = q0.push(1)
    assert _state(q1) == (1, 0, 1)
    q2 = q1.push(2)
    assert _state(q2) == (1, 1, 0)
    q3 = q2.push(3)
    assert _state(q3) == (3, 0, 3)
    q4 = q3.push(4)
    assert _state(q4) == (3, 1, 2)
    q5 = q4.push(5)
    assert _state(q5) == (3, 2, 1)
    x, q6 = q5.pop()
    assert x == 1 and _state(q6) == (2, 2, 0)
    q7 = q6.push(6)
    assert _state(q7) == (5, 0, 5)
    assert list(q7) == [2, 3, 4, 5, 6]
    assert list(q5) == [1, 2, 3, 4, 5]
    assert list(q2) == [1, 2]
    for q in (q0, q1, q2, q3, q4, q5, q6, q7):
        q.check_invariant()


def test_edges() -> None:
    e: RealTimeQueue[str] = RealTimeQueue()
    assert e.is_empty() and len(e) == 0 and list(e) == []
    with pytest.raises(IndexError):
        e.pop()
    with pytest.raises(IndexError):
        e.front()
    one = e.push("a")
    assert one.front() == "a" and len(one) == 1
    x, back = one.pop()
    assert x == "a" and back.is_empty() and not one.is_empty()
    back.check_invariant()


def test_deep_and_worst_case_steps() -> None:
    q: RealTimeQueue[int] = RealTimeQueue()
    worst = 0
    for i in range(100000):
        before = rtq.STEPS
        q = q.push(i)
        worst = max(worst, rtq.STEPS - before)
    assert len(q) == 100000
    snapshot = q
    out = []
    for _ in range(50000):
        before = rtq.STEPS
        x, q = q.pop()
        worst = max(worst, rtq.STEPS - before)
        out.append(x)
    assert out == list(range(50000))
    # Reuse an old version many times: each pop is still O(1).
    for _ in range(1000):
        before = rtq.STEPS
        x, _ = snapshot.pop()
        worst = max(worst, rtq.STEPS - before)
        assert x == 0
    assert worst <= 3
    q.check_invariant()
    snapshot.check_invariant()


def test_random_version_tree() -> None:
    rng = random.Random(1999)
    for _ in range(500):
        versions = [RealTimeQueue()]
        model: "list[list[int]]" = [[]]
        for _ in range(rng.randint(1, 60)):
            v = rng.randrange(len(versions))
            if rng.random() < 0.6 or not model[v]:
                x = rng.randint(0, 99)
                versions.append(versions[v].push(x))
                model.append(model[v] + [x])
            else:
                x, q = versions[v].pop()
                assert x == model[v][0]
                versions.append(q)
                model.append(model[v][1:])
            versions[-1].check_invariant()
        for q, m in zip(versions, model):
            assert len(q) == len(m)
            assert list(q) == m
            if m:
                assert q.front() == m[0]
            q.check_invariant()
