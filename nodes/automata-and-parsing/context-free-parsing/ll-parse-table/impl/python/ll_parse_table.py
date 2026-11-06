# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ll-parse-table/. The authors are listed in prov/3BZN2A.jsonl.

"""The LL(1) parse table of a context-free grammar.

A grammar is a list of productions (A, rhs), where A is a nonterminal and rhs is a
tuple of symbols. The nonterminals are the left sides; every other symbol is a
terminal. The end marker is END and must not occur in the grammar.
"""

END = "$"

Production = tuple[str, tuple[str, ...]]


def nullable_set(productions: list[Production]) -> set[str]:
    """The nonterminals that derive the empty string. O(|V| |G|) time."""
    null: set[str] = set()
    changed = True
    while changed:
        changed = False
        for a, rhs in productions:
            if a not in null and all(x in null for x in rhs):
                null.add(a)
                changed = True
    return null


def first_sets(productions: list[Production], null: set[str]) -> dict[str, set[str]]:
    """FIRST(A) for each nonterminal A: the terminals that begin a string derived from A."""
    nts = {a for a, _ in productions}
    first: dict[str, set[str]] = {a: set() for a in nts}
    changed = True
    while changed:
        changed = False
        for a, rhs in productions:
            new = first_of(rhs, first, null) - first[a]
            if new:
                first[a] |= new
                changed = True
    return first


def first_of(alpha: tuple[str, ...], first: dict[str, set[str]], null: set[str]) -> set[str]:
    """FIRST(alpha) for a string alpha of grammar symbols (without the empty string)."""
    out: set[str] = set()
    for x in alpha:
        if x not in first:  # a terminal
            out.add(x)
            return out
        out |= first[x]
        if x not in null:
            return out
    return out


def follow_sets(productions: list[Production], start: str, null: set[str],
                first: dict[str, set[str]]) -> dict[str, set[str]]:
    """FOLLOW(A) for each nonterminal A, with END in FOLLOW(start)."""
    follow: dict[str, set[str]] = {a: set() for a in first}
    follow[start].add(END)
    changed = True
    while changed:
        changed = False
        for a, rhs in productions:
            for i, x in enumerate(rhs):
                if x not in first:
                    continue
                rest = rhs[i + 1:]
                add = first_of(rest, first, null)
                if all(y in null for y in rest):
                    add = add | follow[a]
                if not add <= follow[x]:
                    follow[x] |= add
                    changed = True
    return follow


class LLParseTable:
    """M[A, a] = the productions to apply when A is on top of the stack and a is the next token.

    Build: O(|V| s^2 |G|) time with s = |Sigma| + 1, by plain fixed-point passes, and
    O(|V| s) cells of space. lookup: O(1) expected time (one hash lookup).
    """

    def __init__(self, productions: list[Production], start: str) -> None:
        self.productions = list(productions)
        self.start = start
        self.nonterminals = {a for a, _ in productions}
        if start not in self.nonterminals:
            raise ValueError("the start symbol has no production")
        self.terminals = {x for _, rhs in productions for x in rhs if x not in self.nonterminals}
        if END in self.terminals or END in self.nonterminals:
            raise ValueError("the end marker must not occur in the grammar")
        self.null = nullable_set(productions)  # @line L1
        self.first = first_sets(productions, self.null)
        self.follow = follow_sets(productions, start, self.null, self.first)
        self.cells: dict[tuple[str, str], list[int]] = {}  # @line L2
        for p, (a, rhs) in enumerate(productions):  # @line L3
            for t in sorted(first_of(rhs, self.first, self.null)):  # @line L4
                self._add(a, t, p)
            if all(x in self.null for x in rhs):  # @line L5
                for t in sorted(self.follow[a]):  # @line L6
                    self._add(a, t, p)

    def _add(self, a: str, t: str, p: int) -> None:
        cell = self.cells.setdefault((a, t), [])
        if p not in cell:
            cell.append(p)

    def entries(self, a: str, t: str) -> tuple[int, ...]:
        """All production indices in the cell M[a, t]."""
        return tuple(self.cells.get((a, t), ()))

    def lookup(self, a: str, t: str) -> int | None:
        """The production for nonterminal a and token t, or None for an error entry.

        Raises ValueError when the cell holds two or more productions (a conflict)."""
        cell = self.cells.get((a, t))  # @line L7
        if not cell:  # @line L8
            return None
        if len(cell) > 1:  # @line L9
            raise ValueError(f"LL(1) conflict at M[{a}, {t}]: productions {cell}")
        return cell[0]  # @line L10

    def conflicts(self) -> list[tuple[str, str]]:
        """The cells with two or more productions, in sorted order."""
        return sorted(k for k, v in self.cells.items() if len(v) > 1)

    def is_ll1(self) -> bool:
        return not self.conflicts()

    def check_invariant(self) -> None:
        """Each cell (A, t) holds exactly the productions A -> alpha with t in PREDICT(A -> alpha)."""
        for (a, t), cell in self.cells.items():
            assert a in self.nonterminals and (t in self.terminals or t == END)
            for p in cell:
                lhs, rhs = self.productions[p]
                assert lhs == a
                nul = all(x in self.null for x in rhs)
                assert t in first_of(rhs, self.first, self.null) or (nul and t in self.follow[a])
