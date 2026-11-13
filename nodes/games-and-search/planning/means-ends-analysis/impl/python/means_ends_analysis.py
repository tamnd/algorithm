# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/means-ends-analysis/. The authors are listed in prov/GDKDXZ.jsonl.

"""Means-ends analysis on propositional STRIPS tasks.

A difference is a goal fact that does not hold. The difference table maps each
fact to the operators that add it. To remove a difference, the method picks an
operator from the table, first makes the preconditions of that operator true
(a subproblem solved by the same method), applies the operator, and then works
on the differences that are left. It backtracks over the choice of difference
and of operator, and a depth bound limits the nesting of subproblems.
"""

from collections import deque
from typing import Dict, FrozenSet, Hashable, Iterable, List, NamedTuple, Optional, Sequence, Tuple

Fact = Hashable
State = FrozenSet[Fact]


class Action(NamedTuple):
    name: str
    pre: FrozenSet[Fact]
    add: FrozenSet[Fact]
    delete: FrozenSet[Fact]


def make_action(name: str, pre: Iterable[Fact] = (), add: Iterable[Fact] = (), delete: Iterable[Fact] = ()) -> Action:
    return Action(name, frozenset(pre), frozenset(add), frozenset(delete))


def run_plan(state: State, plan: Sequence[Action]) -> Optional[State]:
    for a in plan:
        if not a.pre <= state:
            return None
        state = (state - a.delete) | a.add
    return state


def is_plan(init: Iterable[Fact], goal: Iterable[Fact], plan: Sequence[Action]) -> bool:
    final = run_plan(frozenset(init), plan)
    return final is not None and frozenset(goal) <= final


def difference_table(actions: Sequence[Action]) -> Dict[Fact, List[Action]]:
    table: Dict[Fact, List[Action]] = {}
    for a in actions:
        for p in a.add:
            table.setdefault(p, []).append(a)
    return table


def means_ends(init: Iterable[Fact], goal: Iterable[Fact], actions: Sequence[Action], depth: int = 6,
               order=None) -> Optional[List[Action]]:
    """Return a plan found by means-ends analysis, or None.

    depth bounds the nesting of subproblems. order, if given, is a function that
    lists the differences of a state in the order to try them (the GPS ordering
    of differences); the default is a fixed sorted order.
    """
    table = difference_table(actions)  # @line L1
    memo: Dict[Tuple[State, FrozenSet[Fact], int], Optional[Tuple[State, Tuple[Action, ...]]]] = {}
    key = order or (lambda diffs: sorted(diffs, key=repr))

    def solve(s: State, g: FrozenSet[Fact], d: int) -> Optional[Tuple[State, Tuple[Action, ...]]]:
        if g <= s:  # @line L5
            return s, ()
        if d == 0:  # @line L6
            return None
        k = (s, g, d)
        if k in memo:                                    # d falls on every call, so k is never
            return memo[k]                               # on the call stack twice: the memo is exact
        result = None
        for p in key(g - s):  # @line L7 (choose a difference)
            for op in table.get(p, []):  # @line L8 (choose an operator that removes it)
                r1 = solve(s, op.pre, d - 1)  # @line L9 (subproblem: make op applicable)
                if r1 is None:  # @line L10
                    continue
                s1, plan1 = r1  # @line L11
                s2 = (s1 - op.delete) | op.add  # @line L12 (apply op)
                r2 = solve(s2, g, d - 1)  # @line L13 (the differences that are left)
                if r2 is None:  # @line L14
                    continue
                s3, plan2 = r2  # @line L15
                result = (s3, plan1 + (op,) + plan2)  # @line L16
                break
            if result is not None:
                break
        memo[k] = result
        return result  # @line L17 (None here means failure)

    r = solve(frozenset(init), frozenset(goal), depth)  # @line L2
    if r is None:  # @line L3
        return None
    return list(r[1])  # @line L4


def bfs_plan(init: Iterable[Fact], goal: Iterable[Fact], actions: Sequence[Action]) -> Optional[List[Action]]:
    """Reference: a shortest plan by breadth first search over states."""
    init = frozenset(init)
    goal = frozenset(goal)
    parent: Dict[State, Optional[Tuple[State, Action]]] = {init: None}
    queue = deque([init])
    while queue:
        s = queue.popleft()
        if goal <= s:
            plan = []
            while parent[s] is not None:
                s, a = parent[s]
                plan.append(a)
            return plan[::-1]
        for a in actions:
            if a.pre <= s:
                t = (s - a.delete) | a.add
                if t not in parent:
                    parent[t] = (s, a)
                    queue.append(t)
    return None


def register_swap_task():
    """Swap the contents of registers R1 and R2, with R3 free to use.
    contains(r, v) says register r holds value v; assign(r, q) copies q into r."""
    regs = ["R1", "R2", "R3"]
    vals = ["a", "b", "c"]
    acts = []
    for r in regs:
        for q in regs:
            if r == q:
                continue
            for v in vals:
                for w in vals:
                    if v != w:
                        acts.append(make_action(f"assign({r},{q},{v},{w})", [("contains", q, v), ("contains", r, w)],
                                                [("contains", r, v)], [("contains", r, w)]))
    init = frozenset([("contains", "R1", "a"), ("contains", "R2", "b"), ("contains", "R3", "c")])
    goal = frozenset([("contains", "R1", "b"), ("contains", "R2", "a")])
    return init, goal, acts


def small_swap_task():
    """The six-action swap of the correctness proof. The fact "vR" says that register R
    holds value v. Only the copies that matter are kept, and the copies into R3 delete nothing."""
    acts = [
        make_action("saveA", ["aR1"], ["aR3"]),
        make_action("saveB", ["bR2"], ["bR3"]),
        make_action("o1", ["bR2"], ["bR1"], ["aR1"]),
        make_action("o1'", ["bR3"], ["bR1"], ["aR1"]),
        make_action("o2", ["aR1"], ["aR2"], ["bR2"]),
        make_action("o2'", ["aR3"], ["aR2"], ["bR2"]),
    ]
    return frozenset(["aR1", "bR2"]), frozenset(["bR1", "aR2"]), acts
