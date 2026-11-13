# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-superposition/. The authors are listed in prov/F1S9BZ.jsonl.

import math
import random
from fractions import Fraction

from qsim import apply_1q, basis_state, close, measure, probabilities
from quantum_superposition import (
    H, X_BASIS, Z_BASIS, classical_path_probability, coefficients, coin_flip_twice, hadamard_path_sum,
    is_superposition, support, uniform_superposition,
)

R = math.sqrt(0.5)
PLUS = [complex(R), complex(R)]
MINUS = [complex(R), complex(-R)]


def test_superposition_depends_on_the_basis() -> None:
    assert is_superposition(PLUS, Z_BASIS) and not is_superposition(PLUS, X_BASIS)
    assert is_superposition([1 + 0j, 0j], X_BASIS) and not is_superposition([1 + 0j, 0j], Z_BASIS)
    assert support(MINUS, X_BASIS) == [1]
    assert close(coefficients([1 + 0j, 0j], X_BASIS), [complex(R), complex(R)])


def test_uniform_superposition() -> None:
    for n in range(1, 9):
        s = uniform_superposition(n)
        assert all(abs(a - 2 ** (-n / 2)) < 1e-12 for a in s)
        assert abs(sum(probabilities(s)) - 1) < 1e-12


def test_classical_randomness_does_not_interfere() -> None:
    assert coin_flip_twice() == [Fraction(1, 2), Fraction(1, 2)]
    for k in range(1, 7):
        for start in (0, 1):
            assert classical_path_probability(k, start, 0) == Fraction(1, 2)


def test_amplitudes_interfere() -> None:
    # H twice on |0> gives |0>: the two paths to |1> have opposite signs and cancel.
    assert hadamard_path_sum(2, 0, 0) == 2 and hadamard_path_sum(2, 0, 1) == 0
    assert close(apply_1q(apply_1q(basis_state(1, 0), H, 0), H, 0), basis_state(1, 0))
    # the integer path sums divided by 2^(k/2) are the entries of H^k
    for k in range(1, 7):
        s = basis_state(1, 0)
        for _ in range(k):
            s = apply_1q(s, H, 0)
        for end in (0, 1):
            assert abs(s[end] - hadamard_path_sum(k, 0, end) / 2 ** (k / 2)) < 1e-12


def test_equal_weights_different_states() -> None:
    # |+> and |-> give the same statistics in the Z basis but not in the X basis.
    assert close(probabilities(PLUS), probabilities(MINUS))
    hp, hm = apply_1q(PLUS, H, 0), apply_1q(MINUS, H, 0)
    assert close(probabilities(hp), [1.0, 0.0]) and close(probabilities(hm), [0.0, 1.0])


def test_measurement_returns_one_outcome() -> None:
    rng = random.Random(31)
    s = uniform_superposition(3)
    counts = [0] * 8
    shots = 16000
    for _ in range(shots):
        x, post = measure(s, rng)
        assert post == basis_state(3, x)
        counts[x] += 1
    # Hoeffding: each frequency is within 0.02 of 1/8 except with probability below 2 * exp(-2 * 16000 * 0.02^2) < 1e-5.
    assert all(abs(c / shots - 1 / 8) < 0.02 for c in counts)
