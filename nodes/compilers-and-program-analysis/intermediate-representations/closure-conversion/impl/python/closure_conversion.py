# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/closure-conversion/. The authors are listed in prov/EGE7J5.jsonl.
"""Flat closure conversion of the toy lambda language of toylam.py.

The target language is the toy language with two more forms:
    ("tuple", (e0, e1, ..., em))   a record, a value when all parts are values
    ("proj", e, i)                 part i of the record e, counted from 0

A source function becomes a record (code, v1, ..., vm): code is the closed
term fun self -> fun x -> body, and v1 ... vm are the values of the free
variables. Inside body, the i-th free variable is read as self.i. A call
e1 e2 becomes let c = e1 in let a = e2 in (c.0 c) a. The target needs no fix,
since a recursive function reaches itself through self.

The module also has a small evaluator for the target language, with the same
call-by-value, left-to-right rules as toylam.
"""

import toylam

STUCK = toylam.STUCK


def var(x):
    return ("var", x)


def names(e):
    """Every variable name in the source term e, bound or free."""
    tag = e[0]
    if tag == "var":
        return {e[1]}
    if tag in ("int", "bool"):
        return set()
    if tag == "lam":
        return {e[1]} | names(e[2])
    if tag == "let":
        return {e[1]} | names(e[2]) | names(e[3])
    if tag == "fix":
        return {e[1], e[2]} | names(e[3])
    if tag == "prim":
        return names(e[2]) | names(e[3])
    out = set()
    for part in e[1:]:
        out |= names(part)
    return out


class Fresh:
    """Makes names that are not in avoid and were not made before."""

    def __init__(self, avoid=()):
        self.avoid = set(avoid)
        self.n = 0

    def __call__(self, base):
        while True:
            self.n += 1
            name = f"{base}{self.n}"
            if name not in self.avoid:
                self.avoid.add(name)
                return name


# ------------------------------------------------------------ the conversion


def closure_convert(e):
    """The target program of the closed source term e."""
    return convert(e, {}, Fresh(names(e)))  # @line L1


def convert(e, rho, fresh):
    """Convert e. rho maps each free variable of e to the target term that reads it."""
    tag = e[0]
    if tag == "var":  # @line L2
        return rho[e[1]]
    if tag in ("lam", "fix"):  # @line L3
        ys = sorted(toylam.free_vars(e))  # @line L4
        self = fresh("self")
        x, body = (e[1], e[2]) if tag == "lam" else (e[2], e[3])
        inner = {y: ("proj", var(self), i + 1) for i, y in enumerate(ys)}  # @line L5
        if tag == "fix":
            inner[e[1]] = var(self)
        inner[x] = var(x)
        code = ("lam", self, ("lam", x, convert(body, inner, fresh)))  # @line L6
        return ("tuple", (code,) + tuple(rho[y] for y in ys))  # @line L7
    if tag == "app":  # @line L8
        c, a = fresh("c"), fresh("a")
        call = ("app", ("app", ("proj", var(c), 0), var(c)), var(a))
        return ("let", c, convert(e[1], rho, fresh), ("let", a, convert(e[2], rho, fresh), call))
    if tag == "let":  # @line L9
        return ("let", e[1], convert(e[2], rho, fresh), convert(e[3], {**rho, e[1]: var(e[1])}, fresh))
    if tag in ("int", "bool"):  # @line L10
        return e
    if tag == "if":
        return ("if", convert(e[1], rho, fresh), convert(e[2], rho, fresh), convert(e[3], rho, fresh))
    return ("prim", e[1], convert(e[2], rho, fresh), convert(e[3], rho, fresh))


# ------------------------------------------------------------ the target language


def is_value(e):
    if e[0] == "tuple":
        return all(is_value(p) for p in e[1])
    return e[0] in ("int", "bool", "lam", "fix")


def free_vars(e):
    tag = e[0]
    if tag == "tuple":
        out = set()
        for p in e[1]:
            out |= free_vars(p)
        return out
    if tag == "proj":
        return free_vars(e[1])
    if tag == "var":
        return {e[1]}
    if tag in ("int", "bool"):
        return set()
    if tag == "lam":
        return free_vars(e[2]) - {e[1]}
    if tag == "let":
        return free_vars(e[2]) | (free_vars(e[3]) - {e[1]})
    if tag == "fix":
        return free_vars(e[3]) - {e[1], e[2]}
    if tag == "prim":
        return free_vars(e[2]) | free_vars(e[3])
    out = set()
    for p in e[1:]:
        out |= free_vars(p)
    return out


def subst(e, x, v):
    """Replace the free occurrences of x in e by the closed value v."""
    tag = e[0]
    if tag == "var":
        return v if e[1] == x else e
    if tag in ("int", "bool"):
        return e
    if tag == "tuple":
        return ("tuple", tuple(subst(p, x, v) for p in e[1]))
    if tag == "proj":
        return ("proj", subst(e[1], x, v), e[2])
    if tag == "lam":
        return e if e[1] == x else ("lam", e[1], subst(e[2], x, v))
    if tag == "let":
        return ("let", e[1], subst(e[2], x, v), e[3] if e[1] == x else subst(e[3], x, v))
    if tag == "fix":
        return e if x in (e[1], e[2]) else ("fix", e[1], e[2], subst(e[3], x, v))
    if tag == "prim":
        return ("prim", e[1], subst(e[2], x, v), subst(e[3], x, v))
    return (tag,) + tuple(subst(p, x, v) for p in e[1:])


def step(e):
    """One call-by-value step of a target term: the next term, e if e is a value, or STUCK."""
    if is_value(e):
        return e
    tag = e[0]
    if tag == "tuple":
        parts = list(e[1])
        for i, p in enumerate(parts):
            if not is_value(p):
                q = step(p)
                if q == STUCK:
                    return STUCK
                parts[i] = q
                return ("tuple", tuple(parts))
    if tag == "proj":
        if not is_value(e[1]):
            q = step(e[1])
            return STUCK if q == STUCK else ("proj", q, e[2])
        r = e[1]
        if r[0] == "tuple" and 0 <= e[2] < len(r[1]):
            return r[1][e[2]]
        return STUCK
    if tag == "var":
        return STUCK
    if tag == "app":
        f, a = e[1], e[2]
        if not is_value(f):
            q = step(f)
            return STUCK if q == STUCK else ("app", q, a)
        if not is_value(a):
            q = step(a)
            return STUCK if q == STUCK else ("app", f, q)
        if f[0] == "lam":
            return subst(f[2], f[1], a)
        if f[0] == "fix":
            return subst(subst(f[3], f[1], f), f[2], a)
        return STUCK
    if tag == "let":
        if not is_value(e[2]):
            q = step(e[2])
            return STUCK if q == STUCK else ("let", e[1], q, e[3])
        return subst(e[3], e[1], e[2])
    if tag == "if":
        if not is_value(e[1]):
            q = step(e[1])
            return STUCK if q == STUCK else ("if", q, e[2], e[3])
        if e[1][0] == "bool":
            return e[2] if e[1][1] else e[3]
        return STUCK
    if tag == "prim":
        a, b = e[2], e[3]
        if not is_value(a):
            q = step(a)
            return STUCK if q == STUCK else ("prim", e[1], q, b)
        if not is_value(b):
            q = step(b)
            return STUCK if q == STUCK else ("prim", e[1], a, q)
        if a[0] == "int" and b[0] == "int":
            return toylam._prim(e[1], a[1], b[1])
        return STUCK
    raise ValueError(f"not a term: {e!r}")


def evaluate(e, fuel=10000):
    """Run a target term: ("value", v), ("stuck", t) or ("fuel",)."""
    for _ in range(fuel):
        if is_value(e):
            return ("value", e)
        nxt = step(e)
        if nxt == STUCK:
            return ("stuck", e)
        e = nxt
    return ("value", e) if is_value(e) else ("fuel",)


def size(e):
    tag = e[0]
    if tag in ("var", "int", "bool"):
        return 1
    if tag == "tuple":
        return 1 + sum(size(p) for p in e[1])
    if tag == "proj":
        return 1 + size(e[1])
    if tag == "lam":
        return 1 + size(e[2])
    if tag == "fix":
        return 1 + size(e[3])
    if tag in ("let", "prim"):
        return 1 + size(e[2]) + size(e[3])
    return 1 + sum(size(p) for p in e[1:])


def show(e):
    """The surface syntax, with [e0, e1] for a record and e.i for a projection."""
    tag = e[0]
    if tag == "tuple":
        return "[" + ", ".join(show(p) for p in e[1]) + "]"
    if tag == "proj":
        return f"{show(e[1])}.{e[2]}"
    if tag == "var":
        return e[1]
    if tag == "int":
        return str(e[1])
    if tag == "bool":
        return "true" if e[1] else "false"
    if tag == "lam":
        return f"(fun {e[1]} -> {show(e[2])})"
    if tag == "app":
        return f"({show(e[1])} {show(e[2])})"
    if tag == "let":
        return f"(let {e[1]} = {show(e[2])} in {show(e[3])})"
    if tag == "if":
        return f"(if {show(e[1])} then {show(e[2])} else {show(e[3])})"
    if tag == "prim":
        return f"({show(e[2])} {e[1]} {show(e[3])})"
    if tag == "fix":
        return f"(fix {e[1]} {e[2]} -> {show(e[3])})"
    raise ValueError(f"not a term: {e!r}")
