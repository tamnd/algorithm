# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slab-allocator/. The authors are listed in prov/T3R2XK.jsonl.

import random

import pytest

from slab_allocator import PageSource, SlabCache


def make(pages: int = 3, page_words: int = 16, size: int = 3, align: int = 1):
    log = {"ctor": 0, "dtor": 0}

    def ctor(_: int) -> None:
        log["ctor"] += 1

    def dtor(_: int) -> None:
        log["dtor"] += 1

    src = PageSource(pages, page_words)
    return src, SlabCache(size, src, align, ctor, dtor), log


def test_worked_example() -> None:
    src, c, log = make()
    objs = [c.alloc() for _ in range(5)]
    assert objs == [0, 3, 6, 9, 12]  # one slab of 5 objects, now full
    assert log["ctor"] == 5 and len(src.in_use) == 1
    c.free(6)
    assert c.alloc() == 6  # the freed object comes back before any new slab
    assert len(src.in_use) == 1 and log["ctor"] == 5
    assert c.alloc() == 17  # a new slab, with color offset 1
    assert log["ctor"] == 10 and len(src.in_use) == 2
    c.free(17)  # the second slab is now wholly free
    assert c.reap() == 1 and log["dtor"] == 5
    assert src.in_use == {0}


def test_reuse_before_new_slab() -> None:
    rng = random.Random(1994)
    src, c, log = make(pages=8, page_words=32, size=5)
    live: list[int] = []
    for _ in range(2000):
        if live and rng.random() < 0.5:
            c.free(live.pop(rng.randrange(len(live))))
        else:
            slabs_before = len(c.slabs)
            had_free = any(s.free for s in c.slabs.values())
            p = c.alloc()
            if p is None:
                assert not had_free and not src.stack
                continue
            assert p not in live
            live.append(p)
            # a new slab is made only when no slab of the cache has a free object
            assert (len(c.slabs) > slabs_before) == (not had_free)
        c.check_invariant()
        # the constructor ran exactly once per object of each slab ever made
        assert log["ctor"] - log["dtor"] == c.per_slab * len(c.slabs)
        if rng.random() < 0.05:
            used = {p - p % 32 for p in live}
            c.reap()
            assert set(c.slabs) == used, "reap frees exactly the slabs with no live object"


def test_colors_cycle() -> None:
    src = PageSource(6, 16)
    c = SlabCache(3, src, align=1)  # 5 objects per slab, slack 1: colors 0 and 1
    firsts = []
    for _ in range(6):
        firsts.append(c.alloc())
        for _ in range(4):
            c.alloc()
    assert [p % 16 for p in firsts] == [0, 1, 0, 1, 0, 1]


def test_errors() -> None:
    src, c, _ = make()
    p = c.alloc()
    c.free(p)
    with pytest.raises(ValueError):
        c.free(p)
    with pytest.raises(ValueError):
        SlabCache(17, src)
