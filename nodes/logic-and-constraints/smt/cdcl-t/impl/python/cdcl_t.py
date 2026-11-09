# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cdcl-t/. The authors are listed in prov/R7T2R4.jsonl.
"""CDCL(T) with EUF: clause learning over a mixed implication graph.

Clauses use DIMACS literals. The map atoms sends a variable v to a pair of
ground terms (s, t), and then v means s = t. Other variables are plain
Boolean variables. A term is a string or a tuple (f, t1, ..., tk).

The theory solver is congruence closure with a proof forest. Each theory
propagation gets an explanation clause as its reason, so conflict analysis
treats theory steps and Boolean steps in the same way. For clarity the
closure is built again from the trail at each check. A real solver keeps it
and undoes merges on a trail when it backjumps.
"""

from typing import Hashable, Optional

Term = object


# ---------------------------------------------------------------- the theory
class CongruenceClosure:
    """Congruence closure with explanations (see the congruence-closure page)."""

    def __init__(self) -> None:
        self.ids: dict = {}
        self.head: list = []
        self.args: list[tuple[int, ...]] = []
        self.rep: list[int] = []
        self.members: list[list[int]] = []
        self.uses: list[list[int]] = []
        self.table: dict = {}
        self.pparent: list[int] = []
        self.plabel: list[tuple] = []
        self.pending: list[tuple[int, int, tuple]] = []

    def _sig(self, p: int) -> tuple:
        return (self.head[p], tuple(self.rep[c] for c in self.args[p]))

    def add_term(self, t: Term) -> int:
        stack = [(t, False)]
        while stack:
            u, ready = stack.pop()
            if u in self.ids:
                continue
            if isinstance(u, tuple) and not ready:
                stack.append((u, True))
                stack.extend((a, False) for a in u[1:] if a not in self.ids)
                continue
            i = len(self.rep)
            self.ids[u] = i
            self.head.append(u[0] if isinstance(u, tuple) else u)
            self.args.append(tuple(self.ids[a] for a in u[1:]) if isinstance(u, tuple) else ())
            self.rep.append(i)
            self.members.append([i])
            self.uses.append([])
            self.pparent.append(-1)
            self.plabel.append(())
            if isinstance(u, tuple):
                for c in self.args[i]:
                    self.uses[self.rep[c]].append(i)
                q = self.table.setdefault(self._sig(i), i)
                if q != i:
                    self.pending.append((i, q, ("cong", i, q)))
        self._propagate()
        return self.ids[t]

    def merge(self, s: Term, t: Term, label: Hashable) -> None:
        a, b = self.add_term(s), self.add_term(t)
        self.pending.append((a, b, ("input", label)))
        self._propagate()

    def _make_root(self, a: int) -> None:
        prev, prev_label, x = -1, (), a
        while x != -1:
            nxt, nxt_label = self.pparent[x], self.plabel[x]
            self.pparent[x], self.plabel[x] = prev, prev_label
            prev, prev_label, x = x, nxt_label, nxt

    def _propagate(self) -> None:
        while self.pending:
            a, b, why = self.pending.pop()
            ra, rb = self.rep[a], self.rep[b]
            if ra == rb:
                continue
            if len(self.members[ra]) > len(self.members[rb]):
                a, b, ra, rb = b, a, rb, ra
            self._make_root(a)
            self.pparent[a], self.plabel[a] = b, why
            for x in self.members[ra]:
                self.rep[x] = rb
            self.members[rb].extend(self.members[ra])
            self.members[ra] = []
            moved, self.uses[ra] = self.uses[ra], []
            for p in moved:
                q = self.table.setdefault(self._sig(p), p)
                if self.rep[q] != self.rep[p]:
                    self.pending.append((p, q, ("cong", p, q)))
            self.uses[rb].extend(moved)

    def equal(self, s: Term, t: Term) -> bool:
        return self.rep[self.add_term(s)] == self.rep[self.add_term(t)]

    def explain(self, s: Term, t: Term) -> set:
        out: set = set()
        done: set = set()
        todo = [(self.ids[s], self.ids[t])]
        while todo:
            u, v = todo.pop()
            if u == v:
                continue
            anc = set()
            x = u
            while x != -1:
                anc.add(x)
                x = self.pparent[x]
            y = v
            while y not in anc:
                y = self.pparent[y]
            for x in (u, v):
                while x != y:
                    if x not in done:
                        done.add(x)
                        why = self.plabel[x]
                        if why[0] == "input":
                            out.add(why[1])
                        else:
                            todo.extend(zip(self.args[why[1]], self.args[why[2]]))
                    x = self.pparent[x]
        return out


# ---------------------------------------------------------------- the solver
class CDCLT:
    def __init__(self, clauses: list[list[int]], atoms: dict[int, tuple[Term, Term]],
                 restart_first: int = 8, restart_growth: float = 1.5) -> None:
        self.clauses = [list(dict.fromkeys(c)) for c in clauses]
        self.atoms = dict(atoms)
        self.variables = sorted(set(self.atoms) | {abs(l) for c in self.clauses for l in c})
        self.val: dict[int, bool] = {}
        self.level: dict[int, int] = {}
        self.reason: dict[int, Optional[list[int]]] = {}
        self.trail: list[int] = []
        self.trail_lim: list[int] = []  # the trail position of each decision
        self.learned: list[list[int]] = []
        self.theory_clauses: list[list[int]] = []  # explanations and theory conflicts
        self.restart_first, self.restart_growth = restart_first, restart_growth
        self.stats = {"conflicts": 0, "theory_conflicts": 0, "decisions": 0,
                      "t_propagations": 0, "restarts": 0}

    # -------------------------------------------------------- the trail
    def value(self, lit: int) -> Optional[bool]:
        v = self.val.get(abs(lit))
        return None if v is None else (v if lit > 0 else not v)

    def _enqueue(self, lit: int, reason: Optional[list[int]]) -> None:
        v = abs(lit)
        self.val[v] = lit > 0
        self.level[v] = len(self.trail_lim)
        self.reason[v] = reason
        self.trail.append(lit)

    def _backtrack(self, lvl: int) -> None:
        if len(self.trail_lim) <= lvl:
            return
        pos = self.trail_lim[lvl]
        for lit in self.trail[pos:]:
            v = abs(lit)
            del self.val[v], self.level[v], self.reason[v]
        del self.trail[pos:]
        del self.trail_lim[lvl:]

    # -------------------------------------------------------- propagation
    def _bcp(self) -> Optional[list[int]]:
        changed = True
        while changed:
            changed = False
            for c in self.clauses:
                free, sat = [], False
                for l in c:
                    v = self.value(l)
                    if v is True:
                        sat = True
                        break
                    if v is None:
                        free.append(l)
                if sat:
                    continue
                if not free:
                    return c
                if len(free) == 1:
                    lit = free[0]
                    self._enqueue(lit, [lit] + [l for l in c if l != lit])
                    changed = True
        return None

    def _theory(self) -> tuple[Optional[list[int]], int]:
        """Check the theory literals of the trail. Return (a conflict clause,
        0) or (None, the number of propagated literals)."""
        cc = CongruenceClosure()
        for v in self.atoms:
            cc.add_term(self.atoms[v][0])
            cc.add_term(self.atoms[v][1])
        diseqs = []
        for lit in self.trail:
            v = abs(lit)
            if v in self.atoms:
                if lit > 0:
                    cc.merge(*self.atoms[v], v)
                else:
                    diseqs.append(v)
        for w in diseqs:  # a disequality between equal terms is a conflict
            s, t = self.atoms[w]
            if cc.equal(s, t):
                clause = [w] + [-e for e in sorted(cc.explain(s, t))]
                self.theory_clauses.append(clause)
                self.stats["theory_conflicts"] += 1
                return clause, 0
        count = 0
        for v in self.variables:  # theory propagation with explanation clauses
            if v not in self.atoms or v in self.val:
                continue
            s, t = self.atoms[v]
            if cc.equal(s, t):
                reason = [v] + [-e for e in sorted(cc.explain(s, t))]
            else:
                reason = None
                for w in diseqs:
                    u, x = self.atoms[w]
                    for a, b in ((u, x), (x, u)):
                        if cc.equal(s, a) and cc.equal(t, b):
                            expl = cc.explain(s, a) | cc.explain(t, b)
                            reason = [-v, w] + [-e for e in sorted(expl)]
                            break
                    if reason:
                        break
                if reason is None:
                    continue
            self.theory_clauses.append(reason)
            self._enqueue(reason[0], reason)
            count += 1
        self.stats["t_propagations"] += count
        return None, count

    # -------------------------------------------------------- conflict analysis
    def _analyze(self, conflict: list[int]) -> tuple[list[int], int]:
        """First UIP clause and the level to backjump to."""
        cur = len(self.trail_lim)
        seen: set[int] = set()
        learnt: list[int] = [0]
        counter, p, clause, idx = 0, 0, conflict, len(self.trail) - 1
        while True:
            for q in clause:
                v = abs(q)
                if q == p or v in seen or self.level[v] == 0:
                    continue
                seen.add(v)
                if self.level[v] == cur:
                    counter += 1
                else:
                    learnt.append(q)
            while abs(self.trail[idx]) not in seen:
                idx -= 1
            p = self.trail[idx]
            idx -= 1
            counter -= 1
            if counter == 0:
                break
            clause = self.reason[abs(p)]
        learnt[0] = -p
        back = max((self.level[abs(q)] for q in learnt[1:]), default=0)
        return learnt, back

    # -------------------------------------------------------- the main loop
    def solve(self) -> tuple[bool, Optional[dict[int, bool]]]:
        next_restart = float(self.restart_first)
        since_restart = 0
        while True:
            conflict = self._bcp()  # @line L1
            if conflict is None:
                conflict, count = self._theory()  # @line L2
                if conflict is None and count > 0:
                    continue  # @line L3
            if conflict is not None:  # @line L4
                self.stats["conflicts"] += 1
                lvl = max(self.level[abs(l)] for l in conflict) if conflict else 0
                if lvl == 0:  # @line L5
                    return False, None
                self._backtrack(lvl)  # @line L6
                learnt, back = self._analyze(conflict)  # @line L7
                self._backtrack(back)  # @line L8
                self.clauses.append(learnt)  # @line L9
                self.learned.append(learnt)
                self._enqueue(learnt[0], learnt)
                since_restart += 1
                if since_restart >= next_restart:  # @line L10
                    self._backtrack(0)
                    since_restart = 0
                    next_restart *= self.restart_growth
                    self.stats["restarts"] += 1
                continue
            free = [v for v in self.variables if v not in self.val]
            if not free:  # @line L11
                return True, dict(self.val)
            self.trail_lim.append(len(self.trail))  # @line L12
            self._enqueue(free[0], None)
            self.stats["decisions"] += 1


def cdcl_t(clauses: list[list[int]], atoms: dict[int, tuple[Term, Term]]) -> tuple[bool, Optional[dict[int, bool]]]:
    return CDCLT(clauses, atoms).solve()
