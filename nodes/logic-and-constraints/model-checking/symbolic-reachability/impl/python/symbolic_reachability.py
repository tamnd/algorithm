# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/symbolic-reachability/. The authors are listed in prov/5F99Q0.jsonl.

"""Symbolic reachability with reduced ordered BDDs.

A circuit is a dict with these keys:
  "init":   a tuple of 0 and 1, the initial value of each latch
  "inputs": the number of free inputs in each step
  "next":   a list of expressions, the next value of each latch
An expression is a nested tuple: ("const", b), ("x", j) for latch j,
("in", j) for input j, ("not", e), ("and", a, b), ("or", a, b), ("xor", a, b).

The BDD variables are ordered as x0 < x0' < x1 < x1' < ... < inputs: the
current value of latch j is variable 2j, its next value is 2j + 1, and the
input t is variable 2L + t, where L is the number of latches. The image of a
set R is the relational product (exists x, i. R(x) and T(x, i, x')), renamed
from x' back to x. Recursion depth is at most the number of variables.
"""

from typing import Dict, List, Sequence, Tuple

OPS = {
    "and": lambda a, b: a & b,
    "or": lambda a, b: a | b,
    "xor": lambda a, b: a ^ b,
    "xnor": lambda a, b: 1 - (a ^ b),
}


class BDD:
    """A store of reduced ordered BDD nodes. Node 0 is false and node 1 is true."""

    def __init__(self, nvars: int) -> None:
        self.nvars = nvars
        self.var: List[int] = [nvars, nvars]
        self.lo: List[int] = [0, 1]
        self.hi: List[int] = [0, 1]
        self.unique: Dict[Tuple[int, int, int], int] = {}
        self.cache: Dict[tuple, int] = {}

    def mk(self, v: int, lo: int, hi: int) -> int:
        if lo == hi:
            return lo
        key = (v, lo, hi)
        u = self.unique.get(key)
        if u is None:
            u = len(self.var)
            self.var.append(v)
            self.lo.append(lo)
            self.hi.append(hi)
            self.unique[key] = u
        return u

    def literal(self, v: int, positive: bool = True) -> int:
        return self.mk(v, 0, 1) if positive else self.mk(v, 1, 0)

    def apply(self, op: str, f: int, g: int) -> int:
        if f <= 1 and g <= 1:
            return OPS[op](f, g)
        key = (op, f, g)
        r = self.cache.get(key)
        if r is not None:
            return r
        v = min(self.var[f], self.var[g])
        f0, f1 = (self.lo[f], self.hi[f]) if self.var[f] == v else (f, f)
        g0, g1 = (self.lo[g], self.hi[g]) if self.var[g] == v else (g, g)
        r = self.mk(v, self.apply(op, f0, g0), self.apply(op, f1, g1))
        self.cache[key] = r
        return r

    def neg(self, f: int) -> int:
        return self.apply("xor", f, 1)

    def exists(self, f: int, qvars: frozenset) -> int:
        if f <= 1:
            return f
        key = ("exists", f, qvars)
        r = self.cache.get(key)
        if r is not None:
            return r
        lo, hi = self.exists(self.lo[f], qvars), self.exists(self.hi[f], qvars)
        r = self.apply("or", lo, hi) if self.var[f] in qvars else self.mk(self.var[f], lo, hi)
        self.cache[key] = r
        return r

    def and_exists(self, f: int, g: int, qvars: frozenset) -> int:
        """The relational product: exists qvars. f and g, without building f and g."""
        if f == 0 or g == 0:
            return 0
        if f == 1 and g == 1:
            return 1
        if f == 1:
            return self.exists(g, qvars)
        if g == 1:
            return self.exists(f, qvars)
        key = ("relprod", f, g, qvars)
        r = self.cache.get(key)
        if r is not None:
            return r
        v = min(self.var[f], self.var[g])
        f0, f1 = (self.lo[f], self.hi[f]) if self.var[f] == v else (f, f)
        g0, g1 = (self.lo[g], self.hi[g]) if self.var[g] == v else (g, g)
        lo = self.and_exists(f0, g0, qvars)
        if v in qvars and lo == 1:
            r = 1
        else:
            hi = self.and_exists(f1, g1, qvars)
            r = self.apply("or", lo, hi) if v in qvars else self.mk(v, lo, hi)
        self.cache[key] = r
        return r

    def rename(self, f: int, shift: int) -> int:
        """Add shift to each variable of f; the caller keeps the order the same."""
        if f <= 1:
            return f
        key = ("rename", f, shift)
        r = self.cache.get(key)
        if r is None:
            r = self.mk(self.var[f] + shift, self.rename(self.lo[f], shift), self.rename(self.hi[f], shift))
            self.cache[key] = r
        return r

    def size(self, f: int) -> int:
        """The number of nodes reachable from f, terminals included."""
        seen, stack = set(), [f]
        while stack:
            u = stack.pop()
            if u not in seen:
                seen.add(u)
                if u > 1:
                    stack += [self.lo[u], self.hi[u]]
        return len(seen)


class SymbolicSystem:
    """The transition relation of a circuit as one BDD, and its image operators."""

    def __init__(self, circuit) -> None:
        self.c = circuit
        self.L = len(circuit["init"])
        self.bdd = BDD(2 * self.L + circuit["inputs"])
        b = self.bdd
        self.cur = frozenset(2 * j for j in range(self.L))
        self.ins = frozenset(2 * self.L + t for t in range(circuit["inputs"]))
        self.nxt = frozenset(2 * j + 1 for j in range(self.L))
        t = 1
        for j, f in enumerate(circuit["next"]):
            t = b.apply("and", t, b.apply("xnor", b.literal(2 * j + 1), self.expr(f)))
        self.trans = t
        self.init = self.cube(circuit["init"])

    def expr(self, e) -> int:
        """BDD of an expression over the current latches and the inputs."""
        b, op = self.bdd, e[0]
        if op == "const":
            return int(bool(e[1]))
        if op == "x":
            return b.literal(2 * e[1])
        if op == "in":
            return b.literal(2 * self.L + e[1])
        if op == "not":
            return b.neg(self.expr(e[1]))
        return b.apply(op, self.expr(e[1]), self.expr(e[2]))

    def cube(self, state: Sequence[int]) -> int:
        f = 1
        for j in reversed(range(self.L)):
            f = self.bdd.mk(2 * j, 0, f) if state[j] else self.bdd.mk(2 * j, f, 0)
        return f

    def image(self, r: int) -> int:
        """Post(R): exists x, i. R(x) and T(x, i, x'), then x' renamed to x."""
        p = self.bdd.and_exists(r, self.trans, self.cur | self.ins)  # @line L9
        return self.bdd.rename(p, -1)  # @line L10

    def preimage(self, r: int) -> int:
        """Pre(R): exists x', i. T(x, i, x') and R(x')."""
        return self.bdd.and_exists(self.trans, self.bdd.rename(r, 1), self.nxt | self.ins)

    def states(self, f: int) -> set:
        """The explicit set of states of a BDD over the current latches."""
        out = set()
        for bits in range(2 ** self.L):
            s = tuple((bits >> (self.L - 1 - j)) & 1 for j in range(self.L))
            u = f
            while u > 1:
                u = self.bdd.hi[u] if s[self.bdd.var[u] // 2] else self.bdd.lo[u]
            if u == 1:
                out.add(s)
        return out


def reachable(system: SymbolicSystem, frontier: bool = True) -> Tuple[int, int]:
    """The BDD of the reachable states, and the number of image computations.

    With frontier, only the states new in the last step are imaged. Both
    forms stop after d + 1 images, where d is the largest BFS distance of a
    reachable state from the initial states.
    """
    b = system.bdd
    r = system.init  # @line L1
    f = r  # @line L2
    images = 0
    while True:  # @line L3
        new = system.image(f if frontier else r)  # @line L4
        images += 1
        f = b.apply("and", new, b.neg(r))  # @line L5
        r = b.apply("or", r, f)  # @line L6
        if f == 0:  # @line L7
            return r, images  # @line L8


def backward_reachable(system: SymbolicSystem, target: int) -> Tuple[int, int]:
    """The BDD of the states that can reach target, and the number of preimages."""
    b = system.bdd
    r = f = target
    images = 0
    while True:
        new = b.apply("and", system.preimage(f), b.neg(r))
        images += 1
        if new == 0:
            return r, images
        r = b.apply("or", r, new)
        f = new


def evaluate(e, xs: Sequence[int], ins: Sequence[int] = ()) -> int:
    """Value (0 or 1) of an expression; used for the explicit reference."""
    op = e[0]
    if op == "const":
        return int(bool(e[1]))
    if op == "x":
        return int(xs[e[1]])
    if op == "in":
        return int(ins[e[1]])
    if op == "not":
        return 1 - evaluate(e[1], xs, ins)
    return OPS[op](evaluate(e[1], xs, ins), evaluate(e[2], xs, ins))


def step(circuit, xs: Sequence[int], ins: Sequence[int]) -> Tuple[int, ...]:
    return tuple(evaluate(f, xs, ins) for f in circuit["next"])
