# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greibach-normal-form-conversion/. The authors are listed in prov/0QNXET.jsonl.

"""Convert a context-free grammar to Greibach normal form.

A grammar is a list of productions (A, rhs), where rhs is a tuple of symbols.
The nonterminals are the left sides; every other symbol is a terminal. The
result has only productions A -> a B1 ... Bk with a terminal a and nonterminals
Bi, plus S0 -> () for a fresh start S0 when the empty string is in the
language; S0 then occurs on no right side.

The method is the classical one: clean the grammar (no empty productions, no
unit productions, no useless symbols, terminals only in first position), order
the nonterminals, substitute and remove immediate left recursion so that each
A_i -> A_j ... has j > i, then substitute back from the last nonterminal to the
first. The output can be exponentially larger than the input.
"""

from itertools import product
from typing import Sequence

Production = tuple[str, tuple[str, ...]]
Grammar = dict[str, list[tuple[str, ...]]]


def _fresh(base: str, used: set[str]) -> str:
    name = base
    k = 0
    while name in used:
        k += 1
        name = f"{base}{k}"
    used.add(name)
    return name


def _nullable(g: Grammar) -> set[str]:
    null: set[str] = set()
    changed = True
    while changed:
        changed = False
        for a, rhss in g.items():
            if a not in null and any(all(x in null for x in r) for r in rhss):
                null.add(a)
                changed = True
    return null


def _add(g: Grammar, a: str, r: tuple[str, ...]) -> None:
    if r not in g[a]:
        g[a].append(r)


def _clean(g: Grammar, start: str, nts: set[str]) -> Grammar:
    """Remove empty productions, unit productions and useless symbols."""
    null = _nullable(g)
    h: Grammar = {a: [] for a in g}
    for a, rhss in g.items():
        for r in rhss:
            opts = [((x,), ()) if x in null else ((x,),) for x in r]
            for pick in product(*opts):
                nr = tuple(s for part in pick for s in part)
                if nr:
                    _add(h, a, nr)
    # unit pairs (A, B) with A =>* B by unit productions only
    unit: dict[str, set[str]] = {}
    for a in h:
        seen = {a}
        stack = [a]
        while stack:
            b = stack.pop()
            for r in h[b]:
                if len(r) == 1 and r[0] in nts and r[0] not in seen:
                    seen.add(r[0])
                    stack.append(r[0])
        unit[a] = seen
    k: Grammar = {a: [] for a in h}
    for a in h:
        for b in unit[a]:
            for r in h[b]:
                if not (len(r) == 1 and r[0] in nts):
                    _add(k, a, r)
    # generating, then reachable
    gen: set[str] = set()
    changed = True
    while changed:
        changed = False
        for a, rhss in k.items():
            if a not in gen and any(all(x not in nts or x in gen for x in r) for r in rhss):
                gen.add(a)
                changed = True
    k = {a: [r for r in rhss if all(x not in nts or x in gen for x in r)] for a, rhss in k.items() if a in gen}
    if start not in k:
        return {}
    reach = {start}
    stack = [start]
    while stack:
        b = stack.pop()
        for r in k[b]:
            for x in r:
                if x in k and x not in reach:
                    reach.add(x)
                    stack.append(x)
    return {a: k[a] for a in k if a in reach}


def to_gnf(productions: Sequence[Production], start: str) -> tuple[list[Production], str]:
    """Return (gnf_productions, gnf_start) generating the same language."""
    nts = {a for a, _ in productions}
    used = set(nts) | {x for _, r in productions for x in r}
    g: Grammar = {}
    for a, _ in productions:  # nonterminals in order of first appearance
        g.setdefault(a, [])
    for a, r in productions:
        _add(g, a, tuple(r))
    has_empty = start in _nullable(g)                                   # @line L1
    g = _clean(g, start, nts)                                           # @line L2
    term_nt: dict[str, str] = {}
    order: list[str] = list(g)                                          # @line L3
    for a in list(g):                                                   # @line L4
        new = []
        for r in g[a]:
            tail = []
            for x in r[1:]:
                if x not in g:
                    if x not in term_nt:
                        term_nt[x] = _fresh("T_" + x, used)
                        order.append(term_nt[x])
                    x = term_nt[x]
                tail.append(x)
            new.append((r[0],) + tuple(tail))
        g[a] = new
    for x, t in term_nt.items():
        g[t] = [(x,)]
    rank = {a: i for i, a in enumerate(order)}
    extra: list[str] = []
    for i, ai in enumerate(order):                                      # @line L5
        for j in range(i):                                              # @line L6
            aj = order[j]
            new: dict[tuple[str, ...], None] = {}
            for r in g[ai]:
                if r[0] == aj:                                          # @line L7
                    for d in g[aj]:
                        new[d + r[1:]] = None
                else:
                    new[r] = None
            g[ai] = list(new)
        rec = [r[1:] for r in g[ai] if r[0] == ai]                      # @line L8
        if rec:
            rest = [r for r in g[ai] if r[0] != ai]
            b = _fresh(ai + "_rec", used)
            extra.append(b)
            g[ai] = rest + [r + (b,) for r in rest]
            g[b] = rec + [r + (b,) for r in rec]
    for i in range(len(order) - 2, -1, -1):                             # @line L9
        ai = order[i]
        new = {}
        for r in g[ai]:
            if r[0] in rank:                                            # leading A_j with j > i
                for d in g[r[0]]:
                    new[d + r[1:]] = None
            else:
                new[r] = None
        g[ai] = list(new)
    pending = list(extra)                                               # @line L10
    while pending:
        b = pending.pop(0)
        if any(r[0] in g and r[0] in pending for r in g[b]):
            pending.append(b)  # a leading B that is not yet in Greibach form
            continue
        new = {}
        for r in g[b]:
            if r[0] in g:
                for d in g[r[0]]:
                    new[d + r[1:]] = None
            else:
                new[r] = None
        g[b] = list(new)
    out: list[Production] = [(a, r) for a in order + extra for r in g.get(a, [])]
    new_start = start
    if has_empty:                                                       # @line L11
        new_start = _fresh(start + "0", used)
        out = [(new_start, ())] + [(new_start, r) for a, r in out if a == start] + out
    return out, new_start                                               # @line L12


def is_gnf(productions: Sequence[Production], start: str) -> bool:
    """Check the form: A -> a B1 ... Bk, plus start -> () with start on no right side."""
    nts = {a for a, _ in productions}
    for a, r in productions:
        if not r:
            if a != start:
                return False
            continue
        if r[0] in nts or any(x not in nts for x in r[1:]):
            return False
    if any(not r for a, r in productions if a == start):
        if any(start in r for _, r in productions):
            return False
    return True
