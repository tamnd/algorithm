# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burnt-pancake-problem/. The authors are listed in prov/THR7VX.jsonl.
"""Burnt pancakes: flips of signed permutations, a simple sorter, and exact search.

A stack is a tuple of nonzero integers, top first. Pancake k is k or -k; the
sign is + when the burnt side faces down. A flip of the top i pancakes
reverses their order and turns each one over. The goal is (1, 2, ..., n).
"""

from collections import deque
from itertools import permutations, product
from typing import Dict, Iterator, List, Sequence, Tuple

Stack = Tuple[int, ...]


def flip(s: Sequence[int], i: int) -> Stack:
    """Flip the top i pancakes, 1 <= i <= len(s)."""
    if not 1 <= i <= len(s):
        raise ValueError("flip size out of range")
    return tuple(-x for x in reversed(s[:i])) + tuple(s[i:])


def apply_flips(s: Sequence[int], flips: Sequence[int]) -> Stack:
    t = tuple(s)
    for i in flips:
        t = flip(t, i)
    return t


def simple_sort(s: Sequence[int]) -> List[int]:
    """Place the largest unsorted pancake at the bottom of the unsorted part, at most 3 flips each.

    It makes at most 3n - 2 flips.
    """
    t = list(s)
    n = len(t)
    out: List[int] = []

    def do(i: int) -> None:
        nonlocal t
        t = list(flip(t, i))
        out.append(i)

    for k in range(n, 0, -1):
        if t[k - 1] == k:
            continue
        p = [abs(x) for x in t].index(k) + 1
        if p > 1:
            do(p)  # pancake k is now on top
        if t[0] == k:
            do(1)  # burnt side up, so the next flip puts it down
        do(k)
    return out


def all_stacks(n: int) -> Iterator[Stack]:
    for perm in permutations(range(1, n + 1)):
        for signs in product((1, -1), repeat=n):
            yield tuple(p * q for p, q in zip(perm, signs))


def distances(n: int) -> Dict[Stack, int]:
    """Breadth-first search from the sorted stack over all 2^n n! stacks.

    Every flip is its own inverse, so the distance from the goal equals the
    least number of flips that sort the stack.
    """
    goal = tuple(range(1, n + 1))
    dist = {goal: 0}
    queue = deque([goal])
    while queue:
        s = queue.popleft()
        d = dist[s] + 1
        for i in range(1, n + 1):
            t = flip(s, i)
            if t not in dist:
                dist[t] = d
                queue.append(t)
    return dist


def burnt_pancake_number(n: int) -> int:
    """g(n): the largest least number of flips over all stacks of n burnt pancakes."""
    if n == 0:
        return 0
    return max(distances(n).values())


def unburnt_distances(n: int) -> Dict[Tuple[int, ...], int]:
    """The same search for ordinary pancakes, for comparison."""
    goal = tuple(range(1, n + 1))
    dist = {goal: 0}
    queue = deque([goal])
    while queue:
        s = queue.popleft()
        for i in range(2, n + 1):
            t = tuple(reversed(s[:i])) + s[i:]
            if t not in dist:
                dist[t] = dist[s] + 1
                queue.append(t)
    return dist
