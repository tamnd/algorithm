# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/condition-variable/. The authors are listed in prov/TSEGXF.jsonl.
import pytest

from condition_variable import CORRECT, build_buffer, build_flag, safe
from procsim import explore, random_run, replay


def no_errors(res):
    return res.violations == [] and res.deadlocks == [] and not res.truncated


@pytest.mark.parametrize("impl", CORRECT)
@pytest.mark.parametrize("how", ["signal", "broadcast"])
def test_flag_correct(impl, how):
    # signal wakes one waiter, so it is only enough when one thread waits for the flag;
    # a late thread with another predicate would need broadcast
    waiters, late = (2, True) if how == "broadcast" else (1, False)
    res = explore(lambda: build_flag(impl, waiters, how, late=late), invariant=safe)
    assert no_errors(res), (res.deadlocks[:1], res.violations[:1])


@pytest.mark.parametrize("impl", CORRECT)
def test_buffer_two_conditions_signal_while(impl):
    for kw in (dict(producers=1, consumers=2), dict(producers=2, consumers=2), dict(producers=1, consumers=1, items=2)):
        res = explore(lambda: build_buffer(impl, **kw), invariant=safe)
        assert no_errors(res), (kw, res.deadlocks[:1], res.violations[:1])


def test_mesa_if_takes_from_empty_buffer():
    # c0 waits; the producer puts an item and signals; c1 gets the mutex first and
    # takes the item; c0 runs later and, with `if`, does not test again
    res = explore(lambda: build_buffer("native", loop=False), invariant=safe, stop_at_first=True)
    assert res.violations and "out of range" in res.violations[0][1]
    assert no_errors(explore(lambda: build_buffer("native", loop=True), invariant=safe))


def test_wait_without_predicate_loses_the_wakeup():
    # the setter signals before the waiter waits; the signal is not remembered
    res = explore(lambda: build_flag("native", 1, "signal", check=False), invariant=safe)
    assert res.deadlocks
    sim = replay(lambda: build_flag("native", 1, "signal", check=False), res.deadlocks[0])
    assert sim.v["flag"] == 1 and sim.procs["w0"].op == ("_waiting", "c")
    assert no_errors(explore(lambda: build_flag("native", 1, "signal", check=True), invariant=safe))


def test_one_condition_with_signal_deadlocks():
    # a consumer's signal wakes the other consumer, not the producer
    b = lambda: build_buffer("native", two_conds=False, how="signal", producers=1, consumers=2)
    res = explore(b, invariant=safe)
    assert res.violations == [] and res.deadlocks
    sim = replay(b, res.deadlocks[0])
    assert sorted(sim.blocked()) == ["c1", "p0"] or sorted(sim.blocked()) == ["c0", "p0"]
    for how, two in (("broadcast", False), ("signal", True)):
        res = explore(lambda: build_buffer("native", two_conds=two, how=how), invariant=safe)
        assert no_errors(res), how


def test_birrell1_remembers_a_signal_with_no_waiter():
    # the setter signals while nobody waits; s stays 1; the late thread's wait drops through
    res = explore(lambda: build_flag("birrell1", 1, "signal", late=True), invariant=safe, stop_at_first=True)
    assert res.violations and "no signal" in res.violations[0][1]
    # with one waiter and no late thread, the wake-up waiting race at point (1) is handled
    assert no_errors(explore(lambda: build_flag("birrell1", 1, "signal"), invariant=safe))


def test_birrell2_binary_broadcast_strands_a_waiter():
    res = explore(lambda: build_flag("birrell2-binary", 2, "broadcast"), invariant=safe)
    assert res.violations == [] and res.deadlocks
    sim = replay(lambda: build_flag("birrell2-binary", 2, "broadcast"), res.deadlocks[0])
    stuck = [p for p in ("w0", "w1") if not sim.procs[p].done]
    assert len(stuck) == 1 and sim.procs[stuck[0]].op == ("P", "c.s")
    assert sim.v["flag"] == 1 and sim.v["c.waiters"] == 0


def test_birrell2_counting_fixes_broadcast_but_a_late_waiter_steals():
    assert no_errors(explore(lambda: build_flag("birrell2", 2, "broadcast"), invariant=safe))
    for how in ("broadcast", "signal"):
        b = lambda: build_flag("birrell2", 1, how, late=True)
        res = explore(b)  # no invariant, so that states after the theft are explored
        stolen = [d for d in res.deadlocks if replay(b, d).v["early"]]
        assert stolen, how
        sim = replay(b, stolen[0])
        # the late thread began to wait after the wakeup and took it; w0 called wait
        # before the setter woke it, and is still blocked at P(s)
        assert sim.procs["w0"].op == ("P", "c.s") and sim.v["flag"] == 1
    # with broadcast the same schedules are harmless in the third version (with signal and
    # two waiters, waking the late thread is allowed, so only broadcast is a fair check)
    assert no_errors(explore(lambda: build_flag("birrell3", 1, "broadcast", late=True), invariant=safe))


@pytest.mark.parametrize("impl", ["birrell3", "queue"])
def test_birrell3_and_queue_one_condition_broadcast(impl):
    res = explore(lambda: build_buffer(impl, two_conds=False, how="broadcast"), invariant=safe)
    assert no_errors(res)


@pytest.mark.parametrize("impl", CORRECT)
def test_seeded_larger_buffer(impl):
    for seed in range(20):
        r = random_run(lambda: build_buffer(impl, capacity=2, producers=2, consumers=3, items=4),
                       seed, invariant=safe)
        assert r.outcome == "done", (seed, r.outcome, r.message)
        assert r.sim.v["count"] == 0
