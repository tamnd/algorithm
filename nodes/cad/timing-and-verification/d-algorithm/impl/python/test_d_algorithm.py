# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/d-algorithm/. The authors are listed in prov/C6DBQN.jsonl.

import random

import pytest

from d_algorithm import d_algorithm
from gatenet import X, Circuit, completions, random_circuit

# The circuit of the page: z = NAND(NAND(a, b), NAND(b, c)) = ab + bc.
C3 = Circuit(["a", "b", "c"], [("g", "NAND", ["a", "b"]), ("h", "NAND", ["b", "c"]), ("z", "NAND", ["g", "h"])], ["z"])

C17 = Circuit(
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

# z = ab + a'c + bc. The term bc is the consensus of the other two, so its AND gate is redundant.
CONSENSUS = Circuit(
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


def check_against_brute_force(c, fault):
    stats = {}
    t = d_algorithm(c, fault, stats=stats)
    if t is None:
        assert not c.detectable(fault)
    else:
        assert len(t) == len(c.pi)
        assert all(c.detects(v, fault) for v in completions(t))


def test_page_example_h_stuck_at_0():
    fault = (C3.line("h"), 0)
    t = d_algorithm(C3, fault)
    assert t is not None
    assert set(completions(t)) <= set(C3.detecting_vectors(fault))


def test_page_example_traces():
    stats = {}
    assert d_algorithm(C3, (C3.line("h"), 0), stats=stats) == (X, 0, X)
    assert stats == {"calls": 3, "backtracks": 0}
    stats = {}
    assert d_algorithm(CONSENSUS, (CONSENSUS.line("r"), 0), stats=stats) is None
    assert stats == {"calls": 2, "backtracks": 1}


def test_c3_all_faults():
    for fault in C3.faults():
        check_against_brute_force(C3, fault)


def test_c17_all_faults():
    for fault in C17.faults():
        assert d_algorithm(C17, fault) is not None
        check_against_brute_force(C17, fault)


def test_redundant_fault_has_no_test():
    fault = (CONSENSUS.line("r"), 0)
    assert not CONSENSUS.detectable(fault)
    assert d_algorithm(CONSENSUS, fault) is None
    for f in CONSENSUS.faults():
        check_against_brute_force(CONSENSUS, f)


def test_xor_is_rejected():
    c = Circuit(["a", "b"], [("z", "XOR", ["a", "b"])], ["z"])
    with pytest.raises(ValueError):
        d_algorithm(c, (c.line("z"), 0))


@pytest.mark.parametrize("seed", range(60))
def test_random_circuits_against_brute_force(seed):
    rng = random.Random(seed)
    c = random_circuit(rng, rng.randint(2, 7), rng.randint(2, 10), ops=("AND", "OR", "NAND", "NOR", "NOT", "BUF"))
    for fault in c.faults():
        check_against_brute_force(c, fault)
