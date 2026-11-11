# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monitor/. The authors are listed in prov/7D5E07.jsonl.
import pytest

from monitor import build_buffer, build_resource, check
from procsim import explore, random_run, replay

HOARE = ("hoare", "hoare-sem")


def no_errors(res):
    return res.violations == [] and res.deadlocks == [] and not res.truncated


SCENARIOS = [
    ("resource 3x1", lambda mode, loop: build_resource(mode, 3, 1, loop)),
    ("resource 2x2", lambda mode, loop: build_resource(mode, 2, 2, loop)),
    ("buffer 1+2", lambda mode, loop: build_buffer(mode, loop=loop)),
    ("buffer 2+2", lambda mode, loop: build_buffer(mode, producers=2, consumers=2, loop=loop)),
]


@pytest.mark.parametrize("mode", HOARE)
@pytest.mark.parametrize("loop", [False, True])
def test_hoare_semantics_if_is_enough(mode, loop):
    # the proof rules hold: I at each wait, signal and exit, and B when a wait returns
    for name, b in SCENARIOS:
        res = explore(lambda: b(mode, loop), invariant=check)
        assert no_errors(res), (name, res.deadlocks[:1], res.violations[:1])


def test_mesa_needs_while():
    for name, b in SCENARIOS:
        assert no_errors(explore(lambda: b("mesa", True), invariant=check)), name
        res = explore(lambda: b("mesa", False), invariant=check)
        assert res.violations and res.deadlocks == [], name


def test_hoare_and_mesa_differ_when_the_condition_becomes_false_again():
    # Mesa with if: u1 waits for nonbusy; u0 releases and signals; before u1 runs
    # again, u2 enters, finds the resource free and takes it; u1 then takes it too
    b = lambda: build_resource("mesa", 3, 1, False)
    res = explore(b, invariant=check)
    sched, msg = min(res.violations, key=lambda v: len(v[0]))
    assert msg == "two processes hold the resource"
    log = replay(b, sched).log
    kinds = [k for k, _ in log]
    waiter = log[kinds.index("wait")][1]
    i_sig, i_res = kinds.index("signal"), kinds.index("resume")
    assert log[i_res][1] == waiter and i_sig < i_res
    assert any(k == "acquire" and p != waiter for k, p in log[i_sig:i_res])
    assert log[-1] == ("acquire", waiter)
    # with while, the same overtaking still happens: the waiter sees B false and waits again
    seen = explore(lambda: build_resource("mesa", 3, 1, True),
                   invariant=lambda s: "B false" if s.v["B false after wait"] else None,
                   stop_at_first=True)
    assert seen.violations
    # under Hoare semantics it cannot: B holds whenever a wait returns (checked in `check`)
    for mode in HOARE:
        res = explore(lambda: build_resource(mode, 3, 1, False), invariant=check)
        assert no_errors(res) and res.finals >= 1


def test_hoare_implementation_needs_urgent():
    # if exit ignores signallers waiting on urgent, a signaller waits for ever
    for b in (lambda: build_resource("hoare-sem-no-urgent", 3, 1), lambda: build_buffer("hoare-sem-no-urgent")):
        res = explore(b, invariant=check)
        assert res.violations == [] and res.deadlocks
        sim = replay(b, min(res.deadlocks, key=len))
        assert any(sim.procs[p].op == ("P", "urgent") for p in sim.blocked())
        assert sim.v["urgentcount"] >= 1


@pytest.mark.parametrize("mode,loop", [("mesa", True), ("hoare", False), ("hoare-sem", False)])
def test_seeded_larger(mode, loop):
    for seed in range(20):
        r = random_run(lambda: build_resource(mode, 4, 3, loop), seed, invariant=check)
        assert r.outcome == "done", (seed, r.outcome, r.message)
        r = random_run(lambda: build_buffer(mode, capacity=2, producers=2, consumers=3, items=4, loop=loop),
                       seed, invariant=check)
        assert r.outcome == "done" and r.sim.v["count"] == 0, (seed, r.outcome, r.message)
