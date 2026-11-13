# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-many-body-simulation/. The authors are listed in prov/TMRF7Z.jsonl.

import math

from qsim import close, eigvalsh, qop_matrix
from quantum_many_body_simulation import (
    ground_energy,
    heisenberg,
    hubbard_dimer_spectrum,
    transverse_field_ising,
)


def test_hubbard_dimer_closed_form():
    t = 1.0
    for u in (0.0, 1.0, 4.0, 8.0):
        r = math.sqrt(u * u + 16 * t * t)
        assert close(hubbard_dimer_spectrum(t, u), [(u - r) / 2, 0.0, u, (u + r) / 2], 1e-9)


def test_hubbard_dimer_strong_coupling_limit():
    # E0 = -4 t^2 / U + O(t^4 / U^3): the singlet of the Heisenberg exchange J = 4 t^2 / U
    t, u = 1.0, 8.0
    e0 = hubbard_dimer_spectrum(t, u)[0]
    assert abs(e0 - (-0.472136)) < 1e-6
    assert abs(e0 - (-4 * t * t / u)) < 16 * t**4 / u**3


def test_heisenberg_two_spins_and_four_spin_ring():
    assert close(eigvalsh(qop_matrix(heisenberg(2, 1.0, periodic=False), 2)), [-0.75, 0.25, 0.25, 0.25])
    # the ring of 4: H = (J/2)(S^2 - S_A^2 - S_B^2), so E0 = -2J, then -J three times
    e = eigvalsh(qop_matrix(heisenberg(4, 1.0), 4))
    assert close(e[:4], [-2.0, -1.0, -1.0, -1.0])
    assert abs(ground_energy(heisenberg(6, 1.0), 6) - (-(2 + math.sqrt(13)) / 2)) < 1e-9


def test_transverse_field_ising_free_fermion_formula():
    # periodic chain: E0 = -sum_k sqrt(J^2 + g^2 - 2 J g cos k), k = pi (2m - 1) / n
    n, j = 4, 1.0
    for g in (0.3, 1.0, 2.5):
        ks = [math.pi * (2 * m - 1) / n for m in range(1, n + 1)]
        exact = -sum(math.sqrt(j * j + g * g - 2 * j * g * math.cos(k)) for k in ks)
        assert abs(ground_energy(transverse_field_ising(n, j, g), n) - exact) < 1e-9
    assert abs(ground_energy(transverse_field_ising(4, 1.0, 1.0), 4) - (-5.226252)) < 1e-6
    # two open sites: E0 = -sqrt(J^2 + 4 g^2)
    assert abs(ground_energy(transverse_field_ising(2, 1.0, 0.5, periodic=False), 2) + math.sqrt(2)) < 1e-9
