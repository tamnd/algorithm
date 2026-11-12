# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mostly-copying-collection/. The authors are listed in prov/EE82ME.jsonl.

import copy
import random

from mostly_copying_collection import MostlyCopyingHeap, Obj


def reach(objs: dict[int, Obj], starts: list[int]) -> set[int]:
    seen: set[int] = set()
    todo = [a for a in starts if a]
    while todo:
        a = todo.pop()
        if a not in seen:
            seen.add(a)
            todo += [p for p in objs[a].words[:objs[a].nptr] if p]
    return seen


def check(old: dict[int, Obj], h: MostlyCopyingHeap, real_roots: list[int], pinned_pages: set[int]) -> None:
    """The graph seen from the real roots is the same, and pinned objects stay."""
    image: dict[int, int] = {}

    def same(a: int, b: int) -> None:
        if a == 0:
            assert b == 0
            return
        if a in image:
            assert image[a] == b
            return
        image[a] = b
        o, n = old[a], h.objs[b]
        assert o.nptr == n.nptr and o.words[o.nptr:] == n.words[n.nptr:]
        for x, y in zip(o.words[:o.nptr], n.words[:n.nptr]):
            same(x, y)

    for r in real_roots:
        same(r, r)  # a real root is never changed, so its object must not move
    for a in old:
        if h.page_of(a) in pinned_pages:
            assert a in h.objs, "an object on a promoted page was freed or moved"
    for a, o in h.objs.items():
        assert h.space[h.page_of(a)] == h.current
        for p in o.words[:o.nptr]:
            assert p == 0 or p in h.objs, "a dangling pointer"


def test_random_programs() -> None:
    copies = pins = 0
    for seed in range(150):
        rng = random.Random(seed)
        h = MostlyCopyingHeap(pages=24, page_words=rng.randint(3, 8))
        real: list[int] = []
        for _ in range(4):  # rounds of mutation and collection
            for _ in range(rng.randint(5, 15)):
                n = rng.randint(1, min(4, h.P))
                try:
                    a = h.alloc(rng.randint(0, n), n)
                except MemoryError:
                    break
                o = h.objs[a]
                for i in range(n):
                    if i < o.nptr:
                        o.words[i] = rng.choice(list(h.objs) + [0])
                    else:
                        o.words[i] = rng.randrange(1000)
                real.append(a)
            real = rng.sample(real, k=min(len(real), rng.randint(0, 4)))
            noise = [rng.randrange(h.base, h.base + h.npages * h.P) for _ in range(rng.randint(0, 3))]
            roots = real + noise
            frozen = list(roots)
            old = copy.deepcopy(h.objs)
            live = reach(old, real)
            pinned = h.promoted_by(roots)
            try:
                h.collect(roots)
            except MemoryError:
                break
            assert roots == frozen, "ambiguous roots are never changed"
            check(old, h, real, pinned)
            copies += sum(1 for a in live if a not in h.objs)
            pins += len(pinned)
            # exactly the objects on pinned pages, and what they reach, survive
            kept_old = reach(old, [a for a in old if h.page_of(a) in pinned])
            assert live <= kept_old
            assert len(h.objs) == len(kept_old)
    assert copies > 0 and pins > 0


def test_page_example() -> None:
    h = MostlyCopyingHeap(pages=6, page_words=4, base=100)
    A = h.alloc(1, 2)
    B = h.alloc(1, 2)
    C = h.alloc(1, 2)
    F = h.alloc(0, 2)
    D = h.alloc(1, 2)
    E = h.alloc(0, 1)
    assert (A, B, C, F, D, E) == (100, 102, 104, 106, 108, 110)
    h.objs[A].words = [C, 7]
    h.objs[B].words = [E, 0]
    h.objs[C].words = [D, 5]
    h.objs[D].words = [0, 9]
    h.objs[E].words = [3]
    h.collect([100, 3])  # a pointer to A, and a small integer
    assert h.space[:5] == [2, None, None, 2, 2]  # page 0 promoted, pages 3 and 4 hold copies
    assert sorted(h.objs) == [100, 102, 112, 114, 116]
    assert h.objs[100].words == [112, 7]  # A stays; its field now points to the copy of C
    assert h.objs[102].words == [114, 0]  # B is garbage but shares A's page; E is copied for it
    assert h.objs[112].words == [116, 5] and h.objs[116].words == [0, 9] and h.objs[114].words == [3]


def test_interior_and_noise_words_promote_pages() -> None:
    h = MostlyCopyingHeap(pages=4, page_words=4, base=100)
    x = h.alloc(0, 4)  # fills page 0
    y = h.alloc(0, 2)  # page 1
    h.collect([x + 3])  # an interior word pins x's page, and y is garbage
    assert x in h.objs and y not in h.objs
    h.collect([105])  # a word into page 1, which is free now: nothing is promoted
    assert h.objs == {}
