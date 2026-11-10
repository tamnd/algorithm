# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/index-problem-lower-bound/. The authors are listed in prov/N46J3W.jsonl.

from itertools import product

from index_problem_lower_bound import (
    ExactDistinct,
    best_deterministic_error,
    binary_entropy,
    index_via_approx_f0,
    index_via_exact_f0,
    index_via_exact_median,
)


def all_inputs(n: int):
    for x in product((0, 1), repeat=n):
        for i in range(n):
            yield list(x), i


def test_exact_f0_reduction_recovers_every_bit() -> None:
    for n in range(1, 7):
        for x, i in all_inputs(n):
            assert index_via_exact_f0(x, i, ExactDistinct()) == x[i]


def test_approximate_f0_reduction_with_any_allowed_error() -> None:
    eps = 0.05
    n = 8  # eps * (n + 1) = 0.45 < 1/2
    for x, i in all_inputs(n):
        for factor in (1 - eps, 1 - eps / 2, 1, 1 + eps / 2, 1 + eps):
            assert index_via_approx_f0(x, i, lambda t, a=factor: a * t, eps) == x[i]


def test_approximate_f0_reduction_fails_when_eps_is_too_large() -> None:
    # With eps * (s + 1) >= 1/2 an allowed estimate can be on the wrong side.
    eps, x, i = 0.25, [1, 1, 1, 0], 3  # s = 3, true F_0 after Bob's item is 4
    assert index_via_approx_f0(x, i, lambda t: (1 - eps) * t, eps) != x[i]


def test_exact_median_reduction_recovers_every_bit() -> None:
    for n in range(1, 7):
        for x, i in all_inputs(n):
            assert index_via_exact_median(x, i) == x[i]


def test_deterministic_protocols_need_n_bits() -> None:
    # With fewer than n bits, two inputs share a message and Bob errs on one of them.
    for n, c in [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2)]:
        assert best_deterministic_error(n, c) > 0
    assert best_deterministic_error(2, 2) == 0
    assert best_deterministic_error(3, 2) == 1 / 6  # send two bits, guess the third


def test_information_bound_holds_for_the_best_protocols() -> None:
    # c >= (1 - H2(delta)) n for c-bit messages, with delta the average error.
    for n, c in [(2, 1), (3, 1), (3, 2)]:
        delta = best_deterministic_error(n, c)
        assert c >= (1 - binary_entropy(delta)) * n - 1e-12
