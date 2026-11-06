# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lalr-parsing/. The authors are listed in prov/2JWXYX.jsonl.

"""LALR(1) parse tables and the shift-reduce driver that uses them.

A grammar is a list of productions (A, rhs), where rhs is a tuple of symbols.
The nonterminals are the left sides; every other symbol is a terminal. The
grammar is augmented with production 0, S' -> start, and the end marker "$".
The LR(0) automaton is built first; the LALR(1) lookahead sets of its kernel
items are then computed by propagation until nothing changes. The grammar
should have no useless symbols; then the LALR(1) automaton is the canonical
LR(1) automaton with its states merged by core. A parse tree is (A, children),
where each child is a tree or a terminal symbol.
"""

from dataclasses import dataclass, field
from typing import Optional, Sequence, Union

Tree = tuple[str, tuple[Union["Tree", str], ...]]
Production = tuple[str, tuple[str, ...]]
Item = tuple[int, int]  # (production index, dot position)
Action = tuple[str, int]  # ("shift", state), ("reduce", production), ("accept", 0)
END = "$"


@dataclass
class LalrTable:
    """The LALR(1) automaton, its lookahead sets and its parse table."""

    productions: list[Production]
    nonterminals: set[str]
    kernels: list[frozenset[Item]]
    goto: dict[tuple[int, str], int]
    lookahead: dict[tuple[int, Item], set[str]]
    action: dict[tuple[int, str], set[Action]] = field(default_factory=dict)

    def conflicts(self) -> list[tuple[int, str, set[Action]]]:
        """The table entries with more than one action."""
        return [(q, a, acts) for (q, a), acts in sorted(self.action.items()) if len(acts) > 1]


def _first_sets(productions: Sequence[Production], nts: set[str]):
    nullable: set[str] = set()
    first: dict[str, set[str]] = {a: set() for a in nts}
    changed = True
    while changed:
        changed = False
        for a, rhs in productions:
            for x in rhs:
                add = first[x] if x in nts else {x}
                if not add <= first[a]:
                    first[a] |= add
                    changed = True
                if x not in nullable:
                    break
            else:
                if a not in nullable:
                    nullable.add(a)
                    changed = True
    return nullable, first


def _first_of(seq: Sequence[str], tail: set[str], nts: set[str], nullable: set[str], first) -> set[str]:
    """FIRST(seq L) for a set L of terminals."""
    out: set[str] = set()
    for x in seq:
        if x not in nts:
            out.add(x)
            return out
        out |= first[x]
        if x not in nullable:
            return out
    return out | tail


def _closure0(kernel: frozenset[Item], prods, by_lhs, nts) -> list[Item]:
    items = list(kernel)
    seen = set(items)
    k = 0
    while k < len(items):
        p, dot = items[k]
        k += 1
        rhs = prods[p][1]
        if dot < len(rhs) and rhs[dot] in nts:
            for q in by_lhs[rhs[dot]]:
                if (q, 0) not in seen:
                    seen.add((q, 0))
                    items.append((q, 0))
    return items


def _closure1(kernel_la: dict[Item, set[str]], prods, by_lhs, nts, nullable, first) -> dict[Item, set[str]]:
    """LR(1) closure where each LR(0) item carries a set of lookaheads."""
    la = {it: set(s) for it, s in kernel_la.items()}
    work = list(la)
    while work:
        p, dot = work.pop()
        rhs = prods[p][1]
        if dot < len(rhs) and rhs[dot] in nts:
            new = _first_of(rhs[dot + 1:], la[(p, dot)], nts, nullable, first)
            for q in by_lhs[rhs[dot]]:
                cur = la.setdefault((q, 0), set())
                if not new <= cur:
                    cur |= new
                    work.append((q, 0))
    return la


def lalr_table(productions: Sequence[Production], start: str) -> LalrTable:
    """Build the LALR(1) table of the grammar augmented with S' -> start."""
    symbols = {a for a, _ in productions} | {x for _, r in productions for x in r}
    if END in symbols:
        raise ValueError("the end marker $ is a grammar symbol")
    aug = start + "'"
    while aug in symbols:
        aug += "'"
    prods: list[Production] = [(aug, (start,))] + [(a, tuple(r)) for a, r in productions]
    nts = {a for a, _ in prods}
    by_lhs: dict[str, list[int]] = {a: [] for a in nts}
    for p, (a, _) in enumerate(prods):
        by_lhs[a].append(p)
    order: list[str] = []
    for a, r in prods:
        for x in (a,) + r:
            if x not in order:
                order.append(x)
    nullable, first = _first_sets(prods, nts)

    # L1: the LR(0) automaton, states numbered in breadth-first order.
    kernels: list[frozenset[Item]] = [frozenset({(0, 0)})]                     # @line L1
    index = {kernels[0]: 0}
    goto: dict[tuple[int, str], int] = {}
    q = 0
    while q < len(kernels):
        moves: dict[str, set[Item]] = {}
        for p, dot in _closure0(kernels[q], prods, by_lhs, nts):
            rhs = prods[p][1]
            if dot < len(rhs):
                moves.setdefault(rhs[dot], set()).add((p, dot + 1))
        for x in sorted(moves, key=order.index):
            k = frozenset(moves[x])
            if k not in index:
                index[k] = len(kernels)
                kernels.append(k)
            goto[(q, x)] = index[k]
        q += 1

    la: dict[tuple[int, Item], set[str]] = {(s, it): set() for s, k in enumerate(kernels) for it in k}
    la[(0, (0, 0))] = {END}                                                     # @line L2
    changed = True
    while changed:                                                              # @line L3
        changed = False
        for s, k in enumerate(kernels):                                         # @line L4
            closed = _closure1({it: la[(s, it)] for it in k}, prods, by_lhs, nts, nullable, first)  # @line L5
            for (p, dot), look in closed.items():                               # @line L6
                rhs = prods[p][1]
                if dot < len(rhs):
                    target = la[(goto[(s, rhs[dot])], (p, dot + 1))]
                    if not look <= target:
                        target |= look
                        changed = True                                          # @line L7

    table = LalrTable(prods, nts, kernels, goto, la)
    for s, k in enumerate(kernels):                                             # @line L8
        closed = _closure1({it: la[(s, it)] for it in k}, prods, by_lhs, nts, nullable, first)
        for (p, dot), look in closed.items():
            rhs = prods[p][1]
            if dot < len(rhs) and rhs[dot] not in nts:                          # @line L9
                table.action.setdefault((s, rhs[dot]), set()).add(("shift", goto[(s, rhs[dot])]))
            elif dot == len(rhs):                                               # @line L10
                for a in look:
                    act = ("accept", 0) if p == 0 else ("reduce", p)
                    table.action.setdefault((s, a), set()).add(act)
    return table


def lalr_parse(table: LalrTable, w: Sequence[str]) -> Optional[Tree]:
    """Run the shift-reduce driver. Return the parse tree, or None if w is rejected.
    Raises ValueError if the table has a conflict."""
    if table.conflicts():                                                       # @line L11
        raise ValueError("the grammar is not LALR(1)")
    prods = table.productions
    stack = [0]                                                                 # @line L12
    values: list[Union[Tree, str]] = []
    pos = 0
    while True:                                                                 # @line L13
        a = w[pos] if pos < len(w) else END
        acts = table.action.get((stack[-1], a))
        if not acts:
            return None                                                         # @line L17
        kind, arg = next(iter(acts))
        if kind == "shift":                                                     # @line L14
            stack.append(arg)
            values.append(a)
            pos += 1
        elif kind == "reduce":                                                  # @line L15
            lhs, rhs = prods[arg]
            m = len(rhs)
            kids = tuple(values[len(values) - m:])
            del stack[len(stack) - m:]
            del values[len(values) - m:]
            stack.append(table.goto[(stack[-1], lhs)])
            values.append((lhs, kids))
        else:                                                                   # @line L16
            tree = values[-1]
            assert not isinstance(tree, str)
            return tree


def lalr_recognize(productions: Sequence[Production], start: str, w: Sequence[str]) -> bool:
    """Build the table and run the driver; raises ValueError if the grammar is not LALR(1)."""
    return lalr_parse(lalr_table(productions, start), w) is not None
