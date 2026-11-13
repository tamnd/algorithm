# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/no-cloning-theorem/. The authors are listed in prov/0245X0.jsonl.

import random
from fractions import Fraction

from no_cloning_theorem import (
    ONE,
    PLUS,
    ZERO,
    bb84_exact_error_rate,
    bb84_round_trip,
    cnot_copier,
    copy_basis_state,
    is_isometry,
    linear_cloner,
)
from qsim import R2, inner, kron_vec, matvec


def test_unitary_cloning_of_zero_and_plus_breaks_the_inner_product() -> None:
    # A unitary U with U|v>|0> = |v>|v> for v in {|0>, |+>} needs <0|+> = <0|+>^2.
    s = inner(ZERO, PLUS)
    assert s == R2(0, Fraction(1, 2))  # 1/sqrt(2)
    assert s * s == R2(Fraction(1, 2))
    assert s != s * s


def test_a_linear_map_clones_two_independent_states_but_is_not_an_isometry() -> None:
    L = linear_cloner(ZERO, PLUS)
    assert matvec(L, ZERO) == kron_vec(ZERO, ZERO)
    assert matvec(L, PLUS) == kron_vec(PLUS, PLUS)
    assert not is_isometry(L)
    # For the orthogonal pair |0>, |1> the cloner is an isometry.
    assert is_isometry(linear_cloner(ZERO, ONE))


def test_no_linear_map_clones_zero_one_and_plus() -> None:
    # L is fixed by L|0> = |00> and L|1> = |11>, so L|+> = (|00> + |11>)/sqrt(2).
    L = linear_cloner(ZERO, ONE)
    image = matvec(L, PLUS)
    h = R2(0, Fraction(1, 2))
    assert image == [h, R2(0), R2(0), h]
    assert image != kron_vec(PLUS, PLUS)  # |++> has all four amplitudes 1/2


def test_cnot_copies_basis_states_only() -> None:
    assert copy_basis_state(0) == [1, 0, 0, 0]
    assert copy_basis_state(1) == [0, 0, 0, 1]
    out = cnot_copier(PLUS)
    assert out != kron_vec(PLUS, PLUS)
    assert inner(out, kron_vec(PLUS, PLUS)) == R2(0, Fraction(1, 2))  # fidelity 1/2


def test_cloning_condition_on_random_pairs() -> None:
    rng = random.Random(3)
    for _ in range(200):
        a = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(2)]
        b = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(2)]
        a = [x / abs(inner(a, a)) ** 0.5 for x in a]
        b = [x / abs(inner(b, b)) ** 0.5 for x in b]
        s = inner(a, b)
        # The inner product of the two would-be outputs differs from the input one.
        assert abs(s - s * s) > 1e-6


def test_bb84_exact_error_rate_is_one_quarter() -> None:
    assert bb84_exact_error_rate() == R2(Fraction(1, 4))


def test_bb84_sampled_error_rates() -> None:
    sifted, errors = bb84_round_trip(4000, random.Random(1), eve=False)
    assert errors == 0
    assert abs(sifted / 4000 - 0.5) < 0.05  # Hoeffding: 2 exp(-2 * 4000 * 0.05^2) < 1e-8
    sifted, errors = bb84_round_trip(40000, random.Random(2), eve=True)
    assert sifted > 19000
    # Hoeffding on at least 19000 sifted rounds: 2 exp(-2 * 19000 * 0.02^2) < 1e-6.
    assert abs(errors / sifted - 0.25) < 0.02
