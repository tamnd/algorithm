# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hopcroft-minimization/. The authors are listed in prov/HJJDQK.jsonl.

from collections import deque
from collections.abc import Sequence
from typing import NamedTuple


class DFA(NamedTuple):
    """A complete DFA: states 0..n-1, symbols 0..sigma-1, delta[q][a] is the next state."""

    delta: list[list[int]]
    start: int
    finals: frozenset[int]


def reachable(delta: Sequence[Sequence[int]], start: int) -> list[int]:
    """The states reachable from start, by an iterative depth-first search; O(n sigma) time."""
    seen = {start}
    stack = [start]
    while stack:
        q = stack.pop()
        for r in delta[q]:
            if r not in seen:
                seen.add(r)
                stack.append(r)
    return sorted(seen)


def hopcroft_minimize(delta: Sequence[Sequence[int]], start: int, finals: set[int] | frozenset[int]) -> tuple[DFA, dict[int, int]]:
    """Minimize a complete DFA by Hopcroft's algorithm.

    Returns the minimal complete DFA, with its states numbered in breadth-first order
    from the start state, and the map from each reachable input state to its output
    state. Time O(sigma n log n), extra space O(sigma n).
    """
    sigma = len(delta[0]) if delta else 0
    states = reachable(delta, start)  # @line L1
    pre: list[dict[int, list[int]]] = [{r: [] for r in states} for _ in range(sigma)]  # @line L2
    for q in states:
        for a in range(sigma):
            pre[a][delta[q][a]].append(q)
    acc = {q for q in states if q in finals}
    rej = {q for q in states if q not in finals}
    blocks: list[set[int]] = [set(b) for b in (acc, rej) if b]  # @line L3
    block_of: dict[int, int] = {}
    for i, b in enumerate(blocks):
        for q in b:
            block_of[q] = i
    work: deque[tuple[int, int]] = deque()  # @line L4
    in_work: set[tuple[int, int]] = set()
    if len(blocks) == 2:
        small = 0 if len(blocks[0]) <= len(blocks[1]) else 1
        for a in range(sigma):
            work.append((small, a))
            in_work.add((small, a))
    while work:  # @line L5
        s, a = work.popleft()  # @line L6
        in_work.discard((s, a))
        marked: dict[int, list[int]] = {}  # @line L7
        for r in list(blocks[s]):
            for q in pre[a][r]:
                marked.setdefault(block_of[q], []).append(q)
        for b, inside in marked.items():  # @line L8
            if len(inside) == len(blocks[b]):
                continue
            nb = len(blocks)  # @line L9: B1 = B ∩ X gets the new id nb, B2 = B \ X keeps b
            blocks.append(set(inside))
            for q in inside:
                blocks[b].discard(q)
                block_of[q] = nb
            for c in range(sigma):  # @line L10
                if (b, c) in in_work:  # @line L11
                    work.append((nb, c))
                    in_work.add((nb, c))
                else:  # @line L12
                    pick = nb if len(blocks[nb]) <= len(blocks[b]) else b
                    work.append((pick, c))
                    in_work.add((pick, c))
    # @line L13: the quotient, numbered in breadth-first order from the start block
    number = {block_of[start]: 0}
    order = [block_of[start]]
    out: list[list[int]] = []
    i = 0
    while i < len(order):
        rep = next(iter(blocks[order[i]]))
        row = []
        for a in range(sigma):
            t = block_of[delta[rep][a]]
            if t not in number:
                number[t] = len(order)
                order.append(t)
            row.append(number[t])
        out.append(row)
        i += 1
    cls = {q: number[block_of[q]] for q in states}
    out_finals = frozenset(cls[q] for q in acc)
    return DFA(out, cls[start], out_finals), cls
