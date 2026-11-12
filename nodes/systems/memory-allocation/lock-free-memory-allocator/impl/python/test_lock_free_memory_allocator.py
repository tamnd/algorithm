# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lock-free-memory-allocator/. The authors are listed in prov/9J5R6H.jsonl.

import random

from lock_free_memory_allocator import ACTIVE, EMPTY, FULL, PARTIAL, LockFreeAllocator, Run, random_run


def check_quiescent(a: LockFreeAllocator, r: Run) -> None:
    """With no operation in progress, every block is on its free list or held, once."""
    assert not r.current
    assert not r.double and not a.errors
    reserved = {}
    for h in a.heaps:
        if h.active is not None:
            d, credits = h.active
            assert d not in reserved and credits >= 0
            reserved[d] = credits + 1
    slots = [h.partial for h in a.heaps if h.partial is not None] + list(a.sc_partial)
    for sb, d in a.descs.items():
        held = {b[1] for b in r.owner if b[0] == sb}
        if sb in a.freed:
            assert not held and d not in reserved
            assert d not in slots or d.anchor.state == EMPTY
            continue
        anchor = d.anchor
        seen = []
        i = anchor.avail
        for _ in range(anchor.count + reserved.get(d, 0)):
            assert 0 <= i < d.maxcount and i not in seen and i not in held
            seen.append(i)
            i = a.mem[(sb, i)]
        assert len(seen) + len(held) == d.maxcount, "a block is lost or counted twice"
        if d in reserved:
            assert anchor.state == ACTIVE and d not in slots
        else:
            assert anchor.state in (FULL, PARTIAL)
        if anchor.state == PARTIAL:
            assert slots.count(d) == 1 and anchor.count >= 1
        if anchor.state == FULL:
            assert anchor.count == 0 and d not in slots
    for sb in a.freed:
        assert not any(b[0] == sb for b in r.owner)


def aba_schedule(use_tag: bool) -> tuple[LockFreeAllocator, Run]:
    """The scenario of Section 3.2.3: X is delayed between reading next and its CAS."""
    a = LockFreeAllocator(nheaps=1, maxcount=8, maxcredits=2, use_tag=use_tag)
    r = Run(a, 2)
    X, Y = 0, 1
    r.start(Y, "malloc")
    r.finish(Y)  # new superblock: Y gets block 0, Active has 2 reserved blocks
    assert r.held[Y] == [(0, 0)] and a.heaps[0].active[1] == 1
    r.start(X, "malloc")
    for _ in range(5):  # X takes a credit, reads Anchor (avail 1) and next = 2, then stops before its CAS
        r.step(X)
    for _ in range(2):  # Y pops block 1 and block 2
        r.start(Y, "malloc")
        r.finish(Y)
    assert r.held[Y] == [(0, 0), (0, 1), (0, 2)]
    for b in [(0, 0), (0, 1)]:  # Y frees 0 then 1: avail and count are as X read them
        r.start(Y, "free", b)
        r.finish(Y)
    assert a.descs[0].anchor[:3] == (1, 5, ACTIVE)
    r.finish(X)
    r.start(Y, "malloc")
    r.finish(Y)
    return a, r


def test_example_trace() -> None:
    a, r = aba_schedule(use_tag=True)
    assert r.held[0] == [(0, 1)] and r.held[1] == [(0, 2), (0, 0)]
    assert a.descs[0].anchor == (3, 3, ACTIVE, 4)
    assert a.cas_fail == 1 and not r.double
    r.start(0, "free", (0, 1))
    r.finish(0)
    check_quiescent(a, r)


def test_aba_without_tag() -> None:
    a, r = aba_schedule(use_tag=False)
    assert r.held[0] == [(0, 1)]
    assert r.double == [(0, 2)], "without the tag, block 2 is handed out while Y holds it"


def test_states_and_superblock_return() -> None:
    a = LockFreeAllocator(nheaps=1, maxcount=4, maxcredits=2)
    r = Run(a, 1)
    for _ in range(4):
        r.start(0, "malloc")
        r.finish(0)
    d = a.descs[0]
    assert d.anchor.state == FULL and a.heaps[0].active is None
    r.start(0, "free", (0, 2))
    r.finish(0)
    assert d.anchor.state == PARTIAL and a.heaps[0].partial is d  # first free to a FULL superblock
    check_quiescent(a, r)
    for b in [(0, 0), (0, 1), (0, 3)]:
        r.start(0, "free", b)
        r.finish(0)
    assert d.anchor.state == EMPTY and 0 in a.freed and a.heaps[0].partial is None
    check_quiescent(a, r)


def test_random_schedules() -> None:
    rng = random.Random(1)
    for seed in range(600):
        a = LockFreeAllocator(
            nheaps=rng.randint(1, 3), maxcount=rng.randint(2, 7), maxcredits=rng.randint(1, 4), use_tag=True
        )
        r = random_run(a, rng.randint(2, 4), rng.randint(5, 25), seed)
        check_quiescent(a, r)
        for t in list(r.held):  # free everything: every superblock goes back
            for b in list(r.held[t]):
                r.start(t, "free", b)
                r.finish(t)
        check_quiescent(a, r)
        assert all(sb in a.freed or a.descs[sb].anchor.state in (ACTIVE, PARTIAL) for sb in a.descs)


def test_crashed_thread_does_not_block_others() -> None:
    rng = random.Random(2)
    for seed in range(300):
        a = LockFreeAllocator(nheaps=rng.randint(1, 2), maxcount=rng.randint(2, 6), maxcredits=rng.randint(1, 3))
        n = rng.randint(2, 4)
        r = random_run(a, n, 15, seed, crash=0)
        assert all(r.done[t] == 15 for t in range(1, n)), "a stopped thread must not stop the others"
        assert not r.double and not a.errors
