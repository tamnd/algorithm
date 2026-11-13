# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reversible-computation/. The authors are listed in prov/3F0WFR.jsonl.

import random

from reversible_computation import (
    bennett,
    compute_with_garbage,
    evaluate,
    landauer_embedding,
    pebble_schedule,
    play_pebbles,
    run_bits,
)

# Majority of three bits as pairwise ANDs: maj(x) = x0 x1 xor x0 x2 xor x1 x2.
MAJ = [("and", (0, 1)), ("and", (0, 2)), ("and", (1, 2)), ("xor", (3, 4)), ("xor", (6, 5))]
MAJ_OUT = [7]

# A 2-bit adder: inputs a = (x0, x1), b = (x2, x3); outputs the 3-bit sum.
ADD2 = [
    ("xor", (0, 2)),   # 4: s0
    ("and", (0, 2)),   # 5: c0
    ("xor", (1, 3)),   # 6
    ("xor", (6, 5)),   # 7: s1
    ("and", (1, 3)),   # 8
    ("and", (6, 5)),   # 9
    ("or", (8, 9)),    # 10: c1 = s2
]
ADD2_OUT = [4, 7, 10]


def random_circuit(rng, n, g):
    ops = ["and", "or", "xor", "nand", "not"]
    circ = []
    for i in range(g):
        op = rng.choice(ops)
        w = n + i
        args = (rng.randrange(w),) if op == "not" else (rng.randrange(w), rng.randrange(w))
        circ.append((op, args))
    return circ


def check_bennett(circ, n, outputs):
    gates, width, out_wires = bennett(circ, n, outputs)
    g = len(circ)
    for x in range(1 << n):
        y = run_bits(x, gates)
        assert y & ((1 << n) - 1) == x, "the input changed"
        assert (y >> n) & ((1 << g) - 1) == 0, "a work bit is not 0"
        got = sum(((y >> w) & 1) << i for i, w in enumerate(out_wires))
        assert got == evaluate(circ, n, outputs, x)
    return gates, width


def test_reference_values() -> None:
    assert [evaluate(MAJ, 3, MAJ_OUT, x) for x in range(8)] == [0, 0, 0, 1, 0, 1, 1, 1]
    for a in range(4):
        for b in range(4):
            assert evaluate(ADD2, 4, ADD2_OUT, a | (b << 2)) == a + b


def test_garbage_version_keeps_every_gate_value() -> None:
    gates = compute_with_garbage(MAJ, 3)
    for x in range(8):
        y = run_bits(x, gates)
        bits = [(x >> i) & 1 for i in range(3)]
        assert (y >> 3) & 1 == bits[0] & bits[1]
        assert (y >> 7) & 1 == evaluate(MAJ, 3, MAJ_OUT, x)


def test_bennett_on_every_input() -> None:
    gates, width = check_bennett(MAJ, 3, MAJ_OUT)
    assert width == 3 + 5 + 1
    assert len(gates) == 2 * len(compute_with_garbage(MAJ, 3)) + 1
    check_bennett(ADD2, 4, ADD2_OUT)


def test_bennett_on_random_circuits() -> None:
    rng = random.Random(20261113)
    for _ in range(60):
        n, g = rng.randint(1, 5), rng.randint(1, 8)
        circ = random_circuit(rng, n, g)
        m = rng.randint(1, 3)
        outputs = [rng.randrange(n + g) for _ in range(m)]
        check_bennett(circ, n, outputs)


def test_reversible_circuit_is_a_bijection_on_all_wires() -> None:
    gates, width = check_bennett(ADD2, 4, ADD2_OUT)
    images = {run_bits(z, gates) for z in range(1 << width)}
    assert len(images) == 1 << width


def test_landauer_embedding_is_an_involution() -> None:
    rng = random.Random(7)
    for _ in range(20):
        table = [rng.randrange(4) for _ in range(8)]
        p = landauer_embedding(lambda x: table[x], 3, 2)
        assert sorted(p(z) for z in range(32)) == list(range(32))
        assert all(p(p(z)) == z for z in range(32))
        assert all(p(x) >> 3 == table[x] for x in range(8))


def test_binary_pebble_game() -> None:
    for k in range(0, 8):
        moves = pebble_schedule(k)
        final, most = play_pebbles(moves, 2 ** k)
        assert final == {2 ** k}
        assert len(moves) == 3 ** k
        assert most == k + 1


def test_m_ary_pebble_game() -> None:
    for m in (2, 3, 4):
        for k in range(0, 5):
            if m ** k > 300:
                continue
            moves = pebble_schedule(k, m)
            final, most = play_pebbles(moves, m ** k)
            assert final == {m ** k}
            assert len(moves) == (2 * m - 1) ** k
            assert most == (m - 1) * k + 1


def test_bad_schedule_is_rejected() -> None:
    try:
        play_pebbles([2], 4)
    except ValueError:
        return
    raise AssertionError("a move on node 2 without a pebble on node 1 must fail")
