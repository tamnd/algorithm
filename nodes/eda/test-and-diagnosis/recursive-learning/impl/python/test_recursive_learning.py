# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/recursive-learning/. The authors are listed in prov/HZB5S0.jsonl.
"""Recursive learning against the necessary assignments found by enumeration."""

from __future__ import annotations

import random

import pytest

from recursive_learning import consistent_vectors, direct_implications, from_assignment, learn, necessary_assignments
from td2net import Circuit, random_circuit


def necessary_by_enumeration(c: Circuit, assignment):
    """The values shared by every input vector that agrees with the situation, or None."""
    vecs = consistent_vectors(c, assignment)
    if not vecs:
        return None
    sims = [c.simulate(v) for v in vecs]
    return {k: sims[0][k] for k in range(c.n_lines) if all(s[k] == sims[0][k] for s in sims)}


def two_ors() -> Circuit:
    """p and q are both b + c, r = a p and z = q + r."""
    return Circuit(
        ["a", "b", "c"],
        [("p", "OR", ["b", "c"]), ("q", "OR", ["b", "c"]), ("r", "AND", ["a", "p"]), ("z", "OR", ["q", "r"])],
        ["z"],
    )


def named(c, values):
    return {c.name[k]: v for k, v in values.items() if c.kind[k] != "branch"}


def test_depth_one_misses_depth_two_finds():
    c = two_ors()
    s = {c.line("z"): 1}
    assert named(c, learn(c, s, 0)) == {"z": 1}
    assert named(c, learn(c, s, 1)) == {"z": 1}
    assert named(c, learn(c, s, 2)) == {"z": 1, "p": 1, "q": 1}
    assert named(c, necessary_by_enumeration(c, s)) == {"z": 1, "p": 1, "q": 1}


def test_depth_two_with_a():
    c = two_ors()
    s = {c.line("z"): 1, c.line("a"): 1}
    assert named(c, learn(c, s, 1)) == {"a": 1, "z": 1}
    assert named(c, learn(c, s, 2)) == {"a": 1, "z": 1, "p": 1, "q": 1, "r": 1}


def test_direct_implications_example():
    c = Circuit(["a", "b"], [("g", "AND", ["a", "b"]), ("h", "NOT", ["g"])], ["h"])
    vals = direct_implications(c, from_assignment(c, {c.line("h"): 0}))
    assert vals[c.line("a")] == 1 and vals[c.line("b")] == 1
    assert direct_implications(c, from_assignment(c, {c.line("h"): 0, c.line("a"): 0})) is None


def test_single_call_misses_a_constant_line():
    """With nothing assigned, no gate is unjustified, so nothing is learned."""
    c = Circuit(["b"], [("nb", "NOT", ["b"]), ("y", "AND", ["b", "nb"])], ["y"])
    assert learn(c, {}, 5) == {}
    assert necessary_assignments(c, {})[c.line("y")] == 0
    assert necessary_by_enumeration(c, {})[c.line("y")] == 0


def random_situation(rng, c, size):
    return {rng.randrange(c.n_lines): rng.randint(0, 1) for _ in range(size)}


@pytest.mark.parametrize("seed", range(150))
def test_sound_at_every_depth(seed):
    rng = random.Random(seed)
    c = random_circuit(rng, rng.randint(2, 4), rng.randint(2, 6), ops=("AND", "OR", "NAND", "NOR", "NOT", "XOR"))
    s = random_situation(rng, c, rng.randint(1, 3))
    truth = necessary_by_enumeration(c, s)
    for depth in range(4):
        got = learn(c, s, depth)
        if got is None:
            assert truth is None
        elif truth is not None:
            assert all(truth.get(k) == v for k, v in got.items())


@pytest.mark.parametrize("seed", range(150))
def test_enough_depth_finds_conflicts_and_all_necessary_assignments(seed):
    rng = random.Random(10_000 + seed)
    c = random_circuit(rng, rng.randint(2, 4), rng.randint(2, 6), ops=("AND", "OR", "NAND", "NOR", "NOT", "XOR"))
    s = random_situation(rng, c, rng.randint(1, 3))
    truth = necessary_by_enumeration(c, s)
    assert (learn(c, s, c.n_lines) is None) == (truth is None)
    assert necessary_assignments(c, s) == truth
