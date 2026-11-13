# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/no-communication-theorem/. The authors are listed in prov/AMHNNQ.jsonl.

"""Local operations on part B leave the reduced state of part A unchanged.

A state of n qubits is split into A, the high n - k qubits, and B, the low k
qubits. A local operation on B is a list of Kraus operators K (2^k x 2^k
matrices) with sum K^dagger K = I; it acts on the whole state as I_A (x) K.
"""

import math

from qsim import dagger, identity, kron_mat, mat_add, matmul, partial_trace, project_qubit, H, apply_1q


def on_b(K, n, k):
    """The matrix I_A (x) K on n qubits, where K acts on the low k qubits."""
    return kron_mat(identity(1 << (n - k)), K)


def apply_local_channel(rho, n, k, kraus):
    """(id_A (x) Phi)(rho) for the channel Phi on B with the given Kraus operators."""
    out = [[0] * len(rho) for _ in rho]
    for K in kraus:
        E = on_b(K, n, k)
        out = mat_add(out, matmul(matmul(E, rho), dagger(E)))
    return out


def is_trace_preserving(kraus, tol=1e-12):
    d = len(kraus[0])
    total = [[0] * d for _ in range(d)]
    for K in kraus:
        total = mat_add(total, matmul(dagger(K), K))
    return all(abs(total[i][j] - (1 if i == j else 0)) < tol for i in range(d) for j in range(d))


def reduced_a(rho, n, k):
    return partial_trace(rho, n, list(range(k, n)))


def selective_branches(rho, n, k, kraus):
    """For each Kraus operator: (probability, conditional reduced state of A)."""
    out = []
    for K in kraus:
        E = on_b(K, n, k)
        branch = matmul(matmul(E, rho), dagger(E))
        p = sum(branch[i][i] for i in range(len(branch))).real
        if p > 1e-15:
            out.append((p, [[v / p for v in row] for row in reduced_a(branch, n, k)]))
    return out


def bob_frequency_of_one(alice_basis, rounds, rng):
    """Share (|00> + |11>)/sqrt(2); Alice (qubit 1) measures in the Z (0) or X (1) basis,
    then Bob (qubit 0) measures in the Z basis. Returns the fraction of rounds where Bob sees 1."""
    pair = [1 / math.sqrt(2), 0, 0, 1 / math.sqrt(2)]
    ones = 0
    for _ in range(rounds):
        s = apply_1q(pair, H, 1) if alice_basis else pair
        p1, post1 = project_qubit(s, 1, 1)
        s = post1 if rng.random() < p1 else project_qubit(s, 1, 0)[1]
        q1, _ = project_qubit(s, 0, 1)
        ones += rng.random() < q1
    return ones / rounds
