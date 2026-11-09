# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ic3-pdr/. The authors are listed in prov/S90VY0.jsonl.

"""IC3 / property-directed reachability (Bradley 2011; Een, Mishchenko and Brayton 2011).

A circuit is a dict with these keys:
  "init":   a tuple of 0 and 1, the initial value of each latch
  "inputs": the number of free inputs in each step
  "next":   a list of expressions, the next value of each latch
  "prop":   an expression over the latches, the property P
An expression is a nested tuple: ("const", b), ("x", j) for latch j,
("in", j) for input j, ("not", e), ("and", a, b), ("or", a, b), ("xor", a, b).

A frame clause is a frozenset of nonzero ints over the latches: +(j+1)
means "latch j is 1" and -(j+1) means "latch j is 0". frames[0] stands for
the initial state I, and frames[i] for i >= 1 is a set of clauses, the frame
F_i. Clause sets shrink with i, so the state sets F_i grow with i.

ic3 returns ("holds", invariant) with a set of clauses that is inductive
and implies P, or ("fails", (states, inputs)) with a counterexample.
"""

from typing import Callable, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple


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


Clause = FrozenSet[int]


def _lit(xs: List[int], l: int) -> int:
    return xs[l - 1] if l > 0 else -xs[-l - 1]


def cube_of(state: Sequence[int]) -> Tuple[int, ...]:
    """The full cube of a state: one literal for each latch."""
    return tuple((j + 1) if b else -(j + 1) for j, b in enumerate(state))


class IC3:
    def __init__(self, circuit, observer: Optional[Callable] = None) -> None:
        self.c = circuit
        self.init = tuple(circuit["init"])
        self.frames: List[Optional[Set[Clause]]] = [None, set()]
        self.observer = observer
        self.queries = 0

    def _frame_cnf(self, i: int):
        """CNF with the frame F_i on fresh state variables xs."""
        cnf = CNF()
        xs, ins = cnf.frame(self.c)
        if i == 0:
            for j, b in enumerate(self.init):
                cnf.clauses.append([xs[j] if b else -xs[j]])
        else:
            for cl in self.frames[i]:
                cnf.clauses.append([_lit(xs, l) for l in cl])
        return cnf, xs, ins

    def _solve(self, cnf: CNF):
        self.queries += 1
        return Solver(cnf.nv, cnf.clauses).solve()

    def bad_state(self, i: int) -> Optional[Tuple[int, ...]]:
        """A state of F_i where P is false, or None."""
        cnf, xs, _ = self._frame_cnf(i)
        cnf.require(cnf.gate("not", [cnf.encode(self.c["prop"], xs)]))
        m = self._solve(cnf)
        return None if m is None else tuple(int(m[v]) for v in xs)

    def predecessor(self, i: int, cube: Sequence[int]):
        """A pair (state, input) for the query F_i and not cube and T and cube', or None."""
        cnf, xs, ins = self._frame_cnf(i)
        ys = [cnf.new() for _ in xs]
        cnf.transition(self.c, xs, ins, ys)
        cnf.clauses.append([-_lit(xs, l) for l in cube])
        for l in cube:
            cnf.clauses.append([_lit(ys, l)])
        m = self._solve(cnf)
        if m is None:
            return None
        return tuple(int(m[v]) for v in xs), tuple(int(m[v]) for v in ins)

    def _initial_in(self, cube: Sequence[int]) -> bool:
        return all((self.init[abs(l) - 1] == 1) == (l > 0) for l in cube)

    def generalize(self, cube: Sequence[int], i: int) -> Tuple[int, ...]:
        """Drop literals while the cube misses I and stays inductive relative to F_(i-1)."""
        cube = list(cube)
        for l in list(cube):
            if len(cube) == 1:
                break
            trial = [x for x in cube if x != l]
            if not self._initial_in(trial) and self.predecessor(i - 1, trial) is None:
                cube = trial
        return tuple(cube)

    def _add(self, clause: Clause, i: int) -> None:
        for j in range(1, i + 1):
            self.frames[j].add(clause)
        self._notify()

    def _notify(self) -> None:
        if self.observer is not None:
            self.observer(self.frames, len(self.frames) - 1)

    def block(self, s: Tuple[int, ...], k: int):
        """Block the bad state s at level k; return a counterexample or None."""
        stack = [(s, k, None)]  # @line L11
        while stack:  # @line L12
            t, i, _ = stack[-1]  # @line L13
            pred = self.predecessor(i - 1, cube_of(t))
            if pred is None:  # @line L14
                g = self.generalize(cube_of(t), i)  # @line L15
                self._add(frozenset(-l for l in g), i)  # @line L16
                stack.pop()
                continue
            u, inp = pred  # @line L17
            if i - 1 == 0 or u == self.init:  # @line L18
                states = [u] + [e[0] for e in reversed(stack)]
                inputs = [inp] + [e[2] for e in reversed(stack[1:])]
                return states, inputs
            stack.append((u, i - 1, inp))  # @line L19
        return None  # @line L20

    def push_ok(self, i: int, clause: Clause) -> bool:
        """True when F_i and T imply clause in the next state."""
        cnf, xs, ins = self._frame_cnf(i)
        ys = [cnf.new() for _ in xs]
        cnf.transition(self.c, xs, ins, ys)
        for l in clause:
            cnf.clauses.append([-_lit(ys, l)])
        return self._solve(cnf) is None

    def run(self, max_frames: int = 1000):
        if not evaluate(self.c["prop"], self.init):  # @line L1
            return "fails", ([self.init], [])
        k = 1  # @line L2
        while k <= max_frames:  # @line L3
            while True:
                s = self.bad_state(k)  # @line L4
                if s is None:
                    break
                cex = self.block(s, k)  # @line L5
                if cex is not None:
                    return "fails", cex
            self.frames.append(set())  # @line L6
            k += 1
            self._notify()
            for i in range(1, k):  # @line L7
                for cl in sorted(self.frames[i] - self.frames[i + 1], key=sorted):  # @line L8
                    if self.push_ok(i, cl):  # @line L9
                        self.frames[i + 1].add(cl)
                        self._notify()
                if self.frames[i] == self.frames[i + 1]:  # @line L10
                    return "holds", set(self.frames[i])
        return "unknown", k


def ic3(circuit, observer: Optional[Callable] = None):
    """Run IC3 on the circuit; see the module docstring for the result."""
    return IC3(circuit, observer).run()
