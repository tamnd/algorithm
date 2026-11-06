# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shift-reduce-parsing/. The authors are listed in prov/PZXCZZ.jsonl.

"""Shift-reduce parsing: a generic driver and an exact decision procedure.

A grammar is a list of productions (A, rhs) with rhs a tuple of symbols; the
nonterminals are the left sides, every other symbol is a terminal. A tree is
(A, children) where each child is a tree or a terminal.

`shift_reduce(tokens, decide)` is the driver of the page. It knows nothing
about how to choose a move: `decide(symbols, pos)` returns ("shift",),
("reduce", k) for production k, ("accept",) or ("error",).

`ExactDecider` is a decision procedure that works for every context-free
grammar, including ambiguous ones, epsilon-productions and cycles. It sees the
whole input. It calls a configuration good if some sequence of moves from it
ends in accept, and it tests this with the item chains of the stack:
the stack X1...Xm is good at position pos iff it is beta_1 ... beta_m for a
chain of items [S' -> beta_1 . A_2 delta_1], [A_2 -> beta_2 . A_3 delta_2], ...,
[A_m -> beta_m . delta_m] with delta_m delta_(m-1) ... delta_1 =>* w[pos:].
It shifts when shifting keeps the configuration good, and otherwise takes the
first move of a shortest sequence of good reductions after which a shift (or
accept) is good. Deterministic methods such as LR(1) replace it with a table.
"""

from collections import deque
from typing import Callable, Sequence

Production = tuple[str, tuple[str, ...]]
AUG = -1  # the augmented production S' -> S


class ParseError(ValueError):
    """The input is not in the language of the grammar."""


def shift_reduce(
    tokens: Sequence[str],
    prods: Sequence[Production],
    decide: Callable[[list[str], int], tuple],
    trace: list | None = None,
):
    """Run the shift-reduce driver. Returns (tree, reductions), where
    reductions is the list of production indices in the order they were used."""
    stack: list = []  # @line L1: stack of (symbol, tree) pairs; pos = 0
    pos = 0
    reductions: list[int] = []
    while True:  # @line L2
        symbols = [s for s, _ in stack]
        act = decide(symbols, pos)  # @line L3
        if trace is not None:
            trace.append((" ".join(symbols), " ".join(tokens[pos:]), act))
        if act[0] == "shift":  # @line L4
            stack.append((tokens[pos], tokens[pos]))  # @line L5
            pos += 1
        elif act[0] == "reduce":  # @line L6
            a, rhs = prods[act[1]]
            k = len(rhs)
            popped = stack[len(stack) - k:] if k else []  # @line L7
            assert [s for s, _ in popped] == list(rhs), "decide chose a reduction that is not on top"
            del stack[len(stack) - k:]
            stack.append((a, (a, tuple(t for _, t in popped))))  # @line L8
            reductions.append(act[1])
        elif act[0] == "accept":  # @line L9
            return stack[0][1], reductions
        else:  # @line L10
            raise ParseError(f"no move at token {pos}")


def _spans(prods: Sequence[Production], w: Sequence[str]) -> set:
    """The set of (A, i, j) with A =>* w[i:j], by a least fixpoint."""
    nts = {a for a, _ in prods}
    n = len(w)
    known: set = set()
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            for i in range(n + 1):
                ends = {i}
                for x in rhs:
                    nxt = set()
                    for p in ends:
                        if x in nts:
                            nxt.update(q for q in range(p, n + 1) if (x, p, q) in known)
                        elif p < n and w[p] == x:
                            nxt.add(p + 1)
                    ends = nxt
                for j in ends:
                    if (a, i, j) not in known:
                        known.add((a, i, j))
                        changed = True
    return known


class ExactDecider:
    """The exact decision procedure for one input w (see the module docstring)."""

    def __init__(self, prods: Sequence[Production], start: str, tokens: Sequence[str]) -> None:
        self.prods = [(a, tuple(r)) for a, r in prods]
        self.start = start
        self.nts = {a for a, _ in self.prods}
        self.w = list(tokens)
        self.n = len(self.w)
        self.known = _spans(self.prods, self.w)
        self.by_lhs: dict[str, list[int]] = {a: [] for a in self.nts}
        for k, (a, _) in enumerate(self.prods):
            self.by_lhs[a].append(k)
        self._ends: dict = {}
        self._sets: dict = {(): self._closure({(AUG, 0, self.n)})}

    def rhs(self, k: int) -> tuple[str, ...]:
        return (self.start,) if k == AUG else self.prods[k][1]

    def ends(self, k: int, d: int, i: int) -> frozenset:
        """All j with rhs(k)[d:] =>* w[i:j]."""
        key = (k, d, i)
        if key not in self._ends:
            cur = {i}
            for x in self.rhs(k)[d:]:
                nxt = set()
                for p in cur:
                    if x in self.nts:
                        nxt.update(q for q in range(p, self.n + 1) if (x, p, q) in self.known)
                    elif p < self.n and self.w[p] == x:
                        nxt.add(p + 1)
                cur = nxt
            self._ends[key] = frozenset(cur)
        return self._ends[key]

    def _closure(self, items: set) -> frozenset:
        todo = list(items)
        out = set(items)
        while todo:
            k, d, e = todo.pop()
            r = self.rhs(k)
            if d < len(r) and r[d] in self.nts:
                for e2 in range(e + 1):
                    if e in self.ends(k, d + 1, e2):
                        for kb in self.by_lhs[r[d]]:
                            it = (kb, 0, e2)
                            if it not in out:
                                out.add(it)
                                todo.append(it)
        return frozenset(out)

    def items(self, symbols: tuple) -> frozenset:
        """The (item, end) pairs of all item chains that spell the stack.
        Built from the longest cached prefix, one symbol at a time."""
        m = len(symbols)
        while symbols[:m] not in self._sets:
            m -= 1
        for j in range(m + 1, len(symbols) + 1):
            x = symbols[j - 1]
            below = self._sets[symbols[: j - 1]]
            moved = {(k, d + 1, e) for k, d, e in below if d < len(self.rhs(k)) and self.rhs(k)[d] == x}
            self._sets[symbols[:j]] = self._closure(moved)
        return self._sets[symbols]

    def good(self, symbols: tuple, pos: int) -> bool:
        return any(e in self.ends(k, d, pos) for k, d, e in self.items(symbols))

    def _target(self, symbols: tuple, pos: int) -> bool:
        if pos == self.n:
            return symbols == (self.start,)
        return self.good(symbols + (self.w[pos],), pos + 1)

    def _reductions(self, symbols: tuple):
        for k, (a, r) in enumerate(self.prods):
            if len(r) <= len(symbols) and symbols[len(symbols) - len(r):] == r:
                yield k, symbols[: len(symbols) - len(r)] + (a,)

    def __call__(self, stack_symbols: list[str], pos: int) -> tuple:
        cur = tuple(stack_symbols)
        if not self.good(cur, pos):
            return ("error",)
        if pos == self.n and cur == (self.start,):
            return ("accept",)
        if pos < self.n and self._target(cur, pos):
            return ("shift",)
        # Breadth-first search over good reductions for the nearest target.
        first: dict = {cur: None}
        queue = deque([cur])
        while queue:
            s = queue.popleft()
            for k, t in self._reductions(s):
                if t in first or not self.good(t, pos):
                    continue
                first[t] = k if first[s] is None else first[s]
                if self._target(t, pos):
                    return ("reduce", first[t])
                queue.append(t)
        return ("error",)  # unreachable when the configuration is good


def parse(prods: Sequence[Production], start: str, tokens: Sequence[str], trace: list | None = None):
    """Parse tokens with the exact decider; returns (tree, reductions)."""
    if start not in {a for a, _ in prods}:
        raise ValueError("the start symbol has no production")
    return shift_reduce(list(tokens), prods, ExactDecider(prods, start, tokens), trace)
