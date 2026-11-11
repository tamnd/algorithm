# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cigarette-smokers-problem/. The authors are listed in prov/JBBYWT.jsonl.
import pytest

from cigarette_smokers_problem import INGREDIENTS, NEEDS, all_smoked, build, right_smoker
from procsim import explore, random_run, replay


def test_naive_smokers_deadlock():
    b = lambda: build("naive", 1)
    res = explore(b, goal=all_smoked, invariant=right_smoker, stop_at_first=True)
    assert res.deadlocks
    sim = replay(b, res.deadlocks[0])
    # a smoker that cannot use the offer took one of its ingredients and waits for a second one,
    # so the smoker the offer was for waits for ever too
    assert sim.v["smoked"] == 0
    holding_one = [h for h in INGREDIENTS if sim.procs[f"smoker_{h}"].op == ("P", NEEDS[h][1])]
    assert holding_one
    assert all(sim.procs[f"smoker_{h}"].op[0] == "P" for h in INGREDIENTS)


@pytest.mark.parametrize("kind", ["pushers", "indexed", "simultaneous"])
def test_solutions_exhaustive(kind):
    res = explore(lambda: build(kind, 2), goal=all_smoked, invariant=right_smoker)
    assert res.violations == [] and res.deadlocks == [] and not res.truncated
    assert res.finals >= 3  # the offers can be any two of the three pairs


@pytest.mark.parametrize("kind", ["pushers", "indexed", "simultaneous"])
def test_solutions_seeded(kind):
    for seed in range(30):
        r = random_run(lambda: build(kind, 12), seed, goal=all_smoked, invariant=right_smoker)
        assert r.outcome == "done", (seed, r.outcome, r.message)
