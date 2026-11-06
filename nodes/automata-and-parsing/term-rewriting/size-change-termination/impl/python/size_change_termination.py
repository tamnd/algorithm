# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/size-change-termination/. The authors are listed in prov/WBRKWD.jsonl.

"""Size-change termination: the closure algorithm of Lee, Jones and Ben-Amram.

A size-change graph G = (f, g, arcs) describes one call from function f to
function g. An arc (i, j, True) says that argument j of the call is strictly
smaller than parameter i of f; an arc (i, j, False) says that it is smaller or
equal. Parameters are numbered from 0.
"""

from dataclasses import dataclass
from typing import Hashable, Iterable

Arc = tuple[int, int, bool]


@dataclass(frozen=True)
class Graph:
    """A size-change graph from function src to function dst."""

    src: Hashable
    dst: Hashable
    arcs: frozenset[Arc]


@dataclass(frozen=True)
class Result:
    """The verdict, with a witness when the graphs are not size-change terminating.

    witness is an idempotent graph f -> f of the closure with no strict arc
    i -> i, and walk lists the indices of the input graphs whose composition,
    in this order, is the witness.
    """

    terminates: bool
    witness: Graph | None = None
    walk: tuple[int, ...] | None = None


def make_graph(src: Hashable, dst: Hashable, arcs: Iterable[Arc]) -> Graph:
    """Build a graph, keeping one arc per pair (i, j), strict if any is strict. O(arcs)."""
    best: dict[tuple[int, int], bool] = {}
    for i, j, strict in arcs:
        best[(i, j)] = best.get((i, j), False) or bool(strict)
    return Graph(src, dst, frozenset((i, j, s) for (i, j), s in best.items()))


def compose(g: Graph, h: Graph) -> Graph:
    """Return g;h, the graph of the call g followed by the call h.

    Requires g.dst == h.src. There is an arc i -> k if some j has i -> j in g
    and j -> k in h; it is strict if one of the two arcs is strict.
    Cost O(|g.arcs| * |h.arcs|).
    """
    if g.dst != h.src:
        raise ValueError("graphs do not compose")
    by_src: dict[int, list[tuple[int, bool]]] = {}
    for j, k, s in h.arcs:
        by_src.setdefault(j, []).append((k, s))
    return make_graph(
        g.src,
        h.dst,
        ((i, k, s1 or s2) for i, j, s1 in g.arcs for k, s2 in by_src.get(j, ())),
    )


def size_change_terminates(graphs: list[Graph]) -> Result:
    """Decide size-change termination of a finite set of size-change graphs.

    Computes the closure S of the graphs under composition along walks of the
    call graph, then checks every idempotent graph f -> f in S for a strict
    arc i -> i. With F functions of at most p parameters, |S| is at most
    F^2 * 3^(p^2), and the time is O(|S| * |graphs| * p^4) in the worst case;
    the problem is PSPACE-complete, so an exponential closure is expected in
    the worst case.
    """
    base = [make_graph(g.src, g.dst, g.arcs) for g in graphs]
    walks: dict[Graph, tuple[int, ...]] = {}
    work: list[Graph] = []
    for idx, g in enumerate(base):  # @line L1
        if g not in walks:
            walks[g] = (idx,)
            work.append(g)
    while work:  # @line L2
        g = work.pop()  # @line L3
        for idx, h in enumerate(base):  # @line L4
            if h.src != g.dst:
                continue
            k = compose(g, h)  # @line L5
            if k not in walks:  # @line L6
                walks[k] = walks[g] + (idx,)
                work.append(k)
    for g, walk in walks.items():  # @line L7
        if g.src == g.dst and compose(g, g) == g:  # @line L8
            if not any(i == j and s for i, j, s in g.arcs):  # @line L9
                return Result(False, g, walk)
    return Result(True)  # @line L10
