# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/best-effort-htm/. The authors are listed in prov/W7DBTZ.jsonl.

import random

import pytest

from best_effort_htm import LOCK_BUSY, atomic
from htmsim import CAPACITY, CONFLICT, EXPLICIT, HTM, RETRY, Abort, explicit_code, serial_replay_ok
from sched import System, explore, random_run


def increment(addr):
    def body(v):
        x = v.load(addr)
        yield
        v.store(addr, x + 1)
        yield
    return body


def touch_all(addrs):
    def body(v):
        for a in addrs:
            v.store(a, v.load(a) + 1)
            yield
    return body


def transfer(src, dst):
    def body(v):
        a = v.load(src)
        yield
        b = v.load(dst)
        yield
        v.store(src, a - 1)
        yield
        v.store(dst, b + 1)
        yield
    return body


def audit(addrs):
    def body(v):
        total = 0
        for a in addrs:
            total += v.load(a)
            yield
        return total
    return body


def test_conflict_abort_status():
    h = HTM(2, {"x": 0}, read_cap=4, write_cap=4)
    h.begin(0)
    h.load(0, "x")
    h.begin(1)
    h.store(1, "x", 5)            # the requester wins
    with pytest.raises(Abort) as e:
        h.load(0, "x")
    assert e.value.status == CONFLICT | RETRY
    h.commit(1)
    assert h.mem["x"] == 5


def test_capacity_abort_status_even_alone():
    h = HTM(1, {i: 0 for i in range(5)}, read_cap=8, write_cap=4)
    h.begin(0)
    with pytest.raises(Abort) as e:
        for i in range(5):
            h.store(0, i, 1)
    assert e.value.status == CAPACITY          # no RETRY bit
    assert all(v == 0 for v in h.mem.values())
    h2 = HTM(1, {i: 0 for i in range(9)}, read_cap=8, write_cap=4)
    h2.begin(0)
    with pytest.raises(Abort) as e:
        for i in range(9):
            h2.load(0, i)
    assert e.value.status == CAPACITY


def test_explicit_abort_and_interrupt():
    h = HTM(1, {"x": 0})
    h.begin(0)
    h.store(0, "x", 3)
    with pytest.raises(Abort) as e:
        h.abort(0, 0x42)
    assert e.value.status & EXPLICIT and explicit_code(e.value.status) == 0x42
    assert not e.value.status & RETRY and h.mem["x"] == 0
    h.begin(0)
    h.interrupt(0)
    with pytest.raises(Abort) as e:
        h.commit(0)
    assert e.value.status == 0


def test_plain_store_aborts_a_reader():
    h = HTM(2, {"x": 0})
    h.begin(0)
    h.load(0, "x")
    h.store(1, "x", 1)            # an ordinary store from processor 1
    with pytest.raises(Abort) as e:
        h.commit(0)
    assert e.value.status & CONFLICT


def test_hardware_only_retry_never_finishes_a_large_block():
    # Without a fallback, a block larger than the write buffer aborts every time.
    h = HTM(1, {i: 0 for i in range(6)}, write_cap=4)
    for _ in range(100):
        h.begin(0)
        try:
            for i in range(6):
                h.store(0, i, 1)
            h.commit(0)
            break
        except Abort as e:
            assert e.status == CAPACITY
    assert h.stats["commit"] == 0 and h.stats["capacity"] == 100


def test_fallback_gives_progress_on_all_interleavings():
    # Two processors increment a counter. In the second case the HTM can
    # never commit (a read capacity of 0), so only the lock path works.
    for read_cap in (4, 0):
        def make():
            h = HTM(2, {"L": 0, "c": 0}, read_cap=read_cap, write_cap=4)
            return h, [atomic(h, p, "L", increment("c"), tries=1) for p in range(2)]

        n = 0
        for h, sys in explore(make):
            n += 1
            assert sys.finished() and sys.error == [None, None]
            assert h.mem == {"L": 0, "c": 2}
            if read_cap == 0:
                assert [r[1] for r in sys.result] == ["lock", "lock"]
        assert n > 10


def test_capacity_goes_to_the_lock_at_once():
    log = []
    h = HTM(1, {"L": 0, **{i: 0 for i in range(6)}}, read_cap=16, write_cap=4)
    sys = System([atomic(h, 0, "L", touch_all(range(6)), tries=5, log=log)])
    while sys.runnable():
        sys.step(0)
    assert sys.result[0][1] == "lock"
    assert log == [CAPACITY]                   # one try, then the lock
    assert all(h.mem[i] == 1 for i in range(6))


def test_lock_holder_aborts_subscribed_transactions():
    h = HTM(2, {"L": 0, "x": 0})
    h.begin(0)
    assert h.load(0, "L") == 0                 # processor 0 subscribes to the lock
    assert h.cas(1, "L", 0, 1)                 # processor 1 takes the lock
    with pytest.raises(Abort) as e:
        h.load(0, "x")
    assert e.value.status & CONFLICT
    log = []
    sys = System([atomic(h, 0, "L", increment("x"), tries=2, log=log)])
    sys.step(0)                                # waits: the lock is taken
    assert sys.runnable() == []
    h.mem["L"] = 0                             # the holder releases it
    while sys.runnable():
        sys.step(0)
    assert sys.result[0] == (None, "htm") and log == []
    h.cas(1, "L", 0, 1)
    h.begin(0)
    assert h.load(0, "L") == 1
    with pytest.raises(Abort) as e:
        h.abort(0, LOCK_BUSY)
    assert explicit_code(e.value.status) == LOCK_BUSY


def test_random_runs_progress_and_atomicity():
    rng = random.Random(2024)
    accounts = ["a", "b", "c", "d"]
    paths = {"htm": 0, "lock": 0}
    for _ in range(600):
        seed = rng.random()

        def make():
            r = random.Random(seed)
            init = {"L": 0, **{a: 10 for a in accounts}}
            h = HTM(4, init, read_cap=r.choice([2, 4, 8]), write_cap=r.choice([1, 2, 4]))
            procs = []
            for p in range(4):
                if r.random() < 0.3:
                    procs.append(atomic(h, p, "L", audit(accounts), tries=r.choice([1, 3])))
                else:
                    s, d = r.sample(accounts, 2)
                    procs.append(atomic(h, p, "L", transfer(s, d), tries=r.choice([1, 3])))
            return (h, init), procs

        (h, init), sys = random_run(make, rng)
        assert sys.finished() and all(e is None for e in sys.error)
        assert h.mem["L"] == 0
        assert sum(h.mem[a] for a in accounts) == 40
        assert serial_replay_ok(init, h.history, h.mem)
        for res in sys.result:
            paths[res[1]] += 1
            if res[0] is not None:
                assert res[0] == 40                # every audit saw a consistent state
    assert paths["htm"] > 100 and paths["lock"] > 100
