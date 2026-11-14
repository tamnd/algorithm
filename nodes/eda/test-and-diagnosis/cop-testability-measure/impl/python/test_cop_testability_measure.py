# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cop-testability-measure/. The authors are listed in prov/ZPFC9R.jsonl.
"""COP against exact enumeration of all input vectors, in Fractions."""

from __future__ import annotations

import random
from fractions import Fraction

import pytest

from cop_testability_measure import controllability, cop, detection_probability, observability
from td2net import Circuit

HALF = Fraction(1, 2)


def exact(c: Circuit, p=None):
    """Exact C, O and detection probabilities by weighted enumeration of all vectors."""
    if p is None:
        p = [HALF] * len(c.pi)
    cc = [Fraction(0)] * c.n_lines
    obs = [Fraction(0)] * c.n_lines
    det = {f: Fraction(0) for f in c.faults()}
    for vec in c.all_vectors():
        w = Fraction(1)
        for bit, q in zip(vec, p):
            w *= q if bit else 1 - q
        vals = c.simulate(vec)
        for k in range(c.n_lines):
            if vals[k] == 1:
                cc[k] += w
            if c.detects(vec, (k, 1 - vals[k])):
                obs[k] += w
                det[(k, 1 - vals[k])] += w
    return cc, obs, det


def tree_example() -> Circuit:
    return Circuit(
        ["a", "b", "c", "d"],
        [("g", "AND", ["a", "b"]), ("h", "OR", ["c", "d"]), ("z", "NAND", ["g", "h"])],
        ["z"],
    )


def reconvergent() -> Circuit:
    return Circuit(
        ["a", "b", "c"],
        [("x", "AND", ["a", "b"]), ("y", "AND", ["a", "c"]), ("z", "AND", ["x", "y"])],
        ["z"],
    )


def consensus() -> Circuit:
    return Circuit(
        ["a", "b", "c"],
        [
            ("na", "NOT", ["a"]),
            ("p", "AND", ["a", "b"]),
            ("q", "AND", ["na", "c"]),
            ("r", "AND", ["b", "c"]),
            ("z", "OR", ["p", "q", "r"]),
        ],
        ["z"],
    )


def random_forest(rng: random.Random, n_inputs: int, n_gates: int) -> Circuit:
    """A fanout-free circuit: every net feeds at most one sink."""
    inputs = [f"i{k}" for k in range(n_inputs)]
    free = list(inputs)
    gates = []
    ops = ("AND", "OR", "NAND", "NOR", "XOR", "XNOR", "NOT", "BUF")
    for k in range(n_gates):
        if len(free) < 2:
            break
        op = rng.choice(ops)
        arity = 1 if op in ("NOT", "BUF") else rng.randint(2, min(3, len(free)))
        fanin = rng.sample(free, arity)
        for f in fanin:
            free.remove(f)
        name = f"g{k}"
        gates.append((name, op, fanin))
        free.append(name)
    return Circuit(inputs, gates, free)


def random_probabilities(rng: random.Random, n: int) -> list[Fraction]:
    return [Fraction(rng.randint(0, 8), 8) for _ in range(n)]


def test_tree_example_numbers():
    c = tree_example()
    cc, obs = cop(c)
    name = {c.name[k]: k for k in range(c.n_lines)}
    assert cc[name["g"]] == Fraction(1, 4)
    assert cc[name["h"]] == Fraction(3, 4)
    assert cc[name["z"]] == Fraction(13, 16)
    assert obs[name["g"]] == Fraction(3, 4)
    assert obs[name["h"]] == Fraction(1, 4)
    assert obs[name["a"]] == Fraction(3, 8)
    assert obs[name["c"]] == Fraction(1, 8)
    assert detection_probability(cc, obs, (name["a"], 0)) == Fraction(3, 16)
    ec, eo, ed = exact(c)
    assert cc == ec and obs == eo
    assert all(detection_probability(cc, obs, f) == ed[f] for f in c.faults())


@pytest.mark.parametrize("seed", range(80))
def test_exact_on_fanout_free_circuits(seed):
    rng = random.Random(seed)
    c = random_forest(rng, rng.randint(1, 6), rng.randint(1, 7))
    p = random_probabilities(rng, len(c.pi))
    cc, obs = cop(c, p)
    ec, eo, ed = exact(c, p)
    assert cc == ec
    assert obs == eo
    for f in c.faults():
        assert detection_probability(cc, obs, f) == ed[f]


def test_reconvergence_counterexample():
    c = reconvergent()
    cc, obs = cop(c)
    ec, eo, ed = exact(c)
    a, z, ax = c.line("a"), c.line("z"), c.line("a>x")
    assert cc[z] == Fraction(1, 16) and ec[z] == Fraction(1, 8)
    assert obs[a] == Fraction(15, 64) and eo[a] == Fraction(1, 4)
    assert detection_probability(cc, obs, (a, 0)) == Fraction(15, 128)
    assert ed[(a, 0)] == Fraction(1, 8)
    # a>x stuck at 1 is redundant, yet COP gives it a positive detection probability.
    assert ed[(ax, 1)] == 0
    assert detection_probability(cc, obs, (ax, 1)) == Fraction(1, 16)


def test_consensus_redundant_fault():
    c = consensus()
    cc, obs = cop(c)
    _, _, ed = exact(c)
    r = c.line("r")
    assert ed[(r, 0)] == 0
    assert detection_probability(cc, obs, (r, 0)) == Fraction(9, 64)
    z = c.line("z")
    assert cc[z] == Fraction(37, 64)


def test_neither_bound():
    """The stem rule can be too high (here) and too low (the reconvergent example)."""
    c = Circuit(["a"], [("z", "XOR", ["a", "a"])], ["z"])
    cc, obs = cop(c)
    ec, eo, _ = exact(c)
    a, z = c.line("a"), c.line("z")
    assert cc[z] == HALF and ec[z] == 0
    assert obs[a] == 1 and eo[a] == 0


def no_reconvergence_into(c: Circuit, k: int) -> bool:
    """True if no line reaches k along two different paths."""
    paths = [0] * c.n_lines
    paths[k] = 1
    for u in range(k - 1, -1, -1):
        paths[u] = sum(paths[w] for w in c.fanout[u])
        if paths[u] > 1:
            return False
    return True


@pytest.mark.parametrize("seed", range(60))
def test_controllability_exact_without_reconvergence(seed):
    """On any circuit, C[k] is exact when no line reaches k by two paths."""
    from td2net import random_circuit

    rng = random.Random(1000 + seed)
    c = random_circuit(rng, rng.randint(2, 5), rng.randint(2, 8))
    p = random_probabilities(rng, len(c.pi))
    cc = controllability(c, p)
    ec, _, _ = exact(c, p)
    for k in range(c.n_lines):
        assert 0 <= cc[k] <= 1
        if no_reconvergence_into(c, k):
            assert cc[k] == ec[k]


@pytest.mark.parametrize("seed", range(40))
def test_values_are_probabilities(seed):
    from td2net import random_circuit

    rng = random.Random(5000 + seed)
    c = random_circuit(rng, rng.randint(2, 6), rng.randint(2, 10), ops=("AND", "OR", "NAND", "NOR", "NOT", "XOR"))
    cc = controllability(c)
    obs = observability(c, cc)
    for k in range(c.n_lines):
        assert 0 <= cc[k] <= 1 and 0 <= obs[k] <= 1
    for o in c.po:
        assert obs[o] == 1


def test_errors_appear_on_random_reconvergent_circuits():
    """Reconvergence makes COP differ from the exact values on some circuits."""
    from td2net import random_circuit

    rng = random.Random(7)
    wrong = 0
    for _ in range(40):
        c = random_circuit(rng, 4, 7)
        cc, obs = cop(c)
        ec, eo, _ = exact(c)
        if cc != ec or obs != eo:
            wrong += 1
    assert wrong > 0
