# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/enforced-hill-climbing/. The authors are listed in prov/K6E90E.jsonl.

import heapq
import math
import random
from collections import deque, namedtuple

from enforced_hill_climbing import enforced_hill_climbing

Action = namedtuple("Action", "name pre add dele")


def act(name, pre, add, dele=()):
    return Action(name, frozenset(pre), frozenset(add), frozenset(dele))


def h_ff(actions, state, goal):
    """The FF heuristic: the length of a relaxed plan from the relaxed planning graph."""
    level, layers, facts, used = {f: 0 for f in state}, [], frozenset(state), set()
    while not goal <= facts:
        layer = [j for j, a in enumerate(actions) if j not in used and a.pre <= facts]
        new = frozenset(f for j in layer for f in actions[j].add) - facts
        if not new:
            return math.inf
        used.update(layer)
        for f in new:
            level[f] = len(layers) + 1
        layers.append(layer)
        facts |= new
    m = len(layers)
    goals = [set() for _ in range(m + 1)]
    need, pos, count = {}, {}, [0] * (m + 1)
    for g in goal:
        goals[level[g]].add(g)
        need[g] = (m, 0)
    for i in range(m, 0, -1):
        for g in sorted(goals[i], key=repr):
            if any(p < need[g] and g in actions[j].add for j, p in pos.items()):
                continue
            o = min((j for j in layers[i - 1] if g in actions[j].add),
                    key=lambda j: (sum(level[p] for p in actions[j].pre), j))
            pos[o] = (i - 1, count[i - 1])
            count[i - 1] += 1
            for p in actions[o].pre:
                if level[p] >= 1:
                    goals[level[p]].add(p)
                    need[p] = min(need.get(p, (m + 1, 0)), pos[o])
    return len(pos)


def problem(actions, goal):
    goal = frozenset(goal)

    def successors(s):
        for a in actions:
            if a.pre <= s:
                yield a, (s - a.dele) | a.add

    return successors, (lambda s: h_ff(actions, s, goal)), (lambda s: goal <= s)


def valid(actions, init, goal, plan):
    s = init
    for a in plan:
        if a not in actions or not a.pre <= s:
            return False
        s = (s - a.dele) | a.add
    return goal <= s


def reachable(actions, init):
    seen, q = {init}, deque([init])
    while q:
        s = q.popleft()
        for a in actions:
            if a.pre <= s:
                t = (s - a.dele) | a.add
                if t not in seen:
                    seen.add(t)
                    q.append(t)
    return seen


def goal_distances(actions, states, goal):
    pred = {s: [] for s in states}
    for s in states:
        for a in actions:
            if a.pre <= s:
                pred[(s - a.dele) | a.add].append(s)
    d = {s: 0 for s in states if goal <= s}
    q = deque(d)
    while q:
        t = q.popleft()
        for s in pred[t]:
            if s not in d:
                d[s] = d[t] + 1
                q.append(s)
    return {s: d.get(s, math.inf) for s in states}


def greedy_best_first(init, successors, h, is_goal):
    """Complete greedy best-first search, the fallback of FF."""
    tie = 0
    heap, parent = [(h(init), tie, init)], {init: None}
    while heap:
        hs, _, s = heapq.heappop(heap)
        if is_goal(s):
            plan = []
            while parent[s] is not None:
                s, a = parent[s]
                plan.append(a)
            return plan[::-1]
        for a, t in successors(s):
            if t not in parent:
                parent[t] = (s, a)
                ht = h(t)
                if ht < math.inf:
                    tie += 1
                    heapq.heappush(heap, (ht, tie, t))
    return None


def steepest_hill_climbing(init, successors, h, is_goal):
    """Plain hill climbing: move to the best strictly better neighbor, stop when there is none."""
    s, plan = init, []
    while not is_goal(s):
        best = min(((h(t), repr(a.name), a, t) for a, t in successors(s)), default=None, key=lambda x: x[:2])
        if best is None or best[0] >= h(s):
            return None
        plan.append(best[2])
        s = best[3]
    return plan


def random_task(rng):
    nf = rng.randint(4, 8)
    facts = list(range(nf))
    acts = []
    for i in range(rng.randint(4, 8)):
        pre = rng.sample(facts, rng.randint(0, 2))
        add = rng.sample(facts, rng.randint(1, 2))
        dele = rng.sample([f for f in facts if f not in add], rng.randint(0, 2))
        acts.append(act(("a", i), pre, add, dele))
    return acts, frozenset(rng.sample(facts, rng.randint(1, nf // 2))), frozenset(rng.sample(facts, rng.randint(1, 3)))


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


def trap_task():
    """A real route of 5 actions, and a trap that looks one step better and leads to dead ends."""
    acts = [act(("r", i), [("r", i)], [("r", i + 1)], [("r", i)]) for i in range(4)]
    acts.append(act("finish_route", [("r", 4)], ["g"], [("r", 4)]))
    acts.append(act("to_trap", [("r", 0)], ["u"], [("r", 0)]))
    acts.append(act("ap", ["u"], ["p"], ["u"]))
    acts.append(act("aq", ["u"], ["q"], ["u"]))
    acts.append(act("finish", ["p", "q"], ["g"]))
    return acts, frozenset([("r", 0)]), frozenset(["g"])


def test_random_tasks_against_breadth_first_oracle():
    runs = solved = dead_end_free = 0
    for seed in range(600):
        rng = random.Random(seed)
        acts, init, goal = random_task(rng)
        succ, h, is_goal = problem(acts, goal)
        stats = {}
        plan = enforced_hill_climbing(init, succ, h, is_goal, stats)
        states = reachable(acts, init)
        dist = goal_distances(acts, states, goal)
        runs += 1
        if plan is not None:
            solved += 1
            assert valid(acts, init, goal, plan)
            assert len(plan) >= dist[init]
            assert len(stats["depths"]) <= h(init)
        else:
            assert any(d == math.inf for d in dist.values())
        if all(d < math.inf for d in dist.values()):
            dead_end_free += 1
            assert plan is not None
    assert runs == 600 and solved > 100 and dead_end_free > 50


def test_dead_end_trap_fails_and_best_first_finds_a_plan():
    acts, init, goal = trap_task()
    succ, h, is_goal = problem(acts, goal)
    assert h(init) == 4 and h(frozenset(["u"])) == 3
    assert h(frozenset(["p"])) == math.inf and h(frozenset(["q"])) == math.inf
    assert enforced_hill_climbing(init, succ, h, is_goal) is None
    plan = greedy_best_first(init, succ, h, is_goal)
    assert plan is not None and valid(acts, init, goal, plan) and len(plan) == 5


def test_plateau_is_left_by_breadth_first_search():
    # Hoffmann and Nebel (2001), Section 6.1.1: every neighbor of the initial state has the same value.
    acts = [act("opA1", [], ["A"], ["B"]), act("opA2", ["PA"], ["A"]), act("opPA", [], ["PA"]),
            act("opB1", [], ["B"], ["A"]), act("opB2", ["PB"], ["B"]), act("opPB", [], ["PB"])]
    init, goal = frozenset(["B"]), frozenset(["A", "B"])
    succ, h, is_goal = problem(acts, goal)
    assert h(init) == 1 and all(h(t) >= 1 for _, t in succ(init) if not is_goal(t))
    assert steepest_hill_climbing(init, succ, h, is_goal) is None
    stats = {}
    plan = enforced_hill_climbing(init, succ, h, is_goal, stats)
    assert [a.name for a in plan] == ["opPA", "opA2"] and stats["depths"] == [2]


def test_blocks_world_from_every_state():
    for names in (["A", "B", "C"], ["A", "B", "C", "D"]):
        acts, table = blocks(names)
        goal = frozenset(("on", names[i], names[i + 1]) for i in range(len(names) - 1))
        succ, h, is_goal = problem(acts, goal)
        states = reachable(acts, table)
        dist = goal_distances(acts, states, goal)
        longer = 0
        for s in sorted(states, key=lambda s: sorted(map(repr, s))):
            plan = enforced_hill_climbing(s, succ, h, is_goal)
            assert plan is not None and valid(acts, s, goal, plan)
            longer += len(plan) > dist[s]
        assert longer > 0 or len(names) == 3


def test_goal_state_and_unreachable_goal():
    acts = [act("a", ["p"], ["q"])]
    succ, h, is_goal = problem(acts, ["q"])
    assert enforced_hill_climbing(frozenset(["q"]), succ, h, is_goal) == []
    assert enforced_hill_climbing(frozenset(["r"]), succ, h, is_goal) is None
    assert [a.name for a in enforced_hill_climbing(frozenset(["p"]), succ, h, is_goal)] == ["a"]
