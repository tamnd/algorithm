# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-sat/. The authors are listed in prov/WQ19T1.jsonl.

"""A small incremental CDCL solver with assumptions.

Clauses can be added between calls, and learned clauses are kept, because
they follow from the clauses, which only grow. solve(assumptions) decides
the assumption literals first, one per decision level. If an assumption is
false, analyze_final returns the subset of the assumptions that unit
propagation used to make it false: a failed-assumption core. Clauses are
lists of DIMACS ints.
"""


class IncrementalSolver:
    def __init__(self) -> None:
        self.clauses: list[list[int]] = []
        self.n = 0
        self.conflicts = 0
        self.model: dict[int, bool] = {}
        self.core: list[int] = []
        self._reset()

    def _reset(self) -> None:
        self.val: dict[int, bool] = {}
        self.level: dict[int, int] = {}
        self.reason: dict[int, int | None] = {}
        self.trail: list[int] = []
        self.lim: list[int] = []

    def add_clause(self, clause: list[int]) -> None:
        c = list(dict.fromkeys(clause))
        if any(-a in c for a in c):
            return  # a tautology adds nothing
        self.n = max([self.n] + [abs(a) for a in c])
        self.clauses.append(c)

    def _assign(self, lit: int, why: int | None) -> None:
        self.val[abs(lit)] = lit > 0
        self.level[abs(lit)] = len(self.lim)
        self.reason[abs(lit)] = why
        self.trail.append(lit)

    def _value(self, lit: int) -> bool | None:
        v = self.val.get(abs(lit))
        return None if v is None else v == (lit > 0)

    def _backtrack(self, to: int) -> None:
        while len(self.lim) > to:
            start = self.lim.pop()
            while len(self.trail) > start:
                v = abs(self.trail.pop())
                del self.val[v], self.level[v], self.reason[v]

    def _propagate(self) -> int | None:
        changed = True
        while changed:
            changed = False
            for ci, c in enumerate(self.clauses):
                free = 0
                last = 0
                sat = False
                for lit in c:
                    v = self._value(lit)
                    if v is None:
                        free += 1
                        last = lit
                    elif v:
                        sat = True
                        break
                if sat:
                    continue
                if free == 0:
                    return ci
                if free == 1:
                    self._assign(last, ci)
                    changed = True
        return None

    def _analyze(self, confl: int) -> list[int]:
        seen: set[int] = set()
        out: list[int] = []
        counter = 0
        p = 0
        idx = len(self.trail) - 1
        c = confl
        while True:
            for q in self.clauses[c]:
                if q == p:
                    continue
                v = abs(q)
                if v not in seen and self.level[v] > 0:
                    seen.add(v)
                    if self.level[v] == len(self.lim):
                        counter += 1
                    else:
                        out.append(q)
            while abs(self.trail[idx]) not in seen:
                idx -= 1
            p = self.trail[idx]
            idx -= 1
            counter -= 1
            if counter == 0:
                return [-p] + out
            c = self.reason[abs(p)]

    def _analyze_final(self, failed: int) -> list[int]:
        """The assumptions that made the assumption failed false, with failed itself."""
        core = [failed]
        seen = {abs(failed)}
        for lit in reversed(self.trail):
            v = abs(lit)
            if v not in seen or self.level[v] == 0:
                continue
            r = self.reason[v]
            if r is None:
                core.append(lit)  # a decision below the assumption levels is an assumption
            else:
                seen.update(abs(q) for q in self.clauses[r] if abs(q) != v)
        return core

    def solve(self, assumptions: list[int] = ()) -> bool:
        """Decide F under the assumptions; set self.model or self.core."""
        self._reset()  # @line L1
        self.model, self.core = {}, []
        assumptions = list(assumptions)
        n = max([self.n] + [abs(a) for a in assumptions])
        while True:
            confl = self._propagate()  # @line L2
            if confl is not None:
                self.conflicts += 1
                if not self.lim:  # @line L3
                    return False  # F alone is unsatisfiable; the core is empty
                lemma = self._analyze(confl)  # @line L4
                back = max((self.level[abs(q)] for q in lemma[1:]), default=0)
                self._backtrack(back)  # @line L5
                self.clauses.append(lemma)
                continue
            if len(self.lim) < len(assumptions):  # @line L6
                a = assumptions[len(self.lim)]
                value = self._value(a)
                if value is False:  # @line L7
                    self.core = self._analyze_final(a)  # @line L8
                    self._backtrack(0)
                    return False
                self.lim.append(len(self.trail))  # @line L9
                if value is None:
                    self._assign(a, None)
                continue
            free = [v for v in range(1, n + 1) if v not in self.val]
            if not free:  # @line L10
                self.model = dict(self.val)
                self._backtrack(0)
                return True
            self.lim.append(len(self.trail))  # @line L11
            self._assign(-free[0], None)
