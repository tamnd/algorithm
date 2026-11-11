# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flat-combining/. The authors are listed in prov/E3Q27Y.jsonl.

import random

from explorer import Memory, Run, Stats, program, random_run, replay
from flat_combining import FlatCombining
from lincheck import StackSpec, lin_check, linearize


def make(procs, objs=None, **flags):
    def setup():
        mem = Memory()
        fc = FlatCombining(mem, len(procs), **flags)
        if objs is not None:
            objs[:] = [fc]
        return mem, [program(fc.handle(p), ops) for p, ops in enumerate(procs)]

    return setup


def results(run, p=None):
    return [ev[2] for ev in run.history if ev[1] == "res" and (p is None or ev[0] == p)]


def frame_key(g):
    """The local state of a generator chain: the position and the simple locals of each frame."""
    out = []
    while g is not None:
        f = g.gi_frame
        if f is None:
            out.append(None)
            break
        loc = tuple(sorted((k, v) for k, v in f.f_locals.items()
                           if isinstance(v, (int, str, tuple, bool, float, type(None)))))
        out.append((f.f_lasti, loc))
        g = g.gi_yieldfrom
    return tuple(out)


def explore_with_frames(setup, check, max_steps=400):
    """Like explorer.explore, but a state is the memory, the history and the
    local state of each process (not the list of all values it has read).
    A spin that reads the same values again then returns to a state seen
    before, so the search ends although a waiter may spin for ever."""
    stats = Stats()
    seen = set()
    stack = [()]
    while stack:
        prefix = stack.pop()
        run = replay(setup, prefix)
        sched = list(prefix)
        while True:
            en = run.enabled()
            if not en or len(sched) >= max_steps:
                stats.runs += 1
                msg = check(run, bool(en))
                if msg:
                    stats.failure = (msg, sched)
                    return stats
                break
            k = (run.mem.key(), tuple(run.history), tuple(run.deferred), tuple(run.pending),
                 tuple(frame_key(g) for g in run.procs))
            if k in seen:
                break
            seen.add(k)
            stats.states += 1
            for p in reversed(en[1:]):
                stack.append(tuple(sched) + (p,))
            run.step(en[0])
            sched.append(en[0])
    return stats


def test_random_sequential_against_a_stack() -> None:
    rng = random.Random(3)
    ops, model, want = [], [], []
    for _ in range(200):
        if rng.random() < 0.5:
            x = rng.randrange(100)
            ops.append(("push", x))
            model.append(x)
            want.append(None)
        else:
            ops.append(("pop",))
            want.append(model.pop() if model else "EMPTY")
    objs = []
    run = Run(make([ops], objs=objs, cleanup_every=1, max_age=0))
    assert run.finish(0, limit=100000)
    assert results(run) == want
    assert objs[0].data() == tuple(model)


CASES = [
    ([[("push", 1)], [("pop",)]], {}),
    ([[("push", 1), ("pop",)], [("push", 2)]], {}),
    ([[("push", 1), ("pop",)], [("pop",), ("push", 2)]], {"cleanup_every": 1, "max_age": 0}),
]


def test_exhaustive_small_cases() -> None:
    # The third case removes and adds records again in many of its runs.
    for procs, flags in CASES:
        st = explore_with_frames(make(procs, **flags), lin_check(StackSpec()))
        assert st.failure is None, (procs, st.failure)
        assert st.runs > 5


def test_three_threads_seeded() -> None:
    # Three threads have too many states to visit all of them.
    procs = [[("push", 1)], [("push", 2)], [("pop",), ("pop",)]]
    for seed in range(300):
        run = random_run(make(procs, cleanup_every=1, max_age=0), seed, max_steps=5000)
        assert all(op is None for op in run.pending), seed
        assert linearize(run.history, StackSpec()) is not None, seed


def test_one_pass_serves_everybody() -> None:
    # p0 takes the lock and stops. p1 and p2 publish and wait. p0's one
    # combining pass then serves all three requests, and p1 and p2 return
    # after two more reads (active and slot).
    procs = [[("push", 1)], [("push", 2)], [("push", 3)]]
    objs = []
    run = Run(make(procs, objs=objs))
    run.until(0, lambda op: op[0] == "read" and op[1] == "count")
    for p in (1, 2):
        run.until(p, lambda op: op[0] == "read" and op[1] == "lock")
        run.step(p)
    run.finish(0)
    for p in (1, 2):
        assert run.finish_op(p) == 2
    assert sorted(objs[0].data()) == [1, 2, 3]


def test_the_combiner_must_read_its_own_record() -> None:
    # p0 pushes 1, reads its record (not served yet), and stops before it
    # tries the lock. p1 combines and serves both pushes. p0 then gets the
    # lock. With own_first, p0 pushes 1 a second time.
    procs = [[("push", 1)], [("push", 2), ("pop",), ("pop",), ("pop",)]]
    for bug in (False, True):
        objs = []
        run = Run(make(procs, objs=objs, own_first=bug))
        run.until(0, lambda op: op[0] == "read" and op[1] == "lock")
        run.finish_op(1)
        run.finish(0)
        run.finish(1)
        assert results(run, 1) == ([None, 1, 1, 2] if bug else [None, 1, 2, "EMPTY"])
        assert (linearize(run.history, StackSpec()) is None) == bug
    st = explore_with_frames(make(procs, own_first=True), lin_check(StackSpec()))
    assert st.failure is not None


def test_it_blocks_when_the_combiner_stops() -> None:
    # p0 stops while it holds the lock. p1 and p2 spin for ever: flat
    # combining is blocking.
    procs = [[("push", 1)], [("push", 2)], [("pop",)]]
    run = Run(make(procs))
    run.until(0, lambda op: op[0] == "read" and op[1] == "count")
    assert not run.finish(1, limit=3000)
    assert not run.finish(2, limit=3000)
    run.finish(0)
    assert run.finish(1) and run.finish(2)


def test_solo_cost() -> None:
    # Alone, with R records in the list (its own included), an operation
    # costs 1 (publish) + 2 (active, slot) + 2 (lock) + 3 (count, data)
    # + 1 (head) + 2 per record + 2 (serve its own request) + 1 (data)
    # + 1 (unlock) + 2 (active, slot) = 15 + 2 R steps, and 4 more when its
    # record is not in the list. A cleanup pass costs at most 3 more per
    # record.
    for nprocs in (1, 2, 4, 8):
        procs = [[("push", 1)] for _ in range(nprocs)]
        objs = []
        run = Run(make(procs, objs=objs, cleanup_every=10**9))
        for p in range(nprocs):
            r = len(objs[0].list_records()) + 1
            assert run.finish_op(p) == 15 + 2 * r + 4
        procs = [[("push", 1), ("pop",), ("push", 2)]] + [[("push", 0)] for _ in range(nprocs - 1)]
        run = Run(make(procs, objs=objs, cleanup_every=1, max_age=0))
        for p in range(1, nprocs):
            run.finish(p)
        for _ in range(3):
            r = len(objs[0].list_records()) + 1
            assert run.finish_op(0) <= 19 + 5 * r, (nprocs, r)


def test_seeded_runs() -> None:
    for seed in range(100):
        rng = random.Random(seed)
        procs = [[("push", rng.randrange(9)) if rng.random() < 0.5 else ("pop",) for _ in range(4)] for _ in range(3)]
        flags = {"cleanup_every": 1 + seed % 3, "max_age": seed % 2}
        run = random_run(make(procs, **flags), seed, max_steps=20000)
        assert all(op is None for op in run.pending), seed
        assert linearize(run.history, StackSpec()) is not None, seed
