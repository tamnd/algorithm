# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-stacks-queue/. The authors are listed in prov/69X9SB.jsonl.

import random
from collections import deque
from functools import reduce
from typing import Any, Callable

import pytest

from two_stacks_queue import TwoStacksQueue


def concat(a: str, b: str) -> str:
    return a + b


MONOIDS: list[tuple[str, Callable[[Any, Any], Any], Any, Callable[[random.Random], Any]]] = [
    ("sum", lambda a, b: a + b, 0, lambda r: r.randint(-50, 50)),
    ("max", max, float("-inf"), lambda r: r.randint(-50, 50)),
    ("concat", concat, "", lambda r: r.choice("abcde")),
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


def run_stream(rng: random.Random, name: str, op: Callable, e: Any, gen: Callable, steps: int, p_insert: float) -> None:
    cnt = Counter(op)
    q = TwoStacksQueue(cnt, e)
    ref: deque = deque()
    inserts = queries = 0
    for _ in range(steps):
        r = rng.random()
        if r < p_insert or not ref:
            v = gen(rng)
            before = cnt.calls
            q.insert(v)
            assert cnt.calls - before == 1
            ref.append(v)
            inserts += 1
        else:
            size = len(ref)
            before = cnt.calls
            assert q.evict() == ref.popleft()
            assert cnt.calls - before <= size
        before = cnt.calls
        assert q.query() == brute(op, e, ref), name
        assert cnt.calls - before == 1
        queries += 1
        assert q.items() == list(ref)
        saved = cnt.calls
        q.check_invariant()
        cnt.calls = saved  # the check itself is not counted
    # amortized bound: at most 2 calls per insert and 1 per query in total
    assert cnt.calls <= 2 * inserts + queries


def test_page_example() -> None:
    q = TwoStacksQueue(concat, "")
    for c in "abc":
        q.insert(c)
    assert q.query() == "abc"
    assert q.evict() == "a"
    assert q.front == [("c", "c"), ("b", "bc")]
    q.insert("d")
    assert q.back == ["d"] and q.back_agg == "d"
    assert q.query() == "bcd"
    assert q.evict() == "b"
    assert q.evict() == "c"
    assert q.query() == "d"


@pytest.mark.parametrize("name,op,e,gen", MONOIDS)
def test_random_streams(name: str, op: Callable, e: Any, gen: Callable) -> None:
    rng = random.Random(20260)
    for case in range(250):
        p = rng.choice([0.3, 0.5, 0.6, 0.8])
        run_stream(rng, name, op, e, gen, rng.randint(1, 60), p)


@pytest.mark.parametrize("name,op,e,gen", MONOIDS)
def test_fixed_count_window(name: str, op: Callable, e: Any, gen: Callable) -> None:
    rng = random.Random(7)
    for w in range(1, 12):
        q = TwoStacksQueue(op, e)
        ref: deque = deque()
        for _ in range(80):
            v = gen(rng)
            q.insert(v)
            ref.append(v)
            if len(ref) > w:
                assert q.evict() == ref.popleft()
            assert q.query() == brute(op, e, ref)


def test_worst_case_evict_is_linear() -> None:
    for n in [1, 5, 40]:
        cnt = Counter(lambda a, b: a + b)
        q = TwoStacksQueue(cnt, 0)
        for i in range(n):
            q.insert(i)
        before = cnt.calls
        assert q.evict() == 0
        assert cnt.calls - before == n
        before = cnt.calls
        for i in range(1, n):
            assert q.evict() == i
        assert cnt.calls == before


def test_evict_empty() -> None:
    q = TwoStacksQueue(max, float("-inf"))
    assert q.query() == float("-inf")
    with pytest.raises(IndexError):
        q.evict()
