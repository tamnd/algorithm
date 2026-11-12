# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hoard-allocator/. The authors are listed in prov/HAC5RQ.jsonl.

import random

from hoard_allocator import Hoard


def check_books(h: Hoard, live: dict[int, tuple[int, int]]) -> None:
    """u[i] and a[i] match the superblocks, and every live block is in exactly one place."""
    seen = set()
    for i, heap in enumerate(h.heaps):
        assert h.a[i] == h.S * len(heap)
        assert h.u[i] == sum(s.used for s in heap)
        for s in heap:
            assert s.owner == i
            assert len(set(s.free)) == len(s.free)
            assert s.used == s.size * (h.S // s.size - len(s.free))
    small = {p for p in live if p not in h.large}
    for p in small:
        s = h.sbs[p // h.S]
        idx = (p % h.S) // s.size
        assert idx not in s.free
        seen.add((s.sid, idx))
    assert len(seen) == len(small)
    assert sum(h.u) == sum(h.size_class(sz) for p, (_, sz) in live.items() if p not in h.large)


def test_example_trace() -> None:
    h = Hoard(processors=2, sb_size=64, f=0.25, k=0)
    # thread 0 uses heap 1, thread 1 uses heap 2; blocks of 16 bytes, 4 per superblock
    x = [h.malloc(0, 16) for _ in range(5)]
    assert x == [0, 16, 32, 48, 64]
    assert (h.u[1], h.a[1]) == (80, 128)
    y = h.malloc(1, 16)
    assert y == 128 and (h.u[2], h.a[2]) == (16, 64)
    h.free(x[1])  # u1 = 64 < 96: the emptiest superblock (at 64) moves to the global heap
    assert h.transfers == 1 and (h.u[1], h.a[1]) == (48, 64) and (h.u[0], h.a[0]) == (16, 64)
    assert h.invariant_holds(1)
    h.free(x[4])  # a free into a superblock of the global heap changes only heap 0
    assert (h.u[0], h.a[0]) == (0, 64)
    z = [h.malloc(1, 16) for _ in range(4)]
    assert z == [144, 160, 176, 64]  # heap 2 fills its own superblock, then takes the empty one
    assert (h.u[2], h.a[2]) == (80, 128) and h.a[0] == 0
    p = h.malloc(0, 16)
    assert p == 16  # LIFO: the block freed last in heap 1's superblock comes back first
    assert h.os_bytes == 192


def test_malloc_can_break_the_invariant() -> None:
    """Figure 2 checks the threshold only in free, so one transfer is not always enough."""
    h = Hoard(processors=1, sb_size=64, f=0.25, k=0)
    a1 = h.malloc(0, 32)
    h.malloc(0, 32)
    h.malloc(0, 16)
    h.malloc(0, 8)
    assert (h.u[1], h.a[1]) == (88, 192) and not h.invariant_holds(1)
    h.free(a1)
    assert h.transfers == 3 and h.max_moves_per_free == 3
    assert (h.u[1], h.a[1]) == (0, 0) and h.invariant_holds(1)


def test_false_sharing_avoided() -> None:
    """Threads on different heaps never get blocks of one superblock (so of one cache line)."""
    rng = random.Random(5)
    for _ in range(100):
        p = rng.randint(2, 6)
        h = Hoard(processors=p, sb_size=256, f=0.25, k=0)
        owner_heap: dict[int, int] = {}
        for _ in range(60):
            t = rng.randrange(p)
            q = h.malloc(t, 8)
            sid = q // h.S
            assert owner_heap.setdefault(sid, h.heap_of(t)) == h.heap_of(t)
    # a single heap hands consecutive 8-byte blocks of one 64-byte line to different threads
    one = Hoard(processors=1, sb_size=256)
    lines = {one.malloc(t, 8) // 64 for t in range(4)}
    assert len(lines) == 1


def random_trace(rng: random.Random, h: Hoard, steps: int, sizes: list[int]) -> int:
    live: dict[int, tuple[int, int]] = {}
    peak_class_bytes = 0
    for _ in range(steps):
        if live and rng.random() < 0.5:
            q = rng.choice(sorted(live))
            del live[q]
            owner = h.sbs[q // h.S].owner if q not in h.large else 0
            h.free(q)
            if owner:
                assert h.invariant_holds(owner)
        else:
            t = rng.randrange(2 * h.P)
            sz = rng.choice(sizes)
            q = h.malloc(t, sz)
            assert q not in live
            if q not in h.large:
                assert h.sbs[q // h.S].owner == h.heap_of(t)
            live[q] = (t, sz)
        check_books(h, live)
        used = sum(h.u)
        peak_class_bytes = max(peak_class_bytes, used)
    return peak_class_bytes


def test_random_many_classes() -> None:
    rng = random.Random(1)
    for _ in range(300):
        h = Hoard(rng.randint(1, 4), sb_size=rng.choice([64, 128, 256]), f=rng.choice([0.1, 0.25, 0.5]), k=rng.randint(0, 2))
        random_trace(rng, h, 60, [1, 8, 12, 16, 30, 64, 100, 200])


def test_blowup_bound_one_class() -> None:
    """With one size class: a_i <= u_i/(1-f) + (K+1)S always, and memory <= U/(1-f) + P(K+1)S."""
    rng = random.Random(2)
    for _ in range(300):
        p, k, f = rng.randint(1, 4), rng.randint(0, 2), rng.choice([0.1, 0.25, 0.5])
        h = Hoard(p, sb_size=128, f=f, k=k)
        live: dict[int, int] = {}
        peak = 0
        for _ in range(120):
            if live and rng.random() < rng.choice([0.3, 0.6]):
                q = rng.choice(sorted(live))
                del live[q]
                h.free(q)
            else:
                q = h.malloc(rng.randrange(8), 16)
                live[q] = 16
            peak = max(peak, sum(h.u))
            for i in range(1, p + 1):
                assert h.a[i] <= h.u[i] / (1 - f) + (k + 1) * h.S + 1e-9
            assert h.os_bytes <= peak / (1 - f) + p * (k + 1) * h.S + 1e-9
