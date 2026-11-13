# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/limited-discrepancy-search/. The authors are listed in prov/Y4C1CW.jsonl.

"""Limited discrepancy search (Harvey and Ginsberg 1995) and Korf's ILDS (1996).

A tree is given by children(node), which lists the children in the order
that the heuristic prefers. Taking a child other than the first is a
discrepancy. In a tree with more than two children this code counts each
such choice as one discrepancy.

lds() runs iterations k = 0, 1, 2, ...; iteration k visits each leaf whose
path has at most k discrepancies, once. ilds() visits in iteration k each
leaf at the full depth whose path has exactly k discrepancies; it needs the
depth of the tree. The probes recurse, so the depth of the tree must stay
small (well under the Python limit of about 1000 frames).

lds_path() applies LDS to a search problem: children are the successors not
on the current path, sorted by h, and the depth is limited to max_depth.
"""

from collections.abc import Callable, Hashable, Iterable
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LdsResult:
    goal_path: Optional[list]  # nodes from the root to the goal found, or None
    iteration: Optional[int]  # k of the iteration that found it
    leaves: list = field(default_factory=list)  # leaves[k] = leaves visited by iteration k
    visited: int = 0  # nodes visited, over all iterations


def lds(root, children: Callable, is_goal: Callable, max_k: int) -> LdsResult:
    """Harvey and Ginsberg's LDS with discrepancy limits 0 to max_k."""
    res = LdsResult(None, None)

    def probe(node, k, trail):  # @line L4
        res.visited += 1
        if is_goal(node):  # @line L5
            return trail + [node]
        kids = list(children(node))
        if not kids:  # @line L6
            res.leaves[-1].append(node)
            return None
        if k == 0:  # @line L7
            return probe(kids[0], 0, trail + [node])
        for kid in kids[1:]:  # @line L8
            r = probe(kid, k - 1, trail + [node])
            if r is not None:
                return r
        return probe(kids[0], k, trail + [node])  # @line L9

    for k in range(max_k + 1):  # @line L1
        res.leaves.append([])
        r = probe(root, k, [])  # @line L2
        if r is not None:  # @line L3
            res.goal_path, res.iteration = r, k
            return res
    return res


def ilds(root, children: Callable, is_goal: Callable, depth: int) -> LdsResult:
    """Korf's improved LDS on a tree whose leaves are all at the given depth."""
    res = LdsResult(None, None)

    def probe(node, k, rest, trail):
        res.visited += 1
        if is_goal(node):
            return trail + [node]
        kids = list(children(node))
        if not kids:
            res.leaves[-1].append(node)
            return None
        if rest > k:  # room left to agree with the heuristic
            r = probe(kids[0], k, rest - 1, trail + [node])
            if r is not None:
                return r
        if k > 0:
            for kid in kids[1:]:
                r = probe(kid, k - 1, rest - 1, trail + [node])
                if r is not None:
                    return r
        return None

    for k in range(depth + 1):
        res.leaves.append([])
        r = probe(root, k, depth, [])
        if r is not None:
            res.goal_path, res.iteration = r, k
            return res
    return res


def lds_path(
    start: Hashable,
    successors: Callable[[Hashable], Iterable[tuple[Hashable, int]]],
    is_goal: Callable[[Hashable], bool],
    h: Callable[[Hashable], int],
    max_depth: int,
) -> LdsResult:
    """LDS on a search problem; the result path is a list of states.

    A node is a tuple of states from the start; children skip states that
    are already on the path, so each probe is a finite tree. The search
    stops at the first goal found and runs at most max_depth + 1 iterations.
    """

    def children(node):
        if len(node) - 1 >= max_depth:  # a node at the depth limit is a leaf
            return []
        on_path = set(node)
        kids = [(h(m), i, m) for i, (m, _) in enumerate(successors(node[-1])) if m not in on_path]
        kids.sort()
        return [node + (m,) for _, _, m in kids]

    r = lds((start,), children, lambda node: is_goal(node[-1]), max_depth)
    if r.goal_path is not None:
        r.goal_path = list(r.goal_path[-1])
    return r
