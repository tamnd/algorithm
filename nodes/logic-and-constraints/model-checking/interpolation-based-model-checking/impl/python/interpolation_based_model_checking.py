# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interpolation-based-model-checking/. The authors are listed in prov/6ZZFCD.jsonl.

"""Interpolation-based model checking (McMillan 2003).

A circuit is a dict with these keys:
  "init":   a tuple of 0 and 1, the initial value of each latch
  "inputs": the number of free inputs in each step
  "next":   a list of expressions, the next value of each latch
  "prop":   an expression over the latches, the property P
An expression is a nested tuple: ("const", b), ("x", j) for latch j,
("in", j) for input j, ("not", e), ("and", a, b), ("or", a, b), ("xor", a, b).

The SAT solver below logs a resolution proof in a compact way: each clause
carries its partial interpolant in McMillan's system, so an unsatisfiable
pair (A, B) gives a Craig interpolant at the end.

itp_check returns ("holds", R) where R is an inductive invariant expression
that implies P, or ("fails", (states, inputs)) with a counterexample.
"""

from typing import Callable, Dict, List, Optional, Sequence, Tuple


def evaluate(e, xs: Sequence[int], ins: Sequence[int] = ()) -> int:
    """Value (0 or 1) of the expression e in the state xs with the inputs ins."""
    memo: Dict[int, int] = {}
    stack = [(e, False)]
    while stack:
        n, done = stack.pop()
        if id(n) in memo:
            continue
        op = n[0]
        if op == "const":
            memo[id(n)] = int(bool(n[1]))
        elif op == "x":
            memo[id(n)] = int(xs[n[1]])
        elif op == "in":
            memo[id(n)] = int(ins[n[1]])
        elif not done:
            stack.append((n, True))
            stack.extend((k, False) for k in n[1:])
        else:
            a = [memo[id(k)] for k in n[1:]]
            if op == "not":
                memo[id(n)] = 1 - a[0]
            elif op == "and":
                memo[id(n)] = a[0] & a[1]
            elif op == "or":
                memo[id(n)] = a[0] | a[1]
            else:
                memo[id(n)] = a[0] ^ a[1]
    return memo[id(e)]


def step(circuit, xs: Sequence[int], ins: Sequence[int]) -> Tuple[int, ...]:
    """The successor of the state xs under the inputs ins."""
    return tuple(evaluate(f, xs, ins) for f in circuit["next"])


def f_or(a, b):
    """Disjunction of two interpolant formulas, with constants folded."""
    if a is True or b is True:
        return True
    if a is False:
        return b
    if b is False or a is b:
        return a
    return ("or", a, b)


def f_and(a, b):
    """Conjunction of two interpolant formulas, with constants folded."""
    if a is False or b is False:
        return False
    if a is True:
        return b
    if b is True or a is b:
        return a
    return ("and", a, b)


def as_expr(f):
    """Turn the Python constants True and False into constant expressions."""
    return ("const", int(f)) if isinstance(f, bool) else f


class CNF:
    """A growing CNF formula with DIMACS-style integer literals."""

    def __init__(self) -> None:
        self.nv = 0
        self.clauses: List[List[int]] = []

    def new(self) -> int:
        self.nv += 1
        return self.nv

    def gate(self, op: str, a: list):
        """Tseitin variable for op applied to a; constants are folded away."""
        if op == "not":
            return (not a[0]) if isinstance(a[0], bool) else -a[0]
        x, y = a
        if op == "and":
            if x is False or y is False:
                return False
            if x is True:
                return y
            if y is True:
                return x
            g = self.new()
            self.clauses += [[-g, x], [-g, y], [g, -x, -y]]
            return g
        if op == "or":
            if x is True or y is True:
                return True
            if x is False:
                return y
            if y is False:
                return x
            g = self.new()
            self.clauses += [[g, -x], [g, -y], [-g, x, y]]
            return g
        if isinstance(x, bool) and isinstance(y, bool):
            return x != y
        if isinstance(x, bool):
            return -y if x else y
        if isinstance(y, bool):
            return -x if y else x
        g = self.new()
        self.clauses += [[-g, x, y], [-g, -x, -y], [g, -x, y], [g, x, -y]]
        return g

    def encode(self, e, xs: Sequence, ins: Sequence = ()):
        """A literal (or a constant) equal to the expression e over xs and ins."""
        memo: Dict[int, object] = {}
        stack = [(e, False)]
        while stack:
            n, done = stack.pop()
            if id(n) in memo:
                continue
            op = n[0]
            if op == "const":
                memo[id(n)] = bool(n[1])
            elif op == "x":
                memo[id(n)] = xs[n[1]]
            elif op == "in":
                memo[id(n)] = ins[n[1]]
            elif not done:
                stack.append((n, True))
                stack.extend((k, False) for k in n[1:])
            else:
                memo[id(n)] = self.gate(op, [memo[id(k)] for k in n[1:]])
        return memo[id(e)]

    def require(self, lit) -> None:
        """Add the unit clause lit (an empty clause if lit is the constant False)."""
        if lit is True:
            return
        self.clauses.append([] if lit is False else [lit])

    def frame(self, circuit) -> Tuple[List[int], List[int]]:
        """Fresh variables for one state and one input vector."""
        xs = [self.new() for _ in circuit["init"]]
        ins = [self.new() for _ in range(circuit["inputs"])]
        return xs, ins

    def transition(self, circuit, xs, ins, ys) -> None:
        """Clauses of T(xs, ins, ys): each ys[j] equals next[j](xs, ins)."""
        for f, y in zip(circuit["next"], ys):
            lit = self.encode(f, xs, ins)
            if isinstance(lit, bool):
                self.clauses.append([y] if lit else [-y])
            else:
                self.clauses += [[-y, lit], [y, -lit]]


class Solver:
    """CDCL with first-UIP learning that also computes a Craig interpolant.

    The first n_a clauses form A and the rest form B. Each clause keeps its
    partial interpolant in McMillan's system. label maps each variable that
    occurs in both A and B to the expression that stands for it.
    """

    def __init__(self, nvars: int, clauses: List[List[int]], n_a: int = 0, label: Optional[dict] = None) -> None:
        self.n = nvars
        self.val = [0] * (nvars + 1)
        self.level = [0] * (nvars + 1)
        self.reason = [-1] * (nvars + 1)
        self.act = [0.0] * (nvars + 1)
        self.inc = 1.0
        self.trail: List[int] = []
        self.lim: List[int] = []
        self.qhead = 0
        self.cls: List[List[int]] = []
        self.itp: list = []
        self.watch: List[List[int]] = [[] for _ in range(2 * nvars + 1)]
        self.units: List[int] = []
        self.empty = -1
        self.interpolant = None
        va = {abs(l) for c in clauses[:n_a] for l in c}
        vb = {abs(l) for c in clauses[n_a:] for l in c}
        self.a_local = va - vb
        label = label or {}
        for pos, c in enumerate(clauses):
            c = list(dict.fromkeys(c))
            if any(-l in c for l in c):
                continue
            cid = len(self.cls)
            self.cls.append(c)
            if pos < n_a:
                f = False
                for l in c:
                    if abs(l) in vb:
                        leaf = label[abs(l)]
                        f = f_or(f, leaf if l > 0 else ("not", leaf))
                self.itp.append(f)
            else:
                self.itp.append(True)
            if not c:
                self.empty = cid
            elif len(c) == 1:
                self.units.append(cid)
            else:
                self.watch[c[0] + nvars].append(cid)
                self.watch[c[1] + nvars].append(cid)

    def _join(self, f, g, pivot: int):
        return f_or(f, g) if pivot in self.a_local else f_and(f, g)

    def value(self, lit: int) -> int:
        v = self.val[abs(lit)]
        return v if lit > 0 else -v

    def _assign(self, lit: int, cid: int) -> None:
        v = abs(lit)
        self.val[v] = 1 if lit > 0 else -1
        self.level[v] = len(self.lim)
        self.reason[v] = cid
        self.trail.append(lit)

    def _propagate(self) -> int:
        n = self.n
        while self.qhead < len(self.trail):
            false_lit = -self.trail[self.qhead]
            self.qhead += 1
            ws = self.watch[false_lit + n]
            keep: List[int] = []
            k = 0
            while k < len(ws):
                cid = ws[k]
                k += 1
                c = self.cls[cid]
                if c[0] == false_lit:
                    c[0], c[1] = c[1], c[0]
                if self.value(c[0]) == 1:
                    keep.append(cid)
                    continue
                for t in range(2, len(c)):
                    if self.value(c[t]) != -1:
                        c[1], c[t] = c[t], c[1]
                        self.watch[c[1] + n].append(cid)
                        break
                else:
                    keep.append(cid)
                    if self.value(c[0]) == -1:
                        keep.extend(ws[k:])
                        self.watch[false_lit + n] = keep
                        return cid
                    self._assign(c[0], cid)
            self.watch[false_lit + n] = keep
        return -1

    def _analyze(self, confl: int):
        """First-UIP clause, its partial interpolant and the backjump level.

        Literals of level 0 stay in the learnt clause, so that the clause is
        exactly the resolvent of the chain and the interpolant matches it.
        """
        seen = set()
        learnt: List[int] = []
        path, p, idx, cid, cur = 0, 0, len(self.trail) - 1, confl, len(self.lim)
        f = self.itp[confl]
        while True:
            for q in self.cls[cid]:
                v = abs(q)
                if q == p or v in seen:
                    continue
                seen.add(v)
                self.act[v] += self.inc
                if self.level[v] == cur:
                    path += 1
                else:
                    learnt.append(q)
            while abs(self.trail[idx]) not in seen:
                idx -= 1
            p = self.trail[idx]
            idx -= 1
            path -= 1
            if path == 0:
                break
            cid = self.reason[abs(p)]
            f = self._join(f, self.itp[cid], abs(p))
        learnt.insert(0, -p)
        bt = 0
        if len(learnt) > 1:
            best = max(range(1, len(learnt)), key=lambda i: self.level[abs(learnt[i])])
            learnt[1], learnt[best] = learnt[best], learnt[1]
            bt = self.level[abs(learnt[1])]
        return learnt, f, bt

    def _final(self, confl: int) -> None:
        """Resolve the conflict at level 0 down to the empty clause."""
        f = self.itp[confl]
        seen = {abs(l) for l in self.cls[confl]}
        for lit in reversed(self.trail):
            v = abs(lit)
            if v in seen:
                cid = self.reason[v]
                f = self._join(f, self.itp[cid], v)
                seen.update(abs(l) for l in self.cls[cid])
        self.interpolant = as_expr(f)

    def _backjump(self, b: int) -> None:
        for lit in self.trail[self.lim[b]:]:
            self.val[abs(lit)] = 0
            self.reason[abs(lit)] = -1
        del self.trail[self.lim[b]:]
        del self.lim[b:]
        self.qhead = len(self.trail)

    def solve(self) -> Optional[List[bool]]:
        """A model, or None when unsatisfiable; then self.interpolant is set."""
        if self.empty >= 0:
            self.interpolant = as_expr(self.itp[self.empty])
            return None
        for cid in self.units:
            lit = self.cls[cid][0]
            if self.value(lit) == -1:
                self._final(cid)
                return None
            if self.value(lit) == 0:
                self._assign(lit, cid)
        while True:
            confl = self._propagate()
            if confl >= 0:
                if not self.lim:
                    self._final(confl)
                    return None
                learnt, f, bt = self._analyze(confl)
                self._backjump(bt)
                cid = len(self.cls)
                self.cls.append(learnt)
                self.itp.append(f)
                if len(learnt) > 1:
                    self.watch[learnt[0] + self.n].append(cid)
                    self.watch[learnt[1] + self.n].append(cid)
                self._assign(learnt[0], cid)
                self.inc *= 1.05
                continue
            best, v = -1.0, 0
            for u in range(1, self.n + 1):
                if self.val[u] == 0 and self.act[u] > best:
                    best, v = self.act[u], u
            if v == 0:
                return [False] + [x == 1 for x in self.val[1:]]
            self.lim.append(len(self.trail))
            self._assign(-v, -1)


def init_expr(circuit):
    """The initial state as a cube expression over the latches."""
    e = ("const", 1)
    for j, b in enumerate(circuit["init"]):
        e = ("and", e, ("x", j) if b else ("not", ("x", j)))
    return e


def implies(circuit, f, g) -> bool:
    """True when the state formula f implies the state formula g."""
    cnf = CNF()
    xs, _ = cnf.frame(circuit)
    cnf.require(cnf.encode(f, xs))
    cnf.require(cnf.gate("not", [cnf.encode(g, xs)]))
    return Solver(cnf.nv, cnf.clauses).solve() is None


def image_query(circuit, r, k: int):
    """Solve A = R(s0) and T(s0, s1), B = T(s1 .. sk) and some not P(sj), j >= 1.

    Return (model, states, inputs, None) when A and B is satisfiable, else
    (None, None, None, J) where J is an interpolant over the latches of s1.
    """
    cnf = CNF()
    s0, i0 = cnf.frame(circuit)
    cnf.require(cnf.encode(r, s0))
    s1, i1 = cnf.frame(circuit)
    cnf.transition(circuit, s0, i0, s1)
    n_a = len(cnf.clauses)
    states, inputs = [s0, s1], [i0, i1]
    for _ in range(k - 1):
        ys, nxt = cnf.frame(circuit)
        cnf.transition(circuit, states[-1], inputs[-1], ys)
        states.append(ys)
        inputs.append(nxt)
    bad = [cnf.gate("not", [cnf.encode(circuit["prop"], xs)]) for xs in states[1:]]
    if not any(b is True for b in bad):
        cnf.clauses.append([b for b in bad if b is not False])
    label = {v: ("x", j) for j, v in enumerate(s1)}
    solver = Solver(cnf.nv, cnf.clauses, n_a, label)
    model = solver.solve()
    if model is None:
        return None, None, None, solver.interpolant  # @line L9
    return model, states, inputs, None


def itp_check(circuit, kmax: int = 64, observer: Optional[Callable] = None):
    """McMillan's loop: grow R by interpolants until a fixed point or a real path."""
    if not evaluate(circuit["prop"], circuit["init"]):  # @line L1
        return "fails", ([tuple(circuit["init"])], [])
    for k in range(1, kmax + 1):  # @line L2
        r = init_expr(circuit)  # @line L3
        exact = True
        while True:  # @line L4
            model, states, inputs, j = image_query(circuit, r, k)  # @line L5
            if model is not None:  # @line L6
                if not exact:
                    break  # @line L8
                read = [tuple(int(model[v]) for v in xs) for xs in states]
                ins = [tuple(int(model[v]) for v in i) for i in inputs]
                end = next(t for t in range(1, len(read)) if not evaluate(circuit["prop"], read[t]))
                return "fails", (read[: end + 1], ins[:end])  # @line L7
            if observer is not None:
                observer(r, j, k)
            if implies(circuit, j, r):  # @line L10
                return "holds", r
            r = ("or", r, j)  # @line L11
            exact = False
    return "unknown", kmax
