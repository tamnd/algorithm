# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/belief-propagation/. The authors are listed in prov/5AZ02P.jsonl.

"""Belief propagation (the sum-product algorithm) on a factor tree.

A model is a list of factors over the variables 0 .. n-1, where variable v takes
the values 0 .. card[v]-1. A factor is a scope (a nonempty tuple of distinct
variables) and a table from assignments of the scope to nonnegative numbers.
The factor graph has a node for each variable and each factor, and an edge
between a factor and each variable of its scope. It must be a forest; then two
passes over each tree give the exact marginals, with one message in each
direction of each edge (Pearl 1988; Kschischang, Frey and Loeliger 2001).
"""

from typing import Dict, List, NamedTuple, Sequence, Tuple

Assignment = Tuple[int, ...]
Node = Tuple[str, int]  # ("v", i) for variable i, ("f", j) for factor j


class Factor(NamedTuple):
    scope: Tuple[int, ...]
    table: Dict[Assignment, object]


class Result(NamedTuple):
    marginals: List[List[object]]                 # marginals[v][x] = P(X_v = x | e)
    factor_marginals: List[Dict[Assignment, object]]  # P(X_scope | e) for each factor
    partition: object    # the sum, over the assignments that agree with e, of the product of the factors
    messages: int


def factor_graph(factors: Sequence[Factor], n: int) -> Dict[Node, List[Node]]:
    nb: Dict[Node, List[Node]] = {("v", v): [] for v in range(n)}
    for j, f in enumerate(factors):
        if not f.scope or len(set(f.scope)) != len(f.scope):
            raise ValueError("a scope must be nonempty and hold each variable once")
        nb[("f", j)] = [("v", v) for v in f.scope]
        for v in f.scope:
            nb[("v", v)].append(("f", j))
    return nb


def belief_propagation(factors: Sequence[Factor], card: Sequence[int],
                       evidence: Dict[int, int]) -> Result:
    """Exact marginals P(X_v | e) on a factor forest by the two-pass schedule."""
    n = len(card)
    one = next((val ** 0 for f in factors for val in f.table.values()), 1)
    zero = 0 * one
    # lam[v] is the evidence indicator of v: 1 on the observed value, 0 elsewhere.
    lam = [[one if v not in evidence or x == evidence[v] else zero for x in range(card[v])]
           for v in range(n)]
    nb = factor_graph(factors, n)
    msg: Dict[Tuple[Node, Node], List[object]] = {}

    def incoming(u: Node, skip: Node, values: Sequence[object]) -> List[object]:
        """values times the messages into the variable u from all neighbours but skip."""
        m = list(values)
        for g in nb[u]:
            if g != skip:
                m = [a * b for a, b in zip(m, msg[g, u])]
        return m

    def send(u: Node, w: Node) -> None:
        if u[0] == "v":
            msg[u, w] = incoming(u, w, lam[u[1]])  # @line L6
            return
        f = factors[u[1]]  # @line L7
        k = f.scope.index(w[1])
        m = [zero] * card[w[1]]
        for a, val in f.table.items():
            for t, y in enumerate(f.scope):
                if t != k:
                    val = val * msg[("v", y), u][a[t]]
            m[a[k]] = m[a[k]] + val
        msg[u, w] = m

    # A breadth-first order of each tree of the forest, from a variable as root.
    order: List[Node] = []
    parent: Dict[Node, Node] = {}
    root_of: Dict[Node, Node] = {}
    for v in range(n):  # @line L1
        root = ("v", v)
        if root in parent:
            continue
        parent[root] = root
        root_of[root] = root
        i = len(order)
        order.append(root)
        while i < len(order):
            u = order[i]
            i += 1
            for w in nb[u]:
                if w == parent[u]:
                    continue
                if w in parent:
                    raise ValueError("the factor graph has a cycle")
                parent[w] = u
                root_of[w] = root
                order.append(w)
    for u in reversed(order):  # @line L2
        if parent[u] != u:
            send(u, parent[u])
    for u in order:  # @line L3
        if parent[u] != u:
            send(parent[u], u)
    marginals: List[List[object]] = []
    z_tree: Dict[Node, object] = {}
    for v in range(n):  # @line L4
        b = incoming(("v", v), ("none", -1), lam[v])
        s = sum(b, zero)
        if s == 0:
            raise ValueError("the evidence has probability zero")
        z_tree[root_of[("v", v)]] = s  # the same sum at every variable of one tree
        marginals.append([x / s for x in b])
    factor_marginals = []
    for j, f in enumerate(factors):
        s = z_tree[root_of[("f", j)]]
        bf = {}
        for a, val in f.table.items():
            for t, y in enumerate(f.scope):
                val = val * msg[("v", y), ("f", j)][a[t]]
            bf[a] = val / s
        factor_marginals.append(bf)
    z = one
    for s in z_tree.values():
        z = z * s
    return Result(marginals, factor_marginals, z, len(msg))  # @line L5
