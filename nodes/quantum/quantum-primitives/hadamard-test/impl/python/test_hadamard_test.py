# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hadamard-test/. The authors are listed in prov/N1NJ1H.jsonl.

import cmath
import math
import random

from hadamard_test import (
    expectation,
    hadamard_test_exact,
    hadamard_test_sampled,
    hoeffding_radius,
    shots_for,
)
from qsim import H, S, T, TOL, X, Z, matmul, random_state, random_unitary_2x2


def kron(a, b):
    """a (x) b, with a on the high qubits."""
    return [[a[i // len(b)][j // len(b)] * b[i % len(b)][j % len(b)] for j in range(len(a) * len(b))]
            for i in range(len(a) * len(b))]


def random_unitary_4x4(rng):
    """A product of random one-qubit unitaries and a CNOT, so it is entangling."""
    cnot = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
    u = kron(random_unitary_2x2(rng), random_unitary_2x2(rng))
    return matmul(kron(random_unitary_2x2(rng), random_unitary_2x2(rng)), matmul(cnot, u))


def test_real_and_imaginary_parts_are_exact() -> None:
    rng = random.Random(12)
    cases = [(u, 1) for u in (X, Z, H, S, T)] + [(random_unitary_2x2(rng), 1) for _ in range(10)]
    cases += [(random_unitary_4x4(rng), 2) for _ in range(10)]
    for u, n in cases:
        for _ in range(3):
            psi = random_state(n, rng)
            z = expectation(u, psi)
            assert abs(hadamard_test_exact(u, psi) - z.real) <= TOL
            assert abs(hadamard_test_exact(u, psi, imaginary=True) - z.imag) <= TOL


def test_small_cases_by_hand() -> None:
    zero, one = [1, 0], [0, 1]
    plus = [1 / math.sqrt(2), 1 / math.sqrt(2)]
    assert abs(hadamard_test_exact(X, plus) - 1) <= TOL        # |+> is an eigenvector of X, eigenvalue 1
    assert abs(hadamard_test_exact(X, zero) - 0) <= TOL        # <0|X|0> = 0
    assert abs(hadamard_test_exact(Z, one) + 1) <= TOL         # <1|Z|1> = -1
    assert abs(hadamard_test_exact(S, one, imaginary=True) - 1) <= TOL  # <1|S|1> = i
    assert abs(hadamard_test_exact(T, one) - math.cos(math.pi / 4)) <= TOL


def test_global_phase_of_u_changes_the_answer() -> None:
    rng = random.Random(13)
    u = random_unitary_2x2(rng)
    psi = random_state(1, rng)
    alpha = 0.7
    v = [[cmath.exp(1j * alpha) * a for a in row] for row in u]
    z = expectation(u, psi)
    assert abs(hadamard_test_exact(v, psi) - (cmath.exp(1j * alpha) * z).real) <= TOL
    assert abs(hadamard_test_exact(v, psi) - z.real) > 0.01


def test_swap_test_is_a_hadamard_test() -> None:
    """With U = SWAP on |a>|b> the result is <a|<b| SWAP |a>|b> = |<a|b>|^2."""
    rng = random.Random(14)
    swap = [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
    for _ in range(10):
        a, b = random_state(1, rng), random_state(1, rng)
        psi = [x * y for x in a for y in b]
        overlap = abs(sum(complex(p).conjugate() * q for p, q in zip(a, b))) ** 2
        assert abs(hadamard_test_exact(swap, psi) - overlap) <= TOL


def test_mixed_input_gives_the_normalized_trace() -> None:
    """DQC1: the two system qubits are maximally mixed, here as half of two Bell pairs with two
    reference qubits (qubits 2 and 3). The result is Re Tr(U) / 4."""
    rng = random.Random(15)
    psi = [0j] * 16
    for s in range(4):
        psi[(s << 2) | s] = 0.5  # sum_s |s>_ref |s>_sys / 2
    for _ in range(10):
        u = random_unitary_4x4(rng)
        tr = sum(u[i][i] for i in range(4))
        assert abs(hadamard_test_exact(u, psi, extra=2) - tr.real / 4) <= TOL
        assert abs(hadamard_test_exact(u, psi, imaginary=True, extra=2) - tr.imag / 4) <= TOL


def test_sampled_estimate_is_within_the_hoeffding_radius() -> None:
    """2000 shots each, seed 16. With delta = 1e-6 the radius is about 0.12."""
    rng = random.Random(16)
    shots, delta = 2000, 1e-6
    r = hoeffding_radius(shots, delta)
    assert 0.11 < r < 0.13
    for _ in range(5):
        u = random_unitary_2x2(rng)
        psi = random_state(1, rng)
        z = expectation(u, psi)
        assert abs(hadamard_test_sampled(u, psi, shots, rng) - z.real) <= r
        assert abs(hadamard_test_sampled(u, psi, shots, rng, imaginary=True) - z.imag) <= r


def test_shot_count_formula() -> None:
    for eps in (0.1, 0.01):
        for delta in (0.05, 1e-3):
            n = shots_for(eps, delta)
            assert hoeffding_radius(n, delta) <= eps < hoeffding_radius(n - 1, delta)
    assert shots_for(0.01, 0.05) == 73778
