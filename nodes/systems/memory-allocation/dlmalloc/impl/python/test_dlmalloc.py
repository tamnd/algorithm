# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dlmalloc/. The authors are listed in prov/5Q3MDD.jsonl.

import random

from dlmalloc import MIN_CHUNK, MIN_LARGE, DLMalloc, pad_request, small_index, tree_index


def binned(m: DLMalloc) -> dict[int, int]:
    out: dict[int, int] = {}
    for i, b in enumerate(m.smallbins):
        for a in b:
            assert a not in out
            out[a] = i << 3
    for b in m.treebins:
        for size, a in b:
            assert a not in out
            out[a] = size
    return out


def check(m: DLMalloc, live: dict[int, int]) -> None:
    chunks = m.chunks()
    assert set(m.head) == {a for a, _, _ in chunks}
    assert m.top + m.topsize == m.footprint
    prev_inuse = True
    prev_free = False
    feet = {}
    for a, size, inuse in chunks:
        assert m.head[a][2] == prev_inuse
        if a != m.top:
            assert size >= MIN_CHUNK and size % 8 == 0
            assert not (prev_free and not inuse), "two adjacent free chunks"
            if not inuse:
                feet[a + size] = size
        else:
            assert not prev_free, "a free chunk next to top"
        prev_inuse, prev_free = inuse, not inuse
    assert feet == m.foot
    bins = binned(m)
    free_chunks = {a: s for a, s, u in chunks if not u and a != m.top}
    if m.dvsize:
        assert free_chunks.pop(m.dv) == m.dvsize
        assert m.dv not in bins
    assert bins == free_chunks
    for a, s in bins.items():
        if s < MIN_LARGE:
            assert a in m.smallbins[small_index(s)]
        else:
            assert (s, a) in m.treebins[tree_index(s)]
    in_arena = {a: s for a, s, u in chunks if u}
    assert set(in_arena) | set(m.mapped) == set(live)
    for a, req in live.items():
        size = m.mapped.get(a, in_arena.get(a))
        assert size is not None and size >= pad_request(req)


def run(rng: random.Random, steps: int, big: bool) -> None:
    m = DLMalloc(mmap_threshold=2048)
    live: dict[int, int] = {}
    for _ in range(steps):
        if live and rng.random() < 0.45:
            a = rng.choice(sorted(live))
            del live[a]
            m.free(a)
        else:
            req = rng.choice([rng.randint(1, 60), rng.randint(1, 300)])
            if big and rng.random() < 0.1:
                req = rng.randint(1500, 5000)
            nb = pad_request(req)
            before = binned(m)
            dv = m.dvsize
            a = m.malloc(req)
            assert a not in live
            live[a] = req
            fits = {x: s for x, s in before.items() if s >= nb}
            if nb < MIN_LARGE:
                exact = [x for x, s in before.items() if s in (nb, nb + 8)]
                if exact:
                    assert a in exact
                elif nb > dv and fits:
                    assert before.get(a) == min(fits.values())
            elif a in before:
                assert before[a] == min(fits.values())
                assert nb > dv or before[a] - nb < dv - nb
        check(m, live)


def test_example_trace() -> None:
    m = DLMalloc()
    a = m.malloc(20)
    b = m.malloc(100)
    c = m.malloc(20)
    d = m.malloc(300)
    e = m.malloc(20)
    assert (a, b, c, d, e) == (0, 24, 128, 152, 456)
    m.free(b)
    assert m.smallbins[small_index(104)] == [24]
    m.free(d)
    assert m.treebins[tree_index(304)] == [(304, 152)]
    f = m.malloc(40)
    assert f == 24 and (m.dv, m.dvsize) == (72, 56)
    g = m.malloc(48)
    assert g == 72 and m.dvsize == 0
    m.free(c)
    assert m.chunks()[3] == (128, 328, False)
    h = m.malloc(200)
    assert h == 128 and (m.dv, m.dvsize) == (336, 120)
    i = m.malloc(1000)
    assert i == 480 and (m.top, m.topsize) == (1488, 2608)
    check(m, {a: 20, e: 20, f: 40, g: 48, h: 200, i: 1000})
    m.free(e)
    assert (m.dv, m.dvsize) == (336, 144)


def test_mmap_and_top() -> None:
    m = DLMalloc(mmap_threshold=1024)
    a = m.malloc(5000)
    assert a in m.mapped and m.footprint == 0
    m.free(a)
    assert not m.mapped
    b = m.malloc(500)
    c = m.malloc(700)
    assert (b, c) == (0, 504)
    m.free(c)
    m.free(b)
    assert m.chunks() == [(0, 4096, False)]


def test_random_traces() -> None:
    rng = random.Random(1)
    for trial in range(500):
        run(rng, 40, big=trial % 2 == 0)


def test_long_trace() -> None:
    run(random.Random(2), 3000, big=True)
