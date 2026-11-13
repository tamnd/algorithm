# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ancilla-qubits/. The authors are listed in prov/HZ3JH4.jsonl.

import random

from ancilla_qubits import (
    mcx_dirty,
    mcx_one_ancilla,
    mcx_permutation,
    permutation_parity,
    toffoli_count,
    v_chain,
)
from qsim import (
    H,
    TOL,
    apply_1q,
    apply_permutation,
    basis_state,
    max_abs_diff,
    purity,
    random_state,
    reduced_density_matrix,
    run,
    run_classical,
)


def layout(k: int, extra: int):
    """Wires: controls 0 .. k-1, target k, then the ancillas."""
    controls = list(range(k))
    target = k
    ancillas = list(range(k + 1, k + 1 + extra))
    return controls, target, ancillas


def test_v_chain_on_every_input_with_clean_ancillas() -> None:
    for k in range(1, 7):
        controls, target, anc = layout(k, max(k - 2, 0))
        gates = v_chain(controls, target, anc)
        n = k + 1 + len(anc)
        ref = mcx_permutation(n, controls, target)
        for x in range(1 << (k + 1)):  # every value of the controls and the target, ancillas 0
            assert run_classical(x, gates) == ref[x]
        if k >= 2:
            assert toffoli_count(gates) == 2 * k - 3
            assert len(gates) == 2 * k - 3


def test_v_chain_is_wrong_on_a_dirty_ancilla() -> None:
    controls, target, anc = layout(4, 2)
    gates = v_chain(controls, target, anc)
    ref = mcx_permutation(7, controls, target)
    bad = [x for x in range(1 << 7) if run_classical(x, gates) != ref[x]]
    assert bad, "the V-chain needs clean ancillas"
    # c4 = 1, the other controls 0, and the second ancilla starts at 1: the target is flipped by mistake
    x = (1 << anc[1]) | (1 << 3)
    assert (run_classical(x, gates) >> target) & 1 == 1


def test_dirty_ancillas_on_every_input() -> None:
    for k in range(3, 7):  # k = 6 uses 11 wires, 2048 inputs
        controls, target, anc = layout(k, k - 2)
        gates = mcx_dirty(controls, target, anc)
        n = 2 * k - 1
        ref = mcx_permutation(n, controls, target)
        for x in range(1 << n):  # every value of every wire, ancillas included
            assert run_classical(x, gates) == ref[x]
        assert toffoli_count(gates) == len(gates) == 4 * (k - 2)


def test_one_dirty_ancilla_on_every_input() -> None:
    for k in range(3, 9):  # k = 8 uses 10 wires
        controls, target, (anc,) = layout(k, 1)
        gates = mcx_one_ancilla(controls, target, anc)
        n = k + 2
        ref = mcx_permutation(n, controls, target)
        for x in range(1 << n):
            assert run_classical(x, gates) == ref[x]
        if k >= 5:
            assert toffoli_count(gates) == len(gates) == 8 * (k - 3)


def test_dirty_ancilla_in_a_quantum_state() -> None:
    """The ancillas hold a random state, entangled with everything else. The circuit must act as C^k X
    on the controls and the target and as the identity on the ancillas."""
    rng = random.Random(2026)
    controls, target, anc = layout(4, 2)
    gates = mcx_dirty(controls, target, anc)
    perm = mcx_permutation(7, controls, target)
    for _ in range(5):
        psi = random_state(7, rng)
        assert max_abs_diff([run(psi, gates)], [apply_permutation(psi, perm)]) <= TOL


def test_ancilla_left_dirty_is_entangled() -> None:
    """Controls in superposition. The V-chain returns its ancillas to 0, so the controls and the target
    form a pure state. The first half alone (no uncompute) leaves the ancillas entangled with them."""
    controls, target, anc = layout(3, 1)
    gates = v_chain(controls, target, anc)
    psi = basis_state(5, 0)
    for q in controls:
        psi = apply_1q(psi, H, q)
    keep = controls + [target]
    full = run(psi, gates)
    assert all(abs(full[x]) <= TOL for x in range(32) if (x >> anc[0]) & 1)
    assert abs(purity(reduced_density_matrix(full, keep)) - 1) <= TOL
    half = run(psi, gates[:2])  # compute a = c1 c2 and the Toffoli on the target, no uncompute
    # the ancilla is 1 on 2 of the 8 terms: weights 3/4 and 1/4, purity 9/16 + 1/16 = 5/8
    assert abs(purity(reduced_density_matrix(half, keep)) - 5 / 8) <= TOL


def test_parity_shows_why_ancillas_are_needed() -> None:
    """On n >= 4 wires NOT, CNOT and Toffoli gates are even permutations, but C^(n-1) X on n wires is a
    single transposition, which is odd. So C^3 X on 4 wires needs an ancilla in a circuit of these gates."""
    for n in range(4, 8):
        assert permutation_parity(mcx_permutation(n, [], 0)) == 0
        assert permutation_parity(mcx_permutation(n, [1], 0)) == 0
        assert permutation_parity(mcx_permutation(n, [1, 2], 0)) == 0
        assert permutation_parity(mcx_permutation(n, list(range(1, n)), 0)) == 1
    # with one more wire, C^3 X becomes even and the circuits above build it
    assert permutation_parity(mcx_permutation(5, [0, 1, 2], 3)) == 0
