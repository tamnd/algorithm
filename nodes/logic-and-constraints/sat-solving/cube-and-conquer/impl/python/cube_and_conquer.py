# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cube-and-conquer/. The authors are listed in prov/7ZW1HX.jsonl.

"""Cube-and-conquer: a lookahead phase cuts the search tree into cubes, and an
incremental CDCL solver solves the formula under each cube as assumptions.

The cube phase follows CreateCubes* of Heule, Kullmann, Wieringa and Biere
(HVC 2011): theta grows by 5% at every node, shrinks by 30% at a refuted node
or below depth `depth`, and a node becomes a cube when
|decisions| * |assigned| > theta * |vars(F)|. Clauses are lists of DIMACS ints.
"""

from dataclasses import dataclass, field


# ---------------------------------------------------------------- cube phase

def propagate(clauses: list[list[int]], assign: dict[int, bool]) -> dict[int, bool] | None:
    """Unit propagation to a fixpoint; None on a conflict."""
    assign = dict(assign)
    changed = True
    while changed:
        changed = False
        for c in clauses:
            free = None
            count = 0
            for a in c:
                v = assign.get(abs(a))
                if v is None:
                    free = a
                    count += 1
                elif v == (a > 0):
                    break
            else:
                if count == 0:
                    return None
                if count == 1:
                    assign[abs(free)] = free > 0
                    changed = True
    return assign


def _open(clauses: list[list[int]], assign: dict[int, bool]) -> list[list[int]]:
    return [c for c in clauses if not any(assign.get(abs(a)) == (a > 0) for a in c)]


def _reduction(clauses, before, after) -> int:
    return sum(1 for c in _open(clauses, after)
               if any(abs(a) in after and abs(a) not in before for a in c))


def simplify(clauses, assign):
    """Unit propagation and failed literals to a fixpoint. Returns (assign, scores) or (None, None)."""
    assign = propagate(clauses, assign)
    while assign is not None:
        scores = {}
        failed = None
        for x in sorted({abs(a) for c in _open(clauses, assign) for a in c} - set(assign)):
            side = {lit: propagate(clauses, {**assign, x: lit > 0}) for lit in (x, -x)}
            if side[x] is None and side[-x] is None:
                return None, None
            if side[x] is None or side[-x] is None:
                failed = side[-x] if side[x] is None else side[x]
                break
            dp, dn = _reduction(clauses, assign, side[x]), _reduction(clauses, assign, side[-x])
            scores[x] = (1024 * dp * dn + dp + dn, x if dp <= dn else -x)
        if failed is None:
            return assign, scores
        assign = failed
    return None, None


@dataclass
class Partition:
    cubes: list[list[int]] = field(default_factory=list)    # A: the cutoff leaves
    clauses: list[list[int]] = field(default_factory=list)  # C: the negated refuted leaves
    theta_trace: list[float] = field(default_factory=list)


def create_cubes(clauses: list[list[int]], theta: float = 1000.0, depth: int = 20) -> Partition:
    nvars = len({abs(a) for c in clauses for a in c}) or 1
    part = Partition()
    state = {"theta": theta}  # @line L1

    def rec(dec: list[int]) -> None:
        state["theta"] *= 1.05  # @line L2
        base = {abs(a): a > 0 for a in dec}
        assign, scores = simplify(clauses, base)
        refuted = assign is None
        if refuted or len(dec) > depth:  # @line L3
            state["theta"] *= 0.7
        part.theta_trace.append(state["theta"])
        if refuted:  # @line L4
            part.clauses.append([-a for a in dec])
            return
        if not scores or len(dec) * len(assign) > state["theta"] * nvars:  # @line L5
            part.cubes.append(list(dec))  # a cutoff leaf, or every clause is satisfied
            return
        best = max(scores, key=lambda x: (scores[x][0], -x))  # @line L6
        lit = scores[best][1]  # the side that reduces less goes first
        rec(dec + [lit])  # @line L7
        rec(dec + [-lit])

    rec([])
    return part


# ------------------------------------------------------------- conquer phase

class IncrementalSolver:
    """A small CDCL solver with assumptions and a failed-assumption core."""

    def __init__(self) -> None:
        self.clauses: list[list[int]] = []
        self.n = 0
        self.conflicts = 0
        self.model: dict[int, bool] = {}
        self.core: list[int] = []

    def add_clause(self, clause: list[int]) -> None:
        c = list(dict.fromkeys(clause))
        if any(-a in c for a in c):
            return
        self.n = max([self.n] + [abs(a) for a in c])
        self.clauses.append(c)

    def _assign(self, lit, why) -> None:
        self.val[abs(lit)] = lit > 0
        self.level[abs(lit)] = len(self.lim)
        self.reason[abs(lit)] = why
        self.trail.append(lit)

    def _value(self, lit):
        v = self.val.get(abs(lit))
        return None if v is None else v == (lit > 0)

    def _backtrack(self, to: int) -> None:
        while len(self.lim) > to:
            start = self.lim.pop()
            while len(self.trail) > start:
                v = abs(self.trail.pop())
                del self.val[v], self.level[v], self.reason[v]

    def _propagate(self):
        changed = True
        while changed:
            changed = False
            for ci, c in enumerate(self.clauses):
                free, last = 0, 0
                for lit in c:
                    v = self._value(lit)
                    if v is None:
                        free += 1
                        last = lit
                    elif v:
                        break
                else:
                    if free == 0:
                        return ci
                    if free == 1:
                        self._assign(last, ci)
                        changed = True
        return None

    def _analyze(self, confl: int) -> list[int]:
        seen, out, counter, p = set(), [], 0, 0
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
        core, seen = [failed], {abs(failed)}
        for lit in reversed(self.trail):
            v = abs(lit)
            if v not in seen or self.level[v] == 0:
                continue
            if self.reason[v] is None:
                core.append(lit)
            else:
                seen.update(abs(q) for q in self.clauses[self.reason[v]] if abs(q) != v)
        return core

    def solve(self, assumptions=()) -> bool:
        self.val, self.level, self.reason, self.trail, self.lim = {}, {}, {}, [], []
        self.model, self.core = {}, []
        assumptions = list(assumptions)
        n = max([self.n] + [abs(a) for a in assumptions])
        while True:
            confl = self._propagate()
            if confl is not None:
                self.conflicts += 1
                if not self.lim:
                    return False
                lemma = self._analyze(confl)
                self._backtrack(max((self.level[abs(q)] for q in lemma[1:]), default=0))
                self.clauses.append(lemma)
                continue
            if len(self.lim) < len(assumptions):
                a = assumptions[len(self.lim)]
                value = self._value(a)
                if value is False:
                    self.core = self._analyze_final(a)
                    self._backtrack(0)
                    return False
                self.lim.append(len(self.trail))
                if value is None:
                    self._assign(a, None)
                continue
            free = [v for v in range(1, n + 1) if v not in self.val]
            if not free:
                self.model = dict(self.val)
                self._backtrack(0)
                return True
            self.lim.append(len(self.trail))
            self._assign(-free[0], None)


def conquer(clauses: list[list[int]], part: Partition, n: int, use_cores: bool = True):
    """Solve F ∧ C under each cube. Returns (model or None, number of cubes solved)."""
    s = IncrementalSolver()
    for c in clauses + part.clauses:  # @line L8
        s.add_clause(c)
    s.n = max(s.n, n)
    for k, cube in enumerate(part.cubes, 1):  # @line L9
        if s.solve(cube):  # @line L10
            return {v: s.model.get(v, False) for v in range(1, n + 1)}, k
        if not s.core:
            return None, k  # F ∧ C alone is unsatisfiable
        if use_cores:
            s.add_clause([-a for a in s.core])  # @line L11
    return None, len(part.cubes)  # @line L12


def cube_and_conquer(clauses: list[list[int]], n: int, theta: float = 1000.0, depth: int = 20):
    part = create_cubes(clauses, theta, depth)
    model, _ = conquer(clauses, part, n)
    return model
