# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/factorized-representation/. The authors are listed in prov/7ZFJ86.jsonl.

"""Factorized representations of relations and of natural join results over f-trees.

A representation over a forest of attributes is a tuple with one union per
root. A union for the attribute A is a list of pairs (a, factors), sorted by
the value a, where factors is a tuple with one union per child of A. The pair
stands for the singleton <A:a> times the product of the factors, and a union
stands for the union of its pairs. A union with no pairs is the empty relation.
"""

from collections import defaultdict
from math import prod


class FTree:
    """A rooted forest with one attribute per node.

    nodes is a list of (attribute, parent), with parent None for a root. A
    parent must come before its children. The children keep the input order.
    """

    def __init__(self, nodes: list) -> None:
        self.parent = {}
        self.kids = {}
        self.roots = []
        for a, p in nodes:
            if a in self.parent:
                raise ValueError("the attribute %r occurs twice" % (a,))
            if p is not None and p not in self.parent:
                raise ValueError("the parent %r must come before %r" % (p, a))
            self.parent[a] = p
            self.kids[a] = []
            (self.roots if p is None else self.kids[p]).append(a)
        self.attrs = tuple(a for a, _ in nodes)

    def path(self, a: str) -> list:
        """The attributes from the root down to a, a included."""
        out = []
        while a is not None:
            out.append(a)
            a = self.parent[a]
        return out[::-1]


def path_condition(ftree: FTree, schemas: list) -> bool:
    """True when the attributes of each schema lie on one root-to-leaf path."""
    for schema in schemas:
        for a in schema:
            for b in schema:
                if a not in ftree.path(b) and b not in ftree.path(a):
                    return False
    return True


def valid(ftree: FTree, schemas: list) -> bool:
    """True when the f-tree has exactly the attributes of the query and the path condition holds."""
    attrs = {a for schema in schemas for a in schema}
    return len(ftree.attrs) > 0 and set(ftree.attrs) == attrs and path_condition(ftree, schemas)


def from_join(ftree: FTree, rels: list) -> tuple:
    """The representation over ftree of the natural join of rels, a list of dbrel.Relation, read as sets."""
    if not valid(ftree, [r.schema for r in rels]):                              # @line L1
        raise ValueError("the f-tree is not valid for this join")              # @line L1
    users = defaultdict(list)
    for r in rels:
        for a in r.schema:
            above = [b for b in ftree.path(a)[:-1] if b in r.schema]
            pos, ia = [r.index(b) for b in above], r.index(a)
            idx = defaultdict(set)
            for t in r.rows:
                idx[tuple(t[j] for j in pos)].add(t[ia])
            users[a].append((above, idx))

    def product(trees: list, t: dict):
        factors = []
        for a in trees:                                                         # @line L3
            u = union(a, t)                                                     # @line L4
            if not u:                                                           # @line L5
                return None                                                     # @line L5
            factors.append(u)                                                   # @line L4
        return tuple(factors)                                                   # @line L6

    def union(a: str, t: dict) -> list:
        sets = [idx.get(tuple(t[b] for b in above), ()) for above, idx in users[a]]  # @line L7
        small = min(sets, key=len)                                              # @line L7
        values = sorted(v for v in small if all(v in s for s in sets))          # @line L7
        out = []
        for v in values:                                                        # @line L8
            t[a] = v                                                            # @line L9
            p = product(ftree.kids[a], t)                                       # @line L9
            del t[a]                                                            # @line L9
            if p is not None:                                                   # @line L10
                out.append((v, p))                                              # @line L10
        return out                                                              # @line L11

    top = product(ftree.roots, {})                                              # @line L2
    return top if top is not None else tuple([] for _ in ftree.roots)          # @line L2


def factorize(ftree: FTree, rel) -> tuple:
    """The representation over ftree of one relation, read as a set.

    It raises ValueError when the relation has no representation over ftree.
    """
    if set(rel.schema) != set(ftree.attrs):
        raise ValueError("the f-tree and the relation have different attributes")
    pos = {a: rel.index(a) for a in rel.schema}

    def product(trees: list, rows: set) -> tuple:
        return tuple(union(a, rows) for a in trees)

    def union(a: str, rows: set) -> list:
        groups = defaultdict(set)
        for t in rows:
            groups[t[pos[a]]].add(t)
        return [(v, product(ftree.kids[a], groups[v])) for v in sorted(groups)]

    rows = set(rel.rows)
    e = product(ftree.roots, rows)
    if count(e) != len(rows):
        raise ValueError("the relation does not factorize over this f-tree")
    return e


def count(e: tuple) -> int:
    """The number of tuples that the representation stands for."""
    return prod(sum(count(factors) for _, factors in u) for u in e)


def size(e: tuple) -> int:
    """The number of singletons in the representation."""
    return sum(len(u) + sum(size(factors) for _, factors in u) for u in e)


def tuples(ftree: FTree, e: tuple):
    """Yield every tuple once, with the attributes in the order ftree.attrs."""

    def walk(pending: list, t: dict):
        if not pending:
            yield tuple(t[a] for a in ftree.attrs)
            return
        (a, u), rest = pending[0], pending[1:]
        for v, factors in u:
            t[a] = v
            yield from walk(list(zip(ftree.kids[a], factors)) + rest, t)
        t.pop(a, None)

    yield from walk(list(zip(ftree.roots, e)), {})
