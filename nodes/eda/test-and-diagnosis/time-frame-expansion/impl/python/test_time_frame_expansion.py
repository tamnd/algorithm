# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/time-frame-expansion/. The authors are listed in prov/3RBAMV.jsonl.
"""Time-frame expansion against exhaustive sequential simulation from reset."""

from __future__ import annotations

import random
from itertools import product

import pytest

from td2net import Circuit
from time_frame_expansion import (
    SequentialCircuit,
    combinational_test,
    counter_with_enable,
    find_test_sequence,
    reachable_pairs,
    shortest_test_length,
    unroll,
)


def random_sequential(rng: random.Random, n_pi: int, n_ff: int, n_gates: int) -> SequentialCircuit:
    nets = [f"i{k}" for k in range(n_pi)] + [f"s{k}" for k in range(n_ff)]
    inputs = list(nets)
    gates = []
    for k in range(n_gates):
        op = rng.choice(["AND", "OR", "NAND", "NOR", "NOT", "XOR"])
        fanin = [rng.choice(nets)] if op == "NOT" else rng.sample(nets, 2)
        gates.append((f"g{k}", op, fanin))
        nets.append(f"g{k}")
    names = [g[0] for g in gates]
    outputs = [rng.choice(names)] + [rng.choice(names) for _ in range(n_ff)]
    reset = tuple(rng.randint(0, 1) for _ in range(n_ff))
    return SequentialCircuit(Circuit(inputs, gates, outputs), n_pi, n_ff, reset)


def detected_by_some_sequence(seq: SequentialCircuit, fault, k: int) -> bool:
    """Brute force: try every input sequence of exactly k vectors."""
    vectors = list(product((0, 1), repeat=seq.n_pi))
    return any(seq.detects(list(s), fault) for s in product(vectors, repeat=k))


def make(seed: int) -> SequentialCircuit:
    rng = random.Random(seed)
    return random_sequential(rng, rng.randint(1, 2), rng.randint(1, 2), rng.randint(3, 6))


@pytest.mark.parametrize("seed", range(40))
def test_array_simulation_equals_sequential_simulation(seed):
    seq = make(seed)
    rng = random.Random(1000 + seed)
    k = rng.randint(1, 5)
    ila = unroll(seq, k)
    for fault in [None] + seq.core.faults():
        pis = [rng.randint(0, 1) for _ in range(k * seq.n_pi)]
        vals = ila.simulate(pis, fault)
        outs = [tuple(vals[o] for o in ila.outputs[t * seq.n_po : (t + 1) * seq.n_po]) for t in range(k)]
        assert outs == seq.run(ila.frame_vectors(pis), fault)


@pytest.mark.parametrize("seed", range(25))
def test_shortest_sequence_matches_breadth_first_search(seed):
    seq = make(seed)
    k_max = 4
    for fault in seq.core.faults():
        length = shortest_test_length(seq, fault)
        found = find_test_sequence(seq, fault, k_max)
        if length is None or length > k_max:
            assert found is None
        else:
            assert found is not None and len(found) == length
            assert seq.detects(found, fault)


@pytest.mark.parametrize("seed", range(12))
def test_k_frame_array_has_a_test_iff_some_k_sequence_detects(seed):
    seq = make(500 + seed)
    for k in (1, 2, 3):
        ila = unroll(seq, k)
        for fault in seq.core.faults():
            assert (combinational_test(ila, fault) is not None) == detected_by_some_sequence(seq, fault, k)


@pytest.mark.parametrize("seed", range(25))
def test_shortest_test_within_reachable_pairs(seed):
    seq = make(seed)
    for fault in seq.core.faults():
        length = shortest_test_length(seq, fault)
        if length is not None:
            assert length <= reachable_pairs(seq, fault) <= 4**seq.n_ff


@pytest.mark.parametrize("m", range(1, 7))
def test_counter_needs_two_to_the_m_frames(m):
    seq = counter_with_enable(m)
    fault = (seq.core.line("z"), 0)
    assert shortest_test_length(seq, fault) == 2**m
    assert reachable_pairs(seq, fault) == 2**m


@pytest.mark.parametrize("m", range(1, 4))
def test_counter_array_search(m):
    seq = counter_with_enable(m)
    fault = (seq.core.line("z"), 0)
    assert combinational_test(unroll(seq, 2**m - 1), fault) is None
    found = find_test_sequence(seq, fault, 2**m)
    assert len(found) == 2**m
    assert all(v == (1,) for v in found[:-1])
    assert seq.detects(found, fault)


def test_two_bit_counter_example():
    seq = counter_with_enable(2)
    core = seq.core
    assert seq.run([(1,), (1,), (1,), (0,)]) == [(0,), (0,), (0,), (1,)]
    assert [shortest_test_length(seq, (core.line(n), v)) for n, v in [("z", 0), ("z", 1), ("e", 0), ("e", 1)]] == [4, 1, 4, 4]
    lengths = [shortest_test_length(seq, f) for f in core.faults()]
    assert len(lengths) == 28 and None not in lengths and max(lengths) == 4
    assert len(unroll(seq, 4).simulate([1, 1, 1, 0])) == 4 * core.n_lines
