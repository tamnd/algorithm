# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shostak-combination/. The authors are listed in prov/4D6QWA.jsonl.
"""Shostak's method for linear arithmetic over Q with uninterpreted functions.

The Shostak theory is the theory of linear equations over the rationals.
Its canonizer writes a term as a sum of coefficient times variable plus a
constant. Its solver solves an equation for one variable. Uninterpreted
applications are replaced by fresh names, and a congruence step merges two
names when the solved form makes their arguments equal.

Terms:
    int or Fraction        a number
    str                    a variable
    ("+", a, b), ("-", a, b), ("*", c, a) with c a number
    (f, a1, ..., an)       an application of an uninterpreted f
"""

from fractions import Fraction

ONE = ""  # the key of the constant part of a linear form


def is_num(t):
    return isinstance(t, (int, Fraction))


def canon(form):
    """The canonical form: sorted (variable, coefficient) pairs, no zeros."""
    return tuple(sorted((v, Fraction(c)) for v, c in form.items() if c != 0))


def add(p, q, k=1):
    """The linear form p + k q, as a dict."""
    r = dict(p)
    for v, c in q.items():
        r[v] = r.get(v, 0) + k * c
    return r


def apply(S, form):
    """Replace each solitary variable of S by its right-hand side."""
    r = {}
    for v, c in form.items():
        r = add(r, S[v], c) if v in S else add(r, {v: c})
    return r


def solve(form):
    """Solve form = 0. Return None for bottom, {} if trivial, or {x: rhs}."""
    vs = sorted(v for v, c in form.items() if v != ONE and c != 0)
    if not vs:
        return None if form.get(ONE, 0) != 0 else {}
    x = vs[0]  # solve for the least variable
    a = Fraction(form[x])
    rhs = {v: -Fraction(c) / a for v, c in form.items() if v != x and c != 0}
    return {x: rhs}


class Abstraction:
    """Names each distinct application, after canonizing its arguments."""

    def __init__(self):
        self.defs = {}  # name -> (f, tuple of linear-form dicts)
        self.keys = {}  # (f, canonical args) -> name

    def form(self, t):
        if is_num(t):
            return {ONE: Fraction(t)}
        if isinstance(t, str):
            return {t: Fraction(1)}
        op = t[0]
        if op == "+":
            return add(self.form(t[1]), self.form(t[2]))
        if op == "-":
            return add(self.form(t[1]), self.form(t[2]), -1)
        if op == "*":
            return {v: Fraction(t[1]) * c for v, c in self.form(t[2]).items()}
        args = tuple(self.form(a) for a in t[1:])
        key = (op, tuple(canon(a) for a in args))
        if key not in self.keys:
            name = "u%d" % (len(self.defs) + 1)
            self.keys[key] = name
            self.defs[name] = (op, args)
        return {self.keys[key]: Fraction(1)}


def congruent_pair(S, defs):
    """A pair of names whose arguments are equal under S but whose values are not."""
    seen = {}
    for u in sorted(defs):
        f, args = defs[u]
        key = (f, tuple(canon(apply(S, a)) for a in args))
        if key in seen:
            v = seen[key]
            if canon(apply(S, {u: 1})) != canon(apply(S, {v: 1})):
                return u, v
        else:
            seen[key] = u
    return None


def shostak(eqs, diseqs, state=None, trace=None):
    """Decide a conjunction of equalities eqs and disequalities diseqs.

    eqs and diseqs are lists of pairs (s, t). Return True for satisfiable.
    If state is a dict, it receives the final solved form and definitions.
    If trace is a list, it receives one entry per processed equation.
    """
    A = Abstraction()  # @line L1
    gamma = [(A.form(s), A.form(t)) for s, t in eqs]
    delta = [(A.form(s), A.form(t)) for s, t in diseqs]
    S, queue = {}, list(gamma)  # @line L2
    sat = True
    while True:  # @line L3
        if queue:  # @line L4
            s, t = queue.pop(0)
            origin = "input"
        else:
            pair = congruent_pair(S, A.defs)  # @line L5
            if pair is None:
                break  # @line L6
            s, t = {pair[0]: 1}, {pair[1]: 1}
            origin = "congruence"
        eq = add(apply(S, s), apply(S, t), -1)  # @line L7
        star = solve(eq)
        if trace is not None:
            trace.append((origin, canon(eq), star))
        if star is None:  # @line L8
            sat = False
            break
        S = {x: apply(star, rhs) for x, rhs in S.items()}  # @line L9
        S.update(star)
    if sat:
        for s, t in delta:  # @line L10
            if canon(apply(S, s)) == canon(apply(S, t)):
                sat = False
                break
    if state is not None:
        state.update(S=S, defs=A.defs, gamma=gamma, delta=delta)
    return sat  # @line L11
