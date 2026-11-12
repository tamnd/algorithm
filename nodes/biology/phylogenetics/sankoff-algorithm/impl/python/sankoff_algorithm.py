# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sankoff-algorithm/. The authors are listed in prov/AZ0KEP.jsonl.

"""Sankoff's dynamic program for weighted small parsimony on a rooted tree.

A tree is given by `children`, a list in which `children[v]` is the list of
the children of node v, and by the index of the root. A node with no
children is a leaf. `leaf_state[v]` is the observed state of leaf v.
`cost[a][b]` is the cost of a change from state a in a parent to state b in
a child. It may be `math.inf` for a forbidden change.
"""

import math
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


def sankoff(
    children: Sequence[Sequence[int]],
    root: int,
    leaf_state: Mapping[int, S],
    alphabet: Sequence[S],
    cost: Mapping[S, Mapping[S, float]],
) -> tuple[float, dict[int, dict[S, float]], dict[int, S]]:
    """Run Sankoff's two passes for one character.

    Precondition: every leaf state is in `alphabet`, and `cost[a][b]` is
    defined for all states a and b (non-negative, or math.inf). The tree may
    have nodes of any degree. Returns the least total cost over all labelings
    of the internal nodes, the table C with C[v][a] the least cost of the
    subtree of v when v has state a, and one optimal labeling. Ties are
    broken by the order of `alphabet`. The score is math.inf when no
    labeling has a finite cost.
    Cost: O(n k^2) time and O(n k) space for n nodes and k states.
    """
    order = postorder(children, root)
    table: dict[int, dict[S, float]] = {}
    for v in order:  # @line L1
        if not children[v]:
            table[v] = {a: (0 if a == leaf_state[v] else math.inf) for a in alphabet}  # @line L2
            continue
        row: dict[S, float] = {}
        for a in alphabet:  # @line L3
            row[a] = sum(
                min(cost[a][b] + table[w][b] for b in alphabet) for w in children[v]
            )  # @line L4
        table[v] = row
    score = min(table[root][a] for a in alphabet)  # @line L5
    label: dict[int, S] = {root: next(a for a in alphabet if table[root][a] == score)}  # @line L6
    for v in reversed(order):  # parents come before their children
        for w in children[v]:  # @line L7
            p = label[v]
            label[w] = min(alphabet, key=lambda b: cost[p][b] + table[w][b])  # @line L8
    return score, table, label  # @line L9


def labeling_cost(
    children: Sequence[Sequence[int]],
    label: Mapping[int, S],
    cost: Mapping[S, Mapping[S, float]],
) -> float:
    """Sum cost[label of parent][label of child] over all edges of the tree."""
    return sum(cost[label[v]][label[w]] for v, ws in enumerate(children) for w in ws)


def unit_cost(alphabet: Sequence[S]) -> dict[S, dict[S, int]]:
    """The cost matrix of Fitch parsimony: 0 on the diagonal and 1 elsewhere."""
    return {a: {b: int(a != b) for b in alphabet} for a in alphabet}
