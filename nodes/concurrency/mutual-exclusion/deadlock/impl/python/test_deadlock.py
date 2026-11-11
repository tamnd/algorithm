# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deadlock/. The authors are listed in prov/Y272XW.jsonl.
from deadlock import (build_communication, build_opposite_order, build_same_order, build_self_deadlock,
                      deadlocked_states)
from procsim import explore, random_run


def test_opposite_order_deadlocks_on_one_schedule():
    dead = deadlocked_states(build_opposite_order)
    assert len(dead) == 1
    s = dead[0]
    assert s.mutexes["A"].owner == "p" and s.mutexes["B"].owner == "q"
    assert s.waits_for() == {"p": {"q"}, "q": {"p"}}


def test_opposite_order_deadlock_needs_both_first_steps_first():
    r = explore(build_opposite_order)
    assert r.deadlocks == [("p", "q")]
    assert r.finals == 1


def test_same_order_has_no_deadlock_in_any_interleaving():
    r = explore(build_same_order)
    assert r.deadlocks == [] and r.finals == 1 and not r.truncated


def test_random_runs_of_opposite_order_hit_both_outcomes():
    outcomes = {random_run(build_opposite_order, seed).outcome for seed in range(200)}
    assert outcomes == {"done", "deadlock"}


def test_communication_deadlock_without_resources():
    dead = deadlocked_states(lambda: build_communication(False))
    assert len(dead) == 1
    s = dead[0]
    assert s.mutexes == {} and s.chans == {"to_p": [], "to_q": []}
    r = explore(lambda: build_communication(True))
    assert r.deadlocks == [] and r.finals == 1


def test_self_deadlock_of_one_process():
    dead = deadlocked_states(build_self_deadlock)
    assert len(dead) == 1 and dead[0].mutexes["A"].owner == "p"
