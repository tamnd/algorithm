# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/context-modeling/. The authors are listed in prov/SDA0PS.jsonl.

import math

from context_modeling import empirical_conditional_entropy, entropy_rate, order_k_length, random_markov_source, sample


def test_periodic_text() -> None:
    seq = [0, 1] * 500
    assert order_k_length(seq, 0, 2) > 990
    # Order 1 learns the rule; the KT cost of a run of n equal bits is about lg(n)/2 + 1 per context.
    assert order_k_length(seq, 1, 2) < 2 * (0.5 * math.log2(500) + 1) + 2


def test_right_order_reaches_the_entropy_rate() -> None:
    table = random_markov_source(2, 4, seed=7)
    rate = entropy_rate(table, 2, 4)
    n = 50000
    seq = sample(table, 2, 4, n, seed=11)
    per_symbol = {k: order_k_length(seq, k, 4) / n for k in range(5)}
    assert abs(per_symbol[2] - rate) < 0.02
    assert per_symbol[0] > rate + 0.4 and per_symbol[1] > rate + 0.4
    # Orders above 2 add contexts without adding information.
    assert per_symbol[2] < per_symbol[3] < per_symbol[4]


def test_too_large_an_order_dilutes_on_short_input() -> None:
    table = random_markov_source(2, 4, seed=7)
    rate = entropy_rate(table, 2, 4)
    n = 1000
    seq = sample(table, 2, 4, n, seed=11)
    two, eight = order_k_length(seq, 2, 4) / n, order_k_length(seq, 8, 4) / n
    assert eight > two + 0.4
    # Chosen after the fact, the order-8 model looks far better than the source: it overfits.
    assert empirical_conditional_entropy(seq, 8) < rate - 0.5


def test_empirical_conditional_entropy_does_not_increase() -> None:
    table = random_markov_source(3, 3, seed=1)
    seq = sample(table, 3, 3, 5000, seed=2)
    hs = [empirical_conditional_entropy(seq, k) for k in range(8)]
    assert all(b <= a + 1e-12 for a, b in zip(hs, hs[1:]))
    # The adaptive order-k length is never below n H_k.
    for k in range(8):
        assert order_k_length(seq, k, 3) >= len(seq) * hs[k]


def test_empty_and_tiny() -> None:
    assert order_k_length([], 3, 2) == 0
    assert empirical_conditional_entropy([], 2) == 0
    assert abs(order_k_length([1], 3, 2) - 1.0) < 1e-12
