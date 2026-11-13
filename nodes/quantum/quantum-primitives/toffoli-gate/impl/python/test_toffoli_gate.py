# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/toffoli-gate/. The authors are listed in prov/8SZNQR.jsonl.

import itertools

from qsim import H, I2, X, Y, Z, basis_state, is_unitary, matmul, run, run_classical, unitary_of, apply_1q
from toffoli_gate import (
    and_gate,
    clifford_t_toffoli,
    fanout_gate,
    gate_counts,
    global_phase_free_equal,
    nand_gate,
    not_gate,
    permutation_sign,
    proportional,
    toffoli,
    toffoli_bits,
    toffoli_permutation,
    two_qubit_toffoli,
)

# Controls on qubits 2 and 1, target on qubit 0, so the ket |a b c> has index 4a + 2b + c.
A, B, C = 2, 1, 0


def toffoli_matrix():
    return unitary_of(3, lambda v: toffoli(v, A, B, C))


def test_truth_table_on_every_input() -> None:
    for a, b, c in itertools.product((0, 1), repeat=3):
        assert toffoli_bits(a, b, c) == (a, b, c ^ (a & b))
        x = 4 * a + 2 * b + c
        out = toffoli(basis_state(3, x), A, B, C)
        y = 4 * a + 2 * b + (c ^ (a & b))
        assert abs(out[y] - 1) < 1e-12 and sum(abs(v) for v in out) - 1 < 1e-12


def test_matrix_swaps_only_110_and_111() -> None:
    u = toffoli_matrix()
    for r in range(8):
        for col in range(8):
            want = 1 if (r == col and r < 6) or {r, col} == {6, 7} else 0
            assert abs(u[r][col] - want) < 1e-12


def test_self_inverse_and_unitary() -> None:
    u = toffoli_matrix()
    assert is_unitary(u)
    uu = matmul(u, u)
    assert all(abs(uu[i][j] - (1 if i == j else 0)) < 1e-12 for i in range(8) for j in range(8))


def test_clifford_t_decomposition_is_exact() -> None:
    gates = clifford_t_toffoli(A, B, C)
    w = unitary_of(3, lambda v: run(v, gates))
    assert global_phase_free_equal(w, toffoli_matrix())
    counts = gate_counts(gates)
    assert counts["cx"] == 6
    assert counts.get("t", 0) + counts.get("tdg", 0) == 7
    assert counts["h"] == 2 and len(gates) == 15


def test_decomposition_for_every_wire_assignment() -> None:
    for c1, c2, t in itertools.permutations(range(3)):
        gates = clifford_t_toffoli(c1, c2, t)
        w = unitary_of(3, lambda v: run(v, gates))
        u = unitary_of(3, lambda v: toffoli(v, c1, c2, t))
        assert global_phase_free_equal(w, u)


def test_two_qubit_construction_is_exact() -> None:
    w = unitary_of(3, lambda v: two_qubit_toffoli(v, A, B, C))
    assert global_phase_free_equal(w, toffoli_matrix())


def test_classical_gates_from_toffoli() -> None:
    for a, b in itertools.product((0, 1), repeat=2):
        assert and_gate(a, b) == (a, b, a & b)
        assert nand_gate(a, b) == (a, b, 1 - (a & b))
    for c in (0, 1):
        assert not_gate(c) == (1, 1, 1 - c)
        assert fanout_gate(c) == (c, 1, c)


def test_parity_of_toffoli_on_n_wires() -> None:
    # On 3 wires the Toffoli gate is one transposition (odd); on n >= 4 wires it is 2**(n-3) of them (even).
    assert permutation_sign(toffoli_permutation(3)) == -1
    for n in range(4, 8):
        assert permutation_sign(toffoli_permutation(n)) == 1


def test_cnot_and_not_circuits_are_affine_so_they_cannot_make_and() -> None:
    # Every circuit of up to 4 gates from NOT and CNOT on 3 wires computes an affine map over GF(2).
    gates = [("x", q) for q in range(3)] + [("cx", c, t) for c in range(3) for t in range(3) if c != t]
    for k in range(5):
        for circ in itertools.product(gates, repeat=k):
            f = [run_classical(x, circ) for x in range(8)]
            base = f[0]
            for x in range(8):
                for y in range(8):
                    assert f[x ^ y] ^ base == (f[x] ^ base) ^ (f[y] ^ base)
    # The Toffoli map is not affine: f(110) xor f(000) != (f(100) xor f(000)) xor (f(010) xor f(000)).
    tof = toffoli_permutation(3, 1, 2, 0)
    assert tof[6] ^ tof[0] != (tof[4] ^ tof[0]) ^ (tof[2] ^ tof[0])


def kron(*ms):
    out = [[1]]
    for m in ms:
        out = [[a * b for a in ra for b in rb] for ra in out for rb in m]
    return out


def test_toffoli_is_not_clifford() -> None:
    # Toffoli X_a Toffoli = X_a CNOT(b -> c). It is not a Pauli string up to phase, so Toffoli is not Clifford.
    u = toffoli_matrix()
    xa = unitary_of(3, lambda v: apply_1q(v, X, A))
    conj = matmul(matmul(u, xa), u)
    paulis = [I2, X, Y, Z]
    for p in itertools.product(paulis, repeat=3):
        assert not proportional(conj, kron(*p))


def test_ccz_is_toffoli_conjugated_by_hadamard() -> None:
    u = unitary_of(3, lambda v: apply_1q(toffoli(apply_1q(v, H, C), A, B, C), H, C))
    for r in range(8):
        for col in range(8):
            want = (-1 if r == 7 else 1) if r == col else 0
            assert abs(u[r][col] - want) < 1e-12
