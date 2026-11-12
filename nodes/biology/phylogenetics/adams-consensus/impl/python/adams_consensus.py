# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adams-consensus/. The authors are listed in prov/V4J1S8.jsonl.

"""Adams consensus of rooted trees by partition refinement (Adams 1972).

A tree is a nested tuple. A leaf is an int label, and an internal node is a
tuple of two or more subtrees. All trees must have the same leaf set, with
each label once.

For a block B of leaves, each tree splits B by the children of the lowest
common ancestor of B. The Adams tree has a node for B whose children are the
blocks of the common refinement of these k partitions, and it repeats this on
every block. With k trees on n leaves the cost is O(k n^2) time and O(k n)
space.
"""

from typing import Dict, List, Sequence, Set, Tuple, Union

Tree = Union[int, tuple]


class _Rooted:
    """Child lists of one tree, with the leaf labels."""

    def __init__(self, tree: Tree) -> None:
        self.children: List[List[int]] = []
        self.label: List[int] = []
        stack = [(tree, -1)]
        while stack:
            t, parent = stack.pop()
            v = len(self.children)
            self.children.append([])
            if isinstance(t, tuple):
                if len(t) < 2:
                    raise ValueError("an internal node needs at least two children")
                self.label.append(-1)
                for c in reversed(t):
                    stack.append((c, v))
            else:
                self.label.append(t)
            if parent >= 0:
                self.children[parent].append(v)
        self.post: List[int] = []
        stack2 = [(0, False)]
        while stack2:
            v, done = stack2.pop()
            if done:
                self.post.append(v)
                continue
            stack2.append((v, True))
            for c in self.children[v]:
                stack2.append((c, False))
        self.leaves = {self.label[v] for v in range(len(self.label)) if self.label[v] >= 0}

    def split_block(self, block: Set[int]) -> Dict[int, int]:
        """Find v = lca(block) and map each leaf of block to the child of v above it."""
        count = [0] * len(self.children)
        v = -1
        for u in self.post:  # @line L4
            if self.label[u] >= 0:
                count[u] = 1 if self.label[u] in block else 0
            else:
                count[u] = sum(count[c] for c in self.children[u])
            if v < 0 and count[u] == len(block):
                v = u
        part: Dict[int, int] = {}
        for i, c in enumerate(self.children[v]):  # @line L5
            stack = [c]
            while stack:
                u = stack.pop()
                if self.label[u] >= 0:
                    if self.label[u] in block:
                        part[self.label[u]] = i
                else:
                    stack.extend(self.children[u])
        return part


def adams_consensus(trees: Sequence[Tree]) -> Tree:
    """Return the Adams consensus tree of the rooted trees as a nested tuple.

    The children of a node are sorted by their smallest leaf label.
    """
    if not trees:
        raise ValueError("need at least one tree")
    rooted = [_Rooted(t) for t in trees]
    leaf_set = rooted[0].leaves
    for r in rooted:
        if r.leaves != leaf_set or len(r.label) - r.label.count(-1) != len(leaf_set):
            raise ValueError("the trees must have the same leaf set, each label once")
    built: Dict[int, Tree] = {}
    kids: Dict[int, List[int]] = {}
    blocks: List[frozenset] = [frozenset(leaf_set)]  # @line L1
    stack = [(0, False)]
    while stack:  # @line L2
        b, done = stack.pop()
        block = blocks[b]
        if done:
            parts = sorted(kids[b], key=lambda c: min(blocks[c]))
            built[b] = tuple(built[c] for c in parts)
            continue
        if len(block) == 1:  # @line L3
            built[b] = next(iter(block))
            continue
        groups: Dict[Tuple[int, ...], List[int]] = {}
        maps = [r.split_block(set(block)) for r in rooted]  # @line L4
        for x in block:  # @line L6
            key = tuple(m[x] for m in maps)
            groups.setdefault(key, []).append(x)
        kids[b] = []
        stack.append((b, True))  # @line L7
        for g in groups.values():
            c = len(blocks)
            blocks.append(frozenset(g))
            kids[b].append(c)
            stack.append((c, False))  # @line L8
    return built[0]  # @line L9


def clusters(tree: Tree) -> Set[frozenset]:
    """All clusters of a tree with two or more leaves, the root cluster included."""
    r = _Rooted(tree)
    below: Dict[int, frozenset] = {}
    out: Set[frozenset] = set()
    for v in r.post:
        if r.label[v] >= 0:
            below[v] = frozenset([r.label[v]])
        else:
            below[v] = frozenset().union(*(below[c] for c in r.children[v]))
            out.add(below[v])
    return out
