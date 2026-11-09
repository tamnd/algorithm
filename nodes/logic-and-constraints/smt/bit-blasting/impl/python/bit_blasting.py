# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bit-blasting/. The authors are listed in prov/65V2ET.jsonl.

"""Bit-blasting of fixed-width bit-vector formulas into CNF, with a small DPLL solver.

All terms have the same width w. A bit-vector is a list of w literals, least
significant bit first. A literal is a nonzero int in DIMACS style; variable 1 is
the constant true, so the literal 1 is true and -1 is false. Each gate gets a
fresh variable and the Tseitin clauses of its definition.

Terms: ("var", name), ("const", k), ("not", t), ("neg", t), ("and", s, t),
("or", s, t), ("xor", s, t), ("add", s, t), ("sub", s, t), ("mul", s, t),
("shl", t, k), ("lshr", t, k) with a constant k.
Atoms: ("eq", s, t), ("ult", s, t), ("ule", s, t), ("slt", s, t).
Formulas: atoms, ("band", f, g), ("bor", f, g), ("bnot", f), ("true",).
"""

from __future__ import annotations

TRUE = 1


class Blaster:
    """Build a circuit gate by gate and collect its clauses."""

    def __init__(self, w: int) -> None:
        self.w = w
        self.nvars = 1
        self.clauses: list[list[int]] = [[TRUE]]
        self.gates: list[tuple[int, str, int, int]] = []
        self.vars: dict[str, list[int]] = {}

    def fresh(self) -> int:
        self.nvars += 1
        return self.nvars

    # Gates with constant folding; each new gate y gets the clauses of y <-> op(a, b).
    def and2(self, a: int, b: int) -> int:
        if a == -TRUE or b == -TRUE or a == -b:
            return -TRUE
        if a == TRUE or a == b:
            return b
        if b == TRUE:
            return a
        y = self.fresh()
        self.clauses += [[-y, a], [-y, b], [y, -a, -b]]
        self.gates.append((y, "and", a, b))
        return y

    def or2(self, a: int, b: int) -> int:
        return -self.and2(-a, -b)

    def xor2(self, a: int, b: int) -> int:
        if a == -TRUE:
            return b
        if b == -TRUE:
            return a
        if a == TRUE:
            return -b
        if b == TRUE:
            return -a
        if a == b:
            return -TRUE
        if a == -b:
            return TRUE
        y = self.fresh()
        self.clauses += [[-y, a, b], [-y, -a, -b], [y, -a, b], [y, a, -b]]
        self.gates.append((y, "xor", a, b))
        return y

    # Word-level circuits.
    def variable(self, name: str) -> list[int]:
        if name not in self.vars:
            self.vars[name] = [self.fresh() for _ in range(self.w)]  # @line L2
        return self.vars[name]

    def constant(self, k: int) -> list[int]:
        return [TRUE if (k >> i) & 1 else -TRUE for i in range(self.w)]  # @line L3

    def add(self, a: list[int], b: list[int], carry: int = -TRUE) -> list[int]:
        """Ripple-carry adder modulo 2^w."""
        out = []
        for ai, bi in zip(a, b):
            t = self.xor2(ai, bi)
            out.append(self.xor2(t, carry))  # @line L8
            carry = self.or2(self.and2(ai, bi), self.and2(t, carry))  # @line L9
        return out

    def neg(self, a: list[int]) -> list[int]:
        return self.add([-x for x in a], self.constant(0), TRUE)

    def sub(self, a: list[int], b: list[int]) -> list[int]:
        return self.add(a, [-x for x in b], TRUE)

    def mul(self, a: list[int], b: list[int]) -> list[int]:
        """Shift-and-add multiplier modulo 2^w."""
        acc = self.constant(0)
        for i, bi in enumerate(b):
            row = [-TRUE] * i + [self.and2(aj, bi) for aj in a[: self.w - i]]  # @line L10
            acc = self.add(acc, row)
        return acc

    def ult(self, a: list[int], b: list[int]) -> int:
        """Unsigned a < b, scanning from the least significant bit up."""
        lt = -TRUE
        for ai, bi in zip(a, b):
            lt = self.or2(self.and2(-ai, bi), self.and2(-self.xor2(ai, bi), lt))  # @line L11
        return lt

    def eq(self, a: list[int], b: list[int]) -> int:
        e = TRUE
        for ai, bi in zip(a, b):
            e = self.and2(e, -self.xor2(ai, bi))
        return e

    def term(self, t: tuple) -> list[int]:
        op = t[0]
        if op == "var":
            return self.variable(t[1])
        if op == "const":
            return self.constant(t[1])
        if op == "shl":
            a, k = self.term(t[1]), t[2]
            return ([-TRUE] * k + a)[: self.w]
        if op == "lshr":
            a, k = self.term(t[1]), t[2]
            return (a[k:] + [-TRUE] * k)[: self.w]
        args = [self.term(s) for s in t[1:]]  # @line L1
        if op == "not":
            return [-x for x in args[0]]
        if op == "neg":
            return self.neg(args[0])
        a, b = args
        if op == "and":
            return [self.and2(x, y) for x, y in zip(a, b)]
        if op == "or":
            return [self.or2(x, y) for x, y in zip(a, b)]
        if op == "xor":
            return [self.xor2(x, y) for x, y in zip(a, b)]
        if op == "add":
            return self.add(a, b)  # @line L4
        if op == "sub":
            return self.sub(a, b)
        if op == "mul":
            return self.mul(a, b)
        raise ValueError(f"unknown term {op!r}")

    def formula(self, f: tuple) -> int:
        op = f[0]
        if op == "true":
            return TRUE
        if op == "bnot":
            return -self.formula(f[1])
        if op == "band":
            return self.and2(self.formula(f[1]), self.formula(f[2]))
        if op == "bor":
            return self.or2(self.formula(f[1]), self.formula(f[2]))
        a, b = self.term(f[1]), self.term(f[2])
        if op == "eq":
            return self.eq(a, b)  # @line L5
        if op == "ult":
            return self.ult(a, b)
        if op == "ule":
            return -self.ult(b, a)
        if op == "slt":
            # Flip the sign bits, then compare unsigned.
            return self.ult(a[:-1] + [-a[-1]], b[:-1] + [-b[-1]])
        raise ValueError(f"unknown formula {op!r}")


def blast(f: tuple, w: int) -> tuple[Blaster, int]:
    """Return the blaster with its clauses and the output literal of formula f."""
    bb = Blaster(w)
    out = bb.formula(f)
    bb.clauses.append([out])  # @line L6
    return bb, out


def dpll(clauses: list[list[int]], nvars: int) -> list[bool] | None:
    """A small DPLL solver with unit propagation. Returns val[0..nvars] or None."""
    val: list[bool | None] = [None] * (nvars + 1)

    def lit_value(x: int) -> bool | None:
        v = val[abs(x)]
        return None if v is None else (v if x > 0 else not v)

    def propagate(trail: list[int]) -> bool:
        changed = True
        while changed:
            changed = False
            for c in clauses:
                free = None
                nfree = 0
                sat = False
                for x in c:
                    v = lit_value(x)
                    if v is True:
                        sat = True
                        break
                    if v is None:
                        nfree += 1
                        free = x
                if sat:
                    continue
                if nfree == 0:
                    return False
                if nfree == 1:
                    val[abs(free)] = free > 0
                    trail.append(abs(free))
                    changed = True
        return True

    def search() -> bool:
        trail: list[int] = []
        if not propagate(trail):
            for v in trail:
                val[v] = None
            return False
        free = next((v for v in range(1, nvars + 1) if val[v] is None), None)
        if free is None:
            return True
        for choice in (True, False):
            val[free] = choice
            if search():
                return True
            val[free] = None
        for v in trail:
            val[v] = None
        return False

    if search():
        return [bool(v) for v in val]
    return None


def value_of(bits: list[int], val: list[bool]) -> int:
    """The integer sum of 2^i over the true bits."""
    return sum(1 << i for i, x in enumerate(bits) if (val[x] if x > 0 else not val[-x]))


def solve(f: tuple, w: int) -> dict[str, int] | None:
    """Decide formula f over width w; return a model {name: value} or None."""
    bb, _ = blast(f, w)
    val = dpll(bb.clauses, bb.nvars)  # @line L7
    if val is None:
        return None
    return {name: value_of(bits, val) for name, bits in bb.vars.items()}


def simulate(bb: Blaster, inputs: dict[str, int]) -> list[bool]:
    """Evaluate all gates for given input values; return val[0..nvars]."""
    val = [False] * (bb.nvars + 1)
    val[TRUE] = True
    for name, bits in bb.vars.items():
        for i, x in enumerate(bits):
            val[x] = bool((inputs.get(name, 0) >> i) & 1)

    def lv(x: int) -> bool:
        return val[x] if x > 0 else not val[-x]

    for y, op, a, b in bb.gates:
        val[y] = (lv(a) and lv(b)) if op == "and" else (lv(a) != lv(b))
    return val


def evaluate_term(t: tuple, w: int, env: dict[str, int]) -> int:
    """Reference semantics with Python integers modulo 2^w."""
    m = (1 << w) - 1
    op = t[0]
    if op == "var":
        return env[t[1]] & m
    if op == "const":
        return t[1] & m
    if op == "shl":
        return (evaluate_term(t[1], w, env) << t[2]) & m
    if op == "lshr":
        return evaluate_term(t[1], w, env) >> t[2]
    if op == "not":
        return ~evaluate_term(t[1], w, env) & m
    if op == "neg":
        return -evaluate_term(t[1], w, env) & m
    a, b = evaluate_term(t[1], w, env), evaluate_term(t[2], w, env)
    return {
        "and": a & b, "or": a | b, "xor": a ^ b,
        "add": (a + b) & m, "sub": (a - b) & m, "mul": (a * b) & m,
    }[op]


def evaluate(f: tuple, w: int, env: dict[str, int]) -> bool:
    """Reference truth value of formula f."""
    op = f[0]
    if op == "true":
        return True
    if op == "bnot":
        return not evaluate(f[1], w, env)
    if op == "band":
        return evaluate(f[1], w, env) and evaluate(f[2], w, env)
    if op == "bor":
        return evaluate(f[1], w, env) or evaluate(f[2], w, env)
    a, b = evaluate_term(f[1], w, env), evaluate_term(f[2], w, env)
    if op == "slt":
        half = 1 << (w - 1)
        a, b = (a - 2 * half if a >= half else a), (b - 2 * half if b >= half else b)
        return a < b
    return {"eq": a == b, "ult": a < b, "ule": a <= b}[op]
