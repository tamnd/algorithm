# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/beam-stack-search/. The authors are listed in prov/2Y0M90.jsonl.

"""Beam-stack search (Zhou and Hansen 2005) for unit action costs.

The search is a layered beam search in which layer i only admits successors
whose f = i + h lies in the range [fmin, fmax) of item i of the beam stack,
and below the cost U of the best solution found so far. When a layer has
more than `width` candidates, the code keeps those with f below the f of the
(width + 1)-th best candidate and sets fmax to that value. If this keeps no
candidate (all of the best ones tie), it keeps every candidate of the least
f and sets fmax to the next larger f: this tie rule is ours, and it makes
each range nonempty. When a layer is empty, the search backtracks: it pops
the items whose range reaches U, and moves the range of the top item to
[fmax, U). The search stops when the stack is empty; the best solution is
then optimal.

The layers are kept in memory, as in the paper, and they are the closed list
used for duplicate detection: a successor already in an earlier layer is
dropped. The code assumes unit costs and a consistent h.
"""

from collections.abc import Callable, Hashable, Iterable
from dataclasses import dataclass, field
from typing import Optional

INF = float("inf")


@dataclass
class SearchResult:
    path: Optional[list]  # best path found, or None
    cost: Optional[int]  # its cost, or None
    solutions: list = field(default_factory=list)  # (cost, path) of each improvement
    expanded: int = 0  # stored nodes whose successors were generated
    backtracks: int = 0  # times the range of a stack item moved
    peak_stored: int = 0  # largest number of states in the stored layers


def beam_stack_search(
    start: Hashable,
    successors: Callable[[Hashable], Iterable[tuple[Hashable, int]]],
    is_goal: Callable[[Hashable], bool],
    h: Callable[[Hashable], int],
    width: int,
    max_backtracks: int = 10**6,
) -> SearchResult:
    """Return an optimal path, with every improved solution on the way.

    Precondition: every action costs 1, h is consistent with h = 0 at goals,
    width >= 1 and the graph is finite.
    Cost: at most n stored layers of about `width` states each; the number of
    backtracks is finite but can be exponential in the depth.
    """
    if width < 1:
        raise ValueError("the width must be at least 1")
    res = SearchResult(None, None)
    if is_goal(start):
        res.path, res.cost = [start], 0
        res.solutions.append((0, [start]))
        return res
    U = INF  # @line L1
    layers = [[start]]  # @line L2
    parents = [{start: None}]
    layer_of = {start: 0}
    stack: list = []  # stack[i - 1] = [fmin, fmax] for layer i

    def path_to(m, p, i):
        out = [m]
        while i > 0:
            out.append(p)
            i -= 1
            p = parents[i][p]
        return out[::-1]

    while True:  # @line L3
        i = len(layers)
        if len(stack) < i:  # @line L4
            stack.append([0, U])
        fmin, fmax = stack[i - 1]
        cand: dict = {}  # @line L5
        for n in layers[i - 1]:
            if i - 1 + h(n) >= U:
                continue  # f(n) >= U, so every successor has f >= U as well
            res.expanded += 1
            for m, _ in successors(n):
                f = i + h(m)
                if m in layer_of or m in cand:
                    continue
                if fmin <= f < fmax and f < U:  # @line L6
                    cand[m] = (f, len(cand), n)
        goals = [m for m in cand if is_goal(m)]  # @line L7
        if goals:
            m = min(goals, key=lambda x: cand[x][1])
            U = i
            res.path, res.cost = path_to(m, cand[m][2], i), i
            res.solutions.append((i, res.path))
            keep: list = []
        else:
            order = sorted(cand, key=lambda x: (cand[x][0], cand[x][1]))
            keep = order
            if len(order) > width:  # @line L8
                cut = cand[order[width]][0]
                keep = [x for x in order if cand[x][0] < cut]
                if not keep:  # the tie rule of the docstring
                    low = cand[order[0]][0]
                    keep = [x for x in order if cand[x][0] == low]
                    higher = [cand[x][0] for x in order if cand[x][0] > low]
                    cut = min(higher) if higher else fmax
                stack[i - 1][1] = cut  # @line L9
        if keep:  # @line L10
            layers.append(keep)
            parents.append({x: cand[x][2] for x in keep})
            for x in keep:
                layer_of[x] = i
            res.peak_stored = max(res.peak_stored, len(layer_of))
            continue
        while stack and stack[-1][1] >= U:  # @line L11
            stack.pop()
        if not stack:  # @line L12
            return res
        res.backtracks += 1
        if res.backtracks > max_backtracks:
            raise RuntimeError("too many backtracks")
        stack[-1] = [stack[-1][1], U]  # @line L13
        top = len(stack)
        for layer in layers[top:]:  # @line L14
            for x in layer:
                del layer_of[x]
        del layers[top:]
        del parents[top:]
