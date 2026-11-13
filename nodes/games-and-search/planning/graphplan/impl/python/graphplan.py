# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/graphplan/. The authors are listed in prov/RD7TS9.jsonl.

"""GRAPHPLAN of Blum and Furst: a planning graph plus a memoized backward search.

A STRIPS action is Action(name, pre, add, dele) with frozensets of facts. The
function graphplan returns a parallel plan, a list of steps where each step is
a list of actions, or None when no plan exists. The plan has the fewest
parallel steps of all plans. Two actions may share a step when neither deletes
a precondition or an add effect of the other.
"""

from collections import namedtuple

Action = namedtuple("Action", "name pre add dele")


def noop(f):
    return Action(("noop", f), frozenset([f]), frozenset([f]), frozenset())


def is_noop(a):
    return isinstance(a.name, tuple) and len(a.name) == 2 and a.name[0] == "noop"


def interfere(a, b):
    return bool(a.dele & (b.pre | b.add) or b.dele & (a.pre | a.add))


def pair(x, y):
    return frozenset((x, y))


class Graph:
    """Fact levels P, fact mutexes FM, action levels A, action mutexes AM, achievers."""

    def __init__(self, actions, init):
        self.actions = list(actions)
        self.P, self.FM, self.A, self.AM, self.ach = [frozenset(init)], [frozenset()], [], [], []

    def mutex_free(self, facts, k):
        fs = sorted(facts, key=repr)
        return not any(pair(p, q) in self.FM[k] for i, p in enumerate(fs) for q in fs[i + 1:])

    def holds(self, goal, k):
        return goal <= self.P[k] and self.mutex_free(goal, k)

    def expand(self):
        k = len(self.P) - 1
        P, FM = self.P[k], self.FM[k]
        level = [noop(f) for f in sorted(P, key=repr)]
        level += [a for a in self.actions if a.pre <= P and self.mutex_free(a.pre, k)]
        am = set()
        for i, a in enumerate(level):
            for b in level[i + 1:]:
                if interfere(a, b) or any(pair(p, q) in FM for p in a.pre for q in b.pre if p != q):
                    am.add(pair(a, b))
        ach = {}
        for a in level:
            for f in a.add:
                ach.setdefault(f, []).append(a)
        facts = sorted(ach, key=repr)
        fm = {pair(p, q) for i, p in enumerate(facts) for q in facts[i + 1:]
              if all(a != b and pair(a, b) in am for a in ach[p] for b in ach[q])}
        self.A.append(level)
        self.AM.append(frozenset(am))
        self.ach.append(ach)
        self.P.append(frozenset(ach))
        self.FM.append(frozenset(fm))

    def level_off(self):
        """The first n with P[n] = P[n + 1] and FM[n] = FM[n + 1], or None."""
        for n in range(len(self.P) - 1):
            if self.P[n] == self.P[n + 1] and self.FM[n] == self.FM[n + 1]:
                return n
        return None


def graphplan(actions, init, goal, stats=None):
    """Return a plan with the fewest parallel steps, or None if no plan exists."""
    goal = frozenset(goal)
    g = Graph(actions, init)
    while not g.holds(goal, len(g.P) - 1) and g.level_off() is None:  # @line L1
        g.expand()
    k = len(g.P) - 1
    if not g.holds(goal, k):  # @line L2
        return _done(stats, k, "graph leveled off without the goal", None)
    nogood = {}  # @line L3
    while True:  # @line L4
        n = g.level_off()
        before = len(nogood.get(n, ())) if n is not None else None
        plan = _extract(g, nogood, goal, k)  # @line L5
        if plan is not None:  # @line L6
            return _done(stats, k, "plan", plan)
        if n is not None and n < k and len(nogood.get(n, ())) == before:  # @line L7
            return _done(stats, k, "nogoods at the level off stopped growing", None)
        g.expand()  # @line L8
        k += 1


def _done(stats, k, reason, plan):
    if stats is not None:
        stats["levels"], stats["reason"] = k, reason
    return plan


def _extract(g, nogood, goals, i):
    if i == 0:  # @line L9
        return []
    if goals in nogood.get(i, ()):  # @line L10
        return None
    for step in _assign(g, sorted(goals, key=repr), i, []):  # @line L11
        sub = frozenset().union(*(a.pre for a in step))
        plan = _extract(g, nogood, sub, i - 1)  # @line L12
        if plan is not None:  # @line L13
            return plan + [[a for a in step if not is_noop(a)]]
    nogood.setdefault(i, set()).add(goals)  # @line L14
    return None


def _assign(g, goals, i, chosen):
    """Yield sets of pairwise non-mutex actions of A[i - 1] that add every goal."""
    open_goals = [f for f in goals if not any(f in a.add for a in chosen)]
    if not open_goals:  # @line L15
        yield list(chosen)
        return
    f = open_goals[0]  # @line L16
    am = g.AM[i - 1]
    for a in sorted(g.ach[i - 1][f], key=lambda a: not is_noop(a)):  # @line L17
        if all(pair(a, b) not in am for b in chosen):  # @line L18
            yield from _assign(g, goals, i, chosen + [a])


def linearize(plan):
    """Any order inside a step is valid; this keeps the order of the steps."""
    return [a for step in plan for a in step]
