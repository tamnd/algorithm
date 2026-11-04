# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-broadening/. The authors are listed in prov/5WXKC7.jsonl.

import itertools
from collections.abc import Callable, Hashable, Sequence
from typing import Optional, TypeVar

S = TypeVar("S", bound=Hashable)


def iterative_broadening(
    start: S,
    successors: Callable[[S], Sequence[S]],
    is_goal: Callable[[S], bool],
    first_cutoff: int = 2,
    trace: Optional[list] = None,
) -> Optional[list[S]]:
    """Depth-first search with a breadth cutoff c = first_cutoff, first_cutoff + 1, ...

    Precondition: the tree of paths from start is finite (each path ends), and
    first_cutoff >= 1. Each run looks only at the first c children of each
    node, in the order given by successors. Returns a path [start, ..., goal]
    or None when the tree holds no goal. If trace is a list, each goal-tested
    state is appended to it.
    Cost: at most sum over c of the nodes of the tree cut to breadth c; for a
    uniform tree of branching b and depth d, at most (1 + b/(d+1)) b^d fringe
    nodes over all runs. Space: O(depth) stack frames.
    """
    if first_cutoff < 1:
        raise ValueError("the first breadth cutoff must be at least 1")
    pruned = False

    def bounded(s: S, c: int) -> Optional[list[S]]:
        nonlocal pruned
        if trace is not None:
            trace.append(s)
        if is_goal(s):  # @line L6
            return [s]
        children = successors(s)  # @line L7
        if len(children) > c:  # @line L8
            pruned = True
        for t in children[:c]:  # @line L9
            r = bounded(t, c)  # @line L10
            if r is not None:  # @line L11
                r.append(s)
                return r
        return None  # @line L12

    for c in itertools.count(first_cutoff):  # @line L1
        pruned = False  # @line L2
        r = bounded(start, c)  # @line L3
        if r is not None:  # @line L4
            r.reverse()
            return r
        if not pruned:  # @line L5
            return None
    return None
