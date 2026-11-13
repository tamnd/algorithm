# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/macro-operators/. The authors are listed in prov/8C2C7V.jsonl.

"""Macro-operators for STRIPS tasks, and the macro table of Korf (1985) for a sliding tile puzzle.

A STRIPS action is Action(name, pre, add, dele) with frozensets of facts, and
add and dele are disjoint. The function macro composes a sequence of actions
into one action that has the same effect as the sequence in every state where
the sequence is applicable; it returns None when the sequence is applicable in
no state. A macro has the name ("macro", steps), where steps is the tuple of
the composed actions, so expand can turn a plan with macro-operators back into
a plan of primitive actions. The function plan_with_macros adds them to the
actions, runs breadth-first search and expands the plan.

The function macro_table builds Korf's table for the rows x cols sliding tile
puzzle, and solve_with_table solves a state with at most one macro per tile.
"""

from collections import deque, namedtuple
from typing import Dict, List, Optional, Sequence, Tuple

Action = namedtuple("Action", "name pre add dele")


def compose(a: Action, b: Action) -> Optional[Action]:
    """One action for a followed by b, or None if b is never applicable right after a."""
    if a.dele & b.pre:
        return None
    add = (a.add - b.dele) | b.add
    return Action(None, a.pre | (b.pre - a.add), add, (a.dele | b.dele) - add)


def macro(steps: Sequence[Action]) -> Optional[Action]:
    """The macro-operator for a nonempty sequence of actions, or None if no state allows the sequence."""
    result = steps[0]
    for b in steps[1:]:
        result = compose(result, b)
        if result is None:
            return None
    return Action(("macro", tuple(steps)), result.pre, result.add, result.dele)


def is_macro(a: Action) -> bool:
    return isinstance(a.name, tuple) and len(a.name) == 2 and a.name[0] == "macro"


def expand(plan: Sequence[Action]) -> List[Action]:
    """Replace each macro by its steps, recursively, so a macro-operator may contain others."""
    out = []
    for a in plan:
        out.extend(expand(a.name[1]) if is_macro(a) else [a])
    return out


def breadth_first_plan(actions: Sequence[Action], init, goal) -> Optional[List[Action]]:
    """A plan with the fewest operators, or None."""
    start = frozenset(init)
    parent = {start: None}
    queue = deque([start])
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
                t = (s - a.dele) | a.add
                if t not in parent:
                    parent[t] = (s, a)
                    queue.append(t)
    return None


def plan_with_macros(actions, sequences, init, goal) -> Optional[List[Action]]:
    """Search with the actions and the macro-operators of the given sequences; return a plan of primitive actions."""
    chosen = [list(seq) for seq in sequences if seq]  # @line L1
    macros = [m for m in (macro(seq) for seq in chosen) if m is not None]  # @line L2
    plan = breadth_first_plan(list(actions) + macros, init, goal)  # @line L3
    return None if plan is None else expand(plan)  # @line L4


def neighbours(rows: int, cols: int, x: int) -> List[int]:
    r, c = divmod(x, cols)
    out = []
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if 0 <= r + dr < rows and 0 <= c + dc < cols:
            out.append((r + dr) * cols + c + dc)
    return out


def slide(state: Tuple[int, ...], target: int) -> Tuple[int, ...]:
    """Move the blank (0) to the adjacent location target."""
    s = list(state)
    b = s.index(0)
    s[b], s[target] = s[target], s[b]
    return tuple(s)


def macro_table(rows: int, cols: int) -> Dict[Tuple[int, int], List[int]]:
    """Korf's table: entry (i, j) is a shortest move sequence for stage i when the next piece is at location j.

    The goal has tile t at location t - 1 and the blank at the last location. The solution order is the blank
    (stage 0) and then the tiles 1, 2, ... A move is the location that the blank moves to. Stage 0 brings the
    blank home. Stage i >= 1 starts with the blank home and the tiles 1..i-1 home, keeps them home and brings
    tile i from location j to location i - 1. The moves of a stage do not depend on the other tiles, so each
    entry is found by breadth-first search over the labels of the locations.
    """
    n = rows * cols
    home_blank = n - 1
    table = {}
    for j in range(n):
        path, x = [], j
        while x != home_blank:
            r, c = divmod(x, cols)
            x = x + 1 if c < cols - 1 else x + cols
            path.append(x)
        table[(0, j)] = path
    start = tuple(range(n))  # label[x] is the location whose piece is now at x; the blank piece has label n - 1
    moves = {start: []}
    queue = deque([start])
    while queue:
        lab = queue.popleft()
        b = lab.index(home_blank)
        for x in neighbours(rows, cols, b):
            nxt = list(lab)
            nxt[b], nxt[x] = nxt[x], nxt[b]
            nxt = tuple(nxt)
            if nxt not in moves:
                moves[nxt] = moves[lab] + [x]
                queue.append(nxt)
    for lab, path in sorted(moves.items(), key=lambda item: (len(item[1]), item[1])):
        if lab[home_blank] != home_blank:
            continue
        i = 1
        while i < n - 1 and lab[i - 1] == i - 1:
            i += 1
        for stage in range(1, i + 1):
            j = lab[stage - 1]
            if j != stage - 1 and (stage, j) not in table:
                table[(stage, j)] = path
    return table


def solve_with_table(table, rows: int, cols: int, state: Tuple[int, ...]) -> Optional[List[int]]:
    """Moves that solve the state with one macro per stage, or None if some entry is missing."""
    n = rows * cols
    moves = list(table[(0, state.index(0))])
    for x in moves:
        state = slide(state, x)
    for i in range(1, n):
        j = state.index(i)
        if j == i - 1:
            continue
        if (i, j) not in table:
            return None
        for x in table[(i, j)]:
            state = slide(state, x)
        moves.extend(table[(i, j)])
    return moves
