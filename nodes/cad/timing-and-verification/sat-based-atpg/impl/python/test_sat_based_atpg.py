# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sat-based-atpg/. The authors are listed in prov/PFQN6B.jsonl.

import random
from itertools import product

import pytest

from gatenet import Circuit, random_circuit
from sat_based_atpg import Solver, encode, sat_based_atpg

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


def brute_sat(n, clauses):
    for bits in product((0, 1), repeat=n):
        if all(any((bits[abs(a) - 1] == 1) == (a > 0) for a in cl) for cl in clauses):
            return True
    return False


def check_against_brute_force(c, fault, active):
    t = sat_based_atpg(c, fault, active=active)
    if t is None:
        assert not c.detectable(fault)
    else:
        assert c.detects(t, fault)


def test_page_example_h_stuck_at_0():
    fault = (C3.line("h"), 0)
    stats = {}
    t = sat_based_atpg(C3, fault, stats=stats)
    assert t in C3.detecting_vectors(fault)
    n, clauses, _ = encode(C3, fault)
    assert (stats["variables"], stats["clauses"]) == (n, len(clauses)) == (11, 23)
    assert t == (0, 0, 0)
    assert [-9] in clauses and [7] in clauses and [11] in clauses
    n1, clauses1, _ = encode(C3, fault, active=True)
    assert (n1, len(clauses1)) == (13, 29)


@pytest.mark.parametrize("seed", range(30))
def test_inputs_first_bounds_the_search(seed):
    # Without active clauses, the inputs imply every other variable, so the decisions are on inputs only.
    rng = random.Random(100 + seed)
    c = random_circuit(rng, rng.randint(2, 7), rng.randint(2, 12), ops=("AND", "OR", "NAND", "NOR", "NOT", "XOR"))
    for fault in c.faults():
        stats = {}
        sat_based_atpg(c, fault, stats=stats)
        assert stats["decisions"] <= 2 ** len(c.pi) - 1


@pytest.mark.parametrize("active", [False, True])
def test_c3_and_c17_all_faults(active):
    for c in (C3, C17):
        for fault in c.faults():
            check_against_brute_force(c, fault, active)
    for fault in C17.faults():
        assert sat_based_atpg(C17, fault, active=active) is not None


@pytest.mark.parametrize("active", [False, True])
def test_redundant_fault_is_unsatisfiable(active):
    fault = (CONSENSUS.line("r"), 0)
    assert not CONSENSUS.detectable(fault)
    assert sat_based_atpg(CONSENSUS, fault, active=active) is None


def test_active_clauses_keep_satisfiability():
    rng = random.Random(7)
    for _ in range(60):
        c = random_circuit(rng, rng.randint(2, 4), rng.randint(2, 6))
        for fault in c.faults():
            n0, cl0, _ = encode(c, fault)
            n1, cl1, _ = encode(c, fault, active=True)
            det = c.detectable(fault)
            assert (Solver(n0, cl0).solve() is not None) == (Solver(n1, cl1).solve() is not None) == det
            if n1 <= 12:
                assert brute_sat(n0, cl0) == brute_sat(n1, cl1) == det


@pytest.mark.parametrize("seed", range(40))
def test_solver_against_brute_force(seed):
    rng = random.Random(seed)
    n = rng.randint(1, 10)
    clauses = [[rng.choice((1, -1)) * rng.randint(1, n) for _ in range(rng.randint(1, 3))] for _ in range(rng.randint(1, 5 * n))]
    model = Solver(n, clauses).solve()
    assert (model is not None) == brute_sat(n, clauses)
    if model is not None:
        assert all(any((model[abs(a)] == 1) == (a > 0) for a in cl) for cl in clauses)


@pytest.mark.parametrize("seed", range(40))
def test_random_circuits_against_brute_force(seed):
    rng = random.Random(seed)
    ops = ("AND", "OR", "NAND", "NOR", "NOT", "XOR", "XNOR", "BUF") if seed % 2 else ("AND", "OR", "NAND", "NOR", "NOT")
    c = random_circuit(rng, rng.randint(2, 8), rng.randint(2, 10), ops=ops)
    for fault in c.faults():
        check_against_brute_force(c, fault, active=bool(seed % 3 == 0))
