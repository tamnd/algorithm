# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-parsing/. The authors are listed in prov/3Y0Y57.jsonl.

"""Incremental Earley recognition: reparse an edited string and reuse the old chart.

A grammar is a list of productions (A, rhs), where rhs is a tuple of symbols.
The nonterminals are the left sides; every other symbol is a terminal. Empty
right sides, unit productions, left recursion, cycles and ambiguity are all
allowed. An item (p, dot, origin) stands for [A -> alpha . beta, origin], where
productions[p] = (A, alpha beta) and len(alpha) = dot. A chart is a list of
item sets E[0], ..., E[n], one for each position of the input.

An edit (p, q, v) replaces the tokens w[p:q] by the tuple v. The sets E[0..p]
do not change. The sets after the edit are computed again until a set is
"anchored": it equals the old set with origins shifted, and every origin it
uses is anchored or before the edit. From there on, the old sets are shifted
and reused.
"""

from typing import Iterable, Sequence

Production = tuple[str, tuple[str, ...]]
Item = tuple[int, int, int]
Chart = list[frozenset[Item]]


class Grammar:
    """A grammar with the tables that Earley sets need."""

    def __init__(self, productions: Sequence[Production], start: str) -> None:
        self.productions = list(productions)
        self.start = start
        self.nts = {a for a, _ in self.productions}
        self.by_lhs: dict[str, list[int]] = {}
        for i, (a, _) in enumerate(self.productions):
            self.by_lhs.setdefault(a, []).append(i)
        self.nullable: set[str] = set()
        changed = True
        while changed:
            changed = False
            for a, rhs in self.productions:
                if a not in self.nullable and all(x in self.nullable for x in rhs):
                    self.nullable.add(a)
                    changed = True


def earley_set(g: Grammar, chart: Sequence[frozenset[Item]], seed: Iterable[Item], j: int) -> frozenset[Item]:
    """Return E[j]: the closure of seed under prediction and completion.

    chart[0..j-1] are the earlier sets; completion with origin i < j reads
    chart[i], through an index by the symbol after the dot that is built once
    for each such i. The nullable rule of Aycock and Horspool makes one pass
    enough."""
    items: list[Item] = []
    seen: set[Item] = set()
    waiting: dict[str, list[Item]] = {}
    index: dict[int, dict[str, list[Item]]] = {}

    def add(item: Item) -> None:
        if item in seen:
            return
        seen.add(item)
        items.append(item)
        p, dot, _ = item
        rhs = g.productions[p][1]
        if dot < len(rhs):
            waiting.setdefault(rhs[dot], []).append(item)

    for item in seed:
        add(item)
    predicted: set[str] = set()
    completed: set[tuple[str, int]] = set()
    k = 0
    while k < len(items):
        p, dot, origin = items[k]
        k += 1
        lhs, rhs = g.productions[p]
        if dot == len(rhs):
            if (lhs, origin) in completed:
                continue
            completed.add((lhs, origin))
            if origin == j:
                waiters = list(waiting.get(lhs, []))
            else:
                if origin not in index:
                    table: dict[str, list[Item]] = {}
                    for it in chart[origin]:
                        x = _after(g, it)
                        if x is not None:
                            table.setdefault(x, []).append(it)
                    index[origin] = table
                waiters = index[origin].get(lhs, [])
            for q, qdot, qorig in waiters:
                add((q, qdot + 1, qorig))
        elif rhs[dot] in g.nts:
            x = rhs[dot]
            if x not in predicted:
                predicted.add(x)
                for q in g.by_lhs[x]:
                    add((q, 0, j))
            if x in g.nullable:
                add((p, dot + 1, origin))
    return frozenset(items)


def _after(g: Grammar, item: Item) -> str | None:
    p, dot, _ = item
    rhs = g.productions[p][1]
    return rhs[dot] if dot < len(rhs) else None


def scan_seed(g: Grammar, prev: frozenset[Item], a: str) -> list[Item]:
    """Items of prev with the terminal a after the dot, with the dot moved past a."""
    out = []
    for p, dot, origin in prev:
        rhs = g.productions[p][1]
        if dot < len(rhs) and rhs[dot] == a and rhs[dot] not in g.nts:
            out.append((p, dot + 1, origin))
    return out


def earley_chart(g: Grammar, w: Sequence[str]) -> Chart:
    """The full Earley chart of w, computed from scratch."""
    chart: Chart = []
    seed = [(p, 0, 0) for p in g.by_lhs.get(g.start, [])]
    for j in range(len(w) + 1):
        if j > 0:
            seed = scan_seed(g, chart[j - 1], w[j - 1])
        chart.append(earley_set(g, chart, seed, j))
    return chart


def accepts(g: Grammar, chart: Chart) -> bool:
    """True when some [S -> alpha ., 0] is in the last set."""
    for p, dot, origin in chart[-1]:
        a, rhs = g.productions[p]
        if a == g.start and dot == len(rhs) and origin == 0:
            return True
    return False


def reparse(g: Grammar, w: Sequence[str], chart: Chart, p: int, q: int,
            v: Sequence[str]) -> tuple[list[str], Chart, int]:
    """Replace w[p:q] by v. Return (the new string, its chart, the number of
    sets computed again). chart must be the Earley chart of w."""
    n = len(w)
    if not 0 <= p <= q <= n:
        raise ValueError("need 0 <= p <= q <= len(w)")
    w2 = list(w[:p]) + list(v) + list(w[q:])                          # @line L1
    n2 = len(w2)
    delta = len(v) - (q - p)
    q2 = p + len(v)

    def shift_origin(i: int) -> int:
        return i + delta if i >= q else i

    def shift(old: frozenset[Item]) -> frozenset[Item]:
        return frozenset((pp, dot, shift_origin(i)) for pp, dot, i in old)

    new: Chart = list(chart[:p + 1])                                  # @line L2
    anchored: dict[int, bool] = {}
    recomputed = 0
    for k in range(p, n2 + 1):                                        # @line L3
        if k > p:                                                     # @line L4
            new.append(earley_set(g, new, scan_seed(g, new[k - 1], w2[k - 1]), k))
            recomputed += 1
        if k >= q2:                                                   # @line L5
            old = chart[k - delta]
            ok = all((i < q and i <= p) or                            # @line L6
                     (i >= q and (i == k - delta or anchored[i + delta]))
                     for _, _, i in old)
            ok = ok and new[k] == shift(old)                          # @line L7
            anchored[k] = ok
            if ok:                                                    # @line L8
                for j in range(k + 1, n2 + 1):                        # @line L9
                    new.append(shift(chart[j - delta]))
                return w2, new, recomputed                            # @line L10
    return w2, new, recomputed                                        # @line L11


def recognize_after_edit(g: Grammar, w: Sequence[str], chart: Chart, p: int, q: int,
                         v: Sequence[str]) -> bool:
    """True when the start symbol derives the edited string."""
    _, new, _ = reparse(g, w, chart, p, q, v)
    return accepts(g, new)                                            # @line L12
