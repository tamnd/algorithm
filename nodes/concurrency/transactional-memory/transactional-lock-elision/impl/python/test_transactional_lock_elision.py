# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transactional-lock-elision/. The authors are listed in prov/70FJV6.jsonl.

import random

from htmsim import HTM, serial_replay_ok
from sched import System, explore, random_run
from transactional_lock_elision import elide, hold_lock


def increment(addr):
    def body(v):
        x = v.load(addr)
        yield
        v.store(addr, x + 1)
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


def two_increments(subscribe):
    """Processor 0 takes the lock (tries=0); processor 1 elides it."""
    def make():
        h = HTM(2, {"L": 0, "c": 0})
        return h, [elide(h, 0, "L", increment("c"), tries=0),
                   elide(h, 1, "L", increment("c"), tries=1, subscribe=subscribe)]
    return make


def test_without_reading_the_lock_an_update_is_lost():
    finals = set()
    for h, sys in explore(two_increments(subscribe=False)):
        assert sys.finished() and sys.error == [None, None]
        finals.add(h.mem["c"])
    assert finals == {1, 2}            # some interleaving loses an increment


def test_reading_the_lock_makes_every_interleaving_correct():
    n = 0
    for h, sys in explore(two_increments(subscribe=True)):
        n += 1
        assert sys.finished() and sys.error == [None, None]
        assert h.mem == {"L": 0, "c": 2}
    assert n > 10


def test_the_wrong_run_step_by_step():
    # P0 holds the lock and reads c; P1 commits c = 1 inside its
    # transaction; P0 writes c = 1 over it.
    h = HTM(2, {"L": 0, "c": 0})
    sys = System([elide(h, 0, "L", increment("c"), tries=0),
                  elide(h, 1, "L", increment("c"), tries=1, subscribe=False)])
    for p in [0, 0]:                   # P0: CAS the lock, then read c = 0
        sys.step(p)
    assert h.mem["L"] == 1
    while not sys.done[1]:
        sys.step(1)                    # P1 ignores the lock and commits
    assert sys.result[1] == (None, "htm") and h.mem["c"] == 1
    while not sys.done[0]:
        sys.step(0)
    assert h.mem["c"] == 1             # one increment is lost


def test_capacity_abort_goes_to_the_lock_without_more_tries():
    stats = {}
    h = HTM(1, {"L": 0, **{i: 0 for i in range(6)}}, read_cap=16, write_cap=4)

    def body(v):
        for i in range(6):
            v.store(i, 1)
            yield

    sys = System([elide(h, 0, "L", body, tries=5, stats=stats)])
    while sys.runnable():
        sys.step(0)
    assert sys.result[0][1] == "lock"
    assert stats == {"aborts": 1, "locked": 1}
    assert h.stats["capacity"] == 1


def test_lemming_effect_step_by_step():
    for wait, path in ((False, "lock"), (True, "htm")):
        h = HTM(2, {"L": 0, "x": 0, "y": 0})
        stats = {}
        sys = System([hold_lock(h, 0, "L", increment("x")),
                      elide(h, 1, "L", increment("y"), tries=3, wait=wait, stats=stats)])
        sys.step(0)                    # P0 takes the lock
        while 1 in sys.runnable():
            sys.step(1)                # P1 runs as far as it can
        while not sys.finished():
            sys.step(sys.runnable()[0])
        assert sys.result[1][1] == path
        assert stats.get("aborts", 0) == (3 if not wait else 0)
        assert h.mem == {"L": 0, "x": 1, "y": 1}


def test_random_runs_correct_and_lemming_counts():
    # One thread always takes the lock; three threads elide it. The data are
    # disjoint, so every abort and every fallback comes from the lock alone.
    # The holder can abort an elider once (its CAS on the lock), so with at
    # least 2 tries a waiting elider always commits in hardware.
    rng = random.Random(70)
    fallbacks = {False: 0, True: 0}
    for i in range(600):
        wait = bool(i % 2)
        seed = rng.random()

        def make():
            r = random.Random(seed)
            mem = {"L": 0, "h": 0, "a": 0, "b": 0, "c": 0}
            h = HTM(4, mem)
            stats = {}
            procs = [hold_lock(h, 0, "L", increment("h"))]
            for p, a in zip((1, 2, 3), "abc"):
                procs.append(elide(h, p, "L", increment(a), tries=r.choice([2, 3]),
                                   wait=wait, stats=stats))
            return (h, mem, stats), procs

        (h, mem, stats), sys = random_run(make, rng)
        assert sys.finished() and all(e is None for e in sys.error)
        assert h.mem == {"L": 0, "h": 1, "a": 1, "b": 1, "c": 1}
        assert serial_replay_ok(mem, h.history, h.mem)
        fallbacks[wait] += stats.get("locked", 0)
    assert fallbacks[True] == 0        # waiting first: the lock is never needed
    assert fallbacks[False] > 100      # retrying at once: many lemmings


def test_random_transfers_and_audits():
    rng = random.Random(2001)
    accounts = ["a", "b", "c", "d"]
    paths = {"htm": 0, "lock": 0}
    for _ in range(500):
        seed = rng.random()

        def make():
            r = random.Random(seed)
            init = {"L": 0, **{a: 10 for a in accounts}}
            h = HTM(4, init, read_cap=r.choice([3, 5, 8]), write_cap=r.choice([1, 2, 4]))
            procs = []
            for p in range(4):
                if r.random() < 0.3:
                    body = audit(accounts)
                else:
                    body = transfer(*r.sample(accounts, 2))
                if r.random() < 0.2:
                    procs.append(hold_lock(h, p, "L", body))
                else:
                    procs.append(elide(h, p, "L", body, tries=r.choice([1, 3]),
                                       wait=r.random() < 0.5))
            return (h, init), procs

        (h, init), sys = random_run(make, rng)
        assert sys.finished() and all(e is None for e in sys.error)
        assert h.mem["L"] == 0 and sum(h.mem[a] for a in accounts) == 40
        assert serial_replay_ok(init, h.history, h.mem)
        for res in sys.result:
            paths[res[1]] += 1
            if res[0] is not None:
                assert res[0] == 40    # every audit saw a consistent state
    assert paths["htm"] > 100 and paths["lock"] > 100


def test_random_runs_without_subscription_find_errors():
    rng = random.Random(11)
    bad = 0
    for _ in range(300):
        seed = rng.random()

        def make():
            r = random.Random(seed)
            init = {"L": 0, "a": 10, "b": 10}
            h = HTM(3, init)
            procs = [hold_lock(h, 0, "L", transfer("a", "b"))]
            for p in (1, 2):
                body = audit(["a", "b"]) if r.random() < 0.5 else transfer("b", "a")
                procs.append(elide(h, p, "L", body, subscribe=False))
            return h, procs

        h, sys = random_run(make, rng)
        assert sys.finished()
        wrong_audit = any(res[0] is not None and res[0] != 20 for res in sys.result)
        if wrong_audit or h.mem["a"] + h.mem["b"] != 20:
            bad += 1
    assert bad > 0
