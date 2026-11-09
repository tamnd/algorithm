# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nested-depth-first-search/. The authors are listed in prov/CRQF4Q.jsonl.

"""Nested depth-first search (Courcoubetis, Vardi, Wolper and Yannakakis 1992).

The input is a Büchi automaton, or a product of a system with one, given as a
graph: a list of initial states, a dict succ from each state to the list of its
successors, and a set of accepting states. The search returns an accepting
lasso (stem, cycle): stem is a path from an initial state to cycle[0], cycle[0]
is accepting, and cycle is a cycle (the last state has cycle[0] as a successor).
It returns None when no accepting cycle is reachable.

Each state is entered at most once by the outer search and at most once by all
inner searches together, so the time is O(|V| + |E|) and the extra space is two
bits per state plus the two stacks. The code uses explicit stacks, so the depth
of the graph does not hit the Python recursion limit.

With early=True the inner search also stops when it reaches a state on the
outer stack (the improvement of Holzmann, Peled and Yannakakis 1996).
"""

from collections.abc import Hashable, Iterable, Mapping

_END = object()


def nested_depth_first_search(
    init: Iterable[Hashable],
    succ: Mapping[Hashable, list],
    accepting: set,
    early: bool = False,
):
    """Return an accepting lasso (stem, cycle), or None if the language is empty."""
    visited: set = set()  # @line L1
    flagged: set = set()
    on_outer: set = set()
    for s0 in init:  # @line L2
        if s0 in visited:
            continue
        visited.add(s0)  # @line L5
        on_outer.add(s0)
        outer = [(s0, iter(succ.get(s0, ())))]
        while outer:  # @line L3
            s, it = outer[-1]
            t = next(it, _END)  # @line L6
            if t is not _END:
                if t not in visited:  # @line L7
                    visited.add(t)
                    on_outer.add(t)
                    outer.append((t, iter(succ.get(t, ()))))
                continue
            if s in accepting:  # @line L8
                seed = s  # @line L9
                found = _inner(seed, succ, flagged, on_outer if early else None)  # @line L10
                if found is not None:
                    cycle, a = found
                    path = [v for v, _ in outer]
                    if a is not None:
                        # The inner path ends next to an ancestor a of the seed: close
                        # the cycle with the outer stack from a down to the seed.
                        cycle = cycle + path[path.index(a) : -1]
                    return path[:-1], cycle
            on_outer.discard(s)  # @line L11
            outer.pop()
    return None  # @line L4


def _inner(seed, succ, flagged, on_outer):
    """Inner search from seed. Return (path, None), where path is seed ... x and x has
    seed as a successor, or None when no such path exists.

    With on_outer given, it may also return (path, a), where the last state of path
    has a as a successor and a is on the outer stack.
    """
    stack = [(seed, iter(succ.get(seed, ())))]
    while stack:
        x, it = stack[-1]
        t = next(it, _END)  # @line L12
        if t is _END:
            stack.pop()
            continue
        if t == seed:  # @line L13
            return [v for v, _ in stack], None
        if on_outer is not None and t in on_outer:
            return [v for v, _ in stack], t
        if t not in flagged:  # @line L14
            flagged.add(t)  # @line L15
            stack.append((t, iter(succ.get(t, ()))))  # @line L16
    return None  # @line L17
