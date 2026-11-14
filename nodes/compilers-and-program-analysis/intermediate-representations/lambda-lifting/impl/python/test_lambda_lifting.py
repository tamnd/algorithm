# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lambda-lifting/. The authors are listed in prov/ZHK5BH.jsonl.

import random

import lambda_lifting as ll
import toylam


def v(x):
    return ("var", x)


def n(k):
    return ("int", k)


def run(evaluate, *args):
    """evaluate(*args), with a term that grows too deep counted as out of fuel."""
    try:
        return evaluate(*args)
    except RecursionError:
        return ("fuel",)


def same_outcome(src, out):
    """Equal int and bool results, a global or a partial call for a function, stuck for stuck."""
    if src[0] != out[0]:
        return False
    if src[0] != "value":
        return True
    if src[1][0] in ("lam", "fix"):
        return ll.spine(out[1])[0][0] == "global"
    return src[1] == out[1]


def target_fv(e):
    tag = e[0]
    if tag == "var":
        return {e[1]}
    if tag in ("int", "bool", "global"):
        return set()
    if tag == "let":
        return target_fv(e[2]) | (target_fv(e[3]) - {e[1]})
    if tag == "prim":
        return target_fv(e[2]) | target_fv(e[3])
    assert tag in ("app", "if"), tag
    out = set()
    for p in e[1:]:
        out |= target_fv(p)
    return out


def first_order(e):
    """No fun, fix or letrec anywhere in a target term."""
    tag = e[0]
    if tag in ("lam", "fix", "letrec"):
        return False
    if tag in ("var", "int", "bool", "global"):
        return True
    start = 2 if tag in ("let", "prim") else 1
    return all(first_order(p) for p in e[start:])


def check_top_level(defs, main):
    assert first_order(main) and target_fv(main) == set()
    for params, body in defs.values():
        assert first_order(body)
        assert target_fv(body) <= set(params)


# ------------------------------------------------------------ page examples


EXAMPLE = (
    "let", "a", n(1),
    ("app",
     ("fix", "f", "x",
      ("if", ("prim", "<", v("x"), n(1)), v("a"),
       ("app", ("lam", "y", ("prim", "+", ("app", v("f"), v("y")), v("x"))), ("prim", "-", v("x"), n(1))))),
     n(3)),
)

SIMPLE = (
    "let", "a", n(1),
    ("let", "b", n(2),
     ("let", "f", ("lam", "x", ("prim", "+", ("prim", "+", v("x"), v("a")), v("b"))),
      ("app", v("f"), n(10)))),
)

MUTUAL = (
    "let", "d", n(1),
    ("letrec",
     (("f", "n", ("if", ("prim", "<", v("n"), n(1)), n(0), ("app", v("g"), v("n")))),
      ("g", "n", ("app", v("h"), v("n"))),
      ("h", "n", ("prim", "+", n(1), ("app", v("f"), ("prim", "-", v("n"), v("d")))))),
     ("app", v("f"), n(3))),
)


def test_page_example():
    defs, main = ll.lambda_lift(EXAMPLE)
    assert ll.show_program(defs, main) == [
        "F2 a1 x4 = (if (x4 < 1) then a1 else (F5 a1 x4 (x4 - 1)))",
        "F5 a1 x4 y6 = ((F2 a1 y6) + x4)",
        "main = (let a1 = 1 in (F2 a1 3))",
    ]
    assert toylam.evaluate(EXAMPLE) == ll.evaluate(defs, main) == ("value", n(7))
    check_top_level(defs, main)


def test_function_value_becomes_partial_call():
    defs, main = ll.lambda_lift(SIMPLE)
    assert ll.show_program(defs, main) == [
        "F3 a1 b2 x4 = ((x4 + a1) + b2)",
        "main = (let a1 = 1 in (let b2 = 2 in (let f5 = (F3 a1 b2) in (f5 10))))",
    ]
    assert toylam.evaluate(SIMPLE) == ll.evaluate(defs, main) == ("value", n(13))


def test_mutual_recursion_needs_the_fixed_point():
    defs, main = ll.lambda_lift(MUTUAL)
    assert ll.show_program(defs, main) == [
        "F2 d1 n8 = (if (n8 < 1) then 0 else (F3 d1 n8))",
        "F3 d1 n9 = (F4 d1 n9)",
        "F4 d1 n10 = (1 + (F2 d1 (n10 - d1)))",
        "main = (let d1 = 1 in (F2 d1 3))",
    ]
    assert ll.evaluate(defs, main) == ("value", n(3))
    check_top_level(defs, main)
    # With only their own free variables, f and g get no parameter d,
    # and the call of g inside f then passes an unbound d.
    defs1, main1 = ll.lambda_lift(MUTUAL, transitive=False)
    assert ll.show_program(defs1, main1) == [
        "F2 n8 = (if (n8 < 1) then 0 else (F3 n8))",
        "F3 n9 = (F4 d1 n9)",
        "F4 d1 n10 = (1 + (F2 (n10 - d1)))",
        "main = (let d1 = 1 in (F2 3))",
    ]
    assert target_fv(defs1["F3"][1]) == {"d1", "n9"}
    assert ll.evaluate(defs1, main1)[0] == "stuck"


# ------------------------------------------------------------ random terms


def test_random_terms_keep_their_outcome():
    rng = random.Random(20261115)
    compared = applied = 0
    for _ in range(1500):
        e = toylam.random_term(rng, 5)
        want = run(toylam.evaluate, e, 300)
        if want == ("fuel",):
            continue
        defs, main = ll.lambda_lift(e)
        got = run(ll.evaluate, defs, main, 20000)
        assert same_outcome(want, got), toylam.show(e)
        compared += 1
        if want[0] == "value" and want[1][0] in ("lam", "fix"):
            for arg in (n(0), n(2), ("bool", True)):
                w2 = run(toylam.evaluate, ("app", want[1], arg), 300)
                if w2 == ("fuel",):
                    continue
                assert same_outcome(w2, run(ll.evaluate, defs, ("app", got[1], arg), 20000))
                applied += 1
    assert compared > 1400 and applied > 300


def test_every_function_is_at_the_top_level():
    rng = random.Random(7)
    lifted = 0
    for _ in range(1500):
        e = toylam.random_term(rng, 6)
        defs, main = ll.lambda_lift(e)
        check_top_level(defs, main)
        lifted += len(defs)
    assert lifted > 1000
