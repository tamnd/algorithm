# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nelson-oppen/. The authors are listed in prov/P1JJQX.jsonl.
"""Tests of Nelson-Oppen against brute force over a bounded domain.

Why a bounded domain suffices. Let a formula use the integer constants
0..K and have m free subterms (variables and applications). Take any model
over the integers. Map the values of all subterms, and the numbers 0..K, by
a map h that fixes 0..K, sends the values below 0 to -1, -2, ... in order,
and the values above K to K+1, K+2, ... in order. Then h is strictly
increasing, so it keeps every <=, <, = and != between subterms, and it is
one to one, so equal arguments still give equal function values. At most m
values lie outside 0..K, so a model exists with all values in [-m, K+m].
Over the rationals without constants, the ranks 0..m-1 do the same.
"""

import random
from itertools import product

from nelson_oppen import (at_most_two_sat, euf_order_sat, euf_sat,
                          int_order_sat, nelson_oppen, nelson_oppen_guess,
                          purify, rat_order_sat)


def free_terms(lits):
    out = []

    def add(t):
        if isinstance(t, int) or t in out:
            return
        if isinstance(t, tuple):
            for a in t[1:]:
                add(a)
        out.append(t)  # arguments come before the application

    for _, s, t in lits:
        add(s)
        add(t)
    return out


def brute(lits, domain):
    """Search for values of the free subterms, with functional consistency."""
    terms = free_terms(lits)
    pos = {t: i for i, t in enumerate(terms)}

    def ready(t):
        return -1 if isinstance(t, int) else pos[t]

    checks = [[] for _ in terms]
    for lit in lits:
        checks[max(ready(lit[1]), ready(lit[2]))].append(lit)
    val, table = {}, {}

    def ev(t):
        return t if isinstance(t, int) else val[t]

    def holds(op, s, t):
        a, b = ev(s), ev(t)
        return {"=": a == b, "!=": a != b, "<=": a <= b, "<": a < b}[op]

    def go(i):
        if i == len(terms):
            return True
        t = terms[i]
        key = None
        if isinstance(t, tuple):
            key = (t[0],) + tuple(ev(a) for a in t[1:])
        options = [table[key]] if key in table else domain
        for v in options:
            val[t] = v
            added = key is not None and key not in table
            if added:
                table[key] = v
            if all(holds(*lit) for lit in checks[i]) and go(i + 1):
                return True
            if added:
                del table[key]
        del val[t]
        return False

    return go(0)


def brute_int(lits, k):
    m = len(free_terms(lits))
    return brute(lits, list(range(-m, k + m + 1)))


def brute_rat(lits):
    m = len(free_terms(lits))
    return brute(lits, list(range(m)))


def f(t):
    return ("f", t)


def test_convex_exchange():
    # x <= y, y <= x, f(x) <= z, z <= f(y), g(z) != g(f(x)): unsat by exchange
    phi = [("<=", "x", "y"), ("<=", "y", "x"), ("<=", f("x"), "z"),
           ("<=", "z", f("y")), ("!=", ("g", "z"), ("g", f("x")))]
    for integer in (True, False):
        stats = {"calls": 0, "equalities": 0, "splits": 0}
        euf, arith = purify(phi)
        osat = int_order_sat if integer else rat_order_sat
        assert not nelson_oppen(euf, arith, euf_sat, osat, stats=stats)
        assert stats["splits"] == 0 and stats["equalities"] == 3
    assert not brute_int(phi, 0) and not brute_rat(phi)


def test_non_convex_split():
    # 1 <= x <= 2, f(x) != f(1), f(x) != f(2)
    phi = [("<=", 1, "x"), ("<=", "x", 2), ("!=", f("x"), f(1)), ("!=", f("x"), f(2))]
    assert not euf_order_sat(phi, integer=True, method="split")
    assert not euf_order_sat(phi, integer=True, method="guess")
    assert euf_order_sat(phi, integer=True, method="nosplit")  # incomplete
    assert not brute_int(phi, 2)
    # over the rationals x = 3/2 works, and every method says sat
    for method in ("split", "guess", "nosplit"):
        assert euf_order_sat(phi, integer=False, method=method)


def test_not_stably_infinite():
    # EUF with three distinct values, combined with a theory of at most two elements
    phi1 = [("!=", f("a"), f("b")), ("!=", f("a"), f("c")), ("!=", f("b"), f("c"))]
    phi2 = []
    assert nelson_oppen(phi1, phi2, euf_sat, at_most_two_sat)  # says sat
    assert nelson_oppen_guess(phi1, phi2, euf_sat, at_most_two_sat)
    assert not brute(phi1, [0, 1])  # but there is no model with two elements
    assert brute(phi1, [0, 1, 2])  # EUF alone is satisfiable


def random_term(rng, depth, consts):
    r = rng.random()
    if depth == 0 or r < 0.45:
        if consts and rng.random() < 0.25:
            return rng.choice(consts)
        return rng.choice("xyz")
    if r < 0.8:
        return ("f", random_term(rng, depth - 1, consts))
    return ("g", random_term(rng, depth - 1, consts), random_term(rng, depth - 1, consts))


def random_formula(rng, consts):
    lits = []
    for _ in range(rng.randint(2, 4)):
        op = rng.choice(["=", "!=", "<=", "<", "!="])
        s, t = random_term(rng, 1, consts), random_term(rng, 1, consts)
        if isinstance(s, int) and isinstance(t, int):
            continue
        lits.append((op, s, t))
    return lits


def small(lits):
    return len(free_terms(lits)) <= 6


def interval_formula(rng, consts):
    """Formulas that often pin a variable to two integers, so that the
    integer side entails a disjunction of equalities."""
    lits = []
    if rng.random() < 0.6:
        v = rng.choice("xy")
        a = rng.choice(consts[:-1])
        lits += [("<=", a, v), ("<=", v, a + 1)]
        for _ in range(rng.randint(0, 2)):
            lits.append(("!=", f(v), f(rng.choice(consts + ["x", "y"]))))
    for _ in range(rng.randint(1, 4)):
        s, t = random_term(rng, 1, consts), random_term(rng, 1, consts)
        if isinstance(s, int) and isinstance(t, int):
            continue
        lits.append((rng.choice(["=", "!=", "!=", "<=", "<"]), s, t))
    return lits


def test_random_integers_against_brute_force():
    rng = random.Random(1)
    counts = {"sat": 0, "unsat": 0, "nosplit_wrong": 0, "splits": 0}
    done = 0
    while done < 400:
        phi = interval_formula(rng, [0, 1, 2])
        if not phi or len(free_terms(phi)) > 5:
            continue
        done += 1
        truth = brute_int(phi, 2)
        euf, arith = purify(phi)
        stats = {"calls": 0, "equalities": 0, "splits": 0}
        assert nelson_oppen(euf, arith, euf_sat, int_order_sat, stats=stats) == truth, phi
        counts["splits"] += stats["splits"] > 0
        assert euf_order_sat(phi, True, "guess") == truth, phi
        nosplit = euf_order_sat(phi, True, "nosplit")
        if not nosplit:
            assert not truth, phi  # unsat answers are always right
        elif not truth:
            counts["nosplit_wrong"] += 1
        counts["sat" if truth else "unsat"] += 1
    assert counts["sat"] > 100 and counts["unsat"] > 50
    assert counts["splits"] > 0 and counts["nosplit_wrong"] > 0


def test_random_rationals_against_brute_force():
    # the order of Q is convex: single equalities suffice, no split happens
    rng = random.Random(11)
    done = 0
    while done < 250:
        phi = random_formula(rng, [])
        if not phi or not small(phi):
            continue
        done += 1
        truth = brute_rat(phi)
        euf, arith = purify(phi)
        stats = {"calls": 0, "equalities": 0, "splits": 0}
        assert nelson_oppen(euf, arith, euf_sat, rat_order_sat, stats=stats) == truth, phi
        assert stats["splits"] == 0, phi
        assert euf_order_sat(phi, False, "nosplit") == truth, phi
        assert euf_order_sat(phi, False, "guess") == truth, phi


def test_order_solver_alone():
    rng = random.Random(3)
    for _ in range(300):
        lits = []
        for _ in range(rng.randint(1, 4)):
            op = rng.choice(["=", "!=", "<=", "<"])
            s = rng.choice(["x", "y", "z", 0, 1, 2])
            t = rng.choice(["x", "y", "z", 0, 1, 2])
            lits.append((op, s, t))
        names = sorted({x for _, s, t in lits for x in (s, t) if isinstance(x, str)})
        found = False
        for vals in product(range(-3, 6), repeat=len(names)):
            val = dict(zip(names, vals))

            def ev(t):
                return t if isinstance(t, int) else val[t]

            if all({"=": ev(s) == ev(t), "!=": ev(s) != ev(t), "<=": ev(s) <= ev(t),
                    "<": ev(s) < ev(t)}[op] for op, s, t in lits):
                found = True
                break
        assert int_order_sat(lits) == found, lits


def test_at_most_two():
    assert at_most_two_sat([("!=", "a", "b")])
    assert not at_most_two_sat([("!=", "a", "b"), ("!=", "a", "c"), ("!=", "b", "c")])
