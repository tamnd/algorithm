# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conditional-effects/. The authors are listed in prov/DWVFYP.jsonl.

import random

from conditional_effects import (
    bfs_plan,
    briefcase,
    compile_away,
    cond_action,
    cond_reachable,
    cond_successor,
    effect,
    reachable,
)


def project(state, original):
    return frozenset(f for f in state if f in original)


def briefcase_init(objects, where):
    return frozenset({("at-b", "l1")} | {("at", o, l) for o, l in zip(objects, where)} | {("out", o) for o in objects})


def cond_shortest(init, goal, actions):
    for s, d in sorted(cond_reachable(init, actions).items(), key=lambda kv: kv[1]):
        if goal <= s:
            return d
    return None


def test_semantics_hand_cases():
    acts = {a.name: a for a in briefcase(["l1", "l2"], ["o1", "o2"])}
    s = frozenset({("at-b", "l1"), ("at", "o1", "l1"), ("at", "o2", "l1"), ("in", "o1"), ("out", "o2")})
    t = cond_successor(s, acts["move(l1,l2)"])
    assert t == frozenset({("at-b", "l2"), ("at", "o1", "l2"), ("at", "o2", "l1"), ("in", "o1"), ("out", "o2")})
    # Conditions are read in the old state, and an add beats a delete of the same fact.
    a = cond_action("a", [], [effect(["p"], ["q"], []), effect(["r"], [], ["q"]), effect(["q"], ["z"], [])])
    assert cond_successor(frozenset({"p", "r"}), a) == frozenset({"p", "r", "q"})
    assert cond_successor(frozenset({"r", "q"}), a) == frozenset({"r", "z"})


def test_briefcase_counts_and_isomorphism():
    for nl, no in ((2, 1), (2, 2), (3, 2), (3, 3)):
        locs = [f"l{i + 1}" for i in range(nl)]
        objs = [f"o{i + 1}" for i in range(no)]
        acts = briefcase(locs, objs)
        init = briefcase_init(objs, [locs[i % nl] for i in range(no)])
        new_init, compiled = compile_away(init, acts)
        assert len(acts) == nl * (nl - 1) + no * nl + no
        assert len(compiled) == nl * (nl - 1) * 2 ** no + no * nl + no
        original = cond_reachable(init, acts)
        comp = reachable(new_init, compiled)
        facts = frozenset().union(*original)
        assert len(original) == len(comp)
        assert {project(s, facts) for s in comp} == set(original)
        for s, d in comp.items():
            assert original[project(s, facts)] == d


def test_briefcase_plan_lengths():
    locs, objs = ["l1", "l2", "l3"], ["o1", "o2"]
    acts = briefcase(locs, objs)
    init = briefcase_init(objs, ["l1", "l2"])
    new_init, compiled = compile_away(init, acts)
    for goal in ({("at", "o1", "l3"), ("at", "o2", "l3")}, {("at", "o1", "l2"), ("at", "o2", "l1")}, {("at-b", "l3"), ("out", "o1"), ("at", "o1", "l3")}):
        goal = frozenset(goal)
        assert len(bfs_plan(new_init, goal, compiled)) == cond_shortest(init, goal, acts)
    goal = frozenset({("at", "o1", "l3"), ("at", "o2", "l3")})
    # put-in(o1,l1), move(l1,l2), put-in(o2,l2), move(l2,l3)
    assert cond_shortest(init, goal, acts) == 4


def test_random_tasks():
    rng = random.Random(4)
    facts = ["p", "q", "r", "s", "t"]
    for _ in range(60):
        acts = []
        for i in range(4):
            pre = rng.sample(facts, rng.randint(0, 2))
            effs = [effect((), rng.sample(facts, 1), rng.sample(facts, rng.randint(0, 1)))]
            for _ in range(rng.randint(0, 3)):
                effs.append(effect([rng.choice(facts)], rng.sample(facts, rng.randint(0, 1)), rng.sample(facts, rng.randint(0, 1))))
            acts.append(cond_action(f"a{i}", pre, effs))
        init = frozenset(rng.sample(facts, 2))
        new_init, compiled = compile_away(init, acts)
        original = cond_reachable(init, acts)
        comp = reachable(new_init, compiled)
        assert len(original) == len(comp)
        assert {project(s, set(facts)) for s in comp} == set(original)
        for s, d in comp.items():
            assert original[project(s, set(facts))] == d
            for f in facts:
                if ("not", f) in s or f in s:
                    assert (("not", f) in s) != (f in s)
