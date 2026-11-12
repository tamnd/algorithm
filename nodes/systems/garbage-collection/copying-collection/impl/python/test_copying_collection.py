# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/copying-collection/. The authors are listed in prov/D0R5KM.jsonl.

import random

from copying_collection import Heap


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
    live = reachable(old, old_roots)
    live_words = sum(1 + len(old[x]) for x in live)
    before = h.copied_words
    old_space = h.tospace
    h.collect()
    assert h.S == 0 or h.tospace != old_space
    lo, hi = h.tospace, h.tospace + h.S

    # The new graph is isomorphic to the live part of the old one.
    phi: dict[int, int] = {}
    work = []

    def match(a: int | None, b: int | None) -> None:
        assert (a is None) == (b is None)
        if a is None:
            return
        assert lo <= b < hi
        if a in phi:
            assert phi[a] == b
        else:
            phi[a] = b
            work.append(a)

    for a, b in zip(old_roots, h.roots, strict=True):
        match(a, b)
    while work:
        a = work.pop()
        assert h.mem[phi[a]] == 1 + len(old[a])
        for x, y in zip(old[a], h.fields(phi[a]), strict=True):
            match(x, y)

    # Exactly the live objects were copied, once each, and packed from the start of to-space.
    assert set(phi) == live
    assert sorted(phi.values()) == h.objects()
    assert h.free - lo == live_words == h.copied_words - before
    assert all(w is None for w in h.mem[h.free:hi])
    return phi


def build(objs: list[list[int | None]], roots: list[int | None], slack: int = 0) -> Heap:
    """Allocate the objects in order; field and root values are object indexes."""
    need = sum(1 + len(f) for f in objs)
    h = Heap(need + slack)
    addr: list[int] = []
    for f in objs:
        addr.append(h.free)
        h.free += 1 + len(f)
    for a, f in zip(addr, objs):
        h.mem[a] = 1 + len(f)
        h.mem[a + 1:a + 1 + len(f)] = [None if y is None else addr[y] for y in f]
    h.roots = [None if r is None else addr[r] for r in roots]
    return h


def test_example() -> None:
    # A at 0 -> (B, C); B at 3 -> (C); C at 5 -> (A); D at 7 -> (B). The root is A.
    h = build([[1, 2], [2], [0], [1]], [0])
    phi = check(h)
    # Depth-first order with a stack: A is copied first, then B and C when A is scanned.
    assert h.tospace == 9
    assert phi == {0: 9, 3: 12, 5: 14}
    assert h.mem[9:16] == [3, 12, 14, 2, 14, 2, 9]
    assert h.roots == [9]


def test_edges() -> None:
    check(Heap(0))
    check(build([[None]], []))
    check(build([[0]], [0]))
    check(build([[], [None, None], []], [2, 2, None]))
    h = build([[1], [0]], [0, 1])
    check(h)
    check(h)  # two flips bring to-space back to the first semispace
    assert h.tospace == 0


def test_random_heaps() -> None:
    rng = random.Random(1969)
    for _ in range(700):
        m = rng.randint(1, 25)
        objs = [[rng.choice([None, rng.randrange(m)]) for _ in range(rng.randint(0, 4))] for _ in range(m)]
        roots = [rng.choice([None, rng.randrange(m)]) for _ in range(rng.randint(0, 4))]
        h = build(objs, roots, rng.randint(0, 5))
        check(h)
        check(h)


def test_mutator_with_allocation() -> None:
    """Allocate until the semispace is full; allocate() collects and keeps the new fields live."""
    rng = random.Random(4)
    for _ in range(60):
        h = Heap(rng.randint(20, 60))
        for _ in range(200):
            reach = sorted(reachable({a: h.fields(a) for a in h.objects()}, h.roots))
            fields = [rng.choice([None] + reach) for _ in range(rng.randint(0, 3))]
            try:
                a = h.allocate(fields)
            except MemoryError:
                h.roots = h.roots[1:]
                continue
            assert h.tospace <= a < h.end
            assert all(y is None or y in h.objects() for y in h.fields(a))
            if len(h.roots) < 4:
                h.roots.append(a)
            else:
                h.roots[rng.randrange(4)] = a
            if rng.random() < 0.15:
                check(h)
