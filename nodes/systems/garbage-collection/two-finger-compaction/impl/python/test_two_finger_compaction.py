# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-finger-compaction/. The authors are listed in prov/JTB830.jsonl.

import random

from two_finger_compaction import Heap


def reachable(fields: list[list[int | None]], roots: list[int | None]) -> set[int]:
    """Oracle: breadth-first search from the roots."""
    seen = {r for r in roots if r is not None}
    queue = list(seen)
    i = 0
    while i < len(queue):
        for y in fields[queue[i]]:
            if y is not None and y not in seen:
                seen.add(y)
                queue.append(y)
        i += 1
    return seen


def isomorphism(old: list[list[int | None]], old_roots: list[int | None], h: Heap) -> dict[int, int]:
    """Build the map from old to new addresses by walking both graphs; fail if they differ."""
    phi: dict[int, int] = {}
    work = []

    def match(a: int | None, b: int | None) -> None:
        assert (a is None) == (b is None)
        if a is None:
            return
        if a in phi:
            assert phi[a] == b
        else:
            phi[a] = b
            work.append(a)

    assert len(old_roots) == len(h.roots)
    for a, b in zip(old_roots, h.roots):
        match(a, b)
    while work:
        a = work.pop()
        for x, y in zip(old[a], h.fields[phi[a]]):
            match(x, y)
    assert len(set(phi.values())) == len(phi)
    return phi


def check(fields: list[list[int | None]], roots: list[int | None]) -> Heap:
    h = Heap(fields, roots)
    live = reachable(fields, roots)
    top = h.collect()
    assert top == len(live)
    phi = isomorphism(fields, roots, h)
    assert set(phi) == live and set(phi.values()) == set(range(top))
    assert all(phi[a] == a for a in live if a < top)
    assert h.moves == sum(1 for a in live if a >= top)
    assert not any(h.marked)
    return h


def test_example() -> None:
    fields = [[2, None], [None, 6], [5, None], [7, 1], [None, None], [0, None], [3, 4], [6, None]]
    h = check(fields, [3])
    assert h.top == 5 and h.moves == 2
    assert h.fields[:5] == [[2, None], [None, 2], [3, 4], [0, 1], [None, None]]
    assert h.roots == [3]


def test_edges() -> None:
    check([], [])
    check([[None]], [])
    check([[0]], [0])
    check([[None], [None], [None]], [2, 2, None])
    h = check([[1], [0], [None]], [1])
    assert h.top == 2 and h.moves == 0


def test_random_heaps() -> None:
    rng = random.Random(1974)
    for _ in range(800):
        n, k = rng.randint(1, 30), rng.randint(1, 3)
        fields = [[rng.choice([None, rng.randrange(n)]) for _ in range(k)] for _ in range(n)]
        roots = [rng.choice([None, rng.randrange(n)]) for _ in range(rng.randint(0, 4))]
        check(fields, roots)


def test_order_is_not_kept() -> None:
    h = check([[None], [None], [None], [None]], [1, 3])
    assert h.roots == [1, 0]
