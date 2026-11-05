# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/one-pass-regex-matching/. The authors are listed in prov/KX64F8.jsonl.

"""One-pass regex matching: run a deterministic position automaton, one state at a time.

A regular expression is a tuple:
("empty",) for the empty language, ("eps",) for the empty string,
("sym", a) for one symbol, ("alt", r, s), ("cat", r, s) and ("star", r).

Positions are the symbol occurrences of the expression, numbered 1..k from
left to right; position 0 is the start. The compiler builds the Glushkov
sets, keeps the useful positions, and checks that no position has two
useful successors with the same symbol. If the check passes, the matcher
reads the word once, keeps one position, and returns the unique sequence
of positions that the word takes through the expression.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

Regex = tuple[Any, ...]


class NotOnePass(ValueError):
    """The expression is not one-unambiguous, so it has no one-pass table."""


@dataclass
class OnePassTable:
    """next[p] maps a symbol to the unique next position; final is the set F."""

    symbol: list[str]
    next: list[dict[str, int]]
    final: frozenset[int]


def glushkov_sets(regex: Regex) -> tuple[list[str], list[set[int]], set[int]]:
    """Return (symbol, follow, final) with follow[0] = First, by an explicit stack."""
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
    final = set(last)
    if nullable:
        final.add(0)
    return symbol, follow, final


def useful_positions(follow: list[set[int]], final: set[int]) -> set[int]:
    """The positions reachable from 0 that can reach a final position."""
    k = len(follow)
    reach = {0}
    stack = [0]
    while stack:
        p = stack.pop()
        for q in follow[p]:
            if q not in reach:
                reach.add(q)
                stack.append(q)
    back: list[list[int]] = [[] for _ in range(k)]
    for p in range(k):
        for q in follow[p]:
            back[q].append(p)
    live = set(final)
    stack = list(live)
    while stack:
        q = stack.pop()
        for p in back[q]:
            if p not in live:
                live.add(p)
                stack.append(p)
    return reach & live


def compile_one_pass(regex: Regex) -> OnePassTable:
    """Build the one-pass table of `regex`, or raise NotOnePass.

    Cost: O(m * k^2) time for m nodes and k symbol occurrences.
    """
    symbol, follow, final = glushkov_sets(regex)  # @line L1
    final_set = frozenset(final)  # @line L2
    useful = useful_positions(follow, final)  # @line L3
    table: list[dict[str, int]] = [{} for _ in symbol]
    for p in sorted(useful | {0}):  # @line L4
        row: dict[str, int] = {}  # @line L5
        for q in sorted(follow[p] & useful):  # @line L6
            if symbol[q] in row:  # @line L7
                raise NotOnePass(f"position {p} has two successors on {symbol[q]!r}")
            row[symbol[q]] = q  # @line L8
        table[p] = row
    return OnePassTable(symbol, table, final_set)  # @line L9


def run_one_pass(table: OnePassTable, word: str) -> list[int] | None:
    """Return the positions taken by `word`, or None if `word` is not in the language.

    Cost: O(n) table lookups for a word of length n.
    """
    p = 0  # @line L10
    path: list[int] = []
    for a in word:  # @line L11
        q = table.next[p].get(a)
        if q is None:  # @line L12
            return None
        p = q  # @line L13
        path.append(q)
    return path if p in table.final else None  # @line L14


def one_pass_match(regex: Regex, word: str) -> bool:
    """Decide whether `word` is in L(regex); raise NotOnePass if the check fails."""
    return run_one_pass(compile_one_pass(regex), word) is not None


def is_one_pass(regex: Regex) -> bool:
    """True when the expression is one-unambiguous (its trimmed Glushkov automaton is deterministic)."""
    try:
        compile_one_pass(regex)
    except NotOnePass:
        return False
    return True
