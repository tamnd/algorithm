# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phylogenetic-network/. The authors are listed in prov/PV464M.jsonl.

"""Rooted phylogenetic network: a directed acyclic graph with labeled leaves.

Vertices are ints. The network keeps, for each vertex, its list of children
and its list of parents, and a label for each leaf. An arc is added only if it
keeps the graph acyclic. A vertex with two or more parents is a reticulation.

The class answers these queries:

- reticulation_number(): the sum over vertices of (in-degree - 1), which is
  |E| - |V| + 1 for a network with one root.
- is_valid(): one root, leaves are exactly the labeled vertices, each tree
  vertex has one parent and at least two children (the root may have one),
  and each reticulation has exactly one child.
- is_tree_child(): every vertex that is not a leaf has a child that is not a
  reticulation.
- displayed_trees(): the set of trees that the network displays, each as a
  frozenset of clusters (frozensets of labels). Each tree comes from a
  switching, which keeps one parent arc of every reticulation.
"""

from itertools import product
from typing import Dict, FrozenSet, Hashable, List, Set


class CycleError(ValueError):
    """The arc would close a directed cycle."""


class PhylogeneticNetwork:
    def __init__(self) -> None:
        self.children: Dict[int, List[int]] = {}
        self.parents: Dict[int, List[int]] = {}
        self.label: Dict[int, Hashable] = {}
        self._arcs = 0

    def add_vertex(self, v: int, label: Hashable = None) -> None:
        if v in self.children:
            raise ValueError("vertex exists")
        self.children[v] = []
        self.parents[v] = []
        if label is not None:
            if label in self.label.values():
                raise ValueError("label used twice")
            self.label[v] = label

    def reaches(self, u: int, v: int) -> bool:
        """Is there a directed path from u to v?"""
        seen = {u}
        stack = [u]
        while stack:
            x = stack.pop()
            if x == v:
                return True
            for y in self.children[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        return False

    def add_arc(self, u: int, v: int) -> None:
        if u not in self.children or v not in self.children:
            raise KeyError("unknown vertex")
        if v in self.children[u]:
            raise ValueError("parallel arc")
        if self.reaches(v, u):  # @line L1
            raise CycleError("the arc would close a cycle")
        self.children[u].append(v)  # @line L2
        self.parents[v].append(u)  # @line L2
        self._arcs += 1

    def arc_count(self) -> int:
        return self._arcs

    def roots(self) -> List[int]:
        return [v for v in self.children if not self.parents[v]]

    def reticulations(self) -> List[int]:
        return [v for v in self.children if len(self.parents[v]) >= 2]

    def reticulation_number(self) -> int:
        return sum(len(p) - 1 for p in self.parents.values() if p)  # @line L3

    def is_valid(self) -> bool:
        roots = self.roots()
        if len(roots) != 1:
            return False
        root = roots[0]
        for v in self.children:
            indeg, outdeg = len(self.parents[v]), len(self.children[v])
            if outdeg == 0:
                if v not in self.label or indeg != 1:
                    return False
            elif v in self.label:
                return False
            elif v == root:
                continue
            elif indeg == 1 and outdeg < 2:
                return False
            elif indeg >= 2 and outdeg != 1:
                return False
        return True

    def is_tree_child(self) -> bool:
        for v, ch in self.children.items():  # @line L4
            if ch and all(len(self.parents[c]) >= 2 for c in ch):
                return False
        return True  # @line L5

    def displayed_trees(self) -> Set[FrozenSet[FrozenSet[Hashable]]]:
        roots = self.roots()
        if len(roots) != 1:
            raise ValueError("a network has one root")
        root = roots[0]
        ret = self.reticulations()
        out: Set[FrozenSet[FrozenSet[Hashable]]] = set()
        for choice in product(*(self.parents[r] for r in ret)):  # @line L6
            keep = dict(zip(ret, choice))
            kids: Dict[int, List[int]] = {v: [] for v in self.children}
            for v, ps in self.parents.items():  # @line L7
                if len(ps) == 1:
                    kids[ps[0]].append(v)
                elif len(ps) >= 2:
                    kids[keep[v]].append(v)
            out.add(_clusters(root, kids, self.label))  # @line L8
        return out  # @line L9


def _clusters(root: int, kids: Dict[int, List[int]], label: Dict[int, Hashable]) -> FrozenSet[FrozenSet[Hashable]]:
    """Nonempty clusters of the tree given by kids, by an explicit postorder."""
    below: Dict[int, FrozenSet[Hashable]] = {}
    stack = [(root, False)]
    while stack:
        v, done = stack.pop()
        if done:
            s: Set[Hashable] = {label[v]} if v in label else set()
            for c in kids[v]:
                s |= below[c]
            below[v] = frozenset(s)
            continue
        stack.append((v, True))
        for c in kids[v]:
            stack.append((c, False))
    return frozenset(c for c in below.values() if c)
