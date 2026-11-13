# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/planning-as-model-checking/. The authors are listed in prov/N5Z9YX.jsonl.

"""Weak, strong and strong cyclic planning by fixed points, after Cimatti, Pistore, Roveri and Traverso.

A domain is a dict that maps each state to a dict of actions, and each action to
the set of its possible next states (a nondeterministic transition system with
full observation). A policy is a dict from states to sets of actions: a
state-action table. The functions work on explicit sets; a symbolic planner runs
the same fixed points on binary decision diagrams.
"""

from typing import Dict, Hashable, Set, Tuple

State = Hashable
Domain = Dict[State, Dict[object, Set[State]]]
Policy = Dict[State, Set[object]]


def pairs(dom: Domain):
    return {(s, a) for s, acts in dom.items() for a, nxt in acts.items() if nxt}


def weak_preimage(dom: Domain, z: Set[State]):
    """The state-action pairs that can lead into z."""
    return {(s, a) for (s, a) in pairs(dom) if dom[s][a] & z}


def strong_preimage(dom: Domain, z: Set[State]):
    """The state-action pairs that must lead into z."""
    return {(s, a) for (s, a) in pairs(dom) if dom[s][a] <= z}


def _table(sa) -> Policy:
    out: Policy = {}
    for s, a in sa:
        out.setdefault(s, set()).add(a)
    return out


def strong_plan(dom: Domain, goal: Set[State]) -> Tuple[Policy, Dict[State, int]]:
    """Least fixed point: Z_0 = G, Z_{k+1} = Z_k + the states with an action whose outcomes all lie in Z_k.

    Each new state gets the actions that work at the level where it first appears, so the policy
    is acyclic and every run reaches G within the level of its start state."""
    level = {g: 0 for g in goal}  # @line L1
    plan: Policy = {}
    k = 0
    while True:  # @line L2
        z = set(level)
        new = {(s, a) for (s, a) in strong_preimage(dom, z) if s not in z}  # @line L3
        if not new:  # @line L4
            return plan, level
        k += 1
        for s, a in new:  # @line L5
            plan.setdefault(s, set()).add(a)
            level[s] = k


def weak_plan(dom: Domain, goal: Set[State]) -> Tuple[Policy, Dict[State, int]]:
    """Least fixed point with the weak preimage: some run reaches G."""
    level = {g: 0 for g in goal}
    plan: Policy = {}
    k = 0
    while True:
        z = set(level)
        new = {(s, a) for (s, a) in weak_preimage(dom, z) if s not in z}
        if not new:
            return plan, level
        k += 1
        for s, a in new:
            plan.setdefault(s, set()).add(a)
            level[s] = k


def strong_cyclic_plan(dom: Domain, goal: Set[State]) -> Policy:
    """Greatest fixed point: start from all pairs outside G, and repeat two prunings until stable.

    1. Drop the pairs that can lead out of the states that still have a pair (or are goals).
    2. Keep only the pairs from which G can be reached with the remaining pairs.
    Then keep, at each state, the actions that make progress in the weak distance to G, so that
    every run that is fair to the outcomes reaches G."""
    sa = {(s, a) for (s, a) in pairs(dom) if s not in goal}  # @line L6
    while True:  # @line L7
        old = set(sa)  # @line L8
        # pruning 1: outcomes must stay inside the covered states or the goal
        changed = True
        while changed:  # @line L9
            ok = {s for s, _ in sa} | set(goal)
            keep = {(s, a) for (s, a) in sa if dom[s][a] <= ok}
            changed = keep != sa
            sa = keep
        # pruning 2: weak reachability of G with the remaining pairs
        sub = {s: {a: dom[s][a] for (t, a) in sa if t == s} for s in {s for s, _ in sa}}
        _, lev = weak_plan(sub, set(goal))  # @line L10
        sa = {(s, a) for (s, a) in sa if s in lev}  # @line L11
        if sa == old:  # @line L12
            break
    sub = {s: {a: dom[s][a] for (t, a) in sa if t == s} for s in {s for s, _ in sa}}
    plan, lev = weak_plan(sub, set(goal))
    # keep only the actions that can lower the distance to the goal
    return {s: {a for a in acts if any(lev.get(t, 10 ** 9) < lev[s] for t in dom[s][a])} for s, acts in plan.items()}  # @line L13


def reachable_under(dom: Domain, plan: Policy, s0: State, goal: Set[State]):
    """The states that runs of the plan from s0 can visit, stopping at goals."""
    seen, stack = {s0}, [s0]
    while stack:
        s = stack.pop()
        if s in goal:
            continue
        for a in plan.get(s, ()):
            for t in dom[s][a]:
                if t not in seen:
                    seen.add(t)
                    stack.append(t)
    return seen
