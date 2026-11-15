# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generational-search/. The authors are listed in prov/WF74QR.jsonl.
"""Generational search, the search of SAGE, on the toy IR.

concolic_run(prog, args) runs prog on concrete arguments and keeps a
symbolic expression over the input symbols next to each value. It returns a
Run with the arguments, the outcome, the labels of the blocks visited, the
index of the instruction that trapped (or None) and the conditions. A
condition is a pair (e, sense): the run went the way on which
(value of e != 0) equals sense. A br adds its condition, a division or a
remainder adds "divisor != 0", and a shift adds "0 <= amount <= 63".
Conditions with a constant expression are not recorded.

Expressions are tuples: ("in", i), ("k", c) and ("op", op, a, b).

brute_force_solver(lo, hi) returns a solver that is exact over the box
[lo, hi]^k. It changes only the inputs that occur in the conditions and
keeps the others at the values of a hint, the input of the parent run, as
SAGE does. Among the values of a changed input it tries the hint value
first, then the others in increasing order.

generational(prog, solve) runs the search and returns the runs in the
order in which it made them. Each run carries its bound, its parent (an
index into the list, or None), the position it flipped and its score.
"""

import heapq
import itertools

import toyir

_DIV = ("/", "%")
_SHIFT = ("<<", ">>")


class Run:
    __slots__ = ("args", "outcome", "labels", "trap_at", "conds", "bound", "parent", "flip", "score")

    def __init__(self, args, outcome, labels, trap_at, conds):
        self.args = args
        self.outcome = outcome
        self.labels = labels
        self.trap_at = trap_at
        self.conds = conds
        self.bound = 0
        self.parent = None
        self.flip = None
        self.score = 0

    def path(self):
        return (self.labels, self.outcome[0], self.trap_at)


def _mk(op, a, b):
    if a[0] == "k" and b[0] == "k":
        return ("k", toyir._binop(op, a[1], b[1]))
    return ("op", op, a, b)


def concolic_run(prog, args, fuel=10000):
    """One concrete run with the symbolic store next to it. Each instruction
    and each terminator uses one unit of fuel, as in toyir.run."""
    args = list(args)
    if len(args) != len(prog.params):
        raise ValueError("expected %d arguments" % len(prog.params))
    env = dict(zip(prog.params, args))
    sym = {x: ("in", i) for i, x in enumerate(prog.params)}

    def val(a):
        if isinstance(a, int):
            return a
        if a not in env:
            raise toyir.UndefinedName(a)
        return env[a]

    def sval(a):
        return ("k", a) if isinstance(a, int) else sym[a]

    label = prog.entry
    labels = [label]
    conds = []
    while True:
        block = prog.blocks[label]
        for idx, ins in enumerate(block.instrs):
            if fuel <= 0:
                return Run(args, ("fuel",), tuple(labels), None, conds)
            fuel -= 1
            kind = ins[0]
            if kind == "const":
                env[ins[1]] = ins[2]
                sym[ins[1]] = ("k", ins[2])
            elif kind == "copy":
                env[ins[1]] = val(ins[2])
                sym[ins[1]] = sval(ins[2])
            elif kind == "op":
                _, x, op, a, b = ins
                va, vb = val(a), val(b)
                sa, sb = sval(a), sval(b)
                guard = None
                if op in _DIV:
                    guard, ok = sb, vb != 0
                elif op in _SHIFT:
                    guard = _mk("&", _mk("<=", ("k", 0), sb), _mk("<=", sb, ("k", 63)))
                    ok = 0 <= vb <= 63
                if guard is not None:
                    if guard[0] != "k":
                        conds.append((guard, ok))
                    if not ok:
                        return Run(args, ("trap",), tuple(labels), idx, conds)
                env[x] = toyir._binop(op, va, vb)
                sym[x] = _mk(op, sa, sb)
            else:
                raise ValueError("concolic_run handles const, copy and op only, not %r" % (kind,))
        if fuel <= 0:
            return Run(args, ("fuel",), tuple(labels), None, conds)
        fuel -= 1
        t = block.term
        if t[0] == "ret":
            return Run(args, ("ret", val(t[1])), tuple(labels), None, conds)
        if t[0] == "jump":
            label = t[1]
        else:
            taken = val(t[1]) != 0
            s = sval(t[1])
            if s[0] != "k" and t[2] != t[3]:
                conds.append((s, taken))
            label = t[2] if taken else t[3]
        labels.append(label)


def evaluate(e, inputs):
    """The value of e on the inputs; raises toyir._Trap on a bad division
    or shift. Shared subterms are evaluated once."""
    memo = {}

    def ev(e):
        tag = e[0]
        if tag == "k":
            return e[1]
        if tag == "in":
            return inputs[e[1]]
        key = id(e)
        if key not in memo:
            memo[key] = toyir._binop(e[1], ev(e[2]), ev(e[3]))
        return memo[key]

    return ev(e)


def holds(conds, inputs):
    """True when the inputs satisfy every condition; a trap counts as false."""
    for e, sense in conds:
        try:
            v = evaluate(e, inputs)
        except toyir._Trap:
            return False
        if (v != 0) != sense:
            return False
    return True


def inputs_of(conds):
    """The indices of the inputs that occur in the conditions."""
    out = set()
    stack = [e for e, _ in conds]
    seen = set()
    while stack:
        e = stack.pop()
        if id(e) in seen:
            continue
        seen.add(id(e))
        if e[0] == "in":
            out.add(e[1])
        elif e[0] == "op":
            stack.append(e[2])
            stack.append(e[3])
    return sorted(out)


def brute_force_solver(lo=-8, hi=8):
    """A solver that is exact over [lo, hi]^k. Inputs that do not occur in
    the conditions keep their hint values; a changed input tries its hint
    value first. The hint must lie in the box."""

    def solve(conds, k, hint):
        idx = inputs_of(conds)
        orders = [[hint[i]] + [x for x in range(lo, hi + 1) if x != hint[i]] for i in idx]
        v = list(hint)
        for choice in itertools.product(*orders):
            for i, x in zip(idx, choice):
                v[i] = x
            if holds(conds, v):
                return list(v)
        return None

    return solve


def negate(cond):
    e, sense = cond
    return (e, not sense)


def generational(prog, solve=None, start=None, fuel=10000, max_runs=100000):
    """The generational search. Raises RuntimeError on a divergence, which
    exact symbolic tracking rules out."""
    if solve is None:
        solve = brute_force_solver()
    k = len(prog.params)
    v0 = list(start) if start is not None else [0] * k
    first = concolic_run(prog, v0, fuel)  # @line L1
    runs = [first]
    covered = set(first.labels)
    first.score = len(covered)
    work = [(-first.score, 0)]  # @line L2
    while work and len(runs) < max_runs:  # @line L3
        _, i = heapq.heappop(work)  # @line L4
        r = runs[i]
        conds = r.conds  # @line L5
        for j in range(r.bound, len(conds)):  # @line L6
            query = conds[:j] + [negate(conds[j])]
            model = solve(query, k, r.args)  # @line L7
            if model is None:  # @line L8
                continue
            child = concolic_run(prog, model, fuel)  # @line L9
            if child.conds[: j + 1] != query:
                raise RuntimeError("divergence: the run left the expected prefix")
            new = set(child.labels) - covered  # @line L10
            covered |= new
            child.score = len(new)
            child.bound = j + 1  # @line L11
            child.parent = i
            child.flip = j
            runs.append(child)
            heapq.heappush(work, (-child.score, len(runs) - 1))
            if len(runs) >= max_runs:
                break
    return runs
