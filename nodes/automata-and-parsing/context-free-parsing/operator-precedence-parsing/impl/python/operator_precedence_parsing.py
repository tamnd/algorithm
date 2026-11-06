# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/operator-precedence-parsing/. The authors are listed in prov/G04W13.jsonl.

"""Floyd's operator-precedence parser.

A grammar is a list of productions (A, rhs) with rhs a tuple of symbols. The
nonterminals are the left sides; every other symbol is a terminal. The grammar
must be an operator grammar: no empty right side and no two adjacent
nonterminals. The end marker "$" must not be a symbol of the grammar.

The parser finds each handle with the relations <, =, > between terminals.
Each nonterminal slot on its stack holds every nonterminal that can label that
part of the tree, with one parse tree for each, so unit productions and
productions with the same terminals are handled exactly.
"""

END = "$"

Production = tuple[str, tuple[str, ...]]
Tree = tuple[str, list] | str


class ParseError(Exception):
    """Syntax error; position is the 0-indexed token (len(tokens) for the end)."""

    def __init__(self, position: int, message: str) -> None:
        super().__init__(f"{message} at token {position}")
        self.position = position


class PrecedenceTable:
    """The precedence relations of an operator precedence grammar."""

    def __init__(self, start, nts, rel, by_shape, units):
        self.start = start
        self.nts = nts
        self.rel = rel  # (a, b) -> "<", "=" or ">"
        self.by_shape = by_shape  # shape -> productions with that shape
        self.units = units  # B -> the A with a production A -> B


def _productive(productions: list[Production]) -> list[Production]:
    nts = {a for a, _ in productions}
    good: set[str] = set()
    changed = True
    while changed:
        changed = False
        for a, rhs in productions:
            if a not in good and all(x in good or x not in nts for x in rhs):
                good.add(a)
                changed = True
    return [(a, r) for a, r in productions
            if a in good and all(x in good or x not in nts for x in r)]


def _shape(rhs, nts):
    """The right side with every nonterminal replaced by None."""
    return tuple(None if x in nts else x for x in rhs)


def build_precedence(productions: list[Production], start: str) -> PrecedenceTable:
    """Compute LEADING, TRAILING and the precedence relations.

    Raises ValueError if the grammar is not an operator grammar or if two
    relations hold between some pair of terminals.
    """
    nts = {a for a, _ in productions}
    for a, rhs in productions:
        if END in rhs or a == END:
            raise ValueError("the end marker is a grammar symbol")
        if not rhs:
            raise ValueError(f"empty production for {a}")
        for x, y in zip(rhs, rhs[1:]):
            if x in nts and y in nts:
                raise ValueError(f"adjacent nonterminals in {a} -> {' '.join(rhs)}")
    prods = _productive(productions)
    nts = {a for a, _ in prods}
    lead = {a: set() for a in nts}
    trail = {a: set() for a in nts}
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            new_l = set(lead[rhs[0]]) if rhs[0] in nts else {rhs[0]}
            if rhs[0] in nts and len(rhs) > 1:
                new_l.add(rhs[1])
            new_t = set(trail[rhs[-1]]) if rhs[-1] in nts else {rhs[-1]}
            if rhs[-1] in nts and len(rhs) > 1:
                new_t.add(rhs[-2])
            if not new_l <= lead[a] or not new_t <= trail[a]:
                lead[a] |= new_l
                trail[a] |= new_t
                changed = True
    rel: dict[tuple[str, str], str] = {}

    def add(x, y, r):
        old = rel.setdefault((x, y), r)
        if old != r:
            raise ValueError(f"precedence conflict between {x} and {y}: {old} and {r}")

    framed = [(None, (END, start, END))] if start in nts else []
    for _, rhs in framed + prods:
        for i in range(len(rhs) - 1):
            x, y = rhs[i], rhs[i + 1]
            if x not in nts and y not in nts:
                add(x, y, "=")
            if x not in nts and y in nts:
                if i + 2 < len(rhs):
                    add(x, rhs[i + 2], "=")
                for b in lead[y]:
                    add(x, b, "<")
            if x in nts and y not in nts:
                for a in trail[x]:
                    add(a, y, ">")
    rel.pop((END, END), None)
    by_shape: dict[tuple, list[Production]] = {}
    units: dict[str, list[str]] = {}
    for a, rhs in prods:
        if len(rhs) == 1 and rhs[0] in nts:
            units.setdefault(rhs[0], []).append(a)
        else:
            by_shape.setdefault(_shape(rhs, nts), []).append((a, rhs))
    return PrecedenceTable(start, nts, rel, by_shape, units)


def _reduce(table: PrecedenceTable, handle: list, position: int) -> dict:
    """Label sets: the nonterminals that derive the handle, each with a tree."""
    shape = tuple(None if isinstance(x, dict) else x for x in handle)
    out: dict[str, Tree] = {}
    for a, rhs in table.by_shape.get(shape, []):
        if a in out:
            continue
        kids = []
        for x, h in zip(rhs, handle):
            if isinstance(h, dict):
                if x not in h:
                    break
                kids.append(h[x])
            else:
                kids.append(h)
        else:
            out[a] = (a, kids)
    todo = list(out)
    while todo:  # close under unit productions A -> B
        b = todo.pop()
        for a in table.units.get(b, []):
            if a not in out:
                out[a] = (a, [out[b]])
                todo.append(a)
    if not out:
        raise ParseError(position, "no production matches the handle")
    return out


def op_parse(productions: list[Production], start: str, tokens: list[str],
             table: PrecedenceTable | None = None) -> Tree:
    """Parse tokens; return a parse tree or raise ParseError."""
    if table is None:
        table = build_precedence(productions, start)
    rel = table.rel
    stack: list = [END]  # terminals as strings, nonterminal slots as dicts
    terms = [0]  # indices of the terminals in stack
    w = list(tokens) + [END]
    i = 0  # @line L1
    while True:
        t, b = stack[terms[-1]], w[i]  # @line L2
        if b == END and i < len(w) - 1:
            raise ParseError(i, "end marker inside the input")
        if t == END and b == END:  # @line L3
            if len(stack) == 2 and table.start in stack[1]:
                return stack[1][table.start]
            raise ParseError(i, "input does not reduce to the start symbol")
        r = rel.get((t, b))
        if r in ("<", "="):  # @line L4
            terms.append(len(stack))
            stack.append(b)
            i += 1
        elif r == ">":  # @line L5
            while True:  # @line L6
                last = stack[terms.pop()]
                if rel.get((stack[terms[-1]], last)) == "<":
                    break
            lo = terms[-1] + 1  # @line L7
            handle = stack[lo:]
            del stack[lo:]
            stack.append(_reduce(table, handle, i))  # @line L8
        else:
            raise ParseError(i, f"no relation between {t} and {b}")  # @line L9
