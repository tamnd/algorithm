# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/no-cloning-theorem/. The authors are listed in prov/0245X0.jsonl.

"""Small exact checks around the no-cloning theorem, and BB84 under an intercept-resend attack.

States are lists of amplitudes; with exact numbers (the class R2 of qsim) the
checks are exact. Qubit 1 is the left symbol of a ket.
"""

from fractions import Fraction

from qsim import H, H_EXACT, R2, apply_1q, apply_cnot, basis_state, dagger, kron_vec, matmul, project_qubit

ZERO = [R2(1), R2(0)]
ONE = [R2(0), R2(1)]
PLUS = [R2(0, Fraction(1, 2)), R2(0, Fraction(1, 2))]


def cnot_copier(psi):
    """Run CNOT from the input qubit (qubit 1) to a blank qubit (qubit 0) in |0>."""
    return apply_cnot(kron_vec(psi, [1, 0]), 1, 0)


def linear_cloner(psi, phi):
    """The 4 x 2 matrix L with L psi = psi (x) psi and L phi = phi (x) phi.

    It exists when psi and phi are linearly independent: L = [psi psi, phi phi] M^(-1)
    with M = [psi phi]. Linearity alone does not forbid it; unitarity does.
    """
    m00, m01, m10, m11 = psi[0], phi[0], psi[1], phi[1]
    det = m00 * m11 - m01 * m10
    inv = [[m11 / det, -m01 / det], [-m10 / det, m00 / det]]
    pp, ff = kron_vec(psi, psi), kron_vec(phi, phi)
    targets = [[pp[i], ff[i]] for i in range(4)]
    return matmul(targets, inv)


def is_isometry(L):
    """True when L^dagger L = I exactly (use exact entries)."""
    G = matmul(dagger(L), L)
    return all(G[i][j] == (1 if i == j else 0) for i in range(len(G)) for j in range(len(G)))


def bb84_exact_error_rate():
    """The exact error rate on the sifted key under intercept-resend in a random basis.

    Sums over Alice's bit and basis, Eve's basis and outcome, and Bob's outcome,
    keeping only the rounds where Alice and Bob chose the same basis.
    """
    err = R2(0)
    sifted = R2(0)
    for bit in (0, 1):
        for basis in (0, 1):
            sent = _prepare(bit, basis, exact=True)
            for eve_basis in (0, 1):
                for e, p_e in _outcomes(sent, eve_basis):
                    resent = _prepare(e, eve_basis, exact=True)
                    for b, p_b in _outcomes(resent, basis):
                        w = Fraction(1, 8) * p_e * p_b  # bit, basis and Eve's basis are uniform
                        sifted = sifted + w
                        if b != bit:
                            err = err + w
    return err / sifted


def _prepare(bit, basis, exact=False):
    s = [R2(1 - bit), R2(bit)] if exact else [1 - bit, bit]
    if basis:
        s = apply_1q(s, H_EXACT if exact else H, 0)
    return s


def _outcomes(state, basis):
    """(outcome, probability) for a measurement of one qubit in the Z (0) or X (1) basis."""
    s = apply_1q(state, H_EXACT, 0) if basis else state
    return [(k, s[k] * s[k]) for k in (0, 1)]  # real amplitudes, so |a|^2 = a * a


def _measure(state, basis, rng):
    s = apply_1q(state, H, 0) if basis else state
    p1, _ = project_qubit(s, 0, 1)
    return 1 if rng.random() < p1 else 0


def bb84_round_trip(n, rng, eve=False):
    """Send n BB84 qubits. Returns (sifted length, errors in the sifted key).

    Alice draws a bit and a basis (0 = Z, 1 = X). Eve, if present, measures in a
    random basis and resends the state she saw. Bob measures in a random basis.
    The sifted key keeps the rounds where Alice's and Bob's bases agree.
    """
    sifted = errors = 0
    for _ in range(n):
        bit, basis = rng.randrange(2), rng.randrange(2)
        state = _prepare(bit, basis)
        if eve:
            eb = rng.randrange(2)
            state = _prepare(_measure(state, eb, rng), eb)
        bob_basis = rng.randrange(2)
        got = _measure(state, bob_basis, rng)
        if bob_basis == basis:
            sifted += 1
            errors += got != bit
    return sifted, errors


def copy_basis_state(bit):
    """Orthogonal states can be copied: |b>|0> -> |b>|b> by one CNOT."""
    return cnot_copier(basis_state(1, bit))
