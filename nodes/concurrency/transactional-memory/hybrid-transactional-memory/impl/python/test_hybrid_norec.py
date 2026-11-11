# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-transactional-memory/. The authors are listed in prov/932XZC.jsonl.

import random

from htmsim import HTM
from hybrid_norec import HWC, SEQ, atomic
from sched import System, explore_bounded, random_run


def increment(a):
    def body(v):
        x = yield from v.read(a)
        yield from v.write(a, x + 1)
    return body


def transfer(src, dst, count=None):
    def body(v):
        a = yield from v.read(src)
        b = yield from v.read(dst)
        yield from v.write(src, a - 1)
        yield from v.write(dst, b + 1)
        if count is not None:
            n = yield from v.read(count)
            yield from v.write(count, n + 1)
    return body


def audit(addrs):
    def body(v):
        total = 0
        for a in addrs:
            total += yield from v.read(a)
        return total
    return body


def mem(**data):
    return {SEQ: 0, HWC: 0, **data}


def pair(first, second, tries, **flags):
    """Two processors; tries gives the hardware tries of each (0 = software)."""
    def make():
        h = HTM(2, mem(a=10, b=10, c=0))
        return h, [atomic(h, 0, first, tries=tries[0], **flags),
                   atomic(h, 1, second, tries=tries[1], **flags)]
    return make


def outcomes(make, k):
    """Run every schedule with at most k preemptions; count the bad ends."""
    n = bad = 0
    for h, sys in explore_bounded(make, k):
        n += 1
        assert sys.finished() and sys.error == [None, None]
        audits = [r[0] for r in sys.result if r[0] is not None]
        if h.mem["a"] + h.mem["b"] != 20 or any(t != 20 for t in audits):
            bad += 1
        elif h.mem["c"] not in (0, 2):
            bad += 1
    return n, bad


CASES = [
    (transfer("a", "b"), audit(["a", "b"]), (0, 1)),   # software writer, hardware reader
    (transfer("a", "b"), audit(["a", "b"]), (1, 0)),   # hardware writer, software reader
    (increment("c"), increment("c"), (0, 1)),          # one of each on one word
    (increment("c"), increment("c"), (0, 0)),          # NOrec alone
    (transfer("a", "b"), transfer("b", "a"), (1, 0)),
]


def test_every_schedule_with_up_to_4_preemptions_is_correct():
    total = 0
    for first, second, tries in CASES:
        n, bad = outcomes(pair(first, second, tries), 4)
        assert bad == 0
        total += n
    assert total > 10_000


def test_hardware_that_does_not_subscribe_sees_a_half_written_state():
    n, bad = outcomes(pair(transfer("a", "b"), audit(["a", "b"]), (0, 1), subscribe=False), 2)
    assert bad > 0
    # The run found by the search: the software writer has stored a = 9 and
    # not yet b; the hardware audit reads both and commits 19.
    h = HTM(2, mem(a=10, b=10, c=0))
    sys = System([atomic(h, 0, transfer("a", "b"), tries=0),
                  atomic(h, 1, audit(["a", "b"]), tries=1, subscribe=False)])
    for p in [1, 1] + [0] * 14 + [1, 1, 1, 1] + [0] * 3:
        sys.step(p)
    assert sys.finished() and sys.result[1] == (19, "hw")


def test_software_that_ignores_the_hardware_counter_sees_two_states():
    n, bad = outcomes(pair(transfer("a", "b"), audit(["a", "b"]), (1, 0), watch_hw=False), 2)
    assert bad > 0
    # The software audit reads a = 10; a hardware transfer commits without
    # changing SEQ; the audit reads b = 11 and returns 21.
    h = HTM(2, mem(a=10, b=10, c=0))
    sys = System([atomic(h, 0, transfer("a", "b"), tries=1, watch_hw=False),
                  atomic(h, 1, audit(["a", "b"]), tries=0, watch_hw=False)])
    for p in [0] * 4 + [1] * 5 + [0] * 6 + [1] * 3:
        sys.step(p)
    assert sys.finished() and sys.result == [(None, "hw"), (21, "sw")]
    n, bad = outcomes(pair(increment("c"), increment("c"), (0, 1), watch_hw=False), 2)
    assert bad > 0                     # and an increment can be lost


def test_same_schedule_with_the_counter_is_correct():
    # The audit sees HWC change right after it loads a. Its read set is still
    # empty, so validation passes at once, and it loads a again (now 9).
    h = HTM(2, mem(a=10, b=10, c=0))
    stats = {}
    sys = System([atomic(h, 0, transfer("a", "b"), tries=1),
                  atomic(h, 1, audit(["a", "b"]), tries=0, stats=stats)])
    for p in [0] * 4 + [1] * 5 + [0] * 6:
        sys.step(p)
    while not sys.finished():
        sys.step(sys.runnable()[0])
    assert sys.result == [(None, "hw"), (20, "sw")]
    assert stats == {} and h.mem[HWC] == 1
    # Later in the audit, after a is in its read set: a restart.
    h = HTM(2, mem(a=10, b=10, c=0))
    sys = System([atomic(h, 0, transfer("a", "b"), tries=1),
                  atomic(h, 1, audit(["a", "b"]), tries=0, stats=stats)])
    sys.step(0)
    for _ in range(6):
        sys.step(1)                    # the audit has read a = 10 and checked
    while not sys.done[0]:
        sys.step(0)                    # the hardware transfer commits
    while not sys.finished():
        sys.step(1)
    assert sys.result == [(None, "hw"), (20, "sw")]
    assert stats == {"restarts": 1}


def test_three_processors_two_preemptions():
    def make():
        h = HTM(3, mem(a=10, b=10, c=0))
        return h, [atomic(h, 0, transfer("a", "b"), tries=0),
                   atomic(h, 1, transfer("b", "a"), tries=1),
                   atomic(h, 2, audit(["a", "b"]), tries=1)]
    n = 0
    for h, sys in explore_bounded(make, 2):
        n += 1
        assert sys.finished() and h.mem["a"] == 10 and h.mem["b"] == 10
        assert sys.result[2][0] == 20
    assert n > 500


def test_random_runs_mixed_paths():
    rng = random.Random(2011)
    accounts = ["a", "b", "c", "d"]
    paths = {"hw": 0, "sw": 0}
    for _ in range(600):
        seed = rng.random()

        def make():
            r = random.Random(seed)
            init = mem(n=0, **{x: 10 for x in accounts})
            h = HTM(4, init, read_cap=r.choice([3, 6, 8]), write_cap=r.choice([2, 4]))
            procs, transfers = [], 0
            for p in range(4):
                if r.random() < 0.3:
                    body = audit(accounts)
                else:
                    body = transfer(*r.sample(accounts, 2), count="n")
                    transfers += 1
                procs.append(atomic(h, p, body, tries=r.choice([0, 1, 3])))
            return (h, transfers), procs

        (h, transfers), sys = random_run(make, rng)
        assert sys.finished() and all(e is None for e in sys.error)
        assert h.mem[SEQ] % 2 == 0
        assert sum(h.mem[x] for x in accounts) == 40
        assert h.mem["n"] == transfers           # no update was lost
        for res in sys.result:
            paths[res[1]] += 1
            if res[0] is not None:
                assert res[0] == 40
    assert paths["hw"] > 100 and paths["sw"] > 100
