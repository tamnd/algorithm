# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nist-security-levels/. The authors are listed in prov/RP9RYK.jsonl.

import math

import pytest

from nist_security_levels import (
    AES_2016,
    AES_2022,
    CATEGORIES,
    LOG2_PI_4,
    category_of,
    constant_from_table,
    crossover_maxdepth_log2,
    meets_category,
    parallel_grover,
    predicted_quantum_log2,
)

# An assumed depth of one Grover iteration, 2^12, and the gate count that
# makes the model match the 2022 table: (pi / 4)^2 * d * g = 2^29.
DEPTH = 12.0
GATES = 29 - 2 * LOG2_PI_4 - DEPTH


def test_constants_from_the_two_calls():
    assert constant_from_table(AES_2016) == {128: 42, 192: 41, 256: 42}
    assert constant_from_table(AES_2022) == {128: 29, 192: 29, 256: 29}


def test_one_constant_predicts_the_other_key_sizes():
    c22 = constant_from_table(AES_2022)[128]
    for k, (x, _) in AES_2022.items():
        assert predicted_quantum_log2(k, c22) == x
    c16 = constant_from_table(AES_2016)[128]
    for k, (x, _) in AES_2016.items():
        assert abs(predicted_quantum_log2(k, c16) - x) <= 1


@pytest.mark.parametrize("k", [128, 192, 256])
@pytest.mark.parametrize("maxdepth", [40, 64])
def test_parallel_model_reproduces_2022_table(k, maxdepth):
    cost = parallel_grover(k, maxdepth, DEPTH, GATES)
    assert cost.machines > 0
    assert cost.depth == pytest.approx(maxdepth)
    assert cost.total_gates == pytest.approx(AES_2022[k][0] - maxdepth)


def test_gates_times_maxdepth_is_constant():
    products = {round(parallel_grover(128, d, DEPTH, GATES).total_gates + d, 9) for d in range(30, 70)}
    assert len(products) == 1


def test_machine_counts_for_aes128():
    # S = 2^k * (pi/4 * d)^2 / MAXDEPTH^2
    assert parallel_grover(128, 40, DEPTH, GATES).machines == pytest.approx(128 + 2 * (LOG2_PI_4 + 12) - 80)
    assert parallel_grover(128, 64, DEPTH, GATES).machines == pytest.approx(23.30, abs=0.01)


def test_large_maxdepth_saturates():
    # One machine fits in depth 2^75.65, so beyond that the cost stops falling,
    # and the table figure 2^157 / MAXDEPTH understates it (footnote 5).
    cost = parallel_grover(128, 96, DEPTH, GATES)
    assert cost.machines == 0
    assert cost.iterations_per_machine == pytest.approx(64 + LOG2_PI_4)
    assert cost.depth < 96
    assert cost.total_gates > AES_2022[128][0] - 96


def test_grover_beats_classical_only_for_deep_circuits():
    assert crossover_maxdepth_log2(128, AES_2016) == 27
    assert crossover_maxdepth_log2(128, AES_2022) == 14
    assert crossover_maxdepth_log2(256, AES_2022) == 13


def test_categories_are_ordered():
    thresholds = [CATEGORIES[c][1] for c in sorted(CATEGORIES)]
    assert thresholds == sorted(thresholds)


def test_category_of_classical_attacks():
    assert category_of(140) == 0
    assert category_of(145) == 1
    assert category_of(150) == 2
    assert category_of(208) == 3
    assert category_of(272) == 5
    assert not meets_category(4, 209)


def test_category_with_a_quantum_attack():
    # Classical 2^150 but a quantum attack of 2^120 gates at any depth. It
    # fails category 2 (2^146 in every metric), but it meets category 1,
    # because it costs more than 2^157 / 2^40 = 2^117 at the smallest depth.
    assert category_of(150) == 2
    assert category_of(150, lambda d: 120) == 1
    assert category_of(150, lambda d: 110) == 0
    # A Grover-like attack with the same cost as AES-128 meets category 1.
    assert meets_category(1, 143, lambda d: min(157 - d, 143))


def test_float_safety():
    assert math.isfinite(parallel_grover(256, 40, DEPTH, GATES).total_gates)
