# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-product-formulas/. The authors are listed in prov/M9S5CZ.jsonl.

import math
import random

from multi_product_formulas import mpf_coefficients, mpf_lcu, mpf_matrix, product_formula, strang
from qsim import (
    add,
    dagger,
    expm_hermitian,
    matmul,
    matvec,
    norm,
    op_norm,
    pauli_sum_matrix,
    random_state,
    scale,
    sub,
)

EXAMPLE = [(1.0, "ZZ"), (0.5, "IX"), (0.5, "XI")]


def random_terms(rng, n, big_l):
    seen, terms = set(), []
    while len(terms) < big_l:
        s = "".join(rng.choice("IXYZ") for _ in range(n))
        if s not in seen and set(s) != {"I"}:
            seen.add(s)
            terms.append((rng.uniform(-1, 1), s))
    return terms


def test_the_coefficients_solve_the_cancellation_conditions():
    for ks in [[1, 2], [1, 2, 3], [1, 2, 3, 4], [2, 3, 5, 8, 13]]:
        cs = mpf_coefficients(ks)
        assert abs(sum(cs) - 1) < 1e-12
        for j in range(1, len(ks)):
            assert abs(sum(c * k ** (-2 * j) for c, k in zip(cs, ks))) < 1e-12
    assert all(abs(a - b) < 1e-12 for a, b in zip(mpf_coefficients([1, 2]), [-1 / 3, 4 / 3]))
    assert all(abs(a - b) < 1e-12 for a, b in zip(mpf_coefficients([1, 2, 3]), [1 / 24, -16 / 15, 81 / 40]))


def test_strang_is_symmetric_and_second_order():
    h = pauli_sum_matrix(EXAMPLE)
    # S2(t) S2(-t) = I, and the local error falls by 8 when t halves.
    assert op_norm(sub(matmul(strang(EXAMPLE, 0.3), strang(EXAMPLE, -0.3)), expm_hermitian(h, 0))) < 1e-12
    e1 = op_norm(sub(strang(EXAMPLE, 0.1), expm_hermitian(h, 0.1)))
    e2 = op_norm(sub(strang(EXAMPLE, 0.05), expm_hermitian(h, 0.05)))
    assert abs(e1 / e2 - 8) < 0.1


def test_error_order_by_step_doubling():
    # Doubling every k_q multiplies the error of the order-2m formula by about 2^(-2m).
    h = pauli_sum_matrix(EXAMPLE)
    u = expm_hermitian(h, 1.0)
    for ks in [[1], [1, 2], [1, 2, 3], [1, 2, 3, 4]]:
        m = len(ks)
        errs = [op_norm(sub(mpf_matrix(EXAMPLE, 1.0, [k * n for k in ks]), u)) for n in [2, 4, 8]]
        ratio = errs[1] / errs[2]
        assert abs(math.log2(ratio) - 2 * m) < 0.1, (ks, ratio)


def test_local_error_order_by_step_halving():
    # For one call with time t, the error is O(t^(2m+1)), so halving t divides it by about 2^(2m+1).
    rng = random.Random(71)
    terms = random_terms(rng, 2, 4)
    h = pauli_sum_matrix(terms)
    for ks in [[1], [1, 2], [1, 2, 3]]:
        m = len(ks)
        e1 = op_norm(sub(mpf_matrix(terms, 0.1, ks), expm_hermitian(h, 0.1)))
        e2 = op_norm(sub(mpf_matrix(terms, 0.05, ks), expm_hermitian(h, 0.05)))
        assert abs(math.log2(e1 / e2) - (2 * m + 1)) < 0.1, (ks, e1 / e2)


def test_the_example_errors():
    u = expm_hermitian(pauli_sum_matrix(EXAMPLE), 1.0)
    got = [op_norm(sub(mpf_matrix(EXAMPLE, 1.0, ks), u)) for ks in [[1], [1, 2], [1, 2, 3], [1, 2, 3, 4]]]
    want = [0.31367, 0.015944, 0.00046095, 9.0477e-6]
    assert all(abs(g / w - 1) < 1e-4 for g, w in zip(got, want))
    assert abs(op_norm(sub(product_formula(EXAMPLE, 1.0, 2), u)) - 0.071130) < 1e-5


def test_lcu_success_probability():
    rng = random.Random(72)
    psi = random_state(2, rng)
    for ks in [[1, 2], [1, 2, 3]]:
        m = mpf_matrix(EXAMPLE, 1.0, ks)
        good, p, s = mpf_lcu(EXAMPLE, 1.0, ks, psi)
        assert abs(s - sum(abs(c) for c in mpf_coefficients(ks))) < 1e-12
        target = [x / s for x in matvec(m, psi)]
        assert max(abs(x - y) for x, y in zip(good, target)) < 1e-12
        assert abs(p - norm(matvec(m, psi)) ** 2 / s ** 2) < 1e-12
    e0 = [1 + 0j, 0j, 0j, 0j]
    assert abs(mpf_lcu(EXAMPLE, 1.0, [1, 2], e0)[1] - 0.364735) < 1e-6
    assert abs(mpf_lcu(EXAMPLE, 1.0, [1, 2, 3], e0)[1] - 0.101823) < 1e-6


def test_one_round_of_amplification_when_s_is_at_most_two():
    e0 = [1 + 0j, 0j, 0j, 0j]
    m = mpf_matrix(EXAMPLE, 1.0, [1, 2])
    good, p, s = mpf_lcu(EXAMPLE, 1.0, [1, 2], e0, amplify=True)
    a0 = add(scale(1.5, m), scale(-0.5, matmul(m, matmul(dagger(m), m))))
    assert max(abs(x - y) for x, y in zip(good, matvec(a0, e0))) < 1e-12
    assert p > 0.999
