# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brzozowski-derivatives/. The authors are listed in prov/XAA52M.jsonl.

"""Regex matching by Brzozowski derivatives.

A regular expression is a tuple:
("empty",) for the empty language, ("eps",) for the empty string,
("sym", a) for one symbol, ("alt", r, s), ("cat", r, s) and ("star", r).

Inside, expressions are hash-consed: each distinct node gets an integer id,
a union is stored as a frozenset of ids (so it is associative, commutative
and idempotent), and the constructors apply the rules for the empty language
and the empty string. Derivatives are memoized by (id, symbol).
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

Regex = tuple[Any, ...]

EMPTY = 0
EPS = 1


class Builder:
    """A table of normalized expressions, with nullability and derivative caches."""

    def __init__(self) -> None:
        self.nodes: list[tuple[Any, ...]] = [("empty",), ("eps",)]
        self.index: dict[tuple[Any, ...], int] = {("empty",): EMPTY, ("eps",): EPS}
        self.nullable: list[bool] = [False, True]
        self.cache: dict[tuple[int, str], int] = {}

    def _intern(self, node: tuple[Any, ...], nullable: bool) -> int:
        found = self.index.get(node)
        if found is not None:
            return found
        self.nodes.append(node)
        self.nullable.append(nullable)
        self.index[node] = len(self.nodes) - 1
        return len(self.nodes) - 1

    def sym(self, a: str) -> int:
        return self._intern(("sym", a), False)

    def cat(self, x: int, y: int) -> int:
        """Concatenation with ∅x = x∅ = ∅ and εx = xε = x."""
        if x == EMPTY or y == EMPTY:  # @line L10
            return EMPTY
        if x == EPS:
            return y
        if y == EPS:
            return x
        return self._intern(("cat", x, y), self.nullable[x] and self.nullable[y])

    def alt(self, x: int, y: int) -> int:
        """Union as a set of alternatives, without ∅ and without repeats."""
        return self.alt_many((x, y))

    def alt_many(self, parts: Iterable[int]) -> int:
        """The union of all `parts`, flattened into one set of alternatives."""
        members: set[int] = set()  # @line L11
        for z in parts:
            node = self.nodes[z]
            if node[0] == "alt":
                members |= node[1]
            elif z != EMPTY:
                members.add(z)
        if not members:
            return EMPTY
        if len(members) == 1:
            return next(iter(members))
        nullable = any(self.nullable[z] for z in members)
        return self._intern(("alt", frozenset(members)), nullable)

    def star(self, x: int) -> int:
        """Star with ∅* = ε* = ε and (x*)* = x*."""
        if x == EMPTY or x == EPS:  # @line L12
            return EPS
        if self.nodes[x][0] == "star":
            return x
        return self._intern(("star", x), True)

    def build(self, regex: Regex) -> int:
        """Intern a tuple expression, in postorder with an explicit stack."""
        out: list[int] = []
        todo: list[tuple[Regex, bool]] = [(regex, False)]
        while todo:
            node, ready = todo.pop()
            tag = node[0]
            if not ready and tag in ("alt", "cat", "star"):
                todo.append((node, True))
                for child in reversed(node[1:]):
                    todo.append((child, False))
                continue
            if tag == "empty":
                out.append(EMPTY)
            elif tag == "eps":
                out.append(EPS)
            elif tag == "sym":
                out.append(self.sym(node[1]))
            elif tag == "star":
                out.append(self.star(out.pop()))
            elif tag in ("alt", "cat"):
                y = out.pop()
                x = out.pop()
                out.append(self.alt(x, y) if tag == "alt" else self.cat(x, y))
            else:
                raise ValueError(f"unknown node {node!r}")
        return out.pop()

    def derivative(self, r: int, a: str) -> int:
        """The normalized derivative of r by the symbol a.

        Postorder over the nodes that the rules need, with an explicit stack;
        results are kept in self.cache.
        """
        cache = self.cache
        todo: list[tuple[int, bool]] = [(r, False)]
        while todo:
            x, ready = todo.pop()
            if (x, a) in cache:
                continue
            node = self.nodes[x]
            tag = node[0]
            if tag in ("empty", "eps"):  # @line L5
                cache[(x, a)] = EMPTY
                continue
            if tag == "sym":  # @line L6
                cache[(x, a)] = EPS if node[1] == a else EMPTY
                continue
            if tag == "alt":
                needed = list(node[1])
            elif tag == "cat":
                needed = [node[1], node[2]] if self.nullable[node[1]] else [node[1]]
            else:
                needed = [node[1]]
            if not ready:
                todo.append((x, True))
                todo.extend((z, False) for z in needed if (z, a) not in cache)
                continue
            if tag == "alt":  # @line L7
                d = self.alt_many(cache[(z, a)] for z in node[1])
            elif tag == "cat":  # @line L8
                d = self.cat(cache[(node[1], a)], node[2])
                if self.nullable[node[1]]:
                    d = self.alt(d, cache[(node[2], a)])
            else:  # @line L9
                d = self.cat(cache[(node[1], a)], x)
            cache[(x, a)] = d
        return cache[(r, a)]

    def show(self, x: int) -> str:
        """Render an expression with | , concatenation, *, ε and ∅ (for examples)."""
        out: dict[int, str] = {}
        prec: dict[int, int] = {}
        todo: list[tuple[int, bool]] = [(x, False)]
        while todo:
            y, ready = todo.pop()
            if y in out:
                continue
            node = self.nodes[y]
            kids = sorted(node[1], key=self._key) if node[0] == "alt" else [z for z in node[1:] if isinstance(z, int)]
            if node[0] == "sym":
                kids = []
            if not ready and kids:
                todo.append((y, True))
                todo.extend((z, False) for z in kids)
                continue
            tag = node[0]
            if tag == "empty":
                out[y], prec[y] = "∅", 3
            elif tag == "eps":
                out[y], prec[y] = "ε", 3
            elif tag == "sym":
                out[y], prec[y] = node[1], 3
            elif tag == "star":
                s = out[node[1]] if prec[node[1]] == 3 else "(" + out[node[1]] + ")"
                out[y], prec[y] = s + "*", 3
            elif tag == "cat":
                parts = [out[z] if prec[z] >= 2 else "(" + out[z] + ")" for z in node[1:]]
                out[y], prec[y] = "".join(parts), 2
            else:
                out[y], prec[y] = "|".join(out[z] for z in kids), 1
        return out[x]

    def _key(self, z: int) -> tuple[int, int]:
        return (len(self.nodes[z]), z)


def derivative_match(regex: Regex, word: str, builder: Builder | None = None) -> bool:
    """Decide whether `word` is in L(regex) by taking one derivative per symbol.

    Cost: per symbol, O(size of the current derivative) hash operations the
    first time a (derivative, symbol) pair occurs, and O(1) after that.
    """
    b = builder if builder is not None else Builder()
    r = b.build(regex)
    for c in word:  # @line L1
        r = b.derivative(r, c)  # @line L2
        if r == EMPTY:  # @line L3
            return False
    return b.nullable[r]  # @line L4


def derivative_dfa(regex: Regex, alphabet: str) -> tuple[list[int], list[dict[str, int]], set[int]]:
    """Build the DFA whose states are the normalized derivatives of `regex`.

    Returns the states (expression ids, the first is the start), the
    transition table and the set of accepting state numbers.
    """
    b = Builder()
    start = b.build(regex)
    states = [start]
    number = {start: 0}
    delta: list[dict[str, int]] = []
    i = 0
    while i < len(states):
        row = {}
        for c in alphabet:
            d = b.derivative(states[i], c)
            if d not in number:
                number[d] = len(states)
                states.append(d)
            row[c] = number[d]
        delta.append(row)
        i += 1
    accepting = {number[s] for s in states if b.nullable[s]}
    return states, delta, accepting
