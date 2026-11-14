# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/closure-conversion/. The authors are listed in prov/EGE7J5.jsonl.

import random

import closure_conversion as cc
import toylam


def v(x):
    return ("var", x)


def run(e, fuel, evaluate):
    """evaluate(e, fuel), with a term that grows too deep counted as out of fuel."""
    try:
        return evaluate(e, fuel)
    except RecursionError:
        return ("fuel",)


def same_outcome(src, out):
    """Equal int and bool results, a closure record for a function, stuck for stuck."""
    if src[0] != out[0]:
        return False
    if src[0] != "value":
        return True
    if src[1][0] in ("lam", "fix"):
        return out[1][0] == "tuple"
    return src[1] == out[1]


def call_closure(w, arg):
    """The target term that calls the closure record w with arg."""
    return ("app", ("app", ("proj", w, 0), w), arg)


def code_parts(e):
    """All code terms fun self -> fun x -> body of a target term."""
    out = []
    tag = e[0]
    if tag == "tuple":
        out.append(e[1][0])
        for p in e[1]:
            out += code_parts(p)
    elif tag == "lam":
        out += code_parts(e[2])
    elif tag == "proj":
        out += code_parts(e[1])
    elif tag in ("let", "prim"):
        out += code_parts(e[2]) + code_parts(e[3])
    elif tag in ("app", "if"):
        for p in e[1:]:
            out += code_parts(p)
    return out


def lambdas_only_in_code(e, in_code=False):
    """Every fun is the code of a record or the inner fun of such code, and there is no fix."""
    tag = e[0]
    if tag == "fix":
        return False
    if tag == "lam":
        if not in_code:
            return False
        inner = e[2]
        return inner[0] == "lam" and lambdas_only_in_code(inner[2])
    if tag == "tuple":
        return lambdas_only_in_code(e[1][0], True) and all(lambdas_only_in_code(p) for p in e[1][1:])
    if tag == "proj":
        return lambdas_only_in_code(e[1])
    if tag in ("let", "prim"):
        return lambdas_only_in_code(e[2]) and lambdas_only_in_code(e[3])
    if tag in ("app", "if"):
        return all(lambdas_only_in_code(p) for p in e[1:])
    return True


# ------------------------------------------------------------ page examples


EXAMPLE = (
    "let", "a", ("int", 1),
    ("let", "b", ("int", 2),
     ("let", "f", ("lam", "x", ("prim", "+", ("prim", "+", v("x"), v("a")), v("b"))),
      ("app", v("f"), ("int", 10)))),
)

FACT = (
    "let", "m", ("int", 1),
    ("app",
     ("fix", "f", "n",
      ("if", ("prim", "<", v("n"), ("int", 1)), v("m"),
       ("prim", "*", v("n"), ("app", v("f"), ("prim", "-", v("n"), ("int", 1)))))),
     ("int", 5)),
)


def test_page_example():
    out = cc.closure_convert(EXAMPLE)
    assert cc.show(out) == (
        "(let a = 1 in (let b = 2 in (let f = [(fun self1 -> (fun x -> ((x + self1.1) + self1.2))), a, b]"
        " in (let c2 = f in (let a3 = 10 in ((c2.0 c2) a3))))))"
    )
    assert toylam.evaluate(EXAMPLE) == cc.evaluate(out) == ("value", ("int", 13))


def test_recursion_through_self():
    out = cc.closure_convert(FACT)
    assert cc.show(out) == (
        "(let m = 1 in (let c1 = [(fun self3 -> (fun n -> (if (n < 1) then self3.1 else"
        " (n * (let c4 = self3 in (let a5 = (n - 1) in ((c4.0 c4) a5))))))), m]"
        " in (let a2 = 5 in ((c1.0 c1) a2))))"
    )
    assert cc.evaluate(out) == ("value", ("int", 120))


def test_flat_closures_can_be_quadratic():
    for k in range(1, 12):
        body = v("x1")
        for i in range(2, k + 1):
            body = ("prim", "+", body, v(f"x{i}"))
        for i in range(k, 0, -1):
            body = ("lam", f"x{i}", body)
        out = cc.closure_convert(body)
        captured = sum(len(code_record) - 1 for code_record in records(out))
        assert captured == k * (k - 1) // 2


def records(e):
    out = []
    if e[0] == "tuple":
        out.append(e[1])
    for p in e[1:]:
        if isinstance(p, tuple) and p and isinstance(p[0], str):
            out += records(p)
        elif isinstance(p, tuple):
            for q in p:
                out += records(q)
    return out


# ------------------------------------------------------------ random terms


def test_random_terms_keep_their_outcome():
    rng = random.Random(20261115)
    compared = applied = 0
    for _ in range(1500):
        e = toylam.random_term(rng, 5)
        want = run(e, 300, toylam.evaluate)
        if want == ("fuel",):
            continue
        got = run(cc.closure_convert(e), 20000, cc.evaluate)
        assert same_outcome(want, got), toylam.show(e)
        compared += 1
        if want[0] == "value" and want[1][0] in ("lam", "fix"):
            for arg in (("int", 0), ("int", 2), ("bool", True)):
                w2 = run(("app", want[1], arg), 300, toylam.evaluate)
                if w2 == ("fuel",):
                    continue
                assert same_outcome(w2, run(call_closure(got[1], arg), 20000, cc.evaluate))
                applied += 1
    assert compared > 1400 and applied > 500


def test_code_has_no_free_variable_but_its_environment():
    rng = random.Random(7)
    for _ in range(1500):
        out = cc.closure_convert(toylam.random_term(rng, 6))
        assert cc.free_vars(out) == set()
        assert lambdas_only_in_code(out)
        for code in code_parts(out):
            assert cc.free_vars(code) == set()
