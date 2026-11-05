# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backtracking-regex-matching/. The authors are listed in prov/AA2R4Q.jsonl.

"""Backtracking regex matching with an explicit stack.

A regular expression is a tuple:
("empty",) for the empty language, ("eps",) for the empty string,
("sym", a) for one symbol, ("alt", r, s), ("cat", r, s) and ("star", r).
A continuation is a linked list of items: None, or (item, rest).
An item is a regular expression or ("check", star_node, j).
"""

from __future__ import annotations

from typing import Any

Regex = tuple[Any, ...]
Cont = tuple[Any, Any] | None


def backtracking_match(regex: Regex, word: str, stats: dict[str, int] | None = None) -> bool:
    """Decide whether the whole of `word` is in the language of `regex`.

    The search tries the choices of the expression depth-first: the left side of
    a union first, and one more iteration of a star before leaving it. A star
    iteration that consumes no symbol is cut, so the search always stops.
    Precondition: `regex` is built from the tuples above.
    Cost: exponential in len(word) in the worst case, 2^O(m^2 n) steps for a
    regex of m nodes and a word of n symbols; no recursion is used.
    If `stats` is a dict, stats["steps"] receives the number of popped configurations.
    """
    n = len(word)
    stack: list[tuple[int, Cont]] = [(0, (regex, None))]  # @line L1
    steps = 0
    found = False
    while stack:  # @line L2
        i, k = stack.pop()  # @line L3
        steps += 1
        if k is None:  # @line L4
            if i == n:  # @line L5
                found = True
                break
            continue  # @line L6
        x, rest = k  # @line L7
        tag = x[0]
        if tag == "empty":  # @line L8
            continue
        if tag == "eps":  # @line L9
            stack.append((i, rest))
        elif tag == "sym":  # @line L10
            if i < n and word[i] == x[1]:
                stack.append((i + 1, rest))
        elif tag == "alt":  # @line L11
            stack.append((i, (x[2], rest)))
            stack.append((i, (x[1], rest)))
        elif tag == "cat":  # @line L12
            stack.append((i, (x[1], (x[2], rest))))
        elif tag == "star":  # @line L13
            stack.append((i, rest))
            stack.append((i, (x[1], (("check", x, i), rest))))
        elif tag == "check":  # @line L14
            if i > x[2]:
                stack.append((i, (x[1], rest)))
        else:
            raise ValueError(f"unknown node {x!r}")
    if stats is not None:
        stats["steps"] = steps
    return found  # @line L15
