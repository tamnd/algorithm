# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/glushkov-automaton/. The authors are listed in prov/0FZKDT.jsonl.

"""The Glushkov (position) automaton of a regular expression.

A regular expression is a tuple:
("empty",) for the empty language, ("eps",) for the empty string,
("sym", a) for one symbol, ("alt", r, s), ("cat", r, s) and ("star", r).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

Regex = tuple[Any, ...]


@dataclass
class Glushkov:
    """States 0..k. State 0 is initial; state p >= 1 is the p-th symbol occurrence.

    symbol[p] is the symbol of position p (symbol[0] is unused), succ[0] is
    First, succ[p] is Follow(p), and every move into q reads symbol[q].
    """

    symbol: list[str]
    succ: list[list[int]]
    accepting: set[int]

    def transitions(self) -> list[tuple[int, str, int]]:
        """All moves (p, a, q) of the automaton, sorted."""
        return sorted((p, self.symbol[q], q) for p in range(len(self.succ)) for q in self.succ[p])


def glushkov(regex: Regex) -> Glushkov:
    """Build the Glushkov automaton of `regex`, with k + 1 states for k symbol occurrences.

    The tree is walked in postorder with an explicit stack, so deep
    expressions need no recursion. Cost: O(m * k^2) time and O(m * k) space
    for m nodes, without the star normal form refinement.
    """
    symbol = [""]
    follow: list[set[int]] = [set()]
    # Each finished node leaves (nullable, first, last) on this stack.
    done: list[tuple[bool, set[int], set[int]]] = []
    todo: list[tuple[Regex, bool]] = [(regex, False)]
    while todo:  # @line L2
        node, ready = todo.pop()
        tag = node[0]
        if not ready and tag in ("alt", "cat", "star"):
            todo.append((node, True))
            for child in reversed(node[1:]):
                todo.append((child, False))
            continue
        if tag == "empty":  # @line L3
            done.append((False, set(), set()))
        elif tag == "eps":  # @line L4
            done.append((True, set(), set()))
        elif tag == "sym":  # @line L5
            symbol.append(node[1])  # @line L1
            follow.append(set())
            p = len(symbol) - 1
            done.append((False, {p}, {p}))
        elif tag == "alt":  # @line L6
            n2, f2, l2 = done.pop()
            n1, f1, l1 = done.pop()
            done.append((n1 or n2, f1 | f2, l1 | l2))
        elif tag == "cat":  # @line L7
            n2, f2, l2 = done.pop()
            n1, f1, l1 = done.pop()
            for p in l1:  # @line L8
                follow[p] |= f2
            nullable = n1 and n2  # @line L9
            first = f1 | f2 if n1 else f1  # @line L10
            last = l1 | l2 if n2 else l2  # @line L11
            done.append((nullable, first, last))
        elif tag == "star":  # @line L12
            n1, f1, l1 = done.pop()
            for p in l1:  # @line L13
                follow[p] |= f1
            done.append((True, f1, l1))  # @line L14
        else:
            raise ValueError(f"unknown node {node!r}")
    nullable, first, last = done.pop()
    follow[0] = first  # @line L15
    succ = [sorted(f) for f in follow]  # @line L16
    accepting = set(last)  # @line L17
    if nullable:
        accepting.add(0)
    return Glushkov(symbol, succ, accepting)  # @line L18


def accepts(g: Glushkov, word: str) -> bool:
    """Run the automaton on `word` with a set of current states.

    Cost: O(len(word) * number of moves) time, O(k) space.
    """
    current = {0}
    for c in word:
        current = {q for p in current for q in g.succ[p] if g.symbol[q] == c}
        if not current:
            return False
    return bool(current & g.accepting)
