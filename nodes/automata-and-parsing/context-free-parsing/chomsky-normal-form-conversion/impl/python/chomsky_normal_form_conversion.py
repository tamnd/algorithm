# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chomsky-normal-form-conversion/. The authors are listed in prov/P1WQJZ.jsonl.
"""Conversion of a context-free grammar into Chomsky normal form.

A grammar is given by a start symbol, a list of productions (A, rhs) where rhs
is a tuple of symbols (the empty tuple is A -> ε), and the set of terminals.
Every symbol that is not a terminal is a nonterminal. The steps run in the
order START, TERM, BIN, DEL, UNIT, USELESS, which keeps the output size
O(|G|^2). All loops are iterative, so large grammars do not hit the
recursion limit.
"""

from collections import defaultdict, deque


def _fresh(base, used):
    """A new symbol name that starts with base and is not in used; it is added to used."""
    name, i = base, 0
    while name in used:
        i += 1
        name = f"{base}{i}"
    used.add(name)
    return name


def nullable_set(productions):
    """The nonterminals that derive ε, by a worklist with one counter per production (linear time)."""
    count = []
    occurs = defaultdict(list)
    queue = deque()
    nullable = set()
    for idx, (a, rhs) in enumerate(productions):
        count.append(len(rhs))
        for x in rhs:
            occurs[x].append(idx)
        if not rhs and a not in nullable:
            nullable.add(a)
            queue.append(a)
    while queue:
        x = queue.popleft()
        for idx in occurs[x]:
            count[idx] -= 1
            a = productions[idx][0]
            if count[idx] == 0 and a not in nullable:
                nullable.add(a)
                queue.append(a)
    return nullable


def _remove_useless(start, productions, terminals):
    """Keep the productions whose symbols all derive terminal strings and are reachable from start."""
    count = []
    occurs = defaultdict(list)
    queue = deque()
    generating = set()
    for idx, (a, rhs) in enumerate(productions):
        pending = {x for x in rhs if x not in terminals}
        count.append(len(pending))
        for x in pending:
            occurs[x].append(idx)
        if not pending and a not in generating:
            generating.add(a)
            queue.append(a)
    while queue:
        x = queue.popleft()
        for idx in occurs[x]:
            count[idx] -= 1
            a = productions[idx][0]
            if count[idx] == 0 and a not in generating:
                generating.add(a)
                queue.append(a)
    kept = [(a, r) for a, r in productions
            if a in generating and all(x in terminals or x in generating for x in r)]
    by_lhs = defaultdict(list)
    for a, r in kept:
        by_lhs[a].append(r)
    reach = {start}
    stack = [start]
    while stack:
        a = stack.pop()
        for r in by_lhs[a]:
            for x in r:
                if x not in terminals and x not in reach:
                    reach.add(x)
                    stack.append(x)
    return [(a, r) for a, r in kept if a in reach]


def to_cnf(start, productions, terminals):
    """Return (new_start, productions) of a grammar in Chomsky normal form with the same language.

    The output has productions A -> B C and A -> a, and new_start -> ε exactly
    when ε is in the language; new_start appears on no right side.
    """
    terminals = set(terminals)
    used = set(terminals) | {start}
    for a, rhs in productions:
        if a in terminals:
            raise ValueError(f"terminal {a!r} on a left side")
        used.add(a)
        used.update(rhs)

    s0 = _fresh(start + "0", used)
    prods = [(s0, (start,))] + [(a, tuple(r)) for a, r in productions]  # @line L1

    term_nt = {}
    after_term = []
    for a, rhs in prods:  # @line L2
        if len(rhs) >= 2:
            new_rhs = []
            for x in rhs:
                if x in terminals:
                    if x not in term_nt:  # @line L3
                        term_nt[x] = _fresh("T_" + x, used)
                    new_rhs.append(term_nt[x])
                else:
                    new_rhs.append(x)
            after_term.append((a, tuple(new_rhs)))
        else:
            after_term.append((a, rhs))
    after_term += [(t, (x,)) for x, t in term_nt.items()]

    binary = []
    for a, rhs in after_term:  # @line L4
        if len(rhs) <= 2:
            binary.append((a, rhs))
            continue
        cur = a
        for i in range(len(rhs) - 2):  # @line L5
            nxt = _fresh(f"{a}_{i + 1}", used)
            binary.append((cur, (rhs[i], nxt)))
            cur = nxt
        binary.append((cur, (rhs[-2], rhs[-1])))
    binary = list(dict.fromkeys(binary))

    nullable = nullable_set(binary)  # @line L6
    no_eps = []
    for a, rhs in binary:
        if len(rhs) == 2:  # @line L7
            x, y = rhs
            no_eps.append((a, rhs))
            if y in nullable:
                no_eps.append((a, (x,)))
            if x in nullable:
                no_eps.append((a, (y,)))
        elif rhs:  # @line L8
            no_eps.append((a, rhs))
    if s0 in nullable:
        no_eps.append((s0, ()))
    no_eps = list(dict.fromkeys(no_eps))

    def is_unit(rhs):
        return len(rhs) == 1 and rhs[0] not in terminals

    unit_succ = defaultdict(list)
    non_unit = defaultdict(list)
    lhs_order = list(dict.fromkeys(a for a, _ in no_eps))
    for a, rhs in no_eps:
        if is_unit(rhs):
            unit_succ[a].append(rhs[0])
        else:
            non_unit[a].append(rhs)
    out = []
    for a in lhs_order:
        reach = [a]  # @line L9
        seen = {a}
        k = 0
        while k < len(reach):
            for b in unit_succ[reach[k]]:
                if b not in seen:
                    seen.add(b)
                    reach.append(b)
            k += 1
        for b in reach:  # @line L10
            for rhs in non_unit[b]:
                out.append((a, rhs))
    out = list(dict.fromkeys(out))

    result = _remove_useless(s0, out, terminals)  # @line L11
    return s0, result  # @line L12


def is_cnf(start, productions, terminals):
    """Check the shape of Chomsky normal form, with start -> ε only and start on no right side."""
    terminals = set(terminals)
    for a, rhs in productions:
        if a in terminals:
            return False
        if len(rhs) == 0:
            if a != start:
                return False
        elif len(rhs) == 1:
            if rhs[0] not in terminals:
                return False
        elif len(rhs) == 2:
            if any(x in terminals or x == start for x in rhs):
                return False
        else:
            return False
    return True


def grammar_size(productions):
    """|G|, the sum of 1 + |rhs| over the productions."""
    return sum(1 + len(rhs) for _, rhs in productions)


if __name__ == "__main__":
    s0, prods = to_cnf("S", [("S", ("a", "S", "b")), ("S", ())], {"a", "b"})
    for a, rhs in prods:
        print(a, "->", " ".join(rhs) or "ε")
