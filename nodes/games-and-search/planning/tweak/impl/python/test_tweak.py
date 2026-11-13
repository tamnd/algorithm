# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tweak/. The authors are listed in prov/SW1BEM.jsonl.

import random

from tweak import (FINISH, START, SUSSMAN_GOAL, SUSSMAN_INIT, Plan, Schema, Step, blocks_schemas, brute_necessarily_true,
                   bfs_length, ground_actions, necessarily_true, run, solution, tweak)

CONSTANTS = ("a", "b")
PREDICATES = (("P", 1), ("R", 2))


def random_prop(rng, variables):
    name, arity = rng.choice(PREDICATES)
    return (name,) + tuple(rng.choice(CONSTANTS + tuple(variables)) for _ in range(arity))


def random_plan(rng):
    """START plus up to three steps; at most three variables and two constants in all."""
    variables = [f"?v{i}" for i in range(rng.randint(0, 3))]
    plan = Plan([random_prop(rng, ()) for _ in range(rng.randint(0, 3))], [])
    for k in range(rng.randint(1, 3)):
        add_pred = rng.choice(PREDICATES)
        add, delete = [], []
        for _ in range(rng.randint(0, 2)):
            p = random_prop(rng, variables)
            (add if p[0] == add_pred[0] else delete).append(p)
        plan.add_step(Step((f"s{k}",), (), tuple(add), tuple(delete)))
    n = len(plan.steps)
    for _ in range(rng.randint(0, 3)):
        i, j = rng.randrange(2, n), rng.randrange(2, n)
        plan.add_ordering(i, j)
    terms = list(CONSTANTS) + variables
    for _ in range(rng.randint(0, 2)):
        x, y = rng.sample(terms, 2)
        b = plan.b.copy()
        if b.unify(x, y) if rng.random() < 0.5 else b.separate(x, y):
            plan.b = b
    return plan, variables


def test_modal_truth_criterion_agrees_with_brute_force():
    rng = random.Random(41)
    true = false = 0
    for _ in range(3000):
        plan, variables = random_plan(rng)
        s = rng.randrange(1, len(plan.steps))
        p = random_prop(rng, variables)
        expected = brute_necessarily_true(plan, s, p)
        assert necessarily_true(plan, s, p) == expected
        true += expected
        false += not expected
    assert true > 300 and false > 300


def test_criterion_on_a_hand_example():
    plan = Plan([("P", "a")], [])
    c = plan.add_step(Step(("C",), (), (), (("P", "?x"),)))
    w = plan.add_step(Step(("W",), (), (("P", "a"),), ()))
    assert not necessarily_true(plan, FINISH, ("P", "a"))
    plan.b.separate("?x", "a")
    assert necessarily_true(plan, FINISH, ("P", "a"))
    plan2 = Plan([("P", "a")], [])
    c = plan2.add_step(Step(("C",), (), (), (("P", "?x"),)))
    w = plan2.add_step(Step(("W",), (), (("P", "a"),), ()))
    plan2.add_ordering(c, w)
    assert necessarily_true(plan2, FINISH, ("P", "a"))
    assert brute_necessarily_true(plan2, FINISH, ("P", "a"))


def random_ground_task(rng):
    """A random task over the facts P(a), P(b), R(a,b), R(b,a) written as schemas."""
    schemas = []
    for k in range(rng.randint(2, 4)):
        facts = [("P", "?x"), ("P", "?y"), ("R", "?x", "?y"), ("R", "?y", "?x")]
        pre = tuple(rng.sample(facts, rng.randint(1, 2)))
        add = tuple(rng.sample(facts, rng.randint(1, 2)))
        delete = tuple(f for f in rng.sample(facts, rng.randint(0, 2)) if f not in add)
        schemas.append(Schema(f"op{k}", ("?x", "?y"), pre + (("D", "?x"), ("D", "?y")), add, delete, (("?x", "?y"),)))
    all_facts = [("P", "a"), ("P", "b"), ("R", "a", "b"), ("R", "b", "a")]
    init = [f for f in all_facts if rng.random() < 0.4] + [("D", "a"), ("D", "b")]
    goal = rng.sample(all_facts, rng.randint(1, 2))
    return init, goal, schemas


def test_existence_and_length_agree_with_bfs():
    rng = random.Random(42)
    solvable = unsolvable = 0
    for _ in range(150):
        init, goal, schemas = random_ground_task(rng)
        actions = ground_actions(schemas, ("a", "b"))
        best = bfs_length(init, goal, actions)
        plan = tweak(init, goal, schemas, 3)
        if best is None or best > 3:
            assert plan is None
            unsolvable += 1
            continue
        assert len(plan.steps) - 2 == best
        for order in plan.linearizations():
            names = [plan.steps[i].name for i in order if i not in (START, FINISH)]
            names = [(n[0],) + tuple(plan.b.value(t) for t in n[1:]) for n in names]
            final = run(init, actions, names)
            assert final is not None and set(goal) <= final
        solvable += 1
    assert solvable > 40 and unsolvable > 20


def test_sussman_anomaly():
    schemas = blocks_schemas()
    plan = tweak(SUSSMAN_INIT, SUSSMAN_GOAL, schemas, 3)
    assert solution(plan) == [("move-to-table", "c", "a"), ("move-from-table", "b", "c"), ("move-from-table", "a", "b")]
    assert len(list(plan.linearizations())) == 1
    actions = ground_actions(schemas, ("a", "b", "c"))
    assert bfs_length(SUSSMAN_INIT, SUSSMAN_GOAL, actions) == 3
    assert set(SUSSMAN_GOAL) <= run(SUSSMAN_INIT, actions, solution(plan))
