# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/qubit/. The authors are listed in prov/YX77AF.jsonl.

import cmath
import math
import random

import pytest

from qsim import inner
from qubit import (
    KET0, KET1, MINUS, PLUS, X_BASIS, Y_BASIS, Z_BASIS, canonical, normalize, probabilities_in_basis, qubit,
    relative_phase, same_physical_state, sample_counts, with_global_phase,
)

TOL = 1e-12


def test_bases_are_orthonormal() -> None:
    for basis in (Z_BASIS, X_BASIS, Y_BASIS):
        for i in range(2):
            for j in range(2):
                assert abs(inner(basis[i], basis[j]) - (1 if i == j else 0)) < TOL


def test_unit_norm_is_required() -> None:
    with pytest.raises(ValueError):
        qubit(1, 1)
    with pytest.raises(ValueError):
        normalize(0, 0)
    s = normalize(1, 1j)
    assert abs(abs(s[0]) ** 2 + abs(s[1]) ** 2 - 1) < TOL


def test_worked_example() -> None:
    # psi = (3/5)|0> + (4i/5)|1>
    psi = qubit(0.6, 0.8j)
    pz = probabilities_in_basis(psi, Z_BASIS)
    px = probabilities_in_basis(psi, X_BASIS)
    py = probabilities_in_basis(psi, Y_BASIS)
    assert abs(pz[0] - 9 / 25) < TOL and abs(pz[1] - 16 / 25) < TOL
    assert abs(px[0] - 1 / 2) < TOL and abs(px[1] - 1 / 2) < TOL
    assert abs(py[0] - 49 / 50) < TOL and abs(py[1] - 1 / 50) < TOL
    assert abs(relative_phase(psi) - math.pi / 2) < TOL


def test_global_phase_changes_no_probability() -> None:
    for k in range(12):
        theta, phi = math.pi * k / 11, 2 * math.pi * k / 7
        psi = qubit(math.cos(theta / 2), cmath.exp(1j * phi) * math.sin(theta / 2))
        for gamma in (0.3, 1.0, math.pi, 5.0):
            chi = with_global_phase(psi, gamma)
            assert same_physical_state(psi, chi)
            for basis in (Z_BASIS, X_BASIS, Y_BASIS):
                p, q = probabilities_in_basis(psi, basis), probabilities_in_basis(chi, basis)
                assert abs(p[0] - q[0]) < TOL and abs(p[1] - q[1]) < TOL
            c1, c2 = canonical(psi), canonical(chi)
            assert abs(c1[0] - c2[0]) < 1e-9 and abs(c1[1] - c2[1]) < 1e-9


def test_relative_phase_is_observable() -> None:
    # |+> and |-> agree in the computational basis and differ in the X basis.
    assert probabilities_in_basis(PLUS, Z_BASIS) == pytest.approx([0.5, 0.5], abs=TOL)
    assert probabilities_in_basis(MINUS, Z_BASIS) == pytest.approx([0.5, 0.5], abs=TOL)
    assert probabilities_in_basis(PLUS, X_BASIS) == pytest.approx([1, 0], abs=TOL)
    assert probabilities_in_basis(MINUS, X_BASIS) == pytest.approx([0, 1], abs=TOL)
    assert not same_physical_state(PLUS, MINUS)
    assert relative_phase(PLUS) == 0 and abs(relative_phase(MINUS) - math.pi) < TOL


def test_basis_states_have_no_relative_phase() -> None:
    for s in (KET0, KET1):
        with pytest.raises(ValueError):
            relative_phase(s)


def test_sampled_frequencies() -> None:
    # 20000 shots with seed 2024. Hoeffding: P(|freq - p| >= 0.02) <= 2 exp(-2 * 20000 * 0.02^2) < 2e-6.
    psi = qubit(0.6, 0.8j)
    counts = sample_counts(psi, 20000, random.Random(2024))
    assert sum(counts) == 20000
    assert abs(counts[0] / 20000 - 0.36) < 0.02
