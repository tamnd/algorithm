# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/higher-order-trotter-suzuki/. The authors are listed in prov/KW8GH0.jsonl.

import math
import random

from higher_order_trotter_suzuki import (
    bacs_best_order,
    bacs_error_bound,
    bacs_steps,
    exponential_count,
    stage_weights,
    suzuki_p,
    suzuki_sequence,
    sequence_unitary,
)
from qsim import (
    all_pauli_strings,
    expm_hermitian,
    expm_taylor,
    identity,
    is_unitary,
    mat_add,
    mat_mul,
    mat_scale,
    max_abs_diff,
    op_norm,
    pauli_matrix,
    pauli_sum_matrix,
)

CHAIN = [(1.0, "ZZ"), (0.8, "XI"), (0.8, "IX")]


def error(terms, t, r, order):
    n = len(terms[0][1])
    u = sequence_unitary(suzuki_sequence(terms, t, r, order), n)
    return op_norm(mat_add(u, expm_hermitian(pauli_sum_matrix(terms), t), -1.0))


def test_coefficients():
    assert abs(suzuki_p(2) - 1 / (4 - 4 ** (1 / 3))) < 1e-15
    assert abs(suzuki_p(2) - 0.41449077179437573) < 1e-15
    assert abs((1 - 4 * suzuki_p(2)) + 0.6579630871775028) < 1e-15
    for order in (2, 4, 6, 8):
        w = stage_weights(order)
        assert len(w) == 5 ** (order // 2 - 1)
        assert abs(sum(w) - 1.0) < 1e-13
        assert w == w[::-1]  # palindrome, so the formula is symmetric
        for m in range(3, order, 2):  # order conditions sum w^m = 0 for odd m < order
            assert abs(sum(x ** m for x in w)) < 1e-12
        if order >= 4:
            assert min(w) < 0  # a backward step


def test_order_two_is_strang():
    terms = CHAIN
    seq = suzuki_sequence(terms, 0.7, 3, 2)
    assert seq[0] == ("ZZ", 1.0 * 0.7 / 3 / 2)
    assert len(seq) == exponential_count(3, 2, 3)


def test_exponential_counts():
    for order in (2, 4, 6):
        for r in (1, 2, 3):
            assert len(suzuki_sequence(CHAIN, 1.0, r, order)) == exponential_count(3, order, r)
            assert len(suzuki_sequence(CHAIN, 1.0, r, order, merge=False)) == (2 * 3 - 1) * 5 ** (order // 2 - 1) * r


def test_symmetric():
    # S(t) S(-t) = I for each symmetric formula
    for order in (2, 4, 6):
        a = sequence_unitary(suzuki_sequence(CHAIN, 0.6, 1, order), 2)
        b = sequence_unitary(suzuki_sequence(CHAIN, -0.6, 1, order), 2)
        assert max_abs_diff(mat_mul(a, b), identity(4)) < 1e-12
        assert is_unitary(a, 1e-12)


def test_observed_order_by_halving_the_step():
    for order, want, tol in ((2, 4.0, 0.05), (4, 16.0, 0.05), (6, 64.0, 0.05)):
        e1 = error(CHAIN, 1.0, 8, order)
        e2 = error(CHAIN, 1.0, 16, order)
        assert abs(e1 / e2 - want) < tol * want
        assert e2 > 1e-12


def test_exact_references_agree():
    h = pauli_sum_matrix([(0.5, "XYZ"), (-0.3, "ZZI"), (0.9, "IXX"), (0.2, "YII")])
    assert max_abs_diff(expm_hermitian(h, 1.3), expm_taylor(mat_scale(h, -1.3j))) < 1e-12


def test_commuting_terms_exact():
    terms = [(0.4, "ZZI"), (-1.3, "IZZ"), (0.9, "ZIZ")]
    for order in (4, 6):
        assert error(terms, 3.0, 1, order) < 1e-12


def test_bacs_bound_holds():
    rng = random.Random(42)
    strings = [s for s in all_pauli_strings(2) if s != "II"]
    for _ in range(10):
        chosen = rng.sample(strings, 3)
        terms = [(rng.uniform(-1, 1), s) for s in chosen]
        lam = max(op_norm(pauli_sum_matrix(terms)), max(abs(c) for c, _ in terms))
        t = rng.uniform(0.1, 1.0)
        for order in (2, 4):
            for r in (50, 200, 1000):
                b = bacs_error_bound(3, lam, t, r, order)
                if b is not None:
                    assert error(terms, t, r, order) <= b


def test_bacs_steps_reach_the_error():
    terms = CHAIN
    lam = max(op_norm(pauli_sum_matrix(terms)), 1.0)
    for order, eps in ((2, 1e-2), (4, 1e-3)):
        r = bacs_steps(3, lam, 0.5, eps, order)
        b = bacs_error_bound(3, lam, 0.5, r, order)
        assert b is not None and b <= eps
        assert error(terms, 0.5, r, order) <= eps


def test_best_order_grows_slowly():
    ks = [bacs_best_order(10, 1.0, t, 1e-6) for t in (10.0, 1e3, 1e6)]
    assert ks == sorted(ks)
    assert bacs_best_order(10, 1.0, 1e3, 1e-6) == 2 * round(0.5 * math.sqrt(math.log(1e10, 5)) + 1)


def test_higher_order_is_not_always_cheaper():
    # At a loose error target, order 2 needs fewer exponentials than order 4 here.
    eps = 0.05
    count = {}
    for order in (2, 4):
        r = 1
        while error(CHAIN, 0.5, r, order) > eps:
            r += 1
        count[order] = exponential_count(3, order, r)
    assert count[2] < count[4]
