# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/qubitization/. The authors are listed in prov/8Q7YB1.jsonl.
"""Qubitization: the walk operator W = (2 Pi - I) U of a Hermitian block encoding U.

The a ancilla qubits are the high qubits, so Pi = |0^a><0^a| (x) I is the projector on the first
2^n basis states and the encoded matrix H/alpha is the top-left block of U.
"""

import math

from qsim import eigh, householder, identity, kron, matmul, matvec, pauli_matrix, scale

H2 = [[1 / math.sqrt(2) + 0j, 1 / math.sqrt(2) + 0j], [1 / math.sqrt(2) + 0j, -1 / math.sqrt(2) + 0j]]


def lcu_block_encoding(terms):
    """(U, alpha, a) for H = sum_j c_j P_j: U = PREP SELECT PREP with a Householder PREP, so U = U^dagger."""
    n = len(terms[0][1])
    a = max(1, math.ceil(math.log2(len(terms))))
    lam = sum(abs(c) for c, _ in terms)
    w = [complex(math.sqrt(abs(c) / lam)) for c, _ in terms] + [0j] * ((1 << a) - len(terms))
    prep = kron(householder(w), identity(1 << n))
    d = 1 << (a + n)
    select = [[0j] * d for _ in range(d)]
    for j in range(1 << a):
        block = scale(math.copysign(1, terms[j][0]), pauli_matrix(terms[j][1])) if j < len(terms) else identity(1 << n)
        for r in range(1 << n):
            for c in range(1 << n):
                select[(j << n) + r][(j << n) + c] = block[r][c]
    return matmul(prep, matmul(select, prep)), lam, a


def reflection(a, n):
    """2 Pi - I with Pi = |0^a><0^a| (x) I: +1 on the first 2^n basis states, -1 elsewhere."""
    d = 1 << (a + n)
    return [[(1 if i < (1 << n) else -1) + 0j if i == j else 0j for j in range(d)] for i in range(d)]


def walk_operator(u, a, n):
    """W = (2 Pi - I) U. For a Hermitian U with U^2 = I its eigenphases are +-arccos(lambda/alpha)."""
    return matmul(reflection(a, n), u)


def invariant_plane(u, a, n, vec):
    """For an eigenvector |lambda> of H, the pair |G> = |0^a>|lambda> and |G_perp>, with x = lambda/alpha."""
    g = list(vec) + [0j] * ((1 << (a + n)) - len(vec))  # @line L3
    ug = matvec(u, g)
    x = sum(p.conjugate() * q for p, q in zip(g, ug)).real
    s = math.sqrt(max(0.0, 1 - x * x))
    gp = [(q - x * p) / s for p, q in zip(g, ug)]  # @line L4
    return g, gp, x


def qubitize(u, a, n):
    """The walk operator and, for each eigenvalue lambda of the block, the plane and the two eigenphases."""
    w = walk_operator(u, a, n)  # @line L1
    block = [row[: 1 << n] for row in u[: 1 << n]]
    vals, vecs = eigh(block)  # @line L2
    planes = []
    for k, x in enumerate(vals):
        col = [vecs[i][k] for i in range(1 << n)]
        g, gp, xx = invariant_plane(u, a, n, col)
        theta = math.acos(max(-1.0, min(1.0, xx)))  # @line L5
        planes.append((g, gp, xx, theta))
    return w, planes  # @line L6


def hermitian_encoding(u, a, n):
    """From any block encoding U of a Hermitian H/alpha, the Hermitian one (H (x) I) U' (H (x) I) with
    U' = |0><1| (x) U + |1><0| (x) U^dagger on one more ancilla (the new highest qubit). It has a + 1 ancillas."""
    d = len(u)
    ud = [[u[j][i].conjugate() for j in range(d)] for i in range(d)]
    up = [[0j] * (2 * d) for _ in range(2 * d)]
    for i in range(d):
        for j in range(d):
            up[i][d + j] = u[i][j]
            up[d + i][j] = ud[i][j]
    had = kron(H2, identity(d))
    return matmul(had, matmul(up, had)), a + 1
