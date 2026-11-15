# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conflict-driven-answer-set-solving/. The authors are listed in prov/THR1ZW.jsonl.
"""Conflict-driven nogood learning for answer sets (CDNL-ASP), after Gebser, Kaufmann and Schaub (2012).

The input is a ground normal program in the format of lp.py, a list of rules
(head, pos, neg), and optionally a list of constraints (pos, neg). The solver
has one Boolean variable for each atom and one for each distinct rule body.
A literal is +v (v is true) or -v (v is false). A nogood is a frozenset of
literals that must not all be true at the same time.

The static nogoods are those of the completion (Delta_P). Loop nogoods
(Lambda_P) are added on demand: after unit propagation, the solver computes
the greatest unfounded set U of the atoms that are not false, and adds
lambda(p, U) for each p in U. Conflicts are analysed to the first unique
implication point, and the learned nogood is a resolvent of nogoods already
known. Propagation scans all nogoods; a real solver uses watched literals.
"""


def lit_var(lit):
    return lit if lit > 0 else -lit


class Solver:
    def __init__(self, program, constraints=(), blocked=()):
        names = set()
        for h, pos, neg in program:
            names.add(h)
            names.update(pos)
            names.update(neg)
        for pos, neg in constraints:
            names.update(pos)
            names.update(neg)
        self.atom_names = sorted(names)
        self.atom_var = {a: i + 1 for i, a in enumerate(self.atom_names)}
        self.n_atoms = len(self.atom_names)
        self.body_var = {}
        self.body_of = {}
        self.heads_of_body = {}
        self.bodies_of_atom = {self.atom_var[a]: [] for a in self.atom_names}

        def body(pos, neg):
            k = (tuple(sorted(self.atom_var[b] for b in set(pos))), tuple(sorted(self.atom_var[c] for c in set(neg))))
            if k not in self.body_var:
                v = self.n_atoms + len(self.body_var) + 1
                self.body_var[k] = v
                self.body_of[v] = k
                self.heads_of_body[v] = []
            return self.body_var[k]

        for h, pos, neg in program:
            b = body(pos, neg)
            hv = self.atom_var[h]
            if hv not in self.heads_of_body[b]:
                self.heads_of_body[b].append(hv)
                self.bodies_of_atom[hv].append(b)
        constraint_bodies = [body(pos, neg) for pos, neg in constraints]
        self.n_vars = self.n_atoms + len(self.body_var)

        # The completion nogoods Delta_P.
        self.static = []  # @line L1
        for b, (pos, neg) in self.body_of.items():
            self.static.append(frozenset([-b] + list(pos) + [-c for c in neg]))
            for p in pos:
                self.static.append(frozenset([b, -p]))
            for c in neg:
                self.static.append(frozenset([b, c]))
        for a, bodies in self.bodies_of_atom.items():
            for b in bodies:
                self.static.append(frozenset([-a, b]))
            self.static.append(frozenset([a] + [-b for b in bodies]))
        for b in constraint_bodies:
            self.static.append(frozenset([b]))
        # Nogoods that exclude answer sets found before (used to enumerate).
        self.blocking = []
        self.blocked_models = [frozenset(m) for m in blocked]
        for m in blocked:
            m = set(m)
            self.blocking.append(frozenset(self.atom_var[a] if a in m else -self.atom_var[a] for a in self.atom_names))
        self.loop = []
        self.loop_set = set()
        self.learned = []
        self.tight = self._is_tight()

        self.value = [None] * (self.n_vars + 1)
        self.level = [0] * (self.n_vars + 1)
        self.reason = [None] * (self.n_vars + 1)
        self.trail = []
        self.trail_pos = [0] * (self.n_vars + 1)
        self.dl = 0
        self.stats = {"decisions": 0, "conflicts": 0, "loop_nogoods": 0}

    def _is_tight(self):
        """True when the positive dependency graph has no cycle (Fages: then no loop nogood is needed)."""
        succ = {a: set() for a in self.bodies_of_atom}
        for b, (pos, _) in self.body_of.items():
            for h in self.heads_of_body[b]:
                succ[h].update(pos)
        state = {}
        for start in succ:
            if start in state:
                continue
            stack = [(start, iter(succ[start]))]
            state[start] = 1
            while stack:
                node, it = stack[-1]
                nxt = next(it, None)
                if nxt is None:
                    state[node] = 2
                    stack.pop()
                elif state.get(nxt) == 1:
                    return False
                elif nxt not in state:
                    state[nxt] = 1
                    stack.append((nxt, iter(succ[nxt])))
        return True

    # Assignment.
    def is_true(self, lit):
        v = self.value[lit_var(lit)]
        return v is not None and v == (lit > 0)

    def assign(self, lit, reason):
        v = lit_var(lit)
        self.value[v] = lit > 0
        self.level[v] = self.dl
        self.reason[v] = reason
        self.trail_pos[v] = len(self.trail)
        self.trail.append(lit)

    def backjump(self, j):
        while self.trail and self.level[lit_var(self.trail[-1])] > j:
            v = lit_var(self.trail.pop())
            self.value[v] = None
            self.reason[v] = None
        self.dl = j

    # Propagation.
    def nogoods(self):
        return self.static + self.blocking + self.loop + self.learned

    def unit_propagate(self):
        """Unit propagation over all nogoods. Return a violated nogood or None."""
        while True:
            changed = False
            for ng in self.nogoods():
                open_lit = None
                n_open = 0
                satisfied = False
                for lit in ng:
                    v = self.value[lit_var(lit)]
                    if v is None:
                        n_open += 1
                        open_lit = lit
                        if n_open > 1:
                            break
                    elif v != (lit > 0):
                        satisfied = True
                        break
                if satisfied or n_open > 1:
                    continue
                if n_open == 0:
                    return ng  # @line L12
                self.assign(-open_lit, ng)  # @line L11
                changed = True
            if not changed:
                return None

    def unfounded_set(self):
        """The greatest unfounded set: the atoms not false that no body which is not false can derive."""
        derived = set()
        changed = True
        while changed:
            changed = False
            for b, (pos, _) in self.body_of.items():
                if self.value[b] is False or not all(p in derived for p in pos):
                    continue
                for h in self.heads_of_body[b]:
                    if h not in derived and self.value[h] is not False:
                        derived.add(h)
                        changed = True
        return [a for a in range(1, self.n_atoms + 1) if self.value[a] is not False and a not in derived]

    def external_bodies(self, u):
        us = set(u)
        return sorted({b for a in us for b in self.bodies_of_atom[a] if not us.intersection(self.body_of[b][0])})

    def propagate(self):
        """Unit propagation, then unfounded set checks that add loop nogoods. Return a violated nogood or None."""
        while True:  # @line L10
            conflict = self.unit_propagate()
            if conflict is not None or self.tight:  # @line L13
                return conflict
            u = self.unfounded_set()  # @line L14
            if not u:  # @line L15
                return None
            eb = self.external_bodies(u)
            for p in u:
                ng = frozenset([p] + [-b for b in eb])
                if ng not in self.loop_set:
                    self.loop_set.add(ng)
                    self.loop.append(ng)  # @line L16
                    self.stats["loop_nogoods"] += 1

    # Conflict analysis.
    def analyze(self, conflict):
        """Resolve back to the first unique implication point. Return the learned nogood and the backjump level."""
        k = max(self.level[lit_var(l)] for l in conflict)  # @line L17
        delta = set(conflict)
        while True:
            at_k = [l for l in delta if self.level[lit_var(l)] == k]
            if len(at_k) == 1:  # @line L18
                break
            sigma = max(at_k, key=lambda l: self.trail_pos[lit_var(l)])  # @line L19
            eps = self.reason[lit_var(sigma)]
            delta.discard(sigma)
            delta.update(l for l in eps if l != -sigma)  # @line L20
        j = max((self.level[lit_var(l)] for l in delta if self.level[lit_var(l)] != k), default=0)
        return frozenset(delta), j  # @line L21

    def solve(self):
        """Return one answer set as a frozenset of atoms, or None when there is none."""
        while True:  # @line L2
            conflict = self.propagate()  # @line L3
            if conflict is not None:  # @line L4
                self.stats["conflicts"] += 1
                k = max(self.level[lit_var(l)] for l in conflict)
                if k == 0:  # @line L5
                    return None
                if k < self.dl:
                    self.backjump(k)
                learned, j = self.analyze(conflict)  # @line L6
                self.learned.append(learned)  # @line L7
                self.backjump(j)
                continue
            open_vars = [v for v in range(1, self.n_vars + 1) if self.value[v] is None]
            if not open_vars:  # @line L8
                return frozenset(self.atom_names[a - 1] for a in range(1, self.n_atoms + 1) if self.value[a])
            self.dl += 1
            self.stats["decisions"] += 1
            self.assign(-open_vars[0], None)  # @line L9


def answer_sets(program, constraints=(), solvers=None):
    """All answer sets, sorted by size and then by content. Each new search blocks the answer sets found before."""
    found = []
    while True:
        s = Solver(program, constraints, blocked=found)
        m = s.solve()
        if solvers is not None:
            solvers.append(s)
        if m is None:
            break
        found.append(m)
    return sorted(found, key=lambda m: (len(m), sorted(m)))


def has_answer_set(program, constraints=()):
    return Solver(program, constraints).solve() is not None
