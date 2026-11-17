# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generic-join/. The authors are listed in prov/5SQ32K.jsonl.

"""Generic join (Ngo, Re and Rudra 2013), with hash tries.

A query is a list of edges, each a tuple of attribute names, and one relation
(a set of tuples in the order of its edge) per edge. Generic join binds one
attribute at a time, in a fixed global order. For the next attribute v it
takes, from each relation that holds v, the set of v values consistent with the
current prefix (the keys of a trie node), loops over the smallest set, and
keeps a value only if each other set holds it.

stats["work"][i] is the number of candidate values looped over at level i,
summed over all prefixes: the sum of min_e |R_e[t]| that the AGM-style bound
controls. stats["probes"] counts membership tests.
"""

from collections.abc import Sequence


def build_trie(attrs: Sequence[str], rel: set[tuple], order: Sequence[str]) -> dict:
    """A hash trie of rel with its attributes in the global order."""
    pos = sorted(range(len(attrs)), key=lambda j: order.index(attrs[j]))
    root: dict = {}
    for t in rel:
        node = root
        for j in pos:
            node = node.setdefault(t[j], {})
    return root


def generic_join(edges: Sequence[Sequence[str]], rels: Sequence[set[tuple]],
                 order: Sequence[str] | None = None, stats: dict | None = None) -> list[tuple]:
    """Return the natural join as a list of tuples over the attributes in order."""
    if order is None:
        order = sorted({v for e in edges for v in e})
    order = list(order)
    if {v for e in edges for v in e} != set(order):
        raise ValueError("order must list each attribute once")
    n = len(order)
    tries = [build_trie(e, r, order) for e, r in zip(edges, rels)]
    holders = [[j for j, e in enumerate(edges) if v in e] for v in order]
    work = [0] * n
    probes = 0
    out: list[tuple] = []
    # Explicit stack of (level i, prefix values, current trie node of each relation).
    stack = [(0, (), tuple(tries))]  # @line L1
    while stack:
        i, prefix, nodes = stack.pop()
        if i == n:  # @line L2
            out.append(prefix)
            continue
        cands = [nodes[j] for j in holders[i]]  # @line L3
        small = min(range(len(cands)), key=lambda c: len(cands[c]))  # @line L4
        for a in cands[small]:  # @line L5
            work[i] += 1
            ok = True
            for c, node in enumerate(cands):  # @line L6
                if c != small:
                    probes += 1
                    if a not in node:
                        ok = False
                        break
            if ok:  # @line L7
                nxt = list(nodes)
                for c, j in enumerate(holders[i]):
                    nxt[j] = cands[c][a]
                stack.append((i + 1, prefix + (a,), tuple(nxt)))
    if stats is not None:
        stats["work"] = work
        stats["probes"] = probes
    return out
