# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/left-corner-parsing/. The authors are listed in prov/P8PFGP.jsonl.

"""Generalized left-corner recognizer for any context-free grammar.

A grammar is a list of productions (A, rhs), where rhs is a tuple of symbols.
The nonterminals are the left sides and the start symbol; every other symbol
is a terminal. Empty right sides, unit productions, cycles, left recursion and
ambiguity are all allowed.

A left-corner parser finds the first symbol of each production bottom-up, from
the input, and the other symbols top-down, as goals. This recognizer runs all
choices of such a parser at once with a chart. An item [C, i, B -> alpha . beta]
in E[k] says: while looking for the goal C from position i, the parser has
found alpha from i to k, and B is a left corner of C. DONE holds the triples
(C, i, k) such that the goal C was found from i to k.
"""

from typing import Sequence

Production = tuple[str, tuple[str, ...]]
Item = tuple[str, int, int, int]        # (goal C, start i, production index, dot)


def left_corner_closure(productions: Sequence[Production], start: str) -> dict[str, set[str]]:
    """L[C]: the nonterminals B with C = B or C -> B ... -> ... B ... (first symbols)."""
    nts = {a for a, _ in productions} | {start}
    first: dict[str, set[str]] = {a: set() for a in nts}
    for a, rhs in productions:
        if rhs and rhs[0] in nts:
            first[a].add(rhs[0])
    closure: dict[str, set[str]] = {}
    for c in nts:
        seen = {c}
        todo = [c]
        while todo:
            b = todo.pop()
            for d in first[b]:
                if d not in seen:
                    seen.add(d)
                    todo.append(d)
        closure[c] = seen
    return closure


def left_corner_chart(productions: Sequence[Production], start: str, w: Sequence[str]
                      ) -> tuple[list[list[Item]], dict[tuple[str, int], set[int]]]:
    """Return the chart E[0..n] and DONE as a map (C, i) -> set of ends k."""
    prods = [(a, tuple(r)) for a, r in productions]
    nts = {a for a, _ in prods} | {start}
    n = len(w)
    lc = left_corner_closure(prods, start)                               # @line L1
    by_first: dict[str, list[int]] = {}        # productions D -> X gamma, by X
    empty: list[int] = []                      # productions D -> epsilon
    for p, (a, rhs) in enumerate(prods):
        if rhs:
            by_first.setdefault(rhs[0], []).append(p)
        else:
            empty.append(p)
    chart: list[list[Item]] = [[] for _ in range(n + 1)]
    seen: list[set[Item]] = [set() for _ in range(n + 1)]
    done: dict[tuple[str, int], set[int]] = {}
    found: list[set[tuple[str, int, str]]] = [set() for _ in range(n + 1)]
    waiting: dict[tuple[str, int], list[Item]] = {}

    def add(item: Item, k: int) -> None:
        if item not in seen[k]:
            seen[k].add(item)
            chart[k].append(item)

    def start_goal(c: str, k: int) -> None:
        done[(c, k)] = set()
        waiting.setdefault((c, k), [])
        if k < n:                                                        # @line L14
            for p in by_first.get(w[k], []):
                if w[k] not in nts and prods[p][0] in lc[c]:
                    add((c, k, p, 1), k + 1)
        for p in empty:                                                  # @line L15
            if prods[p][0] in lc[c]:
                add((c, k, p, 0), k)

    start_goal(start, 0)                                                 # @line L2
    for k in range(n + 1):                                               # @line L3
        idx = 0
        while idx < len(chart[k]):                                       # @line L4
            c, i, p, d = chart[k][idx]
            idx += 1
            b, rhs = prods[p]
            if d == len(rhs):                                            # @line L5
                if (c, i, b) in found[k]:      # B was already found from i to k under C
                    continue
                found[k].add((c, i, b))
                if b == c and k not in done[(c, i)]:                     # @line L6
                    done[(c, i)].add(k)
                    for (c2, i2, p2, d2) in waiting[(c, i)]:
                        add((c2, i2, p2, d2 + 1), k)
                for q in by_first.get(b, []):                            # @line L7
                    if prods[q][0] in lc[c]:
                        add((c, i, q, 1), k)
            elif rhs[d] in nts:                                          # @line L8
                y = rhs[d]
                if (y, k) not in done:                                   # @line L10
                    start_goal(y, k)
                waiting[(y, k)].append((c, i, p, d))                     # @line L9
                for k2 in list(done[(y, k)]):                            # @line L11
                    add((c, i, p, d + 1), k2)
            elif k < n and rhs[d] == w[k]:                               # @line L12
                add((c, i, p, d + 1), k + 1)
    return chart, done


def left_corner_recognize(productions: Sequence[Production], start: str, w: Sequence[str]) -> bool:
    """Return True if w is in the language of the grammar."""
    _, done = left_corner_chart(productions, start, w)
    return len(w) in done[(start, 0)]                                    # @line L13
