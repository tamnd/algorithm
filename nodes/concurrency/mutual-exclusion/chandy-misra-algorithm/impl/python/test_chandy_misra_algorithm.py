# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chandy-misra-algorithm/. The authors are listed in prov/0J7AS3.jsonl.
import random

from chandy_misra_algorithm import all_meals_eaten, build, precedence
from procsim import explore, random_run


def ring(n):
    return [(i, (i + 1) % n) for i in range(n)]


def has_cycle(g):
    state = {}

    def visit(v):
        state[v] = 1
        for w in g.get(v, ()):
            if state.get(w) == 1 or (w not in state and visit(w)):
                return True
        state[v] = 2
        return False

    return any(v not in state and visit(v) for v in list(g))


def check(s):
    """Every invariant of the proof, in one state."""
    v = s.v
    if has_cycle(precedence(s)):
        return "the precedence graph has a cycle"
    for e, holder in v["fork"].items():
        a, b = (f"p{x}" for x in e.split("-"))
        if v["state"][a] == "eating" and v["state"][b] == "eating":
            return f"neighbours {a} and {b} eat together"
        if v["state"][a] == "eating" and holder != a or v["state"][b] == "eating" and holder != b:
            return f"an eater lacks the fork of {e}"
        if not v["dirty"][e] and v["state"][holder] != "hungry":
            return f"a clean fork of {e} is at {holder}, which is not hungry"
    return None


def test_triangle_exhaustive():
    res = explore(lambda: build(3, ring(3), rounds=1), goal=all_meals_eaten, invariant=check)
    assert res.violations == [] and res.deadlocks == [] and not res.truncated
    assert res.finals >= 1


def test_path_with_two_meals_exhaustive():
    res = explore(lambda: build(3, [(0, 1), (1, 2)], rounds=2), goal=all_meals_eaten, invariant=check)
    assert res.violations == [] and res.deadlocks == [] and not res.truncated


def test_ring_of_five_seeded():
    for seed in range(30):
        r = random_run(lambda: build(5, ring(5), rounds=4), seed, max_steps=20000,
                       goal=all_meals_eaten, invariant=check)
        assert r.outcome == "done", (seed, r.outcome, r.message)


def test_random_conflict_graphs_seeded():
    rng = random.Random(7)
    for _ in range(25):
        n = rng.randint(3, 6)
        edges = [(a, b) for a in range(n) for b in range(a + 1, n) if rng.random() < 0.5]
        r = random_run(lambda: build(n, edges, rounds=3), rng.randrange(10**6), max_steps=20000,
                       goal=all_meals_eaten, invariant=check)
        assert r.outcome == "done", (n, edges, r.outcome, r.message)


def test_eating_makes_a_sink():
    sim = build(3, ring(3), rounds=1)
    while not any(st == "eating" for st in sim.v["state"].values()):
        sim.step(sim.enabled()[0])
    eater = next(u for u, st in sim.v["state"].items() if st == "eating")
    assert precedence(sim)[eater] == set()  # all its forks are dirty: it yields to everyone
