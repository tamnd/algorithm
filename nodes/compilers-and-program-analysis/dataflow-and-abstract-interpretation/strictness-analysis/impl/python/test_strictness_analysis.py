# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/strictness-analysis/. The authors are listed in prov/GYNYB7.jsonl.

import random
import sys
from itertools import product

import toylam as L
from strictness_analysis import abstract_eval, analyse, kleene_step, parse_function

sys.setrecursionlimit(20000)

U = "u_"  # the dummy parameter of a thunk
FUEL = 300  # the step bound; every run of the random test that stops at all stops well before it


def V(x):
    return ("var", x)


def app(a, b):
    return ("app", a, b)


def lam(x, e):
    return ("lam", x, e)


def num(k):
    return ("int", k)


def prim(op, a, b):
    return ("prim", op, a, b)


def call(f, *args):
    e = V(f)
    for a in args:
        e = app(e, a)
    return e


def function(name, params, body):
    """fix name p1 -> fun p2 -> ... -> body, or a plain lambda when name is None."""
    for p in reversed(params[1:]):
        body = lam(p, body)
    return ("fix", name, params[0], body) if name else lam(params[0], body)


# Omega: a closed term whose call-by-value run never stops.
OMEGA = app(("fix", "w", "y", app(V("w"), V("y"))), num(0))


def thunk(e):
    return lam(U, e)


def by_name(e, name):
    """Translate a body so that toylam's call-by-value run passes arguments by name.

    Every lazily bound name holds a thunk; a use forces it with (x 0).
    """
    tag = e[0]
    if tag == "var":
        return app(e, num(0))
    if tag in ("int", "bool"):
        return e
    if tag == "prim":
        return prim(e[1], by_name(e[2], name), by_name(e[3], name))
    if tag == "if":
        return ("if", by_name(e[1], name), by_name(e[2], name), by_name(e[3], name))
    if tag == "let":
        return ("let", e[1], thunk(by_name(e[2], name)), by_name(e[3], name))
    args = []
    while e[0] == "app":
        args.append(e[2])
        e = e[1]
    out = e
    for a in reversed(args):
        out = app(out, thunk(by_name(a, name)))
    return out


def run_lazily(name, params, body, args):
    """Run f a1 ... ak with lazy arguments; args are closed terms. Returns toylam's result."""
    f = function(name, params, by_name(body, name))
    return L.evaluate(call_term(f, [thunk(a) for a in args]), FUEL)


def call_term(f, args):
    e = f
    for a in args:
        e = app(e, a)
    return e


# The worked example: f x y z = if x == 0 then y else f (x - 1) z y.
SWAP_BODY = ("if", prim("==", V("x"), num(0)), V("y"),
             call("f", prim("-", V("x"), num(1)), V("z"), V("y")))
SWAP = function("f", ["x", "y", "z"], SWAP_BODY)


def test_worked_example():
    table, strict, rounds = analyse(SWAP)
    for (x, y, z), r in table.items():
        assert r == x & (y | z)
    assert strict == [True, False, False]
    assert rounds == 3
    fn = parse_function(SWAP)
    zero = {v: 0 for v in table}
    t1 = kleene_step(fn, zero)
    assert all(t1[v] == v[0] & v[1] for v in t1)
    t2 = kleene_step(fn, t1)
    assert t2 == table


def test_worked_example_runs():
    params = ["x", "y", "z"]
    assert run_lazily("f", params, SWAP_BODY, [num(3), OMEGA, num(5)]) == ("value", num(5))
    assert run_lazily("f", params, SWAP_BODY, [num(2), OMEGA, num(5)]) == ("fuel",)
    assert run_lazily("f", params, SWAP_BODY, [OMEGA, num(1), num(5)]) == ("fuel",)


def test_omega_diverges():
    assert L.evaluate(OMEGA, FUEL) == ("fuel",)


def test_accumulator_is_strict():
    body = ("if", prim("==", V("n"), num(0)), V("a"),
            call("s", prim("-", V("n"), num(1)), prim("+", V("a"), V("n"))))
    _, strict, _ = analyse(function("s", ["n", "a"], body))
    assert strict == [True, True]
    assert run_lazily("s", ["n", "a"], body, [num(4), num(0)]) == ("value", num(10))


def test_small_cases():
    # no recursion
    assert analyse(function(None, ["x", "y"], prim("+", V("x"), num(1))))[1] == [True, False]
    # a constant function is strict in nothing
    table, strict, _ = analyse(function(None, ["x"], num(3)))
    assert strict == [False] and table[(0,)] == 1
    # f x = f x is undefined everywhere, so it is strict
    table, strict, _ = analyse(function("f", ["x"], call("f", V("x"))))
    assert strict == [True] and set(table.values()) == {0}
    # a lazy let does not force its right side
    assert analyse(function(None, ["x"], ("let", "y", V("x"), num(5))))[1] == [False]
    assert analyse(function(None, ["x"], ("let", "y", V("x"), V("y"))))[1] == [True]
    # a let may hide a parameter
    body = ("let", "x", num(1), V("x"))
    assert analyse(function(None, ["x"], body))[1] == [False]
    # a condition is always computed, a branch is not
    body = ("if", prim("<", V("x"), num(1)), V("y"), num(0))
    assert analyse(function(None, ["x", "y"], body))[1] == [True, False]


def test_rejects_other_terms():
    bad = [
        num(1),
        function("f", ["x"], V("f")),
        function("f", ["x", "y"], call("f", V("x"))),
        function(None, ["x"], prim("+", V("x"), app(lam("y", V("y")), num(1)))),
        function(None, ["x"], V("y")),
        function("f", ["x"], ("let", "f", num(1), V("x"))),
    ]
    for t in bad:
        try:
            parse_function(t)
        except ValueError:
            continue
        raise AssertionError(f"accepted {t!r}")


def is_monotone(table):
    return all(table[a] <= table[b] for a in table for b in table
               if all(p <= q for p, q in zip(a, b)))


def brute_force_lfp(fn, k):
    """The least fixed point found among all 2^(2^k) tables."""
    points = list(product((0, 1), repeat=k))
    fixed = []
    for bits in product((0, 1), repeat=len(points)):
        t = dict(zip(points, bits))
        if kleene_step(fn, t) == t:
            fixed.append(t)
    least = [t for t in fixed if all(all(t[v] <= s[v] for v in points) for s in fixed)]
    assert len(least) == 1
    return least[0]


# A random generator of well typed first-order functions with int results.
def gen_int(rng, depth, scope, name, k):
    if depth <= 0 or rng.random() < 0.2:
        if scope and rng.random() < 0.7:
            return V(rng.choice(scope))
        return num(rng.randint(0, 3))
    r = rng.random()
    d = depth - 1
    if r < 0.3:
        return ("if", gen_bool(rng, d, scope, name, k), gen_int(rng, d, scope, name, k),
                gen_int(rng, d, scope, name, k))
    if r < 0.55:
        return prim(rng.choice("+-*"), gen_int(rng, d, scope, name, k), gen_int(rng, d, scope, name, k))
    if r < 0.7:
        x = rng.choice(("p", "q"))
        return ("let", x, gen_arg(rng, scope), gen_int(rng, d, scope + [x], name, k))
    if name and r < 0.9:
        return call(name, *[gen_arg(rng, scope) for _ in range(k)])
    return V(rng.choice(scope)) if scope else num(1)


def gen_arg(rng, scope):
    """An argument of a call: at most one name, so the thunks of a lazy run stay small."""
    r = rng.random()
    if not scope or r < 0.2:
        return num(rng.randint(0, 3))
    x = V(rng.choice(scope))
    if r < 0.6:
        return x
    return prim(rng.choice("+-"), x, num(rng.randint(1, 2)))


def gen_bool(rng, depth, scope, name, k):
    return prim(rng.choice(("<", "==")), gen_int(rng, depth, scope, name, k),
                gen_int(rng, depth, scope, name, k))


def random_function(rng):
    k = rng.randint(1, 3)
    params = ["x", "y", "z"][:k]
    name = "f" if rng.random() < 0.8 else None
    if name:
        # guard the recursion with a test on the first argument, so many runs stop
        body = ("if", prim("<", V("x"), num(1)), gen_int(rng, 2, params, None, k),
                gen_int(rng, 3, params, name, k))
    else:
        body = gen_int(rng, 4, params, None, k)
    return name, params, body


def test_random_against_lazy_runs():
    """If the analysis says f is strict in x_i, then f with a looping x_i must not stop."""
    rng = random.Random(2024)
    checked = stopped_when_lazy = 0
    for _ in range(600):
        name, params, body = random_function(rng)
        table, strict, rounds = analyse(function(name, params, body))
        k = len(params)
        assert is_monotone(table)
        assert rounds <= 2 ** k + 1
        for i in range(k):
            args = [num(rng.randint(-2, 4)) for _ in range(k)]
            args[i] = OMEGA
            result = run_lazily(name, params, body, args)
            if strict[i]:
                checked += 1
                assert result[0] != "value", (L.show(body), i, result)
            elif result[0] == "value":
                stopped_when_lazy += 1
    assert checked >= 300 and stopped_when_lazy >= 100


def test_random_against_brute_force_lfp():
    rng = random.Random(7)
    for _ in range(500):
        name, params, body = random_function(rng)
        if len(params) > 2:
            continue
        fn = parse_function(function(name, params, body))
        table, _, _ = analyse(function(name, params, body))
        assert table == brute_force_lfp(fn, len(params))
        for v in table:
            assert abstract_eval(fn, v, table) == table[v]
