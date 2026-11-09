# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dpll-t/. The authors are listed in prov/R9CQRP.jsonl.
"""A basic strategy of Abstract DPLL Modulo Theories, with EUF as the theory.

A formula is a list of clauses. A clause is a list of nonzero integers in the
DIMACS style: v is the atom v, and -v its negation. The map atoms sends a
variable to a pair (s, t) of ground terms, and then v means s = t. Variables
that are not in atoms are plain Boolean variables. A term is a string (a
constant) or a tuple (f, t1, ..., tk).

The strategy applies the rules of Nieuwenhuis, Oliveras and Tinelli (2006):
Propagate, T-Propagate, Decide, Fail, T-Learn and T-Backjump. Its backjump
clause is the negation of the decisions, so T-Backjump goes back exactly one
decision, as in the DPLL procedure. The theory solver is a plain congruence
closure that is built again at each call.
"""

from typing import Optional

Term = object


# ---------------------------------------------------------------- the theory
class EUFTheory:
    """Decides a conjunction of EUF literals and finds minimal conflicts."""

    def _closure(self, eqs: list[tuple[Term, Term]], extra: list[Term]) -> dict:
        terms: list[Term] = []
        seen: set = set()
        stack = [x for e in eqs for x in e] + list(extra)
        while stack:
            u = stack.pop()
            if u not in seen:
                seen.add(u)
                terms.append(u)
                if isinstance(u, tuple):
                    stack.extend(u[1:])
        parent = {t: t for t in terms}

        def find(x: Term) -> Term:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for s, t in eqs:
            parent[find(s)] = find(t)
        apps = [t for t in terms if isinstance(t, tuple)]
        changed = True
        while changed:  # apply congruence until nothing changes
            changed = False
            table: dict = {}
            for p in apps:
                sig = (p[0], len(p)) + tuple(find(c) for c in p[1:])
                q = table.setdefault(sig, p)
                if find(q) != find(p):
                    parent[find(p)] = find(q)
                    changed = True
        return {t: find(t) for t in terms}

    def consistent(self, lits: list[tuple[Term, Term, bool]]) -> bool:
        eqs = [(s, t) for s, t, pos in lits if pos]
        cls = self._closure(eqs, [x for s, t, _ in lits for x in (s, t)])
        return all(cls[s] != cls[t] for s, t, pos in lits if not pos)

    def conflict(self, lits: list[tuple[Term, Term, bool]]) -> Optional[list[int]]:
        """None if the conjunction is satisfiable. Otherwise the positions of a
        subset that is unsatisfiable and minimal: dropping any one of its
        literals makes it satisfiable (deletion-based minimization)."""
        if self.consistent(lits):
            return None
        keep = list(range(len(lits)))
        for i in range(len(lits)):
            trial = [j for j in keep if j != i]
            if not self.consistent([lits[j] for j in trial]):
                keep = trial
        return keep

    def entailed(self, lits: list[tuple[Term, Term, bool]], s: Term, t: Term) -> bool:
        eqs = [(a, b) for a, b, pos in lits if pos]
        cls = self._closure(eqs, [s, t])
        return cls[s] == cls[t]


# ---------------------------------------------------------------- the solver
class DPLLT:
    def __init__(self, clauses: list[list[int]], atoms: dict[int, tuple[Term, Term]],
                 theory_propagate: bool = True) -> None:
        self.clauses = [list(c) for c in clauses]
        self.atoms = dict(atoms)
        self.theory = EUFTheory()
        self.theory_propagate = theory_propagate
        self.variables = sorted(set(self.atoms) | {abs(l) for c in self.clauses for l in c})
        self.trail: list[tuple[int, bool]] = []  # (literal, is a decision)
        self.val: dict[int, bool] = {}
        self.lemmas: list[list[int]] = []  # the clauses added by T-Learn
        self.stats = {"decisions": 0, "backjumps": 0, "t_propagations": 0}

    def value(self, lit: int) -> Optional[bool]:
        v = self.val.get(abs(lit))
        return None if v is None else (v if lit > 0 else not v)

    def _assign(self, lit: int, decision: bool) -> None:
        self.trail.append((lit, decision))
        self.val[abs(lit)] = lit > 0

    def _theory_literals(self) -> tuple[list[tuple[Term, Term, bool]], list[int]]:
        lits, origin = [], []
        for lit, _ in self.trail:
            if abs(lit) in self.atoms:
                s, t = self.atoms[abs(lit)]
                lits.append((s, t, lit > 0))
                origin.append(lit)
        return lits, origin

    def _propagate(self) -> Optional[list[int]]:
        """Apply Propagate until no clause is unit. Return a falsified clause."""
        changed = True
        while changed:
            changed = False
            for c in self.clauses:
                vals = [self.value(l) for l in c]
                if True in vals:
                    continue
                free = [l for l, v in zip(c, vals) if v is None]
                if not free:
                    return c
                if len(free) == 1:
                    self._assign(free[0], False)
                    changed = True
        return None

    def solve(self) -> tuple[bool, Optional[dict[int, bool]]]:
        """Return (True, a total T-consistent model) or (False, None)."""
        self.trail, self.val = [], {}  # @line L1
        while True:  # @line L2
            falsified = self._propagate()  # @line L3
            if falsified is not None:  # @line L4
                decisions = [i for i, (_, d) in enumerate(self.trail) if d]
                if not decisions:  # @line L5
                    return False, None
                i = decisions[-1]  # @line L6
                d = self.trail[i][0]
                for lit, _ in self.trail[i:]:
                    del self.val[abs(lit)]
                del self.trail[i:]
                self._assign(-d, False)
                self.stats["backjumps"] += 1
                if self.lemmas and falsified is self.lemmas[-1]:
                    self.clauses.remove(falsified)  # @line L7: T-Forget the used lemma
                continue
            lits, origin = self._theory_literals()
            core = self.theory.conflict(lits)  # @line L8
            if core is not None:  # @line L9
                lemma = [-origin[j] for j in core]
                self.clauses.append(lemma)  # T-Learn; the lemma is falsified by the trail
                self.lemmas.append(lemma)
                continue
            if self.theory_propagate:  # @line L10
                found = False
                for v in self.variables:
                    if v in self.atoms and v not in self.val:
                        s, t = self.atoms[v]
                        if self.theory.entailed(lits, s, t):
                            self._assign(v, False)
                            self.stats["t_propagations"] += 1
                            found = True
                if found:
                    continue
            free = [v for v in self.variables if v not in self.val]
            if not free:  # @line L11
                return True, dict(self.val)
            self._assign(free[0], True)  # @line L12
            self.stats["decisions"] += 1


def dpll_t(clauses: list[list[int]], atoms: dict[int, tuple[Term, Term]]) -> tuple[bool, Optional[dict[int, bool]]]:
    return DPLLT(clauses, atoms).solve()
