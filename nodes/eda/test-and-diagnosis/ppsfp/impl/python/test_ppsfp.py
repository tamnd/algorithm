# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ppsfp/. The authors are listed in prov/THPQ1N.jsonl.

import random

import pytest

from gatenet import Circuit, random_circuit
from ppsfp import eval_word, good_words, ppsfp, propagate

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


def bits(word, n):
    """Bit 0 first, so the string reads in vector order."""
    return "".join(str(word >> i & 1) for i in range(n))


def test_eval_word_matches_gates_bit_by_bit():
    rng = random.Random(1)
    mask = (1 << 8) - 1
    for op in OPS:
        for _ in range(50):
            n = 1 if op in ("NOT", "BUF") else rng.randint(2, 4)
            words = [rng.getrandbits(8) for _ in range(n)]
            out = eval_word(op, words, mask)
            for k in range(8):
                c = Circuit([f"x{i}" for i in range(n)], [("y", op, [f"x{i}" for i in range(n)])], ["y"])
                assert out >> k & 1 == c.outputs([w >> k & 1 for w in words])[0]


def test_page_words_and_masks():
    good = good_words(C3, SEQ, 15)
    assert {C3.name[k]: bits(good[k], 4) for k in range(C3.n_lines)} == {
        "a": "1001", "b": "0111", "b>g": "0111", "b>h": "0111", "c": "1010", "g": "1110", "h": "1101", "z": "0011",
    }
    seen = {}
    evals = {}
    for f in C3.faults():
        counter = [0]
        seen[C3.fault_name(f)] = bits(propagate(C3, good, f, 15, counter), 4)
        evals[C3.fault_name(f)] = counter[0]
    assert seen == {
        "a/0": "0001", "a/1": "0100", "b/0": "0011", "b/1": "1000", "b>g/0": "0001", "b>g/1": "1000",
        "b>h/0": "0010", "b>h/1": "1000", "c/0": "0010", "c/1": "0100", "g/0": "1100", "g/1": "0001",
        "h/0": "1100", "h/1": "0010", "z/0": "0011", "z/1": "1100",
    }
    assert evals["b/0"] == 5 and evals["z/0"] == 0 and sum(evals.values()) == 30


@pytest.mark.parametrize("width", [1, 2, 3, 4, 64])
def test_page_example(width):
    assert names(C3, ppsfp(C3, SEQ, width=width)) == FIRSTS
    assert names(C3, ppsfp(C3, SEQ, drop=False, width=width)) == ALL_DETECTED


def test_page_stats():
    stats = {}
    ppsfp(C3, SEQ, width=4, stats=stats)
    assert stats == {"blocks": 1, "fault_runs": 16, "gate_evals": 30}
    stats = {}
    ppsfp(C3, SEQ, width=1, stats=stats)
    assert stats == {"blocks": 4, "fault_runs": 37, "gate_evals": 39}  # 16 + 10 + 8 + 3 fault runs


def test_c17_all_vectors():
    vectors = C17.all_vectors()
    result = ppsfp(C17, vectors, drop=False)
    assert result == serial(C17, vectors, drop=False)
    assert [len(s) for s in result] == C17_COUNTS
    rng = random.Random(17)
    rng.shuffle(vectors)
    assert ppsfp(C17, vectors, width=5) == serial(C17, vectors)


def test_redundant_faults_by_exhaustive_patterns():
    detected = set().union(*ppsfp(CONSENSUS, CONSENSUS.all_vectors(), width=8))
    undetected = {CONSENSUS.fault_name(f) for f in CONSENSUS.faults() if f not in detected}
    assert undetected == REDUNDANT


def test_fault_subset_and_order():
    rng = random.Random(5)
    faults = C17.faults()
    rng.shuffle(faults)
    faults = faults[:13]
    vectors = [tuple(rng.randint(0, 1) for _ in range(5)) for _ in range(9)]
    assert ppsfp(C17, vectors, faults=faults, width=4) == serial(C17, vectors, faults=faults)


def test_random_circuits_against_serial():
    rng = random.Random(2024)
    for _ in range(120):
        c = random_circuit(rng, rng.randint(2, 6), rng.randint(3, 14), ops=OPS)
        vectors = [tuple(rng.randint(0, 1) for _ in c.pi) for _ in range(rng.randint(1, 10))]
        width = rng.randint(1, 6)
        for drop in (True, False):
            assert ppsfp(c, vectors, drop=drop, width=width) == serial(c, vectors, drop=drop)


def test_empty_block_size_rejected():
    with pytest.raises(ValueError):
        ppsfp(C3, SEQ, width=0)
