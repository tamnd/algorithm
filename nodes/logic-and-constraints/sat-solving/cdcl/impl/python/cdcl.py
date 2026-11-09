# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cdcl/. The authors are listed in prov/H3D7MV.jsonl.

"""Conflict-driven clause learning (CDCL) for CNF satisfiability.

A clause is a list of nonzero ints in DIMACS style: v is the variable v and
-v is its negation. cdcl(n, clauses) returns a model as a list of n literals
(the i-th entry is i + 1 or -(i + 1)), or None when the formula has no model.

The solver uses two watched literals for unit propagation, first-UIP clause
learning with recursive minimization, non-chronological backjumping, VSIDS
decisions in a lazy binary heap, phase saving, Luby or glucose-style restarts,
and LBD-based reduction of the learned clauses. The worst case is exponential
in n, as for every known SAT algorithm.
"""

from __future__ import annotations

import heapq
from collections import deque
from collections.abc import Iterable, Sequence


def luby(i: int) -> int:
    """Return the i-th term (i >= 1) of 1, 1, 2, 1, 1, 2, 4, 1, 1, 2, ..."""
    if i < 1:
        raise ValueError("the Luby sequence starts at i = 1")
    while True:
        k = 1
        while (1 << k) - 1 < i:
            k += 1
        if i == (1 << k) - 1:
            return 1 << (k - 1)
        i -= (1 << (k - 1)) - 1


def _idx(lit: int) -> int:
    """Index of a literal in the watch lists: 2v for v and 2v + 1 for -v."""
    return 2 * lit if lit > 0 else -2 * lit + 1


class Solver:
    """A CDCL solver for one CNF formula over the variables 1..n.

    Precondition: each literal l of each clause has 1 <= |l| <= n.
    Options: restart is "luby", "glucose" or None; restart_unit scales the
    Luby sequence; reduce_first and reduce_inc set the conflicts between two
    reductions of the learned clauses (reduce_first=0 turns reduction off);
    minimize turns recursive clause minimization on or off.
    """

    def __init__(
        self,
        n: int,
        clauses: Iterable[Sequence[int]],
        *,
        restart: str | None = "luby",
        restart_unit: int = 100,
        reduce_first: int = 2000,
        reduce_inc: int = 300,
        minimize: bool = True,
        var_decay: float = 0.95,
        check: bool = False,
    ) -> None:
        self.n = n
        self.value = [0] * (n + 1)  # 1 true, -1 false, 0 unassigned
        self.level = [0] * (n + 1)
        self.reason = [-1] * (n + 1)  # index of the reason clause, -1 if none
        self.trail: list[int] = []
        self.trail_lim: list[int] = []  # trail index where each level starts
        self.qhead = 0
        self.clauses: list[list[int] | None] = []
        self.is_learned: list[bool] = []
        self.lbd: list[int] = []
        self.watches: list[list[int]] = [[] for _ in range(2 * n + 2)]
        self.activity = [0.0] * (n + 1)
        self.var_inc = 1.0
        self.var_decay = var_decay
        self.heap: list[tuple[float, int]] = [(0.0, v) for v in range(1, n + 1)]
        self.phase = [False] * (n + 1)
        self.seen = [False] * (n + 1)
        self.restart = restart
        self.restart_unit = restart_unit
        self.reduce_first = reduce_first
        self.reduce_inc = reduce_inc
        self.minimize = minimize
        self.check = check
        self.learned_log: list[list[int]] = []
        self.conflicts = 0
        self.restarts = 0
        self.reductions = 0
        self.ok = True
        for c in clauses:
            self.add_input_clause(c)

    # ------------------------------------------------------------ basics

    def val(self, lit: int) -> int:
        x = self.value[abs(lit)]
        return x if lit > 0 else -x

    def decision_level(self) -> int:
        return len(self.trail_lim)

    def enqueue(self, lit: int, reason: int) -> None:
        v = abs(lit)
        self.value[v] = 1 if lit > 0 else -1
        self.level[v] = len(self.trail_lim)
        self.reason[v] = reason
        self.trail.append(lit)

    def attach(self, c: list[int], learned: bool, lbd: int = 0) -> int:
        ci = len(self.clauses)
        self.clauses.append(c)
        self.is_learned.append(learned)
        self.lbd.append(lbd)
        self.watches[_idx(c[0])].append(ci)
        self.watches[_idx(c[1])].append(ci)
        return ci

    def add_input_clause(self, clause: Sequence[int]) -> None:
        c: list[int] = []
        for lit in clause:
            if lit == 0 or abs(lit) > self.n:
                raise ValueError(f"literal {lit} is out of range")
            if lit not in c:
                c.append(lit)
        if any(-lit in c for lit in c):
            return  # a tautology is always true
        if not c:
            self.ok = False
        elif len(c) == 1:
            if self.val(c[0]) == -1:
                self.ok = False
            elif self.val(c[0]) == 0:
                self.enqueue(c[0], -1)
        else:
            self.attach(c, False)

    def decide(self, lit: int) -> None:
        """Open a new decision level and assign lit (lit must be unassigned)."""
        self.trail_lim.append(len(self.trail))
        self.enqueue(lit, -1)

    # ------------------------------------------------- unit propagation

    def propagate(self) -> int | None:
        """Unit propagation with two watched literals.

        Returns the index of a clause that is false under the trail, or None
        when the trail is closed under unit propagation.
        """
        value, clauses, watches = self.value, self.clauses, self.watches
        while self.qhead < len(self.trail):
            p = self.trail[self.qhead]
            self.qhead += 1
            false_lit = -p
            ws = watches[_idx(false_lit)]
            i = j = 0
            while i < len(ws):
                ci = ws[i]
                i += 1
                c = clauses[ci]
                if c is None:
                    continue  # a deleted clause: drop its watch
                if c[0] == false_lit:
                    c[0], c[1] = c[1], c[0]
                other = c[0]
                x = value[abs(other)]
                if (x if other > 0 else -x) == 1:
                    ws[j] = ci
                    j += 1
                    continue
                moved = False
                for k in range(2, len(c)):
                    y = value[abs(c[k])]
                    if (y if c[k] > 0 else -y) != -1:
                        c[1], c[k] = c[k], c[1]
                        watches[_idx(c[1])].append(ci)
                        moved = True
                        break
                if moved:
                    continue
                ws[j] = ci
                j += 1
                if (x if other > 0 else -x) == -1:
                    while i < len(ws):
                        ws[j] = ws[i]
                        j += 1
                        i += 1
                    del ws[j:]
                    self.qhead = len(self.trail)
                    return ci
                self.enqueue(other, ci)
            del ws[j:]
        return None

    # ---------------------------------------------- conflict analysis

    def bump(self, v: int) -> None:
        self.activity[v] += self.var_inc
        if self.activity[v] > 1e100:
            for u in range(1, self.n + 1):
                self.activity[u] *= 1e-100
            self.var_inc *= 1e-100
            self.rebuild_heap()
        elif self.value[v] == 0:
            heapq.heappush(self.heap, (-self.activity[v], v))

    def rebuild_heap(self) -> None:
        self.heap = [(-self.activity[v], v) for v in range(1, self.n + 1) if self.value[v] == 0]
        heapq.heapify(self.heap)

    def analyze(self, confl: int) -> tuple[list[int], int, int]:
        """Return the first-UIP clause (asserting literal first), the backjump
        level and the LBD of the clause. The trail must hold a conflict at a
        decision level of at least 1."""
        seen, level, trail = self.seen, self.level, self.trail
        dl = len(self.trail_lim)
        learnt = [0]
        counter = 0
        p = 0
        index = len(trail) - 1
        ci = confl
        while True:
            c = self.clauses[ci]
            assert c is not None
            for q in c:
                v = abs(q)
                if v == abs(p) or seen[v] or level[v] == 0:
                    continue
                seen[v] = True
                self.bump(v)
                if level[v] >= dl:
                    counter += 1
                else:
                    learnt.append(q)
            while not seen[abs(trail[index])]:
                index -= 1
            p = trail[index]
            index -= 1
            seen[abs(p)] = False
            counter -= 1
            if counter == 0:
                break
            ci = self.reason[abs(p)]
        learnt[0] = -p
        to_clear = [abs(q) for q in learnt[1:]]
        if self.minimize:
            kept = [learnt[0]]
            for q in learnt[1:]:
                if self.reason[abs(q)] == -1 or not self.redundant(q, to_clear):
                    kept.append(q)
            learnt = kept
        for v in to_clear:
            seen[v] = False
        lbd = len({level[abs(q)] for q in learnt})
        if len(learnt) == 1:
            return learnt, 0, lbd
        m = max(range(1, len(learnt)), key=lambda i: level[abs(learnt[i])])
        learnt[1], learnt[m] = learnt[m], learnt[1]
        return learnt, level[abs(learnt[1])], lbd

    def redundant(self, q: int, to_clear: list[int]) -> bool:
        """True when q follows from the other marked literals and level 0,
        through the reasons (Sorensson and Biere 2009). Explicit stack."""
        seen, level, reason = self.seen, self.level, self.reason
        top = len(to_clear)
        stack = [abs(q)]
        while stack:
            v = stack.pop()
            c = self.clauses[reason[v]]
            assert c is not None
            for r in c:
                u = abs(r)
                if u == v or seen[u] or level[u] == 0:
                    continue
                if reason[u] == -1:
                    for w in to_clear[top:]:
                        seen[w] = False
                    del to_clear[top:]
                    return False
                seen[u] = True
                to_clear.append(u)
                stack.append(u)
        return True

    def cancel_until(self, b: int) -> None:
        """Backjump: undo every assignment of a level above b."""
        if len(self.trail_lim) <= b:
            return
        start = self.trail_lim[b]
        for i in range(len(self.trail) - 1, start - 1, -1):
            lit = self.trail[i]
            v = abs(lit)
            self.phase[v] = lit > 0  # phase saving
            self.value[v] = 0
            self.reason[v] = -1
            heapq.heappush(self.heap, (-self.activity[v], v))
        del self.trail[start:]
        del self.trail_lim[b:]
        self.qhead = len(self.trail)

    def pick_branch_lit(self) -> int:
        if len(self.heap) > 8 * self.n + 64:
            self.rebuild_heap()
        while self.heap:
            a, v = heapq.heappop(self.heap)
            if self.value[v] == 0 and -a == self.activity[v]:
                return v if self.phase[v] else -v
        raise AssertionError("no unassigned variable")

    # ------------------------------------------------ clause database

    def locked(self, ci: int) -> bool:
        c = self.clauses[ci]
        return c is not None and any(self.reason[abs(q)] == ci and self.val(q) == 1 for q in c)

    def reduce_db(self) -> None:
        """Delete the worse half of the learned clauses with LBD above 2 that
        are not the reason of an assigned literal."""
        cands = [
            ci
            for ci, c in enumerate(self.clauses)
            if c is not None and self.is_learned[ci] and self.lbd[ci] > 2 and not self.locked(ci)
        ]
        cands.sort(key=lambda ci: (-self.lbd[ci], -len(self.clauses[ci] or []), ci))
        for ci in cands[: len(cands) // 2]:
            self.clauses[ci] = None  # watches are dropped lazily in propagate
        self.reductions += 1

    def check_watches(self) -> bool:
        """Each live clause of length >= 2 is watched by its first two literals."""
        for ci, c in enumerate(self.clauses):
            if c is None:
                continue
            if ci not in self.watches[_idx(c[0])] or ci not in self.watches[_idx(c[1])]:
                return False
        return True

    # ------------------------------------------------------- the loop

    def solve(self) -> list[int] | None:
        if not self.ok:  # @line L1
            return None
        self.qhead = 0  # @line L2
        since_restart = 0
        next_restart = luby(1) * self.restart_unit
        next_reduce = self.reduce_first
        recent: deque[int] = deque(maxlen=50)
        lbd_total = 0
        while True:  # @line L3
            confl = self.propagate()  # @line L4
            if confl is not None:  # @line L5
                self.conflicts += 1
                since_restart += 1
                if not self.trail_lim:  # @line L6
                    self.ok = False
                    return None
                dl = len(self.trail_lim)
                learnt, b, lbd = self.analyze(confl)  # @line L7
                if self.check:
                    assert [self.level[abs(q)] for q in learnt].count(dl) == 1
                    assert self.level[abs(learnt[0])] == dl
                    assert all(self.val(q) == -1 for q in learnt)
                self.cancel_until(b)  # @line L8
                if self.check:
                    assert self.val(learnt[0]) == 0
                    assert all(self.val(q) == -1 for q in learnt[1:])
                self.learned_log.append(list(learnt))
                if len(learnt) == 1:  # @line L9
                    self.enqueue(learnt[0], -1)
                else:
                    ci = self.attach(learnt, True, lbd)
                    self.enqueue(learnt[0], ci)
                self.var_inc /= self.var_decay  # @line L10
                recent.append(lbd)
                lbd_total += lbd
            else:
                if len(self.trail) == self.n:  # @line L11
                    return [v if self.value[v] > 0 else -v for v in range(1, self.n + 1)]
                due = False
                if self.restart == "luby":
                    due = since_restart >= next_restart
                elif self.restart == "glucose":
                    due = len(recent) == 50 and 0.8 * sum(recent) / 50 > lbd_total / self.conflicts
                if due:  # @line L12
                    self.cancel_until(0)
                    self.restarts += 1
                    since_restart = 0
                    next_restart = luby(self.restarts + 1) * self.restart_unit
                    recent.clear()
                    continue
                if self.reduce_first and self.conflicts >= next_reduce:  # @line L13
                    self.reduce_db()
                    next_reduce = self.conflicts + self.reduce_first + self.reduce_inc * self.reductions
                lit = self.pick_branch_lit()  # @line L14
                self.decide(lit)  # @line L15


def cdcl(n: int, clauses: Iterable[Sequence[int]], **options: object) -> list[int] | None:
    """Return a model of the CNF formula over 1..n as a list of literals, or
    None when it is unsatisfiable. Options are those of Solver."""
    return Solver(n, clauses, **options).solve()  # type: ignore[arg-type]
