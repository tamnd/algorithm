# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cps-conversion/. The authors are listed in prov/J9VE11.jsonl.

import random

import toylam
from cps_conversion import (
    Fresh,
    administrative_normal,
    administrative_redexes,
    alpha_equal,
    cps,
    names,
    plotkin,
    plotkin_program,
    rename_apart,
    tail,
)


def v(x):
    return ("var", x)


def app(*ts):
    out = ts[0]
    for t in ts[1:]:
        out = ("app", out, t)
    return out


def run(e, fuel):
    """toylam.evaluate, with a term that grows too deep counted as out of fuel."""
    try:
        return toylam.evaluate(e, fuel)
    except RecursionError:
        return ("fuel",)


def same_outcome(src, out):
    """Equal int and bool results, a function for a function, stuck for stuck."""
    if src[0] != out[0]:
        return False
    if src[0] != "value":
        return True
    fun = ("lam", "fix")
    if src[1][0] in fun or out[1][0] in fun:
        return src[1][0] in fun and out[1][0] in fun
    return src[1] == out[1]


def random_pure(rng, depth, scope=()):
    """A random term built from variables, functions and calls only."""
    if depth <= 0 or (scope and rng.random() < 0.25):
        return v(rng.choice(scope)) if scope else ("lam", "x", v("x"))
    if rng.random() < 0.4:
        x = rng.choice(toylam.NAMES)
        return ("lam", x, random_pure(rng, depth - 1, scope + (x,)))
    return ("app", random_pure(rng, depth - 1, scope), random_pure(rng, depth - 1, scope))


# ------------------------------------------------------------ the CPS grammar


def trivial_ok(e):
    tag = e[0]
    if tag in ("var", "int", "bool"):
        return True
    body = e[3] if tag == "fix" else e[2] if tag == "lam" else None
    if body is None:
        return False
    if body[0] == "lam":  # fun x -> fun k -> S
        body = body[2]
    return serious_ok(body)


def serious_ok(e):
    """e is a serious CPS term: every call in it is a tail call whose operator
    and arguments are trivial."""
    tag = e[0]
    if tag == "app":
        parts = []
        while e[0] == "app":
            parts.append(e[2])
            e = e[1]
        parts.append(e)
        return len(parts) in (2, 3) and all(trivial_ok(p) for p in parts)
    if tag == "let":
        rhs = e[2]
        if rhs[0] == "prim":
            ok = trivial_ok(rhs[2]) and trivial_ok(rhs[3])
        else:
            ok = trivial_ok(rhs)
        return ok and serious_ok(e[3])
    if tag == "if":
        return trivial_ok(e[1]) and serious_ok(e[2]) and serious_ok(e[3])
    return False


# ------------------------------------------------------------ page examples


EXAMPLE = ("let", "f", ("lam", "x", ("prim", "+", v("x"), ("int", 1))), app(v("f"), app(v("f"), ("int", 2))))


def test_page_example():
    out = cps(EXAMPLE)
    assert toylam.show(out) == (
        "(let k3 = (fun a4 -> a4) in (let f2 = (fun x1 -> (fun k5 -> (let t6 = (x1 + 1) in (k5 t6))))"
        " in ((f2 2) (fun t7 -> ((f2 t7) k3)))))"
    )
    assert toylam.evaluate(out) == ("value", ("int", 4))
    fresh = Fresh(names(EXAMPLE))
    p = plotkin_program(EXAMPLE, fresh)
    assert toylam.size(p) == 66 and toylam.size(out) == 23
    assert administrative_redexes(p, fresh.source) == 9
    assert toylam.evaluate(p) == ("value", ("int", 4))
    fresh = Fresh(names(EXAMPLE) | {"k"})
    e = rename_apart(EXAMPLE, fresh)
    reduced = administrative_normal(app(plotkin(e, fresh), v("k")), fresh.source)
    assert toylam.show(reduced) == (
        "(let f2 = (fun x1 -> (fun k15 -> (let t18 = (x1 + 1) in (k15 t18)))) in ((f2 2) (fun v7 -> ((f2 v7) k))))"
    )
    assert alpha_equal(reduced, tail(e, v("k"), fresh))


def test_nested_call():
    e = app(app(v("f"), v("x")), app(v("g"), v("y")))
    assert toylam.show(tail(e, v("k"), Fresh(names(e)))) == "((f x) (fun t1 -> ((g y) (fun t2 -> ((t1 t2) k)))))"
    fresh = Fresh(names(e))
    p = plotkin(e, fresh)
    assert administrative_redexes(p, fresh.source) == 6 and toylam.size(p) == 46
    reduced = administrative_normal(app(p, v("k")), fresh.source)
    assert toylam.show(reduced) == "((f x) (fun v2 -> ((g y) (fun v3 -> ((v2 v3) k)))))"


def test_call_by_value_order_is_kept():
    loop = app(("fix", "f", "x", app(v("f"), v("x"))), ("int", 0))
    e = app(("lam", "y", ("int", 1)), loop)
    assert run(e, 2000) == ("fuel",)
    # A call-by-name reading would return 1. The CBV translation must loop.
    assert run(cps(e), 20000) == ("fuel",)
    assert run(plotkin_program(e), 20000) == ("fuel",)


# ------------------------------------------------------------ random terms


def test_random_terms_keep_their_outcome():
    rng = random.Random(20261115)
    compared = 0
    for _ in range(1500):
        e = toylam.random_term(rng, 5)
        want = run(e, 300)
        if want == ("fuel",):
            continue
        assert same_outcome(want, run(cps(e), 20000)), toylam.show(e)
        assert same_outcome(want, run(plotkin_program(e), 20000)), toylam.show(e)
        compared += 1
    assert compared > 1400


def test_every_call_is_a_tail_call():
    rng = random.Random(7)
    for _ in range(1500):
        out = cps(toylam.random_term(rng, 6))
        assert out[0] == "let" and serious_ok(out[3])


def test_no_administrative_redex():
    rng = random.Random(11)
    made = 0
    for _ in range(1000):
        e = toylam.random_term(rng, 6)
        fresh = Fresh(names(e))
        assert administrative_redexes(cps(e, fresh), fresh.source) == 0
        fresh = Fresh(names(e))
        made += administrative_redexes(plotkin_program(e, fresh), fresh.source)
    assert made > 1000


def test_one_pass_is_plotkin_then_administrative_reduction():
    rng = random.Random(3)
    for _ in range(800):
        e = random_pure(rng, 6)
        fresh = Fresh(names(e) | {"k"})
        e = rename_apart(e, fresh)
        reduced = administrative_normal(app(plotkin(e, fresh), v("k")), fresh.source)
        assert alpha_equal(reduced, tail(e, v("k"), fresh)), toylam.show(e)


def test_output_size_is_linear():
    rng = random.Random(5)
    for _ in range(1500):
        e = toylam.random_term(rng, 7)
        assert toylam.size(cps(e)) <= 6 * toylam.size(e) + 4
