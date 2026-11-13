# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ucpop/. The authors are listed in prov/9M4E8C.jsonl.

import random
from collections import deque

from ucpop import (FINISH, START, PartialPlan, bfs_length, briefcase, compile_to_strips, effect, holds, is_plan,
                   make_action, refine, successor, ucpop)


def direct_bfs_length(init, goal, actions):
    """Reference without compilation: breadth-first search with the conditional semantics."""
    start = frozenset(init)
    dist = {start: 0}
    queue = deque([start])
    while queue:
        s = queue.popleft()
        if holds(s, goal):
            return dist[s]
        for a in actions:
            if holds(s, a.pre):
                t = successor(s, a)
                if t not in dist:
                    dist[t] = dist[s] + 1
                    queue.append(t)
    return None


def random_literal(rng, facts):
    return (rng.choice(facts), rng.random() < 0.7)


def random_task(rng, n_facts, n_actions):
    facts = list(range(n_facts))
    acts = []
    for k in range(n_actions):
        pre = {random_literal(rng, facts) for _ in range(rng.randint(0, 1))}
        effects, used = [], set()
        for _ in range(rng.randint(1, 2)):
            cond = {random_literal(rng, facts) for _ in range(rng.randint(0, 2))}
            f = rng.choice(facts)
            if rng.random() < 0.6:
                add, dele = [f], []
            else:
                add, dele = [], [f]
            if f in used:
                continue
            used.add(f)
            effects.append(effect(cond, add, dele))
        acts.append(make_action(f"a{k}", pre, effects))
    init = frozenset(f for f in facts if rng.random() < 0.4)
    goal = frozenset(random_literal(rng, facts) for _ in range(rng.randint(1, 2)))
    return init, goal, acts


def all_valid(plan, init, goal):
    orders = list(plan.linearizations())
    return bool(orders) and all(is_plan(init, goal, plan.actions(o)) for o in orders)


def test_compilation_preserves_the_task():
    rng = random.Random(31)
    for _ in range(300):
        init, goal, acts = random_task(rng, 4, rng.randint(1, 4))
        assert bfs_length(init, goal, compile_to_strips(acts)) == direct_bfs_length(init, goal, acts)


def test_compiled_actions_match_the_semantics():
    rng = random.Random(32)
    for _ in range(200):
        init, goal, acts = random_task(rng, 4, 3)
        compiled = compile_to_strips(acts)
        for bits in range(16):
            s = frozenset(f for f in range(4) if bits >> f & 1)
            for a in acts:
                versions = [c for c in compiled if c.name == a.name and holds(s, c.pre)]
                if holds(s, a.pre):
                    assert {(s - c.delete) | c.add for c in versions} == {successor(s, a)}
                else:
                    assert versions == []


def test_existence_and_length_agree_with_bfs_on_the_compiled_task():
    rng = random.Random(33)
    solvable = unsolvable = 0
    for k in range(300):
        init, goal, acts = random_task(rng, 3 + k % 2, rng.randint(1, 4))
        best = bfs_length(init, goal, compile_to_strips(acts))
        plan = ucpop(init, goal, acts)
        if best is None:
            assert plan is None
            unsolvable += 1
        else:
            assert len(plan.steps) - 2 == best
            assert all_valid(plan, init, goal)
            solvable += 1
    assert solvable > 80 and unsolvable > 40


def test_every_complete_plan_is_a_solution():
    rng = random.Random(34)
    seen = 0
    for _ in range(150):
        init, goal, acts = random_task(rng, 4, 3)
        for plan in refine(PartialPlan(init, goal), acts, 3):
            assert all_valid(plan, init, goal)
            seen += 1
    assert seen > 50


def test_briefcase_needs_confrontation():
    init, goal, acts = briefcase()
    plan = ucpop(init, goal, acts)
    names = {tuple(a.name for a in plan.actions(o)) for o in plan.linearizations()}
    assert names == {("take-out(P)", "put-in(D,home)", "move-b(home,office)"),
                     ("put-in(D,home)", "take-out(P)", "move-b(home,office)")}
    assert bfs_length(init, goal, compile_to_strips(acts)) == 3
    assert all_valid(plan, init, goal)
    move = next(i for i, s in enumerate(plan.steps) if s.name == "move-b(home,office)")
    assert ((("in", "P"), False), move) in plan.goals


def test_sussman_anomaly_without_conditional_effects():
    acts = []
    blocks = "abc"
    for b in blocks:
        for x in blocks:
            if x == b:
                continue
            acts.append(make_action(f"move({b},{x},table)", [(("on", b, x), True), (("clear", b), True)],
                                    [effect([], [("ontable", b), ("clear", x)], [("on", b, x)])]))
            acts.append(make_action(f"move({b},table,{x})", [(("ontable", b), True), (("clear", b), True), (("clear", x), True)],
                                    [effect([], [("on", b, x)], [("ontable", b), ("clear", x)])]))
            for y in blocks:
                if y not in (b, x):
                    acts.append(make_action(f"move({b},{x},{y})", [(("on", b, x), True), (("clear", b), True), (("clear", y), True)],
                                            [effect([], [("on", b, y), ("clear", x)], [("on", b, x), ("clear", y)])]))
    init = {("on", "c", "a"), ("ontable", "a"), ("ontable", "b"), ("clear", "c"), ("clear", "b")}
    goal = {(("on", "a", "b"), True), (("on", "b", "c"), True)}
    plan = ucpop(init, goal, acts, max_steps=3)
    assert [a.name for a in plan.one_linearization()] == ["move(c,a,table)", "move(b,table,c)", "move(a,table,b)"]
    assert all_valid(plan, init, goal)


def test_negative_goal_uses_the_closed_world():
    lamp = ("on", "lamp")
    toggle = make_action("switch", [], [effect([(lamp, True)], [], [lamp]), effect([(lamp, False)], [lamp], [])])
    plan = ucpop([lamp], [(lamp, False)], [toggle])
    assert [a.name for a in plan.one_linearization()] == ["switch"]
    assert ucpop([], [(lamp, False)], [toggle]).steps[2:] == []
    plan = ucpop([], [(lamp, True), (("seen", "x"), False)], [toggle])
    assert [a.name for a in plan.one_linearization()] == ["switch"]
    assert ucpop([], [(lamp, True), (("seen", "x"), True)], [toggle]) is None


def test_an_action_may_not_add_and_delete_a_fact():
    try:
        make_action("bad", [], [effect([], ["p"], []), effect([(("q", 1), True)], [], ["p"])])
        assert False
    except ValueError:
        pass
