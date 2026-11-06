# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/glr-parsing/. The authors are listed in prov/Z0RM8G.jsonl.

"""Generalized LR (GLR) recognizer and parser for any context-free grammar.

A grammar is a list of productions (A, rhs), where rhs is a tuple of symbols.
The nonterminals are the left sides and the start symbol; every other symbol
is a terminal. Empty right sides, unit productions, left recursion, hidden
left recursion, cycles and ambiguity are all allowed.

The parser runs the LR(0) automaton of the grammar on all branches at once.
The branches share one graph-structured stack: a node is a pair (state,
level), where the level is the number of input symbols read when the node was
pushed, and an edge v -> x means that the cell v lies directly on the cell x.
Every edge carries one parse tree for the grammar symbol that the edge stands
for, so an accepting edge gives one parse tree of the input. A parse tree is
(A, children), where each child is a tree or a terminal symbol.
"""

from typing import Optional, Sequence, Union

Tree = tuple[str, tuple[Union["Tree", str], ...]]
Production = tuple[str, tuple[str, ...]]
Item = tuple[int, int]
Edge = tuple[int, int]


class Lr0Automaton:
    """The LR(0) automaton of the grammar augmented with S' -> S.

    Production 0 of `prods` is the augmenting production; production p >= 1
    is productions[p - 1]. `goto[q]` maps a symbol to the next state, and
    `reductions[q]` lists the productions p >= 1 with a complete item in q.
    """

    def __init__(self, prods: list[Production], states: list[frozenset[Item]],
                 goto: list[dict[str, int]], reductions: list[list[int]]) -> None:
        self.prods = prods
        self.states = states
        self.goto = goto
        self.reductions = reductions


def lr0_automaton(productions: Sequence[Production], start: str) -> Lr0Automaton:
    """Build the canonical LR(0) automaton by closure and goto."""
    prods: list[Production] = [("S'", (start,))] + [(a, tuple(r)) for a, r in productions]
    nts = {a for a, _ in productions} | {start}
    by_lhs: dict[str, list[int]] = {}
    for p, (a, _) in enumerate(prods):
        if p > 0:
            by_lhs.setdefault(a, []).append(p)

    def closure(kernel: set[Item]) -> frozenset[Item]:
        items = set(kernel)
        todo = list(kernel)
        while todo:
            p, d = todo.pop()
            rhs = prods[p][1]
            if d < len(rhs) and rhs[d] in nts:
                for q in by_lhs.get(rhs[d], []):
                    if (q, 0) not in items:
                        items.add((q, 0))
                        todo.append((q, 0))
        return frozenset(items)

    states = [closure({(0, 0)})]
    index = {states[0]: 0}
    goto: list[dict[str, int]] = []
    k = 0
    while k < len(states):
        moves: dict[str, set[Item]] = {}
        for p, d in states[k]:
            rhs = prods[p][1]
            if d < len(rhs):
                moves.setdefault(rhs[d], set()).add((p, d + 1))
        row: dict[str, int] = {}
        for x, kernel in moves.items():
            target = closure(kernel)
            if target not in index:
                index[target] = len(states)
                states.append(target)
            row[x] = index[target]
        goto.append(row)
        k += 1
    reductions = [sorted(p for p, d in s if p > 0 and d == len(prods[p][1])) for s in states]
    return Lr0Automaton(prods, states, goto, reductions)


def glr_parse(productions: Sequence[Production], start: str, w: Sequence[str]) -> Optional[Tree]:
    """Return one parse tree of w from start, or None if w is not in the language."""
    aut = lr0_automaton(productions, start)                              # @line L1
    prods, goto, red = aut.prods, aut.goto, aut.reductions
    nts = {a for a, _ in productions} | {start}
    n = len(w)
    node_of: dict[tuple[int, int], int] = {}
    state: list[int] = []
    level: list[int] = []
    out: list[dict[int, Union[Tree, str]]] = []   # out[v][x] = tree on the edge v -> x

    def new_node(s: int, j: int) -> int:
        node_of[(s, j)] = len(state)
        state.append(s)
        level.append(j)
        out.append({})
        return len(state) - 1

    root = new_node(0, 0)                                                # @line L2
    frontier = [root]
    for j in range(n + 1):                                               # @line L3
        queue: list[tuple[int, int, Optional[Edge]]] = [
            (u, p, None) for u in frontier for p in red[state[u]]]       # @line L4
        while queue:                                                     # @line L5
            u, p, e = queue.pop()                                        # @line L6
            a, rhs = prods[p]
            for x, kids in _paths(out, level, u, len(rhs), e, j):        # @line L7
                tree: Tree = (a, tuple(kids))
                key = (goto[state[x]][a], j)
                v = node_of.get(key)
                if v is None:                                            # @line L8
                    v = new_node(*key)
                    frontier.append(v)
                    queue.extend((v, q, None) for q in red[key[0]])
                elif x not in out[v]:                                    # @line L9
                    queue.extend((u2, q, (v, x)) for u2 in frontier
                                 for q in red[state[u2]] if prods[q][1])
                if x not in out[v]:                                      # @line L10
                    out[v][x] = tree
        if j < n:                                                        # @line L11
            nxt: list[int] = []
            a = w[j]
            for u in frontier:
                s = goto[state[u]].get(a) if a not in nts else None
                if s is None:
                    continue
                v = node_of.get((s, j + 1))                              # @line L12
                if v is None:
                    v = new_node(s, j + 1)
                    nxt.append(v)
                out[v][u] = a
            frontier = nxt
    acc = goto[0].get(start)                                             # @line L13
    top = node_of.get((acc, n)) if acc is not None else None
    if top is None or root not in out[top]:
        return None
    tree = out[top][root]
    return tree if isinstance(tree, tuple) else None


def glr_recognize(productions: Sequence[Production], start: str, w: Sequence[str]) -> bool:
    """Return True if w is in the language of the grammar."""
    return glr_parse(productions, start, w) is not None


def _paths(out: list[dict[int, Union[Tree, str]]], level: list[int], u: int, m: int,
           through: Optional[Edge], j: int) -> list[tuple[int, list[Union[Tree, str]]]]:
    """All paths of m edges from u, as (end node, edge trees from bottom to top).

    If `through` is an edge (v, x) whose source is at level j, only paths that
    use it are returned. Such a path stays at level j until it uses the edge,
    because edges never go up a level, so a path that leaves level j first is
    cut off. The search keeps its own stack and does not recurse.
    """
    result: list[tuple[int, list[Union[Tree, str]]]] = []
    stack: list[tuple[int, int, bool, list[Union[Tree, str]]]] = [(u, 0, through is None, [])]
    while stack:
        node, depth, used, trees = stack.pop()
        if depth == m:
            if used:
                result.append((node, trees[::-1]))
            continue
        if not used and level[node] < j:
            continue
        for x, t in out[node].items():
            stack.append((x, depth + 1, used or (node, x) == through, trees + [t]))
    return result
