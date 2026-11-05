# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moore-minimization/. The authors are listed in prov/7CHN37.jsonl.

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
    order = [start]
    while stack:
        q = stack.pop()
        for r in delta[q]:
            if r not in seen:
                seen.add(r)
                stack.append(r)
                order.append(r)
    return sorted(order)


def moore_minimize(delta: Sequence[Sequence[int]], start: int, finals: set[int] | frozenset[int]) -> tuple[DFA, dict[int, int]]:
    """Minimize a complete DFA by Moore's partition refinement.

    Returns the minimal complete DFA and the map from each reachable state of the
    input to its state in the output. Each round costs O(n sigma) expected time with
    hashing, and there are at most n - 1 rounds, so the time is O(sigma n^2).
    """
    sigma = len(delta[0]) if delta else 0
    states = reachable(delta, start)  # @line L1
    cls = {q: (1 if q in finals else 0) for q in states}  # @line L2
    k = len(set(cls.values()))  # @line L3
    while True:  # @line L4
        sig = {q: (cls[q],) + tuple(cls[delta[q][a]] for a in range(sigma)) for q in states}  # @line L5
        number: dict[tuple[int, ...], int] = {}
        new = {q: number.setdefault(sig[q], len(number)) for q in states}  # @line L6
        k_new = len(number)  # @line L7
        stable = k_new == k  # @line L8
        cls, k = new, k_new  # @line L9
        if stable:  # @line L10
            break
    out = [[0] * sigma for _ in range(k)]  # @line L11
    for q in states:
        for a in range(sigma):
            out[cls[q]][a] = cls[delta[q][a]]
    out_finals = frozenset(cls[q] for q in states if q in finals)
    return DFA(out, cls[start], out_finals), cls
