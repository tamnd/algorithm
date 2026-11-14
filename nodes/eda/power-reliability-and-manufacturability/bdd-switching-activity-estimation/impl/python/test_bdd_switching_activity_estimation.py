# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bdd-switching-activity-estimation/. The authors are listed in prov/D7CR16.jsonl.

import itertools
import random
from fractions import Fraction

from bdd import BDD
from bdd_switching_activity_estimation import (
    gate_bdd,
    independent_pairs,
    switching_activity,
    transport_activity,
)
from netlist import KINDS, Circuit, gate_value, random_circuit, transitions

HALF = Fraction(1, 2)

# y = ab + ac, the reconvergent example of the page.
RECONV = Circuit(["a", "b", "c"], [("u", "AND", ["a", "b"]), ("v", "AND", ["a", "c"]), ("y", "OR", ["u", "v"])])


def brute_force(c, J, delay_model):
    """Expected transitions of every node per cycle, by enumeration of all 4^n vector pairs, in Fraction."""
    n = len(c.inputs)
    out = {v: Fraction(0) for v in c.nodes}
    for x in itertools.product((0, 1), repeat=n):
        for y in itertools.product((0, 1), repeat=n):
            w = Fraction(1)
            for i in range(n):
                w *= J[i][(x[i], y[i])]
            if w == 0:
                continue
            for v, k in transitions(c, x, y, delay_model).items():
                if k:
                    out[v] += w * k
    return out


def random_joint(rng):
    """A random law of (x_i, x'_i), sometimes with equal marginals and sometimes not."""
    ws = [rng.randint(0, 4) for _ in range(4)]
    if sum(ws) == 0:
        ws[0] = 1
    s = sum(ws)
    return {(a, b): Fraction(ws[2 * a + b], s) for a in (0, 1) for b in (0, 1)}


def test_bdd_package_against_truth_tables():
    for kind in KINDS:
        for k in ([1] if kind in ("BUF", "NOT") else [2, 3]):
            m = BDD()
            u = gate_bdd(m, kind, [m.var(j) for j in range(k)])
            for bits in itertools.product((0, 1), repeat=k):
                assert m.evaluate(u, dict(enumerate(bits))) == gate_value(kind, bits)
    # Canonicity: the same function built two ways gives the same node.
    m = BDD()
    a, b, c = m.var(0), m.var(1), m.var(2)
    f = m.AND(a, m.OR(b, c))
    g = m.OR(m.AND(a, b), m.AND(a, c))
    assert f == g and m.size(f) == 5


def test_page_example_temporally_independent():
    J = independent_pairs({"a": HALF, "b": HALF, "c": HALF}, ["a", "b", "c"])
    alpha = switching_activity(RECONV, J)
    assert alpha["y"] == 2 * Fraction(3, 8) * Fraction(5, 8) == Fraction(15, 32)
    assert alpha["u"] == alpha["v"] == Fraction(3, 8)
    assert alpha == brute_force(RECONV, J, "zero")


def test_page_example_with_temporal_correlation():
    # Each input keeps its value with probability 3/4 and has P = 1/2.
    keep = {(0, 0): Fraction(3, 8), (1, 1): Fraction(3, 8), (0, 1): Fraction(1, 8), (1, 0): Fraction(1, 8)}
    J = [keep] * 3
    alpha = switching_activity(RECONV, J)
    assert alpha["y"] == Fraction(69, 256)
    assert alpha == brute_force(RECONV, J, "zero")
    tr = transport_activity(RECONV, J)
    assert tr == brute_force(RECONV, J, "transport")


def test_zero_delay_equals_enumeration_on_random_circuits():
    rng = random.Random(2)
    for _ in range(60):
        c = random_circuit(rng, rng.randint(1, 5), rng.randint(1, 10))
        J = [random_joint(rng) for _ in c.inputs]
        assert switching_activity(c, J) == brute_force(c, J, "zero")


def test_transport_delay_equals_enumeration_on_random_circuits():
    rng = random.Random(3)
    for _ in range(40):
        c = random_circuit(rng, rng.randint(1, 4), rng.randint(1, 8), max_delay=3)
        J = [random_joint(rng) for _ in c.inputs]
        assert transport_activity(c, J) == brute_force(c, J, "transport")


def test_page_example_with_skew():
    skew = Circuit(RECONV.inputs, RECONV.gates, {"v": 2})
    J = independent_pairs({"a": HALF, "b": HALF, "c": HALF}, ["a", "b", "c"])
    assert transport_activity(RECONV, J)["y"] == Fraction(15, 32)
    assert transport_activity(skew, J)["y"] == HALF
    assert transport_activity(skew, J) == brute_force(skew, J, "transport")


def test_transport_counts_glitches():
    c = Circuit(["a"], [("n", "NOT", ["a"]), ("y", "AND", ["a", "n"])])
    J = independent_pairs({"a": HALF}, ["a"])
    assert switching_activity(c, J)["y"] == 0
    assert transport_activity(c, J)["y"] == HALF


def test_independent_vectors_give_2p_1_minus_p():
    rng = random.Random(4)
    for _ in range(30):
        c = random_circuit(rng, rng.randint(1, 5), rng.randint(1, 8))
        p = {x: Fraction(rng.randint(0, 4), 4) for x in c.inputs}
        J = independent_pairs(p, c.inputs)
        alpha = switching_activity(c, J)
        prob = {v: Fraction(0) for v in c.nodes}
        for x in itertools.product((0, 1), repeat=len(c.inputs)):
            w = Fraction(1)
            for name, b in zip(c.inputs, x):
                w *= p[name] if b else 1 - p[name]
            val = c.evaluate(x)
            for v in c.nodes:
                prob[v] += w * val[v]
        for v in c.nodes:
            assert alpha[v] == 2 * prob[v] * (1 - prob[v])
