# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fan-algorithm/. The authors are listed in prov/DJVVW8.jsonl.

import random

import pytest

from fan_algorithm import (
    bound_and_head_lines,
    d_frontier,
    dominators,
    fan,
    imply,
    postdominator_tree,
    unique_sensitization,
    x_paths,
)
from podem_baseline import podem
from td2net import X, Circuit, completions, random_circuit

# Unique sensitization and multiple backtrace: the fault x/0 must pass g, u and z.
C1 = Circuit(
    ["x", "e", "k", "f", "h"],
    [
        ("s", "OR", ["e", "k"]),
        ("g", "AND", ["x", "s"]),
        ("w1", "NOR", ["e", "f"]),
        ("u", "AND", ["g", "w1"]),
        ("w2", "NOR", ["e", "h"]),
        ("z", "AND", ["u", "w2"]),
    ],
    ["z"],
)

# Head lines: the consensus circuit z = ab + a'c + bc with b and c widened into fanout-free cones.
C2 = Circuit(
    ["a", "b1", "b2", "c1", "c2"],
    [
        ("b", "AND", ["b1", "b2"]),
        ("c", "OR", ["c1", "c2"]),
        ("na", "NOT", ["a"]),
        ("p", "AND", ["a", "b"]),
        ("q", "AND", ["na", "c"]),
        ("r", "AND", ["b", "c"]),
        ("z", "OR", ["p", "q", "r"]),
    ],
    ["z"],
)


def run(c, fault):
    sf, sp = {}, {}
    t = fan(c, fault, sf)
    tp = podem(c, fault, sp)
    return t, sf, tp, sp


def test_page_example_unique_sensitization():
    t, sf, tp, sp = run(C1, (C1.line("x"), 0))
    assert t == (1, 0, 1, 0, 0) and sf == {"steps": 6, "backtracks": 0}
    assert tp == (1, 0, 1, 0, 0) and sp == {"steps": 7, "backtracks": 1}


def test_page_example_head_lines():
    fault = (C2.line("r"), 0)
    _, heads = bound_and_head_lines(C2, fault)
    assert [C2.name[h] for h in heads] == ["a", "b", "c"]
    t, sf, tp, sp = run(C2, fault)
    assert t is None and tp is None and not C2.detectable(fault)
    assert sf == {"steps": 7, "backtracks": 3}
    assert sp == {"steps": 13, "backtracks": 6}


def test_page_example_totals():
    for c, totals in ((C1, (13, 9)), (C2, (24, 13))):
        tp = tf = 0
        for fault in c.faults():
            _, sf, _, sp = run(c, fault)
            tp += sp["backtracks"]
            tf += sf["backtracks"]
        assert (tp, tf) == totals


def test_head_lines_cut_the_bound_lines():
    rng = random.Random(7)
    for _ in range(60):
        c = random_circuit(rng, rng.randint(2, 6), rng.randint(2, 9))
        fault = rng.choice(c.faults())
        bound, heads = bound_and_head_lines(c, fault)
        assert len(heads) <= len(c.pi)
        for v in c.all_vectors()[:16]:
            good = c.simulate(v)
            bad = c.simulate(v, fault)
            g2, b2 = imply(c, fault, {h: good[h] for h in heads})
            for k in range(c.n_lines):
                if bound[k]:
                    assert (g2[k], b2[k]) == (good[k], bad[k])


def brute_dominators(c, g):
    """Lines d such that no path from g to an output avoids d, by one search per d."""
    po = set(c.po)

    def reaches(avoid):
        if g == avoid:
            return False
        seen, stack = {g}, [g]
        while stack:
            u = stack.pop()
            if u in po:
                return True
            for w in c.fanout[u]:
                if w != avoid and w not in seen:
                    seen.add(w)
                    stack.append(w)
        return False

    if not reaches(-1):
        return []
    return [d for d in sorted(c.cone(g)) if not reaches(d)]


def test_dominators_against_path_search():
    rng = random.Random(5)
    for _ in range(80):
        c = random_circuit(rng, rng.randint(2, 6), rng.randint(2, 12))
        ipdom = postdominator_tree(c)
        for g in range(c.n_lines):
            assert sorted(dominators(ipdom, g)) == brute_dominators(c, g)
    ipdom = postdominator_tree(C1)
    assert [C1.name[d] for d in dominators(ipdom, C1.line("g"))] == ["g", "u", "z"]


def test_unique_sensitization_values_are_necessary():
    rng = random.Random(11)
    checked = 0
    for _ in range(150):
        c = random_circuit(rng, rng.randint(3, 6), rng.randint(3, 9))
        fault = rng.choice(c.faults())
        _, heads = bound_and_head_lines(c, fault)
        tests = c.detecting_vectors(fault)
        for v in tests[:4]:
            good = c.simulate(v)
            part = {h: good[h] for h in heads if rng.random() < 0.5}
            g, b = imply(c, fault, part)
            if any(X not in (g[o], b[o]) and g[o] != b[o] for o in c.po):
                continue  # FAN returns at line L5 before it looks at R
            xp = x_paths(c, g, b)
            front = [k for k in d_frontier(c, g, b) if xp[k]]
            req = unique_sensitization(c, fault, g, front, c.cone(fault[0]), postdominator_tree(c))
            for k, val in req:
                checked += 1
                assert good[k] == val
    assert checked > 50


def check(c, fault):
    sf, sp = {}, {}
    t = fan(c, fault, sf)
    tp = podem(c, fault, sp)
    det = c.detectable(fault)
    assert (t is not None) == det
    assert (tp is not None) == det
    _, heads = bound_and_head_lines(c, fault)
    assert sf["steps"] <= 2 ** (len(heads) + 1)
    assert sp["steps"] <= 2 ** (len(c.pi) + 1)
    if t is not None:
        assert len(t) == len(c.pi)
        assert all(c.detects(v, fault) for v in completions(t))
    return sf["backtracks"], sp["backtracks"]


@pytest.mark.parametrize("seed", range(60))
def test_random_circuits_against_exhaustive_search(seed):
    rng = random.Random(seed)
    ops = ("AND", "OR", "NAND", "NOR", "NOT", "XOR", "XNOR", "BUF") if seed % 2 else ("AND", "OR", "NAND", "NOR", "NOT")
    c = random_circuit(rng, rng.randint(2, 7), rng.randint(2, 10), ops=ops)
    for fault in c.faults():
        check(c, fault)


def test_c17_all_faults():
    c = Circuit(
        ["1", "2", "3", "6", "7"],
        [
            ("10", "NAND", ["1", "3"]),
            ("11", "NAND", ["3", "6"]),
            ("16", "NAND", ["2", "11"]),
            ("19", "NAND", ["11", "7"]),
            ("22", "NAND", ["10", "16"]),
            ("23", "NAND", ["16", "19"]),
        ],
        ["22", "23"],
    )
    for fault in c.faults():
        assert fan(c, fault) is not None
        check(c, fault)
    assert X == 2
