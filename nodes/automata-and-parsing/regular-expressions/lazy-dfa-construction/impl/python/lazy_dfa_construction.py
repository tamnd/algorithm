# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lazy-dfa-construction/. The authors are listed in prov/1VRZ3Y.jsonl.

"""Lazy DFA construction: build DFA states while reading the text, and cache them.

A regular expression is a tuple:
("empty",) for the empty language, ("eps",) for the empty string,
("sym", a) for one symbol, ("alt", r, s), ("cat", r, s) and ("star", r).

The DFA is the subset construction of an NFA, but a DFA state is made only
when the text reaches it. The cache of DFA states has a capacity; when a new
state is needed and the cache is full, the whole cache is flushed.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

Regex = tuple[Any, ...]


@dataclass
class NFA:
    """An NFA with epsilon-moves. moves[q] lists (symbol, target) pairs."""

    eps: list[list[int]]
    moves: list[list[tuple[str, int]]]
    start: int
    accepting: frozenset[int]


def thompson_nfa(regex: Regex) -> NFA:
    """Thompson's construction, with two states per node and an explicit stack."""
    eps: list[list[int]] = []
    moves: list[list[tuple[str, int]]] = []

    def new() -> int:
        eps.append([])
        moves.append([])
        return len(eps) - 1

    frags: list[tuple[int, int]] = []
    todo: list[tuple[Regex, bool]] = [(regex, False)]
    while todo:
        node, ready = todo.pop()
        tag = node[0]
        if not ready and tag in ("alt", "cat", "star"):
            todo.append((node, True))
            for child in reversed(node[1:]):
                todo.append((child, False))
            continue
        s, f = new(), new()
        if tag == "eps":
            eps[s].append(f)
        elif tag == "sym":
            moves[s].append((node[1], f))
        elif tag == "alt":
            s2, f2 = frags.pop()
            s1, f1 = frags.pop()
            eps[s] += [s1, s2]
            eps[f1].append(f)
            eps[f2].append(f)
        elif tag == "cat":
            s2, f2 = frags.pop()
            s1, f1 = frags.pop()
            eps[s].append(s1)
            eps[f1].append(s2)
            eps[f2].append(f)
        elif tag == "star":
            s1, f1 = frags.pop()
            eps[s] += [s1, f]
            eps[f1] += [s1, f]
        elif tag != "empty":
            raise ValueError(f"unknown node {node!r}")
        frags.append((s, f))
    start, final = frags.pop()
    return NFA(eps, moves, start, frozenset([final]))


def glushkov_nfa(regex: Regex) -> NFA:
    """The Glushkov (position) automaton: no epsilon-moves, state 0 is initial."""
    symbol = [""]
    follow: list[set[int]] = [set()]
    done: list[tuple[bool, set[int], set[int]]] = []
    todo: list[tuple[Regex, bool]] = [(regex, False)]
    while todo:
        node, ready = todo.pop()
        tag = node[0]
        if not ready and tag in ("alt", "cat", "star"):
            todo.append((node, True))
            for child in reversed(node[1:]):
                todo.append((child, False))
            continue
        if tag in ("empty", "eps"):
            done.append((tag == "eps", set(), set()))
        elif tag == "sym":
            symbol.append(node[1])
            follow.append(set())
            p = len(symbol) - 1
            done.append((False, {p}, {p}))
        elif tag == "alt":
            n2, f2, l2 = done.pop()
            n1, f1, l1 = done.pop()
            done.append((n1 or n2, f1 | f2, l1 | l2))
        elif tag == "cat":
            n2, f2, l2 = done.pop()
            n1, f1, l1 = done.pop()
            for p in l1:
                follow[p] |= f2
            done.append((n1 and n2, f1 | f2 if n1 else f1, l1 | l2 if n2 else l2))
        elif tag == "star":
            n1, f1, l1 = done.pop()
            for p in l1:
                follow[p] |= f1
            done.append((True, f1, l1))
        else:
            raise ValueError(f"unknown node {node!r}")
    nullable, first, last = done.pop()
    follow[0] = first
    moves = [sorted((symbol[q], q) for q in follow[p]) for p in range(len(symbol))]
    accepting = set(last) | ({0} if nullable else set())
    return NFA([[] for _ in symbol], moves, 0, frozenset(accepting))


@dataclass
class DState:
    """A cached DFA state: a set of NFA states and a partial transition table."""

    nfa_set: frozenset[int]
    accepting: bool
    next: dict[str, DState] = field(default_factory=dict)


class LazyDFA:
    """The subset DFA of `nfa`, built on demand.

    capacity is the largest number of cached DFA states (None for no limit).
    With unanchored=True, the NFA start state is added after every symbol,
    so a state is accepting when some substring ending here is accepted.
    """

    def __init__(self, nfa: NFA, capacity: int | None = None, unanchored: bool = False) -> None:
        if capacity is not None and capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.nfa = nfa
        self.capacity = capacity
        self.unanchored = unanchored
        self.states: dict[frozenset[int], DState] = {}  # @line L1
        self.built = 0  # DFA states made, over all flushes
        self.computed = 0  # transitions computed from the NFA
        self.flushes = 0
        self.start_set = self.closure([nfa.start])

    def closure(self, qs: Iterable[int]) -> frozenset[int]:
        """All NFA states reachable from qs by epsilon-moves, with an explicit stack."""
        seen = set(qs)
        stack = list(seen)
        while stack:
            q = stack.pop()
            for r in self.nfa.eps[q]:
                if r not in seen:
                    seen.add(r)
                    stack.append(r)
        return frozenset(seen)

    def state(self, u: frozenset[int]) -> DState:
        """The cached DFA state for the NFA-state set u, made if needed."""
        d = self.states.get(u)
        if d is None:  # @line L12
            d = DState(u, not u.isdisjoint(self.nfa.accepting))
            self.states[u] = d
            self.built += 1
        return d  # @line L13

    def step(self, s: DState, c: str) -> DState:
        """The DFA state after s on the symbol c."""
        t = s.next.get(c)  # @line L4
        if t is None:  # @line L5
            targets = [q2 for q in s.nfa_set for (a, q2) in self.nfa.moves[q] if a == c]
            if self.unanchored:
                targets.append(self.nfa.start)
            u = self.closure(targets)  # @line L6
            self.computed += 1
            if self.capacity is not None and u not in self.states and len(self.states) >= self.capacity:  # @line L7
                self.states.clear()
                self.flushes += 1
            t = self.state(u)  # @line L8
            s.next[c] = t  # @line L9
        return t

    def start(self) -> DState:
        return self.state(self.start_set)  # @line L2

    def accepts(self, word: str) -> bool:
        """Decide whether the NFA accepts `word` (anchored at both ends)."""
        s = self.start()
        for c in word:  # @line L3
            s = self.step(s, c)  # @line L10
        return s.accepting  # @line L11

    def trace(self, word: str) -> list[frozenset[int]]:
        """The NFA-state sets after each prefix of `word` (for examples)."""
        s = self.start()
        out = [s.nfa_set]
        for c in word:
            s = self.step(s, c)
            out.append(s.nfa_set)
        return out

    def match_ends(self, text: str) -> list[int]:
        """With unanchored=True: every i such that some text[j:i] is accepted."""
        s = self.start()
        out = [0] if s.accepting else []
        for i, c in enumerate(text, 1):
            s = self.step(s, c)
            if s.accepting:
                out.append(i)
        return out


def lazy_dfa_match(regex: Regex, word: str, capacity: int | None = None) -> bool:
    """Decide whether `word` is in L(regex) with a lazy DFA over the Thompson NFA.

    Cost: O(m) time per transition computed and O(1) per cached transition,
    so O(m n) in the worst case for m nodes and n symbols.
    """
    return LazyDFA(thompson_nfa(regex), capacity).accepts(word)


def lazy_dfa_search(regex: Regex, text: str, capacity: int | None = None) -> list[int]:
    """The end positions i of the substrings text[j:i] that are in L(regex)."""
    return LazyDFA(thompson_nfa(regex), capacity, unanchored=True).match_ends(text)
