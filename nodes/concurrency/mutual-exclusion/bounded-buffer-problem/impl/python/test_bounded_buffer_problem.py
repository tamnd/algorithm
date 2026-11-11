# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bounded-buffer-problem/. The authors are listed in prov/3ZSHF1.jsonl.
import pytest

from bounded_buffer_problem import build, no_error
from procsim import explore, random_run, replay


def all_items_once(s):
    """The goal: every process has finished and every item was taken once, in order per producer."""
    if not s.all_done():
        return False
    got = s.v["got"]
    for p in {x[0] for x in got}:
        mine = [x[1] for x in got if x[0] == p]
        if mine != sorted(mine) or len(set(mine)) != len(mine):
            return False
    return True


def test_semaphores_exhaustive():
    for producers, consumers, capacity in [(1, 1, 1), (1, 1, 2), (2, 1, 1), (1, 2, 2), (2, 2, 1), (2, 2, 2)]:
        res = explore(lambda: build("semaphores", capacity, producers, consumers, items=2),
                      goal=all_items_once, invariant=no_error)
        assert res.violations == [] and res.deadlocks == [] and not res.truncated, (producers, consumers)


def test_swapped_p_deadlocks():
    res = explore(lambda: build("semaphores", 1, 1, 1, items=2, swapped=True), stop_at_first=True)
    assert res.deadlocks
    sim = replay(lambda: build("semaphores", 1, 1, 1, items=2, swapped=True), res.deadlocks[0])
    # the buffer is full, the producer holds mutex and waits for empty,
    # and the consumer waits for mutex
    assert sim.procs["p0"].op == ("P", "empty") and sim.procs["c0"].op == ("P", "mutex")
    assert sim.sems["mutex"].count == 0 and sim.sems["empty"].count == 0


def test_without_mutex_one_producer_one_consumer_is_safe():
    res = explore(lambda: build("semaphores", 2, 1, 1, items=3, mutex=False),
                  goal=all_items_once, invariant=no_error)
    assert res.violations == [] and res.deadlocks == [] and not res.truncated


def test_without_mutex_two_producers_overwrite():
    res = explore(lambda: build("semaphores", 2, 2, 1, items=1, mutex=False), invariant=no_error,
                  stop_at_first=True)
    assert res.violations and "overwrites" in res.violations[0][1]


@pytest.mark.parametrize("mode", ["mesa", "hoare"])
def test_monitor_with_while_exhaustive(mode):
    for producers, consumers, capacity in [(1, 2, 1), (2, 1, 1), (1, 1, 2)]:
        res = explore(lambda: build("monitor", capacity, producers, consumers, items=2, mode=mode),
                      goal=all_items_once, invariant=no_error)
        assert res.violations == [] and res.deadlocks == [] and not res.truncated


def test_monitor_with_if_breaks_under_mesa():
    res = explore(lambda: build("monitor", 1, 1, 2, items=2, loop=False, mode="mesa"),
                  invariant=no_error, stop_at_first=True)
    assert res.violations and "empty slot" in res.violations[0][1]


def test_monitor_with_if_is_safe_under_hoare():
    for producers, consumers in [(1, 2), (2, 1)]:
        res = explore(lambda: build("monitor", 1, producers, consumers, items=2, loop=False, mode="hoare"),
                      goal=all_items_once, invariant=no_error)
        assert res.violations == [] and res.deadlocks == [] and not res.truncated


def test_sleep_and_wakeup_lose_a_wakeup():
    res = explore(lambda: build("sleep", 1, items=3), invariant=no_error)
    # a late wakeup, decided while the buffer held an item, can also wake the
    # consumer after the buffer is empty again, and it then takes from an empty slot
    assert any("empty slot" in msg for _, msg in res.violations)
    both =[d for d in res.deadlocks
            if all(p.op == ("_asleep",) for p in replay(lambda: build("sleep", 1, items=3), d).procs.values())]
    assert both  # the consumer sleeps with an item in the buffer, and the full buffer puts the producer to sleep
    shortest = min(both, key=len)  # the classic: c0 sees 0, p0 puts and its wakeup is lost, both sleep
    assert len(shortest) == 10
    assert replay(lambda: build("sleep", 1, items=3), shortest).v["count"] == 1


def test_seeded_larger_runs():
    for seed in range(20):
        for kind in ("semaphores", "monitor"):
            r = random_run(lambda: build(kind, 3, 3, 2, items=4), seed, goal=all_items_once,
                           invariant=no_error)
            assert r.outcome == "done", (kind, seed, r.outcome, r.message)
            assert len(r.sim.v["got"]) == 12
