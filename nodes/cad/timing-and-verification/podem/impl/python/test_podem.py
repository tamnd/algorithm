# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/podem/. The authors are listed in prov/FHMN9N.jsonl.

import random

import pytest

from gatenet import X, Circuit, completions, random_circuit
from podem import backtrace, controllability, podem

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


def check_against_brute_force(c, fault, guided):
    stats = {}
    t = podem(c, fault, guided=guided, stats=stats)
    assert stats["steps"] <= 2 ** (len(c.pi) + 1)
    if t is None:
        assert not c.detectable(fault)
    else:
        assert len(t) == len(c.pi)
        assert all(c.detects(v, fault) for v in completions(t))


def test_page_example_h_stuck_at_0():
    fault = (C3.line("h"), 0)
    t = podem(C3, fault)
    assert t is not None
    assert all(C3.detects(v, fault) for v in completions(t))
    assert set(completions(t)) <= set(C3.detecting_vectors(fault))
    assert sorted(C3.detecting_vectors(fault)) == [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 0, 1)]


def test_page_example_traces():
    stats = {}
    assert podem(C3, (C3.line("h"), 0), stats=stats) == (X, 0, X)
    assert stats == {"steps": 2, "backtracks": 0}
    stats = {}
    assert podem(CONSENSUS, (CONSENSUS.line("a"), 0), stats=stats) == (1, 1, 0)
    assert stats == {"steps": 5, "backtracks": 1}
    stats = {}
    assert podem(CONSENSUS, (CONSENSUS.line("r"), 0), stats=stats) is None
    assert stats == {"steps": 7, "backtracks": 3}


@pytest.mark.parametrize("guided", [False, True])
def test_c3_all_faults(guided):
    for fault in C3.faults():
        check_against_brute_force(C3, fault, guided)


@pytest.mark.parametrize("guided", [False, True])
def test_c17_all_faults(guided):
    assert C17.n_lines == 17
    for fault in C17.faults():
        assert podem(C17, fault, guided=guided) is not None
        check_against_brute_force(C17, fault, guided)


def test_redundant_fault_has_no_test():
    fault = (CONSENSUS.line("r"), 0)
    assert not CONSENSUS.detectable(fault)
    assert podem(CONSENSUS, fault) is None
    assert podem(CONSENSUS, fault, guided=True) is None


def test_scoap_values_of_page_example():
    cc0, cc1 = controllability(C3)
    by_name = {C3.name[k]: (cc0[k], cc1[k]) for k in range(C3.n_lines)}
    assert by_name["a"] == (1, 1)
    assert by_name["g"] == (3, 2)
    assert by_name["z"] == (5, 4)


def test_backtrace_ends_at_unassigned_input():
    good = C17.simulate([X] * 5)
    for k in range(C17.n_lines):
        for v in (0, 1):
            p, u = backtrace(C17, good, good, k, v)
            assert C17.kind[p] == "pi" and u in (0, 1)


@pytest.mark.parametrize("seed", range(40))
def test_random_circuits_against_brute_force(seed):
    rng = random.Random(seed)
    ops = ("AND", "OR", "NAND", "NOR", "NOT", "XOR", "XNOR", "BUF") if seed % 2 else ("AND", "OR", "NAND", "NOR", "NOT")
    c = random_circuit(rng, rng.randint(2, 7), rng.randint(2, 9), ops=ops)
    for fault in c.faults():
        check_against_brute_force(c, fault, guided=bool(seed % 3 == 0))
