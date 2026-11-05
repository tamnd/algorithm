# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/antimirov-derivatives/. The authors are listed in prov/B0378X.jsonl.

"""Antimirov partial derivatives and the partial derivative automaton.

A regular expression is a tuple:
("empty",) for the empty language, ("eps",) for the empty string,
("sym", a) for one symbol, ("alt", r, s), ("cat", r, s) and ("star", r).

Terms are hash-consed: each distinct term is a small integer, so equal
terms are shared and a set of terms is a frozenset of integers. The
partial derivative of a term by a symbol is a set of terms, and the terms
reachable from the input expression are the states of an NFA with at most
k + 1 states, where k is the number of symbol occurrences.
"""

from __future__ import annotations

from typing import Any

Regex = tuple[Any, ...]

EMPTY, EPS, SYM, ALT, CAT, STAR = range(6)
_KIND = {"empty": EMPTY, "eps": EPS, "sym": SYM, "alt": ALT, "cat": CAT, "star": STAR}


class Terms:
    """A store of hash-consed terms with memoized nullability and partial derivatives."""

    def __init__(self) -> None:
        self.node: list[tuple[Any, ...]] = []
        self.nullable: list[bool] = []
        self._ids: dict[tuple[Any, ...], int] = {}
        self._memo: dict[tuple[int, str], frozenset[int]] = {}
        self.empty = self._make((EMPTY,))
        self.eps = self._make((EPS,))

    def _make(self, key: tuple[Any, ...]) -> int:
        i = self._ids.get(key)
        if i is not None:
            return i
        kind = key[0]
        if kind == EMPTY or kind == SYM:
            nul = False
        elif kind == EPS or kind == STAR:
            nul = True
        elif kind == ALT:
            nul = self.nullable[key[1]] or self.nullable[key[2]]
        else:
            nul = self.nullable[key[1]] and self.nullable[key[2]]
        i = len(self.node)
        self.node.append(key)
        self.nullable.append(nul)
        self._ids[key] = i
        return i

    def intern(self, regex: Regex) -> int:
        """The id of a tuple regex, built bottom-up with an explicit stack."""
        out: list[int] = []
        todo: list[tuple[Regex, bool]] = [(regex, False)]
        while todo:
            r, ready = todo.pop()
            kind = _KIND.get(r[0])
            if kind is None:
                raise ValueError(f"unknown node {r!r}")
            if kind in (ALT, CAT, STAR) and not ready:
                todo.append((r, True))
                for child in reversed(r[1:]):
                    todo.append((child, False))
                continue
            if kind == EMPTY:
                out.append(self.empty)
            elif kind == EPS:
                out.append(self.eps)
            elif kind == SYM:
                out.append(self._make((SYM, r[1])))
            elif kind == STAR:
                out.append(self._make((STAR, out.pop())))
            else:
                right = out.pop()
                left = out.pop()
                out.append(self._make((kind, left, right)))
        return out.pop()

    def odot(self, terms: frozenset[int], t: int) -> frozenset[int]:
        """S ⊙ t: concatenate t to each term of S, with ε t = t, S ∅ = ∅ and S ε = S."""
        if t == self.empty:  # @line L14
            return frozenset()
        if t == self.eps:
            return terms
        return frozenset(t if z == self.eps else self._make((CAT, z, t)) for z in terms)

    def partial(self, x: int, a: str) -> frozenset[int]:
        """The set of partial derivatives of term x by the symbol a (memoized, no recursion)."""
        memo = self._memo
        if (x, a) in memo:
            return memo[(x, a)]
        stack = [x]
        while stack:
            y = stack[-1]
            if (y, a) in memo:
                stack.pop()
                continue
            node = self.node[y]
            kind = node[0]
            if kind == EMPTY or kind == EPS:  # @line L9
                result: frozenset[int] | None = frozenset()
            elif kind == SYM:  # @line L10
                result = frozenset([self.eps]) if node[1] == a else frozenset()
            elif kind == ALT:  # @line L11
                need = [c for c in node[1:] if (c, a) not in memo]
                result = None if need else memo[(node[1], a)] | memo[(node[2], a)]
            elif kind == CAT:  # @line L12
                s, t = node[1], node[2]
                need = [c for c in ([s, t] if self.nullable[s] else [s]) if (c, a) not in memo]
                if need:
                    result = None
                else:
                    result = self.odot(memo[(s, a)], t)
                    if self.nullable[s]:
                        result = result | memo[(t, a)]
            else:  # @line L13
                need = [] if (node[1], a) in memo else [node[1]]
                result = None if need else self.odot(memo[(node[1], a)], y)
            if result is None:
                stack.extend(need)
            else:
                memo[(y, a)] = result
                stack.pop()
        return memo[(x, a)]

    def symbols(self, x: int) -> list[str]:
        """The distinct symbols that occur in term x, sorted."""
        seen = {x}
        stack = [x]
        out: set[str] = set()
        while stack:
            node = self.node[stack.pop()]
            if node[0] == SYM:
                out.add(node[1])
            elif node[0] in (ALT, CAT, STAR):
                for c in node[1:]:
                    if c not in seen:
                        seen.add(c)
                        stack.append(c)
        return sorted(out)

    def show(self, x: int) -> str:
        """The term x in this site's notation, with parentheses where needed."""
        prec = {ALT: 0, CAT: 1, STAR: 2}
        out: list[str] = []
        todo: list[Any] = [(x, 0)]
        while todo:
            item = todo.pop()
            if isinstance(item, str):
                out.append(item)
                continue
            y, ctx = item
            node = self.node[y]
            kind = node[0]
            if kind == EMPTY:
                out.append("∅")
                continue
            if kind == EPS:
                out.append("ε")
                continue
            if kind == SYM:
                out.append(node[1])
                continue
            p = prec[kind]
            parts: list[Any] = []
            if p < ctx:
                parts.append("(")
            if kind == ALT:
                parts += [(node[1], 0), " | ", (node[2], 0)]
            elif kind == CAT:
                parts += [(node[1], 1), (node[2], 2)]
            else:
                parts += [(node[1], 3), "*"]
            if p < ctx:
                parts.append(")")
            todo.extend(reversed(parts))
        return "".join(out)


class PDAutomaton:
    """The partial derivative automaton of a regular expression."""

    def __init__(self, regex: Regex) -> None:
        self.terms = T = Terms()
        self.start = T.intern(regex)
        self.alphabet = T.symbols(self.start)
        self.states: list[int] = [self.start]  # @line L1
        self.delta: dict[int, dict[str, frozenset[int]]] = {}
        seen = {self.start}
        todo = [self.start]
        while todo:  # @line L2
            x = todo.pop()  # @line L3
            row: dict[str, frozenset[int]] = {}
            for a in self.alphabet:  # @line L4
                targets = T.partial(x, a)  # @line L5
                if targets:
                    row[a] = targets  # @line L6
                for y in targets:
                    if y not in seen:  # @line L7
                        seen.add(y)
                        self.states.append(y)
                        todo.append(y)
            self.delta[x] = row
        self.final = frozenset(x for x in self.states if T.nullable[x])  # @line L8

    def transitions(self) -> int:
        """The number of moves (x, a, y)."""
        return sum(len(ys) for row in self.delta.values() for ys in row.values())

    def accepts(self, word: str) -> bool:
        """Decide whether word is in the language, by running the NFA on sets of states."""
        current = {self.start}  # @line L16
        for c in word:  # @line L17
            nxt: set[int] = set()
            for x in current:
                nxt |= self.delta[x].get(c, frozenset())
            current = nxt
            if not current:
                return False
        return not self.final.isdisjoint(current)  # @line L18

    def accepts_from(self, x: int, word: str) -> bool:
        """Decide whether word is in the language of the state x."""
        current = {x}
        for c in word:
            nxt: set[int] = set()
            for y in current:
                nxt |= self.delta[y].get(c, frozenset())
            current = nxt
        return not self.final.isdisjoint(current)


def symbol_occurrences(regex: Regex) -> int:
    """k, the number of symbol leaves of the tuple regex."""
    count = 0
    stack = [regex]
    while stack:
        r = stack.pop()
        if r[0] == "sym":
            count += 1
        elif r[0] in ("alt", "cat", "star"):
            stack.extend(r[1:])
    return count


def antimirov_match(regex: Regex, word: str) -> bool:
    """Decide whether word is in L(regex) with the partial derivative automaton."""
    automaton = PDAutomaton(regex)  # @line L15
    return automaton.accepts(word)
