# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/situation-calculus-regression/. The authors are listed in prov/A4NKPR.jsonl.
"""Regression against progression by simulation, on random ground domains."""

import itertools
import random

from situation_calculus_regression import (
    FALSE,
    TRUE,
    Action,
    BasicActionTheory,
    Formulas,
    yale_shooting,
)


def random_formula(f: Formulas, rng: random.Random, fluents, depth: int) -> int:
    if depth == 0 or rng.random() < 0.3:
        r = rng.random()
        if r < 0.08:
            return TRUE
        if r < 0.16:
            return FALSE
        return f.fluent(rng.choice(fluents))
    op = rng.choice(["not", "and", "or"])
    if op == "not":
        return f.neg(random_formula(f, rng, fluents, depth - 1))
    a = random_formula(f, rng, fluents, depth - 1)
    b = random_formula(f, rng, fluents, depth - 1)
    return f.conj(a, b) if op == "and" else f.disj(a, b)


def random_theory(rng: random.Random) -> BasicActionTheory:
    f = Formulas()
    k = rng.randint(1, 6)
    fluents = ["F%d" % i for i in range(k)]
    actions = {}
    for j in range(rng.randint(1, 4)):
        name = "a%d" % j
        poss = TRUE if rng.random() < 0.5 else random_formula(f, rng, fluents, 2)
        plus, minus = {}, {}
        for fl in fluents:
            if rng.random() < 0.5:
                plus[fl] = random_formula(f, rng, fluents, 2)
            if rng.random() < 0.5:
                minus[fl] = random_formula(f, rng, fluents, 2)
        actions[name] = Action(name, poss, plus, minus)
    initial = [random_formula(f, rng, fluents, 2) for _ in range(rng.randint(0, 3))]
    return BasicActionTheory(f, fluents, actions, initial)


def all_states(fluents):
    for bits in itertools.product([False, True], repeat=len(fluents)):
        yield dict(zip(fluents, bits))


def test_regression_agrees_with_progression_on_every_state():
    """For every initial state s, R[phi] holds at s iff phi holds after simulating the actions from s."""
    rng = random.Random(1)
    for _ in range(300):
        bat = random_theory(rng)
        names = sorted(bat.actions)
        seq = [rng.choice(names) for _ in range(rng.randint(0, 8))]
        phi = random_formula(bat.f, rng, bat.fluents, 3)
        reg = bat.regress(phi, seq)
        for s in all_states(bat.fluents):
            t = dict(s)
            for a in seq:
                t = bat.step(t, a)
            assert bat.f.evaluate(reg, s) == bat.f.evaluate(phi, t)


def test_projection_and_executability_match_simulation():
    rng = random.Random(2)
    for _ in range(400):
        bat = random_theory(rng)
        names = sorted(bat.actions)
        seq = [rng.choice(names) for _ in range(rng.randint(0, 8))]
        phi = random_formula(bat.f, rng, bat.fluents, 3)
        assert bat.project_by_regression(phi, seq) == bat.project_by_simulation(phi, seq)
        assert bat.executable_by_regression(seq) == bat.executable_by_simulation(seq)


def test_regressed_dag_grows_linearly():
    """dag_size(R[phi]) <= dag_size(phi) + sum over the steps of the sizes of the successor state formulas."""
    rng = random.Random(3)
    for _ in range(100):
        bat = random_theory(rng)
        names = sorted(bat.actions)
        seq = [rng.choice(names) for _ in range(rng.randint(0, 12))]
        phi = random_formula(bat.f, rng, bat.fluents, 3)
        bound = bat.f.dag_size(phi)
        for a in seq:
            bound += sum(bat.f.dag_size(bat.phi[a][fl]) for fl in bat.fluents)
        assert bat.f.dag_size(bat.regress(phi, seq)) <= bound


def test_tree_blows_up_but_dag_does_not():
    """An action that sets p to (p iff q) doubles the tree at each step, while the DAG grows by a constant."""
    f = Formulas()
    p, q = f.fluent("p"), f.fluent("q")
    same = f.disj(f.conj(p, q), f.conj(f.neg(p), f.neg(q)))
    # p(do(a, s)) <-> gamma_plus or (p and not gamma_minus), with gamma_plus = not p and not q, gamma_minus = not q.
    act = Action("a", TRUE, {"p": f.conj(f.neg(p), f.neg(q))}, {"p": f.neg(q)})
    bat = BasicActionTheory(f, ["p", "q"], {"a": act}, [])
    for s in all_states(["p", "q"]):
        assert bat.step(s, "a")["p"] == f.evaluate(same, s)
    trees, dags = [], []
    for n in range(1, 9):
        r = bat.regress(p, ["a"] * n)
        trees.append(f.tree_size(r))
        dags.append(f.dag_size(r))
    assert all(trees[i + 1] > 2 * trees[i] for i in range(len(trees) - 1))
    assert all(dags[i + 1] - dags[i] <= f.dag_size(bat.phi["a"]["p"]) for i in range(len(dags) - 1))


def test_yale_shooting():
    bat, f = yale_shooting(initial_alive_only=True)
    alive, loaded = f.fluent("alive"), f.fluent("loaded")
    assert bat.regress(f.neg(alive), ["load", "wait", "shoot"]) == TRUE
    assert bat.regress(alive, ["wait", "shoot"]) == f.conj(alive, f.neg(loaded))
    assert not bat.project_by_regression(alive, ["wait", "shoot"])
    assert bat.executable_formula(["load", "wait", "shoot"]) == f.neg(loaded)
    assert not bat.executable_by_regression(["load", "wait", "shoot"])
    bat2, f2 = yale_shooting(initial_alive_only=False)
    assert bat2.project_by_regression(f2.fluent("alive"), ["wait", "shoot"])
    assert bat2.project_by_regression(f2.neg(f2.fluent("alive")), ["load", "wait", "shoot"])
    assert bat2.executable_by_regression(["load", "wait", "shoot"])
    assert not bat2.executable_by_regression(["load", "load"])
