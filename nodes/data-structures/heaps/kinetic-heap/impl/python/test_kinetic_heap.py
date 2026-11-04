# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kinetic-heap/. The authors are listed in prov/NF6DCE.jsonl.

import random
from fractions import Fraction

import pytest

from kinetic_heap import KineticHeap


def depth_sum(n: int) -> int:
    return sum((i + 1).bit_length() - 1 for i in range(n))


def test_page_example() -> None:
    h = KineticHeap(now=0)
    lines = {"A": (0, 3), "B": (1, 1), "C": (2, 0), "D": (5, -1), "E": (4, -2)}
    for e, (a, b) in lines.items():
        h.insert(e, a, b)
    assert h.heap == ["A", "B", "C", "D", "E"]
    assert {i: h.cert[i][0] for i in h.cert} == {
        1: Fraction(1, 2), 2: Fraction(2, 3), 3: Fraction(2), 4: Fraction(1)}
    trace = []
    while True:
        nxt = h._next()
        if nxt is None:
            break
        h.advance(nxt[0])
        h.check_invariant()
        trace.append((nxt[0], "".join(map(str, h.heap)), h.find_min()))
    assert trace == [
        (Fraction(1, 2), "BACDE", "B"),
        (Fraction(4, 5), "BECDA", "B"),
        (Fraction(1), "ECBDA", "E"),
        (Fraction(3), "EDBCA", "E"),
    ]
    assert h.events == 5 < 6 == depth_sum(5)
    h.advance(100)
    assert h.events == 5 and h.find_min() == "E"


def test_tangent_lines_meet_the_bound() -> None:
    for n in [1, 2, 7, 15, 40]:
        h = KineticHeap(now=-10**6)
        for s in range(n):
            h.insert(s, s * s, -2 * s)
        h.advance(10**6)
        assert h.events == depth_sum(n)
        h.check_invariant()


def test_parallel_and_equal_lines() -> None:
    h = KineticHeap()
    for e in range(10):
        h.insert(e, 3, 1)
    h.advance(50)
    assert h.events == 0 and h.value(h.find_min()) == 53
    h.insert("x", 60, -1)
    h.advance(Fraction(103, 2))
    h.check_invariant()
    assert h.find_min() == "x" and h.value("x") == Fraction(17, 2) and h.events == 0


def test_errors() -> None:
    h = KineticHeap()
    with pytest.raises(IndexError):
        h.find_min()
    h.insert(1, 0, 0)
    with pytest.raises(KeyError):
        h.insert(1, 0, 0)
    h.advance(3)
    with pytest.raises(ValueError):
        h.advance(2)
    assert h.delete_min() == 1 and len(h) == 0


def test_random_against_brute_force() -> None:
    rng = random.Random(1999)
    for case in range(600):
        h = KineticHeap(now=rng.randint(-5, 5))
        alive: dict[int, tuple[int, int]] = {}
        nxt = 0
        for _ in range(rng.randint(1, 60)):
            op = rng.random()
            if op < 0.4 or not alive:
                a, b = rng.randint(-20, 20), rng.randint(-4, 4)
                h.insert(nxt, a + b * h.now, b)
                alive[nxt] = (a, b)
                nxt += 1
            elif op < 0.55:
                e = rng.choice(list(alive))
                h.delete(e)
                del alive[e]
            elif op < 0.65:
                m = min(h.value(x) for x in h.heap)
                e = h.find_min()
                assert h.value(e) == m and h.delete_min() == e
                del alive[e]
            else:
                start = h.events
                bound = sum(
                    1
                    for i in range(1, len(h.heap))
                    for j in _ancestors(i)
                    if h.line[h.heap[i]][1] < h.line[h.heap[j]][1]
                )
                h.advance(h.now + Fraction(rng.randint(0, 12), rng.randint(1, 3)))
                assert h.events - start <= bound
            if h.heap:
                m = min(h.value(x) for x in h.heap)
                assert h.value(h.find_min()) == m
            if case % 4 == 0:
                h.check_invariant()
        h.check_invariant()


def _ancestors(i: int) -> list[int]:
    out = []
    while i > 0:
        i = (i - 1) // 2
        out.append(i)
    return out
