# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cheney-copying-collector/. The authors are listed in prov/CWN22Y.jsonl.

import random

from cheney_copying_collector import Heap


def bfs_order(objs: dict[int, list[int | None]], roots: list[int | None]) -> list[int]:
    """Oracle: the objects in the order a breadth-first search discovers them.

    The roots are taken in order, then the queue is first in, first out, and
    the fields of each object are taken in order.
    """
    seen: set[int] = set()
    order: list[int] = []
    for r in roots:
        if r is not None and r not in seen:
            seen.add(r)
            order.append(r)
    i = 0
    while i < len(order):
        for y in objs[order[i]]:
            if y is not None and y not in seen:
                seen.add(y)
                order.append(y)
        i += 1
    return order


def check(h: Heap) -> dict[int, int]:
    """Collect h and compare with the state before. Return the map old -> new."""
    old = {a: h.fields(a) for a in h.objects()}
    old_roots = list(h.roots)
    order = bfs_order(old, old_roots)
    h.collect()
    lo = h.tospace

    # The copies lie in to-space in breadth-first order, packed from the start.
    phi, a = {}, lo
    for x in order:
        phi[x] = a
        a += 1 + len(old[x])
    assert h.free == a
    assert h.objects() == [phi[x] for x in order]

    # Every reference is updated, so the graphs are isomorphic under phi.
    assert h.roots == [None if r is None else phi[r] for r in old_roots]
    for x in order:
        assert h.fields(phi[x]) == [None if y is None else phi[y] for y in old[x]]
    assert all(w is None for w in h.mem[h.free:h.end])
    return phi


def build(objs: list[list[int | None]], roots: list[int | None], slack: int = 0) -> Heap:
    """Allocate the objects in order; field and root values are object indexes."""
    h = Heap(sum(1 + len(f) for f in objs) + slack)
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
    # A -> (B, C), B -> (D), C -> (E), D and E have no fields, G -> (A) is garbage.
    h = build([[1, 2], [3], [4], [], [], [0]], [0])
    phi = check(h)
    assert phi == {0: 11, 3: 14, 5: 16, 7: 18, 8: 19}
    assert h.mem[11:20] == [3, 14, 16, 2, 18, 2, 19, 1, 1]
    assert h.roots == [11]


def test_edges() -> None:
    check(Heap(0))
    check(build([[None]], []))
    check(build([[0]], [0]))
    check(build([[], [None, None], []], [2, 2, None]))
    h = build([[1], [0]], [1, 0])
    assert check(h) == {2: 4, 0: 6}  # the root order decides: the second object is copied first
    check(h)
    assert h.tospace == 0


def test_long_list_needs_no_stack() -> None:
    n = 100_000
    h = build([[i + 1] for i in range(n - 1)] + [[None]], [0])
    check(h)
    assert h.free - h.tospace == 2 * n


def test_random_heaps() -> None:
    rng = random.Random(1970)
    for _ in range(700):
        m = rng.randint(1, 25)
        objs = [[rng.choice([None, rng.randrange(m)]) for _ in range(rng.randint(0, 4))] for _ in range(m)]
        roots = [rng.choice([None, rng.randrange(m)]) for _ in range(rng.randint(0, 4))]
        h = build(objs, roots, rng.randint(0, 5))
        check(h)
        check(h)


def test_mutator_with_allocation() -> None:
    rng = random.Random(5)
    for _ in range(60):
        h = Heap(rng.randint(20, 60))
        for _ in range(200):
            reach = sorted(bfs_order({a: h.fields(a) for a in h.objects()}, h.roots))
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
