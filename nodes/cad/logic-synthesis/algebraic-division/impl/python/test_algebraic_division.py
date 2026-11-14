# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/algebraic-division/. The authors are listed in prov/NKSP1R.jsonl.

import itertools
import random

import pytest

from algebraic_division import (
    algebraic_product,
    evaluate,
    literals,
    parse,
    show,
    support,
    weak_divide,
)


def brute_quotient(f, d):
    """Every cube q over the variables of f outside sup(d) with q x d inside f."""
    sd = support(d)
    free = sorted(support(f) - sd)
    q = set()
    for choice in itertools.product((None, 0, 1), repeat=len(free)):
        cube = frozenset(2 * v + c for v, c in zip(free, choice) if c is not None)
        if all(cube | di in f for di in d):
            q.add(cube)
    return frozenset(q)


def same_function(f, g, variables) -> bool:
    for bits in itertools.product((0, 1), repeat=len(variables)):
        point = dict(zip(variables, bits))
        if evaluate(f, point) != evaluate(g, point):
            return False
    return True


def test_page_example() -> None:
    f = parse("ac + ad + bc + bd + e")
    q, r = weak_divide(f, parse("a + b"))
    assert show(q) == "c + d" and show(r) == "e"
    assert (literals(f), literals(q) + 2 + literals(r)) == (9, 5)


def test_partial_quotient() -> None:
    q, r = weak_divide(parse("ac + ad + bc + be"), parse("a + b"))
    assert show(q) == "c" and show(r) == "ad + be"


def test_boolean_divisor_not_found() -> None:
    # a + bc = (a + b)(a + c) as functions, but the algebraic quotient is empty
    f = parse("a + bc")
    q, r = weak_divide(f, parse("a + b"))
    assert q == frozenset() and r == f
    g = parse("a + b")
    h = parse("a + c")
    prod = frozenset(x | y for x in g for y in h)
    assert same_function(prod, f, [0, 1, 2])


def test_edge_cases() -> None:
    f = parse("ab + c")
    assert weak_divide(f, parse("1")) == (f, frozenset())
    assert weak_divide(f, f) == (frozenset([frozenset()]), frozenset())
    assert weak_divide(frozenset(), parse("a")) == (frozenset(), frozenset())
    assert weak_divide(f, parse("d")) == (frozenset(), f)
    q, r = weak_divide(parse("ab + a'c"), parse("a"))
    assert show(q) == "b" and show(r) == "a'c"
    with pytest.raises(ZeroDivisionError):
        weak_divide(f, frozenset())


def random_cube(rng, variables):
    k = rng.randrange(0, len(variables) + 1)
    return frozenset(2 * v + rng.randrange(2) for v in rng.sample(variables, k))


def test_random_against_brute_force() -> None:
    rng = random.Random(7)
    nonempty = 0
    for _ in range(800):
        n = rng.randrange(2, 7)
        variables = list(range(n))
        rng.shuffle(variables)
        cut = rng.randrange(1, n)
        dv, qv = variables[:cut], variables[cut:]
        d = frozenset(random_cube(rng, dv) for _ in range(rng.randrange(1, 4)))
        planted = frozenset(random_cube(rng, qv) for _ in range(rng.randrange(0, 4)))
        noise = frozenset(random_cube(rng, list(range(n))) for _ in range(rng.randrange(0, 5)))
        f = algebraic_product(planted, d) | noise
        q, r = weak_divide(f, d)
        assert q == brute_quotient(f, d)
        assert planted <= q
        assert not support(q) & support(d)
        qd = algebraic_product(q, d)
        assert qd | r == f and not qd & r
        assert same_function(f, qd | r, list(range(n)))
        nonempty += bool(q)
    assert nonempty > 400


def test_random_divisors_with_shared_variables() -> None:
    rng = random.Random(11)
    for _ in range(600):
        n = rng.randrange(1, 6)
        variables = list(range(n))
        f = frozenset(random_cube(rng, variables) for _ in range(rng.randrange(0, 7)))
        d = frozenset(random_cube(rng, variables) for _ in range(rng.randrange(1, 3)))
        q, r = weak_divide(f, d)
        assert q == brute_quotient(f, d)
        assert algebraic_product(q, d) | r == f
