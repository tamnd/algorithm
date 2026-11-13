# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/landmark-heuristic/. The authors are listed in prov/SVVVV7.jsonl.

import math
import random
from collections import deque
from fractions import Fraction

from landmark_heuristic import (Action, PathLandmarkCount, cost_partitioning, fact_landmarks,
                                is_landmark_by_relaxation, landmark_count, natural_orderings, relaxed_reachable)


def act(name, pre, add, dele=()):
    return Action(name, frozenset(pre), frozenset(add), frozenset(dele))


def successors(actions, s):
    for a in actions:
        if a.pre <= s:
            yield a, (s - a.dele) | a.add


def reachable(actions, init):
    seen, q = {init}, deque([init])
    while q:
        s = q.popleft()
        for _, t in successors(actions, s):
            if t not in seen:
                seen.add(t)
                q.append(t)
    return seen


def goal_distances(actions, states, goal):
    """h* on every reachable state, by breadth-first search backward over the reachable graph."""
    pred = {s: [] for s in states}
    for s in states:
        for _, t in successors(actions, s):
            pred[t].append(s)
    dist = {s: 0 for s in states if goal <= s}
    q = deque(dist)
    while q:
        t = q.popleft()
        for s in pred[t]:
            if s not in dist:
                dist[s] = dist[t] + 1
                q.append(s)
    return {s: dist.get(s, math.inf) for s in states}


def h_plus(actions, state, goal):
    """The optimal relaxed plan length, by breadth-first search over relaxed states."""
    rel = [act(a.name, a.pre, a.add) for a in actions]
    return goal_distances(rel, reachable(rel, state), goal)[state]


def simple_plans(actions, init, goal):
    """The state sequences of all plans that never repeat a state."""
    out, states = [], [init]

    def dfs(s):
        if goal <= s:
            out.append(list(states))
            return
        for _, t in successors(actions, s):
            if t not in states:
                states.append(t)
                dfs(t)
                states.pop()

    dfs(init)
    return out


def exact_landmark(actions, init, goal, fact):
    """True when no plan avoids the fact: the goal is unreachable through states without it."""
    if fact in init:
        return True
    seen, q = {init}, deque([init])
    while q:
        s = q.popleft()
        if goal <= s:
            return False
        for _, t in successors(actions, s):
            if fact not in t and t not in seen:
                seen.add(t)
                q.append(t)
    return True


def random_task(rng):
    nf = rng.randint(4, 7)
    facts = list(range(nf))
    acts = []
    for i in range(rng.randint(3, 7)):
        pre = rng.sample(facts, rng.randint(0, 2))
        add = rng.sample(facts, rng.randint(1, 2))
        dele = rng.sample([f for f in facts if f not in add], rng.randint(0, 2))
        acts.append(act(("a", i), pre, add, dele))
    return acts, frozenset(rng.sample(facts, rng.randint(1, nf // 2))), frozenset(rng.sample(facts, rng.randint(1, 3)))


def all_facts(acts, init, goal):
    facts = set(init) | set(goal)
    for a in acts:
        facts |= a.pre | a.add | a.dele
    return facts


def blocks(names):
    acts = []
    for x in names:
        acts.append(act(("pickup", x), [("clear", x), ("ontable", x), "he"], [("holding", x)],
                        [("clear", x), ("ontable", x), "he"]))
        acts.append(act(("putdown", x), [("holding", x)], [("clear", x), ("ontable", x), "he"], [("holding", x)]))
        for y in names:
            if x != y:
                acts.append(act(("stack", x, y), [("holding", x), ("clear", y)],
                                [("on", x, y), ("clear", x), "he"], [("holding", x), ("clear", y)]))
                acts.append(act(("unstack", x, y), [("on", x, y), ("clear", x), "he"],
                                [("holding", x), ("clear", y)], [("on", x, y), ("clear", x), "he"]))
    init = frozenset([("ontable", x) for x in names] + [("clear", x) for x in names] + ["he"])
    return acts, init


def logistics():
    """One package at A; a truck serves A and the airport B; a plane flies between B and E; the goal is at E."""
    acts = [act(("drive", "A", "B"), [("truck", "A")], [("truck", "B")], [("truck", "A")]),
            act(("drive", "B", "A"), [("truck", "B")], [("truck", "A")], [("truck", "B")]),
            act(("fly", "B", "E"), [("plane", "B")], [("plane", "E")], [("plane", "B")]),
            act(("fly", "E", "B"), [("plane", "E")], [("plane", "B")], [("plane", "E")])]
    for x in ["A", "B"]:
        acts.append(act(("load-truck", x), [("pkg", x), ("truck", x)], [("pkg", "truck")], [("pkg", x)]))
        acts.append(act(("unload-truck", x), [("pkg", "truck"), ("truck", x)], [("pkg", x)], [("pkg", "truck")]))
    for x in ["B", "E"]:
        acts.append(act(("load-plane", x), [("pkg", x), ("plane", x)], [("pkg", "plane")], [("pkg", x)]))
        acts.append(act(("unload-plane", x), [("pkg", "plane"), ("plane", x)], [("pkg", x)], [("pkg", "plane")]))
    return acts, frozenset([("pkg", "A"), ("truck", "A"), ("plane", "E")]), frozenset([("pkg", "E")])


def test_landmarks_are_true_on_every_plan():
    """Every plan contains a plan with no repeated state among its states, so checking these plans suffices."""
    solvable = plans_seen = found = exact = 0
    for seed in range(600):
        rng = random.Random(seed)
        acts, init, goal = random_task(rng)
        marks = fact_landmarks(acts, init, goal)
        if marks is None:
            assert not relaxed_reachable(acts, init, goal)
            continue
        plans = simple_plans(acts, init, goal)
        if not plans:
            continue
        solvable += 1
        plans_seen += len(plans)
        facts = all_facts(acts, init, goal)
        tested = frozenset(f for f in facts if is_landmark_by_relaxation(acts, init, goal, f))
        assert marks <= tested
        for plan in plans:
            for l in tested:
                assert any(l in s for s in plan)
            for l, m in natural_orderings(acts, init, goal):
                first = next(i for i, s in enumerate(plan) if m in s)
                assert any(l in s for s in plan[:first])
        real = {f for f in facts if exact_landmark(acts, init, goal, f)}
        assert tested <= real
        found += len(marks - init)
        exact += len(real - init)
    assert solvable > 250 and plans_seen > 2000 and found < exact


def test_fixed_point_finds_exactly_the_causal_landmarks_of_the_relaxed_task():
    """A fact outside the state is a causal landmark of the relaxed task if it is a goal, or if no relaxed
    plan avoids using it as a precondition."""
    for seed in range(600):
        rng = random.Random(10_000 + seed)
        acts, init, goal = random_task(rng)
        marks = fact_landmarks(acts, init, goal)
        if marks is None:
            continue
        causal = {f for f in all_facts(acts, init, goal) - init
                  if f in goal or not relaxed_reachable([a for a in acts if f not in a.pre], init, goal)}
        assert marks - init == causal


def test_heuristic_values_against_breadth_first_search():
    over = 0
    for seed in range(600):
        rng = random.Random(seed)
        acts, init, goal = random_task(rng)
        states = reachable(acts, init)
        dist = goal_distances(acts, states, goal)
        for s in states:
            c, u = landmark_count(acts, s, goal), cost_partitioning(acts, s, goal)
            assert (c == 0) == (goal <= s) == (u == 0)
            assert (c == math.inf) == (not relaxed_reachable(acts, s, goal)) == (u == math.inf)
            if c == math.inf:
                assert dist[s] == math.inf
            assert u <= dist[s] and u <= c
            over += c > dist[s]
        u = cost_partitioning(acts, init, goal)
        assert u <= h_plus(acts, init, goal)
    assert over > 0


def test_one_action_that_adds_two_landmarks():
    acts = [act("ab", [], ["p", "q"]), act("g", ["p", "q"], ["g"])]
    init, goal = frozenset(), frozenset(["g"])
    assert fact_landmarks(acts, init, goal) == {"p", "q", "g"}
    assert landmark_count(acts, init, goal) == 3
    assert cost_partitioning(acts, init, goal) == 2
    assert goal_distances(acts, reachable(acts, init), goal)[init] == 2


def test_the_relaxation_misses_a_landmark():
    acts = [act("work", ["home"], ["job"], ["home"]), act("call", ["job"], ["taxi"]), act("ride", ["taxi"], ["home"])]
    init, goal = frozenset(["home"]), frozenset(["job", "home"])
    assert fact_landmarks(acts, init, goal) == {"home", "job"}
    assert not is_landmark_by_relaxation(acts, init, goal, "taxi")
    assert exact_landmark(acts, init, goal, "taxi")
    assert landmark_count(acts, init, goal) == 1
    assert goal_distances(acts, reachable(acts, init), goal)[init] == 3


def test_logistics_landmarks_and_orderings():
    acts, init, goal = logistics()
    marks = fact_landmarks(acts, init, goal)
    assert marks - init == {("pkg", "truck"), ("truck", "B"), ("pkg", "B"), ("plane", "B"), ("pkg", "plane"),
                            ("pkg", "E")}
    order = natural_orderings(acts, init, goal)
    assert (("pkg", "truck"), ("pkg", "B")) in order and (("pkg", "B"), ("pkg", "plane")) in order
    assert (("pkg", "plane"), ("pkg", "E")) in order
    assert landmark_count(acts, init, goal) == 6 == h_plus(acts, init, goal)
    assert goal_distances(acts, reachable(acts, init), goal)[init] == 7


def test_blocks_world():
    acts, init = blocks(["A", "B", "C"])
    goal = frozenset([("on", "A", "B"), ("on", "B", "C")])
    assert fact_landmarks(acts, init, goal) - init == {("holding", "A"), ("holding", "B"), ("on", "A", "B"),
                                                       ("on", "B", "C")}
    states = reachable(acts, init)
    dist = goal_distances(acts, states, goal)
    assert landmark_count(acts, init, goal) == cost_partitioning(acts, init, goal) == dist[init] == 4
    counts = [sum(cmp(landmark_count(acts, s, goal), dist[s]) == k for s in states) for k in (-1, 0, 1)]
    assert counts == [13, 5, 4]
    assert all(cost_partitioning(acts, s, goal) <= dist[s] for s in states)


def cmp(x, y):
    return (x > y) - (x < y)


def test_path_count_is_zero_at_the_end_of_every_plan():
    for seed in range(300):
        rng = random.Random(seed)
        acts, init, goal = random_task(rng)
        h = PathLandmarkCount(acts, init, goal)
        start = h.accept(None, init)
        assert h.value(start, init) == landmark_count(acts, init, goal)
        if h.marks is None:
            continue
        for plan in simple_plans(acts, init, goal)[:50]:
            accepted = start
            for s in plan[1:]:
                accepted = h.accept(accepted, s)
                assert isinstance(h.value(accepted, s), int)
            assert h.value(accepted, plan[-1]) == 0


def test_cost_partitioning_is_exact_on_fractions():
    acts = [act("pq", [], ["p", "q"]), act("qr", [], ["q", "r"]), act("g", ["p", "q", "r"], ["g"])]
    init, goal = frozenset(), frozenset(["g"])
    assert cost_partitioning(acts, init, goal) == Fraction(5, 2)
    assert landmark_count(acts, init, goal) == 4
    assert goal_distances(acts, reachable(acts, init), goal)[init] == 3
