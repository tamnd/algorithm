# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-deepening-search/. The authors are listed in prov/76CY83.jsonl.

import itertools
import sys
from collections.abc import Callable, Hashable, Iterable
from typing import Optional, TypeVar, Union

S = TypeVar("S", bound=Hashable)

CUTOFF = "cutoff"


def _depth_limited(
    start: S,
    successors: Callable[[S], Iterable[S]],
    is_goal: Callable[[S], bool],
    limit: int,
    trace: Optional[list],
) -> Union[list[S], str, None]:
    """Depth-limited search with a check for cycles on the current path."""
    on_path = {start}

    def dls(s: S, k: int) -> Union[list[S], str, None]:
        if trace is not None:
            trace.append(s)
        if is_goal(s):
            return [s]
        if k == 0:
            return CUTOFF if any(t not in on_path for t in successors(s)) else None
        cut = False
        for t in successors(s):
            if t in on_path:
                continue
            on_path.add(t)
            r = dls(t, k - 1)
            on_path.discard(t)
            if isinstance(r, list):
                r.append(s)
                return r
            if r == CUTOFF:
                cut = True
        return CUTOFF if cut else None

    r = dls(start, limit)
    if isinstance(r, list):
        r.reverse()
    return r


def iterative_deepening_search(
    start: S,
    successors: Callable[[S], Iterable[S]],
    is_goal: Callable[[S], bool],
    max_depth: Optional[int] = None,
    trace: Optional[list] = None,
) -> Union[list[S], str, None]:
    """Run depth-limited search with the limits 0, 1, 2, ... until it does not cut off.

    Precondition: successors(s) is finite for each s. Returns a path
    [start, ..., goal] with the fewest actions, or None (failure) when no goal
    can be reached. The check for cycles on the current path makes the search
    stop on each finite space. On an infinite space with no goal it runs for
    ever unless max_depth is given; then CUTOFF is returned after the limit
    max_depth. If trace is a list, each goal-tested state is appended to it.
    Cost: O(b^d) goal tests and O(d) stack frames, for branching factor b and
    goal depth d.
    """
    old = sys.getrecursionlimit()
    try:
        for limit in itertools.count():  # @line L1
            if max_depth is not None and limit > max_depth:
                return CUTOFF
            sys.setrecursionlimit(max(old, limit + 100))
            r = _depth_limited(start, successors, is_goal, limit, trace)  # @line L2
            if r != CUTOFF:  # @line L3
                return r
    finally:
        sys.setrecursionlimit(old)
    return None
