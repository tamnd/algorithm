# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lisp2-compaction/. The authors are listed in prov/ANR9PV.jsonl.

import random

from lisp2_compaction import HEADER, Heap


def snapshot(h: Heap) -> dict[int, list[int | None]]:
    """The fields of every object, by address."""
    return {a: h.fields(a) for a in h.objects()}


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
    """Collect h and check the result against the state before. Return the map old -> new."""
    old = snapshot(h)
    old_roots = list(h.roots)
    live = sorted(reachable(old, old_roots))
    top = h.collect()

    # The live objects keep their order and are packed from address 0.
    expected, a = {}, 0
    for x in live:
        expected[x] = a
        a += HEADER + len(old[x])
    assert top == a == h.top
    assert h.objects() == [expected[x] for x in live]

    # Every root and every field is updated: the graphs are isomorphic under expected.
    assert h.roots == [None if r is None else expected[r] for r in old_roots]
    for x in live:
        assert h.fields(expected[x]) == [None if y is None else expected[y] for y in old[x]]

    # Nothing is left behind: no marks, and the free area is clear.
    assert not any(h.marked)
    assert all(w is None for w in h.mem[top:])
    return expected


def build(objs: list[list[int | None]], roots: list[int | None], slack: int = 0) -> Heap:
    """Lay the objects out in order; field and root values are object indexes."""
    addr, a = [], 0
    for f in objs:
        addr.append(a)
        a += HEADER + len(f)
    h = Heap(a + slack)
    for f in objs:
        h.allocate([None if y is None else addr[y] for y in f])
    h.roots = [None if r is None else addr[r] for r in roots]
    return h


def test_example() -> None:
    # A at 0, B at 3, C at 5, D at 9, E at 12; the root is A.
    h = build([[2], [], [0, 4], [2], [None]], [0])
    assert h.objects() == [0, 3, 5, 9, 12]
    fwd = check(h)
    assert fwd == {0: 0, 5: 3, 12: 7}
    assert h.mem == [3, 0, 3, 4, 3, 0, 7, 3, 7, None, None, None, None, None, None]
    assert h.roots == [0]


def test_edges() -> None:
    check(Heap(0))
    check(build([[None]], []))
    check(build([[0]], [0]))
    check(build([[], [None, None], []], [2, 2, None]))
    h = build([[1], [0]], [1])
    assert check(h) == {0: 0, 3: 3}


def test_random_heaps() -> None:
    rng = random.Random(1966)
    for _ in range(700):
        m = rng.randint(1, 25)
        objs = [[rng.choice([None, rng.randrange(m)]) for _ in range(rng.randint(0, 4))] for _ in range(m)]
        roots = [rng.choice([None, rng.randrange(m)]) for _ in range(rng.randint(0, 4))]
        check(build(objs, roots, rng.randint(0, 5)))


def test_mutator_cycles() -> None:
    """Allocate until the heap is full, collect, and go on; the roots change all the time."""
    rng = random.Random(2)
    for _ in range(60):
        h = Heap(rng.randint(20, 80))
        for _ in range(150):
            known = h.objects()
            fields = [rng.choice([None] + known) if known else None for _ in range(rng.randint(0, 3))]
            try:
                a = h.allocate(fields)
            except MemoryError:
                check(h)
                continue
            if len(h.roots) < 4:
                h.roots.append(a)
            else:
                h.roots[rng.randrange(4)] = a
            if rng.random() < 0.2:
                check(h)


def test_slide_is_safe_in_place() -> None:
    """A large live object right after a small garbage object overlaps its own old place."""
    h = build([[], [None] * 10], [1])
    assert check(h) == {2: 0}
