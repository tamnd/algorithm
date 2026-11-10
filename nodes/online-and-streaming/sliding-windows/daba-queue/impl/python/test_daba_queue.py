# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/daba-queue/. The authors are listed in prov/JMSPSC.jsonl.

import random
from collections import deque
from functools import reduce
from typing import Any, Callable

import pytest

from daba_queue import DabaQueue


def concat(a: str, b: str) -> str:
    return a + b


def maxcount(a: tuple[float, int], b: tuple[float, int]) -> tuple[float, int]:
    if a[0] > b[0]:
        return a
    if b[0] > a[0]:
        return b
    return (a[0], a[1] + b[1])


MONOIDS: list[tuple[str, Callable[[Any, Any], Any], Any, Callable[[random.Random], Any]]] = [
    ("sum", lambda a, b: a + b, 0, lambda r: r.randint(-50, 50)),
    ("max", max, float("-inf"), lambda r: r.randint(-50, 50)),
    ("concat", concat, "", lambda r: r.choice("abcde")),
    ("maxcount", maxcount, (float("-inf"), 0), lambda r: (r.randint(0, 4), 1)),
]


class Counter:
    def __init__(self, op: Callable[[Any, Any], Any]) -> None:
        self.op = op
        self.calls = 0

    def __call__(self, a: Any, b: Any) -> Any:
        self.calls += 1
        return self.op(a, b)


def brute(op: Callable[[Any, Any], Any], e: Any, window: deque) -> Any:
    return reduce(op, window, e)


def checked(q: DabaQueue, cnt: Counter) -> None:
    saved = cnt.calls
    q.check_invariant()
    cnt.calls = saved  # the check itself is not counted


def test_page_example() -> None:
    cnt = Counter(concat)
    q = DabaQueue(cnt, "")
    rows = []
    for op in ["ia", "ib", "ic", "id", "ie", "e", "e", "if"]:
        before = cnt.calls
        if op[0] == "i":
            q.insert(op[1])
        else:
            q.evict()
        f = q.F
        rows.append(([p - f for p in (q.F, q.L, q.R, q.A, q.B, q.E)], [q.agg[i] for i in range(q.F, q.E)], cnt.calls - before))
    assert rows == [
        ([0, 1, 1, 1, 1, 1], ["a"], 1),
        ([0, 1, 1, 1, 2, 2], ["ab", "b"], 4),
        ([0, 2, 2, 2, 2, 3], ["ab", "b", "c"], 1),
        ([0, 1, 2, 3, 4, 4], ["abcd", "b", "c", "d"], 4),
        ([0, 2, 2, 2, 4, 5], ["abcd", "bcd", "cd", "d", "e"], 4),
        ([0, 2, 2, 2, 3, 4], ["bcd", "cd", "d", "e"], 0),
        ([0, 2, 2, 2, 2, 3], ["cd", "d", "e"], 0),
        ([0, 1, 2, 3, 4, 4], ["cdef", "d", "e", "f"], 4),
    ]
    assert q.query() == "cdef"


def test_paper_trace() -> None:
    # Fig. 5 of Tangwongsan, Hirzel and Schneider (arXiv 2009.13768), maxcount.
    q = DabaQueue(maxcount, (float("-inf"), 0))
    seq = "i4 i5 i3 i4 i0 i4 i4 e e i2 i6 i5 i6 i1 i6 i5 e e".split()
    snap = {}
    for k, op in enumerate(seq):
        if op[0] == "i":
            q.insert((int(op[1]), 1))
        else:
            q.evict()
        q.check_invariant()
        snap[k] = [q.agg[i] for i in range(q.F, q.E)]
    assert snap[7] == [(5, 1), (4, 1), (4, 1), (0, 1), (4, 1), (4, 1)]
    assert snap[13] == [(6, 2), (4, 3), (4, 2), (4, 2), (4, 1), (2, 1), (6, 1), (6, 1), (6, 2), (1, 1)]
    assert snap[15] == [(6, 2), (6, 2), (6, 2), (4, 2), (4, 1), (2, 1), (6, 1), (6, 1), (6, 1), (1, 1), (6, 1), (6, 1)]
    assert snap[17] == [(6, 2), (6, 2), (6, 2), (6, 2), (6, 2), (6, 1), (6, 1), (1, 1), (6, 1), (6, 1)]
    assert q.query() == (6, 3)


@pytest.mark.parametrize("name,op,e,gen", MONOIDS)
def test_random_streams_and_operator_counts(name: str, op: Callable, e: Any, gen: Callable) -> None:
    rng = random.Random(4242)
    worst_insert = worst_evict = 0
    for case in range(200):
        cnt = Counter(op)
        q = DabaQueue(cnt, e)
        ref: deque = deque()
        p = rng.choice([0.3, 0.5, 0.6, 0.8])
        for _ in range(rng.randint(1, 70)):
            if rng.random() < p or not ref:
                v = gen(rng)
                before = cnt.calls
                q.insert(v)
                d = cnt.calls - before
                assert d <= 4
                worst_insert = max(worst_insert, d)
                ref.append(v)
            else:
                before = cnt.calls
                assert q.evict() == ref.popleft()
                d = cnt.calls - before
                assert d <= 3
                worst_evict = max(worst_evict, d)
            before = cnt.calls
            assert q.query() == brute(op, e, ref), name
            assert cnt.calls - before == 1
            assert q.items() == list(ref)
            checked(q, cnt)
    # the bounds of 4 and 3 calls are reached
    assert worst_insert == 4 and worst_evict == 3


@pytest.mark.parametrize("name,op,e,gen", MONOIDS)
def test_count_window(name: str, op: Callable, e: Any, gen: Callable) -> None:
    rng = random.Random(99)
    for w in range(1, 14):
        cnt = Counter(op)
        q = DabaQueue(cnt, e)
        ref: deque = deque()
        for _ in range(100):
            v = gen(rng)
            q.insert(v)
            ref.append(v)
            if len(ref) > w:
                assert q.evict() == ref.popleft()
            assert q.query() == brute(op, e, ref)
        checked(q, cnt)


def test_adversarial_grow_then_drain() -> None:
    # Long runs of inserts, then of evicts, the pattern that makes Two-Stacks flip a whole stack.
    for n in [1, 2, 3, 17, 64]:
        cnt = Counter(lambda a, b: a + b)
        q = DabaQueue(cnt, 0)
        for i in range(n):
            before = cnt.calls
            q.insert(i)
            assert cnt.calls - before <= 4
            q.check_invariant()
        for i in range(n):
            before = cnt.calls
            assert q.evict() == i
            assert cnt.calls - before <= 3
            assert q.query() == sum(range(i + 1, n))
        assert len(q) == 0 and q.query() == 0


def test_evict_empty() -> None:
    q = DabaQueue(max, float("-inf"))
    with pytest.raises(IndexError):
        q.evict()
