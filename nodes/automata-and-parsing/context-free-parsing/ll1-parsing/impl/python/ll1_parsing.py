# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ll1-parsing/. The authors are listed in prov/DYEHVA.jsonl.

"""Table-driven LL(1) parsing.

A grammar is a list of productions (A, rhs) with rhs a tuple of symbols. The
nonterminals are the left sides; every other symbol is a terminal. A parse tree is
a pair (A, children) for a nonterminal node, and a plain string for a token leaf.
"""

END = "$"

Production = tuple[str, tuple[str, ...]]
Tree = tuple[str, list] | str


class ParseError(Exception):
    """The input is not in the language; position is the index of the bad token."""

    def __init__(self, position: int, message: str) -> None:
        super().__init__(f"at token {position}: {message}")
        self.position = position


def build_table(productions: list[Production], start: str) -> dict[tuple[str, str], int]:
    """The LL(1) table M[A, a] -> production index. Raises ValueError on a conflict."""
    nts = {a for a, _ in productions}
    null: set[str] = set()
    first: dict[str, set[str]] = {a: set() for a in nts}
    follow: dict[str, set[str]] = {a: set() for a in nts}
    follow[start].add(END)

    def first_of(alpha: tuple[str, ...]) -> tuple[set[str], bool]:
        out: set[str] = set()
        for x in alpha:
            if x not in nts:
                out.add(x)
                return out, False
            out |= first[x]
            if x not in null:
                return out, False
        return out, True

    changed = True
    while changed:
        changed = False
        for a, rhs in productions:
            f, nul = first_of(rhs)
            if nul and a not in null:
                null.add(a)
                changed = True
            if not f <= first[a]:
                first[a] |= f
                changed = True
            for i, x in enumerate(rhs):
                if x in nts:
                    g, rest_nul = first_of(rhs[i + 1:])
                    if rest_nul:
                        g = g | follow[a]
                    if not g <= follow[x]:
                        follow[x] |= g
                        changed = True
    table: dict[tuple[str, str], int] = {}
    for p, (a, rhs) in enumerate(productions):
        f, nul = first_of(rhs)
        for t in f | (follow[a] if nul else set()):
            if table.setdefault((a, t), p) != p:
                raise ValueError(f"not LL(1): conflict at M[{a}, {t}]")
    return table


def ll1_parse(productions: list[Production], start: str, tokens: list[str],
              table: dict[tuple[str, str], int] | None = None) -> Tree:
    """Parse tokens with an LL(1) grammar and return the parse tree.

    Precondition: the grammar is LL(1) (build_table raises ValueError otherwise) and
    END does not occur in it. Raises ParseError when tokens is not in the language.
    Cost: O(n + number of tree nodes) time after the table is built, which is O(n)
    for a grammar without nullable cycles; O(n) extra space for the stack.
    """
    if table is None:
        table = build_table(productions, start)
    nts = {a for a, _ in productions}
    w = list(tokens) + [END]  # @line L1
    i = 0
    top: list = ["root", []]  # @line L2
    stack: list[tuple[str, list | None]] = [(END, None), (start, top[1])]
    while True:  # @line L3
        x, parent = stack.pop()  # @line L4
        if x == END:  # @line L5
            if i != len(w) - 1:
                raise ParseError(i, f"expected the end of the input, found {w[i]!r}")
            return top[1][0]
        if x not in nts:  # @line L6
            if x != w[i]:  # @line L7
                raise ParseError(i, f"expected {x!r}, found {w[i]!r}")
            parent.append(w[i])  # @line L8
            i += 1
        else:  # @line L9
            p = table.get((x, w[i]))  # @line L10
            if p is None:  # @line L11
                raise ParseError(i, f"no production of {x} starts with {w[i]!r}")
            rhs = productions[p][1]  # @line L12
            node: tuple[str, list] = (x, [])
            parent.append(node)
            for y in reversed(rhs):  # @line L13
                stack.append((y, node[1]))
