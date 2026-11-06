# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/canonical-lr-parsing/. The authors are listed in prov/12M6QZ.jsonl.

from dataclasses import dataclass, field
from collections.abc import Sequence

END = "$"  # the end marker; it must not be a terminal of the grammar
START = "S'"  # the new start symbol of the augmented grammar

Production = tuple[str, tuple[str, ...]]
Item = tuple[int, int, str]  # (production index, dot position, lookahead)


@dataclass
class LRTables:
    """The canonical LR(1) automaton and its parse tables.

    productions[0] is S' -> S; productions[k] for k >= 1 is the (k-1)-th input production.
    action[(state, terminal)] is ("shift", t), ("reduce", k) or ("accept",).
    goto[(state, nonterminal)] is a state. conflicts lists each entry that got two actions.
    """

    productions: list[Production]
    nonterminals: set[str]
    states: list[frozenset[Item]]
    action: dict[tuple[int, str], tuple] = field(default_factory=dict)
    goto: dict[tuple[int, str], int] = field(default_factory=dict)
    conflicts: list[tuple[tuple[int, str], tuple, tuple]] = field(default_factory=list)


def first_sets(productions: Sequence[Production], nts: set[str]) -> tuple[dict[str, set[str]], set[str]]:
    """FIRST of each nonterminal and the set of nullable nonterminals, by a fixpoint.

    Cost: O(|G| * |V| * |Sigma|) set work in the worst case.
    """
    first: dict[str, set[str]] = {a: set() for a in nts}
    nullable: set[str] = set()
    changed = True
    while changed:
        changed = False
        for a, rhs in productions:
            all_nullable = True
            for x in rhs:
                f = first[x] if x in nts else {x}
                if not f <= first[a]:
                    first[a] |= f
                    changed = True
                if x not in nullable:
                    all_nullable = False
                    break
            if all_nullable and a not in nullable:
                nullable.add(a)
                changed = True
    return first, nullable


def first_of(seq: Sequence[str], la: str, first: dict[str, set[str]], nullable: set[str]) -> set[str]:
    """FIRST(seq la): the terminals that can begin a string derived from seq followed by la."""
    out: set[str] = set()
    for x in seq:
        if x in first:
            out |= first[x]
            if x not in nullable:
                return out
        else:
            out.add(x)
            return out
    out.add(la)
    return out


def closure(items, productions, first, nullable) -> frozenset[Item]:
    """CLOSURE of a set of LR(1) items, with an explicit work list."""
    result = set(items)  # @line L14
    work = list(items)
    while work:  # @line L16
        p, d, la = work.pop()
        rhs = productions[p][1]
        if d < len(rhs) and rhs[d] in first:  # @line L15
            for b in first_of(rhs[d + 1:], la, first, nullable):
                for q, (lhs, _) in enumerate(productions):
                    if lhs == rhs[d] and (q, 0, b) not in result:
                        result.add((q, 0, b))
                        work.append((q, 0, b))
    return frozenset(result)


def goto_set(items, x, productions, first, nullable) -> frozenset[Item]:
    """GOTO(I, X): move the dot over X in each item that allows it, then close."""
    kernel = {(p, d + 1, la) for p, d, la in items
              if d < len(productions[p][1]) and productions[p][1][d] == x}
    return closure(kernel, productions, first, nullable)  # @line L17


def build_tables(start: str, grammar: Sequence[Production]) -> LRTables:
    """Build the canonical LR(1) tables of a context-free grammar.

    grammar is a list of productions (A, (X1, ..., Xk)); the nonterminals are the left
    sides, every other symbol is a terminal. A conflict keeps the first action and is
    listed in tables.conflicts; the grammar is LR(1) when the list is empty (for a
    grammar without useless symbols). Cost: polynomial in the number of item sets,
    which can be exponential in |G|.
    """
    productions: list[Production] = [(START, (start,))] + [(a, tuple(r)) for a, r in grammar]
    nts = {a for a, _ in productions}
    first, nullable = first_sets(productions, nts)
    i0 = closure({(0, 0, END)}, productions, first, nullable)  # @line L1
    t = LRTables(productions, nts, [i0])
    index = {i0: 0}  # @line L2
    trans: dict[tuple[int, str], int] = {}
    i = 0
    while i < len(t.states):  # @line L3
        symbols: list[str] = []
        for p, d, _ in sorted(t.states[i]):
            rhs = productions[p][1]
            if d < len(rhs) and rhs[d] not in symbols:
                symbols.append(rhs[d])
        for x in symbols:  # @line L4
            j = goto_set(t.states[i], x, productions, first, nullable)  # @line L5
            if j not in index:  # @line L6
                index[j] = len(t.states)
                t.states.append(j)
            trans[(i, x)] = index[j]  # @line L7
        i += 1  # @line L8

    def put(key, act):
        if key in t.action and t.action[key] != act:
            if (key, t.action[key], act) not in t.conflicts:
                t.conflicts.append((key, t.action[key], act))
        else:
            t.action[key] = act

    for s, items in enumerate(t.states):  # @line L9
        for p, d, la in sorted(items):
            lhs, rhs = productions[p]
            if d < len(rhs) and rhs[d] not in nts:  # @line L10
                put((s, rhs[d]), ("shift", trans[(s, rhs[d])]))
            elif d == len(rhs) and p != 0:  # @line L11
                put((s, la), ("reduce", p))
            elif d == len(rhs):  # @line L12
                put((s, END), ("accept",))
    t.goto = {(s, x): v for (s, x), v in trans.items() if x in nts}  # @line L13
    return t


def parse(t: LRTables, tokens: Sequence[str]) -> list[int] | None:
    """Run the LR driver on tokens. Return the list of reductions (indices into the
    input grammar, from 0) in the order made, which is a rightmost derivation in
    reverse, or None when the input is rejected. Cost: O(n) steps for an LR(1) grammar.
    """
    toks = list(tokens) + [END]
    stack = [0]  # @line L18
    pos = 0
    out: list[int] = []
    while True:  # @line L19
        s = stack[-1]  # @line L20
        act = t.action.get((s, toks[pos]))
        if act is None:  # @line L24
            return None
        if act[0] == "shift":  # @line L21
            stack.append(act[1])
            pos += 1
        elif act[0] == "reduce":  # @line L22
            lhs, rhs = t.productions[act[1]]
            if rhs:
                del stack[-len(rhs):]
            stack.append(t.goto[(stack[-1], lhs)])
            out.append(act[1] - 1)
        else:  # @line L23
            return out
