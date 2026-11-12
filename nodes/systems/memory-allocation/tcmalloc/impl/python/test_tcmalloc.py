# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tcmalloc/. The authors are listed in prov/XSTE1X.jsonl.

import random

from tcmalloc import MAX_SMALL, PAGE, TCMalloc, batch, size_class


def check(m: TCMalloc, live: dict[int, int], full: bool = True) -> None:
    # page heap: spans tile [0, heap_pages), the pagemap agrees, no two free spans touch
    spans = sorted({id(s): s for s in m.pagemap.values()}.values(), key=lambda s: s.start)
    at = 0
    prev_free = False
    for s in spans:
        assert s.start == at and s.npages > 0
        assert all(m.pagemap[p] is s for p in range(s.start, s.start + s.npages))
        assert not (prev_free and s.free), "two adjacent free spans"
        assert s.free == (s in m.free_spans)
        prev_free = s.free
        at += s.npages
    assert at == m.heap_pages
    # every object of every small span is in exactly one place
    cached = {}
    for t, lists in m.caches.items():
        size = 0
        for c, fl in lists.items():
            # length may exceed max_length after max_length drops (L9, L11): no check here
            assert fl.max_length >= 1
            assert fl.lowater <= len(fl.items)
            size += c * len(fl.items)
            for p in fl.items:
                assert p not in cached
                cached[p] = c
        assert m.cache_size.get(t, 0) == size
    outside: dict[int, int] = {}  # span start -> objects held by caches or by the program
    small_live = [p for p, n in live.items() if n <= MAX_SMALL]
    for p in list(cached) + small_live:
        s = m.pagemap[p // PAGE]
        assert s.cls and (p - s.start * PAGE) % s.cls == 0
        outside[s.start] = outside.get(s.start, 0) + 1
    assert len(set(cached) | set(small_live)) == len(cached) + len(small_live)
    for s in spans:
        if s.free or s.cls == 0:
            assert not s.objects
            continue
        inside = set(s.objects)
        assert len(inside) == len(s.objects) and not inside & set(cached)
        if full:
            assert inside <= set(range(s.start * PAGE, (s.start + 1) * PAGE - s.cls + 1, s.cls))
        assert s.refcount == outside.get(s.start, 0) > 0
        assert len(inside) + s.refcount == PAGE // s.cls
        assert (s in m.central[s.cls]) == bool(s.objects)
    for p, n in live.items():
        s = m.pagemap[p // PAGE]
        assert not s.free
        if n > MAX_SMALL:
            assert s.cls == 0 and s.start * PAGE == p and s.npages * PAGE >= n
        else:
            assert s.cls == size_class(n) and p not in cached


def run(rng: random.Random, steps: int, threads: int, sizes: list[int], max_cache: int) -> TCMalloc:
    m = TCMalloc(max_cache=max_cache)
    live: dict[int, int] = {}
    for step in range(steps):
        t = rng.randrange(threads)
        if live and rng.random() < 0.5:
            p = rng.choice(sorted(live))
            del live[p]
            m.free(t, p)
        else:
            n = rng.choice(sizes)
            p = m.malloc(t, n)
            assert p not in live
            live[p] = n
        check(m, live, full=step % 10 == 0)
    for p in sorted(live):
        m.free(0, p)
    for t in list(m.caches):
        for c, fl in m.caches[t].items():
            m._release(t, c, fl, len(fl.items))
    check(m, {})
    assert m.free_spans and len(m.free_spans) == 1  # all memory coalesced back into one span
    return m


def test_example_trace() -> None:
    m = TCMalloc()
    c = size_class(100)
    assert c == 104 and batch(c) == 32
    p1 = m.malloc(0, 100)  # empty list: fetch min(max_length=1, 32) = 1 object
    assert m.central_locks == 1 and m.caches[0][c].max_length == 2
    p2 = m.malloc(0, 100)  # fetch 2, keep 1 in the cache
    assert m.central_locks == 2 and len(m.caches[0][c].items) == 1 and m.caches[0][c].max_length == 3
    p3 = m.malloc(0, 100)  # fast path: no lock
    assert m.central_locks == 2 and p3 == p2 + c
    assert [p1, p2, p3] == [0, 104, 208]
    m.free(1, p1)  # another thread frees: it goes to thread 1's cache
    assert m.caches[1][c].items == [0]
    big = m.malloc(0, 20000)  # 3 pages from the page heap
    assert big == PAGE * 1 and m.pagemap[1].npages == 3
    m.free(0, big)
    assert m.heap_pages == 16 and len(m.free_spans) == 1


def test_slow_start() -> None:
    m = TCMalloc(max_cache=1 << 30)
    c = size_class(64)
    b = batch(c)
    lengths = []
    for _ in range(2000):
        m.malloc(0, 64)
        lengths.append(m.caches[0][c].max_length)
    steps = sorted(set(lengths))
    assert steps[: b] == list(range(2, b + 2)) or steps[:b - 1] == list(range(2, b + 1))
    assert all(x % b == 0 for x in steps if x > b)
    # each central visit brings at most max_length objects, so visits drop as the list grows
    assert m.central_locks < 2000 // 8


def test_scavenge_low_water() -> None:
    m = TCMalloc(max_cache=1 << 30)
    c = size_class(16)
    ps = [m.malloc(0, 16) for _ in range(40)]
    for p in ps:
        m.free(0, p)
    fl = m.caches[0][c]
    m.scavenge(0)  # sets the low-water mark to the current length
    n = len(fl.items)
    assert fl.lowater == n
    for _ in range(6):
        m.malloc(0, 16)
    assert fl.lowater == n - 6
    m.scavenge(0)  # releases half of the low-water mark: never touched objects
    assert len(fl.items) == (n - 6) - (n - 6) // 2
    assert fl.lowater == len(fl.items)


def test_random_traces() -> None:
    rng = random.Random(1)
    for _ in range(400):
        run(rng, 60, rng.randint(1, 3), [1, 8, 30, 64, 100, 500, 1024, 3000, 20000], rng.choice([512, 2048, 16384]))


def test_long_trace() -> None:
    run(random.Random(2), 2500, 3, [8, 16, 24, 64, 128, 256, 9000], 4096)
