# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yacc/. The authors are listed in prov/NSTRHE.jsonl.

"""The algorithm of a yacc-style parser generator, and the parser it produces.

Yacc(productions, precedence) builds an LALR(1) table from the LR(0) automaton by
lookahead propagation, resolves its conflicts with operator precedence and the
default rules (shift over reduce, earlier rule over later rule), and keeps a
report of the conflicts that the default rules settled. Yacc.parse runs the
table on a token list, computes semantic values with the actions of the
productions, and recovers from syntax errors with the special token "error".

A production is (lhs, rhs) or (lhs, rhs, action) or (lhs, rhs, action, prec),
where rhs is a tuple of symbols, action maps the list of right-side values to
the value of the left side (default: the first value, or None for an empty
right side), and prec names a terminal whose precedence the rule takes, as
%prec does. The left sides are the nonterminals; every other symbol is a
terminal. The first production's left side is the start symbol.

precedence is a list of (associativity, terminals) from lowest to highest, with
associativity "left", "right" or "nonassoc", like %left, %right and %nonassoc
lines in the order they are written.
"""

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Any

END = "$"
ERROR = "error"
_HASH = object()  # the dummy lookahead of the propagation method


@dataclass
class Production:
    lhs: str
    rhs: tuple[str, ...]
    action: Callable[[list[Any]], Any] | None = None
    prec: str | None = None


@dataclass
class Conflict:
    state: int
    token: str
    kind: str  # "shift/reduce" or "reduce/reduce"
    chosen: tuple
    discarded: tuple


@dataclass
class ParseResult:
    accepted: bool
    value: Any = None
    errors: list[int] = field(default_factory=list)  # token positions of reported errors


class Yacc:
    """An LALR(1) parser built the way yacc builds it."""

    def __init__(self, productions: Sequence[tuple], precedence: Sequence[tuple[str, Sequence[str]]] = ()) -> None:
        user = [Production(*p) for p in productions]
        self.nonterminals: list[str] = []
        for p in user:
            if p.lhs not in self.nonterminals:
                self.nonterminals.append(p.lhs)
        self.terminals: list[str] = []
        for p in user:
            for x in p.rhs:
                if x not in self.nonterminals and x not in self.terminals:
                    self.terminals.append(x)
        start = self.nonterminals[0]
        aug = start + "'"
        while aug in self.nonterminals or aug in self.terminals:
            aug += "'"
        self.prods = [Production(aug, (start,))] + user
        self.nts = set(self.nonterminals) | {aug}
        self.level: dict[str, tuple[int, str]] = {}
        for i, (assoc, toks) in enumerate(precedence):
            for t in toks:
                self.level[t] = (i + 1, assoc)
        self._first_sets()
        self._build()

    # ------------------------------------------------------------ grammar analysis

    def _first_sets(self) -> None:
        self.nullable: set[str] = set()
        self.first: dict[str, set[str]] = {a: set() for a in self.nts}
        changed = True
        while changed:
            changed = False
            for p in self.prods:
                if p.lhs not in self.nullable and all(x in self.nullable for x in p.rhs):
                    self.nullable.add(p.lhs)
                    changed = True
                for x in p.rhs:
                    add = self.first[x] if x in self.nts else {x}
                    if not add <= self.first[p.lhs]:
                        self.first[p.lhs] |= add
                        changed = True
                    if x not in self.nullable:
                        break

    def _first_seq(self, seq: Sequence[str]) -> tuple[set[str], bool]:
        out: set[str] = set()
        for x in seq:
            if x in self.nts:
                out |= self.first[x]
                if x not in self.nullable:
                    return out, False
            else:
                out.add(x)
                return out, False
        return out, True

    def _closure_la(self, kernel: dict[tuple[int, int], set]) -> dict[tuple[int, int], set]:
        """LR(1) closure where each item carries a set of lookaheads."""
        items = {it: set(la) for it, la in kernel.items()}
        todo = list(items)
        while todo:
            p, d = todo.pop()
            rhs = self.prods[p].rhs
            if d >= len(rhs) or rhs[d] not in self.nts:
                continue
            first, rest_nullable = self._first_seq(rhs[d + 1:])
            la = first | items[(p, d)] if rest_nullable else first
            for q, prod in enumerate(self.prods):
                if prod.lhs == rhs[d]:
                    cur = items.setdefault((q, 0), set())
                    if not la <= cur:
                        cur |= la
                        todo.append((q, 0))
        return items

    def _lr0_closure(self, kernel: frozenset) -> list[tuple[int, int]]:
        out = set(kernel)
        todo = list(kernel)
        while todo:
            p, d = todo.pop()
            rhs = self.prods[p].rhs
            if d < len(rhs) and rhs[d] in self.nts:
                for q, prod in enumerate(self.prods):
                    if prod.lhs == rhs[d] and (q, 0) not in out:
                        out.add((q, 0))
                        todo.append((q, 0))
        return sorted(out)

    # ------------------------------------------------------------ table construction

    def _build(self) -> None:
        order = []
        for p in self.prods:
            for x in p.rhs:
                if x not in order:
                    order.append(x)
        # L1: the LR(0) automaton, states numbered in breadth-first order
        self.kernels: list[frozenset] = [frozenset({(0, 0)})]  # @line L1
        number = {self.kernels[0]: 0}
        self.goto: dict[tuple[int, str], int] = {}
        q = 0
        while q < len(self.kernels):
            items = self._lr0_closure(self.kernels[q])
            for x in order:
                nxt = frozenset((p, d + 1) for p, d in items
                                if d < len(self.prods[p].rhs) and self.prods[p].rhs[d] == x)
                if nxt:
                    if nxt not in number:
                        number[nxt] = len(self.kernels)
                        self.kernels.append(nxt)
                    self.goto[(q, x)] = number[nxt]
            q += 1
        # L2: spontaneous lookaheads and propagation links
        la: dict[tuple[int, tuple[int, int]], set[str]] = {
            (s, it): set() for s, k in enumerate(self.kernels) for it in k}
        la[(0, (0, 0))].add(END)
        links: dict[tuple[int, tuple[int, int]], list] = {key: [] for key in la}
        for s, kernel in enumerate(self.kernels):
            for it in kernel:
                closed = self._closure_la({it: {_HASH}})  # @line L2
                for (p, d), las in closed.items():
                    rhs = self.prods[p].rhs
                    if d == len(rhs):
                        continue
                    target = (self.goto[(s, rhs[d])], (p, d + 1))
                    for a in las:
                        if a is _HASH:
                            links[(s, it)].append(target)
                        else:
                            la[target].add(a)
        # L3: propagate until no lookahead set changes
        todo = [key for key in la if la[key]]
        while todo:
            key = todo.pop()
            for target in links[key]:  # @line L3
                if not la[key] <= la[target]:
                    la[target] |= la[key]
                    todo.append(target)
        self.kernel_lookaheads = la
        # L4: fill the cells; accept is kept as a reduction by production 0
        cells: dict[tuple[int, str], list] = {}
        for (s, x), t in self.goto.items():
            if x not in self.nts:
                cells.setdefault((s, x), []).append(("shift", t))  # @line L4
        for s, kernel in enumerate(self.kernels):
            closed = self._closure_la({it: la[(s, it)] for it in kernel})
            for (p, d), las in closed.items():
                if d == len(self.prods[p].rhs):
                    for a in las:
                        cells.setdefault((s, a), []).append(("reduce", p))
        self.raw = {k: tuple(sorted(v, key=_order)) for k, v in cells.items()}
        self.action: dict[tuple[int, str], tuple] = {}
        self.conflicts: list[Conflict] = []
        self.resolved_by_precedence = 0
        for key in sorted(self.raw, key=lambda k: (k[0], str(k[1]))):
            acts = self.raw[key]
            chosen = self._resolve(key, acts) if len(acts) > 1 else acts[0]
            if chosen is not None:
                if chosen == ("reduce", 0):
                    chosen = ("accept",)
                self.action[key] = chosen
        # a state whose only action is one reduction reduces without reading the lookahead
        rows: dict[int, set] = {}
        for (st, _), act in self.action.items():
            rows.setdefault(st, set()).add(act)
        self.default = {st: next(iter(acts)) for st, acts in rows.items()
                        if len(acts) == 1 and next(iter(acts))[0] == "reduce"}

    def rule_prec(self, p: int) -> tuple[int, str] | None:
        """The precedence of production p: from its %prec token, else from its last terminal."""
        prod = self.prods[p]
        if prod.prec is not None:
            return self.level.get(prod.prec)
        for x in reversed(prod.rhs):
            if x not in self.nts:
                return self.level.get(x)
        return None

    def _resolve(self, key: tuple[int, str], acts: tuple) -> tuple | None:
        state, token = key
        shift = next((a for a in acts if a[0] == "shift"), None)
        reduces = [a for a in acts if a[0] == "reduce"]
        tok = self.level.get(token)
        kept = []
        for r in reduces:  # @line L5
            rp = self.rule_prec(r[1])
            if shift is None or tok is None or rp is None:
                kept.append(r)
            elif tok[0] > rp[0]:
                pass  # the token binds tighter: shift
            elif tok[0] < rp[0] or tok[1] == "left":
                shift = None
                kept.append(r)
            elif tok[1] == "right":
                pass
            else:  # nonassoc: neither, the cell becomes an error
                shift = None
        if len(kept) + (shift is not None) < len(acts):
            self.resolved_by_precedence += 1
        if shift is not None and kept:  # @line L6
            self.conflicts.append(Conflict(state, token, "shift/reduce", shift, tuple(kept)))
            return shift
        if len(kept) > 1:  # @line L7
            self.conflicts.append(Conflict(state, token, "reduce/reduce", kept[0], tuple(kept[1:])))
            return kept[0]
        if kept:
            return kept[0]
        return shift  # None when %nonassoc made the cell an error

    # ------------------------------------------------------------ the parser

    def parse(self, tokens: Sequence[tuple[str, Any] | str], max_steps: int = 1_000_000) -> ParseResult:
        """Run the parser. Tokens are kinds or (kind, value) pairs; END is appended."""
        toks = [(t, t) if isinstance(t, str) else (t[0], t[1]) for t in tokens] + [(END, None)]
        states = [0]
        values: list[Any] = [None]
        i = 0
        quiet = 0  # tokens still to shift before errors are reported again
        result = ParseResult(False)
        for _ in range(max_steps):
            kind, val = toks[i]
            act = self.default.get(states[-1]) or self.action.get((states[-1], kind))  # @line L8
            if act is None:
                # L12: error recovery with the error token
                if quiet == 0:
                    result.errors.append(i)  # @line L12
                elif quiet == 3:
                    if kind == END:
                        return result
                    i += 1  # discard the token that could not follow the error token
                quiet = 3
                while (states[-1], ERROR) not in self.action or self.action[(states[-1], ERROR)][0] != "shift":
                    if len(states) == 1:
                        return result
                    states.pop()
                    values.pop()
                states.append(self.action[(states[-1], ERROR)][1])
                values.append(None)
                continue
            if act[0] == "shift":  # @line L9
                states.append(act[1])
                values.append(val)
                i += 1
                if quiet:
                    quiet -= 1
            elif act[0] == "reduce":  # @line L10
                prod = self.prods[act[1]]
                k = len(prod.rhs)
                args = values[len(values) - k:] if k else []
                if k:
                    del states[-k:]
                    del values[-k:]
                if prod.action is not None:
                    value = prod.action(args)
                else:
                    value = args[0] if args else None
                states.append(self.goto[(states[-1], prod.lhs)])
                values.append(value)
            else:  # @line L11
                result.accepted = True
                result.value = values[-1]
                return result
        raise RuntimeError("step limit exceeded")


def _order(a: tuple) -> tuple:
    return (0, a[1]) if a[0] == "shift" else (1, a[1])
