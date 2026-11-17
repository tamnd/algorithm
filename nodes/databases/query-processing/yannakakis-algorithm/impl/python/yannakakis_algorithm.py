# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yannakakis-algorithm/. The authors are listed in prov/D8JPK9.jsonl.

"""Yannakakis algorithm (VLDB 1981) for an acyclic join given by a join tree.

A join tree is a list of nodes. Node u has a tuple of attribute names
attrs[u], a relation rels[u] (a set of tuples in the order of attrs[u]) and a
parent parent[u] (-1 for the root). The tree must satisfy the running
intersection property: the nodes that hold an attribute form a connected
subtree.

The algorithm runs a bottom-up semijoin pass and a top-down semijoin pass
(the full reducer), then joins the reduced relations bottom-up with hash
joins, projecting away attributes that are not needed above.

stats["max_intermediate"] is the largest intermediate result J_u.
"""

from collections.abc import Sequence


def _proj(attrs: Sequence[str], t: tuple, onto: Sequence[str]) -> tuple:
    return tuple(t[attrs.index(a)] for a in onto)


def semijoin(la: Sequence[str], left: set[tuple], ra: Sequence[str], right: set[tuple]) -> set[tuple]:
    """left semijoin right: the tuples of left that agree with some tuple of right."""
    common = [a for a in la if a in ra]
    keys = {_proj(ra, t, common) for t in right}
    return {t for t in left if _proj(la, t, common) in keys}


def hash_join(la: Sequence[str], left: set[tuple], ra: Sequence[str], right: set[tuple]):
    """Natural join; returns (attrs, tuples)."""
    common = [a for a in la if a in ra]
    extra = [a for a in ra if a not in la]
    table: dict[tuple, list[tuple]] = {}
    for t in right:
        table.setdefault(_proj(ra, t, common), []).append(_proj(ra, t, extra))
    out = {t + x for t in left for x in table.get(_proj(la, t, common), ())}
    return list(la) + extra, out


def orders(parent: Sequence[int]) -> tuple[list[int], list[list[int]]]:
    """A pre-order of the tree and the list of children of each node."""
    children: list[list[int]] = [[] for _ in parent]
    roots = []
    for u, p in enumerate(parent):
        (roots if p < 0 else children[p]).append(u)
    if len(roots) != 1:
        raise ValueError("the join tree must have exactly one root")
    pre, stack = [], roots[:]
    while stack:
        u = stack.pop()
        pre.append(u)
        stack.extend(reversed(children[u]))
    if len(pre) != len(parent):
        raise ValueError("parent pointers do not form a tree")
    return pre, children


def full_reducer(attrs: Sequence[Sequence[str]], rels: Sequence[set[tuple]],
                 parent: Sequence[int]) -> list[set[tuple]]:
    """Return the relations after the two semijoin passes."""
    pre, _ = orders(parent)
    r = [set(x) for x in rels]
    for u in reversed(pre):  # @line L1
        p = parent[u]
        if p >= 0:
            r[p] = semijoin(attrs[p], r[p], attrs[u], r[u])
    for u in pre:  # @line L2
        p = parent[u]
        if p >= 0:
            r[u] = semijoin(attrs[u], r[u], attrs[p], r[p])
    return r


def yannakakis(attrs: Sequence[Sequence[str]], rels: Sequence[set[tuple]], parent: Sequence[int],
               out: Sequence[str] | None = None, stats: dict | None = None) -> set[tuple]:
    """Return the join projected on out (all attributes in sorted order if out is None)."""
    allattrs = sorted({a for at in attrs for a in at})
    out = allattrs if out is None else list(out)
    if not set(out) <= set(allattrs):
        raise ValueError("unknown output attribute")
    pre, children = orders(parent)
    r = full_reducer(attrs, rels, parent)
    # J_u holds only attributes of the subtree of u. Line L6 keeps the
    # attributes shared with the parent and the output attributes; by the
    # running intersection property no other attribute appears above u.
    joined: list[tuple[list[str], set[tuple]] | None] = [None] * len(attrs)
    biggest = 0
    for u in reversed(pre):  # @line L3
        ja, jt = list(attrs[u]), r[u]  # @line L4
        for c in children[u]:  # @line L5
            ca, ct = joined[c]
            ja, jt = hash_join(ja, jt, ca, ct)
            joined[c] = None
            biggest = max(biggest, len(jt))
        up = attrs[parent[u]] if parent[u] >= 0 else ()
        keep = [a for a in ja if a in up or a in out]  # @line L6
        if keep != ja:
            jt = {_proj(ja, t, keep) for t in jt}
            ja = keep
        biggest = max(biggest, len(jt))
        joined[u] = (ja, jt)
    ra, rt = joined[pre[0]]  # @line L7
    if stats is not None:
        stats["max_intermediate"] = biggest
    return {_proj(ra, t, out) for t in rt}
