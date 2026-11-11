# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/readers-writers-problem/. The authors are listed in prov/GNF11S.jsonl.
import pytest

from procsim import explore, random_run
from readers_writers_problem import build, exclusion


def advance(sim, p, pred):
    """Step only process p until pred(sim) holds."""
    while not pred(sim):
        assert sim.can_step(p), (p, sim.procs[p].op)
        sim.step(p)


def blocked(p):
    return lambda sim: not sim.can_step(p)


def reads_up(sim):
    target = sim.v["reads"] + 1
    return lambda s: s.v["reads"] == target


def writes_up(sim):
    target = sim.v["writes"] + 1
    return lambda s: s.v["writes"] == target


@pytest.mark.parametrize("policy", [1, 2, 3])
@pytest.mark.parametrize("readers,writers", [(2, 1), (1, 2)])
def test_exclusion_and_no_deadlock_exhaustive(policy, readers, writers):
    res = explore(lambda: build(policy, readers, writers, rounds=2), invariant=exclusion)
    assert res.violations == [] and res.deadlocks == [] and not res.truncated
    assert res.finals >= 1


@pytest.mark.parametrize("policy", [1, 2, 3])
def test_seeded_larger_runs(policy):
    for seed in range(20):
        r = random_run(lambda: build(policy, 3, 2, rounds=3), seed, invariant=exclusion)
        assert r.outcome == "done", (seed, r.outcome, r.message)
        assert r.sim.v["reads"] == 9 and r.sim.v["writes"] == 6


def test_problem_1_starves_the_writer():
    sim = build(1, 2, 1, rounds=40)
    advance(sim, "r0", reads_up(sim))  # r0 reads and holds w for the readers
    a, b = "r1", "r0"
    for _ in range(30):
        advance(sim, a, reads_up(sim))  # a enters while b still reads
        assert not sim.can_step("w0")
        advance(sim, b, reads_up(sim))  # b leaves and enters again: readcount never reaches 0
        assert not sim.can_step("w0")
        a, b = b, a
    assert sim.v["writes"] == 0 and sim.v["reads"] == 61
    assert sim.procs["w0"].op == ("P", "w")


def test_problem_2_starves_the_reader():
    sim = build(2, 1, 2, rounds=1, writer_rounds=20)
    advance(sim, "w0", writes_up(sim))  # writecount = 1 and w0 holds r
    advance(sim, "r0", blocked("r0"))
    assert sim.procs["r0"].op == ("P", "r")
    advance(sim, "w1", blocked("w1"))  # writecount = 2, w1 waits at P(w)
    a, b = "w0", "w1"
    for _ in range(15):
        advance(sim, a, lambda s: s.sems["w"].count == 1)  # a has written and released w
        advance(sim, b, writes_up(sim))
        advance(sim, a, blocked(a))  # a registers again before writecount reaches 0
        assert sim.v["writecount"] == 2 and not sim.can_step("r0")
        a, b = b, a
    assert sim.v["reads"] == 0 and sim.v["writes"] == 16


def test_weak_turnstile_starves_the_writer():
    sim = build(3, 2, 1, rounds=40, fifo=False)
    advance(sim, "r0", reads_up(sim))
    a, b = "r1", "r0"
    disabled_in_each_cycle = []
    for _ in range(30):
        seen_disabled = False
        target = sim.v["reads"] + 1
        while sim.v["reads"] != target:
            sim.step(a)
            seen_disabled |= not sim.can_step("w0")
        advance(sim, b, reads_up(sim))
        disabled_in_each_cycle.append(seen_disabled)
        a, b = b, a
    # w0 is enabled only now and then, so weak fairness does not force its step
    assert all(disabled_in_each_cycle)
    assert sim.v["writes"] == 0 and sim.procs["w0"].op == ("P", "turnstile")


def test_fifo_turnstile_bounds_the_bypass_exhaustive():
    def bounded(s):
        msg = exclusion(s)
        if msg:
            return msg
        if any(n > 2 for n in s.v["bypass"].values()):
            return f"bypass {s.v['bypass']}"
        return None

    res = explore(lambda: build(3, 2, 1, rounds=2, writer_rounds=1, fifo=True), invariant=bounded)
    assert res.violations == [] and res.deadlocks == [] and not res.truncated


def test_fifo_turnstile_writer_is_always_enabled_at_the_turnstile():
    sim = build(3, 2, 1, rounds=5, fifo=True)
    advance(sim, "r0", reads_up(sim))
    advance(sim, "r1", lambda s: s.procs["r1"].op == ("V", "turnstile"))
    assert sim.can_step("w0")  # a strong P only joins the queue
    sim.step("w0")
    reads_when_queued = sim.v["reads"]
    while sim.v["writes"] == 0:  # the adversary runs the readers whenever it can
        en = [p for p in sim.enabled() if p != "w0"] or ["w0"]
        sim.step(en[0])
    assert sim.v["reads"] - reads_when_queued <= 2
