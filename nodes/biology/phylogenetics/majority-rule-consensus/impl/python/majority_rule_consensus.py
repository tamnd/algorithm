# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/majority-rule-consensus/. The authors are listed in prov/X4MGF9.jsonl.

"""Majority-rule consensus of rooted trees (Margush and McMorris 1981).

A tree is a nested tuple. A leaf is an int label from 0 to n-1, and an
internal node is a tuple of two or more subtrees. All trees must have the same
leaf set, each label once. For unrooted trees, root every tree at the same
taxon first; then the clusters that do not hold that taxon are the splits.

Each cluster is a bit set in a Python int, and a dict counts how many trees
have it. The clusters in more than half of the trees are pairwise compatible
and form the output tree. With k trees on n leaves the cost is O(k n^2 / w + n^2)
expected time on w-bit words, and O(k n^2 / w) words for the table.
"""

from typing import Dict, List, Sequence, Tuple, Union

Tree = Union[int, tuple]


def cluster_masks(tree: Tree) -> Tuple[List[int], int]:
    """Return the bit sets of the clusters of internal nodes, and the leaf set mask."""
    out: List[int] = []
    mask: Dict[int, int] = {}
    stack = [(tree, False)]
    while stack:
        t, done = stack.pop()
        if not isinstance(t, tuple):
            mask[id(t)] = 0
            continue
        if not done:
            if len(t) < 2:
                raise ValueError("an internal node needs at least two children")
            stack.append((t, True))
            for c in t:
                stack.append((c, False))
            continue
        m = 0
        for c in t:
            if isinstance(c, tuple):
                cm = mask[id(c)]
            else:
                cm = 1 << c
            if m & cm:
                raise ValueError("a leaf label occurs twice")
            m |= cm
        mask[id(t)] = m
        out.append(m)
    if not isinstance(tree, tuple):
        return [], 1 << tree
    return out, mask[id(tree)]


def majority_rule_consensus(trees: Sequence[Tree]) -> Tuple[Tree, Dict[int, int]]:
    """Return the majority-rule tree and, for each of its nontrivial clusters, the number of trees that have it.

    Clusters are bit sets: bit x is set when leaf x is in the cluster.
    Children of a node are sorted by their smallest leaf label.
    """
    if not trees:
        raise ValueError("need at least one tree")
    k = len(trees)
    count: Dict[int, int] = {}  # @line L1
    full = -1
    for t in trees:  # @line L2
        masks, leaves = cluster_masks(t)
        if full >= 0 and leaves != full:
            raise ValueError("the trees have different leaf sets")
        full = leaves
        for m in masks:  # @line L3
            count[m] = count.get(m, 0) + 1
    keep = [m for m, c in count.items() if 2 * c > k and m != full]  # @line L4
    keep.sort(key=lambda m: -bin(m).count("1"))  # @line L5
    n = full.bit_length()
    owner = [full] * n
    kids: Dict[int, List[int]] = {full: []}
    for m in keep:  # @line L6
        x = (m & -m).bit_length() - 1
        kids[owner[x]].append(m)  # @line L7
        kids[m] = []
        y = m
        while y:
            low = y & -y
            owner[low.bit_length() - 1] = m  # @line L8
            y ^= low
    for x in range(n):
        if full >> x & 1:
            kids[owner[x]].append(-1 - x)
    support = {m: count[m] for m in keep}
    return _build(full, kids), support  # @line L9


def _build(full: int, kids: Dict[int, List[int]]) -> Tree:
    def low(m: int) -> int:
        return -1 - m if m < 0 else (m & -m).bit_length() - 1

    built: Dict[int, Tree] = {}
    stack = [(full, False)]
    while stack:
        m, done = stack.pop()
        if m < 0:
            built[m] = -1 - m
            continue
        if not done:
            stack.append((m, True))
            for c in kids[m]:
                stack.append((c, False))
            continue
        built[m] = tuple(built[c] for c in sorted(kids[m], key=low))
    return built[full]
