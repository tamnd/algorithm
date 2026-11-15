# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/worklist-dataflow-algorithm/. The authors are listed in prov/5353DC.jsonl.
"""The worklist dataflow algorithm (Kildall 1973) on the toy IR.

The lattice uses the meet convention of Kildall and the dragon book: top is
the identity of meet and the start value, and the result is the maximal
fixed point (MFP). A backward problem runs the same solver on the reverse
CFG, with the ret blocks as start nodes.

Five analyses are given: reaching definitions, live variables, available
expressions and very busy expressions (gen-kill problems on frozensets),
and constant propagation (a flat lattice per variable, not distributive).
"""

from collections import deque

from toyir import defs, preds, succs, term_uses, uses

TOP = "top"  # constant propagation: no value seen yet
NAC = "nac"  # constant propagation: not a constant (bottom)


def worklist(nodes, succ, starts, boundary, top, meet, transfer, order=None):
    """Solve IN[s] = (boundary if s is a start else top) meet the meet over
    the edges (n, s) of transfer(n, IN[n]), for the greatest solution.

    nodes: the nodes; succ: dict node -> list of successors in the direction
    of the analysis; starts: the start nodes. Returns (IN, stats), where
    stats counts transfer applications, meets and changes of IN."""
    order = list(nodes) if order is None else list(order)
    inn = {n: top for n in nodes}  # @line L1
    for s in starts:
        inn[s] = boundary  # @line L2
    work = deque(order)  # @line L3
    queued = set(order)
    stats = {"transfers": 0, "meets": 0, "changes": 0}
    changes = {n: 0 for n in nodes}
    while work:  # @line L4
        n = work.popleft()  # @line L5
        queued.discard(n)
        out = transfer(n, inn[n])  # @line L6
        stats["transfers"] += 1
        for s in succ[n]:  # @line L7
            new = meet(inn[s], out)  # @line L8
            stats["meets"] += 1
            if new != inn[s]:  # @line L9
                inn[s] = new  # @line L10
                changes[s] += 1
                stats["changes"] += 1
                if s not in queued:  # @line L11
                    work.append(s)
                    queued.add(s)
    stats["max_changes"] = max(changes.values(), default=0)
    return inn, stats


def reverse_postorder(nodes, succ, starts):
    """Nodes in reverse postorder of a DFS from the starts; nodes that the
    starts do not reach come last, in their given order."""
    seen, post = set(), []
    for root in starts:
        if root in seen:
            continue
        seen.add(root)
        stack = [(root, iter(succ[root]))]
        while stack:
            v, it = stack[-1]
            w = next(it, None)
            if w is None:
                post.append(v)
                stack.pop()
            elif w not in seen:
                seen.add(w)
                stack.append((w, iter(succ[w])))
    order = post[::-1]
    return order + [n for n in nodes if n not in seen]


def graph(prog, forward):
    """The CFG in the direction of the analysis: (nodes, succ, starts)."""
    nodes = list(prog.blocks)
    if forward:
        return nodes, {n: succs(prog, n) for n in nodes}, [prog.entry]
    p = preds(prog)
    exits = [n for n in nodes if prog.blocks[n].term[0] == "ret"]
    return nodes, {n: p[n] for n in nodes}, exits


def solve(prog, an):
    """Run the worklist algorithm for the analysis an. Returns (IN, OUT,
    stats) in CFG terms: IN[L] holds at the start of block L, OUT[L] at its
    end, for forward and backward problems alike."""
    nodes, succ, starts = graph(prog, an.forward)
    order = reverse_postorder(nodes, succ, starts)
    before, stats = worklist(nodes, succ, starts, an.boundary, an.top, an.meet, an.transfer, order)
    after = {n: an.transfer(n, before[n]) for n in nodes}
    if an.forward:
        return before, after, stats
    return after, before, stats


# ------------------------------------------------------------ gen-kill problems


def compose(first, second):
    """The gen-kill pair of second after first: gen2 | (gen1 - kill2),
    kill1 | kill2."""
    g1, k1 = first
    g2, k2 = second
    return g2 | (g1 - k2), k1 | k2


class GenKill:
    """A gen-kill problem. step(label, i, ins) gives the gen-kill pair of
    one instruction (ins is None for the terminator); the block pair is the
    composition in the direction of the analysis."""

    def __init__(self, prog, forward, must, universe, step, boundary=frozenset()):
        self.prog = prog
        self.forward = forward
        self.must = must
        self.universe = frozenset(universe)
        self.top = self.universe if must else frozenset()
        self.boundary = frozenset(boundary)
        self.height = len(self.universe)
        self.step = step
        self.block = {}
        for label, b in prog.blocks.items():
            items = [(i, ins) for i, ins in enumerate(b.instrs)] + [(len(b.instrs), None)]
            if not forward:
                items.reverse()
            pair = (frozenset(), frozenset())
            for i, ins in items:
                g, k = step(label, i, ins)
                pair = compose(pair, (frozenset(g), frozenset(k)))
            self.block[label] = pair

    def meet(self, a, b):
        return a & b if self.must else a | b

    def transfer(self, label, x):
        g, k = self.block[label]
        return g | (x - k)

    def leq(self, a, b):
        return self.meet(a, b) == a


def _check(prog):
    for b in prog.blocks.values():
        for ins in b.instrs:
            if ins[0] not in ("const", "copy", "op"):
                raise ValueError("these analyses take const, copy and op only")


def names(prog):
    out = list(prog.params)
    for b in prog.blocks.values():
        for ins in b.instrs:
            for a in uses(ins) + [defs(ins)]:
                if a not in out:
                    out.append(a)
        for a in term_uses(b.term):
            if a not in out:
                out.append(a)
    return out


def expressions(prog):
    """The expressions (op, a, b) of the program, in program order."""
    out = []
    for b in prog.blocks.values():
        for ins in b.instrs:
            if ins[0] == "op" and ins[2:] not in out:
                out.append(ins[2:])
    return out


def reaching_definitions(prog):
    """Forward, may. A definition is the pair (label, index)."""
    _check(prog)
    sites = [(lab, i) for lab, b in prog.blocks.items() for i in range(len(b.instrs))]
    by_var = {}
    for lab, i in sites:
        by_var.setdefault(defs(prog.blocks[lab].instrs[i]), set()).add((lab, i))

    def step(label, i, ins):
        if ins is None:
            return set(), set()
        return {(label, i)}, by_var[defs(ins)] - {(label, i)}

    return GenKill(prog, True, False, sites, step)


def live_variables(prog):
    """Backward, may. A fact is a variable name."""
    _check(prog)

    def step(label, i, ins):
        if ins is None:
            return set(term_uses(prog.blocks[label].term)), set()
        return set(uses(ins)), {defs(ins)}

    return GenKill(prog, False, False, names(prog), step)


def _killed(exprs, x):
    return {e for e in exprs if x in (e[1], e[2])}


def available_expressions(prog):
    """Forward, must. A fact is an expression (op, a, b)."""
    _check(prog)
    exprs = expressions(prog)

    def step(label, i, ins):
        if ins is None:
            return set(), set()
        kill = _killed(exprs, defs(ins))
        gen = {ins[2:]} - kill if ins[0] == "op" else set()
        return gen, kill

    return GenKill(prog, True, True, exprs, step)


def very_busy_expressions(prog):
    """Backward, must. A fact is an expression (op, a, b)."""
    _check(prog)
    exprs = expressions(prog)

    def step(label, i, ins):
        if ins is None:
            return set(), set()
        kill = _killed(exprs, defs(ins))
        gen = {ins[2:]} if ins[0] == "op" else set()
        return gen, kill

    return GenKill(prog, False, True, exprs, step)


# --------------------------------------------------------- constant propagation


def flat_meet(a, b):
    if a == TOP:
        return b
    if b == TOP or a == b:
        return a
    return NAC


def fold(op, a, b):
    """The abstract value of a op b on the flat lattice."""
    if a == NAC or b == NAC:
        return NAC
    if a == TOP or b == TOP:
        return TOP
    if op in ("/", "%") and b == 0:
        return NAC  # the program traps here; NAC is a safe answer
    if op in ("<<", ">>") and not 0 <= b <= 63:
        return NAC
    if op in ("/", "%"):
        q = abs(a) // abs(b)
        if (a < 0) != (b < 0):
            q = -q
        return q if op == "/" else a - b * q
    table = {
        "+": lambda: a + b, "-": lambda: a - b, "*": lambda: a * b,
        "&": lambda: a & b, "|": lambda: a | b, "^": lambda: a ^ b,
        "<<": lambda: a << b, ">>": lambda: a >> b,
        "<": lambda: int(a < b), "<=": lambda: int(a <= b),
        "==": lambda: int(a == b), "!=": lambda: int(a != b),
    }
    return table[op]()


class ConstantPropagation:
    """Forward. A value is a tuple with one flat-lattice entry per name.
    Parameters start as NAC, the other names as TOP (not yet defined)."""

    forward = True

    def __init__(self, prog):
        _check(prog)
        self.prog = prog
        self.vars = names(prog)
        self.index = {x: i for i, x in enumerate(self.vars)}
        self.top = tuple(TOP for _ in self.vars)
        self.boundary = tuple(NAC if x in prog.params else TOP for x in self.vars)
        self.height = 2 * len(self.vars)

    def meet(self, a, b):
        return tuple(flat_meet(x, y) for x, y in zip(a, b))

    def leq(self, a, b):
        return self.meet(a, b) == a

    def value(self, env, a):
        return a if isinstance(a, int) else env[self.index[a]]

    def step(self, env, ins):
        env = list(env)
        k, x = ins[0], ins[1]
        if k == "const":
            env[self.index[x]] = ins[2]
        elif k == "copy":
            env[self.index[x]] = self.value(env, ins[2])
        else:
            env[self.index[x]] = fold(ins[2], self.value(env, ins[3]), self.value(env, ins[4]))
        return tuple(env)

    def transfer(self, label, env):
        for ins in self.prog.blocks[label].instrs:
            env = self.step(env, ins)
        return env


def constant_propagation(prog):
    return ConstantPropagation(prog)


ANALYSES = {
    "reaching-definitions": reaching_definitions,
    "live-variables": live_variables,
    "available-expressions": available_expressions,
    "very-busy-expressions": very_busy_expressions,
    "constant-propagation": constant_propagation,
}
