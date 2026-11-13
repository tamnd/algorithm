# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partial-order-plan/. The authors are listed in prov/QH51FZ.jsonl.

import random
from itertools import permutations

from partial_order_plan import (FINISH, START, Link, PartialOrderPlan, is_plan, make_action, move_actions, successor,
                                sussman_plan, SUSSMAN_GOAL, SUSSMAN_INIT)


def random_actions(rng, n_facts, n_actions):
    facts = list(range(n_facts))
    acts = []
    for k in range(n_actions):
        pre = rng.sample(facts, rng.randint(0, 2))
        add = rng.sample(facts, rng.randint(1, 2))
        delete = [f for f in rng.sample(facts, rng.randint(0, 2)) if f not in add]
        acts.append(make_action(f"a{k}", pre, add, delete))
    return acts


def orders_of(plan):
    """Brute force: every permutation of the steps that respects every ordering."""
    pairs = plan.orderings
    out = set()
    for perm in permutations(range(len(plan.steps))):
        pos = {s: i for i, s in enumerate(perm)}
        if all(pos[i] < pos[j] for i, j in pairs):
            out.add(perm)
    return out


def random_plan(rng, n_facts=4, n_steps=3, n_links=4, n_orders=2):
    acts = random_actions(rng, n_facts, 6)
    init = frozenset(f for f in range(n_facts) if rng.random() < 0.5)
    goal = frozenset(rng.sample(range(n_facts), 2))
    plan = PartialOrderPlan(init, goal)
    for _ in range(n_steps):
        plan.add_step(rng.choice(acts))
    for _ in range(n_links):
        j = rng.randrange(1, len(plan.steps))
        if not plan.steps[j].pre:
            continue
        p = rng.choice(sorted(plan.steps[j].pre))
        producers = [i for i in range(len(plan.steps)) if p in plan.steps[i].add and i != j]
        if producers:
            plan.add_link(rng.choice(producers), p, j)
    for _ in range(n_orders if n_steps >= 2 else 0):
        i, j = rng.sample(range(2, len(plan.steps)), 2)
        plan.add_ordering(i, j)
    return plan


def plan_from_sequence(init, goal, seq):
    """Last-adder links, and every threat ordered as in seq."""
    plan = PartialOrderPlan(init, goal)
    ids = [plan.add_step(a) for a in seq]
    order = [START] + ids + [FINISH]
    for pos, j in enumerate(order):
        for p in sorted(plan.steps[j].pre):
            producer = START
            for i in order[1:pos]:
                if p in plan.steps[i].add:
                    producer = i
            assert plan.add_link(producer, p, j)
    for link in list(plan.links):
        for k in ids:
            if link.fact in plan.steps[k].delete and k not in (link.producer, link.consumer):
                if order.index(k) < order.index(link.producer):
                    assert plan.add_ordering(k, link.producer)
                else:
                    assert plan.add_ordering(link.consumer, k)
    return plan


def test_consistency_is_acyclicity():
    rng = random.Random(1)
    for _ in range(300):
        plan = PartialOrderPlan([0], [0])
        for _ in range(rng.randint(0, 4)):
            plan.add_step(make_action("x"))
        n = len(plan.steps)
        for _ in range(rng.randint(0, 6)):
            i, j = rng.sample(range(n), 2)
            plan.add_ordering_unchecked(i, j)
        assert plan.is_consistent() == bool(orders_of(plan))


def test_linearizations_match_brute_force():
    rng = random.Random(2)
    for _ in range(200):
        plan = random_plan(rng, n_steps=rng.randint(0, 4))
        assert plan.is_consistent()
        lins = list(plan.linearizations())
        assert len(lins) == len(set(lins))
        assert set(lins) == orders_of(plan)


def test_precedes_and_can_order():
    rng = random.Random(3)
    for _ in range(200):
        plan = random_plan(rng)
        lins = orders_of(plan)
        n = len(plan.steps)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                always = all(l.index(i) < l.index(j) for l in lins)
                assert plan.precedes(i, j) == always
                assert plan.can_order(i, j) == any(l.index(i) < l.index(j) for l in lins)


def test_threats_match_brute_force():
    rng = random.Random(4)
    checked = 0
    for _ in range(300):
        plan = random_plan(rng, n_steps=rng.randint(1, 4))
        lins = orders_of(plan)
        found = set(plan.threats())
        for link in plan.links:
            for k, step in enumerate(plan.steps):
                if link.fact not in step.delete:
                    continue
                between = any(l.index(link.producer) < l.index(k) < l.index(link.consumer) for l in lins)
                assert ((k, link) in found) == between
                checked += 1
        for k, link in found:
            assert link.fact in plan.steps[k].delete
    assert checked > 100


def test_open_conditions():
    rng = random.Random(5)
    for _ in range(100):
        plan = random_plan(rng)
        linked = {(l.fact, l.consumer) for l in plan.links}
        expected = {(p, j) for j, s in enumerate(plan.steps) for p in s.pre if (p, j) not in linked}
        assert set(plan.open_conditions()) == expected


def test_every_linearization_of_a_solution_is_valid():
    rng = random.Random(6)
    solutions = 0
    for _ in range(300):
        n = rng.randint(3, 5)
        acts = random_actions(rng, n, 6)
        init = frozenset(f for f in range(n) if rng.random() < 0.5)
        state, seq = init, []
        for _ in range(rng.randint(1, 5)):
            options = [a for a in acts if a.pre <= state]
            if not options:
                break
            a = rng.choice(options)
            seq.append(a)
            state = successor(state, a)
        goal = frozenset(rng.sample(sorted(state), min(2, len(state))))
        plan = plan_from_sequence(init, goal, seq)
        assert plan.is_solution()
        lins = list(plan.linearizations())
        assert tuple([START] + list(range(2, len(plan.steps))) + [FINISH]) in lins
        for order in lins:
            assert is_plan(init, goal, plan.actions(order))
        solutions += 1
    assert solutions == 300


def test_random_plans_soundness():
    rng = random.Random(7)
    for _ in range(400):
        plan = random_plan(rng, n_links=8)
        if plan.is_solution():
            assert plan.every_linearization_valid()


def test_sussman_plan():
    plan = sussman_plan()
    assert plan.is_solution()
    lins = list(plan.linearizations())
    assert lins == [(START, 2, 3, 4, FINISH)]
    assert [a.name for a in plan.actions(lins[0])] == ["move(c,a,table)", "move(b,table,c)", "move(a,table,b)"]
    assert is_plan(SUSSMAN_INIT, SUSSMAN_GOAL, plan.actions(lins[0]))


def test_sussman_plan_with_threats():
    plan = sussman_plan(resolve=False)
    assert not plan.open_conditions()
    threats = plan.threats()
    assert set(threats) == {(3, Link(START, ("clear", "c"), 2)), (4, Link(START, ("clear", "b"), 3))}
    lins = list(plan.linearizations())
    assert len(lins) == 3
    valid = [l for l in lins if is_plan(SUSSMAN_INIT, SUSSMAN_GOAL, plan.actions(l))]
    assert valid == [(START, 2, 3, 4, FINISH)]


def test_link_rules():
    acts = {a.name: a for a in move_actions("abc")}
    plan = PartialOrderPlan(SUSSMAN_INIT, SUSSMAN_GOAL)
    s = plan.add_step(acts["move(c,a,table)"])
    try:
        plan.add_link(s, ("on", "a", "b"), FINISH)
        assert False
    except ValueError:
        pass
    assert plan.add_link(START, ("clear", "c"), s)
    assert not plan.add_ordering(s, START)
    assert plan.is_consistent()
