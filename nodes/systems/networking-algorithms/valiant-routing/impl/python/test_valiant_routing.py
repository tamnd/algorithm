# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/valiant-routing/. The authors are listed in prov/NZAZBW.jsonl.

import random

from valiant_routing import (
    bit_fixing_dims,
    bit_reversal,
    greedy_route,
    run_phase,
    shared_edge_counts,
    transpose,
    valiant_route,
)


def test_bit_fixing_route() -> None:
    assert bit_fixing_dims(4, 0b0110, 0b1011) == [3, 2, 0]
    assert bit_fixing_dims(4, 5, 5) == []


def test_delay_lemma_holds() -> None:
    # Delay of p is at most the number of other packets whose routes share an edge with p.
    rng = random.Random(1)
    for _ in range(40):
        n = rng.randrange(2, 9)
        size = 1 << n
        start = [rng.randrange(size) for _ in range(size)]
        target = [rng.randrange(size) for _ in range(size)]
        _, delay, _ = run_phase(n, start, target)
        shared = shared_edge_counts(n, start, target)
        assert all(d <= s for d, s in zip(delay, shared))
    for n in (6, 8):
        _, delay, _ = run_phase(n, list(range(1 << n)), bit_reversal(n))
        assert all(d <= s for d, s in zip(delay, shared_edge_counts(n, list(range(1 << n)), bit_reversal(n))))


def test_greedy_is_slow_on_bit_reversal_and_transpose() -> None:
    expected = {6: 7, 8: 12, 10: 21, 12: 38}
    for n, steps in expected.items():
        root = 1 << (n // 2)
        assert greedy_route(n, bit_reversal(n)) == steps >= root // 2
        assert greedy_route(n, transpose(n)) == steps


def test_valiant_is_fast_on_the_same_permutations() -> None:
    for n in (6, 8, 10, 12):
        for seed in range(3):
            phased = valiant_route(n, bit_reversal(n), random.Random(seed))
            assert phased <= 14 * n
            assert valiant_route(n, transpose(n), random.Random(seed)) <= 14 * n
    assert valiant_route(12, bit_reversal(12), random.Random(0)) < greedy_route(12, bit_reversal(12))


def test_pipelined_form_delivers_too() -> None:
    for n in (4, 8, 10):
        steps = valiant_route(n, bit_reversal(n), random.Random(5), phased=False)
        assert steps <= 14 * n


def test_mean_edge_load_is_one_half() -> None:
    n = 10
    size = 1 << n
    rng = random.Random(7)
    total = 0
    trials = 20
    for _ in range(trials):
        r = [rng.randrange(size) for _ in range(size)]
        total += sum(len(bit_fixing_dims(n, p, r[p])) for p in range(size))
    mean_load = total / (trials * size * n)
    assert 0.48 < mean_load < 0.52
