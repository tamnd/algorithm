# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deductive-fault-simulation/. The authors are listed in prov/WGDS9V.jsonl.

import random
from itertools import product

from deductive_fault_simulation import deductive_fault_simulation, gate_list
from gatenet import Circuit, random_circuit

# The circuits below are the same in the tests of the four td1 fault simulators
# (parallel, PPSFP, deductive, critical path tracing), with the same expected sets,
# so the four methods are checked to report the same detected faults.

# The circuit of the page: z = NAND(NAND(a, b), NAND(b, c)) = ab + bc, with fanout at b.
C3 = Circuit(["a", "b", "c"], [("g", "NAND", ["a", "b"]), ("h", "NAND", ["b", "c"]), ("z", "NAND", ["g", "h"])], ["z"])
SEQ = [(1, 0, 1), (0, 1, 0), (0, 1, 1), (1, 1, 0)]
FIRSTS = [
    {"b/1", "b>g/1", "b>h/1", "g/0", "h/0", "z/1"},
    {"a/1", "c/1"},
    {"b/0", "b>h/0", "c/0", "h/1", "z/0"},
    {"a/0", "b>g/0", "g/1"},
]
ALL_DETECTED = [
    {"b/1", "b>g/1", "b>h/1", "g/0", "h/0", "z/1"},
    {"a/1", "c/1", "g/0", "h/0", "z/1"},
    {"b/0", "b>h/0", "c/0", "h/1", "z/0"},
    {"a/0", "b/0", "b>g/0", "g/1", "z/0"},
]

# ISCAS-85 c17: six NAND gates, two outputs, reconvergent fanout at 3, 11 and 16.
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
C17_COUNTS = [9, 10, 9, 12, 10, 12, 8, 13, 8, 7, 10, 9, 9, 8, 13, 14, 11, 12, 11, 13, 11, 11, 9, 13, 8, 7, 10, 9, 8, 4, 13, 14]

# z = ab + a'c + bc: the consensus term bc is redundant, so r/0 and the faults that only kill r are undetectable.
CONSENSUS = Circuit(
    ["a", "b", "c"],
    [("p", "AND", ["a", "b"]), ("na", "NOT", ["a"]), ("q", "AND", ["na", "c"]), ("r", "AND", ["b", "c"]), ("z", "OR", ["p", "q", "r"])],
    ["z"],
)
REDUNDANT = {"r/0", "b>r/0", "c>r/0"}

OPS = ("AND", "OR", "NAND", "NOR", "NOT", "BUF", "XOR", "XNOR")


def serial(c, vectors, faults=None, drop=True):
    """Reference method: inject each fault on its own and simulate every vector."""
    alive = list(c.faults() if faults is None else faults)
    result = []
    for vector in vectors:
        detected = {f for f in alive if c.detects(vector, f)}
        result.append(detected)
        if drop:
            alive = [f for f in alive if f not in detected]
    return result


def names(c, sets):
    return [{c.fault_name(f) for f in s} for s in sets]


def test_gate_rule_against_flipping_inputs():
    # Each input list is a set of abstract faults; a fault flips exactly the inputs whose list holds it.
    rng = random.Random(3)
    for op in OPS:
        for _ in range(200):
            n = 1 if op in ("NOT", "BUF") else rng.randint(2, 4)
            vals = [rng.randint(0, 1) for _ in range(n)]
            lists = [{f for f in range(6) if rng.random() < 0.4} for _ in range(n)]
            c = Circuit([f"x{i}" for i in range(n)], [("y", op, [f"x{i}" for i in range(n)])], ["y"])
            good = c.outputs(vals)[0]
            expect = set()
            for f in range(6):
                flipped = [v ^ (f in lst) for v, lst in zip(vals, lists)]
                if c.outputs(flipped)[0] != good:
                    expect.add(f)
            assert gate_list(op, vals, lists) == expect


def test_page_lists_at_111():
    lists = []
    deductive_fault_simulation(C3, [(1, 1, 1)], drop=False, lists_out=lists)
    got = {C3.name[k]: {C3.fault_name(f) for f in lists[0][k]} for k in range(C3.n_lines)}
    assert got == {
        "a": {"a/0"}, "b": {"b/0"}, "b>g": {"b/0", "b>g/0"}, "b>h": {"b/0", "b>h/0"}, "c": {"c/0"},
        "g": {"a/0", "b/0", "b>g/0", "g/1"}, "h": {"b/0", "b>h/0", "c/0", "h/1"}, "z": {"b/0", "z/0"},
    }


def test_lists_are_exact_on_every_line():
    # The list of each line is exactly the set of faults that flip that line.
    rng = random.Random(11)
    for c in [C3, C17, CONSENSUS] + [random_circuit(rng, 4, 9, ops=OPS) for _ in range(20)]:
        for vector in c.all_vectors():
            lists = []
            deductive_fault_simulation(c, [vector], drop=False, lists_out=lists)
            good = c.simulate(vector)
            for f in c.faults():
                bad = c.simulate(vector, f)
                for k in range(c.n_lines):
                    assert (f in lists[0][k]) == (bad[k] != good[k])


def test_page_example():
    assert names(C3, deductive_fault_simulation(C3, SEQ)) == FIRSTS
    assert names(C3, deductive_fault_simulation(C3, SEQ, drop=False)) == ALL_DETECTED
    stats = {}
    deductive_fault_simulation(C3, SEQ, stats=stats)
    assert stats == {"list_elements": 40}


def test_c17_all_vectors():
    vectors = C17.all_vectors()
    result = deductive_fault_simulation(C17, vectors, drop=False)
    assert result == serial(C17, vectors, drop=False)
    assert [len(s) for s in result] == C17_COUNTS
    rng = random.Random(17)
    rng.shuffle(vectors)
    assert deductive_fault_simulation(C17, vectors) == serial(C17, vectors)


def test_redundant_faults_by_exhaustive_patterns():
    detected = set().union(*deductive_fault_simulation(CONSENSUS, CONSENSUS.all_vectors()))
    undetected = {CONSENSUS.fault_name(f) for f in CONSENSUS.faults() if f not in detected}
    assert undetected == REDUNDANT


def test_random_circuits_against_serial():
    rng = random.Random(2024)
    for _ in range(120):
        c = random_circuit(rng, rng.randint(2, 6), rng.randint(3, 14), ops=OPS)
        vectors = [tuple(rng.randint(0, 1) for _ in c.pi) for _ in range(rng.randint(1, 10))]
        for drop in (True, False):
            assert deductive_fault_simulation(c, vectors, drop=drop) == serial(c, vectors, drop=drop)
        faults = c.faults()
        rng.shuffle(faults)
        faults = faults[: len(faults) // 2]
        assert deductive_fault_simulation(c, vectors, faults=faults) == serial(c, vectors, faults=faults)


def test_xor_counts_parity():
    # Two flipped inputs of an XOR cancel: a stem fault that reaches both inputs is not seen.
    c = Circuit(["a"], [("n", "BUF", ["a"]), ("z", "XOR", ["a", "n"])], ["z"])
    for vector in product((0, 1), repeat=1):
        detected = deductive_fault_simulation(c, [vector], drop=False)[0]
        assert {c.fault_name(f) for f in detected} == {c.fault_name(f) for f in c.faults() if c.detects(vector, f)}
        assert c.line("a") not in {f[0] for f in detected}
