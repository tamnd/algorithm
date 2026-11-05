# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brzozowski-minimization/. The authors are listed in prov/VRYA87.jsonl.

from collections import deque
from collections.abc import Iterable, Sequence
from typing import NamedTuple


class DFA(NamedTuple):
    """A complete DFA: states 0..k-1, symbols 0..sigma-1, delta[q][a] is the next state."""

    delta: list[list[int]]
    start: int
    finals: frozenset[int]


NFA = Sequence[Sequence[Iterable[int]]]  # nfa[q][a] is the set of next states


def reverse(nfa: NFA, sigma: int) -> list[list[set[int]]]:
    """Reverse every transition: p -a-> q becomes q -a-> p. O(n sigma + m) time for m transitions."""
    rev: list[list[set[int]]] = [[set() for _ in range(sigma)] for _ in nfa]
    for p, row in enumerate(nfa):
        for a in range(sigma):
            for q in row[a]:
                rev[q][a].add(p)
    return rev


def determinize(nfa: NFA, sigma: int, starts: Iterable[int], finals: Iterable[int]) -> tuple[DFA, list[frozenset[int]]]:
    """Subset construction on the reachable subsets, including the empty set when it is reached.

    The subsets are numbered in breadth-first order. With d reachable subsets and m
    transitions, the time is O(sigma d (n + m)) in the worst case.
    """
    final_set = set(finals)
    s0 = frozenset(starts)  # @line L6
    index = {s0: 0}
    subsets = [s0]
    queue = deque([s0])
    delta: list[list[int]] = []
    while queue:  # @line L7
        s = queue.popleft()  # @line L8
        row = []
        for a in range(sigma):
            t = frozenset(r for q in s for r in nfa[q][a])  # @line L9
            if t not in index:  # @line L10
                index[t] = len(subsets)
                subsets.append(t)
                queue.append(t)
            row.append(index[t])  # @line L11
        delta.append(row)
    dfa_finals = frozenset(i for i, s in enumerate(subsets) if s & final_set)  # @line L12
    return DFA(delta, 0, dfa_finals), subsets  # @line L13


def brzozowski_minimize(nfa: NFA, sigma: int, starts: Iterable[int], finals: Iterable[int]) -> DFA:
    """Minimal complete DFA of the NFA (a DFA is the case of one-element sets), as det(rev(det(rev(N)))).

    Each determinization can produce exponentially many subsets, so the time is
    O(sigma (n^2 d1 + d1 d2)) for intermediate size d1 and output size d2, at most O(sigma 4^n).
    """
    starts, finals = list(starts), list(finals)
    rev1 = reverse(nfa, sigma)  # @line L1
    d1, _ = determinize(rev1, sigma, finals, starts)  # @line L2
    as_nfa = [[(d1.delta[p][a],) for a in range(sigma)] for p in range(len(d1.delta))]
    rev2 = reverse(as_nfa, sigma)  # @line L3
    d2, _ = determinize(rev2, sigma, d1.finals, [d1.start])  # @line L4
    return d2  # @line L5
