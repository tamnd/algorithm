# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trotter-suzuki-product-formulas/. The authors are listed in prov/B7XF2R.jsonl.

import math
import random

from qsim import (
    all_pauli_strings,
    dagger,
    eigh,
    expm_hermitian,
    expm_taylor,
    identity,
    is_unitary,
    mat_add,
    mat_mul,
    mat_scale,
    max_abs_diff,
    op_norm,
    pauli_decompose,
    pauli_matrix,
    pauli_sum_apply,
    pauli_sum_matrix,
    random_state,
    trace,
    vec_dist,
)
from trotter_suzuki_product_formulas import (
    apply_sequence,
    error_bound,
    first_order_constant,
    first_order_pair_constant,
    second_order_constant,
    sequence_unitary,
    steps_for_error,
    trotter_sequence,
    trotterize,
)

TOL = 1e-9


def random_terms(rng, n, big_l):
    strings = [s for s in all_pauli_strings(n) if set(s) != {"I"}]
    chosen = rng.sample(strings, big_l)
    return [(rng.uniform(-1, 1), s) for s in chosen]


def exact(terms, t):
    return expm_hermitian(pauli_sum_matrix(terms), t)


def trotter_error(terms, t, r, order):
    n = len(terms[0][1])
    u = sequence_unitary(trotter_sequence(terms, t, r, order), n)
    return op_norm(mat_add(u, exact(terms, t), -1.0))


def test_hand_example_one_step():
    # H = X + Z, one first order step: e^(-iZt) e^(-iXt) applied X first.
    t = 0.3
    terms = [(1.0, "X"), (1.0, "Z")]
    u = sequence_unitary(trotter_sequence(terms, t, 1, 1), 1)
    c, s = math.cos(t), math.sin(t)
    # e^(-iZt) e^(-iXt) = c^2 I - i s c (X + Z) - i s^2 Y
    want = mat_add(mat_add(mat_scale(identity(2), c * c), mat_scale(mat_add(pauli_matrix("X"), pauli_matrix("Z")), -1j * s * c)), mat_scale(pauli_matrix("Y"), -1j * s * s))
    assert max_abs_diff(u, want) < 1e-12
    ex = exact(terms, t)
    want_ex = mat_add(mat_scale(identity(2), math.cos(math.sqrt(2) * t)), mat_scale(mat_add(pauli_matrix("X"), pauli_matrix("Z")), -1j * math.sin(math.sqrt(2) * t) / math.sqrt(2)))
    assert max_abs_diff(ex, want_ex) < 1e-12


def test_two_exact_exponentials_agree():
    rng = random.Random(11)
    for n in (1, 2, 3, 4, 5):
        terms = random_terms(rng, n, min(4 ** n - 1, 6))
        h = pauli_sum_matrix(terms)
        t = rng.uniform(0.2, 2.0)
        a = expm_hermitian(h, t)
        b = expm_taylor(mat_scale(h, -1j * t))
        assert max_abs_diff(a, b) < 1e-11
        assert is_unitary(a, 1e-11)


def test_eigh_reconstructs():
    rng = random.Random(5)
    for n in (1, 2, 3):
        h = pauli_sum_matrix(random_terms(rng, n, min(4 ** n - 1, 5)))
        vals, v = eigh(h)
        d = len(h)
        rebuilt = [[sum(v[i][k] * vals[k] * v[j][k].conjugate() for k in range(d)) for j in range(d)] for i in range(d)]
        assert max_abs_diff(rebuilt, h) < 1e-12
        assert max_abs_diff(mat_mul(dagger(v), v), identity(d)) < 1e-12


def test_six_qubit_state_against_taylor_on_vector():
    rng = random.Random(6)
    n = 6
    terms = [(1.0, "I" * i + "ZZ" + "I" * (n - i - 2)) for i in range(n - 1)]
    terms += [(0.7, "I" * i + "X" + "I" * (n - i - 1)) for i in range(n)]
    psi = random_state(n, rng)
    t = 1.0
    # reference: (sum_k (-iHt/m)^k / k!)^m psi, with m = 20 and 30 terms
    m = 20
    ref = psi
    for _ in range(m):
        term, acc = ref, ref
        for k in range(1, 30):
            term = [(-1j * t / m / k) * z for z in pauli_sum_apply(terms, term)]
            acc = [a + b for a, b in zip(acc, term)]
        ref = acc
    # first order: the error is below the pairwise commutator bound
    err1 = vec_dist(apply_sequence(psi, trotter_sequence(terms, t, 64, 1)), ref)
    assert 1e-6 < err1 <= t * t / (2 * 64) * first_order_pair_constant(terms)
    # second order: halving the step divides the error by about 4
    e8 = vec_dist(apply_sequence(psi, trotter_sequence(terms, t, 8, 2)), ref)
    e16 = vec_dist(apply_sequence(psi, trotter_sequence(terms, t, 16, 2)), ref)
    assert abs(e8 / e16 - 4.0) < 0.4
    assert e16 < err1


def test_sequence_is_unitary():
    rng = random.Random(3)
    terms = random_terms(rng, 3, 5)
    for order in (1, 2):
        u = sequence_unitary(trotter_sequence(terms, 0.9, 3, order), 3)
        assert is_unitary(u, 1e-12)


def test_bounds_hold_on_random_pauli_sums():
    rng = random.Random(2024)
    for _ in range(25):
        n = rng.choice((1, 2, 3))
        big_l = rng.randint(2, min(4 ** n - 1, 6))
        terms = random_terms(rng, n, big_l)
        t = rng.uniform(0.1, 2.0)
        r = rng.randint(1, 6)
        a1 = first_order_constant(terms)
        assert a1 <= first_order_pair_constant(terms) + 1e-12
        for order in (1, 2):
            err = trotter_error(terms, t, r, order)
            assert err <= error_bound(terms, t, r, order) + 1e-12


def test_bounds_hold_on_four_qubits():
    rng = random.Random(77)
    terms = random_terms(rng, 4, 6)
    for order in (1, 2):
        err = trotter_error(terms, 1.0, 4, order)
        assert err <= error_bound(terms, 1.0, 4, order) + 1e-12


def test_observed_order_by_halving_the_step():
    terms = [(1.0, "ZZ"), (0.8, "XI"), (0.8, "IX")]
    t = 1.0
    for order, want in ((1, 2.0), (2, 4.0)):
        e1 = trotter_error(terms, t, 32, order)
        e2 = trotter_error(terms, t, 64, order)
        assert abs(e1 / e2 - want) < 0.05 * want


def test_commuting_terms_have_zero_error():
    terms = [(0.4, "ZZI"), (-1.3, "IZZ"), (0.9, "ZIZ"), (0.2, "ZII")]
    assert first_order_constant(terms) == 0.0
    for order in (1, 2):
        assert trotter_error(terms, 2.5, 1, order) < 1e-12


def test_gate_counts():
    terms = [(1.0, "ZZ"), (0.5, "XI"), (0.5, "IX")]
    for r in (1, 2, 5):
        assert len(trotter_sequence(terms, 1.0, r, 1)) == 3 * r
        assert len(trotter_sequence(terms, 1.0, r, 2)) == 2 * (3 - 1) * r + 1
        assert len(trotter_sequence(terms, 1.0, r, 2, merge=False)) == (2 * 3 - 1) * r


def test_steps_for_error_is_least():
    rng = random.Random(9)
    terms = random_terms(rng, 2, 4)
    for order in (1, 2):
        for eps in (1e-1, 1e-2, 1e-3):
            r = steps_for_error(terms, 1.5, eps, order)
            assert error_bound(terms, 1.5, r, order) <= eps
            assert r == 1 or error_bound(terms, 1.5, r - 1, order) > eps
            rr, seq = trotterize(terms, 1.5, eps, order)
            assert rr == r
            u = sequence_unitary(seq, 2)
            assert op_norm(mat_add(u, exact(terms, 1.5), -1.0)) <= eps


def test_second_order_constant_matches_two_term_formula():
    # For H = A + B: || [B, [B, A]] || / 12 + || [A, [A, B]] || / 24.
    terms = [(1.0, "X"), (0.5, "Z")]
    # [Z,[Z,X]] = 4X, [X,[X,Z]] = 4Z
    want = (0.25 * 4) / 12 + (0.5 * 4) / 24
    assert abs(second_order_constant(terms) - want) < 1e-12


def test_pauli_decomposition_on_every_input():
    rng = random.Random(1)
    for n in (1, 2, 3):
        d = 1 << n
        for _ in range(4):
            m = [[complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(d)] for _ in range(d)]
            coeffs = pauli_decompose(m)
            assert len(coeffs) <= 4 ** n
            rebuilt = [[0j] * d for _ in range(d)]
            for s, c in coeffs.items():
                rebuilt = mat_add(rebuilt, pauli_matrix(s), c)
            assert max_abs_diff(rebuilt, m) < 1e-12
            for s in all_pauli_strings(n):
                direct = trace(mat_mul(pauli_matrix(s), m)) / d
                assert abs(coeffs.get(s, 0) - direct) < 1e-12
            herm = mat_scale(mat_add(m, dagger(m)), 0.5)
            for c in pauli_decompose(herm).values():
                assert abs(c.imag) < 1e-12
        terms = random_terms(rng, n, min(4 ** n - 1, 5))
        back = pauli_decompose(pauli_sum_matrix(terms), tol=1e-12)
        assert len(back) == len(terms)
        for c, s in terms:
            assert abs(back[s] - c) < 1e-12


def test_swap_decomposition():
    swap = [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
    coeffs = pauli_decompose(swap, tol=1e-12)
    assert coeffs.keys() == {"II", "XX", "YY", "ZZ"}
    assert all(abs(c - 0.5) < 1e-12 for c in coeffs.values())
