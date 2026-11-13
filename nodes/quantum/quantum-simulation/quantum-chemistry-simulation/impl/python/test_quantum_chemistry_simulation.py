# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-chemistry-simulation/. The authors are listed in prov/184NCZ.jsonl.

from qsim import add, close, dagger, identity, pauli_on, qop_add, qop_matrix, qop_mul, qop_scale, scale
from quantum_chemistry_simulation import (
    h2_matrix,
    h2_terms,
    hartree_fock_energy,
    nuclear_repulsion,
    sector_energies,
    two_by_two_ci,
)


def test_hamiltonian_is_hermitian():
    m = h2_matrix()
    assert close(m, dagger(m), 1e-12)


def test_ground_state_matches_the_two_by_two_ci():
    m = h2_matrix()
    e = sector_energies(m, 2, 0)
    assert abs(e[0] - two_by_two_ci()) < 1e-9
    assert abs(e[0] - (-1.851046)) < 1e-6
    assert abs(e[0] + nuclear_repulsion() - (-1.137270)) < 1e-6


def test_hartree_fock_and_correlation_energy():
    assert abs(hartree_fock_energy() + nuclear_repulsion() - (-1.116685)) < 1e-6
    corr = two_by_two_ci() - hartree_fock_energy()
    assert abs(corr - (-0.020585)) < 1e-6
    assert abs(corr) > 0.0016  # larger than chemical accuracy, 1 kcal/mol = 1.6 mHa


def test_other_sectors():
    m = h2_matrix()
    # the triplet h_gg + h_uu + J_gu - K appears with 2 S_z = -2, 0 and 2
    trip = -1.252477 - 0.475934 + 0.663472 - 0.181287
    for sz2 in (-2, 0, 2):
        assert any(abs(x - trip) < 1e-9 for x in sector_energies(m, 2, sz2))
    assert abs(sector_energies(m, 1, 1)[0] - (-1.252477)) < 1e-9
    # the global minimum of the Fock space is the two-electron ground state
    assert min(min(sector_energies(m, n, s)) for n, s in ((1, 1), (3, 1), (4, 0))) > sector_energies(m, 2, 0)[0]


def jw(n, j, dg):
    z = {q: "Z" for q in range(j)}
    return {pauli_on(n, {**z, j: "X"}): 0.5, pauli_on(n, {**z, j: "Y"}): (-0.5j if dg else 0.5j)}


def test_qubit_hamiltonian_has_fifteen_pauli_terms():
    q = {}
    for c, w in h2_terms():
        o = {"IIII": 1}
        for j, dg in w:
            o = qop_mul(o, jw(4, j, dg))
        q = qop_add(q, qop_scale(o, c))
    q = qop_add(q, {"IIII": nuclear_repulsion()})
    assert len(q) == 15
    assert abs(q["XXYY"] - (-0.045322)) < 1e-6 and abs(q["IIIZ"] - 0.171201) < 1e-6
    assert close(qop_matrix(q, 4), add(h2_matrix(), scale(nuclear_repulsion(), identity(16))), 1e-12)
