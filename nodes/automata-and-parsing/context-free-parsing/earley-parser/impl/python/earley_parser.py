# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/earley-parser/. The authors are listed in prov/X30PDD.jsonl.

"""Earley's recognizer and parser for any context-free grammar.

A grammar is a list of productions (A, rhs), where rhs is a tuple of symbols.
The nonterminals are the left sides; every other symbol is a terminal. Empty
right sides, unit productions, left recursion, cycles and ambiguity are all
allowed. Empty productions are handled by the nullable-prediction rule of
Aycock and Horspool. An item (p, dot, origin) in set j stands for
[A -> alpha . beta, origin] where productions[p] = (A, alpha beta) and
len(alpha) = dot. A parse tree is (A, children), where each child is a tree or
a terminal symbol.
"""

from typing import Optional, Sequence, Union

Tree = tuple[str, tuple[Union["Tree", str], ...]]
Production = tuple[str, tuple[str, ...]]
Item = tuple[int, int, int]


def nullable_set(productions: Sequence[Production]) -> tuple[set[str], dict[str, int]]:
    """Return (N, why): N is the set of nonterminals that derive the empty
    string and why[A] is a production of A whose right side is made of
    nonterminals that became nullable before A (used to build empty trees)."""
    nullable: set[str] = set()
    why: dict[str, int] = {}
    changed = True
    while changed:
        changed = False
        for p, (a, rhs) in enumerate(productions):
            if a not in nullable and all(x in nullable for x in rhs):
                nullable.add(a)
                why[a] = p
                changed = True
    return nullable, why


class _Chart:
    """The item sets E[0..n] with one back pointer per item (its first creation)."""

    def __init__(self, n: int) -> None:
        self.items: list[list[Item]] = [[] for _ in range(n + 1)]
        self.seen: list[dict[Item, object]] = [{} for _ in range(n + 1)]
        self.waiting: list[dict[str, list[Item]]] = [{} for _ in range(n + 1)]

    def add(self, j: int, item: Item, after: Optional[str], back: object) -> None:
        if item in self.seen[j]:
            return
        self.seen[j][item] = back
        self.items[j].append(item)
        if after is not None:
            self.waiting[j].setdefault(after, []).append(item)


def _run(productions: Sequence[Production], start: str, w: Sequence[str]):
    nts = {a for a, _ in productions}
    by_lhs: dict[str, list[int]] = {}
    for p, (a, _) in enumerate(productions):
        by_lhs.setdefault(a, []).append(p)
    nullable, why = nullable_set(productions)                         # @line L1
    n = len(w)
    chart = _Chart(n)                                                 # @line L2

    def after(p: int, dot: int) -> Optional[str]:
        rhs = productions[p][1]
        return rhs[dot] if dot < len(rhs) else None

    for p in by_lhs.get(start, []):                                   # @line L3
        chart.add(0, (p, 0, 0), after(p, 0), None)
    for j in range(n + 1):                                            # @line L4
        predicted: set[str] = set()
        completed: set[tuple[str, int]] = set()
        k = 0
        while k < len(chart.items[j]):                                # @line L5
            item = chart.items[j][k]
            k += 1
            p, dot, origin = item
            lhs, rhs = productions[p]
            if dot == len(rhs):                                       # @line L6
                if (lhs, origin) in completed:
                    continue
                completed.add((lhs, origin))
                for q, qdot, qorig in list(chart.waiting[origin].get(lhs, [])):  # @line L7
                    nxt = (q, qdot + 1, qorig)
                    chart.add(j, nxt, after(q, qdot + 1), ("c", origin, (q, qdot, qorig), item))
            elif rhs[dot] in nts:                                     # @line L8
                x = rhs[dot]
                if x not in predicted:
                    predicted.add(x)
                    for q in by_lhs[x]:                               # @line L9
                        chart.add(j, (q, 0, j), after(q, 0), None)
                if x in nullable:                                     # @line L10
                    chart.add(j, (p, dot + 1, origin), after(p, dot + 1), ("e", item, x))
            elif j < n and rhs[dot] == w[j]:                          # @line L11
                chart.add(j + 1, (p, dot + 1, origin), after(p, dot + 1), ("t", item, w[j]))  # @line L12
    return chart, nullable, why


def earley_chart(productions: Sequence[Production], start: str, w: Sequence[str]) -> list[list[Item]]:
    """Return the item sets E[0], ..., E[n] as lists of (p, dot, origin), in insertion order."""
    if not any(a == start for a, _ in productions):
        return [[] for _ in range(len(w) + 1)]
    chart, _, _ = _run(productions, start, w)
    return chart.items


def _final_item(productions: Sequence[Production], start: str, chart: _Chart, n: int) -> Optional[Item]:
    for p, dot, origin in chart.items[n]:                             # @line L13
        a, rhs = productions[p]
        if a == start and dot == len(rhs) and origin == 0:
            return (p, dot, origin)
    return None


def earley_recognize(productions: Sequence[Production], start: str, w: Sequence[str]) -> bool:
    """Return True if and only if start derives the string w."""
    if not any(a == start for a, _ in productions):
        return False
    chart, _, _ = _run(productions, start, w)
    return _final_item(productions, start, chart, len(w)) is not None


def _empty_trees(productions: Sequence[Production], nullable: set[str], why: dict[str, int]) -> dict[str, Tree]:
    """One finite tree deriving the empty string for each nullable nonterminal.
    why[A] uses only nonterminals made nullable earlier, so a pass in that order works."""
    trees: dict[str, Tree] = {}
    for a in why:
        rhs = productions[why[a]][1]
        trees[a] = (a, tuple(trees[x] for x in rhs))
    return trees


def earley_parse(productions: Sequence[Production], start: str, w: Sequence[str]) -> Optional[Tree]:
    """Return one parse tree of w from start, or None if w is not in the language.

    Each item keeps the back pointer of its first creation, which points to items
    created strictly earlier, so following the pointers ends. The tree is built
    with an explicit stack, without recursion."""
    if not any(a == start for a, _ in productions):
        return None
    chart, nullable, why = _run(productions, start, w)
    n = len(w)
    root = _final_item(productions, start, chart, n)
    if root is None:
        return None
    eps = _empty_trees(productions, nullable, why)

    def children_refs(j: int, item: Item) -> list[tuple]:
        """Walk the back pointers of a completed item to its dot-0 item."""
        refs: list[tuple] = []
        cur_j, cur = j, item
        while True:
            back = chart.seen[cur_j][cur]
            if back is None:
                break
            kind = back[0]
            if kind == "t":
                refs.append(("t", back[2]))
                cur, cur_j = back[1], cur_j - 1
            elif kind == "e":
                refs.append(("e", back[2]))
                cur = back[1]
            else:
                _, mid, prev, child = back
                refs.append(("c", cur_j, child))
                cur, cur_j = prev, mid
        refs.reverse()
        return refs

    built: dict[tuple[int, Item], Tree] = {}
    stack: list[tuple[int, Item, bool]] = [(n, root, False)]
    while stack:
        j, item, ready = stack.pop()
        if (j, item) in built:
            continue
        refs = children_refs(j, item)
        if not ready:
            stack.append((j, item, True))
            for r in refs:
                if r[0] == "c" and (r[1], r[2]) not in built:
                    stack.append((r[1], r[2], False))
            continue
        kids: list[Union[Tree, str]] = []
        for r in refs:
            if r[0] == "t":
                kids.append(r[1])
            elif r[0] == "e":
                kids.append(eps[r[1]])
            else:
                kids.append(built[(r[1], r[2])])
        built[(j, item)] = (productions[item[0]][0], tuple(kids))
    return built[(n, root)]
