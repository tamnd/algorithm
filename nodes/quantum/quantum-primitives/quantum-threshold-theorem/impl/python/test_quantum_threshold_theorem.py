# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-threshold-theorem/. The authors are listed in prov/SATJ60.jsonl.
"""Tests of the concatenation recursion. These are code-capacity models (perfect decoding), not a
fault-tolerant simulation; see the module docstring."""

import math
import random
from fractions import Fraction

from quantum_threshold_theorem import (N, concatenated_majority, concatenated_steane, depolarizing, exact_majority_rate,
                                       failures_by_weight, levels_needed, majority_tree, pseudo_threshold,
                                       steane_level)


def test_majority_recursion_is_exact() -> None:
    for p in (Fraction(1, 10), Fraction(1, 3), Fraction(2, 5)):
        assert exact_majority_rate(p, 1) == 3 * p ** 2 - 2 * p ** 3
        assert exact_majority_rate(p, 2) == concatenated_majority(p, 2)  # all 512 patterns of 9 bits


def test_majority_level_three_by_sampling() -> None:
    rng = random.Random(6061)
    p, shots = 0.2, 20000
    fails = sum(majority_tree([int(rng.random() < p) for _ in range(27)]) for _ in range(shots))
    # Hoeffding: |mean - expected| <= sqrt(ln(2/delta) / (2 shots)) with probability 1 - delta, delta = 1e-6
    tol = math.sqrt(math.log(2 / 1e-6) / (2 * shots))
    assert abs(fails / shots - concatenated_majority(p, 3)) < tol


def test_majority_threshold_and_double_exponential_fall() -> None:
    # f(p) <= 3 p^2, so the recursion bound is p_k <= p_th (p / p_th)^(2^k) with p_th = 1/3
    p_th = Fraction(1, 3)
    for p in (Fraction(1, 10), Fraction(1, 5), Fraction(3, 10)):
        for k in range(6):
            assert concatenated_majority(p, k) <= p_th * (p / p_th) ** (2 ** k)
    # the true threshold of the majority map is its fixed point 1/2
    assert concatenated_majority(Fraction(1, 2), 4) == Fraction(1, 2)
    assert concatenated_majority(0.45, 8) < 0.01 and concatenated_majority(0.55, 8) > 0.99


def test_steane_failures_by_weight() -> None:
    fails = failures_by_weight()
    totals = [math.comb(N, w) * 3 ** w for w in range(N + 1)]
    assert sum(totals) == 4 ** N
    assert fails[0] == 0 and fails[1] == 0  # every single-qubit Pauli error is corrected
    # of the 189 errors of weight 2, exactly the 42 of the form X_i Z_j with i != j are corrected
    assert fails[2] == 189 - 42 == 147
    assert fails == [0, 0, 147, 693, 2226, 3822, 3675, 1725]


def test_steane_level_is_exact() -> None:
    p = Fraction(1, 100)
    q = steane_level(depolarizing(p))
    assert sum(q) == 1
    fails = failures_by_weight()
    assert 1 - q[0] == sum(f * (p / 3) ** w * (1 - p) ** (N - w) for w, f in enumerate(fails))
    assert q[1] == q[3]  # X and Z are symmetric in the Steane code
    # for small p the logical rate is (147/9) p^2 + O(p^3)
    tiny = Fraction(1, 10 ** 6)
    ratio = (1 - steane_level(depolarizing(tiny))[0]) / tiny ** 2
    assert abs(ratio - Fraction(147, 9)) < Fraction(1, 10 ** 3)


def test_steane_below_and_above_threshold() -> None:
    pt = pseudo_threshold()
    assert 0.0810 < pt < 0.0812  # one level helps for depolarizing noise below about 8.1%
    low = [concatenated_steane(0.01, k) for k in range(4)]
    assert all(b < a for a, b in zip(low, low[1:])) and low[3] < 1e-7
    # with q_k about A q_(k-1)^2 and A = 147/9, log(A q_k) about doubles per level: double exponential decay
    a_const = 147 / 9
    assert all(math.log(a_const * b) < 1.8 * math.log(a_const * a) for a, b in zip(low[1:], low[2:]))
    high = [concatenated_steane(0.12, k) for k in range(4)]
    assert all(b > a for a, b in zip(high, high[1:]))


def test_levels_and_overhead_are_small() -> None:
    # with p ten times below a threshold of 1e-2 the bound reaches 1e-15 in 4 levels, 7^4 = 2401 qubits
    k = levels_needed(1e-3, 1e-2, 1e-15)
    assert k == 4 and 7 ** k == 2401
    # the levels grow like log log(1/target): 1e-30 needs one more level
    assert levels_needed(1e-3, 1e-2, 1e-30) == 5
