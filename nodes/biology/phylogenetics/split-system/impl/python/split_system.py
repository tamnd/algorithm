# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/split-system/. The authors are listed in prov/1ZMY7S.jsonl.

"""A split system on a fixed taxon set, stored as a set of bit masks.

Taxon i of the list `taxa` is bit i. A split A|B is stored as the mask of the
side that does not hold taxa[0], the reference taxon r. With this rule each
split has one mask, and the stored masks are the clusters of the tree rooted
at r. Two splits are compatible exactly when their masks are disjoint or
nested.

An unrooted tree is a dict that maps each vertex to the list of its
neighbours. The leaves are the taxa (strings); the internal vertices are ints.
"""

from __future__ import annotations

from typing import Hashable, Iterable

Tree = dict[Hashable, list[Hashable]]


class SplitSystem:
    def __init__(self, taxa: Iterable[str]):
        self.taxa = list(taxa)
        if len(set(self.taxa)) != len(self.taxa) or len(self.taxa) < 2:
            raise ValueError("need at least two distinct taxa")
        self.index = {x: i for i, x in enumerate(self.taxa)}
        self.full = (1 << len(self.taxa)) - 1
        self.masks: set[int] = set()

    # -- the representation -------------------------------------------------

    def normalize(self, mask: int) -> int:
        """The canonical mask of the split with side `mask`: the side without taxon 0."""
        if mask <= 0 or mask >= self.full:
            raise ValueError("both sides of a split must be non-empty")
        return self.full ^ mask if mask & 1 else mask

    def mask_of(self, side: Iterable[str]) -> int:
        m = 0
        for x in side:
            m |= 1 << self.index[x]
        return m

    def side(self, mask: int) -> frozenset[str]:
        return frozenset(x for i, x in enumerate(self.taxa) if mask >> i & 1)

    # -- operations ---------------------------------------------------------

    def add(self, side: Iterable[str]) -> int:
        m = self.normalize(self.mask_of(side))
        self.masks.add(m)
        return m

    def __contains__(self, side: Iterable[str]) -> bool:
        return self.normalize(self.mask_of(side)) in self.masks

    def __len__(self) -> int:
        return len(self.masks)

    def splits(self) -> set[tuple[frozenset[str], frozenset[str]]]:
        """Each split as (side without taxa[0], side with taxa[0])."""
        return {(self.side(m), self.side(self.full ^ m)) for m in self.masks}

    @staticmethod
    def compatible_masks(a: int, b: int) -> bool:
        """Two normalized masks are compatible iff they are disjoint or nested."""
        c = a & b
        return c == 0 or c == a or c == b

    def is_trivial(self, mask: int) -> bool:
        return mask & (mask - 1) == 0 or mask == self.full ^ 1

    def nontrivial(self) -> set[int]:
        return {m for m in self.masks if not self.is_trivial(m)}

    def is_compatible(self) -> bool:
        """True iff the splits are pairwise compatible. O(k^2) mask operations."""
        ms = list(self.masks)
        return all(self.compatible_masks(ms[i], ms[j]) for i in range(len(ms)) for j in range(i))

    # -- the link with trees ------------------------------------------------

    @classmethod
    def from_tree(cls, tree: Tree, taxa: Iterable[str] | None = None) -> "SplitSystem":
        """The splits of all edges of an unrooted tree, trivial ones included."""
        leaves = sorted(v for v, nb in tree.items() if len(nb) == 1) if taxa is None else list(taxa)
        S = cls(leaves)
        r = S.taxa[0]
        below: dict[Hashable, int] = {}
        parent = {r: None}  # @line L1
        order = [r]
        for v in order:  # breadth-first order from r; the list grows as we go
            for w in tree[v]:
                if w not in parent:
                    parent[w] = v
                    order.append(w)
        if len(order) != len(tree):
            raise ValueError("the graph is not connected")
        for v in reversed(order):  # @line L2 (children before parents)
            m = (1 << S.index[v]) if v in S.index and v != r else 0  # @line L3
            for w in tree[v]:  # @line L4
                if w != parent[v]:
                    m |= below[w]
            below[v] = m
            if v != r:  # @line L5 (the edge from v to its parent)
                S.masks.add(m)
        S.masks.discard(0)  # an internal vertex of degree 1 would give an empty side
        return S  # @line L6

    def to_tree(self) -> Tree:
        """The unique tree whose split set is this system plus the trivial splits.

        Raise ValueError if the splits are not pairwise compatible. Needs at least 3 taxa.
        Process the clusters by decreasing size. For each taxon x keep deepest[x], the smallest
        cluster seen so far that holds x. The parent of a cluster C is deepest[x] for any x in C.
        """
        n = len(self.taxa)
        if n < 3:
            raise ValueError("need at least three taxa")
        top = self.full ^ 1  # the cluster X - {r}, the side of the trivial split of r
        clusters = set(self.masks) | {1 << i for i in range(1, n)} | {top}
        order = sorted(clusters, key=lambda m: -m.bit_count())
        vid: dict[int, Hashable] = {}
        tree: Tree = {self.taxa[0]: []}
        deepest = [top] * n
        next_id = 0
        for C in order:
            if C.bit_count() == 1:
                vid[C] = self.taxa[C.bit_length() - 1]
            else:
                vid[C] = next_id
                next_id += 1
            tree[vid[C]] = []
            if C == top:
                parent = self.taxa[0]
            else:
                x = (C & -C).bit_length() - 1  # any taxon of C
                P = deepest[x]
                if P & C != C:
                    raise ValueError("the splits are not pairwise compatible")
                parent = vid[P]
                # Every taxon of C must have the same deepest cluster P, else some cluster crosses C.
            m = C
            while m:
                low = m & -m
                i = low.bit_length() - 1
                if C != top and deepest[i] != P:
                    raise ValueError("the splits are not pairwise compatible")
                deepest[i] = C
                m ^= low
            tree[vid[C]].append(parent)
            tree[parent].append(vid[C])
        return tree


def splits_of_tree(tree: Tree) -> set[frozenset[frozenset[str]]]:
    """Reference: each split as an unordered pair of leaf sets, by removing each edge (O(n^2))."""
    leaves = {v for v, nb in tree.items() if len(nb) == 1}
    out = set()
    for u in tree:
        for v in tree[u]:
            seen = {u, v}
            stack = [v]
            side = set()
            while stack:
                w = stack.pop()
                if w in leaves:
                    side.add(w)
                for z in tree[w]:
                    if z not in seen:
                        seen.add(z)
                        stack.append(z)
            out.add(frozenset([frozenset(side), frozenset(leaves - side)]))
    return out
