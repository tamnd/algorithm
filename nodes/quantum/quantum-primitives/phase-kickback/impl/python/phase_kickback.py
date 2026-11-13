# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-kickback/. The authors are listed in prov/2ZD3YZ.jsonl.
"""Phase kickback: a controlled unitary acting on an eigenvector of U puts the eigenvalue on the control.

Layout: the target register is qubits 0 .. t-1 and the control is qubit t (the high qubit), so the
state |c>|u> has the basis index c * 2**t + u. Qubit 0 is the least significant bit (see qsim.py).
"""

import cmath

from qsim import H, X, apply_1q, apply_matrix, prob_qubit


def kron_vec(a, b):
    """|a> (x) |b>, with a on the high qubits."""
    return [x * y for x in a for y in b]


def eigen_2x2(u):
    """The eigenvalues and unit eigenvectors of a 2 x 2 matrix with two distinct eigenvalues."""
    a, b, c, d = u[0][0], u[0][1], u[1][0], u[1][1]
    tr, det = a + d, a * d - b * c
    disc = cmath.sqrt(tr * tr - 4 * det)
    out = []
    for lam in ((tr + disc) / 2, (tr - disc) / 2):
        v = [b, lam - a] if abs(b) + abs(lam - a) > 1e-12 else [lam - d, c]
        s = (abs(v[0]) ** 2 + abs(v[1]) ** 2) ** 0.5
        out.append((lam, [v[0] / s, v[1] / s]))
    return out


def kickback(u, target, control):
    """The template. target is an eigenvector of u, control is a one-qubit state (alpha, beta).
    Returns the joint state after the controlled-u gate."""
    t = len(target).bit_length() - 1
    state = list(target)  # @line L1
    state = kron_vec(control, state)  # @line L2
    return apply_matrix(state, u, list(range(t)), [t])  # @line L3


def control_after_kickback(u, target, control, eigenvalue):
    """What L4 of the template says: the control becomes (alpha, e^(i phi) beta) and the target is unchanged."""
    return kron_vec([control[0], eigenvalue * control[1]], target)  # @line L4


def readout_one_bit(state, t: int) -> float:
    """H on the control, then the probability that it reads 1."""
    return prob_qubit(apply_1q(state, H, t), t, 1)  # @line L5


def bit_oracle_matrix(f):
    """U_f on |x>|y> for one input bit and one output bit; x is the high qubit."""
    m = [[0j] * 4 for _ in range(4)]
    for x in range(2):
        for y in range(2):
            m[(x << 1) | (y ^ f[x])][(x << 1) | y] = 1
    return m


def deutsch(f) -> int:
    """Deutsch's algorithm with one query: returns f(0) xor f(1)."""
    s = 2 ** -0.5
    state = kron_vec([s, s], [s, -s])  # |+>|->
    state = apply_matrix(state, bit_oracle_matrix(f), [0, 1])
    return 1 if readout_one_bit(state, 1) > 0.5 else 0


def cnot_on(control, target):
    """CNOT with control qubit 1 (high) and target qubit 0 on |control>|target>."""
    return apply_matrix(kron_vec(control, target), X, [0], [1])
