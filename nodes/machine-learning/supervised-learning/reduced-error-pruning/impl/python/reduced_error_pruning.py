# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reduced-error-pruning/. The authors are listed in prov/QKQX68.jsonl.

"""Reduced-error pruning (Quinlan 1987) of a decision tree on a pruning set.

A node tests the categorical attribute attr and has a child for each value
in children; a case whose value has no child stops at the node. Every node
has a label, the majority class of the training cases that reached it, which
it predicts when it is a leaf or when a case stops at it. A pruned tree is
given by the set `cut` of node ids that are made leaves.
"""

from collections import Counter
from typing import Hashable, Sequence


class Node:
    __slots__ = ("id", "label", "attr", "children")

    def __init__(self, label, attr=None, children=None):
        self.id = 0
        self.label, self.attr, self.children = label, attr, dict(children or {})

    def is_leaf(self) -> bool:
        return not self.children


def number(root: Node) -> list:
    """Give the nodes preorder ids and return them in preorder."""
    out, stack = [], [root]
    while stack:
        t = stack.pop()
        t.id = len(out)
        out.append(t)
        stack.extend(reversed(list(t.children.values())))
    return out


def count_errors(root: Node, X, y) -> tuple:
    """wrong[t]: pruning cases that reach t with a class other than label(t);
    stop[t]: those among them that also stop at t (no branch for their value).
    Cost: O(m h) for m cases and depth h."""
    nodes = number(root)
    wrong, stop = [0] * len(nodes), [0] * len(nodes)
    for x, c in zip(X, y):  # @line L1
        t = root  # @line L1
        while True:  # @line L1
            wrong[t.id] += c != t.label  # @line L1
            nxt = t.children.get(x[t.attr]) if not t.is_leaf() else None  # @line L1
            if nxt is None:  # @line L1
                stop[t.id] += c != t.label  # @line L1
                break  # @line L1
            t = nxt  # @line L1
    return wrong, stop


def reduced_error_prune(root: Node, X, y) -> tuple:
    """Bottom-up reduced-error pruning. Returns (cut, errors): the smallest pruned
    tree with the fewest errors on (X, y), and that number of errors.
    A node is made a leaf when that does not increase the errors (ties prune).
    Cost: O(m h + |T|)."""
    wrong, stop = count_errors(root, X, y)
    cut: set = set()

    def prune(t: Node) -> int:
        if t.is_leaf():  # @line L3
            return wrong[t.id]  # @line L3
        sub = stop[t.id] + sum(prune(u) for u in t.children.values())  # @line L4
        if wrong[t.id] <= sub:  # @line L5
            cut.add(t.id)  # @line L5
            return wrong[t.id]  # @line L5
        return sub  # @line L6

    errors = prune(root)  # @line L2
    return cut, errors  # @line L2


def classify(root: Node, cut, x) -> Hashable:
    t = root
    while not (t.is_leaf() or t.id in cut):
        nxt = t.children.get(x[t.attr])
        if nxt is None:
            break
        t = nxt
    return t.label


def errors_of(root: Node, cut, X, y) -> int:
    return sum(classify(root, cut, x) != c for x, c in zip(X, y))


def _internal(t: Node, cut) -> list:
    if t.is_leaf() or t.id in cut:
        return []
    return [t] + [s for u in t.children.values() for s in _internal(u, cut)]


def _branch_errors(t: Node, cut, wrong, stop) -> int:
    if t.is_leaf() or t.id in cut:
        return wrong[t.id]
    return stop[t.id] + sum(_branch_errors(u, cut, wrong, stop) for u in t.children.values())


def quinlan_iterative(root: Node, X, y) -> set:
    """Quinlan's (1987) statement: replace a subtree by a leaf if that does not
    increase the errors on the pruning set and no subtree of it has the same
    property; repeat until no replacement qualifies."""
    wrong, stop = count_errors(root, X, y)
    cut: set = set()
    while True:
        ok = {t.id for t in _internal(root, cut) if wrong[t.id] <= _branch_errors(t, cut, wrong, stop)}
        lowest = [t for t in _internal(root, cut)
                  if t.id in ok and not any(s.id in ok for s in _internal(t, cut)[1:])]
        if not lowest:
            return cut
        cut.add(lowest[0].id)


def greedy_best_first(root: Node, X, y) -> set:
    """The variant in Mitchell (1997, Section 3.7.1.1): repeatedly prune the node
    whose removal most increases accuracy on the pruning set; stop when every
    removal would lower it. It can end with more errors than the bottom-up rule."""
    wrong, stop = count_errors(root, X, y)
    cut: set = set()
    while True:
        gains = [(_branch_errors(t, cut, wrong, stop) - wrong[t.id], -t.id, t) for t in _internal(root, cut)]
        gains = [g for g in gains if g[0] >= 0]
        if not gains:
            return cut
        cut.add(max(gains, key=lambda g: g[:2])[2].id)


def grow_id3(X, y, attrs: Sequence[int], idx=None) -> Node:
    """A small unpruned ID3 tree (information gain, one branch per value seen)."""
    from math import log2
    idx = list(range(len(y))) if idx is None else idx
    labels = [y[i] for i in idx]
    cnt = Counter(labels)
    label = max(sorted(cnt), key=lambda c: cnt[c])
    if len(cnt) == 1 or not attrs:
        return Node(label)

    def h(ls):
        n = len(ls)
        return -sum(v / n * log2(v / n) for v in Counter(ls).values())

    def gain(a):
        groups: dict = {}
        for i in idx:
            groups.setdefault(X[i][a], []).append(y[i])
        return h(labels) - sum(len(g) / len(idx) * h(g) for g in groups.values())

    a = max(attrs, key=lambda b: (gain(b), -list(attrs).index(b)))
    rest = [b for b in attrs if b != a]
    kids = {}
    for v in sorted({X[i][a] for i in idx}):
        kids[v] = grow_id3(X, y, rest, [i for i in idx if X[i][a] == v])
    return Node(label, a, kids)
