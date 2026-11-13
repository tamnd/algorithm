# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goal-regression/. The authors are listed in prov/X17W61.jsonl.

"""Goal regression for propositional STRIPS actions.

The regression of a goal set g through an action a is (g minus add(a)) union pre(a).
It is defined when a deletes no fact of g. It is useful only when a is relevant,
that is when a also adds a fact of g. Actions must have disjoint add and delete lists.
"""

from typing import FrozenSet, Hashable, Iterable, List, NamedTuple, Optional, Sequence

Fact = Hashable


class Action(NamedTuple):
    name: str
    pre: FrozenSet[Fact]
    add: FrozenSet[Fact]
    delete: FrozenSet[Fact]


def make_action(name: str, pre: Iterable[Fact] = (), add: Iterable[Fact] = (), delete: Iterable[Fact] = ()) -> Action:
    a = Action(name, frozenset(pre), frozenset(add), frozenset(delete))
    if a.add & a.delete:
        raise ValueError("add and delete lists must be disjoint")
    return a


def run_plan(state: FrozenSet[Fact], plan: Sequence[Action]) -> Optional[FrozenSet[Fact]]:
    for a in plan:
        if not a.pre <= state:
            return None
        state = (state - a.delete) | a.add
    return state


def consistent(g: FrozenSet[Fact], a: Action) -> bool:
    """a deletes no fact of g."""
    return not (a.delete & g)


def relevant(g: FrozenSet[Fact], a: Action) -> bool:
    """a adds a fact of g and deletes none."""
    return bool(a.add & g) and not (a.delete & g)


def regress(g: Iterable[Fact], a: Action) -> Optional[FrozenSet[Fact]]:
    """The weakest set of facts that must hold before a so that g holds after it, or None
    if no state works (a deletes a fact of g)."""
    g = frozenset(g)
    if a.delete & g:  # @line L1
        return None
    return (g - a.add) | a.pre  # @line L2


def regress_plan(g: Iterable[Fact], plan: Sequence[Action]) -> Optional[FrozenSet[Fact]]:
    """Regress g through the whole plan, last action first."""
    cur: Optional[FrozenSet[Fact]] = frozenset(g)  # @line L3
    for a in reversed(plan):  # @line L4
        cur = regress(cur, a)  # @line L5
        if cur is None:  # @line L6
            return None
    return cur  # @line L7


def suffix_conditions(g: Iterable[Fact], plan: Sequence[Action]) -> List[Optional[FrozenSet[Fact]]]:
    """conds[i] is the regression of g through plan[i:], so conds[len(plan)] = g.
    During execution, the rest of the plan from step i reaches g exactly when the
    current state contains conds[i]; a monitor checks this before each step."""
    conds: List[Optional[FrozenSet[Fact]]] = [None] * (len(plan) + 1)
    cur: Optional[FrozenSet[Fact]] = frozenset(g)
    conds[len(plan)] = cur
    for i in range(len(plan) - 1, -1, -1):
        cur = None if cur is None else regress(cur, plan[i])
        conds[i] = cur
    return conds
