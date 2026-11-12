# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mark-compact/. The authors are listed in prov/H0T260.jsonl.

import random

from mark_compact import Heap


def reachable(objs: dict[int, list[int | None]], roots: list[int | None]) -> set[int]:
    """Oracle: breadth-first search from the roots."""
    seen = {r for r in roots if r is not None}
    queue = list(seen)
    i = 0
    while i < len(queue):
        for y in objs[queue[i]]:
            if y is not None and y not in seen:
                seen.add(y)
                queue.append(y)
        i += 1
    return seen


def check(h: Heap) -> dict[int, int]:
    """Collect h and compare with the state before. Return the map old -> new."""
    old = {a: h.fields(a) for a in h.objects()}
    old_roots = list(h.roots)
    live = sorted(reachable(old, old_roots))
    top = h.collect()
    expected, a = {}, 0
    for x in live:
        expected[x] = a
        a += 1 + len(old[x])
    assert top == a == h.top
    assert h.objects() == [expected[x] for x in live]
    assert h.roots == [None if r is None else expected[r] for r in old_roots]
    for x in live:
        assert h.fields(expected[x]) == [None if y is None else expected[y] for y in old[x]]
    assert not any(h.marked)
    assert all(w is None for w in h.mem[top:])
    return expected


def build(objs: list[list[int | None]], roots: list[int | None], slack: int = 0) -> Heap:
    """Lay the objects out in order; field and root values are object indexes."""
    addr, a = [], 0
    for f in objs:
        addr.append(a)
        a += 1 + len(f)
    h = Heap(a + slack)
    for f in objs:
        h.allocate([None if y is None else addr[y] for y in f])
    h.roots = [None if r is None else addr[r] for r in roots]
    return h


def test_example() -> None:
    # P at 0, Q at 2, R at 3, S at 6, T at 8; the roots are S and P.
    h = build([[3], [], [0, 4], [4], [2]], [3, 0])
    assert h.objects() == [0, 2, 3, 6, 8]
    assert check(h) == {0: 0, 3: 2, 6: 5, 8: 7}
    assert h.mem[:9] == [2, 5, 3, 0, 7, 2, 7, 2, 2]
    assert h.roots == [5, 0]


def test_edges() -> None:
    check(Heap(0))
    check(build([[None]], []))
    check(build([[0]], [0]))
    check(build([[], [None, None], []], [2, 2, None]))


def test_random_heaps() -> None:
    rng = random.Random(1978)
    for _ in range(700):
        m = rng.randint(1, 25)
        objs = [[rng.choice([None, rng.randrange(m)]) for _ in range(rng.randint(0, 4))] for _ in range(m)]
        roots = [rng.choice([None, rng.randrange(m)]) for _ in range(rng.randint(0, 4))]
        check(build(objs, roots, rng.randint(0, 5)))


def test_mutator_with_allocation() -> None:
    """A mutator that allocates and drops objects; the heap collects itself when full."""
    rng = random.Random(3)
    for _ in range(60):
        h = Heap(rng.randint(30, 90))
        for _ in range(200):
            reach = sorted(reachable({a: h.fields(a) for a in h.objects()}, h.roots))
            fields = [rng.choice([None] + reach) for _ in range(rng.randint(0, 3))]
            try:
                a = h.allocate(fields)
            except MemoryError:
                h.roots = h.roots[1:]
                continue
            # allocate() may have collected: the field values must have been updated too.
            assert all(y is None or y in h.objects() for y in h.fields(a))
            if len(h.roots) < 4:
                h.roots.append(a)
            else:
                h.roots[rng.randrange(4)] = a
            if rng.random() < 0.15:
                check(h)
