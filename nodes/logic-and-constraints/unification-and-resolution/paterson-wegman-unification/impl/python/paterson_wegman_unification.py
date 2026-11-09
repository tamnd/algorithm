# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/paterson-wegman-unification/. The authors are listed in prov/D70D3M.jsonl.

"""Paterson-Wegman linear unification (1978) on a term DAG.

A term is a variable (a Python str) or a tuple (symbol, arg1, ..., argk).
A constant is a tuple with one item, for example ("a",).
The two input terms are first stored in one DAG with shared subterms, so
each variable is one node. The core runs in time linear in the DAG size.
"""

from typing import Iterator, Optional, Union

Term = Union[str, tuple]
Subst = dict[str, Term]


class UnificationFailure(Exception):
    """Raised inside the algorithm on a clash or a cycle."""


class TermGraph:
    """A term DAG: node i has a symbol, a tuple of child ids and parent ids."""

    def __init__(self) -> None:
        self.table: dict[tuple, int] = {}
        self.symbol: list = []
        self.children: list[tuple[int, ...]] = []
        self.parents: list[list[int]] = []
        self.is_var: list[bool] = []

    def add(self, term: Term) -> int:
        """Store term with sharing and return its node id. Cost: O(size of term)."""
        out: list[int] = []
        stack: list[tuple[Term, bool]] = [(term, False)]
        while stack:
            u, done = stack.pop()
            if not isinstance(u, str) and not done:
                stack.append((u, True))
                for a in reversed(u[1:]):
                    stack.append((a, False))
                continue
            if isinstance(u, str):
                key: tuple = ("var", u)
            else:
                k = len(u) - 1
                args = tuple(out[len(out) - k:]) if k else ()
                del out[len(out) - k:]
                key = ("app", u[0], args)
            node = self.table.get(key)
            if node is None:
                node = len(self.symbol)
                self.table[key] = node
                self.symbol.append(key[1])
                self.children.append(key[2] if key[0] == "app" else ())
                self.parents.append([])
                self.is_var.append(key[0] == "var")
                for c in self.children[node]:
                    self.parents[c].append(node)
            out.append(node)
        return out[0]


def unify_dag(graph: TermGraph, u: int, v: int) -> Optional[dict[int, int]]:
    """Unify the nodes u and v of graph.

    Return a map from each bound variable node to the node it is bound to
    (a triangular, DAG-shaped most general unifier), or None if u and v do
    not unify. Cost: O(number of nodes + number of edges of graph).
    """
    n = len(graph.symbol)
    edges: list[list[int]] = [[] for _ in range(n)]
    ptr: list[int] = [-1] * n
    complete = [False] * n
    binding: dict[int, int] = {}

    def finish(r: int) -> Iterator[int]:
        """Process the class of r. Yields each parent node that must be finished first."""
        if ptr[r] != -1:
            raise UnificationFailure("cycle")  # @line L5
        ptr[r] = r  # @line L6
        stack, members = [r], [r]
        while stack:  # @line L7
            s = stack.pop()  # @line L8
            if not graph.is_var[s] and not graph.is_var[r]:
                if graph.symbol[s] != graph.symbol[r] or len(graph.children[s]) != len(graph.children[r]):
                    raise UnificationFailure("clash")  # @line L9
            for p in graph.parents[s]:  # @line L10
                if not complete[p]:
                    yield p
            for t in edges[s]:  # @line L11
                if ptr[t] == -1:
                    ptr[t] = r  # @line L12
                    stack.append(t)
                    members.append(t)
                elif ptr[t] != r:
                    raise UnificationFailure("cycle")  # @line L13
            if s != r and graph.is_var[s]:
                binding[s] = r  # @line L14
            elif s != r:
                for a, b in zip(graph.children[r], graph.children[s]):  # @line L15
                    edges[a].append(b)
                    edges[b].append(a)
        for m in members:  # @line L16
            complete[m] = True

    def run(r: int) -> None:
        # An explicit stack of generators replaces the recursion of FINISH.
        calls = [finish(r)]
        while calls:
            try:
                p = next(calls[-1])
            except StopIteration:
                calls.pop()
                continue
            if not complete[p]:
                calls.append(finish(p))

    edges[u].append(v)  # @line L1
    edges[v].append(u)
    try:
        for r in range(n):  # @line L2
            if not graph.is_var[r] and not complete[r]:
                run(r)
        for r in range(n):  # @line L3
            if graph.is_var[r] and not complete[r]:
                run(r)
    except UnificationFailure:
        return None
    return binding  # @line L4


def expand(graph: TermGraph, binding: dict[int, int], node: int, memo: dict[int, Term]) -> Term:
    """Return the tree term of node under the triangular binding."""
    stack = [(node, False)]
    while stack:
        d, done = stack.pop()
        if d in memo:
            continue
        if graph.is_var[d]:
            target = binding.get(d, d)
            if target == d:
                memo[d] = graph.symbol[d]
            elif done:
                memo[d] = memo[target]
            else:
                stack.append((d, True))
                stack.append((target, False))
            continue
        kids = graph.children[d]
        if done:
            memo[d] = (graph.symbol[d], *[memo[k] for k in kids])
        else:
            stack.append((d, True))
            stack.extend((k, False) for k in kids if k not in memo)
    return memo[node]


def paterson_wegman_unification(s: Term, t: Term) -> Optional[Subst]:
    """Return an idempotent most general unifier of s and t, or None.

    The unification itself runs in linear time on the shared DAG. The
    returned dict holds tree terms, which can be exponentially larger than
    the DAG; use unify_dag to keep the linear-size triangular form.
    """
    graph = TermGraph()
    u, v = graph.add(s), graph.add(t)
    binding = unify_dag(graph, u, v)
    if binding is None:
        return None
    memo: dict[int, Term] = {}
    sigma: Subst = {}
    for x in binding:
        sigma[graph.symbol[x]] = expand(graph, binding, x, memo)
    return sigma
