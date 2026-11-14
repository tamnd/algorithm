# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/critical-path-tracing/. The authors are listed in prov/KS79ZE.jsonl.

import random

from critical_path_tracing import critical_lines, critical_path_tracing, sensitive_inputs
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

# A 2-to-1 multiplexer z = ab + a'c: under 111 the branch a>p is critical, but the stem a is not.
MUX = Circuit(["a", "b", "c"], [("p", "AND", ["a", "b"]), ("na", "NOT", ["a"]), ("q", "AND", ["na", "c"]), ("z", "OR", ["p", "q"])], ["z"])

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


def flip_critical(c, vector):
    """Brute force: line k is critical when the fault k stuck at the opposite of its good value is detected."""
    good = c.simulate(vector)
    return [c.detects(vector, (k, 1 - good[k])) for k in range(c.n_lines)]


def crit_names(c, vector):
    crit = critical_lines(c, vector)
    return {c.name[k] for k in range(c.n_lines) if crit[k]}


def test_sensitive_inputs():
    assert sensitive_inputs("NAND", [1, 1]) == [0, 1]
    assert sensitive_inputs("NAND", [1, 0]) == [1]
    assert sensitive_inputs("NAND", [0, 0]) == []
    assert sensitive_inputs("NOR", [0, 1, 0]) == [1]
    assert sensitive_inputs("XOR", [1, 0, 1]) == [0, 1, 2]


def test_page_trace():
    assert crit_names(C3, (1, 0, 1)) == {"b", "b>g", "b>h", "g", "h", "z"}
    assert crit_names(C3, (0, 1, 0)) == {"a", "c", "g", "h", "z"}


def test_stem_critical_with_no_critical_branch():
    # Under 111 both branches of b are masked alone, but flipping b flips both g and h, and z.
    assert crit_names(C3, (1, 1, 1)) == {"b", "z"}
    assert flip_critical(C3, (1, 1, 1)) == critical_lines(C3, (1, 1, 1))


def test_critical_branch_with_stem_not_critical():
    assert crit_names(MUX, (1, 1, 1)) == {"a>p", "b", "p", "z"}
    assert flip_critical(MUX, (1, 1, 1)) == critical_lines(MUX, (1, 1, 1))


def test_critical_lines_against_brute_force():
    rng = random.Random(9)
    circuits = [C3, C17, CONSENSUS, MUX] + [random_circuit(rng, 4, 10, ops=OPS) for _ in range(25)]
    for c in circuits:
        for vector in c.all_vectors():
            assert critical_lines(c, vector) == flip_critical(c, vector)


def test_page_example():
    assert names(C3, critical_path_tracing(C3, SEQ)) == FIRSTS
    assert names(C3, critical_path_tracing(C3, SEQ, drop=False)) == ALL_DETECTED
    stats = {}
    critical_path_tracing(C3, SEQ, stats=stats)
    assert stats == {"stem_gate_evals": 19, "stem_checks": 4}


def test_c17_all_vectors():
    vectors = C17.all_vectors()
    result = critical_path_tracing(C17, vectors, drop=False)
    assert result == serial(C17, vectors, drop=False)
    assert [len(s) for s in result] == C17_COUNTS
    rng = random.Random(17)
    rng.shuffle(vectors)
    assert critical_path_tracing(C17, vectors) == serial(C17, vectors)


def test_redundant_faults_by_exhaustive_patterns():
    detected = set().union(*critical_path_tracing(CONSENSUS, CONSENSUS.all_vectors()))
    undetected = {CONSENSUS.fault_name(f) for f in CONSENSUS.faults() if f not in detected}
    assert undetected == REDUNDANT


def test_random_circuits_against_serial():
    rng = random.Random(2024)
    for _ in range(120):
        c = random_circuit(rng, rng.randint(2, 6), rng.randint(3, 14), ops=OPS)
        vectors = [tuple(rng.randint(0, 1) for _ in c.pi) for _ in range(rng.randint(1, 10))]
        for drop in (True, False):
            assert critical_path_tracing(c, vectors, drop=drop) == serial(c, vectors, drop=drop)
