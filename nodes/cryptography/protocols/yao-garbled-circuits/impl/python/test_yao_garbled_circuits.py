# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yao-garbled-circuits/. The authors are listed in prov/7XSXVN.jsonl.
# There are no official test vectors for garbled circuits (the labels are
# random). The tests compare the garbled run with plain evaluation on every
# small input, count the ciphertexts per AND gate, and check the label
# invariants the correctness proof uses.

import random

import pytest

from yao_garbled_circuits import (
    KAPPA,
    adder,
    ciphertexts_per_and,
    comparator,
    evaluate,
    from_bits,
    garble,
    lsb,
    plain_eval,
    to_bits,
    yao_protocol,
)

W = 3
MODES = ("classic", "grr3", "half")


@pytest.mark.parametrize("mode", MODES)
def test_comparator_on_all_inputs(mode: str) -> None:
    rng = random.Random(1986)
    circ = comparator(W)
    for a in range(2 ** W):
        for b in range(2 ** W):
            x, y = to_bits(a, W), to_bits(b, W)
            assert plain_eval(circ, x, y) == [int(a > b), int(a <= b)]
            assert yao_protocol(circ, x, y, rng, mode) == [int(a > b), int(a <= b)]


@pytest.mark.parametrize("mode", MODES)
def test_adder_on_all_inputs(mode: str) -> None:
    rng = random.Random(2015)
    circ = adder(W)
    for a in range(2 ** W):
        for b in range(2 ** W):
            x, y = to_bits(a, W), to_bits(b, W)
            assert from_bits(plain_eval(circ, x, y)) == a + b
            assert from_bits(yao_protocol(circ, x, y, rng, mode)) == a + b


def test_random_circuits_match_plain_evaluation() -> None:
    rng = random.Random(5)
    from yao_garbled_circuits import Circuit
    for _ in range(40):
        n_in = 4
        gates = []
        wires = list(range(2 * n_in))
        for k in range(30):
            op = rng.choice(["AND", "XOR", "INV"])
            gates.append((op, rng.choice(wires), rng.choice(wires), 2 * n_in + k))
            wires.append(2 * n_in + k)
        circ = Circuit(2 * n_in + 30, list(range(n_in)), list(range(n_in, 2 * n_in)), wires[-5:], gates)
        x = [rng.getrandbits(1) for _ in range(n_in)]
        y = [rng.getrandbits(1) for _ in range(n_in)]
        for mode in MODES:
            assert yao_protocol(circ, x, y, rng, mode) == plain_eval(circ, x, y)


def test_ciphertexts_per_and_gate() -> None:
    rng = random.Random(1)
    circ = comparator(8)
    counts = {mode: ciphertexts_per_and(circ, garble(circ, rng, mode)[0]) for mode in MODES}
    assert counts == {"classic": {4}, "grr3": {3}, "half": {2}}
    # XOR and INV gates have no table at all (free XOR).
    gc, _ = garble(circ, rng, "half")
    and_gates = sum(1 for g in circ.gates if g[0] == "AND")
    assert len(gc.tables) == and_gates == 8
    assert sum(len(t) for t in gc.tables.values()) * KAPPA == 2 * KAPPA * 8


def test_label_invariants() -> None:
    rng = random.Random(9)
    circ = adder(4)
    gc, sec = garble(circ, rng, "half")
    assert lsb(sec.delta) == 1 and sec.delta.bit_length() <= KAPPA
    for w in range(circ.n_wires):
        if w in sec.zero_labels:
            # The two labels of a wire differ in their permute bit.
            assert lsb(sec.label(w, 0)) != lsb(sec.label(w, 1))
    # The evaluator holding W^v on every input wire gets W^v on every wire:
    # check it on the outputs by decoding with lsb and the decode bits.
    for a, b in ((3, 5), (15, 15), (0, 9)):
        x, y = to_bits(a, 4), to_bits(b, 4)
        labels = {w: sec.label(w, v) for w, v in zip(circ.garbler_inputs + circ.evaluator_inputs, x + y)}
        assert from_bits(evaluate(circ, gc, labels)) == a + b


def test_wrong_label_does_not_decode_reliably() -> None:
    # A label that is neither W^0 nor W^1 gives garbage: the evaluator cannot
    # make up labels for values it was not given.
    rng = random.Random(4)
    circ = comparator(W)
    wrong = 0
    for _ in range(200):
        gc, sec = garble(circ, rng, "half")
        labels = {w: sec.label(w, 0) for w in circ.garbler_inputs + circ.evaluator_inputs}
        labels[circ.garbler_inputs[1]] = rng.getrandbits(KAPPA)
        bad = evaluate(circ, gc, labels)
        wrong += bad != plain_eval(circ, [0] * W, [0] * W)
    assert 50 < wrong < 200
