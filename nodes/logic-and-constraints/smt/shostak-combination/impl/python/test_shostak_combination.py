# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shostak-combination/. The authors are listed in prov/4D6QWA.jsonl.
"""Tests of Shostak's method against an independent decision procedure.

The reference removes the function symbols by Ackermann's reduction: each
application gets a fresh variable, and for two applications f(a) and f(b)
the case split "some argument differs, or the values are equal" is made by
search. Each case is a conjunction of linear equations and disequations over
Q. It is satisfiable exactly when the equations are consistent and no
disequation becomes 0 = 0 modulo the equations, because Q^n is not a finite
union of proper affine subspaces.

For satisfiable inputs, the tests also build the model of the proof page
(random values for the free variables) and check it on the original terms.
"""

import random
from fractions import Fraction
from itertools import product

from shostak_combination import shostak

OPS = ("+", "-", "*")


# ---------- the reference: Ackermann reduction and case splits ----------

def lin(t, names):
    """Linear form of t as a dict; applications are looked up in names."""
    if isinstance(t, (int, Fraction)):
        return {1: Fraction(t)}
    if isinstance(t, str):
        return {t: Fraction(1)}
    if t[0] in OPS:
        if t[0] == "*":
            return {v: t[1] * c for v, c in lin(t[2], names).items()}
        p, q = lin(t[1], names), lin(t[2], names)
        k = 1 if t[0] == "+" else -1
        r = dict(p)
        for v, c in q.items():
            r[v] = r.get(v, 0) + k * c
        return r
    return {names[t]: Fraction(1)}


def applications(t, out):
    if isinstance(t, tuple):
        for a in t[1:] if t[0] not in OPS else t[1:]:
            applications(a, out)
        if t[0] not in OPS and t not in out:
            out.append(t)


def diff(p, q):
    r = dict(p)
    for v, c in q.items():
        r[v] = r.get(v, 0) - c
    return {v: c for v, c in r.items() if c != 0}


def eliminate(rows):
    """Gauss-Jordan elimination of forms = 0. Return the pivots or None."""
    pivots = {}
    for row in rows:
        r = reduce_form(dict(row), pivots)
        vs = [v for v in r if v != 1]
        if not vs:
            if r.get(1, 0) != 0:
                return None
            continue
        x = vs[0]
        a = r[x]
        expr = {v: -c / a for v, c in r.items() if v != x}
        for y in pivots:
            if x in pivots[y]:
                c = pivots[y].pop(x)
                for v, d in expr.items():
                    pivots[y][v] = pivots[y].get(v, 0) + c * d
                pivots[y] = {v: d for v, d in pivots[y].items() if d != 0}
        pivots[x] = expr
    return pivots


def reduce_form(r, pivots):
    out = {}
    for v, c in r.items():
        if v in pivots:
            for w, d in pivots[v].items():
                out[w] = out.get(w, 0) + c * d
        else:
            out[v] = out.get(v, 0) + c
    return {v: c for v, c in out.items() if c != 0}


def conj_sat(eqs, neqs):
    pivots = eliminate(eqs)
    if pivots is None:
        return False
    return all(reduce_form(d, pivots) for d in neqs)


def reference(eqs, diseqs):
    apps = []
    for s, t in eqs + diseqs:
        applications(s, apps)
        applications(t, apps)
    names = {a: "#%d" % i for i, a in enumerate(apps)}
    E = [diff(lin(s, names), lin(t, names)) for s, t in eqs]
    N = [diff(lin(s, names), lin(t, names)) for s, t in diseqs]
    pairs = [(a, b) for i, a in enumerate(apps) for b in apps[i + 1:]
             if a[0] == b[0] and len(a) == len(b)]

    def go(i, E, N):
        if not conj_sat(E, N):
            return False
        if i == len(pairs):
            return True
        a, b = pairs[i]
        pivots = eliminate(E)
        same = diff({names[a]: 1}, {names[b]: 1})
        if not reduce_form(same, pivots):  # the values are already equal
            return go(i + 1, E, N)
        args = [diff(lin(x, names), lin(y, names)) for x, y in zip(a[1:], b[1:])]
        if go(i + 1, E + [same], N):
            return True
        return any(go(i + 1, E, N + [d]) for d in args if reduce_form(d, pivots))

    return go(0, E, N)


# ---------- the model of the proof page ----------

def check_model(eqs, diseqs, state, rng):
    S, defs = state["S"], state["defs"]
    variables = set()
    for f, args in defs.values():
        for a in args:
            variables |= set(a)
    for s, t in state["gamma"] + state["delta"]:
        variables |= set(s) | set(t)
    variables |= set(defs) | set(S)
    variables.discard("")
    val = {v: Fraction(rng.randint(-10**9, 10**9)) for v in variables if v not in S}

    def value(form):
        total = Fraction(0)
        for v, c in form.items():
            if v == "":
                total += c
            elif v in S:
                total += c * value(S[v])
            else:
                total += c * val[v]
        return total

    table = {}
    for u, (f, args) in defs.items():
        key = (f, tuple(value(a) for a in args))
        assert table.setdefault(key, value({u: 1})) == value({u: 1})  # f is a function

    def ev(t):
        if isinstance(t, (int, Fraction)):
            return Fraction(t)
        if isinstance(t, str):
            return value({t: 1})
        if t[0] == "+":
            return ev(t[1]) + ev(t[2])
        if t[0] == "-":
            return ev(t[1]) - ev(t[2])
        if t[0] == "*":
            return t[1] * ev(t[2])
        return table[(t[0], tuple(ev(a) for a in t[1:]))]

    assert all(ev(s) == ev(t) for s, t in eqs)
    assert all(ev(s) != ev(t) for s, t in diseqs)


# ---------- tests ----------

def test_handbook_example():
    # Handbook Example 33.5.4: a + 3b - 2c = 1, a - b - 6c = 1, b + a != a - c
    eqs = [(("-", ("+", "a", ("*", 3, "b")), ("*", 2, "c")), 1),
           (("-", ("-", "a", "b"), ("*", 6, "c")), 1)]
    diseqs = [(("+", "b", "a"), ("-", "a", "c"))]
    state = {}
    assert not shostak(eqs, diseqs, state)
    S = state["S"]
    assert S["a"] == {"": 1, "c": 5} and S["b"] == {"c": -1}
    assert shostak(eqs, [])
    # with uninterpreted functions the same equalities make f(b + a) = f(a - c)
    assert not shostak(eqs, [(("f", ("+", "b", "a")), ("f", ("-", "a", "c")))])


def test_congruence_through_arithmetic():
    # f(x) = y + 1, x = 2y - z, z = y, f(y) != y + 1
    eqs = [(("f", "x"), ("+", "y", 1)), ("x", ("-", ("*", 2, "y"), "z")), ("z", "y")]
    diseqs = [(("f", "y"), ("+", "y", 1))]
    trace = []
    assert not shostak(eqs, diseqs, trace=trace)
    assert [o for o, _, _ in trace] == ["input", "input", "input", "congruence"]
    assert not reference(eqs, diseqs)
    # without z = y it is satisfiable
    state = {}
    assert shostak(eqs[:2], diseqs, state)
    check_model(eqs[:2], diseqs, state, random.Random(0))


def test_canonizer_without_equalities():
    # f(x + y) and f(y + x) get one name: no equation is needed
    assert not shostak([], [(("f", ("+", "x", "y")), ("f", ("+", "y", "x")))])
    # x + y = y + x - 1 is false
    assert not shostak([(("+", "x", "y"), ("-", ("+", "y", "x"), 1))], [])


def test_nested_congruence():
    # x = y implies f(f(x)) = f(f(y)), found by two congruence steps
    eqs = [("x", "y")]
    diseqs = [(("f", ("f", "x")), ("f", ("f", "y")))]
    trace = []
    assert not shostak(eqs, diseqs, trace=trace)
    # f(x) - x = 1 and x = f(x) - 1 are the same equation
    assert shostak([(("-", ("f", "x"), "x"), 1)], [("x", ("-", ("f", "x"), 1)), ("x", "y")]) is False


def random_term(rng, depth):
    r = rng.random()
    if depth == 0 or r < 0.35:
        return rng.choice(["x", "y", "z", "x", "y", "x", 0, 1])
    if r < 0.6:
        return (rng.choice(["+", "-"]), random_term(rng, depth - 1), random_term(rng, depth - 1))
    if r < 0.67:
        return ("*", rng.choice([2, -1, Fraction(1, 2)]), random_term(rng, depth - 1))
    if r < 0.9:
        return ("f", random_term(rng, depth - 1))
    return ("g", random_term(rng, depth - 1), random_term(rng, depth - 1))


def random_problem(rng):
    while True:
        eqs = [(random_term(rng, 1), random_term(rng, 2)) for _ in range(rng.randint(1, 4))]
        diseqs = []
        for _ in range(rng.randint(1, 2)):
            if rng.random() < 0.5:  # two applications of f, to provoke congruence
                diseqs.append((("f", random_term(rng, 1)), ("f", random_term(rng, 1))))
            else:
                diseqs.append((random_term(rng, 2), random_term(rng, 1)))
        apps = []
        for s, t in eqs + diseqs:
            applications(s, apps)
            applications(t, apps)
        if len(apps) <= 6:  # keeps the case splits of the reference small
            return eqs, diseqs


def test_random_against_reference():
    rng = random.Random(5)
    counts = {True: 0, False: 0, "congruence": 0}
    for _ in range(600):
        eqs, diseqs = random_problem(rng)
        state, trace = {}, []
        got = shostak(eqs, diseqs, state, trace)
        assert got == reference(eqs, diseqs), (eqs, diseqs)
        if got:
            check_model(eqs, diseqs, state, rng)
        counts[got] += 1
        counts["congruence"] += any(o == "congruence" for o, _, _ in trace)
    assert counts[True] > 300 and counts[False] > 80 and counts["congruence"] > 50


def test_solver_and_canonizer():
    # canon(s) = canon(t) exactly when s - t is 0 for all values
    rng = random.Random(9)
    for _ in range(300):
        s, t = random_term(rng, 2), random_term(rng, 2)
        if any(isinstance(x, tuple) and x[0] in ("f", "g") for x in (s, t)):
            continue
        same = not shostak([], [(s, t)])
        values_agree = True
        for vals in product([0, 1, 3, -7], repeat=3):
            env = dict(zip("xyz", vals))

            def ev(u):
                if isinstance(u, (int, Fraction)):
                    return Fraction(u)
                if isinstance(u, str):
                    return Fraction(env[u])
                if u[0] == "*":
                    return u[1] * ev(u[2])
                if u[0] in ("f", "g"):
                    raise ValueError
                a, b = ev(u[1]), ev(u[2])
                return a + b if u[0] == "+" else a - b

            try:
                values_agree &= ev(s) == ev(t)
            except ValueError:
                values_agree = None
                break
        if values_agree is not None:
            assert same == values_agree, (s, t)
