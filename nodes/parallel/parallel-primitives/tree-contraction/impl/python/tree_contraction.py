# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-contraction/. The authors are listed in prov/TWC8P7.jsonl.

"""Randomized tree contraction (rake and compress) that computes all subtree sums.

The tree is rooted, and each node has at most two children. Each round rakes all
leaves into their parents, then compresses an independent set of unary nodes chosen
by coin flips. The removed nodes are put back in the reverse order of the rounds.
Every comprehension and every loop over a set marked "parallel" is one parallel step
over independent nodes.
"""

import random
from dataclasses import dataclass, field


@dataclass
class Stats:
    """For each round: the live nodes at its start, the nodes raked and the nodes compressed."""

    live: list[int] = field(default_factory=list)
    raked: list[int] = field(default_factory=list)
    compressed: list[int] = field(default_factory=list)


def subtree_sums(
    parent: list[int | None], weight: list[int], rng: random.Random, stats: Stats | None = None
) -> list[int]:
    """Return sub[v], the sum of the weights in the subtree of v, for each node v.

    parent[v] is the parent of v or None at a root. Each node may have at most two
    children. A forest is allowed; each tree is contracted to its root.
    """
    n = len(parent)
    children: list[list[int]] = [[] for _ in range(n)]
    for v in range(n):
        p = parent[v]
        if p is not None:
            children[p].append(v)
    if any(len(c) > 2 for c in children):
        raise ValueError("a node has more than two children")
    par = list(parent)
    acc = list(weight)  # acc[v]: the weight of v plus the weights folded into v
    sub: list[int] = [0] * n
    compressed_child: dict[int, int] = {}  # a compressed node and its child at that time
    history: list[list[int]] = []
    live = list(range(n))
    while any(par[v] is not None for v in live):  # @line L1: some tree has two or more nodes
        if stats is not None:
            stats.live.append(len(live))
        # @line L2 RAKE: each node pulls in its leaf children (owner computes, so no write conflict)
        leaves = {v for v in live if par[v] is not None and not children[v]}
        for p in {par[v] for v in leaves}:  # parallel over parents
            for u in [u for u in children[p] if u in leaves]:
                acc[p] += acc[u]  # the RAKE fold
                sub[u] = acc[u]
            children[p] = [u for u in children[p] if u not in leaves]
        live2 = [v for v in live if v not in leaves]
        # @line L3: coins
        coin = {v: rng.random() < 0.5 for v in live2}

        def unary(v: int) -> bool:
            return par[v] is not None and len(children[v]) == 1

        # @line L4 CHOOSE: unary with heads, and the parent is not a unary node with heads
        chosen = [
            v
            for v in live2
            if unary(v) and coin[v] and not (unary(par[v]) and coin[par[v]])  # type: ignore[arg-type]
        ]
        cset = set(chosen)
        # @line L5 COMPRESS: link the child to the parent; the parent pulls in the folded value
        for v in chosen:  # parallel: the chosen nodes are independent
            p, c = par[v], children[v][0]
            compressed_child[v] = c
            par[c] = p
        for p in {par[v] for v in chosen}:  # parallel over parents, owner computes
            assert p not in cset
            new = []
            for u in children[p]:  # type: ignore[index]
                if u in cset:
                    acc[p] += acc[u]  # type: ignore[index]  # the COMPRESS fold
                    new.append(compressed_child[u])
                else:
                    new.append(u)
            children[p] = new  # type: ignore[index]
        if stats is not None:
            stats.raked.append(len(leaves))
            stats.compressed.append(len(chosen))
        history.append(chosen)
        live = [v for v in live2 if v not in cset]  # @line L6: a pack
    for v in live:  # @line L7 BASE: each root is alone, its subtree sum is its value
        sub[v] = acc[v]
    for chosen in reversed(history):  # @line L8 EXPAND: the last round first
        for v in chosen:  # parallel
            sub[v] = acc[v] + sub[compressed_child[v]]
    return sub
