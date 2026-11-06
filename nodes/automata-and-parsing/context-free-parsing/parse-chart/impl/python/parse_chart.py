# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parse-chart/. The authors are listed in prov/37Y8RW.jsonl.

"""A parse chart of dotted edges, and a general chart parser that uses it.

A grammar is a list of productions (A, rhs) with rhs a tuple of symbols. The
nonterminals are the left sides; every other symbol is a terminal. An edge
(i, j, (p, d)) says that the first d symbols of production p derive
tokens[i:j]. Any context-free grammar is allowed, with empty productions,
unit cycles, left recursion and ambiguity.
"""

Production = tuple[str, tuple[str, ...]]
Tree = tuple[str, list] | str
Edge = tuple[int, int, tuple[int, int]]


class ParseError(Exception):
    """The input is not a sentence; position is len(tokens) or the first unusable token."""

    def __init__(self, position: int, message: str) -> None:
        super().__init__(f"{message} at token {position}")
        self.position = position


class Chart:
    """Edges indexed by span, with the two indexes that the fundamental rule needs."""

    def __init__(self, prods: list[Production], n: int) -> None:
        self.prods = prods
        self.n = n
        self.back: dict[Edge, tuple | None] = {}  # edge -> how it was first built
        self.active = [dict() for _ in range(n + 1)]  # j -> X -> [(i, item)] waiting for X at j
        self.passive = [dict() for _ in range(n + 1)]  # i -> A -> [(j, item)] complete A from i

    def add(self, i: int, j: int, item: tuple[int, int], back) -> bool:
        """Insert an edge; return False if it was already there."""
        key = (i, j, item)
        if key in self.back:  # @line L1
            return False
        self.back[key] = back  # @line L2
        p, d = item
        lhs, rhs = self.prods[p]
        if d < len(rhs):
            self.active[j].setdefault(rhs[d], []).append((i, item))  # @line L3
        else:
            self.passive[i].setdefault(lhs, []).append((j, item))  # @line L4
        return True

    def __contains__(self, edge: Edge) -> bool:
        return edge in self.back

    def waiting(self, j: int, x: str) -> list:
        """The active edges (i, item) that end at j and need x next."""
        return self.active[j].get(x, [])

    def complete(self, i: int, a: str) -> list:
        """The complete edges (j, item) for the nonterminal a that start at i."""
        return self.passive[i].get(a, [])

    def __len__(self) -> int:
        return len(self.back)


def fill_chart(productions: list[Production], start: str, tokens: list[str]) -> Chart:
    """Run the chart parser; return the chart."""
    nts = {a for a, _ in productions}
    by_lhs: dict[str, list[int]] = {}
    for p, (a, _) in enumerate(productions):
        by_lhs.setdefault(a, []).append(p)
    n = len(tokens)
    chart = Chart(productions, n)
    agenda: list[Edge] = []

    def push(i, j, item, back):
        if chart.add(i, j, item, back):
            agenda.append((i, j, item))

    for p in by_lhs.get(start, []):  # @line L5
        push(0, 0, (p, 0), None)
    while agenda:  # @line L6
        i, j, item = agenda.pop()
        p, d = item
        lhs, rhs = productions[p]
        if d < len(rhs):
            x = rhs[d]
            if x in nts:
                for q in by_lhs[x]:  # @line L7
                    push(j, j, (q, 0), None)
                for k, it in list(chart.complete(j, x)):  # @line L8
                    push(i, k, (p, d + 1), ((i, j, item), (j, k, it)))
            elif j < n and tokens[j] == x:  # @line L9
                push(i, j + 1, (p, d + 1), ((i, j, item), x))
        else:
            for h, it in list(chart.waiting(i, lhs)):  # @line L10
                push(h, j, (it[0], it[1] + 1), ((h, i, it), (i, j, item)))
    return chart


def _children(chart: Chart, edge: Edge) -> list:
    kids = []
    back = chart.back[edge]
    while back is not None:
        prev, child = back
        kids.append(child)
        back = chart.back[prev]
    kids.reverse()
    return kids


def chart_tree(chart: Chart, edge: Edge) -> Tree:
    """Read one parse tree off the backpointers of a complete edge, without recursion."""
    built: dict[Edge, Tree] = {}
    todo = [(edge, False)]
    while todo:
        e, ready = todo.pop()
        if e in built:
            continue
        kids = _children(chart, e)
        if ready:
            lhs = chart.prods[e[2][0]][0]
            built[e] = (lhs, [k if isinstance(k, str) else built[k] for k in kids])
            continue
        todo.append((e, True))
        todo.extend((k, False) for k in kids if not isinstance(k, str) and k not in built)
    return built[edge]


def chart_parse(productions: list[Production], start: str, tokens: list[str]) -> Tree:
    """Return a parse tree of tokens, or raise ParseError."""
    chart = fill_chart(productions, start, tokens)
    n = len(tokens)
    for j, item in chart.complete(0, start):  # @line L11
        if j == n:
            return chart_tree(chart, (0, n, item))  # @line L12
    last = max((j for (_, j, _) in chart.back), default=0)
    raise ParseError(min(last, n), "no parse")
