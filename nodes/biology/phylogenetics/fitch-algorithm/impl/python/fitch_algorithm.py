# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fitch-algorithm/. The authors are listed in prov/NYTSYT.jsonl.

"""Fitch's algorithm for unit-cost small parsimony on a rooted binary tree.

A tree is given by `children`, a list in which `children[v]` is the list of
the children of node v, and by the index of the root. A node with no
children is a leaf. `leaf_state[v]` is the observed state of leaf v.
"""

from collections.abc import Hashable, Sequence
from typing import TypeVar

S = TypeVar("S", bound=Hashable)


def postorder(children: Sequence[Sequence[int]], root: int) -> list[int]:
    """Return the nodes below `root` in postorder, with an explicit stack."""
    order: list[int] = []
    stack = [(root, False)]
    while stack:
        v, done = stack.pop()
        if done:
            order.append(v)
        else:
            stack.append((v, True))
            for w in reversed(children[v]):
                stack.append((w, False))
    return order


def fitch(
    children: Sequence[Sequence[int]], root: int, leaf_state: dict[int, S]
) -> tuple[int, dict[int, frozenset[S]], dict[int, S]]:
    """Run Fitch's two passes for one character.

    Precondition: each internal node has exactly two children, and each leaf
    has a state in `leaf_state`. Returns the parsimony score (the least number
    of changes over all labelings of the internal nodes), the first-pass set
    of each node, and one most parsimonious labeling of all nodes. Ties are
    broken by the smallest state, so the states must be comparable.
    Cost: O(n) set operations, which is O(n k) time for n nodes and k states.
    """
    order = postorder(children, root)
    sets: dict[int, frozenset[S]] = {}
    score = 0  # @line L1
    for v in order:  # @line L2
        if not children[v]:
            sets[v] = frozenset([leaf_state[v]])  # @line L3
            continue
        if len(children[v]) != 2:
            raise ValueError("Fitch's algorithm needs a binary tree")
        left, right = children[v]  # @line L4
        common = sets[left] & sets[right]
        if common:
            sets[v] = common  # @line L5
        else:
            sets[v] = sets[left] | sets[right]  # @line L6
            score += 1
    label: dict[int, S] = {root: min(sets[root])}  # @line L7
    for v in reversed(order):  # parents come before their children
        for w in children[v]:  # @line L8
            if label[v] in sets[w]:
                label[w] = label[v]  # @line L9
            else:
                label[w] = min(sets[w])  # @line L10
    return score, sets, label  # @line L11


def fitch_score(
    children: Sequence[Sequence[int]], root: int, sequences: dict[int, str]
) -> int:
    """Return the parsimony score of aligned sequences at the leaves: the sum over sites."""
    if not sequences:
        return 0
    length = len(next(iter(sequences.values())))
    total = 0
    for i in range(length):
        total += fitch(children, root, {v: s[i] for v, s in sequences.items()})[0]
    return total


def changes(children: Sequence[Sequence[int]], label: dict[int, S]) -> int:
    """Count the edges whose two ends have different labels."""
    return sum(
        1 for v, ws in enumerate(children) if v in label for w in ws if label[v] != label[w]
    )
