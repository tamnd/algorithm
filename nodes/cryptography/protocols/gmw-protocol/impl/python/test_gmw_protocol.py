# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gmw-protocol/. The authors are listed in prov/6M8M74.jsonl.
# There are no official test vectors for GMW. The tests compare the protocol
# with plain evaluation on random circuits and on an adder, check that the
# number of rounds equals the AND depth, and check that P2's view is uniform.

import random
from collections import Counter

import pytest

from gmw_protocol import (
    Circuit,
    adder,
    and_depths,
    from_bits,
    gmw,
    plain_eval,
    random_circuit,
    to_bits,
)

MODES = ("ot", "triple")


@pytest.mark.parametrize("mode", MODES)
def test_random_circuits_match_plain_evaluation(mode: str) -> None:
    rng = random.Random(1987)
    for _ in range(200):
        circ = random_circuit(4, 40, 6, rng)
        x = [rng.getrandbits(1) for _ in range(4)]
        y = [rng.getrandbits(1) for _ in range(4)]
        out, _ = gmw(circ, x, y, rng, mode)
        assert out == plain_eval(circ, x, y)


@pytest.mark.parametrize("mode", MODES)
def test_adder_on_all_inputs(mode: str) -> None:
    rng = random.Random(1991)
    circ = adder(4)
    for a in range(16):
        for b in range(16):
            out, _ = gmw(circ, to_bits(a, 4), to_bits(b, 4), rng, mode)
            assert from_bits(out) == a + b


def test_rounds_equal_and_depth() -> None:
    rng = random.Random(3)
    for _ in range(100):
        circ = random_circuit(3, rng.randint(1, 50), 3, rng)
        dep = and_depths(circ)
        depth = max(dep[g[3]] for g in circ.gates)
        for mode in MODES:
            _, st = gmw(circ, [0, 1, 1], [1, 0, 1], rng, mode)
            assert st.rounds == depth
    # The w-bit ripple-carry adder has AND depth w, so w rounds.
    for w in (1, 4, 8, 16):
        _, st = gmw(adder(w), [0] * w, [1] * w, rng, "ot")
        assert st.rounds == w and st.ots == w


def test_cost_counters() -> None:
    rng = random.Random(4)
    circ = random_circuit(4, 60, 4, rng)
    n_and = sum(1 for g in circ.gates if g[0] == "AND")
    _, st = gmw(circ, [1, 0, 1, 0], [0, 0, 1, 1], rng, "ot")
    assert st.ots == n_and and st.triples == 0
    _, st = gmw(circ, [1, 0, 1, 0], [0, 0, 1, 1], rng, "triple")
    assert st.triples == n_and and st.opened_bits == 4 * n_and and st.ots == 0


@pytest.mark.parametrize("mode", MODES)
def test_view_of_p2_does_not_depend_on_p1_input(mode: str) -> None:
    # One AND gate of P1's bit a and P2's bit b. P2's view during the gates
    # (its share of a and what it got in the AND step) must have the same
    # distribution for a = 0 and a = 1.
    circ = Circuit(3, [0], [1], [2], [("AND", 0, 1, 2)])
    rng = random.Random(6)
    counts = {}
    for a in (0, 1):
        c = Counter()
        for _ in range(8000):
            _, st = gmw(circ, [a], [1], rng, mode)
            c[tuple(st.view2)] += 1
        counts[a] = c
    keys = set(counts[0]) | set(counts[1])
    assert keys == set(counts[0]) == set(counts[1])
    stat = sum((counts[0][k] - counts[1][k]) ** 2 / (counts[0][k] + counts[1][k]) for k in keys)
    assert stat < 25.0  # at most 7 degrees of freedom, 0.999 quantile about 24.3
