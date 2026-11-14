# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/signal-probability-propagation/. The authors are listed in prov/CC4R1Y.jsonl.

import itertools
import random
from fractions import Fraction

from netlist import KINDS, Circuit, random_circuit
from signal_probability_propagation import (
    Poly,
    exact_probabilities,
    gate_formula,
    probability_polynomials,
    propagate,
    signal_probabilities,
)

HALF = Fraction(1, 2)


def brute_force(c, p):
    """Exact P(node = 1) by enumeration of all 2^n input vectors, in Fraction."""
    out = {v: Fraction(0) for v in c.nodes}
    for x in itertools.product((0, 1), repeat=len(c.inputs)):
        w = Fraction(1)
        for name, b in zip(c.inputs, x):
            w *= p[name] if b else 1 - p[name]
        if w == 0:
            continue
        val = c.evaluate(x)
        for v in c.nodes:
            if val[v]:
                out[v] += w
    return out


def random_probs(rng, c):
    return {x: Fraction(rng.randint(0, 8), 8) for x in c.inputs}


# y = ab + ac, the reconvergent example of the page.
RECONV = Circuit(["a", "b", "c"], [("u", "AND", ["a", "b"]), ("v", "AND", ["a", "c"]), ("y", "OR", ["u", "v"])])

# The fanout-free example of the page: y = (a AND b) OR (NOT c), z = y XOR d.
TREE = Circuit(
    ["a", "b", "c", "d"],
    [("u", "AND", ["a", "b"]), ("w", "NOT", ["c"]), ("y", "OR", ["u", "w"]), ("z", "XOR", ["y", "d"])],
)


def test_gate_formulas_against_truth_tables():
    rng = random.Random(1)
    for kind in KINDS:
        arity = [1] if kind in ("BUF", "NOT") else [2, 3, 4]
        for k in arity:
            for _ in range(5):
                c = Circuit([f"i{j}" for j in range(k)], [("o", kind, [f"i{j}" for j in range(k)])])
                p = random_probs(rng, c)
                assert gate_formula(kind, [p[x] for x in c.inputs]) == brute_force(c, p)["o"]


def test_page_examples():
    p = {"a": HALF, "b": HALF, "c": HALF}
    assert brute_force(RECONV, p)["y"] == Fraction(3, 8)
    assert propagate(RECONV, p)["y"] == Fraction(7, 16)
    assert exact_probabilities(RECONV, p)["y"] == Fraction(3, 8)
    poly = probability_polynomials(RECONV)["y"]
    assert poly == Poly({frozenset("ab"): 1, frozenset("ac"): 1, frozenset("abc"): -1})
    assert signal_probabilities(RECONV, p, "numeric") == propagate(RECONV, p)
    q = {"a": Fraction(1, 2), "b": Fraction(1, 4), "c": Fraction(3, 4), "d": Fraction(1, 3)}
    exact = brute_force(TREE, q)
    assert propagate(TREE, q) == exact
    assert exact["y"] == Fraction(11, 32) and exact["z"] == Fraction(43, 96)


def test_x_and_not_x():
    c = Circuit(["a"], [("n", "NOT", ["a"]), ("y", "AND", ["a", "n"])])
    p = {"a": HALF}
    assert exact_probabilities(c, p)["y"] == 0
    assert propagate(c, p)["y"] == Fraction(1, 4)


def test_propagation_exact_without_reconvergence():
    rng = random.Random(2)
    count = 0
    for _ in range(300):
        c = random_circuit(rng, rng.randint(1, 7), rng.randint(1, 8), fanout_free=rng.random() < 0.5)
        if c.has_reconvergence():
            continue
        count += 1
        p = random_probs(rng, c)
        assert propagate(c, p) == brute_force(c, p)
    assert count > 100


def test_fanout_free_circuits_have_no_reconvergence():
    rng = random.Random(3)
    for _ in range(200):
        c = random_circuit(rng, rng.randint(1, 7), rng.randint(1, 8), fanout_free=True)
        assert c.is_fanout_free() and not c.has_reconvergence()
        p = random_probs(rng, c)
        assert propagate(c, p) == brute_force(c, p)


def test_polynomials_exact_on_every_circuit():
    rng = random.Random(4)
    for _ in range(200):
        c = random_circuit(rng, rng.randint(1, 6), rng.randint(1, 9))
        p = random_probs(rng, c)
        assert exact_probabilities(c, p) == brute_force(c, p)


def test_polynomials_are_multilinear_and_match_on_vertices():
    rng = random.Random(5)
    for _ in range(50):
        c = random_circuit(rng, rng.randint(1, 5), rng.randint(1, 7))
        polys = probability_polynomials(c)
        for x in itertools.product((0, 1), repeat=len(c.inputs)):
            vertex = {name: Fraction(b) for name, b in zip(c.inputs, x)}
            val = c.evaluate(x)
            for v in c.nodes:
                assert polys[v].evaluate(vertex) == val[v]


def test_independence_is_wrong_under_reconvergence():
    rng = random.Random(6)
    wrong = 0
    for _ in range(300):
        c = random_circuit(rng, rng.randint(2, 6), rng.randint(3, 9))
        if not c.has_reconvergence():
            continue
        p = {x: HALF for x in c.inputs}
        if propagate(c, p) != brute_force(c, p):
            wrong += 1
    assert wrong > 50


def test_model_counting_reduction():
    # (a or not b) and (b or c) and (not a or not c): P(F = 1) with p = 1/2 is #F / 2^n.
    c = Circuit(
        ["a", "b", "c"],
        [
            ("nb", "NOT", ["b"]),
            ("na", "NOT", ["a"]),
            ("nc", "NOT", ["c"]),
            ("c1", "OR", ["a", "nb"]),
            ("c2", "OR", ["b", "c"]),
            ("c3", "OR", ["na", "nc"]),
            ("F", "AND", ["c1", "c2", "c3"]),
        ],
    )
    models = sum(c.evaluate(x)["F"] for x in itertools.product((0, 1), repeat=3))
    pr = exact_probabilities(c, {x: HALF for x in c.inputs})["F"]
    assert pr * 8 == models == 2
