# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/depth-limited-search/. The authors are listed in prov/T1ZWEX.jsonl.

import sys
from collections.abc import Callable, Hashable, Iterable
from typing import Optional, TypeVar, Union

S = TypeVar("S", bound=Hashable)

CUTOFF = "cutoff"


def depth_limited_search(
    start: S,
    successors: Callable[[S], Iterable[S]],
    is_goal: Callable[[S], bool],
    limit: int,
    check_cycles: bool = True,
    trace: Optional[list] = None,
) -> Union[list[S], str, None]:
    """Depth-first search that does not go below depth `limit`.

    Precondition: limit >= 0, and successors(s) is finite for each s.
    Returns a path [start, ..., goal] with at most `limit` actions, or CUTOFF
    when no goal was found but the limit cut off some path, or None (failure)
    when no goal can be reached from start at all. With check_cycles, a child
    whose state is already on the current path is skipped. If trace is a list,
    each state passed to the goal test is appended to it.
    Cost: O(b^limit) goal tests and successor calls for branching factor b,
    O(limit) stack frames.
    """
    if limit < 0:
        raise ValueError("the depth limit must be non-negative")
    on_path: set = {start}  # @line L1
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old, limit + 100))

    def allowed(s: S) -> bool:
        return not check_cycles or s not in on_path

    def dls(s: S, k: int) -> Union[list[S], str, None]:
        if trace is not None:
            trace.append(s)
        if is_goal(s):  # @line L3
            return [s]
        if k == 0:  # @line L4
            if any(allowed(t) for t in successors(s)):  # @line L5
                return CUTOFF
            return None  # @line L6
        cut = False  # @line L7
        for t in successors(s):  # @line L8
            if not allowed(t):
                continue
            on_path.add(t)  # @line L9
            r = dls(t, k - 1)  # @line L10
            on_path.discard(t)  # @line L11
            if isinstance(r, list):  # @line L12
                r.append(s)
                return r
            if r == CUTOFF:  # @line L13
                cut = True
        return CUTOFF if cut else None  # @line L14

    try:
        r = dls(start, limit)  # @line L2
    finally:
        sys.setrecursionlimit(old)
    if isinstance(r, list):
        r.reverse()
    return r
