# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implication-graph/. The authors are listed in prov/2V1W4P.jsonl.

"""The implication graph of a CDCL solver.

The nodes are the true literals of the current partial assignment, plus a
conflict node kappa while a clause is false. A decision has no in-edges. A
literal l implied by a reason clause C has an edge from -q for each other
literal q of C. Each node has the decision level of its assignment. Literals
are nonzero ints in DIMACS style.
"""

from __future__ import annotations

from collections.abc import Sequence


class ImplicationGraph:
    """Implication graph over the variables 1..n.

    The trail lists the nodes in the order of assignment, which is a
    topological order of the graph. Costs: decide O(1), imply and conflict
    O(|C|), backjump O(number of removed nodes and edges), uips and
    first_uip_clause O(size of the conflict level and its in-edges).
    """

    def __init__(self, n: int) -> None:
        self.n = n
        self.trail: list[int] = []
        self.lim: list[int] = []  # lim[i] is the trail index where level i + 1 starts
        self.level: dict[int, int] = {}
        self.pos: dict[int, int] = {}
        self.preds: dict[int, list[int]] = {}
        self.kappa: list[int] | None = None  # predecessors of the conflict node

    def decision_level(self) -> int:
        return len(self.lim)

    def value(self, lit: int) -> int:
        """1 if lit is a node, -1 if -lit is a node, 0 if its variable is free."""
        return 1 if lit in self.level else -1 if -lit in self.level else 0

    def _add(self, lit: int, preds: list[int]) -> None:
        self.level[lit] = len(self.lim)
        self.pos[lit] = len(self.trail)
        self.preds[lit] = preds
        self.trail.append(lit)

    def decide(self, lit: int) -> None:
        """Open a new level with the decision lit. Precondition: lit is free
        and there is no conflict node."""
        if self.value(lit) != 0 or self.kappa is not None:
            raise ValueError("decide needs a free literal and no conflict")
        self.lim.append(len(self.trail))  # @line L1
        self._add(lit, [])  # @line L2

    def imply(self, lit: int, reason: Sequence[int]) -> None:
        """Add lit with the reason clause. Precondition: lit is free, lit is in
        reason, and every other literal of reason is false."""
        others = [q for q in reason if q != lit]
        if self.value(lit) != 0 or lit not in reason or any(self.value(q) != -1 for q in others):
            raise ValueError("imply needs a free literal and a reason that is unit on it")
        preds = [-q for q in others]  # @line L3 @line L4
        self._add(lit, preds)  # @line L5

    def conflict(self, clause: Sequence[int]) -> None:
        """Add the conflict node for a clause whose literals are all false."""
        if any(self.value(q) != -1 for q in clause):
            raise ValueError("conflict needs a false clause")
        self.kappa = [-q for q in clause]  # @line L6

    def backjump(self, b: int) -> None:
        """Remove the conflict node and every node of level above b."""
        if not 0 <= b <= len(self.lim):
            raise ValueError("bad level")
        self.kappa = None  # @line L7
        if b == len(self.lim):
            return
        cut = self.lim[b]
        for lit in self.trail[cut:]:
            del self.level[lit], self.pos[lit], self.preds[lit]
        del self.trail[cut:]
        del self.lim[b:]

    def uips(self) -> list[int]:
        """The unique implication points of the conflict level, the one
        closest to the conflict first. Precondition: a conflict node exists,
        its level d is at least 1, and every node of level d is reachable from
        the decision of level d."""
        if self.kappa is None:
            raise ValueError("no conflict")
        d = max((self.level[w] for w in self.kappa), default=0)
        if d == 0:
            raise ValueError("the conflict is at level 0")
        marked = {w for w in self.kappa if self.level[w] == d}  # @line L8
        count = len(marked)
        found: list[int] = []
        start = self.lim[d - 1]
        end = self.lim[d] if d < len(self.lim) else len(self.trail)
        for i in range(end - 1, start - 1, -1):  # @line L9
            v = self.trail[i]
            if v in marked:  # @line L10
                if count == 1:  # @line L11
                    found.append(v)
                count -= 1  # @line L12
                for w in self.preds[v]:  # @line L13
                    if self.level[w] == d and w not in marked:
                        marked.add(w)
                        count += 1
        return found  # @line L14

    def first_uip_clause(self) -> tuple[list[int], int]:
        """The first UIP clause and its backjump level. The clause holds the
        negation of the first UIP and the negations of the nodes of levels 1
        to d - 1 with an edge into the part between the first UIP and the
        conflict; level-0 nodes are left out because they are fixed."""
        if self.kappa is None:
            raise ValueError("no conflict")
        d = max((self.level[w] for w in self.kappa), default=0)
        if d == 0:
            raise ValueError("the conflict is at level 0")
        marked = {w for w in self.kappa if self.level[w] == d}
        lower = {w for w in self.kappa if 0 < self.level[w] < d}
        count = len(marked)
        i = len(self.trail) - 1
        while True:
            v = self.trail[i]
            i -= 1
            if v not in marked:
                continue
            if count == 1:
                clause = [-v] + sorted((-w for w in lower), key=lambda q: -self.level[-q])
                b = max((self.level[w] for w in lower), default=0)
                return clause, b
            count -= 1
            for w in self.preds[v]:
                if self.level[w] == d:
                    if w not in marked:
                        marked.add(w)
                        count += 1
                elif self.level[w] > 0:
                    lower.add(w)

    def check_invariant(self) -> bool:
        """Every node has the level of its trail segment, decisions start the
        levels and have no in-edges, every edge goes from an earlier node of a
        level that is not larger, and no variable has two nodes."""
        if len({abs(x) for x in self.trail}) != len(self.trail):
            return False
        starts = set(self.lim)
        for i, lit in enumerate(self.trail):
            lvl = sum(1 for s in self.lim if s <= i)
            if self.level[lit] != lvl or self.pos[lit] != i:
                return False
            if i in starts and self.preds[lit]:
                return False
            for w in self.preds[lit]:
                if w not in self.pos or self.pos[w] >= i or self.level[w] > lvl:
                    return False
        if self.kappa is not None and any(w not in self.pos for w in self.kappa):
            return False
        return len(self.level) == len(self.trail) == len(self.pos) == len(self.preds)
