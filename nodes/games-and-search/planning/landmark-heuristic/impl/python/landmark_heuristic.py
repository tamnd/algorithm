# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/landmark-heuristic/. The authors are listed in prov/SVVVV7.jsonl.

"""Fact landmarks of a STRIPS task and two heuristics built on them.

A STRIPS action is Action(name, pre, add, dele) with frozensets of facts. The
landmarks come from a fixed point over the delete relaxation: LM(f) is the set
of facts that every relaxed derivation of f passes through. The union of LM(g)
over the goals is the set of causal landmarks of the relaxed task, and each of
them is true at some point on every real plan.

landmark_count counts the landmarks that are not true in the state. It is 0
exactly at goal states and is not admissible. cost_partitioning splits the
cost 1 of each action evenly among the open landmarks that it adds, and sums
the cheapest share of each landmark. It is admissible. PathLandmarkCount is
the path-based count of LAMA without orderings: it finds the landmarks once,
from the initial state, and remembers which ones the path has achieved.
"""

import math
from collections import namedtuple
from fractions import Fraction
from typing import Dict, FrozenSet, Hashable, Optional, Sequence, Set, Tuple

Action = namedtuple("Action", "name pre add dele")


def landmark_table(actions: Sequence[Action], state, goal) -> Optional[Dict[Hashable, FrozenSet[Hashable]]]:
    """LM(f) for every fact that is relaxed reachable from the state, or None if some goal is not."""
    state, goal = frozenset(state), frozenset(goal)
    table = {f: frozenset([f]) for f in state}
    changed = True
    while changed:
        changed = False
        for a in actions:
            if not all(p in table for p in a.pre):
                continue
            below = frozenset().union(*(table[p] for p in a.pre))
            for f in a.add:
                if f in state:
                    continue
                new = below | {f}
                if f in table:
                    new = table[f] & new
                if table.get(f) != new:
                    table[f] = new
                    changed = True
    if not all(g in table for g in goal):
        return None
    return table


def fact_landmarks(actions: Sequence[Action], state, goal) -> Optional[FrozenSet[Hashable]]:
    """The causal fact landmarks of the relaxed task from the state, or None if the goal is relaxed unreachable."""
    table = landmark_table(actions, state, goal)
    if table is None:
        return None
    return frozenset().union(*(table[g] for g in goal))


def natural_orderings(actions: Sequence[Action], state, goal) -> Set[Tuple[Hashable, Hashable]]:
    """Pairs (l, m) of landmarks such that l is true at some point before m first becomes true."""
    table = landmark_table(actions, state, goal)
    if table is None:
        return set()
    marks = frozenset().union(*(table[g] for g in goal))
    return {(l, m) for m in marks for l in table[m] if l != m}


def relaxed_reachable(actions: Sequence[Action], state, goal) -> bool:
    facts, changed = set(state), True
    while changed:
        changed = False
        for a in actions:
            if a.pre <= facts and not a.add <= facts:
                facts |= a.add
                changed = True
    return frozenset(goal) <= facts


def is_landmark_by_relaxation(actions: Sequence[Action], state, goal, fact) -> bool:
    """Proposition 1 of Hoffmann, Porteous and Sebastia (2004): a sufficient test for a fact landmark."""
    if fact in state:
        return True
    return not relaxed_reachable([a for a in actions if fact not in a.add], state, goal)


def landmark_count(actions: Sequence[Action], state, goal) -> float:
    """The number of landmarks found from the state that are not true in it, or math.inf."""
    state = frozenset(state)
    marks = fact_landmarks(actions, state, goal)  # @line L1
    if marks is None:  # @line L2
        return math.inf
    return len(marks - state)  # @line L3


def cost_partitioning(actions: Sequence[Action], state, goal):
    """Uniform cost partitioning over the open landmarks (unit action costs). Admissible."""
    state = frozenset(state)
    marks = fact_landmarks(actions, state, goal)
    if marks is None:
        return math.inf
    open_marks = marks - state
    total = Fraction(0)
    for l in open_marks:
        total += min(Fraction(1, len(a.add & open_marks)) for a in actions if l in a.add)  # @line L4
    return total  # @line L5


class PathLandmarkCount:
    """The landmark count of LAMA with no orderings: landmarks are found once and accepted along the path."""

    def __init__(self, actions: Sequence[Action], init, goal):
        self.goal = frozenset(goal)
        self.marks = fact_landmarks(actions, frozenset(init), self.goal)

    def accept(self, accepted: Optional[FrozenSet[Hashable]], state) -> FrozenSet[Hashable]:
        """The accepted set after reaching the state; pass None for the initial state."""
        if self.marks is None:
            return frozenset()
        reached = self.marks & frozenset(state)
        return reached if accepted is None else accepted | reached

    def value(self, accepted: FrozenSet[Hashable], state) -> float:
        if self.marks is None:
            return math.inf
        required_again = {g for g in self.goal & accepted if g not in state}
        return len(self.marks - accepted) + len(required_again)
