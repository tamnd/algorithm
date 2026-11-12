# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jemalloc/. The authors are listed in prov/6D7E5P.jsonl.

import random

from jemalloc import CHUNK, MAX_ORDER, NPAGES, PAGE, QUANTUM, Jemalloc, Run, run_layout, size_class


def run_at(m: Jemalloc, p: int) -> Run:
    k = p & ~(CHUNK - 1)
    r = m.pagemap[k][(p - k) // PAGE]
    assert r is not None
    return r


def check(m: Jemalloc, live: dict[int, int]) -> None:
    # live objects are disjoint and sit where their class says
    spans = sorted((p, size_class(n)) for p, n in live.items())
    for (p, s), (q, _) in zip(spans, spans[1:]):
        assert p + s <= q, "two live objects overlap"
    in_run: dict[int, int] = {}
    for p, n in live.items():
        c = size_class(n)
        assert c >= n
        if n > CHUNK // 2:
            assert p % CHUNK == 0 and m.huge[p] == c and p not in m.owner
            continue
        r = run_at(m, p)
        if c > PAGE // 2:
            assert r.cls == 0 and r.start == p and r.npages * PAGE == c
            continue
        assert r.cls == c and p % min(c, QUANTUM) == 0
        i, rest = divmod(p - r.start - r.hdr, c)
        assert rest == 0 and r.bitmap >> i & 1
        in_run[id(r)] = in_run.get(id(r), 0) + 1
    # each arena chunk is tiled by free buddy blocks and runs
    for k, a in m.owner.items():
        pm = m.pagemap[k]
        cover = [0] * NPAGES
        runs = {id(r): r for r in pm if r is not None}.values()
        assert runs, "a chunk with no run should have been given back"
        for r in runs:
            assert r.arena is a and r.chunk == k and r.page % r.npages == 0
            assert pm[r.page : r.page + r.npages] == [r] * r.npages
            for i in range(r.page, r.page + r.npages):
                cover[i] += 1
            if r.cls:
                assert bin(r.bitmap).count("1") == r.used == in_run.get(id(r), 0)
                assert r.hdr + r.nregs * r.cls <= r.npages * PAGE
                place = (a.current.get(r.cls) is r) + (r in a.nonfull.get(r.cls, ()))
                if r.used == r.nregs:
                    assert place <= 1 and r not in a.nonfull.get(r.cls, ())
                else:
                    assert place == 1
                assert r.used > 0 or (a.current.get(r.cls) is r and not r.promoted)
            else:
                assert r.start in live
        for o in range(MAX_ORDER):
            for ch, pg in a.free[o]:
                if ch != k:
                    continue
                assert pg % (1 << o) == 0 and (ch, pg ^ (1 << o)) not in a.free[o], "free buddies not merged"
                assert pm[pg : pg + (1 << o)] == [None] * (1 << o)
                for i in range(pg, pg + (1 << o)):
                    cover[i] += 1
        assert cover == [1] * NPAGES
    for a in m.arenas:
        assert not a.free[MAX_ORDER]
        for o in range(MAX_ORDER):
            assert all(ch in m.owner and m.owner[ch] is a for ch, _ in a.free[o])
        for c, rs in a.nonfull.items():
            for r in rs:
                assert r.cls == c and 0 < r.used < r.nregs and r.promoted and a.current.get(c) is not r
    assert m.mapped == len(m.owner) + sum(s // CHUNK for s in m.huge.values())


def trace(rng: random.Random, steps: int, threads: int, sizes: list[int], ncpus: int) -> None:
    m = Jemalloc(ncpus)
    live: dict[int, int] = {}
    for step in range(steps):
        t = rng.randrange(threads)
        if live and rng.random() < 0.45:
            p = rng.choice(sorted(live))
            del live[p]
            m.free(t, p)
        else:
            n = rng.choice(sizes)
            a = m.arena(t)
            p = m.malloc(t, n)
            assert p not in live
            live[p] = n
            c = size_class(n)
            if c <= PAGE // 2:
                r = run_at(m, p)
                i = (p - r.start - r.hdr) // c
                assert r.arena is a and a.current[c] is r
                assert r.bitmap & ((2 << i) - 1) == (2 << i) - 1, "not the first free region"
            elif n <= CHUNK // 2:
                assert m.owner[p & ~(CHUNK - 1)] is a
        if step % 4 == 0:
            check(m, live)
    check(m, live)
    for p in sorted(live):
        m.free(0, p)
    check(m, {})
    # only QINIT current runs may stay
    for k in m.owner:
        for r in m.pagemap[k]:
            assert r is None or (r.cls and r.used == 0 and not r.promoted)


def test_size_classes() -> None:
    assert [size_class(n) for n in (1, 2, 3, 5, 8)] == [2, 2, 4, 8, 8]
    assert [size_class(n) for n in (9, 16, 17, 500, 512)] == [16, 16, 32, 512, 512]
    assert [size_class(n) for n in (513, 1025, 2049, 5000, 1 << 20)] == [1024, 2048, 4096, 8192, 1 << 20]
    assert [size_class(n) for n in ((1 << 20) + 1, 5 * 1024 * 1024)] == [CHUNK, 3 * CHUNK]
    assert run_layout(16) == (1, 253, 48)
    assert run_layout(2048) == (16, 31, 32)  # about 3% lost, as in the paper
    for c in [2, 4, 8] + list(range(16, 513, 16)) + [1024, 2048]:
        pages, n, h = run_layout(c)
        assert h + n * c <= pages * PAGE < h + (n + 1) * c + 16 + QUANTUM
        assert (pages * PAGE - n * c - (n + 7) // 8) * 32 <= pages * PAGE


def test_example_trace() -> None:
    m = Jemalloc(ncpus=2)
    assert len(m.arenas) == 8
    a = m.malloc(0, 20)  # thread 0 -> arena 0, new chunk 1, 1-page run of 32-byte regions
    assert a == CHUNK + 32 and m.thread_arena[0].index == 0
    b = m.malloc(1, 20)  # thread 1 -> arena 1, its own chunk 2
    assert b == 2 * CHUNK + 32 and m.thread_arena[1].index == 1
    c = m.malloc(0, 30)  # same run, next region
    assert c == CHUNK + 64
    d = m.malloc(0, 3000)  # large: one page by buddy split
    assert d == CHUNK + PAGE
    m.free(1, a)  # thread 1 frees: chunk 1 belongs to arena 0
    assert m.arenas[0].locks == 4 and m.arenas[1].locks == 1
    e = m.malloc(0, 17)  # first free region again
    assert e == a
    h = m.malloc(0, 3 << 20)  # huge: 2 dedicated chunks
    assert h == 3 * CHUNK and m.huge[h] == 2 * CHUNK and m.mapped == 4
    m.free(0, h)
    m.free(0, d)
    assert m.mapped == 2


def test_round_robin_arenas() -> None:
    assert len(Jemalloc(ncpus=1).arenas) == 1
    m = Jemalloc(ncpus=4)
    assert len(m.arenas) == 16
    order = [7, 3, 11, 0, 5] + list(range(20, 40))
    for t in order:
        m.malloc(t, 8)
    for k, t in enumerate(order):
        assert m.thread_arena[t].index == k % 16


def test_run_choice_order() -> None:
    m = Jemalloc(ncpus=1)
    c = 512
    pages, n, _ = run_layout(c)
    assert n == 31
    ps = [m.malloc(0, c) for _ in range(4 * n)]
    runs = sorted({id(run_at(m, p)): run_at(m, p) for p in ps}.values(), key=lambda r: r.start)
    assert len(runs) == 4 and m.arenas[0].current[c] is runs[3]
    keep = {0: 10, 1: 20, 2: 28}  # Q25, Q50, Q75; run 3 stays full and current
    for j, k in keep.items():
        mine = [p for p in ps if run_at(m, p) is runs[j]]
        for p in mine[k:]:
            m.free(0, p)
    assert [runs[j].quartile() for j in range(3)] == [1, 2, 3]
    p = m.malloc(0, c)  # current is full: Q50 is chosen first
    assert run_at(m, p) is runs[1]
    for _ in range(n - 21):
        m.malloc(0, c)
    p = m.malloc(0, c)  # run 1 is full again; Q25 is next
    assert run_at(m, p) is runs[0]


def test_random_small() -> None:
    rng = random.Random(1)
    for _ in range(300):
        trace(rng, 80, rng.randint(1, 5), [1, 3, 8, 16, 24, 100, 500, 512, 700, 2000], rng.choice([1, 2]))


def test_random_mixed() -> None:
    rng = random.Random(2)
    for _ in range(200):
        sizes = [8, 48, 1000, 3000, 9000, 70000, 600000, 1 << 20, (1 << 20) + 1, 5 << 20]
        trace(rng, 60, rng.randint(1, 4), sizes, rng.choice([1, 2, 4]))


def test_long_trace() -> None:
    trace(random.Random(3), 3000, 6, [16, 32, 48, 64, 2048, 4096, 16384], 1)
