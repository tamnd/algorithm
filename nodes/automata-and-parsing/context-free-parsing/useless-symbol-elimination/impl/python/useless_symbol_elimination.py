# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/useless-symbol-elimination/. The authors are listed in prov/09FBBP.jsonl.

"""Remove the useless symbols of a context-free grammar.

A grammar is a list of productions (A, rhs), where rhs is a tuple of symbols.
The nonterminals are the left sides, the start symbol and the optional set
`nonterminals` (which lets a nonterminal have no production at all); every
other symbol is a terminal. A nonterminal is generating if it derives some
terminal string, and reachable if it occurs in some sentential form derived
from the start symbol. The result keeps exactly the productions whose symbols
are all generating and reachable, in their input order, and generates the same
language. Everything runs in O(|G|) time with worklists, without recursion.
"""

from typing import Iterable, Optional, Sequence

Production = tuple[str, tuple[str, ...]]


def nonterminal_set(
    productions: Sequence[Production], start: str, nonterminals: Optional[Iterable[str]] = None
) -> set[str]:
    nts = {a for a, _ in productions}
    nts.add(start)
    if nonterminals is not None:
        nts.update(nonterminals)
    return nts


def generating_set(productions: Sequence[Production], nts: set[str]) -> set[str]:
    """Nonterminals that derive a terminal string. count[p] is the number of
    nonterminal occurrences in the right side of p not yet known generating."""
    count = [0] * len(productions)                                       # @line L1
    uses: dict[str, list[int]] = {}
    for p, (_, rhs) in enumerate(productions):
        for x in rhs:
            if x in nts:
                count[p] += 1
                uses.setdefault(x, []).append(p)
    gen: set[str] = set()                                                # @line L2
    work = [a for p, (a, _) in enumerate(productions) if count[p] == 0]
    while work:                                                          # @line L3
        x = work.pop()                                                   # @line L4
        if x in gen:
            continue
        gen.add(x)                                                       # @line L5
        for p in uses.get(x, ()):                                        # @line L6
            count[p] -= 1
            if count[p] == 0:
                work.append(productions[p][0])
    return gen


def reachable_set(productions: Sequence[Production], start: str, nts: set[str]) -> set[str]:
    """Nonterminals reachable from start through the given productions."""
    by_lhs: dict[str, list[tuple[str, ...]]] = {}
    for a, rhs in productions:
        by_lhs.setdefault(a, []).append(rhs)
    reach = {start}                                                      # @line L8
    work = [start]
    while work:                                                          # @line L9
        a = work.pop()
        for rhs in by_lhs.get(a, ()):                                    # @line L10
            for x in rhs:
                if x in nts and x not in reach:
                    reach.add(x)
                    work.append(x)
    return reach


def eliminate_useless(
    productions: Sequence[Production], start: str, nonterminals: Optional[Iterable[str]] = None
) -> list[Production]:
    """Return the productions of the trimmed grammar, in input order.
    The list is empty exactly when the language of the grammar is empty."""
    nts = nonterminal_set(productions, start, nonterminals)
    gen = generating_set(productions, nts)
    p1 = [                                                               # @line L7
        (a, rhs)
        for a, rhs in productions
        if a in gen and all(x not in nts or x in gen for x in rhs)
    ]
    reach = reachable_set(p1, start, nts)
    return [(a, rhs) for a, rhs in p1 if a in reach]                     # @line L11
