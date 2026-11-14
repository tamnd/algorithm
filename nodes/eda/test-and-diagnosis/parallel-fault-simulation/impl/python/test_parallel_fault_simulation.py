# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-fault-simulation/. The authors are listed in prov/S63TGE.jsonl.

import random

import pytest

from gatenet import Circuit, random_circuit
from parallel_fault_simulation import eval_word, parallel_fault_simulation

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


def test_eval_word_matches_gates_bit_by_bit():
    rng = random.Random(1)
    mask = (1 << 8) - 1
    for op in OPS:
        for _ in range(50):
            n = 1 if op in ("NOT", "BUF") else rng.randint(2, 4)
            words = [rng.getrandbits(8) for _ in range(n)]
            out = eval_word(op, words, mask)
            for k in range(8):
                bits = [w >> k & 1 for w in words]
                c = Circuit([f"x{i}" for i in range(n)], [("y", op, [f"x{i}" for i in range(n)])], ["y"])
                assert out >> k & 1 == c.outputs(bits)[0]


@pytest.mark.parametrize("width", [2, 3, 8, 17, 64])
def test_page_example(width):
    assert names(C3, parallel_fault_simulation(C3, SEQ, width=width)) == FIRSTS
    assert names(C3, parallel_fault_simulation(C3, SEQ, drop=False, width=width)) == ALL_DETECTED


def test_page_pass_counts():
    stats = {}
    parallel_fault_simulation(C3, SEQ, width=8, stats=stats)
    assert stats == {"passes": 8, "word_evals": 64}  # 16, 10, 8 and 3 faults alive: 3 + 2 + 2 + 1 passes
    stats = {}
    parallel_fault_simulation(C3, SEQ, width=8, drop=False, stats=stats)
    assert stats["passes"] == 12
    stats = {}
    parallel_fault_simulation(C3, SEQ, width=64, stats=stats)
    assert stats["passes"] == 4


def test_c17_all_vectors():
    vectors = C17.all_vectors()
    result = parallel_fault_simulation(C17, vectors, drop=False)
    assert result == serial(C17, vectors, drop=False)
    assert [len(s) for s in result] == C17_COUNTS
    rng = random.Random(17)
    rng.shuffle(vectors)
    assert parallel_fault_simulation(C17, vectors, width=5) == serial(C17, vectors)


def test_redundant_faults_by_exhaustive_patterns():
    detected = set().union(*parallel_fault_simulation(CONSENSUS, CONSENSUS.all_vectors(), width=4))
    undetected = {CONSENSUS.fault_name(f) for f in CONSENSUS.faults() if f not in detected}
    assert undetected == REDUNDANT
    # Exhaustive patterns: an undetected fault here is redundant.
    for f in CONSENSUS.faults():
        if CONSENSUS.fault_name(f) in REDUNDANT:
            assert not CONSENSUS.detectable(f)


def test_fault_subset_and_order():
    rng = random.Random(5)
    faults = C17.faults()
    rng.shuffle(faults)
    faults = faults[:13]
    vectors = [tuple(rng.randint(0, 1) for _ in range(5)) for _ in range(9)]
    assert parallel_fault_simulation(C17, vectors, faults=faults, width=4) == serial(C17, vectors, faults=faults)


def test_random_circuits_against_serial():
    rng = random.Random(2024)
    for _ in range(120):
        c = random_circuit(rng, rng.randint(2, 6), rng.randint(3, 14), ops=OPS)
        vectors = [tuple(rng.randint(0, 1) for _ in c.pi) for _ in range(rng.randint(1, 10))]
        width = rng.randint(2, 9)
        for drop in (True, False):
            assert parallel_fault_simulation(c, vectors, drop=drop, width=width) == serial(c, vectors, drop=drop)


def test_width_must_hold_good_and_one_fault():
    with pytest.raises(ValueError):
        parallel_fault_simulation(C3, SEQ, width=1)
