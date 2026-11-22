# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sybilguard/. The authors are listed in prov/QFN0T8.jsonl.

"""SybilGuard random routes, registry tables and verification (Yu et al., SIGCOMM 2006, Section 4).

A small synthetic model of the protocol on an undirected social graph given
as an adjacency dict. The position of a neighbor in a node's list is the
number of that edge. Identities are node names; real public keys, edge keys
and network messages are left out.
"""

import random
from typing import Hashable, Iterable, Mapping, Optional, Sequence

Node = Hashable
Adj = Mapping[Node, Sequence[Node]]
Perm = Mapping[Node, Sequence[int]]
Registry = dict[tuple[Node, Node], list[Node]]


def routing_tables(adj: Adj, rng: random.Random) -> dict[Node, list[int]]:
    """A uniformly random permutation of the edges of every node.

    perm[x][i] is the edge on which x forwards a route that arrived on edge i.
    Cost: O(n + m) time and space.
    """
    perm: dict[Node, list[int]] = {}
    for x in adj:
        p = list(range(len(adj[x])))
        rng.shuffle(p)  # @line L1
        perm[x] = p
    return perm


def next_hop(adj: Adj, perm: Perm, prev: Node, x: Node) -> Node:
    """The node after x on a route that entered x from prev. Cost: O(deg x)."""
    return adj[x][perm[x][list(adj[x]).index(prev)]]


def route(adj: Adj, perm: Perm, s: Node, j: int, w: int) -> list[Node]:
    """The witness list of the route of s along its edge j: the nodes at hops 1 to w.

    Precondition: 0 <= j < deg(s) and w >= 1. Cost: O(w d) time for maximum degree d.
    """
    prev, x = s, adj[s][j]
    out = [x]
    for _ in range(w - 1):
        prev, x = x, next_hop(adj, perm, prev, x)
        out.append(x)
    return out


def registries(
    adj: Adj,
    perm: Perm,
    w: int,
    honest: Optional[set] = None,
    forged: Optional[Mapping[tuple[Node, Node], Sequence[Node]]] = None,
) -> Registry:
    """Registry tables of the honest nodes after w synchronous rounds of propagation.

    reg[(p, x)][i - 1] is the identity whose route enters x from p at hop i.
    Nodes outside honest are Sybil nodes: on an attack edge (p, x) with p a
    Sybil node, the table is the adversary's choice forged[(p, x)], cut to w
    entries. honest=None means that every node is honest.
    Cost: O(w^2 m) time and O(w m) space.
    """
    if honest is None:
        honest = set(adj)
    forged = forged or {}
    inv = {p: {k: i for i, k in enumerate(perm[p])} for p in adj}
    reg: Registry = {(p, x): [] for x in honest for p in adj[x]}
    for _ in range(w):  # @line L2
        new: Registry = {}
        for (p, x) in reg:  # @line L3
            if p not in honest:
                new[(p, x)] = list(forged.get((p, x), []))[:w]
                continue
            q = adj[p][inv[p][list(adj[p]).index(x)]]
            new[(p, x)] = [p] + reg[(q, p)][: w - 1]  # @line L4
        reg = new
    return reg


def verify(
    adj: Adj,
    perm: Perm,
    w: int,
    reg: Registry,
    v: Node,
    suspect: Node,
    suspect_routes: Iterable[Sequence[Node]],
    honest: Optional[set] = None,
) -> bool:
    """Does the verifier v accept the identity suspect?

    suspect_routes are the witness lists that the suspect sends; a Sybil
    suspect may send any lists. A route of v that reaches a node outside
    honest is under the adversary's control and is counted as accepting.
    Cost: O(d w + L) time for maximum degree d and total claimed length L.
    """
    if honest is None:
        honest = set(adj)
    claimed = set()
    for r in suspect_routes:
        claimed.update(r)
    accepted = 0  # @line L5
    for j in range(len(adj[v])):  # @line L6
        r = route(adj, perm, v, j, w)
        if any(y not in honest for y in r):
            accepted += 1
            continue
        x = next((y for y in r if y in claimed), None)  # @line L7
        if x is not None and any(suspect in reg[(p, x)] for p in adj[x]):  # @line L8
            accepted += 1
    return 2 * accepted >= len(adj[v])  # @line L9


def own_routes(adj: Adj, perm: Perm, s: Node, w: int) -> list[list[Node]]:
    """The d witness lists of an honest node s, one per edge. Cost: O(d^2 w)."""
    return [route(adj, perm, s, j, w) for j in range(len(adj[s]))]
