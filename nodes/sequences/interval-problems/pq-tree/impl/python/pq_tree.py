# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pq-tree/. The authors are listed in prov/HCBMN4.jsonl.
"""PQ-trees with a simple REDUCE.

A tree is made of nodes ("leaf", x), ("P", [children]) and ("Q", [children]).
A P-node allows any order of its children, a Q-node only the given order or
its reverse. The frontier of a tree is its leaves from left to right; the tree
represents every frontier obtained by these reorderings.

reduce(tree, s) returns a tree for the frontiers of tree in which the set s
is consecutive, or None if there are none. It applies the templates of Booth
and Lueker by one recursion over the pertinent part of the tree, in O(n) time
per call (the original bottom-up version runs in O(|s|) amortized time).
"""

from itertools import permutations
from typing import Iterable, Optional

EMPTY, FULL, PARTIAL = "empty", "full", "partial"


def leaf(x):
    return ("leaf", x)


def universal(items: Iterable) -> tuple:
    """The tree that allows every order of the items."""
    items = list(items)
    if len(items) == 1:
        return leaf(items[0])
    return ("P", [leaf(x) for x in items])


def leaves(t) -> list:
    if t[0] == "leaf":
        return [t[1]]
    out = []
    for c in t[1]:
        out.extend(leaves(c))
    return out


def _make(kind, kids):
    """Build a node, normalizing: one child -> that child, Q of two -> P."""
    if len(kids) == 1:
        return kids[0]
    if kind == "Q" and len(kids) == 2:
        kind = "P"
    return (kind, kids)


def _group(kids):
    """A P-node over kids (or the single kid), or None when kids is empty."""
    if not kids:
        return None
    return _make("P", kids)


def _count(t, s, memo):
    """Store (leaves of t in s, leaves of t) by id(t); return the pair."""
    if t[0] == "leaf":
        pair = (1 if t[1] in s else 0, 1)
    else:
        k = size = 0
        for c in t[1]:
            a, b = _count(c, s, memo)
            k, size = k + a, size + b
        pair = (k, size)
    memo[id(t)] = pair
    return pair


def _label(t, memo):
    k, size = memo[id(t)]
    if k == 0:
        return EMPTY
    return FULL if k == size else PARTIAL


class _Fail(Exception):
    pass


def _singly(t, memo):
    """Arrange a partial node as a sequence: empty part left, full part right."""
    kind, kids = t
    labels = [_label(c, memo) for c in kids]
    if kind == "P":  # templates P4 and P5 for a non-root node  # @line L10
        empties = [c for c, l in zip(kids, labels) if l == EMPTY]
        fulls = [c for c, l in zip(kids, labels) if l == FULL]
        partials = [c for c, l in zip(kids, labels) if l == PARTIAL]
        if len(partials) > 1:  # @line L10
            raise _Fail
        seq = []
        if empties:
            seq.append(_group(empties))  # @line L11
        if partials:
            seq.extend(_singly(partials[0], memo))
        if fulls:
            seq.append(_group(fulls))
        return seq
    # Q-node: the labels must read E* [partial] F*, in one of the two directions
    for order in (list(range(len(kids))), list(range(len(kids) - 1, -1, -1))):
        ls = [labels[i] for i in order]
        rank = {EMPTY: 0, PARTIAL: 1, FULL: 2}
        if all(rank[a] <= rank[b] for a, b in zip(ls, ls[1:])) and ls.count(PARTIAL) <= 1:  # @line L12
            seq = []
            for i in order:
                if labels[i] == PARTIAL:
                    seq.extend(_singly(kids[i], memo))  # @line L13
                else:
                    seq.append(kids[i])
            return seq
    raise _Fail  # @line L12


def _root(t, memo):
    """Rearrange the pertinent root so that its full leaves are consecutive."""
    kind, kids = t
    labels = [_label(c, memo) for c in kids]
    if kind == "P":  # templates P2, P4, P6 at the root  # @line L5
        empties = [c for c, l in zip(kids, labels) if l == EMPTY]
        fulls = [c for c, l in zip(kids, labels) if l == FULL]
        partials = [c for c, l in zip(kids, labels) if l == PARTIAL]
        if len(partials) > 2:  # @line L5
            raise _Fail
        if not partials:
            return _make("P", empties + [_group(fulls)])  # @line L7
        seq = _singly(partials[0], memo)  # @line L6
        if fulls:
            seq.append(_group(fulls))
        if len(partials) == 2:
            seq.extend(reversed(_singly(partials[1], memo)))
        return _make("P", empties + [_make("Q", seq)])  # @line L7
    # Q-node: the non-empty children form a block, inner ones full
    nonempty = [i for i, l in enumerate(labels) if l != EMPTY]
    i, j = nonempty[0], nonempty[-1]
    if any(labels[x] == EMPTY for x in range(i, j + 1)):  # @line L8
        raise _Fail
    if any(labels[x] == PARTIAL for x in range(i + 1, j)):
        raise _Fail
    seq = []
    for x, c in enumerate(kids):
        if labels[x] == PARTIAL and x == i:
            seq.extend(_singly(c, memo))  # full part toward the block
        elif labels[x] == PARTIAL and x == j:
            seq.extend(reversed(_singly(c, memo)))
        else:
            seq.append(c)
    return _make("Q", seq)  # @line L9


def _reduce(t, s, memo):
    if t[0] == "leaf" or _label(t, memo) != PARTIAL:
        return t
    kids = t[1]
    touched = [x for x, c in enumerate(kids) if _label(c, memo) != EMPTY]
    if len(touched) == 1 and _label(kids[touched[0]], memo) == PARTIAL:  # @line L3
        # all of s lies below one child: the pertinent root is lower
        x = touched[0]
        new = list(kids)
        new[x] = _reduce(kids[x], s, memo)
        return (t[0], new)
    return _root(t, memo)  # @line L4


def reduce(tree, s) -> Optional[tuple]:
    """Restrict tree to the frontiers in which the set s is consecutive."""
    s = set(s)
    memo: dict = {}
    _count(tree, s, memo)  # @line L2
    if len(s) <= 1:  # @line L1
        return tree
    try:
        return _reduce(tree, s, memo)
    except _Fail:
        return None


def frontiers(t) -> set:
    """All frontiers that t represents (exponential; for testing)."""
    if t[0] == "leaf":
        return {(t[1],)}
    kind, kids = t
    subs = [frontiers(c) for c in kids]
    orders = permutations(range(len(kids))) if kind == "P" else [
        tuple(range(len(kids))), tuple(range(len(kids) - 1, -1, -1))]
    out = set()
    for order in orders:
        partial = {()}
        for i in order:
            partial = {p + f for p in partial for f in subs[i]}
        out |= partial
    return out


def consecutive_ones_order(universe, sets) -> Optional[list]:
    """An order of universe in which every set is consecutive, or None."""
    tree = universal(universe)
    for s in sets:
        tree = reduce(tree, s)
        if tree is None:
            return None
    return leaves(tree)
