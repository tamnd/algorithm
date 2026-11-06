# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/recursive-descent-parsing/. The authors are listed in prov/FBHW41.jsonl.

"""A predictive recursive descent parser for an LL(1) grammar.

A grammar is a list of productions (A, rhs) with rhs a tuple of symbols; the
nonterminals are the left sides and every other symbol is a terminal. The
end marker "$" must not be a grammar symbol. A parse tree is (A, children),
where each child is a tree or a terminal.

Each nonterminal gets one procedure, PROC(A). The procedures are Python
generators: a call PROC(B) is a `yield B` that the driver answers with the
subtree of B. So the recursion of the method lives on an explicit list, and a
deeply nested input does not hit the Python recursion limit.
"""

from typing import Generator, Sequence, Union

Tree = tuple[str, tuple[Union["Tree", str], ...]]
Production = tuple[str, tuple[str, ...]]
END = "$"


class GrammarError(ValueError):
    """The grammar is not LL(1), or it is left recursive."""


class ParseError(ValueError):
    """The input is not in the language of the grammar."""


def _analyse(prods: Sequence[Production], start: str):
    nts = {a for a, _ in prods}
    nullable: set[str] = set()
    first: dict[str, set[str]] = {a: set() for a in nts}
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            if a not in nullable and all(x in nullable for x in rhs):
                nullable.add(a)
                changed = True
            for x in rhs:
                f = first[x] if x in nts else {x}
                if not f <= first[a]:
                    first[a] |= f
                    changed = True
                if x not in nullable:
                    break

    def first_of(seq: Sequence[str]) -> tuple[set[str], bool]:
        out: set[str] = set()
        for x in seq:
            out |= first[x] if x in nts else {x}
            if x not in nullable:
                return out, False
        return out, True

    follow: dict[str, set[str]] = {a: set() for a in nts}
    follow[start].add(END)
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            for i, x in enumerate(rhs):
                if x in nts:
                    f, nul = first_of(rhs[i + 1:])
                    add = f | follow[a] if nul else f
                    if not add <= follow[x]:
                        follow[x] |= add
                        changed = True
    return nts, nullable, first_of, follow


class RecursiveDescentParser:
    """Build with an LL(1) grammar; then parse(tokens) returns the parse tree.

    Construction costs O(|V| * |Sigma| * |G|) set operations. A parse costs
    time linear in the size of the parse tree, which is O(n) for a fixed
    grammar and an input of n tokens.
    """

    def __init__(self, productions: Sequence[Production], start: str) -> None:
        self.prods = [(a, tuple(r)) for a, r in productions]
        self.start = start
        nts, nullable, first_of, follow = _analyse(self.prods, start)
        if start not in nts or END in {x for _, r in self.prods for x in r}:
            raise GrammarError("bad start symbol or end marker in the grammar")
        self.nts = nts
        # @line L1: PREDICT(A -> alpha) = FIRST(alpha), plus FOLLOW(A) if alpha is nullable
        self.table: dict[tuple[str, str], int] = {}
        for k, (a, rhs) in enumerate(self.prods):
            f, nul = first_of(rhs)
            for t in f | follow[a] if nul else f:
                if (a, t) in self.table:
                    raise GrammarError(f"not LL(1): two productions of {a} on {t!r}")
                self.table[(a, t)] = k
        # Left recursion through nullable prefixes: A -> beta B gamma with beta nullable.
        edges: dict[str, set[str]] = {a: set() for a in nts}
        for a, rhs in self.prods:
            for x in rhs:
                if x in nts:
                    edges[a].add(x)
                if x not in nullable:
                    break
        color = {a: 0 for a in nts}
        for root in nts:
            if color[root]:
                continue
            color[root] = 1
            path = [(root, iter(edges[root]))]
            while path:
                node, it = path[-1]
                nxt = next(it, None)
                if nxt is None:
                    color[node] = 2
                    path.pop()
                elif color[nxt] == 1:
                    raise GrammarError(f"left recursive at {nxt}")
                elif color[nxt] == 0:
                    color[nxt] = 1
                    path.append((nxt, iter(edges[nxt])))

    def parse(self, tokens: Sequence[str]) -> Tree:
        """Return the parse tree of tokens, or raise ParseError."""
        toks = list(tokens) + [END]
        pos = 0

        def proc(a: str) -> Generator[str, Tree, Tree]:
            nonlocal pos
            k = self.table.get((a, toks[pos]))  # @line L5
            if k is None:
                raise ParseError(f"no production of {a} on {toks[pos]!r} at {pos}")
            rhs = self.prods[k][1]
            children: list[Union[Tree, str]] = []  # @line L6
            for x in rhs:  # @line L7
                if x not in self.nts:  # @line L8
                    if toks[pos] != x:  # @line L9
                        raise ParseError(f"expected {x!r} at {pos}, found {toks[pos]!r}")
                    children.append(x)  # @line L10
                    pos += 1
                else:
                    children.append((yield x))  # @line L11
            return (a, tuple(children))  # @line L12

        stack = [proc(self.start)]  # @line L2
        value: Tree | None = None
        result: Tree | None = None
        while stack:
            try:
                callee = stack[-1].send(value)  # type: ignore[arg-type]
            except StopIteration as done:
                stack.pop()
                value = done.value
                result = value
                continue
            stack.append(proc(callee))
            value = None
        if toks[pos] != END:  # @line L3
            raise ParseError(f"extra input at {pos}")
        assert result is not None
        return result  # @line L4

    def recognize(self, tokens: Sequence[str]) -> bool:
        try:
            self.parse(tokens)
        except ParseError:
            return False
        return True
