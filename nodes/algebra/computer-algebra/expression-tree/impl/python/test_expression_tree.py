# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/expression-tree/. The authors are listed in prov/5TDXMG.jsonl.

import random
from fractions import Fraction
from typing import Dict, List, Tuple

import pytest

from expression_tree import (
    Expr,
    add,
    const,
    diff,
    equal,
    eval_expr,
    height,
    mul,
    power,
    size,
    sub,
    subs,
    sym,
    to_string,
)

Poly = Dict[Tuple[int, int], Fraction]  # exponents of (x, y) -> coefficient


def expand(e: Expr) -> Poly:
    """Independent oracle: the polynomial in Q[x, y] that e denotes."""
    out: Dict[int, Poly] = {}
    stack: List[Tuple[Expr, bool]] = [(e, False)]
    while stack:
        u, done = stack.pop()
        if not u.kids:
            if u.op == "const":
                out[id(u)] = {(0, 0): u.val} if u.val != 0 else {}
            else:
                out[id(u)] = {(1, 0) if u.val == "x" else (0, 1): Fraction(1)}
        elif not done:
            stack.append((u, True))
            stack.extend((k, False) for k in u.kids)
        else:
            a, b = (out[id(k)] for k in u.kids)
            if u.op in "+-":
                r = dict(a)
                for m, c in b.items():
                    r[m] = r.get(m, 0) + (c if u.op == "+" else -c)
            elif u.op == "*":
                r = pmul(a, b)
            else:
                r = {(0, 0): Fraction(1)}
                for _ in range(int(u.kids[1].val)):
                    r = pmul(r, a)
            out[id(u)] = {m: c for m, c in r.items() if c != 0}
    return out[id(e)]


def pmul(a: Poly, b: Poly) -> Poly:
    r: Poly = {}
    for (i, j), c in a.items():
        for (k, l), d in b.items():
            r[(i + k, j + l)] = r.get((i + k, j + l), 0) + c * d
    return {m: c for m, c in r.items() if c != 0}


def pdiff_x(a: Poly) -> Poly:
    return {(i - 1, j): c * i for (i, j), c in a.items() if i > 0}


def py_eval(e: Expr, env: Dict[str, Fraction]) -> Fraction:
    """Second oracle: Python's own parser and arithmetic on the printed form."""
    return Fraction(eval(to_string(e), {"Fraction": Fraction}, dict(env)))


def rand_tree(rng: random.Random, depth: int) -> Expr:
    if depth == 0 or rng.random() < 0.25:
        r = rng.random()
        if r < 0.4:
            return const(Fraction(rng.randint(-5, 5), rng.randint(1, 3)))
        return sym("x" if r < 0.75 else "y")
    op = rng.choice("+-*^" if depth > 1 else "+-*")
    if op == "^":
        return power(rand_tree(rng, depth - 2), rng.randint(0, 3))
    a, b = rand_tree(rng, depth - 1), rand_tree(rng, depth - 1)
    return {"+": add, "-": sub, "*": mul}[op](a, b)


def example() -> Expr:
    return mul(add(sym("x"), const(3)), sub(sym("x"), sym("y")))


def test_worked_example() -> None:
    e = example()
    e.check_invariant()
    assert size(e) == 7 and height(e) == 2
    assert eval_expr(e, {"x": 2, "y": 5}) == -15
    assert e.eval({"x": 2, "y": 5}) == -15
    d = diff(e, "x")
    # d/dx (x+3)(x-y) = (x - y) + (x + 3)
    assert to_string(d) == "((x - y) + (x + (3)))"
    assert eval_expr(d, {"x": 2, "y": 5}) == 2
    s = subs(e, "x", add(sym("y"), const(1)))
    assert to_string(s) == "(((y + (1)) + (3)) * ((y + (1)) - y))"
    assert eval_expr(s, {"y": 0}) == 4


def test_atoms_and_edge_cases() -> None:
    assert eval_expr(const(0), {}) == 0
    assert eval_expr(sym("x"), {"x": 7}) == 7
    assert size(const(4)) == 1 and height(sym("x")) == 0
    assert equal(diff(const(4), "x"), const(0))
    assert equal(diff(sym("y"), "x"), const(0))
    assert equal(diff(sym("x"), "x"), const(1))
    assert equal(diff(power(sym("x"), 0), "x"), const(0))
    assert eval_expr(power(sym("x"), 0), {"x": 0}) == 1
    assert subs(const(2), "x", sym("y")).val == 2
    with pytest.raises(ValueError):
        power(sym("x"), -1)
    with pytest.raises(KeyError):
        eval_expr(sym("z"), {"x": 1})


def test_deep_tree_no_recursion() -> None:
    e: Expr = sym("x")
    for i in range(50000):
        e = add(e, const(1)) if i % 2 == 0 else sub(e, const(Fraction(1, 2)))
    e.check_invariant()
    assert height(e) == 50000
    assert eval_expr(e, {"x": 0}) == Fraction(25000, 2)
    assert eval_expr(diff(e, "x"), {"x": 9}) == 1
    assert eval_expr(subs(e, "x", const(1)), {}) == 12501
    assert equal(e, e) and not equal(e, add(e, const(0)))


def test_equal_is_syntactic() -> None:
    a = add(sym("x"), sym("y"))
    b = add(sym("x"), sym("y"))
    c = add(sym("y"), sym("x"))
    assert equal(a, b) and not equal(a, c)
    assert eval_expr(a, {"x": 1, "y": 2}) == eval_expr(c, {"x": 1, "y": 2})


def test_random_against_oracles() -> None:
    rng = random.Random(20261107)
    for _ in range(600):
        e = rand_tree(rng, rng.randint(1, 6))
        e.check_invariant()
        p = expand(e)
        for _ in range(3):
            env = {"x": Fraction(rng.randint(-6, 6), rng.randint(1, 4)), "y": Fraction(rng.randint(-6, 6))}
            v = eval_expr(e, env)
            assert v == py_eval(e, env)
            assert v == sum(c * env["x"] ** i * env["y"] ** j for (i, j), c in p.items())
        # derivative: the expansion of diff(e) is d/dx of the expansion of e
        d = diff(e, "x")
        d.check_invariant()
        assert expand(d) == pdiff_x(p)
        # substitution law: eval(subs(e, x, r), env) = eval(e, env[x := eval(r, env)])
        r = rand_tree(rng, 3)
        env = {"x": Fraction(rng.randint(-4, 4)), "y": Fraction(rng.randint(-4, 4), 3)}
        se = subs(e, "x", r)
        se.check_invariant()
        assert eval_expr(se, env) == eval_expr(e, {"x": eval_expr(r, env), "y": env["y"]})
        assert equal(subs(e, "z", r), e)
        assert equal(e, rand_tree(random.Random(0), 0)) == (to_string(e) == to_string(rand_tree(random.Random(0), 0)))
