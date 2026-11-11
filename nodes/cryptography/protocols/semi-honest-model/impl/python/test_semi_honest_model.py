# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semi-honest-model/. The authors are listed in prov/ZHSBS2.jsonl.
# There are no official test vectors for semi-honest simulation. The tests
# enumerate every random choice on tiny moduli and compare exact distributions.

import itertools

from semi_honest_model import (
    additive_sum_simulator,
    additive_sum_view,
    distribution,
    ideal_coin_joint,
    leaky_coin_joint,
    real_distribution,
    ring_sum_view_of_party,
    simulated_distribution,
    simulator_coin_count,
)

M = 3


def test_simulator_matches_real_view_for_one_corrupt_party() -> None:
    for inputs in [(0, 0, 0), (1, 2, 0), (2, 2, 2), (0, 1, 2)]:
        y = sum(inputs) % M
        for j in range(3):
            real = real_distribution(inputs, [j], M)
            sim = simulated_distribution({j: inputs[j]}, y, 3, M)
            assert real == sim


def test_simulator_matches_real_view_for_two_corrupt_parties() -> None:
    inputs = (2, 0, 1)
    y = sum(inputs) % M
    real = real_distribution(inputs, [0, 2], M)
    sim = simulated_distribution({0: 2, 2: 1}, y, 3, M)
    assert real == sim


def test_view_depends_only_on_own_input_and_output() -> None:
    # Same input of party 0 and same sum: the views have the same distribution.
    assert real_distribution((1, 0, 2), [0], M) == real_distribution((1, 2, 0), [0], M)
    # Different sum: the distributions differ (the output is part of the view).
    assert real_distribution((1, 0, 2), [0], M) != real_distribution((1, 0, 1), [0], M)


def test_simulated_view_is_consistent() -> None:
    n = 3
    for coins in itertools.product(range(M), repeat=simulator_coin_count(n, 1)):
        v = additive_sum_simulator({1: 2}, 1, n, coins, M)
        partials = v[-1]
        assert sum(partials) % M == 1
        # The corrupted party's partial sum equals the sum of what it received.
        assert partials[1] == sum(v[0][2]) % M


def test_real_view_one_example() -> None:
    v = additive_sum_view((1, 2, 0), [(0, 1), (2, 2), (1, 1)], [0], M)
    # Party 0 shares 1 as (0, 1, 0); party 1 shares 2 as (2, 2, 1); party 2 shares 0 as (1, 1, 1).
    assert v == ((1, (0, 1), (0, 2, 1)), (0, 1, 2))


def test_ring_protocol_has_no_simulator() -> None:
    # Party 1 has input 0 and the sum is 3 in both runs, so the ideal world
    # gives it the same information. Its real views differ, so no simulator
    # can match both, and the protocol is not secure even for semi-honest parties.
    a = ring_sum_view_of_party((1, 0, 2), 1, 7)
    b = ring_sum_view_of_party((2, 0, 1), 1, 7)
    assert a[0] == b[0] and a[2] == b[2]
    assert a != b
    assert a[1] == 1 and b[1] == 2


def test_randomized_functionality_needs_the_joint_distribution() -> None:
    real = distribution([leaky_coin_joint(c) for c in (0, 1)])
    ideal = distribution([ideal_coin_joint(c, s) for c in (0, 1) for s in (0, 1)])
    # Party 2's view alone is a uniform bit in both worlds.
    marg_real = distribution([leaky_coin_joint(c)[1] for c in (0, 1)])
    marg_ideal = distribution([ideal_coin_joint(c, s)[1] for c in (0, 1) for s in (0, 1)])
    assert marg_real == marg_ideal == {0: 0.5, 1: 0.5}
    # Jointly with party 1's output, the worlds differ.
    assert real != ideal
    assert real[(0, 0)] == 0.5 and ideal[(0, 0)] == 0.25
