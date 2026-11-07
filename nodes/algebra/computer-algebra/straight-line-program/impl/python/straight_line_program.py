# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/straight-line-program/. The authors are listed in prov/JGQ9GZ.jsonl.
"""Straight-line programs for polynomials in K[x_1, ..., x_n].

A program is a list of instructions. Instruction j is one of
    ("var", i)        the input x_i, 0 <= i < n
    ("const", c)      a constant of K
    ("+", a, b), ("-", a, b), ("*", a, b)   with a, b < j
The value of the program is the value of its last instruction. The length L
is the number of instructions. Coefficients can be Python ints, Fractions,
or ints mod p (pass p to the functions that take it).

Cost model: operations in K. Evaluation costs L operations, the degree bound
O(L) integer operations, the gradient (reverse mode, Baur and Strassen) at
most 5 L operations, and expansion can cost exponential time in L because
the dense or sparse form can have exponentially many terms.
"""

from __future__ import annotations

import random


class SLP:
    def __init__(self, n: int):
        self.n = n
        self.ins: list = []

    def _push(self, ins) -> int:
        self.ins.append(ins)
        return len(self.ins) - 1

    def var(self, i: int) -> int:
        assert 0 <= i < self.n
        return self._push(("var", i))

    def const(self, c) -> int:
        return self._push(("const", c))

    def op(self, o: str, a: int, b: int) -> int:
        assert o in "+-*" and 0 <= a < len(self.ins) and 0 <= b < len(self.ins)
        return self._push((o, a, b))

    def __len__(self) -> int:
        return len(self.ins)


def evaluate(prog: SLP, point: list, p: int | None = None):
    """Value at point; one pass over the instructions."""
    val = []  # @line L1
    for ins in prog.ins:  # @line L2
        k = ins[0]  # @line L3
        if k == "var":
            v = point[ins[1]]
        elif k == "const":
            v = ins[1]
        else:
            a, b = val[ins[1]], val[ins[2]]
            v = a + b if k == "+" else a - b if k == "-" else a * b
        if p is not None:
            v %= p
        val.append(v)  # @line L4
    return val[-1] if val else 0  # @line L5


def degree_bound(prog: SLP) -> list:
    """Upper bounds for the total degree of every instruction (-1 for zero constants)."""
    deg = []
    for ins in prog.ins:
        k = ins[0]
        if k == "var":
            deg.append(1)
        elif k == "const":
            deg.append(0 if ins[1] != 0 else -1)
        elif k == "*":
            a, b = deg[ins[1]], deg[ins[2]]
            deg.append(-1 if a < 0 or b < 0 else a + b)
        else:
            deg.append(max(deg[ins[1]], deg[ins[2]]))
    return deg


def expand(prog: SLP, p: int | None = None, max_terms: int = 10**5) -> dict:
    """The polynomial as {exponent tuple: coefficient}; raises if it grows too big."""
    n = prog.n
    polys = []
    for ins in prog.ins:
        k = ins[0]
        if k == "var":
            e = [0] * n
            e[ins[1]] = 1
            f = {tuple(e): 1}
        elif k == "const":
            f = {(0,) * n: ins[1]} if ins[1] else {}
        elif k in "+-":
            f = dict(polys[ins[1]])
            s = 1 if k == "+" else -1
            for e, c in polys[ins[2]].items():
                f[e] = f.get(e, 0) + s * c
        else:
            f = {}
            for e1, c1 in polys[ins[1]].items():
                for e2, c2 in polys[ins[2]].items():
                    e = tuple(x + y for x, y in zip(e1, e2))
                    f[e] = f.get(e, 0) + c1 * c2
        if p is not None:
            f = {e: c % p for e, c in f.items()}
        f = {e: c for e, c in f.items() if c != 0}
        if len(f) > max_terms:
            raise OverflowError("expanded form too large")
        polys.append(f)
    return polys[-1] if polys else {}


def gradient(prog: SLP, point: list, p: int | None = None) -> list:
    """All partial derivatives at point, by the reverse mode (Baur and Strassen)."""
    val = []
    for ins in prog.ins:  # forward pass  # @line G1
        k = ins[0]
        if k == "var":
            v = point[ins[1]]
        elif k == "const":
            v = ins[1]
        else:
            a, b = val[ins[1]], val[ins[2]]
            v = a + b if k == "+" else a - b if k == "-" else a * b
        val.append(v % p if p is not None else v)
    L = len(prog.ins)
    adj = [0] * L  # adj[j] = d(output) / d(value of j)
    grad = [0] * prog.n  # @line G2
    if L == 0:
        return grad
    adj[-1] = 1  # @line G3
    for j in range(L - 1, -1, -1):  # backward pass  # @line G4
        g = adj[j]
        if p is not None:
            g %= p
        if g == 0:
            continue
        ins = prog.ins[j]
        k = ins[0]
        if k == "var":
            grad[ins[1]] += g  # @line G5
        elif k == "+":  # @line G6
            adj[ins[1]] += g
            adj[ins[2]] += g
        elif k == "-":
            adj[ins[1]] += g
            adj[ins[2]] -= g
        elif k == "*":  # @line G7
            adj[ins[1]] += g * val[ins[2]]
            adj[ins[2]] += g * val[ins[1]]
    return [x % p for x in grad] if p is not None else grad  # @line G8


def is_zero(prog: SLP, p: int, rng: random.Random, trials: int = 20) -> bool:
    """Randomized zero test over Z/pZ (Schwartz-Zippel).

    A nonzero program of degree at most D < p is reported zero with
    probability at most (D / p)^trials. A zero program is always reported
    zero.
    """
    for _ in range(trials):
        pt = [rng.randrange(p) for _ in range(prog.n)]
        if evaluate(prog, pt, p) != 0:
            return False
    return True


def compose(outer: SLP, inner: list) -> SLP:
    """outer(g_1, ..., g_m) for programs g_i in the same n variables.

    The length is at most the sum of the lengths plus 2.
    """
    assert len(inner) == outer.n and inner and all(len(g) for g in inner)
    n = inner[0].n
    res = SLP(n)
    outs = []
    for g in inner:
        base = len(res.ins)
        for ins in g.ins:
            if ins[0] in "+-*":
                res.ins.append((ins[0], ins[1] + base, ins[2] + base))
            else:
                res.ins.append(ins)
        outs.append(len(res.ins) - 1)
    where = []  # index in res of each instruction of outer
    for ins in outer.ins:
        if ins[0] == "var":
            where.append(outs[ins[1]])  # reuse g_i, no new instruction
        elif ins[0] == "const":
            where.append(res._push(ins))
        else:
            where.append(res._push((ins[0], where[ins[1]], where[ins[2]])))
    if not where:
        res.const(0)
    elif where[-1] != len(res.ins) - 1:  # the output must be last
        res._push(("+", where[-1], res.const(0)))
    return res
