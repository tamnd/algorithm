# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deadlock-prevention/. The authors are listed in prov/KAC40H.jsonl.
import random

from deadlock_prevention import build, has_cycle, naive, one_shot, ordered, release_and_retry
from procsim import explore, random_run, replay


def held(sim, name):
    return [m for m, mx in sim.mutexes.items() if mx.owner == name]


def test_naive_can_deadlock():
    res = explore(lambda: build(naive))
    assert res.deadlocks and not res.truncated
    sim = replay(lambda: build(naive), list(res.deadlocks[0]))
    assert has_cycle(sim.waits_for())
    assert all(len(held(sim, p)) == 1 for p in "pqs")  # each holds one and waits


def test_one_shot_never_deadlocks_and_never_holds_while_waiting():
    def hold_and_wait(sim):
        for p in sim.blocked():
            if held(sim, p):
                return f"{p} waits while holding"
        return None

    res = explore(lambda: build(one_shot), invariant=hold_and_wait)
    assert res.deadlocks == [] and res.violations == [] and res.finals == 1 and not res.truncated


def test_ordered_never_deadlocks_and_the_wait_for_graph_stays_acyclic():
    res = explore(lambda: build(ordered), invariant=lambda s: "cycle" if has_cycle(s.waits_for()) else None)
    assert res.deadlocks == [] and res.violations == [] and res.finals == 1 and not res.truncated


def test_release_and_retry_never_deadlocks_but_can_livelock():
    res = explore(lambda: build(release_and_retry))
    assert res.deadlocks == [] and res.finals == 1 and not res.truncated
    # a round robin schedule in lock step returns to the start state with no progress
    sim = build(release_and_retry)
    keys = []
    for _ in range(3):
        for _ in range(3):
            for p in "pqs":
                sim.step(p)
        keys.append(sim.key())
    assert keys[0] == keys[1] == keys[2] and not sim.log
    # random schedules do finish
    for seed in range(50):
        r = random_run(lambda: build(release_and_retry), seed, max_steps=2000)
        assert r.outcome == "done"


def test_random_runs_of_the_naive_version_find_the_deadlock():
    outcomes = {random_run(lambda: build(naive), seed).outcome for seed in range(200)}
    assert outcomes == {"done", "deadlock"}


def test_seeded_random_schedules_of_the_fixes_always_finish():
    rng = random.Random(6)
    for proc in (one_shot, ordered, release_and_retry):
        for _ in range(100):
            r = random_run(lambda: build(proc), rng.randrange(10**6), max_steps=2000)
            assert r.outcome == "done" and sorted(e[1] for e in r.sim.log) == ["p", "q", "s"]
