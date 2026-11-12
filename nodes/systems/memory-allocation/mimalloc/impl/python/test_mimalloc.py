# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mimalloc/. The authors are listed in prov/2S5369.jsonl.

import random

from mimalloc import SEG, Mimalloc, size_class


def check(m: Mimalloc, live: dict[int, tuple[int, int]]) -> None:
    """Every block of every page is in exactly one place, and the counters agree."""
    owner_of_live: dict[int, int] = {}
    for p, (_, n) in live.items():
        seg = m.segments[p & ~(SEG - 1)]
        page = seg.pages[(p - seg.base) // seg.page_size]
        assert page is not None and page.block >= n
        owner_of_live[p] = id(page)
    for seg in m.segments.values():
        for page in seg.pages:
            if page is None:
                continue
            blocks = {page.base + i * page.block for i in range(page.capacity)}
            mine = [p for p, pid in owner_of_live.items() if pid == id(page)]
            places = page.free + page.local_free + page.thread_free + mine
            assert sorted(places) == sorted(blocks)
            assert page.thread_freed == len(page.thread_free)
            assert page.used - page.thread_freed == len(mine) > 0 or page.used == page.thread_freed
            assert page.used == len(mine) + len(page.thread_free)
            assert page in m.heap(seg.thread).pages[page.block]


def run(rng: random.Random, steps: int, threads: int, page_size: int, sizes: list[int]) -> None:
    beats: list[int] = []
    m = Mimalloc(page_size=page_size, deferred_free=beats.append)
    live: dict[int, tuple[int, int]] = {}
    fast_run: dict[tuple[int, int], int] = {}
    for _ in range(steps):
        t = rng.randrange(threads)
        before = m.atomics
        if live and rng.random() < 0.5:
            p = rng.choice(sorted(live))
            owner, _ = live.pop(p)
            m.free(t, p)
            if t == owner:
                assert m.atomics == before, "a local free used an atomic operation"
            else:
                assert m.atomics == before + 2
        else:
            n = rng.choice(sizes)
            calls = m.generic_calls
            p = m.malloc(t, n)
            assert p not in live
            live[p] = (t, n)
            key = (t, size_class(n))
            if m.generic_calls == calls:
                assert m.atomics == before, "the fast path used an atomic operation"
                fast_run[key] = fast_run.get(key, 0) + 1
                # heartbeat: the fast path serves at most one page worth of blocks in a row
                assert fast_run[key] <= max(1, page_size // size_class(n))
            else:
                assert beats[-1] == t
                fast_run[key] = 0
            seg = m.segments[p & ~(SEG - 1)]
            assert seg.thread == t, "allocation is always in the local heap"
        check(m, live)
    assert len(beats) == m.generic_calls


def test_example_trace() -> None:
    m = Mimalloc(page_size=128)  # pages of 128 bytes: 8 blocks of 16 bytes
    a = [m.malloc(0, 16) for _ in range(8)]
    s = SEG
    assert a == [s + 16 * i for i in range(8)] and m.generic_calls == 1
    page = m.heap(0).direct[16]
    m.free(0, a[1])  # local free: goes to local_free, not to free
    assert page.local_free == [s + 16] and page.free == [] and page.used == 7
    m.free(1, a[2])  # thread 1 frees: atomic push on thread_free
    assert page.thread_free == [s + 32] and page.thread_freed == 1 and m.atomics == 2
    b = m.malloc(0, 16)  # free is empty: generic collects both lists
    assert m.generic_calls == 2 and b == s + 16
    assert page.used == 7 and page.thread_freed == 0 and m.atomics == 3
    c = m.malloc(0, 16)
    assert {b, c} == {s + 16, s + 32} and m.generic_calls == 2
    for p in a[:1] + a[3:] + [b, c]:
        m.free(0, p)
    assert m.segments[s].pages[0] is None  # used - thread_freed reached 0: the page is freed


def test_size_class() -> None:
    assert [size_class(n) for n in (1, 8, 9, 64, 65, 80, 81, 129, 1000)] == [8, 8, 16, 64, 80, 80, 96, 160, 1024]
    for n in range(1, 5000):
        c = size_class(n)
        assert c >= n and size_class(c) == c and c - n <= max(7, c // 4)


def test_random_small_pages() -> None:
    rng = random.Random(1)
    for _ in range(400):
        run(rng, 50, rng.randint(1, 4), 128, [1, 8, 16, 24, 40])


def test_random_with_large() -> None:
    rng = random.Random(2)
    for _ in range(100):
        run(rng, 60, 3, 256, [8, 16, 32, 48, 100, 2000])


def test_long_trace() -> None:
    run(random.Random(3), 2000, 3, 512, [8, 16, 24, 32, 64, 96])
