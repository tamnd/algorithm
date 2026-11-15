# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/concolic-testing/. The authors are listed in prov/C4AWCW.jsonl.
"""Concolic testing with the depth-first search of DART, on the toy IR.

concolic_run(prog, args) runs prog on concrete arguments and keeps, next to
each concrete value, a symbolic expression over the input symbols. It
returns a Run: the arguments, the outcome, the labels of the blocks visited,
the index of the instruction that trapped (or None) and the list of
conditions. A condition is a pair (e, sense): the run went the way on which
(value of e != 0) equals sense. A br adds its condition. A division or a
remainder adds the implicit condition "divisor != 0", and a shift adds
"0 <= amount <= 63". A condition whose expression is a constant is not
recorded, since no input can change it.

Expressions are tuples: ("in", i) for input i, ("k", c) for a constant and
("op", op, a, b). Operations on two constants are folded.

brute_force_solver(lo, hi) returns a solver that tries every input in the
box [lo, hi]^k in a fixed order. It is exact over the box: it finds a model
in the box whenever one exists. concolic(prog, solve) runs the depth-first
search and returns the list of runs, one per path that it explores.
"""

import itertools

import toyir

_DIV = ("/", "%")
_SHIFT = ("<<", ">>")


class Run:
    __slots__ = ("args", "outcome", "labels", "trap_at", "conds")

    def __init__(self, args, outcome, labels, trap_at, conds):
        self.args = args
        self.outcome = outcome
        self.labels = labels
        self.trap_at = trap_at
        self.conds = conds

    def path(self):
        """The identity of the path: the blocks, the kind of outcome and
        the instruction that trapped, if any."""
        return (self.labels, self.outcome[0], self.trap_at)


def _mk(op, a, b):
    if a[0] == "k" and b[0] == "k":
        return ("k", toyir._binop(op, a[1], b[1]))
    return ("op", op, a, b)


def concolic_run(prog, args, fuel=10000):
    """One run on concrete args, with the symbolic store next to it. Each
    instruction and each terminator uses one unit of fuel, as in toyir.run."""
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
    """The value of expression e on the inputs. Raises toyir._Trap on a
    division by zero or a bad shift. Shared subterms are evaluated once."""
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
    """True when the inputs satisfy every condition. A condition whose
    evaluation traps counts as false."""
    for e, sense in conds:
        try:
            v = evaluate(e, inputs)
        except toyir._Trap:
            return False
        if (v != 0) != sense:
            return False
    return True


def brute_force_solver(lo=-8, hi=8):
    """A solver that tries every input in [lo, hi]^k, in lexicographic order."""

    def solve(conds, k):
        for v in itertools.product(range(lo, hi + 1), repeat=k):
            if holds(conds, v):
                return list(v)
        return None

    return solve


def negate(cond):
    e, sense = cond
    return (e, not sense)


def concolic(prog, solve=None, start=None, fuel=10000, max_runs=100000):
    """The DART search. Returns the list of runs, one per explored path.
    Raises RuntimeError if a run does not follow the prefix that the solver
    was asked for (a divergence); with exact symbolic tracking this does not
    happen."""
    if solve is None:
        solve = brute_force_solver()
    k = len(prog.params)
    v = list(start) if start is not None else [0] * k  # @line L1
    stack = []  # @line L2
    runs = []
    while len(runs) < max_runs:  # @line L3
        r = concolic_run(prog, v, fuel)  # @line L4
        if [c for c, _ in stack] != r.conds[: len(stack)]:
            raise RuntimeError("divergence: the run left the expected prefix")
        for c in r.conds[len(stack):]:  # @line L5
            stack.append((c, False))
        runs.append(r)  # @line L6
        while True:  # @line L7
            if not stack:  # @line L8
                return runs
            c, done = stack[-1]  # @line L9
            if done:  # @line L10
                stack.pop()
                continue
            prefix = [d for d, _ in stack[:-1]]
            model = solve(prefix + [negate(c)], k)  # @line L11
            if model is None:  # @line L12
                stack.pop()
                continue
            stack[-1] = (negate(c), True)  # @line L13
            v = model
            break
    return runs
