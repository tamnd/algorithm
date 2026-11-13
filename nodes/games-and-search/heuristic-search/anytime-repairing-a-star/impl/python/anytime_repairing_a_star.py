# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anytime-repairing-a-star/. The authors are listed in prov/PYDPRD.jsonl.

"""ARA*, anytime repairing A* (Likhachev, Gordon and Thrun 2003).

The code follows the pseudocode of the paper and of the page. Each call
of improve_path is a weighted A* search with the weight eps that expands
each state at most once. A state whose g drops after it was expanded in the
current call goes to INCONS, and INCONS goes back to OPEN before the next
call, so the next search reuses the work of the earlier ones.

After each call the code reports the solution with the bound of the paper,
    eps' = min(eps, g(goal) / min over OPEN and INCONS of (g + h)).
The goal is never expanded, so once g(goal) is finite the goal is in OPEN
and the ratio is at least 1; the code still takes the max with 1 as a guard.
OPEN is a binary heap with lazy deletion. Ties in the key go to the larger
g, then first in, first out. Weights are Fractions, so keys are exact.
"""

import heapq
import itertools
from collections.abc import Callable, Hashable, Iterable, Sequence
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Optional, Union

Number = Union[int, Fraction]
INF = float("inf")


@dataclass
class Solution:
    eps: Fraction  # the weight of the call
    bound: Fraction  # eps': g(goal) <= bound * C*
    cost: Number  # g(goal) after the call
    path: list  # states from the start to the goal
    expansions: int  # expansions in this call


@dataclass
class AraResult:
    solutions: list = field(default_factory=list)  # one Solution per call, in order
    expanded: list = field(default_factory=list)  # all expansions, in order

    @property
    def best(self) -> Optional[Solution]:
        return self.solutions[-1] if self.solutions else None


def ara_star(
    start: Hashable,
    goal: Hashable,
    successors: Callable[[Hashable], Iterable[tuple[Hashable, Number]]],
    h: Callable[[Hashable], Number],
    schedule: Sequence[Number] = (3, 2, Fraction(3, 2), 1),
) -> AraResult:
    """Run ARA* with the weights of schedule, which must decrease to 1.

    Precondition: positive costs, finitely many successors per state, and a
    consistent h with h(goal) = 0. Every reported solution satisfies
    cost <= bound * C*, the costs never increase, and the last one is optimal.
    Cost: each call expands each state at most once, so it takes
    O(m log m) time, where m counts the successor pairs looked at.
    """
    sched = [Fraction(e) for e in schedule]
    if not sched or sched[-1] != 1 or any(a <= b for a, b in zip(sched, sched[1:])):
        raise ValueError("the schedule must decrease strictly and end with 1")
    res = AraResult()
    g: dict = {start: 0, goal: INF}  # @line L1
    if start == goal:
        g[goal] = 0
    parent: dict = {start: None}
    hv: dict = {}

    def hh(s):
        if s not in hv:
            hv[s] = h(s)
        return hv[s]

    seq = itertools.count()
    open_set: set = {start}  # @line L2
    closed: set = set()
    incons: set = set()
    state = {"eps": sched[0], "heap": []}

    def fvalue(s):
        return g[s] + state["eps"] * hh(s)

    def rebuild():
        state["heap"] = [(fvalue(s), -g[s], next(seq), s) for s in open_set]
        heapq.heapify(state["heap"])

    def min_open():
        heap = state["heap"]
        while heap:
            f, ng, _, s = heap[0]
            if s in open_set and -ng == g[s]:
                return f, s
            heapq.heappop(heap)  # a stale entry
        return INF, None

    def improve_path() -> int:
        count = 0
        while True:
            f, s = min_open()
            if s is None or not fvalue(goal) > f:  # @line L12
                return count
            heapq.heappop(state["heap"])  # @line L13
            open_set.discard(s)
            closed.add(s)
            res.expanded.append(s)
            count += 1
            for t, c in successors(s):  # @line L14
                if t not in g or g[t] > g[s] + c:  # @line L15
                    g[t] = g[s] + c  # @line L16
                    parent[t] = s
                    if t not in closed:  # @line L17
                        open_set.add(t)
                        heapq.heappush(state["heap"], (fvalue(t), -g[t], next(seq), t))
                    else:
                        incons.add(t)  # @line L18

    def report(count):
        low = min((g[s] + hh(s) for s in open_set | incons), default=INF)
        eps = state["eps"]
        if low == INF:
            bound = Fraction(1)
        elif low == 0:
            bound = eps
        else:
            bound = max(Fraction(1), min(eps, Fraction(g[goal]) / Fraction(low)))
        path, s = [], goal
        while s is not None:
            path.append(s)
            s = parent[s]
        res.solutions.append(Solution(eps, bound, g[goal], path[::-1], count))

    rebuild()
    count = improve_path()  # @line L3
    if g[goal] == INF:
        return res  # @line L4
    report(count)  # @line L5
    for eps in sched[1:]:
        if res.solutions[-1].bound <= 1:  # @line L6
            break
        state["eps"] = eps  # @line L7
        open_set |= incons  # @line L8
        incons.clear()
        rebuild()  # @line L9
        closed.clear()
        count = improve_path()  # @line L10
        report(count)  # @line L11
    return res
