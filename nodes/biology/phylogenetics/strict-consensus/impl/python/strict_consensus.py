# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strict-consensus/. The authors are listed in prov/RNKXSB.jsonl.

"""Strict consensus of rooted trees by the cluster table of Day (1985).

A tree is a nested tuple. A leaf is an int label, and an internal node is a
tuple of two or more subtrees. All input trees must have the same leaf set,
each label once, and no internal node with a single child. For unrooted trees,
root every tree at the same reference taxon first; then the clusters that do
not hold that taxon are the splits.

The strict consensus keeps the clusters that are in every input tree. With k
trees on n leaves the cost is O(k n) time and O(n) extra space.
"""

from typing import Dict, List, Sequence, Set, Tuple, Union

Tree = Union[int, tuple]


def _index(tree: Tree) -> Tuple[List[List[int]], List[int], int]:
    """Flatten a nested tuple into child lists. Return (children, label, root).

    label[v] is the leaf label of node v, or -1 for an internal node.
    """
    children: List[List[int]] = []
    label: List[int] = []
    stack = [(tree, -1)]
    while stack:
        t, parent = stack.pop()
        v = len(children)
        children.append([])
        if isinstance(t, tuple):
            if len(t) < 2:
                raise ValueError("an internal node needs at least two children")
            label.append(-1)
            for c in reversed(t):
                stack.append((c, v))
        else:
            label.append(t)
        if parent >= 0:
            children[parent].append(v)
    return children, label, 0


def _postorder(children: List[List[int]], root: int) -> List[int]:
    out: List[int] = []
    stack = [(root, False)]
    while stack:
        v, done = stack.pop()
        if done:
            out.append(v)
            continue
        stack.append((v, True))
        for c in reversed(children[v]):
            stack.append((c, False))
    return out


def strict_consensus(trees: Sequence[Tree]) -> Tree:
    """Return the strict consensus tree of the rooted trees as a nested tuple.

    Children appear in the left-to-right order of the first tree.
    """
    if not trees:
        raise ValueError("need at least one tree")
    ch1, lab1, root1 = _index(trees[0])
    post1 = _postorder(ch1, root1)
    leaves = [v for v in post1 if lab1[v] >= 0]
    n = len(leaves)
    rank: Dict[int, int] = {}
    for i, v in enumerate(leaves):  # @line L1
        rank[lab1[v]] = i + 1
    if len(rank) != n:
        raise ValueError("a leaf label occurs twice")
    lo = [0] * len(ch1)
    hi = [0] * len(ch1)
    for v in post1:  # @line L2
        if lab1[v] >= 0:
            lo[v] = hi[v] = rank[lab1[v]]
        else:
            lo[v] = lo[ch1[v][0]]
            hi[v] = hi[ch1[v][-1]]
    table: List[Tuple[int, int]] = [(0, 0)] * (n + 1)
    row_of: Dict[int, int] = {}
    leftmost = {root1}
    for v in range(len(ch1)):
        if ch1[v]:
            leftmost.add(ch1[v][0])
    for v in post1:  # @line L3
        if lab1[v] < 0:
            r = hi[v] if v in leftmost else lo[v]
            table[r] = (lo[v], hi[v])
            row_of[v] = r
    count = [0] * (n + 1)
    for r in row_of.values():  # @line L4
        count[r] = 1
    for t in trees[1:]:  # @line L5
        ch, lab, root = _index(t)
        mn = [0] * len(ch)
        mx = [0] * len(ch)
        size = [0] * len(ch)
        for w in _postorder(ch, root):  # @line L6
            if lab[w] >= 0:
                if lab[w] not in rank:
                    raise ValueError("the trees have different leaf sets")
                mn[w] = mx[w] = rank[lab[w]]
                size[w] = 1
                continue
            mn[w] = min(mn[c] for c in ch[w])
            mx[w] = max(mx[c] for c in ch[w])
            size[w] = sum(size[c] for c in ch[w])
            a, b = mn[w], mx[w]
            if b - a + 1 == size[w]:  # @line L7
                if table[a] == (a, b):
                    count[a] += 1
                elif table[b] == (a, b):
                    count[b] += 1
        if size[root] != n:
            raise ValueError("the trees have different leaf sets")
    k = len(trees)
    keep = {v for v, r in row_of.items() if count[r] == k}  # @line L8
    keep.add(root1)
    return _contract(ch1, lab1, root1, keep)  # @line L9


def _contract(children: List[List[int]], label: List[int], root: int, keep: Set[int]) -> Tree:
    """Contract every internal edge of the first tree whose lower node is not kept."""
    built: Dict[int, list] = {}
    for v in _postorder(children, root):
        if label[v] >= 0:
            built[v] = [label[v]]
            continue
        parts: list = []
        for c in children[v]:
            if label[c] >= 0 or c in keep:
                parts.append(tuple(built[c]) if label[c] < 0 else label[c])
            else:
                parts.extend(built[c])
        built[v] = parts
    return tuple(built[root])


def clusters(tree: Tree) -> Set[frozenset]:
    """All clusters of a tree with two or more leaves, the root cluster included."""
    ch, lab, root = _index(tree)
    below: Dict[int, frozenset] = {}
    out: Set[frozenset] = set()
    for v in _postorder(ch, root):
        if lab[v] >= 0:
            below[v] = frozenset([lab[v]])
        else:
            below[v] = frozenset().union(*(below[c] for c in ch[v]))
            out.add(below[v])
    return out
