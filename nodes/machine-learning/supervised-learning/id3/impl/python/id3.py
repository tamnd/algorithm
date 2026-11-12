# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/id3/. The authors are listed in prov/3VDGHC.jsonl.

"""ID3 (Quinlan 1986): a multiway decision tree on categorical attributes,
grown top-down by information gain, with no pruning, plus the windowing loop.

A tree is either ("leaf", label) or ("node", attribute, children, default),
where children maps each attribute value to a subtree and default is the
majority label at the node, used for a value not seen in training.
"""

import random
from collections import Counter
from math import log2
from typing import Any, Hashable, Sequence


def entropy(labels: Sequence[Hashable]) -> float:
    """The entropy of the label distribution, in bits."""
    n = len(labels)
    return -sum(c / n * log2(c / n) for c in Counter(labels).values()) if n else 0.0


def gain(X: Sequence[Sequence[Hashable]], y: Sequence[Hashable], a: int) -> float:
    """Information gain of splitting (X, y) on attribute a, in bits. Cost: O(n)."""
    groups: dict = {}
    for xi, yi in zip(X, y):
        groups.setdefault(xi[a], []).append(yi)
    n = len(y)
    return entropy(y) - sum(len(g) / n * entropy(g) for g in groups.values())


def majority(y: Sequence[Hashable]) -> Hashable:
    """The most frequent label; a tie goes to the smallest label."""
    c = Counter(y)
    return max(sorted(c), key=lambda v: c[v])


def id3(X: Sequence[Sequence[Hashable]], y: Sequence[Hashable], attributes: Sequence[int],
        values: dict | None = None, default: Hashable = None) -> Any:
    """Grow the ID3 tree of (X, y) using the given attribute indices.

    values[a] lists the values of attribute a that get a branch; by default
    the values seen in X. A gain tie goes to the attribute listed first.
    The recursion depth is at most len(attributes) + 1.
    Cost: O(d n) counting per level of the tree and at most d levels.
    """
    if values is None:
        values = {a: sorted(set(x[a] for x in X)) for a in attributes}
    if not y:  # @line L1
        return ("leaf", default)  # @line L1
    if len(set(y)) == 1:  # @line L2
        return ("leaf", y[0])  # @line L2
    m = majority(y)  # @line L3
    if not attributes:  # @line L4
        return ("leaf", m)  # @line L4
    best = max(attributes, key=lambda a: (gain(X, y, a), -attributes.index(a)))  # @line L5
    rest = [a for a in attributes if a != best]
    children = {}  # @line L6
    for v in values[best]:  # @line L7
        idx = [i for i, xi in enumerate(X) if xi[best] == v]
        children[v] = id3([X[i] for i in idx], [y[i] for i in idx], rest, values, m)  # @line L8
    return ("node", best, children, m)  # @line L9


def predict(tree: Any, x: Sequence[Hashable]) -> Hashable:
    """Follow the branches of x to a leaf. Cost: O(depth)."""
    while tree[0] == "node":
        _, a, children, default = tree
        if x[a] not in children:
            return default
        tree = children[x[a]]
    return tree[1]


def id3_windowed(X, y, attributes, window: int, increment: int, rng: random.Random) -> Any:
    """Quinlan's windowing: grow a tree on a random window of the examples,
    add some of the examples it misclassifies, and repeat until it classifies
    all examples or every misclassified example is already in the window.
    """
    values = {a: sorted(set(x[a] for x in X)) for a in attributes}
    order = list(range(len(y)))
    rng.shuffle(order)
    win = set(order[:window])
    while True:
        idx = sorted(win)
        tree = id3([X[i] for i in idx], [y[i] for i in idx], list(attributes), values, majority(y))
        wrong = [i for i in order if i not in win and predict(tree, X[i]) != y[i]]
        if not wrong:
            return tree
        win.update(wrong[:increment])
