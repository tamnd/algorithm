# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sat-based-bounded-model-checking/. The authors are listed in prov/3TYGHB.jsonl.

"""SAT-based bounded model checking (Biere, Cimatti, Clarke and Zhu 1999).

A circuit is a dict with these keys:
  "init":   a tuple of 0 and 1, the initial value of each latch
  "inputs": the number of free inputs in each step
  "next":   a list of expressions, the next value of each latch
  "prop":   an expression over the latches, the property P
An expression is a nested tuple: ("const", b), ("x", j) for latch j,
("in", j) for input j, ("not", e), ("and", a, b), ("or", a, b), ("xor", a, b).

bmc_safety looks for the shortest path from the initial state to a state
where P is false. bmc_lasso looks for a lasso on which q is never true, that
is a counterexample to the liveness property F q. Both build a CNF formula
with the Tseitin encoding and solve it with the small CDCL solver below.
"""

from typing import Dict, List, Optional, Sequence, Tuple


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
    """CDCL: two watched literals, first-UIP learning, activity-based decisions."""

    def __init__(self, nvars: int, clauses: List[List[int]]) -> None:
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
        self.watch: List[List[int]] = [[] for _ in range(2 * nvars + 1)]
        self.units: List[int] = []
        self.ok = True
        for c in clauses:
            c = list(dict.fromkeys(c))
            if any(-l in c for l in c):
                continue
            cid = len(self.cls)
            self.cls.append(c)
            if not c:
                self.ok = False
            elif len(c) == 1:
                self.units.append(cid)
            else:
                self.watch[c[0] + nvars].append(cid)
                self.watch[c[1] + nvars].append(cid)

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

    def _analyze(self, confl: int) -> Tuple[List[int], int]:
        seen = set()
        learnt: List[int] = []
        path, p, idx, cid, cur = 0, 0, len(self.trail) - 1, confl, len(self.lim)
        while True:
            for q in self.cls[cid]:
                v = abs(q)
                if q == p or v in seen:
                    continue
                seen.add(v)
                self.act[v] += self.inc
                if self.level[v] == cur:
                    path += 1
                elif self.level[v] > 0:
                    learnt.append(q)
            while abs(self.trail[idx]) not in seen:
                idx -= 1
            p = self.trail[idx]
            idx -= 1
            path -= 1
            if path == 0:
                break
            cid = self.reason[abs(p)]
        learnt.insert(0, -p)
        bt = 0
        if len(learnt) > 1:
            best = max(range(1, len(learnt)), key=lambda i: self.level[abs(learnt[i])])
            learnt[1], learnt[best] = learnt[best], learnt[1]
            bt = self.level[abs(learnt[1])]
        return learnt, bt

    def _backjump(self, b: int) -> None:
        for lit in self.trail[self.lim[b]:]:
            self.val[abs(lit)] = 0
            self.reason[abs(lit)] = -1
        del self.trail[self.lim[b]:]
        del self.lim[b:]
        self.qhead = len(self.trail)

    def solve(self) -> Optional[List[bool]]:
        """A model as a list indexed by variable, or None when unsatisfiable."""
        if not self.ok:
            return None
        for cid in self.units:
            lit = self.cls[cid][0]
            if self.value(lit) == -1:
                return None
            if self.value(lit) == 0:
                self._assign(lit, cid)
        while True:
            confl = self._propagate()
            if confl >= 0:
                if not self.lim:
                    return None
                learnt, bt = self._analyze(confl)
                self._backjump(bt)
                cid = len(self.cls)
                self.cls.append(learnt)
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


def unroll(circuit, k: int) -> Tuple[CNF, List[List[int]], List[List[int]]]:
    """CNF of I(s0) and T(s0, s1) and ... and T(s(k-1), sk), with the frames."""
    cnf = CNF()
    xs, ins = cnf.frame(circuit)
    states, inputs = [xs], [ins]
    for j, b in enumerate(circuit["init"]):
        cnf.clauses.append([xs[j] if b else -xs[j]])
    for _ in range(k):
        ys, nxt = cnf.frame(circuit)
        cnf.transition(circuit, states[-1], inputs[-1], ys)
        states.append(ys)
        inputs.append(nxt)
    return cnf, states, inputs


def _read(model, frames) -> List[Tuple[int, ...]]:
    return [tuple(int(model[v]) for v in f) for f in frames]


def bmc_safety(circuit, kmax: int):
    """Shortest counterexample (states, inputs) of length at most kmax, or None.

    states[0] is the initial state, states[i+1] = step(states[i], inputs[i]),
    and P is false in states[-1] and true in all earlier states.
    """
    for k in range(kmax + 1):  # @line L1
        cnf, states, inputs = unroll(circuit, k)  # @line L2
        cnf.require(cnf.gate("not", [cnf.encode(circuit["prop"], states[k])]))  # @line L3
        model = Solver(cnf.nv, cnf.clauses).solve()
        if model is not None:  # @line L4
            return _read(model, states), _read(model, inputs[:k])  # @line L5
    return None  # @line L6


def bmc_lasso(circuit, q, kmax: int):
    """A lasso (states, inputs, l) on which q is false in each state, or None.

    The path states[0..k] starts in the initial state, and the input
    inputs[k] leads from states[k] back to states[l]. The lasso is an
    infinite path on which q never holds, a counterexample to F q.
    """
    for k in range(kmax + 1):  # @line L7
        cnf, states, inputs = unroll(circuit, k)  # @line L8
        for xs in states:
            cnf.require(cnf.gate("not", [cnf.encode(q, xs)]))  # @line L9
        back = [cnf.new() for _ in circuit["init"]]
        cnf.transition(circuit, states[k], inputs[k], back)
        loops = []
        for l in range(k + 1):
            e = cnf.new()
            loops.append(e)
            for a, b in zip(back, states[l]):
                cnf.clauses += [[-e, -a, b], [-e, a, -b]]  # @line L10
        cnf.clauses.append(loops)  # @line L11
        model = Solver(cnf.nv, cnf.clauses).solve()
        if model is not None:  # @line L12
            l = next(i for i, e in enumerate(loops) if model[e])
            return _read(model, states), _read(model, inputs), l  # @line L13
    return None  # @line L14
