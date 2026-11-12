# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pinwheel-scheduling/. The authors are listed in prov/TDMAY5.jsonl.

"""Exact decision procedure for pinwheel scheduling.

An instance is a list of positive integers a_1..a_n. A schedule assigns one
task to each integer time slot; it is valid when every window of a_i
consecutive slots contains task i. The search state is the countdown vector
c, where c_i is the number of slots left in which task i must appear
(1 <= c_i <= a_i). Scheduling task j sets c_j = a_j and lowers every other
entry by 1; a state with an entry that would fall to 0 has no such move.
The instance is schedulable iff the start state (a_1, .., a_n) can make
moves forever, that is, iff it is not removed when states with no live move
are pruned repeatedly. A walk through live states then repeats a state and
gives a cyclic schedule.

Cost: O(n S) time and space for S reachable states, with S <= a_1 a_2 .. a_n.
"""

from collections import deque
from fractions import Fraction


def step(state: tuple[int, ...], j: int, a: tuple[int, ...]) -> tuple[int, ...] | None:
    """The state after slot j is given to task j, or None if a task misses."""
    nxt = []
    for i, c in enumerate(state):
        if i == j:
            nxt.append(a[i])
        elif c == 1:
            return None
        else:
            nxt.append(c - 1)
    return tuple(nxt)


def pinwheel_schedule(periods: list[int]) -> list[int] | None:
    """A cyclic schedule (task index per slot) or None if the instance is not schedulable."""
    if not periods or min(periods) < 1:
        raise ValueError("periods must be positive integers")
    a = tuple(periods)
    if sum(Fraction(1, x) for x in a) > 1:  # @line L1
        return None
    start = a  # @line L2
    succ: dict[tuple[int, ...], list[tuple[int, tuple[int, ...]]]] = {}
    todo = deque([start])
    while todo:  # @line L3
        s = todo.popleft()
        if s in succ:
            continue
        out = []
        for j in range(len(a)):  # @line L4
            t = step(s, j, a)
            if t is not None:
                out.append((j, t))
                if t not in succ:
                    todo.append(t)
        succ[s] = out
    pred: dict[tuple[int, ...], list[tuple[int, ...]]] = {s: [] for s in succ}
    for s, out in succ.items():
        for _, t in out:
            pred[t].append(s)
    live = {s: len(out) for s, out in succ.items()}
    dead = deque(s for s, k in live.items() if k == 0)
    gone = set(dead)
    while dead:  # @line L5
        t = dead.popleft()
        for s in pred[t]:
            live[s] -= 1
            if live[s] == 0 and s not in gone:
                gone.add(s)
                dead.append(s)
    if start in gone:  # @line L6
        return None
    seen: dict[tuple[int, ...], int] = {}
    moves: list[int] = []
    s = start
    while s not in seen:  # @line L7
        seen[s] = len(moves)
        j, s = next((j, t) for j, t in succ[s] if t not in gone)
        moves.append(j)
    return moves[seen[s]:]  # @line L8


def is_valid_cyclic(periods: list[int], cycle: list[int]) -> bool:
    """True if repeating the cycle forever puts task i in every window of periods[i] slots."""
    m = len(cycle)
    for i, p in enumerate(periods):
        slots = [k for k, x in enumerate(cycle) if x == i]
        if not slots:
            return False
        gaps = [(slots[(k + 1) % len(slots)] - slots[k]) % m or m for k in range(len(slots))]
        if max(gaps) > p:
            return False
    return True
