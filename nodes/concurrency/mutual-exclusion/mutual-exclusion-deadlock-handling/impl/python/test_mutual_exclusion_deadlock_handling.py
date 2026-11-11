# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mutual-exclusion-deadlock-handling/. The authors are listed in prov/Z43BNF.jsonl.
import random

from mutual_exclusion_deadlock_handling import build, wait_edges
from procsim import explore, random_run

TWO = {"t1": ["x", "y"], "t2": ["y", "x"]}
THREE = {"t1": ["x", "y"], "t2": ["y", "z"], "t3": ["z", "x"]}
TS2 = {"t1": 1, "t2": 2}
TS3 = {"t1": 1, "t2": 2, "t3": 3}


def has_cycle(edges):
    g = {}
    for a, b in edges:
        g.setdefault(a, set()).add(b)
    state = {}

    def visit(v):
        state[v] = 1
        for w in g.get(v, ()):
            if state.get(w) == 1 or (w not in state and visit(w)):
                return True
        state[v] = 2
        return False

    return any(v not in state and visit(v) for v in list(g))


def check(rule):
    def inv(s):
        ts = s.v["ts"]
        for a, b in wait_edges(s):
            if rule == "wait-die" and not ts[a] < ts[b]:
                return f"{a} waits for an older {b}"
            if rule == "wound-wait" and not (ts[a] > ts[b] or s.v["wounded"][b]):
                return f"{a} waits for a younger {b} that is not wounded"
        return "cycle" if has_cycle(wait_edges(s)) else None
    return inv


def test_plain_waiting_deadlocks():
    assert explore(lambda: build(TWO, TS2, "wait")).deadlocks
    assert explore(lambda: build(THREE, TS3, "wait")).deadlocks


def test_exhaustive_two_by_two_is_deadlock_free():
    for rule in ("wait-die", "wound-wait"):
        res = explore(lambda: build(TWO, TS2, rule), invariant=check(rule))
        assert res.deadlocks == [] and res.violations == [] and not res.truncated
        assert res.finals == 1


def test_exhaustive_three_cycle_is_deadlock_free():
    for rule in ("wait-die", "wound-wait"):
        res = explore(lambda: build(THREE, TS3, rule), invariant=check(rule))
        assert res.deadlocks == [] and res.violations == [] and not res.truncated


def test_random_schedules_commit_everything():
    rng = random.Random(41)
    for rule in ("wait-die", "wound-wait"):
        aborts = 0
        for _ in range(150):
            n = rng.randint(2, 4)
            names = [f"t{i}" for i in range(n)]
            programs = {t: rng.sample("abcd", rng.randint(1, 3)) for t in names}
            ts = dict(zip(names, rng.sample(range(100), n)))
            r = random_run(lambda: build(programs, ts, rule), rng.randrange(10**6),
                           max_steps=5000, invariant=check(rule))
            assert r.outcome == "done", (rule, programs, r.outcome, r.message)
            assert sorted(e[1] for e in r.sim.log if e[0] == "commit") == sorted(names)
            aborts += sum(e[0] == "abort" for e in r.sim.log)
        assert aborts > 0


def test_who_is_aborted():
    # t1 (older) holds x; t2 (younger) holds y; then each asks for the other lock
    for rule, victim in (("wait-die", "t2"), ("wound-wait", "t2")):
        sim = build(TWO, TS2, rule)
        sim.step("t1")  # t1 takes x
        sim.step("t2")  # t2 takes y
        sim.step("t1")  # t1 asks for y, held by the younger t2
        sim.step("t2")  # t2 asks for x, held by the older t1
        if rule == "wait-die":
            assert sim.v["waiting"]["t1"] == "y"  # the older waits
        else:
            assert sim.v["wounded"]["t2"] is True  # the older wounds the younger
        for i in range(200):  # round robin; a scheduler that always picks t2 starves t1
            ready = sim.enabled()
            if not ready:
                break
            sim.step(ready[i % len(ready)])
        assert sim.all_done()
        aborted = [e[1] for e in sim.log if e[0] == "abort"]
        assert aborted and set(aborted) == {victim}
