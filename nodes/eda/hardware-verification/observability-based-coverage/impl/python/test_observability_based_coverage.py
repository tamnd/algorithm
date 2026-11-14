# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/observability-based-coverage/. The authors are listed in prov/XHG8NR.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from observability_based_coverage import (
    GATE_TYPES, Circuit, example_circuit, exact_coverage, fanin_cones,
    observable_sites, simulate, tag_coverage, tag_sets, tagged_sites)


def all_vectors(circuit):
    for bits in itertools.product((0, 1), repeat=len(circuit.inputs)):
        yield dict(zip(circuit.inputs, bits))


def random_kind(rng, k):
    if k == 1:
        return rng.choice(("NOT", "BUF"))
    return rng.choice(("AND", "OR", "NAND", "NOR", "XOR", "XNOR"))


def random_circuit(rng):
    n = rng.randint(2, 5)
    inputs = ["i%d" % i for i in range(n)]
    lines = list(inputs)
    gates = []
    for g in range(rng.randint(1, 9)):
        k = rng.choice((1, 2, 2, 2, 3))
        k = min(k, len(lines))
        ins = rng.sample(lines, k)
        kind = random_kind(rng, k)
        name = "g%d" % g
        gates.append((name, kind, ins))
        lines.append(name)
    outs = sorted(set(rng.sample(lines, rng.randint(1, 3))) | {lines[-1]})
    return Circuit(inputs, gates, outs)


def random_fanout_free_circuit(rng):
    """Every line feeds at most one gate input."""
    inputs = []
    pool = []

    def fresh_input():
        name = "i%d" % len(inputs)
        inputs.append(name)
        return name

    for _ in range(rng.randint(1, 3)):
        pool.append(fresh_input())
    gates = []
    for g in range(rng.randint(1, 8)):
        k = rng.choice((1, 2, 2, 3))
        while len(pool) < k:
            pool.append(fresh_input())
        ins = rng.sample(pool, k)
        for x in ins:
            pool.remove(x)
        name = "g%d" % g
        gates.append((name, random_kind(rng, k), ins))
        pool.append(name)
    return Circuit(inputs, gates, sorted(pool))


def test_example_of_the_page():
    c = example_circuit()
    v1 = dict(x=0, b=1, c=1, d=0)
    v2 = dict(x=1, b=0, c=1, d=1)
    _, tag = tag_sets(c, v1)
    assert tag["p"] == {"p", "x"} and tag["q"] == {"q", "x"}
    assert tag["y"] == {"y", "p", "q"} and tag["z"] == {"z"}
    assert tagged_sites(c, v1) == {"p", "q", "y", "z"}
    assert observable_sites(c, v1) == {"x", "p", "q", "y", "z"}
    assert tagged_sites(c, v2) == observable_sites(c, v2) == {"x", "c", "d", "q", "y", "z"}
    covered, ratio = tag_coverage(c, [v1, v2])
    assert ratio == Fraction(7, 8) and covered == set(c.lines()) - {"b"}
    assert exact_coverage(c, [v1, v2]) == (covered, ratio)
    assert tag_coverage(c, [v1])[1] == Fraction(4, 8)
    assert exact_coverage(c, [v1])[1] == Fraction(5, 8)


def test_converse_fails_on_reconvergence():
    c = example_circuit()
    v = dict(x=0, b=1, c=1, d=0)
    assert "x" not in tagged_sites(c, v)
    good = simulate(c, v)
    bad = simulate(c, v, flip="x")
    assert good["y"] == 0 and bad["y"] == 1


def test_cones_lemma_on_random_circuits():
    rng = random.Random(11)
    for _ in range(80):
        c = random_circuit(rng)
        fin = fanin_cones(c)
        for v in all_vectors(c):
            good = simulate(c, v)
            for t in c.lines():
                bad = simulate(c, v, flip=t)
                for line in c.lines():
                    if t not in fin[line]:
                        assert bad[line] == good[line]


def test_soundness_on_random_circuits():
    rng = random.Random(2024)
    strict = 0
    for _ in range(180):
        c = random_circuit(rng)
        fin = fanin_cones(c)
        for v in all_vectors(c):
            good, tag = tag_sets(c, v, fin)
            flipped = {t: simulate(c, v, flip=t) for t in c.lines()}
            for line in c.lines():
                for t in tag[line]:
                    assert flipped[t][line] != good[line]
            tagged = tagged_sites(c, v, fin)
            exact = observable_sites(c, v)
            assert tagged <= exact
            strict += len(exact - tagged)
    assert strict > 0  # the rule is not complete on these circuits


def test_exact_on_fanout_free_circuits():
    rng = random.Random(7)
    for _ in range(250):
        c = random_fanout_free_circuit(rng)
        fin = fanin_cones(c)
        for v in all_vectors(c):
            assert tagged_sites(c, v, fin) == observable_sites(c, v)


def test_coverage_never_exceeds_exact():
    rng = random.Random(99)
    for _ in range(100):
        c = random_circuit(rng)
        vectors = list(all_vectors(c))
        rng.shuffle(vectors)
        some = vectors[: rng.randint(1, len(vectors))]
        tc, tr = tag_coverage(c, some)
        ec, er = exact_coverage(c, some)
        assert tc <= ec and tr <= er


def test_gate_types_and_errors():
    assert set(GATE_TYPES) == {"AND", "OR", "NAND", "NOR", "XOR", "XNOR", "NOT", "BUF"}
    with pytest.raises(ValueError):
        Circuit(["a"], [("g", "AND", ["a", "h"])], ["g"])
    with pytest.raises(ValueError):
        Circuit(["a"], [("g", "NOT", ["a", "a"])], ["g"])
    with pytest.raises(ValueError):
        Circuit(["a", "b"], [("g", "MUX", ["a", "b"])], ["g"])
