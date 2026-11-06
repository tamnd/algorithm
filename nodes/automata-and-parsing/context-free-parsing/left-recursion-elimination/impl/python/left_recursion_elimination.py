# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/left-recursion-elimination/. The authors are listed in prov/KFFADV.jsonl.

"""Paull's algorithm: remove all left recursion from a context-free grammar.

A grammar is a list of productions (A, rhs) with rhs a tuple of symbols. The
nonterminals are the left sides; every other symbol is a terminal. The result
generates the same language and has no derivation A =>+ A beta.
"""

Production = tuple[str, tuple[str, ...]]


def _fresh(name: str, used: set[str]) -> str:
    new = name + "'"
    while new in used:
        new += "'"
    used.add(new)
    return new


def prepare(productions: list[Production], start: str) -> tuple[list[Production], bool]:
    """Make the grammar fit for the main loop: no useless rules, no empty rules, no unit cycles.

    Returns the new productions and whether the empty string is in the language.
    The language changes only by the loss of the empty string.
    """
    nts = {a for a, _ in productions} | {start}

    def productive(ps: list[Production]) -> list[Production]:
        good: set[str] = set()
        changed = True
        while changed:
            changed = False
            for a, rhs in ps:
                if a not in good and all(x in good or x not in nts for x in rhs):
                    good.add(a)
                    changed = True
        return [(a, r) for a, r in ps if a in good and all(x in good or x not in nts for x in r)]

    # 1. keep only productions whose symbols all derive some terminal string
    prods = productive(productions)
    # 2. remove empty productions: add every version with some nullable symbols left out
    null: set[str] = set()
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            if a not in null and all(x in null for x in rhs):
                null.add(a)
                changed = True
    out: list[Production] = []
    seen: set[Production] = set()
    for a, rhs in prods:
        versions: list[tuple[str, ...]] = [()]
        for x in rhs:
            versions = [v + (x,) for v in versions] + (versions if x in null else [])
        for v in versions:
            if v and (a, v) not in seen:
                seen.add((a, v))
                out.append((a, v))
    # a symbol that derived only the empty string now derives nothing
    out = productive(out)
    # 3. merge each cycle of unit productions A -> B -> ... -> A into one nonterminal
    unit = {a: {r[0] for b, r in out if b == a and len(r) == 1 and r[0] in nts} for a in nts}
    reach = {}
    for a in nts:
        seen_a, todo = {a}, [a]
        while todo:
            for b in unit[todo.pop()]:
                if b not in seen_a:
                    seen_a.add(b)
                    todo.append(b)
        reach[a] = seen_a
    order = [start] + [a for a, _ in productions if a != start]
    rep = {}
    for a in order:
        if a not in rep:
            for b in reach[a]:
                if a in reach[b] and b not in rep:
                    rep[b] = a
    merged: list[Production] = []
    seen = set()
    for a, rhs in out:
        p = (rep[a], tuple(rep.get(x, x) for x in rhs))
        if p != (p[0], (p[0],)) and p not in seen:
            seen.add(p)
            merged.append(p)
    return merged, start in null


def eliminate_left_recursion(productions: list[Production], start: str) -> tuple[list[Production], str]:
    """Return (productions, start) of an equivalent grammar without left recursion.

    The nonterminals are processed in the order of their first appearance as a left
    side, with the start symbol first. Cost: O(m * h) time after prepare, where m is
    the number of nonterminals and h the size of the result, which can be exponential
    in the size of the input.
    """
    used = {a for a, _ in productions} | {s for _, r in productions for s in r} | {start}
    prods, has_empty = prepare(productions, start)
    order: list[str] = []
    for a, _ in [(start, ())] + prods:
        if a not in order and any(b == a for b, _ in prods):
            order.append(a)
    rules = {a: [r for b, r in prods if b == a] for a in order}  # @line L1
    result: list[Production] = []
    for i, ai in enumerate(order):  # @line L2
        for aj in order[:i]:  # @line L3
            new: list[tuple[str, ...]] = []
            for rhs in rules[ai]:  # @line L4
                if rhs[0] == aj:
                    new.extend(delta + rhs[1:] for delta in rules[aj])  # @line L5
                else:
                    new.append(rhs)
            rules[ai] = list(dict.fromkeys(new))
        alphas = [r[1:] for r in rules[ai] if r[0] == ai]  # @line L6
        betas = [r for r in rules[ai] if r[0] != ai]
        if alphas:  # @line L7
            prime = _fresh(ai, used)
            rules[ai] = [b + (prime,) for b in betas]  # @line L8
            result.extend((prime, a + (prime,)) for a in alphas)  # @line L9
            result.append((prime, ()))
    final = [(a, r) for a in order for r in rules[a]] + result  # @line L10
    if has_empty:
        s0 = _fresh(start, used)
        top = [(s0, (start,))] if start in rules else []
        return top + [(s0, ())] + final, s0
    return final, start
