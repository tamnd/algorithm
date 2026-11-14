# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/concurrent-fault-simulation/. The authors are listed in prov/NCVK7P.jsonl.

import random

import pytest

from concurrent_fault_simulation import concurrent_fault_simulation
from gatenet import Circuit, random_circuit

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


def serial(c, vectors, faults=None, drop=True):
    """Reference method: simulate the good circuit and each faulty circuit on its own."""
    alive = list(c.faults() if faults is None else faults)
    result = []
    for vector in vectors:
        good = c.outputs(vector)
        detected = {f for f in alive if c.outputs(vector, f) != good}
        result.append(detected)
        if drop:
            alive = [f for f in alive if f not in detected]
    return result


def names(c, faults):
    return sorted(c.fault_name(f) for f in faults)


def test_page_example_two_vectors():
    vectors = [(1, 1, 0), (0, 1, 1)]
    stats = {}
    got = concurrent_fault_simulation(C3, vectors, stats=stats)
    assert got == serial(C3, vectors)
    assert names(C3, got[0]) == ["a/0", "b/0", "b>g/0", "g/1", "z/0"]
    assert names(C3, got[1]) == ["b>h/0", "c/0", "h/1"]
    assert stats == {"events": 14, "gate_evals": 14, "fault_evals": 22}
    kept = concurrent_fault_simulation(C3, vectors, drop=False)
    assert names(C3, kept[1]) == ["b/0", "b>h/0", "c/0", "h/1", "z/0"]


@pytest.mark.parametrize("drop", [True, False])
def test_c17_exhaustive_vectors(drop):
    vectors = C17.all_vectors()
    rng = random.Random(1)
    rng.shuffle(vectors)
    assert concurrent_fault_simulation(C17, vectors, drop=drop) == serial(C17, vectors, drop=drop)
    total = set().union(*concurrent_fault_simulation(C17, vectors))
    assert len(total) == 34


def test_c17_counts_of_the_page():
    counts = []
    for drop in (True, False):
        stats = {}
        concurrent_fault_simulation(C17, C17.all_vectors(), drop=drop, stats=stats)
        counts.append((stats["events"], stats["fault_evals"]))
    assert counts == [(309, 130), (350, 816)]
    vectors = C17.all_vectors()
    random.Random(1).shuffle(vectors)
    stats = {}
    concurrent_fault_simulation(C17, vectors, stats=stats)
    assert (stats["events"], stats["fault_evals"]) == (384, 153)


def test_fault_subset():
    faults = [(C3.line("h"), 0), (C3.line("b"), 1)]
    vectors = C3.all_vectors()
    assert concurrent_fault_simulation(C3, vectors, faults=faults) == serial(C3, vectors, faults=faults)


def test_repeated_vector_causes_no_events():
    stats = {}
    concurrent_fault_simulation(C17, [(0, 1, 0, 1, 1)] * 3, drop=False, stats=stats)
    one = {}
    concurrent_fault_simulation(C17, [(0, 1, 0, 1, 1)], drop=False, stats=one)
    assert stats["fault_evals"] == one["fault_evals"]
    assert stats["events"] == one["events"] + 2 * len(C17.pi)


@pytest.mark.parametrize("seed", range(60))
def test_random_circuits_against_serial(seed):
    rng = random.Random(seed)
    ops = ("AND", "OR", "NAND", "NOR", "NOT", "XOR", "XNOR", "BUF")
    c = random_circuit(rng, rng.randint(2, 8), rng.randint(2, 14), ops=ops)
    vectors = [tuple(rng.randint(0, 1) for _ in c.pi) for _ in range(rng.randint(1, 12))]
    drop = seed % 2 == 0
    assert concurrent_fault_simulation(c, vectors, drop=drop) == serial(c, vectors, drop=drop)
