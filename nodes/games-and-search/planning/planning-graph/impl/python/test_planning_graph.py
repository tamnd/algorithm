# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/planning-graph/. The authors are listed in prov/PJJTVQ.jsonl.

import random
from itertools import combinations

from planning_graph import Action, PlanningGraph, interfere, pair


def act(name, pre, add, dele=()):
    return Action(name, frozenset(pre), frozenset(add), frozenset(dele))


def blocks(names):
    acts = []
    for x in names:
        acts.append(act(("pickup", x), [("clear", x), ("ontable", x), "handempty"], [("holding", x)],
                        [("clear", x), ("ontable", x), "handempty"]))
        acts.append(act(("putdown", x), [("holding", x)], [("clear", x), ("ontable", x), "handempty"], [("holding", x)]))
        for y in names:
            if x != y:
                acts.append(act(("stack", x, y), [("holding", x), ("clear", y)],
                                [("on", x, y), ("clear", x), "handempty"], [("holding", x), ("clear", y)]))
                acts.append(act(("unstack", x, y), [("on", x, y), ("clear", x), "handempty"],
                                [("holding", x), ("clear", y)], [("on", x, y), ("clear", x), "handempty"]))
    return acts


def gripper():
    acts = []
    rooms, balls, hands = ["a", "b"], ["b1", "b2"], ["l", "r"]
    for r in rooms:
        for t in rooms:
            if r != t:
                acts.append(act(("move", r, t), [("robby", r)], [("robby", t)], [("robby", r)]))
        for b in balls:
            for g in hands:
                acts.append(act(("pick", b, r, g), [("at", b, r), ("robby", r), ("free", g)], [("carry", b, g)],
                                [("at", b, r), ("free", g)]))
                acts.append(act(("drop", b, r, g), [("carry", b, g), ("robby", r)], [("at", b, r), ("free", g)],
                                [("carry", b, g)]))
    init = frozenset([("robby", "a"), ("at", "b1", "a"), ("at", "b2", "a"), ("free", "l"), ("free", "r")])
    return acts, init


def random_task(rng, nf, na):
    facts = list(range(nf))
    acts = []
    for i in range(na):
        pre = rng.sample(facts, rng.randint(0, 2))
        add = rng.sample(facts, rng.randint(1, 2))
        dele = rng.sample([f for f in facts if f not in add], rng.randint(0, 2))
        acts.append(act(("a", i), pre, add, dele))
    init = frozenset(rng.sample(facts, rng.randint(1, nf // 2)))
    return acts, init


def apply_set(s, acts):
    dele = frozenset().union(*(a.dele for a in acts))
    add = frozenset().union(*(a.add for a in acts))
    return (s - dele) | add


def steps(actions, s):
    """All nonempty sets of pairwise non-interfering actions applicable in s."""
    app = [a for a in actions if a.pre <= s]
    out = []

    def grow(i, chosen):
        if chosen:
            out.append(list(chosen))
        for j in range(i, len(app)):
            if all(not interfere(app[j], b) for b in chosen):
                chosen.append(app[j])
                grow(j + 1, chosen)
                chosen.pop()

    grow(0, [])
    return out


def reach_within(actions, init, k):
    """R[t] is the set of states reachable by at most t parallel steps."""
    R = [{frozenset(init)}]
    for _ in range(k):
        nxt = set(R[-1])
        for s in R[-1]:
            for st in steps(actions, s):
                nxt.add(apply_set(s, st))
        R.append(nxt)
    return R


def check_sound(actions, init, K):
    g = PlanningGraph(actions, init)
    for _ in range(K):
        g.expand()
    R = reach_within(actions, init, K)
    for k in range(K + 1):
        for s in R[k]:
            assert s <= g.P[k]
            for p, q in combinations(sorted(s, key=repr), 2):
                assert pair(p, q) not in g.FM[k]
            if k < K:
                level = set(g.A[k])
                for st in steps(actions, s):
                    for a in st:
                        assert a in level
                    for a, b in combinations(st, 2):
                        assert pair(a, b) not in g.AM[k]


def test_mutexes_are_sound_on_random_tasks():
    for seed in range(40):
        rng = random.Random(seed)
        acts, init = random_task(rng, rng.randint(4, 8), rng.randint(4, 8))
        check_sound(acts, init, 4)


def test_mutexes_are_sound_on_blocks_and_gripper():
    acts = blocks(["A", "B", "C"])
    init = frozenset([("on", "A", "B"), ("ontable", "B"), ("ontable", "C"), ("clear", "A"), ("clear", "C"), "handempty"])
    check_sound(acts, init, 5)
    acts, init = gripper()
    check_sound(acts, init, 4)


def tokens_task():
    acts = []
    for t in ["t1", "t2"]:
        for x in ["x", "y", "z"]:
            acts.append(act(("put", t, x), [t], [x], [t]))
    acts.append(act("make_u", ["x", "y"], ["u"]))
    acts.append(act("make_v", ["z"], ["v"]))
    return acts, frozenset(["t1", "t2"])


def test_mutexes_are_not_complete():
    acts, init = tokens_task()
    g = PlanningGraph(acts, init).build()
    n = g.level_off_index()
    assert {"u", "v"} <= g.P[n] and pair("u", "v") not in g.FM[n]
    R = reach_within(acts, init, 6)
    assert R[5] == R[6]
    assert any("u" in s for s in R[6]) and any("v" in s for s in R[6])
    assert not any({"u", "v"} <= s for s in R[6])


def test_graph_levels_off_and_is_monotone():
    for seed in range(40):
        rng = random.Random(1000 + seed)
        acts, init = random_task(rng, rng.randint(4, 8), rng.randint(4, 8))
        g = PlanningGraph(acts, init).build()
        n = g.level_off_index()
        assert n is not None and n <= len(acts) + 2 * len(g.P[-1]) ** 2
        for _ in range(3):
            g.expand()
        for k in range(len(g.P) - 1):
            assert g.P[k] <= g.P[k + 1]
            old = {pair(p, q) for p, q in combinations(sorted(g.P[k], key=repr), 2)}
            assert g.FM[k + 1] & old <= g.FM[k]
            if k + 1 < len(g.A):
                assert set(g.A[k]) <= set(g.A[k + 1])
        for k in range(n, len(g.P)):
            assert g.P[k] == g.P[n] and g.FM[k] == g.FM[n]


def test_two_blocks_example():
    acts = blocks(["A", "B"])
    init = frozenset([("ontable", "A"), ("ontable", "B"), ("clear", "A"), ("clear", "B"), "handempty"])
    g = PlanningGraph(acts, init).build(goal=[("on", "A", "B")])
    assert len(g.P) - 1 == 2
    assert [len(p) for p in g.P] == [5, 7, 9]
    assert [len(m) for m in g.FM] == [0, 7, 16]
    assert [sum(1 for a in lv if not a.name[0] == "noop") for lv in g.A] == [2, 6]
    assert [len(m) for m in g.AM] == [7, 54]
    g.build()
    assert g.level_off_index() == 2
    states = reach_within(acts, init, 4)[4]
    assert len(states) == 5
    never = {pair(p, q) for p, q in combinations(sorted(g.P[2], key=repr), 2)
             if not any(p in s and q in s for s in states)}
    assert never == set(g.FM[2])
    assert g.holds([("on", "A", "B")], 2)
    assert pair(("holding", "A"), "handempty") in g.FM[1]
    assert pair(("on", "A", "B"), ("on", "B", "A")) in g.FM[2]
