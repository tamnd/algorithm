# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hartigan-algorithm/. The authors are listed in prov/HBJAYD.jsonl.

"""Hartigan's algorithm for unit-cost small parsimony on a rooted tree of any degree.

A tree is given by `children`, a list in which `children[v]` is the list of
the children of node v, and by the index of the root. A node with no
children is a leaf. `leaf_state[v]` is the observed state of leaf v.
"""

from collections import Counter
from collections.abc import Hashable, Mapping, Sequence
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


def hartigan(
    children: Sequence[Sequence[int]], root: int, leaf_state: Mapping[int, S]
) -> tuple[int, dict[int, frozenset[S]], dict[int, frozenset[S]], dict[int, frozenset[S]]]:
    """Run Hartigan's two passes for one character with unit costs.

    Precondition: each leaf has a state in `leaf_state`. Internal nodes may
    have any positive number of children. Returns the parsimony score, the
    upper sets U, the lower sets L, and the final sets F: F[v] is the set of
    all states that v has in at least one most parsimonious labeling.
    Only states that occur at the leaves can occur in U and F, so the
    alphabet is the set of leaf states.
    Cost: O(n k) time for n nodes and k states.
    """
    alphabet = frozenset(leaf_state[v] for v in range(len(children)) if not children[v] and v in leaf_state)
    order = postorder(children, root)
    upper: dict[int, frozenset[S]] = {}
    lower: dict[int, frozenset[S]] = {}
    score = 0  # @line L1
    for v in order:  # @line L2
        if not children[v]:
            upper[v], lower[v] = frozenset([leaf_state[v]]), frozenset()  # @line L3
            continue
        count: Counter[S] = Counter()
        for w in children[v]:  # @line L4
            count.update(upper[w])
        best = max(count.values())  # @line L5
        upper[v] = frozenset(a for a in alphabet if count[a] == best)  # @line L6
        lower[v] = frozenset(a for a in alphabet if count[a] == best - 1)
        score += len(children[v]) - best  # @line L7
    final: dict[int, frozenset[S]] = {root: upper[root]}  # @line L8
    for v in reversed(order):  # parents come before their children
        for w in children[v]:  # @line L9
            if not children[w]:
                final[w] = upper[w]  # @line L10
                continue
            f = final[v] & (upper[w] | lower[w])  # @line L11
            if not final[v] <= upper[w]:
                f = f | upper[w]  # @line L12
            final[w] = f
    return score, upper, lower, final  # @line L13
