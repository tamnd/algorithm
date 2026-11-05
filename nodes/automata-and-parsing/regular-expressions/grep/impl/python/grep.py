# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grep/. The authors are listed in prov/B1JFJE.jsonl.

"""Line search with a regular expression, by NFA simulation.

A regular expression is a tuple:
("empty",) for the empty language, ("eps",) for the empty string,
("sym", a) for one symbol, ("alt", r, s), ("cat", r, s) and ("star", r).
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

Regex = tuple[Any, ...]


class NFA:
    """A Thompson NFA: each state has at most one symbol move and some epsilon-moves."""

    def __init__(self) -> None:
        self.sym: list[tuple[str, int] | None] = []
        self.eps: list[list[int]] = []
        self.start = 0
        self.accept = 0

    def new_state(self) -> int:
        self.sym.append(None)
        self.eps.append([])
        return len(self.eps) - 1


def thompson(regex: Regex) -> NFA:
    """Build a Thompson NFA for `regex` with at most 2m states for m nodes.

    The tree is walked in postorder with an explicit stack, so deep
    expressions need no recursion. Cost: O(m) time and space.
    """
    nfa = NFA()
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
        s, f = nfa.new_state(), nfa.new_state()
        if tag == "empty":
            pass
        elif tag == "eps":
            nfa.eps[s].append(f)
        elif tag == "sym":
            nfa.sym[s] = (node[1], f)
        elif tag == "alt":
            s2, f2 = frags.pop()
            s1, f1 = frags.pop()
            nfa.eps[s] += [s1, s2]
            nfa.eps[f1].append(f)
            nfa.eps[f2].append(f)
        elif tag == "cat":
            s2, f2 = frags.pop()
            s1, f1 = frags.pop()
            nfa.eps[s].append(s1)
            nfa.eps[f1].append(s2)
            nfa.eps[f2].append(f)
        elif tag == "star":
            s1, f1 = frags.pop()
            nfa.eps[s] += [s1, f]
            nfa.eps[f1] += [s1, f]
        else:
            raise ValueError(f"unknown node {node!r}")
        frags.append((s, f))
    nfa.start, nfa.accept = frags.pop()
    return nfa


def _close(nfa: NFA, states: Iterable[int]) -> set[int]:
    closed = set(states)
    stack = list(closed)
    while stack:
        q = stack.pop()
        for r in nfa.eps[q]:
            if r not in closed:
                closed.add(r)
                stack.append(r)
    return closed


def line_matches(nfa: NFA, line: str) -> bool:
    """Decide whether some substring of `line` is in the language of the NFA.

    Cost: O(len(line) * number of states) time, O(number of states) space.
    """
    s = _close(nfa, [nfa.start])  # @line L3
    matched = nfa.accept in s  # @line L4
    i = 0  # @line L5
    while not matched and i < len(line):  # @line L6
        c = line[i]  # @line L7
        i += 1
        t = []  # @line L8
        for q in s:
            move = nfa.sym[q]
            if move is not None and move[0] == c:
                t.append(move[1])
        t.append(nfa.start)
        s = _close(nfa, t)  # @line L9
        matched = nfa.accept in s  # @line L10
    return matched


def grep(regex: Regex, lines: Iterable[str], invert: bool = False) -> list[str]:
    """Return the lines that contain a substring in the language of `regex`.

    With invert=True, return the lines that contain no such substring, as grep -v.
    Precondition: `regex` is built from the tuples above.
    Cost: O(m) to build the NFA, then O(m) time per character, for m nodes of
    the expression; O(m) extra space.
    """
    nfa = thompson(regex)  # @line L1
    out = []
    for line in lines:  # @line L2
        if line_matches(nfa, line) != invert:  # @line L11
            out.append(line)
    return out
