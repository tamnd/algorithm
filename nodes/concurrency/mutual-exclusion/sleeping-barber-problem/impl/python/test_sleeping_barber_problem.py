# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sleeping-barber-problem/. The authors are listed in prov/PY293Y.jsonl.
import pytest

from procsim import explore, random_run, replay
from sleeping_barber_problem import build, served_after_cut, shop_rules


def everyone_handled(s):
    """The goal: each customer has left, served or turned away, and every seated one got a haircut."""
    return s.all_done() and s.v["seated"] + s.v["turned_away"] == sum(
        1 for n in s.procs if n.startswith("c")) and s.v["cuts"] == s.v["seated"]


def test_naive_loses_a_wakeup():
    b = lambda: build("naive", 1, 1)
    res = explore(b, goal=everyone_handled, invariant=shop_rules(1), stop_at_first=True)
    assert res.deadlocks
    sim = replay(b, res.deadlocks[0])
    # the barber saw an empty shop, the customer sat down and its wakeup was
    # lost because the barber was not yet asleep; now both wait for ever
    assert sim.procs["barber"].op == ("_asleep",)
    assert sim.v["waiting"] == 1 and sim.v["cuts"] == 0
    assert sim.procs["c0"].op[0] == "await"


@pytest.mark.parametrize("kind", ["semaphores", "rendezvous"])
@pytest.mark.parametrize("chairs,customers", [(1, 1), (1, 3), (2, 3)])
def test_semaphore_solution_exhaustive(kind, chairs, customers):
    res = explore(lambda: build(kind, chairs, customers), goal=everyone_handled,
                  invariant=shop_rules(chairs))
    assert res.violations == [] and res.deadlocks == [] and not res.truncated
    assert res.finals >= 1


def test_some_customer_is_turned_away():
    b = lambda: build("semaphores", 1, 3)
    res = explore(b, goal=lambda s: everyone_handled(s) and s.v["turned_away"] == 0)
    assert res.deadlocks  # final states in which someone left without a haircut


def test_textbook_customer_can_leave_before_the_haircut_ends():
    res = explore(lambda: build("semaphores", 1, 1), invariant=served_after_cut, stop_at_first=True)
    assert res.violations


def test_rendezvous_customer_leaves_after_the_haircut():
    for chairs, customers in [(1, 3), (2, 3)]:
        res = explore(lambda: build("rendezvous", chairs, customers), invariant=served_after_cut)
        assert res.violations == [] and not res.truncated


def test_seeded_larger_runs():
    for seed in range(30):
        for kind in ("semaphores", "rendezvous"):
            r = random_run(lambda: build(kind, 3, 8), seed, goal=everyone_handled,
                           invariant=shop_rules(3))
            assert r.outcome == "done", (kind, seed, r.outcome, r.message)
