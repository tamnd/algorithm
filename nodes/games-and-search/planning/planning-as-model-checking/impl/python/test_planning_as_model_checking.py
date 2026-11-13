# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/planning-as-model-checking/. The authors are listed in prov/N5Z9YX.jsonl.

import random
from itertools import product

from planning_as_model_checking import reachable_under, strong_cyclic_plan, strong_plan, weak_plan


# ---- references by enumeration of memoryless policies ----

def policy_reaches(dom, pol, s, goal, cyclic):
    """Does the one-action policy pol bring s to the goal: always (strong) or under fairness (strong cyclic)?"""
    seen, stack = {s}, [s]
    while stack:
        u = stack.pop()
        if u in goal:
            continue
        if pol.get(u) is None:
            return False
        for t in dom[u][pol[u]]:
            if t not in seen:
                seen.add(t)
                stack.append(t)
    inner = {u for u in seen if u not in goal}
    # every visited state must reach the goal in the graph of the policy
    good = set(goal)
    changed = True
    while changed:
        changed = False
        for u in inner:
            if u not in good and dom[u][pol[u]] & good:
                good.add(u)
                changed = True
    if not inner <= good:
        return False
    if cyclic:
        return True
    # strong: the graph of the policy on the visited states has no cycle
    color = {}

    def dfs(u):
        color[u] = 1
        for t in dom[u][pol[u]]:
            if t in inner:
                if color.get(t) == 1 or (t not in color and not dfs(t)):
                    return False
        color[u] = 2
        return True

    return all(color.get(u) == 2 or dfs(u) for u in inner)


def brute_domain(dom, goal, cyclic):
    states = [s for s in dom if s not in goal]
    choices = [[a for a, n in dom[s].items() if n] + [None] for s in states]
    out = set(goal)
    for pick in product(*choices):
        pol = dict(zip(states, pick))
        for s in states:
            if s not in out and policy_reaches(dom, {u: a for u, a in pol.items() if a is not None}, s, goal, cyclic):
                out.add(s)
    return out


def all_runs_reach(dom, plan, s, goal, k):
    """Every run of the plan from s, with any choice among its actions, is in the goal within k steps."""
    if s in goal:
        return True
    if k == 0 or not plan.get(s):
        return False
    return all(all_runs_reach(dom, plan, t, goal, k - 1) for a in plan[s] for t in dom[s][a])


# ---- examples of the page ----

def robot():
    """A robot picks up a block. pick can fail and leave the block on the table, or drop it on the floor."""
    return {
        "table": {"pick": {"held", "table", "floor"}},
        "floor": {"pick": {"held", "floor"}, "push": {"table"}},
        "held": {},
    }


def test_robot_example():
    dom, goal = robot(), {"held"}
    sp, lev = strong_plan(dom, goal)
    assert sp == {} and lev == {"held": 0}
    wp, wl = weak_plan(dom, goal)
    assert wl == {"held": 0, "table": 1, "floor": 1}
    sc = strong_cyclic_plan(dom, goal)
    assert sc == {"table": {"pick"}, "floor": {"pick"}}


def test_toss_until_heads():
    dom = {"T": {"toss": {"H", "T"}}, "H": {}}
    assert strong_plan(dom, {"H"})[0] == {}
    assert strong_cyclic_plan(dom, {"H"}) == {"T": {"toss"}}


def test_progress_step_drops_a_self_loop():
    dom = {"s": {"a": {"s"}, "b": {"g"}}, "g": {}}
    assert strong_cyclic_plan(dom, {"g"}) == {"s": {"b"}}


def test_strong_plan_with_levels():
    # a corridor 0..3 where the step right is safe from 0 and 1, and the step from 2 can slip back
    dom = {
        0: {"r": {1}},
        1: {"r": {2}, "jump": {3, 2}},
        2: {"r": {3, 1}, "carry": {3}},
        3: {},
    }
    plan, lev = strong_plan(dom, {3})
    assert lev == {3: 0, 2: 1, 1: 2, 0: 3}
    assert plan == {2: {"carry"}, 1: {"r", "jump"}, 0: {"r"}}
    assert all(all_runs_reach(dom, plan, s, {3}, lev[s]) for s in lev)


def random_domain(rng, n, k):
    dom = {}
    for s in range(n):
        dom[s] = {}
        for a in range(k):
            if rng.random() < 0.8:
                dom[s][a] = {t for t in range(n) if rng.random() < 0.3} or {rng.randrange(n)}
    goal = {s for s in range(n) if rng.random() < 0.25} or {n - 1}
    for g in goal:
        dom[g] = {}
    return dom, goal


def test_against_enumeration_of_policies():
    rng = random.Random(17)
    for _ in range(150):
        dom, goal = random_domain(rng, rng.randint(1, 5), rng.randint(1, 3))
        sp, lev = strong_plan(dom, goal)
        assert set(lev) == brute_domain(dom, goal, cyclic=False)
        assert all(all_runs_reach(dom, sp, s, goal, lev[s]) for s in lev)
        sc = strong_cyclic_plan(dom, goal)
        assert set(sc) | goal == brute_domain(dom, goal, cyclic=True)
        for s in sc:
            # closed: the runs stay where the plan is defined, and the goal stays reachable
            reach = reachable_under(dom, sc, s, goal)
            assert all(u in goal or sc.get(u) for u in reach)
            for u in reach:
                assert goal & reachable_under(dom, sc, u, goal)
        _, wl = weak_plan(dom, goal)
        # weak: plain reachability in the graph of all actions
        reach = set(goal)
        changed = True
        while changed:
            changed = False
            for s in dom:
                if s not in reach and any(n & reach for n in dom[s].values()):
                    reach.add(s)
                    changed = True
        assert set(wl) == reach
        assert set(lev) <= set(sc) | goal <= set(wl)
