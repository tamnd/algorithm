# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expectiminimax/. The authors are listed in prov/8K5D18.jsonl.

"""Expectiminimax: the value of a finite game tree with MAX, MIN and chance nodes.

A node is one of
    ("leaf", value)
    ("max", [child, ...])
    ("min", [child, ...])
    ("chance", [(probability, child), ...])
with values and probabilities given as int or Fraction, so that the result is exact.
"""

from fractions import Fraction
from typing import Any

Node = tuple[str, Any]


def expectiminimax(root: Node, counter: list[int] | None = None) -> Fraction:
    """Return the expectiminimax value of the tree rooted at root.

    Precondition: every MAX and MIN node has at least one child, every chance
    node has outcomes with probabilities >= 0 that sum to 1.
    Cost: one visit per node, so O(N) time for a tree with N nodes, which is
    O((b k)^d) for d rounds of a decision with b moves and a chance event with
    k outcomes; O(depth) extra space for the explicit stack. If counter is
    given, counter[0] is increased by the number of leaves evaluated.
    """
    # Each frame is [node, index of the next child, accumulated value].
    stack: list[list[Any]] = [[root, 0, None]]
    result: Fraction = Fraction(0)
    while stack:
        frame = stack[-1]
        kind, data = frame[0]
        if kind == "leaf":
            if counter is not None:
                counter[0] += 1
            value = Fraction(data)  # @line L1
            stack.pop()
        else:
            children = data
            i = frame[1]
            if i < len(children):
                frame[1] = i + 1
                child = children[i][1] if kind == "chance" else children[i]
                stack.append([child, 0, None])
                continue
            value = frame[2]
            stack.pop()
        if not stack:
            result = value
            break
        parent = stack[-1]
        pkind, pdata = parent[0]
        if pkind == "max":
            parent[2] = value if parent[2] is None else max(parent[2], value)  # @line L2
        elif pkind == "min":
            parent[2] = value if parent[2] is None else min(parent[2], value)  # @line L3
        else:
            p = Fraction(pdata[parent[1] - 1][0])
            parent[2] = (Fraction(0) if parent[2] is None else parent[2]) + p * value  # @line L4
    return result


def best_move(root: Node) -> int:
    """Return the index of a best move at a MAX or MIN root (the first one on ties).

    Precondition: root is a MAX or MIN node. Cost: as expectiminimax on the whole tree.
    """
    kind, children = root
    if kind not in ("max", "min"):
        raise ValueError("the root must be a MAX or MIN node")
    values = [expectiminimax(c) for c in children]
    target = max(values) if kind == "max" else min(values)
    return values.index(target)


def map_leaves(root: Node, f) -> Node:
    """Return a copy of the tree with every leaf value v replaced by f(v). Cost O(N)."""
    kind, data = root
    if kind == "leaf":
        return ("leaf", f(data))
    if kind == "chance":
        return ("chance", [(p, map_leaves(c, f)) for p, c in data])
    return (kind, [map_leaves(c, f) for c in data])
