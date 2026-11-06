# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epsilon-production-elimination/. The authors are listed in prov/YT0RZM.jsonl.

"""Remove the empty productions A -> () from a context-free grammar.

A grammar is a list of productions (A, rhs), where rhs is a tuple of symbols.
The nonterminals are the left sides; every other symbol is a terminal. The
result generates the same nonempty strings as the input. With keep_empty=True
and the empty string in the language, a fresh start symbol S' with S' -> S and
S' -> () is added; S' is on no right side. A nonterminal that derives only the
empty string disappears from the result.
"""

from itertools import product
from typing import Sequence

Production = tuple[str, tuple[str, ...]]


def nullable_set(productions: Sequence[Production]) -> set[str]:
    """Nonterminals that derive the empty string, by a worklist in O(|G|) time.

    count[p] is the number of symbols of the right side of production p that are
    not yet known to be nullable; a left side becomes nullable when a count hits 0."""
    nts = {a for a, _ in productions}
    count = [len(rhs) for _, rhs in productions]
    uses: dict[str, list[int]] = {}
    for p, (_, rhs) in enumerate(productions):
        for x in rhs:
            if x in nts:
                uses.setdefault(x, []).append(p)
    nullable: set[str] = set()
    work = [a for p, (a, rhs) in enumerate(productions) if not rhs]
    for a in work:
        nullable.add(a)
    while work:
        x = work.pop()
        for p in uses.get(x, []):
            count[p] -= 1  # one occurrence of x is now known nullable
            a = productions[p][0]
            if count[p] == 0 and a not in nullable:
                nullable.add(a)
                work.append(a)
    return nullable


def eliminate_epsilon(
    productions: Sequence[Production], start: str, keep_empty: bool = True
) -> tuple[list[Production], str]:
    """Return (new_productions, new_start) with no empty production, except
    S' -> () for a fresh start S' when keep_empty is set and start is nullable."""
    nullable = nullable_set(productions)                                # @line L1
    out: dict[Production, None] = {}                                    # @line L2
    for a, rhs in productions:                                          # @line L3
        choices = [((x,), ()) if x in nullable else ((x,),) for x in rhs]
        for pick in product(*choices):                                  # @line L4
            new_rhs = tuple(s for part in pick for s in part)           # @line L5
            if new_rhs:                                                 # @line L6
                out[(a, new_rhs)] = None
    nts = {a for a, _ in productions}
    # A nonterminal of G left without productions (its only productions were
    # empty) derives no string in the result, so a production that mentions it
    # is never used in a derivation of a terminal string. Drop such productions,
    # so that the symbol is not read as a terminal; dropping can leave another
    # nonterminal without productions, so repeat until nothing changes.
    result = list(out)
    while True:
        lhs = {a for a, _ in result}
        kept = [(a, r) for a, r in result if all(x in lhs or x not in nts for x in r)]
        if len(kept) == len(result):
            break
        result = kept
    if keep_empty and start in nullable:                                # @line L7
        symbols = {a for a, _ in productions} | {x for _, r in productions for x in r}
        new_start = start + "'"
        while new_start in symbols:
            new_start += "'"
        head = [(new_start, (start,))] if any(a == start for a, _ in result) else []
        result = head + [(new_start, ())] + result
        return result, new_start
    return result, start                                                # @line L8
