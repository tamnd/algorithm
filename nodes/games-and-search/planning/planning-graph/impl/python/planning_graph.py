# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/planning-graph/. The authors are listed in prov/PJJTVQ.jsonl.

"""The planning graph of Blum and Furst, with no-ops and mutexes.

A STRIPS action is Action(name, pre, add, dele), where pre, add and dele are
frozensets of facts. Level k of the graph is the fact set P[k] with the fact
mutexes FM[k]. Between P[k] and P[k + 1] is the action level A[k] with the
action mutexes AM[k]. A mutex is stored as a frozenset of two elements. The
no-op of a fact f has the name ("noop", f), the precondition {f} and the add
list {f}.
"""

from collections import namedtuple

Action = namedtuple("Action", "name pre add dele")


def noop(f):
    return Action(("noop", f), frozenset([f]), frozenset([f]), frozenset())


def is_noop(a):
    return isinstance(a.name, tuple) and len(a.name) == 2 and a.name[0] == "noop"


def interfere(a, b):
    """One action deletes a precondition or an add effect of the other.

    This covers the inconsistent effects rule (one deletes what the other adds)
    and the interference rule of Blum and Furst.
    """
    return bool(a.dele & (b.pre | b.add) or b.dele & (a.pre | a.add))


def pair(x, y):
    return frozenset((x, y))


def _key(x):
    return repr(x)


class PlanningGraph:
    def __init__(self, actions, init):
        self.actions = list(actions)
        self.P = [frozenset(init)]  # @line L14
        self.FM = [frozenset()]
        self.A = []
        self.AM = []

    def mutex_free(self, facts, k):
        """No two of the facts are mutex at fact level k."""
        fm = self.FM[k]
        fs = sorted(facts, key=_key)
        return not any(pair(p, q) in fm for i, p in enumerate(fs) for q in fs[i + 1:])

    def holds(self, goal, k):
        """The goal facts are all in P[k] and pairwise not mutex there."""
        return frozenset(goal) <= self.P[k] and self.mutex_free(goal, k)

    def expand(self):
        """Add the action level A[k] and the fact level P[k + 1]."""
        k = len(self.P) - 1
        P, FM = self.P[k], self.FM[k]
        level = [noop(f) for f in sorted(P, key=_key)]  # @line L1
        for a in self.actions:  # @line L2
            if a.pre <= P and self.mutex_free(a.pre, k):  # @line L3
                level.append(a)
        am = set()  # @line L4
        for i, a in enumerate(level):  # @line L5
            for b in level[i + 1:]:
                if interfere(a, b):  # @line L6
                    am.add(pair(a, b))
                elif any(pair(p, q) in FM for p in a.pre for q in b.pre if p != q):  # @line L7
                    am.add(pair(a, b))
        achievers = {}
        for a in level:
            for f in a.add:
                achievers.setdefault(f, []).append(a)
        new_p = frozenset(achievers)  # @line L8
        fm = set()  # @line L9
        facts = sorted(new_p, key=_key)
        for i, p in enumerate(facts):  # @line L10
            for q in facts[i + 1:]:
                if all(a != b and pair(a, b) in am for a in achievers[p] for b in achievers[q]):  # @line L11
                    fm.add(pair(p, q))  # @line L12
        self.A.append(level)
        self.AM.append(frozenset(am))
        self.P.append(new_p)
        self.FM.append(frozenset(fm))
        return level, am, new_p, fm  # @line L13

    def leveled_off(self):
        """The last two fact levels have the same facts and the same mutexes."""
        return len(self.P) >= 2 and self.P[-1] == self.P[-2] and self.FM[-1] == self.FM[-2]

    def build(self, goal=None, limit=1000):
        """Expand until the goal holds at the last level or the graph levels off."""
        while not (goal is not None and self.holds(goal, len(self.P) - 1)) and not self.leveled_off():  # @line L15
            if len(self.P) > limit:
                raise RuntimeError("level limit reached")
            self.expand()  # @line L16
        return self  # @line L17

    def level_off_index(self):
        """The first level n with P[n] = P[n + 1] and FM[n] = FM[n + 1], or None."""
        for n in range(len(self.P) - 1):
            if self.P[n] == self.P[n + 1] and self.FM[n] == self.FM[n + 1]:
                return n
        return None
