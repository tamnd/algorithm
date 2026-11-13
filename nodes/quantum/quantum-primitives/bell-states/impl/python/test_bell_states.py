# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bell-states/. The authors are listed in prov/7ZRWP7.jsonl.

import random
from fractions import Fraction

from bell_states import NAMES, bell_basis_coefficients, bell_formula, bell_measure_circuit, bell_state
from qsim import R2, X, Y, Z, apply_1q, basis_state, inner, kron_mat, matvec, max_abs_diff, outer, partial_trace, random_unitary_1q

LABELS = list(NAMES)
TOL = 1e-12


def test_circuit_gives_the_closed_form_exactly() -> None:
    for x, y in LABELS:
        assert bell_state(x, y, exact=True) == bell_formula(x, y)


def test_orthonormal_exactly() -> None:
    for a in LABELS:
        for b in LABELS:
            assert inner(bell_formula(*a), bell_formula(*b)) == (1 if a == b else 0)


def test_complete_basis_exactly() -> None:
    total = [[R2(0)] * 4 for _ in range(4)]
    for xy in LABELS:
        b = bell_formula(*xy)
        total = [[t + e for t, e in zip(rt, re)] for rt, re in zip(total, outer(b, b))]
    assert total == [[1 if i == j else 0 for j in range(4)] for i in range(4)]


def test_each_half_is_maximally_mixed_exactly() -> None:
    half = Fraction(1, 2)
    for xy in LABELS:
        b = bell_formula(*xy)
        rho = outer(b, b)
        for keep in ([0], [1]):
            assert partial_trace(rho, 2, keep) == [[half, 0], [0, half]]


def test_not_a_product_state() -> None:
    # c00 c11 - c01 c10 = 0 exactly for product states; here it is +-1/2.
    for xy in LABELS:
        c = bell_formula(*xy)
        det = c[0] * c[3] - c[1] * c[2]
        assert det in (R2(Fraction(1, 2)), R2(Fraction(-1, 2)))


def test_bell_measurement_reads_the_label() -> None:
    for x, y in LABELS:
        out = bell_measure_circuit(bell_state(x, y))
        assert max_abs_diff(out, basis_state(2, 2 * x + y)) < TOL


def test_local_paulis_on_one_half_permute_the_basis() -> None:
    for x, y in LABELS:
        s = bell_formula(0, 0)
        if y:
            s = apply_1q(s, X, 1)
        if x:
            s = apply_1q(s, Z, 1)
        assert s == bell_formula(x, y)


def test_pauli_correlations() -> None:
    expected = {(0, 0): (1, 1, -1), (1, 0): (1, -1, 1), (0, 1): (-1, 1, 1), (1, 1): (-1, -1, -1)}
    for xy, (zz, xx, yy) in expected.items():
        b = bell_state(*xy)
        got = [inner(b, matvec(kron_mat(P, P), b)).real for P in (Z, X, Y)]
        assert max_abs_diff(got, [zz, xx, yy]) < TOL


def test_transpose_trick_and_singlet_invariance() -> None:
    rng = random.Random(7)
    phi = bell_state(0, 0)
    psi_minus = bell_state(1, 1)
    for _ in range(50):
        A = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(2)] for _ in range(2)]
        At = [[A[0][0], A[1][0]], [A[0][1], A[1][1]]]
        assert max_abs_diff(apply_1q(phi, A, 1), apply_1q(phi, At, 0)) < TOL
        U = random_unitary_1q(rng)
        det = U[0][0] * U[1][1] - U[0][1] * U[1][0]
        both = apply_1q(apply_1q(psi_minus, U, 1), U, 0)
        assert max_abs_diff(both, [det * a for a in psi_minus]) < TOL


def test_coefficients_of_a_product_state() -> None:
    s = [1, 0, 0, 0]  # |00> = (Phi+ + Phi-)/sqrt(2)
    c = bell_basis_coefficients(s)
    assert max_abs_diff([c[k] for k in LABELS], [2 ** -0.5, 0, 2 ** -0.5, 0]) < TOL
