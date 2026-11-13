# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mutex-relation/. The authors are listed in prov/GRM387.jsonl.

"""Mutex pairs of facts and actions, computed level by level as in a planning graph.

A STRIPS action is Action(name, pre, add, dele) with frozensets of facts. The
function mutex_levels returns, for each fact level k, the set of fact pairs
marked mutex at level k, and for each action level the set of action pairs.
The pairs at the level-off point are invariants: no reachable state holds both
facts of such a pair.
"""

from collections import namedtuple

Action = namedtuple("Action", "name pre add dele")


def pair(x, y):
    return frozenset((x, y))


def noop(f):
    return Action(("noop", f), frozenset([f]), frozenset([f]), frozenset())


def inconsistent_effects(a, b):
    return bool(a.dele & b.add or b.dele & a.add)


def interference(a, b):
    return bool(a.dele & b.pre or b.dele & a.pre)


def competing_needs(a, b, fact_mutex):
    return any(pair(p, q) in fact_mutex for p in a.pre for q in b.pre if p != q)


def action_mutex(a, b, fact_mutex):
    """The three action rules: inconsistent effects, interference, competing needs."""
    return inconsistent_effects(a, b) or interference(a, b) or competing_needs(a, b, fact_mutex)


def fact_mutex_rule(p, q, achievers, am):
    """Every achiever of p is mutex with every achiever of q, and none adds both."""
    return all(a != b and pair(a, b) in am for a in achievers[p] for b in achievers[q])


def mutex_levels(actions, init, max_levels=10000):
    """Return (P, FM, AM): fact sets, fact mutexes and action mutexes per level, to the level off."""
    P, FM, AM = [frozenset(init)], [frozenset()], []
    while len(P) < max_levels:
        facts, fm = P[-1], FM[-1]
        level = [noop(f) for f in sorted(facts, key=repr)]
        for a in actions:
            if a.pre <= facts and not any(pair(p, q) in fm for p in a.pre for q in a.pre if p != q):
                level.append(a)
        am = {pair(a, b) for i, a in enumerate(level) for b in level[i + 1:] if action_mutex(a, b, fm)}
        achievers = {}
        for a in level:
            for f in a.add:
                achievers.setdefault(f, []).append(a)
        order = sorted(achievers, key=repr)
        new_fm = frozenset(pair(p, q) for i, p in enumerate(order) for q in order[i + 1:]
                           if fact_mutex_rule(p, q, achievers, am))
        AM.append(frozenset(am))
        P.append(frozenset(achievers))
        FM.append(new_fm)
        if P[-1] == P[-2] and FM[-1] == FM[-2]:
            return P, FM, AM
    raise RuntimeError("no level off within the limit")


def invariant_mutexes(actions, init):
    """Fact pairs that are mutex once the graph has leveled off."""
    P, FM, _ = mutex_levels(actions, init)
    return P[-1], FM[-1]
