# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unit-production-elimination/. The authors are listed in prov/QDYQHJ.jsonl.

"""Remove the unit productions A -> B (B a nonterminal) from a context-free grammar.

A grammar is a list of productions (A, rhs), where rhs is a tuple of symbols.
The nonterminals are the left sides, the start symbol and the optional set
`nonterminals`; every other symbol is a terminal. The result has no unit
production and generates the same language, for every grammar, including
grammars with empty productions and cycles of unit productions. The search
for unit pairs uses a worklist, without recursion.
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


def is_unit(rhs: tuple[str, ...], nts: set[str]) -> bool:
    return len(rhs) == 1 and rhs[0] in nts


def unit_pairs(productions: Sequence[Production], nts: set[str]) -> dict[str, list[str]]:
    """For each nonterminal A, the nonterminals B with A =>* B by unit productions
    only (A itself first), in the order the search finds them."""
    succ: dict[str, list[str]] = {}
    for a, rhs in productions:
        if is_unit(rhs, nts):
            succ.setdefault(a, []).append(rhs[0])
    pairs: dict[str, list[str]] = {}
    for a in sorted(nts):                                               # @line L2
        found, order, work = {a}, [a], [a]                              # @line L3
        while work:                                                     # @line L4
            b = work.pop()                                              # @line L5
            for c in succ.get(b, ()):
                if c not in found:
                    found.add(c)
                    order.append(c)
                    work.append(c)
        pairs[a] = order
    return pairs


def eliminate_units(
    productions: Sequence[Production], start: str, nonterminals: Optional[Iterable[str]] = None
) -> list[Production]:
    """Return the productions of an equivalent grammar without unit productions.
    The productions of each A are those of P that are not unit, then the copies
    from the nonterminals that A reaches by unit productions, without duplicates."""
    nts = nonterminal_set(productions, start, nonterminals)
    by_lhs: dict[str, list[tuple[str, ...]]] = {}
    for a, rhs in productions:
        if not is_unit(rhs, nts):
            by_lhs.setdefault(a, []).append(rhs)
    out: dict[Production, None] = {}                                    # @line L1
    for a, reach in unit_pairs(productions, nts).items():
        for b in reach:                                                 # @line L6
            for rhs in by_lhs.get(b, ()):
                out[(a, rhs)] = None
    return list(out)                                                    # @line L7
