# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/replanning/. The authors are listed in prov/S4BFGJ.jsonl.

"""Replanning: plan in a simple model, act, and plan again when the world does not follow it.

A probabilistic domain maps each state to a dict of actions, and each action to a list of
(probability, next state) pairs. The all-outcomes determinization turns each outcome into a
deterministic action, as in FF-Replan. A deterministic domain maps each state to a dict from
actions to next states. A plan is a list of (action, expected next state) pairs.
"""

from collections import deque
from typing import Dict, Hashable, List, Optional, Sequence, Tuple

State = Hashable
Step = Tuple[object, State]


def all_outcomes(dom) -> Dict[State, Dict[object, State]]:
    """Each outcome of each action becomes its own deterministic action (a, i)."""
    return {s: {(a, i): t for a, outs in sorted(acts.items(), key=repr) for i, (p, t) in enumerate(outs) if p > 0}
            for s, acts in dom.items()}


def most_likely(dom) -> Dict[State, Dict[object, State]]:
    """Each action keeps only its most likely outcome (the first one on ties)."""
    out = {}
    for s, acts in dom.items():
        out[s] = {}
        for a, outs in sorted(acts.items(), key=repr):
            best = max(range(len(outs)), key=lambda i: (outs[i][0], -i))
            out[s][(a, best)] = outs[best][1]
    return out


def bfs_plan(det, s0: State, goal) -> Optional[List[Step]]:
    """A shortest plan in a deterministic domain, with a fixed order of actions."""
    if s0 in goal:
        return []
    parent = {s0: None}
    q = deque([s0])
    while q:
        s = q.popleft()
        for a, t in det.get(s, {}).items():
            if t not in parent:
                parent[t] = (s, a)
                if t in goal:
                    plan = []
                    while parent[t] is not None:
                        u, b = parent[t]
                        plan.append((b, t))
                        t = u
                    return plan[::-1]
                q.append(t)
    return None


class Replanner:
    """Follow the current plan while the observed state is the expected one; else plan again.

    det is a determinization, whose actions are pairs (real action, outcome index)."""

    def __init__(self, det, goal):
        self.det, self.goal = det, set(goal)
        self.expected, self.rest = None, []
        self.calls = 0

    def memory(self):
        return self.expected, tuple(self.rest)

    def act(self, s: State):
        """The next real action, or None if the model has no plan from s."""
        if s != self.expected or not self.rest:
            self.calls += 1
            plan = bfs_plan(self.det, s, self.goal)
            if plan is None:
                return None
            self.rest = plan
        (a, _), t = self.rest[0]
        self.expected, self.rest = t, self.rest[1:]
        return a


def run(dom, det, s0: State, goal, rng, limit: int = 1000):
    """Simulate the replanner in the real probabilistic domain. Returns (reached, steps, planner calls)."""
    agent, s = Replanner(det, goal), s0
    for k in range(limit):
        if s in goal:
            return True, k, agent.calls
        a = agent.act(s)
        if a is None:
            return False, k, agent.calls
        r, acc = rng.random(), 0.0
        for p, t in dom[s][a]:
            acc += float(p)
            if r < acc:
                s = t
                break
        else:
            s = dom[s][a][-1][1]
    return s in goal, limit, agent.calls


def repair(det, plan: Sequence[Step], start: State, s: State, goal) -> Optional[List[Step]]:
    """Plan repair by reconnection: reach, by a shortest path from s, a state from which a suffix of
    the old plan works, and then follow that suffix. Falls back to planning from scratch."""
    states = [start] + [t for _, t in plan]
    entry = {}
    for k in range(len(plan), -1, -1):
        # the state before step k of the old plan, and the suffix from there
        entry.setdefault(states[k], list(plan[k:]))
    if s in entry:
        return entry[s]
    bridge = bfs_plan(det, s, set(entry))
    if bridge is None:
        return bfs_plan(det, s, goal)
    return bridge + entry[bridge[-1][1]]


def is_plan(det, s: State, plan: Sequence[Step], goal) -> bool:
    for a, t in plan:
        if det.get(s, {}).get(a) != t:
            return False
        s = t
    return s in goal


def stability_distance(p, q) -> int:
    """Fox et al.: the number of actions in one plan and not in the other, counted with multiplicity."""
    from collections import Counter
    cp, cq = Counter(a for a, _ in p), Counter(a for a, _ in q)
    return sum((cp - cq).values()) + sum((cq - cp).values())
