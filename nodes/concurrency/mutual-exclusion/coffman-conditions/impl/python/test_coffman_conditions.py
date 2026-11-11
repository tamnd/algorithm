# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coffman-conditions/. The authors are listed in prov/90K4PA.jsonl.
from coffman_conditions import ONE_UNIT, TWO_UNITS, build, has_cycle, wait_for_graph
from procsim import explore, replay


def test_two_units_cycle_state_is_reachable():
    # p1 and p3 take R1, p2 and p4 take R2, then p1 asks for R2 and p2 for R1.
    s = replay(lambda: build(*TWO_UNITS), ["p1", "p3", "p2", "p4"])
    assert s.v["avail"] == {"R1": 0, "R2": 0}
    g = wait_for_graph(s)
    assert g["p1"] == {"p2", "p4"} and g["p2"] == {"p1", "p3"}
    assert has_cycle(g)
    assert sorted(s.blocked()) == ["p1", "p2"] and sorted(s.enabled()) == ["p3", "p4"]


def test_two_units_cycle_is_not_a_deadlock_in_any_interleaving():
    cycles = []

    def note(s):
        if has_cycle(wait_for_graph(s)):
            cycles.append(1)
        return None

    r = explore(lambda: build(*TWO_UNITS), invariant=note)
    assert not r.truncated and r.deadlocks == [] and r.finals == 1
    assert cycles  # the cycle occurs in some reachable states


def test_one_unit_cycle_is_a_deadlock():
    r = explore(lambda: build(*ONE_UNIT))
    assert len(r.deadlocks) == 1
    s = replay(lambda: build(*ONE_UNIT), list(r.deadlocks[0]))
    assert wait_for_graph(s) == {"p1": {"p2"}, "p2": {"p1"}}


def test_every_one_unit_cycle_state_is_dead():
    # With single units, each reachable state with a cycle has no way out.
    def check(s):
        if has_cycle(wait_for_graph(s)) and s.enabled():
            return "a cycle with an enabled process"
        return None

    r = explore(lambda: build(*ONE_UNIT), invariant=check)
    assert r.violations == []
