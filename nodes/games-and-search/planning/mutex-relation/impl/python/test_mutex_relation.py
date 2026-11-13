# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mutex-relation/. The authors are listed in prov/GRM387.jsonl.

import random
from collections import deque
from itertools import combinations

from mutex_relation import Action, invariant_mutexes, mutex_levels, pair


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


def table(names):
    return frozenset([("ontable", x) for x in names] + [("clear", x) for x in names] + ["handempty"])


def random_task(rng, nf, na):
    facts = list(range(nf))
    acts = []
    for i in range(na):
        pre = rng.sample(facts, rng.randint(0, 2))
        add = rng.sample(facts, rng.randint(1, 2))
        dele = rng.sample([f for f in facts if f not in add], rng.randint(0, 2))
        acts.append(act(("a", i), pre, add, dele))
    return acts, frozenset(rng.sample(facts, rng.randint(1, nf // 2)))


def bfs_depths(actions, init):
    """Map each reachable state to its BFS depth (the fewest sequential actions)."""
    depth = {init: 0}
    q = deque([init])
    while q:
        s = q.popleft()
        for a in actions:
            if a.pre <= s:
                t = (s - a.dele) | a.add
                if t not in depth:
                    depth[t] = depth[s] + 1
                    q.append(t)
    return depth


def never_together(states, facts):
    fs = sorted(facts, key=repr)
    return {pair(p, q) for p, q in combinations(fs, 2) if not any(p in s and q in s for s in states)}


def test_sound_at_every_level_on_random_tasks():
    for seed in range(60):
        rng = random.Random(seed)
        acts, init = random_task(rng, rng.randint(4, 8), rng.randint(4, 8))
        P, FM, _ = mutex_levels(acts, init)
        for s, d in bfs_depths(acts, init).items():
            for k in range(d, len(P)):
                assert s <= P[k]
                assert not any(pair(p, q) in FM[k] for p, q in combinations(sorted(s), 2))


def test_invariants_on_blocks_world():
    for names, n_states in ((["A", "B", "C"], 22), (["A", "B", "C", "D"], 125)):
        acts = blocks(names)
        facts, fm = invariant_mutexes(acts, table(names))
        states = bfs_depths(acts, table(names))
        assert len(states) == n_states
        truth = never_together(states, facts)
        assert fm <= truth
        assert fm == truth


def test_not_complete_with_two_tokens():
    acts = [act(("put", t, x), [t], [x], [t]) for t in ["t1", "t2"] for x in ["x", "y", "z"]]
    acts += [act("make_u", ["x", "y"], ["u"]), act("make_v", ["z"], ["v"])]
    init = frozenset(["t1", "t2"])
    facts, fm = invariant_mutexes(acts, init)
    states = bfs_depths(acts, init)
    truth = never_together(states, facts)
    assert fm < truth
    assert pair("u", "v") in truth and pair("u", "v") not in fm
    assert sorted(len(s) for s in states).count(0) == 0


def test_mutexes_only_disappear():
    for seed in range(40):
        rng = random.Random(500 + seed)
        acts, init = random_task(rng, rng.randint(4, 8), rng.randint(4, 8))
        P, FM, AM = mutex_levels(acts, init)
        for k in range(len(P) - 1):
            old = {pair(p, q) for p, q in combinations(sorted(P[k]), 2)}
            assert FM[k + 1] & old <= FM[k]
