# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boehm-gc/. The authors are listed in prov/SF0WFK.jsonl.

import random

from boehm_gc import ATOMIC, NORMAL, BoehmHeap


def objects(h: BoehmHeap) -> list[tuple[int, int, str]]:
    """(start, size, kind) of every allocated object."""
    out = []
    for b, blk in enumerate(h.blocks):
        if blk:
            out += [(h.addr(b, i), blk.size, blk.kind) for i, u in enumerate(blk.allocated) if u]
    return out


def closure(h: BoehmHeap, roots: list[int]) -> tuple[set[int], set[int]]:
    """The objects that pointer-looking words retain, and the blocks they blacklist.

    Computed by a plain search over the object list, independent of the collector.
    """
    objs = objects(h)

    def find(w: int):
        for a, s, k in objs:
            if a <= w < a + s and (h.interior or w == a):
                return a, s, k
        return None

    kept: set[int] = set()
    black: set[int] = set()
    todo = list(roots)
    while todo:
        w = todo.pop()
        o = find(w)
        if o is None:
            if h.lo <= w < h.hi and h.blocks[h.block_of(w)] is None:
                black.add(h.block_of(w))
            continue
        a, s, k = o
        if a not in kept:
            kept.add(a)
            if k == NORMAL:
                todo += [h.load(x) for x in range(a, a + s)]
    return kept, black


def test_random_programs() -> None:
    gcs = 0
    for seed in range(60):
        rng = random.Random(seed)
        h = BoehmHeap(lo=1000, nblocks=12, block_words=8, interior=rng.random() < 0.7)
        roots: list[int] = []  # true pointers held by the program
        noise = [rng.randrange(990, 1110) for _ in range(rng.randint(0, 3))]
        shadow: dict[int, list[int]] = {}  # the contents the program wrote
        edges: dict[int, list[int]] = {}  # the true pointers in each object

        def reachable() -> set[int]:
            seen: set[int] = set()
            todo = list(roots)
            while todo:
                a = todo.pop()
                if a not in seen:
                    seen.add(a)
                    todo += edges[a]
            return seen

        for step in range(150):
            h.roots = roots + noise
            op = rng.random()
            if op < 0.5:
                n = rng.randint(1, 8)
                kind = ATOMIC if rng.random() < 0.2 else NORMAL
                a = h.allocate(n, kind)
                if a is None:
                    break
                s = h.size_class(n)
                words, ptrs = [], []
                for _ in range(s):
                    if kind == NORMAL and roots and rng.random() < 0.4:
                        t = rng.choice(roots)
                        words.append(t)
                        ptrs.append(t)
                    else:
                        words.append(rng.randrange(0, 1200))  # data, which may look like a pointer
                for k, w in enumerate(words):
                    h.store(a + k, w)
                shadow[a], edges[a] = words, ptrs
                roots.append(a)
            elif op < 0.8 and roots:
                roots.remove(rng.choice(roots))
            else:
                h.roots = roots + noise
                expect_kept, expect_black = closure(h, h.roots)
                h.collect()
                gcs += 1
                assert set(a for a, _, _ in objects(h)) == expect_kept
                assert h.blacklist == expect_black
            # safety: what the program can reach is allocated and unchanged
            live = {a for a, _, _ in objects(h)}
            for a in reachable():
                assert a in live
                assert [h.load(x) for x in range(a, a + len(shadow[a]))] == shadow[a]
            # the allocator took a blacklisted block only when nothing else was free
            assert sum(1 for _, bl in h.refills if bl) == h.fallbacks
    assert gcs > 100


def build(blacklisting: bool) -> tuple[BoehmHeap, int, int, int]:
    """The page example: a noise word 1009 points into block 2 before it is used."""
    h = BoehmHeap(lo=1000, nblocks=4, block_words=4, classes=(1, 2, 4), blacklisting=blacklisting)
    h.roots = [1009]
    h.collect()  # an early collection sees the noise word
    p = h.allocate(4)
    q = h.allocate(4)
    r = h.allocate(4)
    h.store(r, p)  # r points to p
    return h, p, q, r


def test_page_example_blacklisting() -> None:
    h, p, q, r = build(True)
    assert h.blacklist == {2}
    assert (p, q, r) == (1000, 1004, 1012)  # block 2 is skipped
    h.collect()  # the program holds none of them
    assert objects(h) == [] and h.blacklist == {2}


def test_page_example_without_blacklisting() -> None:
    h, p, q, r = build(False)
    assert (p, q, r) == (1000, 1004, 1008)
    h.collect()
    assert sorted(a for a, _, _ in objects(h)) == [1000, 1008]  # 1009 falsely retains r, and so p


def test_atomic_objects_are_not_scanned() -> None:
    h = BoehmHeap(lo=1000, nblocks=4, block_words=8)
    a = h.allocate(2)
    b = h.allocate(2, ATOMIC)
    h.store(b, a)
    h.collect([b])
    assert {x for x, _, _ in objects(h)} == {b}


def test_interior_pointers() -> None:
    for interior, kept in ((True, 1), (False, 0)):
        h = BoehmHeap(lo=1000, nblocks=4, block_words=8, interior=interior)
        a = h.allocate(4)
        h.collect([a + 2])
        assert len(objects(h)) == kept


def test_sweep_reuses_free_slots_and_blocks() -> None:
    h = BoehmHeap(lo=1000, nblocks=2, block_words=4, classes=(1, 2, 4))
    xs = [h.allocate(1) for _ in range(4)]
    assert xs == [1000, 1001, 1002, 1003]
    h.collect([1001, 1003])
    assert h.free_lists[(1, NORMAL)] == [1002, 1000]
    assert h.allocate(1) == 1000
    h.collect([])
    assert h.blocks == [None, None] and h.free_lists == {}
