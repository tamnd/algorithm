# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gll-parsing/. The authors are listed in prov/0BHT8C.jsonl.

"""A GLL recognizer: generalized top-down parsing with descriptors and a graph-structured stack.

gll(productions, tokens) decides whether the token sequence belongs to the
language of the grammar, for any context-free grammar, including left-recursive,
ambiguous and cyclic ones and grammars with epsilon-productions.

A production is (lhs, rhs) with rhs a tuple of symbols. The left sides are the
nonterminals; every other symbol is a terminal. The first production's left
side is the start symbol.

A grammar slot is (p, d): production p with the dot before rhs[d]. A GSS node is
(p, d, i): the return slot (p, d), right after a nonterminal, and the input
position i at which that nonterminal was called. The root node is ROOT. A
descriptor (p, d, u, i) says: continue at slot (p, d) with stack top u at input
position i.
"""

from collections.abc import Sequence
from dataclasses import dataclass, field

ROOT = ("$root",)


@dataclass
class GLLResult:
    accepted: bool
    ends: set[int] = field(default_factory=set)  # positions i such that S derives tokens[:i]
    spans: set[tuple[str, int, int]] = field(default_factory=set)  # (A, i, j): A called at i derives tokens[i:j]
    descriptors: int = 0  # the number of distinct descriptors processed
    gss_nodes: int = 0
    gss_edges: int = 0


def gll(productions: Sequence[tuple[str, Sequence[str]]], tokens: Sequence[str]) -> GLLResult:
    """Recognize tokens with the grammar; also report the derived spans that the search found."""
    prods = [(a, tuple(rhs)) for a, rhs in productions]
    nts = {a for a, _ in prods}
    by_lhs: dict[str, list[int]] = {}
    for p, (a, _) in enumerate(prods):
        by_lhs.setdefault(a, []).append(p)
    start = prods[0][0]
    n = len(tokens)

    seen: set[tuple] = set()  # U: every descriptor ever added
    todo: list[tuple] = []  # R: descriptors still to process
    edges: dict[tuple, set[tuple]] = {}  # GSS node -> the nodes below it
    popped: dict[tuple, set[int]] = {}  # P: GSS node -> positions at which it was popped
    result = GLLResult(False)

    def add(p: int, d: int, u: tuple, i: int) -> None:
        if (p, d, u, i) not in seen:  # @line L12
            seen.add((p, d, u, i))
            todo.append((p, d, u, i))

    def create(p: int, d: int, u: tuple, i: int) -> tuple:
        v = (p, d, i)  # @line L7
        below = edges.setdefault(v, set())
        if u not in below:  # @line L8
            below.add(u)
            for k in list(popped.get(v, ())):
                add(p, d, u, k)
        return v  # @line L9

    def pop(u: tuple, i: int) -> None:
        if u == ROOT:  # @line L10
            result.ends.add(i)
            return
        ks = popped.setdefault(u, set())
        if i not in ks:  # @line L11
            ks.add(i)
            p, d, _ = u
            for v in list(edges[u]):
                add(p, d, v, i)

    for p in by_lhs[start]:
        add(p, 0, ROOT, 0)  # @line L1
    while todo:
        p, d, u, i = todo.pop()  # @line L2
        rhs = prods[p][1]
        while d < len(rhs) and rhs[d] not in nts:  # @line L3
            if i < n and tokens[i] == rhs[d]:
                d += 1
                i += 1
            else:
                break
        else:
            if d < len(rhs):
                v = create(p, d + 1, u, i)  # @line L4
                for q in by_lhs[rhs[d]]:
                    add(q, 0, v, i)
            else:
                pop(u, i)  # @line L5
    result.accepted = n in result.ends  # @line L6
    for (p, d, i), ks in popped.items():
        a = prods[p][1][d - 1]
        for j in ks:
            result.spans.add((a, i, j))
    result.descriptors = len(seen)
    result.gss_nodes = len(edges)
    result.gss_edges = sum(len(s) for s in edges.values())
    return result
