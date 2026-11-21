# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/faceted-execution/. The authors are listed in prov/5EDZCZ.jsonl.

import itertools
import random

from faceted_execution import (MOD, Facet, evaluate, faceted_run,
                               initial_store, make, project, view)

VARS = ["h", "l", "m"]
HIGH = {"h"}
DOMAIN = [0, 1, 2]
FUEL = 200


# Independent oracle: a recursive plain interpreter.

class OutOfFuel(Exception):
    pass


def o_eval(e, s):
    if isinstance(e, int):
        return e % MOD
    if isinstance(e, str):
        return s[e]
    a, b = o_eval(e[1], s), o_eval(e[2], s)
    return {"+": (a + b) % MOD, "-": (a - b) % MOD, "*": (a * b) % MOD,
            "<": int(a < b), "==": int(a == b)}[e[0]]


def o_exec(c, s, fuel):
    fuel[0] -= 1
    if fuel[0] < 0:
        raise OutOfFuel
    tag = c[0]
    if tag == "assign":
        s[c[1]] = o_eval(c[2], s)
    elif tag == "seq":
        o_exec(c[1], s, fuel)
        o_exec(c[2], s, fuel)
    elif tag == "if":
        o_exec(c[2] if o_eval(c[1], s) else c[3], s, fuel)
    elif tag == "while":
        if o_eval(c[1], s):
            o_exec(c[2], s, fuel)
            o_exec(c, s, fuel)


def o_run_steps(c, s, fuel=FUEL):
    s = dict(s)
    left = [fuel]
    try:
        o_exec(c, s, left)
    except OutOfFuel:
        return None, fuel
    return s, fuel - left[0]


def o_run(c, s, fuel=FUEL):
    return o_run_steps(c, s, fuel)[0]


def stores():
    for vals in itertools.product(DOMAIN, repeat=len(VARS)):
        yield dict(zip(VARS, vals))


def defaulted(s):
    return {x: (0 if x in HIGH else v) for x, v in s.items()}


def low(s):
    return tuple(s[x] for x in VARS if x not in HIGH)


def fac(c, s, fuel=2 * FUEL):
    return faceted_run(c, initial_store(s, HIGH), fuel)


def faceted_is_tini(c):
    seen = {}
    for s in stores():
        t = fac(c, s)
        if t is None:
            continue
        out = low(project(t, "L"))
        if seen.setdefault(low(s), out) != out:
            return False
    return True


def is_tini_plain(c):
    seen = {}
    for s in stores():
        t = o_run(c, s)
        if t is None:
            continue
        if seen.setdefault(low(s), low(t)) != low(t):
            return False
    return True


def rand_expr(rng, depth=0):
    r = rng.random()
    if depth >= 2 or r < 0.35:
        return rng.choice(VARS)
    if r < 0.5:
        return rng.randrange(3)
    return (rng.choice(["+", "-", "*", "<", "=="]),
            rand_expr(rng, depth + 1), rand_expr(rng, depth + 1))


def rand_cmd(rng, budget):
    if budget <= 1:
        return ("assign", rng.choice(VARS), rand_expr(rng)), 1
    r = rng.random()
    if r < 0.35:
        return ("assign", rng.choice(VARS), rand_expr(rng)), 1
    if r < 0.4:
        return ("skip",), 1
    if r < 0.65:
        c1, n1 = rand_cmd(rng, budget // 2)
        c2, n2 = rand_cmd(rng, budget - n1)
        return ("seq", c1, c2), n1 + n2
    if r < 0.88:
        c1, n1 = rand_cmd(rng, (budget - 1) // 2)
        c2, n2 = rand_cmd(rng, max(1, budget - 1 - n1))
        return ("if", rand_expr(rng), c1, c2), 1 + n1 + n2
    c1, n1 = rand_cmd(rng, budget - 1)
    return ("while", rand_expr(rng), c1), 1 + n1


def seq(*cs):
    out = cs[-1]
    for c in reversed(cs[:-1]):
        out = ("seq", c, out)
    return out


FENTON = seq(("assign", "l", 1), ("assign", "m", 1),
             ("if", "h", ("assign", "m", 0), ("skip",)),
             ("if", "m", ("assign", "l", 0), ("skip",)))


def test_worked_example():
    t = fac(FENTON, {"h": 1, "l": 5, "m": 5})
    assert t == {"h": Facet(1, 0), "l": Facet(1, 0), "m": Facet(0, 1)}
    assert project(t, "L") == {"h": 0, "l": 0, "m": 1}
    assert project(t, "H") == {"h": 1, "l": 1, "m": 0}
    # With h = 0 the two views agree and no facet is made.
    assert fac(FENTON, {"h": 0, "l": 5, "m": 5}) == {"h": 0, "l": 0, "m": 1}
    assert faceted_is_tini(FENTON)
    assert not is_tini_plain(FENTON)


def test_make_view_evaluate():
    assert make(3, 3) == 3
    assert make(3, 4) == Facet(3, 4)
    assert view(Facet(3, 4), "H") == 3 and view(Facet(3, 4), "L") == 4
    assert view(7, "L") == 7
    assert evaluate(("+", "h", "l"), {"h": Facet(2, 0), "l": 1}) == Facet(3, 1)
    assert evaluate(("*", "h", 0), {"h": Facet(2, 0)}) == 0
    assert evaluate(("-", 0, 1), {}) == MOD - 1


def test_explicit_flow():
    t = fac(("assign", "l", "h"), {"h": 2, "l": 1, "m": 0})
    assert t["l"] == Facet(2, 0)


def test_high_loop():
    # A loop on h runs only in the H view; the L view sees h = 0.
    prog = seq(("assign", "m", 0),
               ("while", "h", seq(("assign", "h", ("-", "h", 1)),
                                  ("assign", "m", ("+", "m", 1)))),
               ("assign", "l", ("+", "l", 1)))
    t = fac(prog, {"h": 2, "l": 4, "m": 9})
    assert t == {"h": 0, "l": 5, "m": Facet(2, 0)}


def test_high_divergence_hides_low_view():
    # If the H view does not end, the single run does not end, so the
    # result is TINI only.
    prog = seq(("while", ("==", "h", 1), ("skip",)), ("assign", "l", 1))
    assert fac(prog, {"h": 1, "l": 0, "m": 0}) is None
    assert fac(prog, {"h": 0, "l": 0, "m": 0}) == {"h": 0, "l": 1, "m": 0}
    assert faceted_is_tini(prog)


def test_inputs_unchanged_and_no_high():
    store = {"a": 1, "b": 2}
    t = faceted_run(("assign", "a", ("+", "a", "b")), store)
    assert t == {"a": 3, "b": 2} and store == {"a": 1, "b": 2}


def test_deep_program_no_recursion():
    prog = ("assign", "l", 0)
    for _ in range(3000):
        prog = ("seq", ("assign", "l", ("+", "l", "h")), prog)
    t = fac(prog, {"h": 1, "l": 0, "m": 0}, fuel=100_000)
    assert t["l"] == 0


def test_random_projection_tini_transparency():
    rng = random.Random(2012)
    tini_programs = 0
    for _ in range(500):
        prog, _n = rand_cmd(rng, rng.randint(1, 10))
        plain = {}
        for s in stores():
            plain[tuple(s.values())] = o_run_steps(prog, s, 2 * FUEL)
        seen = {}
        tini = True
        for s in stores():
            th, _k = plain[tuple(s.values())]
            if th is not None and seen.setdefault(low(s), low(th)) != low(th):
                tini = False
        tini_programs += tini
        seen = {}
        for s in stores():
            th, kh = plain[tuple(s.values())]
            tl, kl = plain[tuple(defaulted(s).values())]
            t = fac(prog, s)
            if t is None:
                # The single run takes at most the steps of both views.
                assert th is None or tl is None or kh + kl > 2 * FUEL
                continue
            assert project(t, "H") == th, (prog, s)
            assert project(t, "L") == tl, (prog, s)
            out = low(project(t, "L"))
            assert seen.setdefault(low(s), out) == out, (prog, s)
            if tini:
                assert out == low(th), (prog, s)
    assert tini_programs >= 100
