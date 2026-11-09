# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-induction/. The authors are listed in prov/ZHFE5T.jsonl.

"""k-induction with simple path constraints (Sheeran, Singh and Stalmarck 2000).

A circuit is a dict with these keys:
  "init":   a tuple of 0 and 1, the initial value of each latch
  "inputs": the number of free inputs in each step
  "next":   a list of expressions, the next value of each latch
  "prop":   an expression over the latches, the property P
An expression is a nested tuple: ("const", b), ("x", j) for latch j,
("in", j) for input j, ("not", e), ("and", a, b), ("or", a, b), ("xor", a, b).

k_induction returns ("holds", k) when P is an invariant, proved by the
step case at depth k; ("fails", (states, inputs)) with a shortest
counterexample; or ("unknown", kmax) when the bound runs out.
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


def _path(circuit, k: int, initial: bool):
    """CNF of a path s0 .. sk, with I(s0) when initial is true."""
    cnf = CNF()
    xs, ins = cnf.frame(circuit)
    states, inputs = [xs], [ins]
    if initial:
        for j, b in enumerate(circuit["init"]):
            cnf.clauses.append([xs[j] if b else -xs[j]])
    for _ in range(k):
        ys, nxt = cnf.frame(circuit)
        cnf.transition(circuit, states[-1], inputs[-1], ys)
        states.append(ys)
        inputs.append(nxt)
    return cnf, states, inputs


def base_case(circuit, k: int):
    """A path of exactly k steps from I to a state where P is false, or None."""
    cnf, states, inputs = _path(circuit, k, True)
    cnf.require(cnf.gate("not", [cnf.encode(circuit["prop"], states[k])]))
    model = Solver(cnf.nv, cnf.clauses).solve()
    if model is None:
        return None
    read = lambda fs: [tuple(int(model[v]) for v in f) for f in fs]
    return read(states), read(inputs[:k])


def step_case(circuit, k: int, simple_path: bool = True) -> bool:
    """True when P(s0), ..., P(sk) and T imply P(s(k+1)) on all paths.

    With simple_path, only paths whose k + 2 states are pairwise different
    count, which makes the check succeed for some k on each finite system
    where P is an invariant.
    """
    cnf, states, _ = _path(circuit, k + 1, False)
    for xs in states[:-1]:
        cnf.require(cnf.encode(circuit["prop"], xs))
    cnf.require(cnf.gate("not", [cnf.encode(circuit["prop"], states[-1])]))  # @line L4
    if simple_path:
        for i in range(len(states)):
            for j in range(i + 1, len(states)):
                cnf.clauses.append([cnf.gate("xor", [a, b]) for a, b in zip(states[i], states[j])])  # @line L5
    return Solver(cnf.nv, cnf.clauses).solve() is None


def k_induction(circuit, kmax: int, simple_path: bool = True):
    """Run the base case and the step case for k = 0, 1, ..., kmax."""
    for k in range(kmax + 1):  # @line L1
        cex = base_case(circuit, k)  # @line L2
        if cex is not None:
            return "fails", cex  # @line L3
        if step_case(circuit, k, simple_path):  # @line L6
            return "holds", k  # @line L7
    return "unknown", kmax  # @line L8
