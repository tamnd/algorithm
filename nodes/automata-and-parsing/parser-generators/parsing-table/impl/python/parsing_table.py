# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parsing-table/. The authors are listed in prov/JQ131J.jsonl.

"""A parsing table: a dense grid of cells indexed by (row, column) that records conflicts.

The same structure holds an LR table (rows are automaton states, columns are the
terminals, the end marker and the nonterminals) and an LL(1) table (rows are the
nonterminals, columns are the terminals and the end marker). A cell holds the
actions added to it, in the order they were added; a cell with two different
actions is a conflict.

Actions are tuples:
  ("shift", q), ("reduce", p), ("goto", q), ("accept",) for LR tables,
  ("predict", p) for LL tables, where p is a production index.

A grammar is a list of productions (A, rhs) with rhs a tuple of symbols; the left
sides are the nonterminals, every other symbol is a terminal, and the first
production's left side is the start symbol.
"""

from collections.abc import Callable, Hashable, Sequence

END = "$"
Action = tuple
Production = tuple[str, tuple[str, ...]]


class ParsingTable:
    """Rows of cells over a fixed list of column symbols, with conflict tracking."""

    def __init__(self, columns: Sequence[Hashable], rows: int = 0) -> None:
        self.columns = list(columns)
        self.index = {c: i for i, c in enumerate(self.columns)}
        if len(self.index) != len(self.columns):
            raise ValueError("column symbols must be distinct")
        self.cells: list[list[tuple[Action, ...]]] = []
        self.conflicting: set[tuple[int, int]] = set()
        for _ in range(rows):
            self.add_row()

    def add_row(self) -> int:
        """Append an empty row and return its number."""
        self.cells.append([() for _ in self.columns])
        return len(self.cells) - 1

    @property
    def rows(self) -> int:
        return len(self.cells)

    def add(self, row: int, column: Hashable, action: Action) -> None:
        """Put action into the cell; a second, different action makes the cell a conflict."""
        c = self.index[column]
        cell = self.cells[row][c]
        if not cell:  # @line L1
            self.cells[row][c] = (action,)
        elif action not in cell:  # @line L2
            self.cells[row][c] = cell + (action,)
            self.conflicting.add((row, c))

    def lookup(self, row: int, column: Hashable) -> tuple[Action, ...]:
        """The actions of the cell, in insertion order; () means error."""
        c = self.index.get(column)
        if c is None or not 0 <= row < len(self.cells):
            return ()
        return self.cells[row][c]  # @line L3

    def conflicts(self) -> list[tuple[int, Hashable, tuple[Action, ...]]]:
        """The conflicting cells as (row, column symbol, actions), sorted by position."""
        return [(r, self.columns[c], self.cells[r][c]) for r, c in sorted(self.conflicting)]

    def resolve(self, choose: Callable[[int, Hashable, tuple[Action, ...]], Action | None]) -> None:
        """Replace each conflicting cell by the single action choose returns (None empties it)."""
        for r, c in sorted(self.conflicting):  # @line L4
            pick = choose(r, self.columns[c], self.cells[r][c])
            self.cells[r][c] = () if pick is None else (pick,)  # @line L5
        self.conflicting.clear()  # @line L6

    def entries(self) -> int:
        """The number of (cell, action) pairs stored."""
        return sum(len(cell) for row in self.cells for cell in row)


def _symbols(grammar: Sequence[Production]) -> tuple[list[str], list[str]]:
    nts: list[str] = []
    for a, _ in grammar:
        if a not in nts:
            nts.append(a)
    terms: list[str] = []
    for _, rhs in grammar:
        for x in rhs:
            if x not in nts and x not in terms:
                terms.append(x)
    return nts, terms


def first_follow(grammar: Sequence[Production]) -> tuple[set[str], dict[str, set[str]], dict[str, set[str]]]:
    """Nullable nonterminals, FIRST and FOLLOW sets, by iteration to a fixed point."""
    nts, _ = _symbols(grammar)
    ntset = set(nts)
    nullable: set[str] = set()
    first: dict[str, set[str]] = {a: set() for a in nts}
    changed = True
    while changed:
        changed = False
        for a, rhs in grammar:
            if a not in nullable and all(x in nullable for x in rhs):
                nullable.add(a)
                changed = True
            for x in rhs:
                add = first[x] if x in ntset else {x}
                if not add <= first[a]:
                    first[a] |= add
                    changed = True
                if x not in nullable:
                    break
    follow: dict[str, set[str]] = {a: set() for a in nts}
    follow[nts[0]].add(END)
    changed = True
    while changed:
        changed = False
        for a, rhs in grammar:
            for i, x in enumerate(rhs):
                if x not in ntset:
                    continue
                add: set[str] = set()
                rest_nullable = True
                for y in rhs[i + 1:]:
                    add |= first[y] if y in ntset else {y}
                    if y not in nullable:
                        rest_nullable = False
                        break
                if rest_nullable:
                    add |= follow[a]
                if not add <= follow[x]:
                    follow[x] |= add
                    changed = True
    return nullable, first, follow


def ll1_table(grammar: Sequence[Production]) -> ParsingTable:
    """The LL(1) table: row i is the i-th nonterminal; conflicts are recorded, not resolved."""
    nts, terms = _symbols(grammar)
    ntset = set(nts)
    nullable, first, follow = first_follow(grammar)
    table = ParsingTable(terms + [END], rows=len(nts))
    row = {a: i for i, a in enumerate(nts)}
    for p, (a, rhs) in enumerate(grammar):
        predict: set[str] = set()
        all_nullable = True
        for x in rhs:
            predict |= first[x] if x in ntset else {x}
            if x not in nullable:
                all_nullable = False
                break
        if all_nullable:
            predict |= follow[a]
        for t in sorted(predict):
            table.add(row[a], t, ("predict", p))
    return table


def slr_table(grammar: Sequence[Production]) -> tuple[ParsingTable, list[Production]]:
    """The SLR(1) table over the LR(0) automaton of the augmented grammar.

    Returns the table and the augmented production list, whose production 0 is
    S' -> S. Columns are the terminals, the end marker and the nonterminals.
    """
    nts, terms = _symbols(grammar)
    start = nts[0]
    aug_name = start + "'"
    while aug_name in nts or aug_name in terms:
        aug_name += "'"
    prods: list[Production] = [(aug_name, (start,))] + list(grammar)
    ntset = set(nts) | {aug_name}
    _, _, follow = first_follow(prods)
    order: list[str] = []
    for _, rhs in prods:
        for x in rhs:
            if x not in order:
                order.append(x)

    def closure(items: frozenset[tuple[int, int]]) -> frozenset[tuple[int, int]]:
        out = set(items)
        todo = list(items)
        while todo:
            p, d = todo.pop()
            rhs = prods[p][1]
            if d < len(rhs) and rhs[d] in ntset:
                for j, (b, _) in enumerate(prods):
                    if b == rhs[d] and (j, 0) not in out:
                        out.add((j, 0))
                        todo.append((j, 0))
        return frozenset(out)

    table = ParsingTable(terms + [END] + nts)
    kernels = [frozenset({(0, 0)})]
    number = {kernels[0]: 0}
    table.add_row()
    q = 0
    while q < len(kernels):
        items = closure(kernels[q])
        for x in order:
            nxt = frozenset((p, d + 1) for p, d in items if d < len(prods[p][1]) and prods[p][1][d] == x)
            if not nxt:
                continue
            if nxt not in number:
                number[nxt] = len(kernels)
                kernels.append(nxt)
                table.add_row()
            target = number[nxt]
            table.add(q, x, ("goto", target) if x in ntset else ("shift", target))
        for p, d in sorted(items):
            if d == len(prods[p][1]):
                if p == 0:
                    table.add(q, END, ("accept",))
                else:
                    for t in sorted(follow[prods[p][0]]):
                        table.add(q, t, ("reduce", p))
        q += 1
    return table, prods


class StepLimit(Exception):
    """The driver ran more steps than allowed (possible only after conflicts were resolved)."""


def _single(actions: tuple[Action, ...]) -> Action | None:
    if not actions:
        return None
    if len(actions) > 1:
        raise ValueError("the table still has a conflict in this cell; resolve it first")
    return actions[0]


def lr_parse(table: ParsingTable, prods: Sequence[Production], tokens: Sequence[str],
             max_steps: int | None = None) -> bool:
    """Run the LR driver on tokens; True when the table accepts them."""
    stack = [0]  # @line L7
    toks = list(tokens) + [END]
    i = 0
    steps = 0
    while True:
        steps += 1
        if max_steps is not None and steps > max_steps:
            raise StepLimit(f"more than {max_steps} steps")
        act = _single(table.lookup(stack[-1], toks[i]))  # @line L8
        if act is None:
            return False
        if act[0] == "shift":  # @line L9
            stack.append(act[1])
            i += 1
        elif act[0] == "reduce":  # @line L10
            a, rhs = prods[act[1]]
            if rhs:
                del stack[-len(rhs):]
            go = _single(table.lookup(stack[-1], a))
            if go is None:
                return False
            stack.append(go[1])
        else:  # @line L11
            return True


def ll_parse(table: ParsingTable, grammar: Sequence[Production], tokens: Sequence[str],
             max_steps: int | None = None) -> bool:
    """Run the LL(1) driver on tokens; True when the table accepts them."""
    nts, _ = _symbols(grammar)
    row = {a: i for i, a in enumerate(nts)}
    stack = [END, nts[0]]
    toks = list(tokens) + [END]
    i = 0
    steps = 0
    while True:
        steps += 1
        if max_steps is not None and steps > max_steps:
            raise StepLimit(f"more than {max_steps} steps")
        top = stack.pop()
        if top in row:
            act = _single(table.lookup(row[top], toks[i]))
            if act is None:
                return False
            stack.extend(reversed(grammar[act[1]][1]))
        elif top == toks[i]:
            if top == END:
                return True
            i += 1
        else:
            return False
