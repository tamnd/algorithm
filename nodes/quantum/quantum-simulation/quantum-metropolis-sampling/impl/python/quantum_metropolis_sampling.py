# SPDX-License-Identifier: MIT
"""The idealized quantum Metropolis walk, simulated with exact state vectors.

The walk of Temme et al. (2011) moves between eigenvectors |E_i> of a Hamiltonian H.
A step applies a random unitary C from a move set, measures the energy, and accepts
the new eigenvector |E_k> with probability min(1, e^(-beta (E_k - E_i))). On rejection
the walk returns to |E_i>. This file simulates the ideal version: the energy
measurement is exact (a projective measurement in the eigenbasis of H, which needs a
nondegenerate spectrum) and the return on rejection is free (the simulator keeps a copy
of the old state). On a quantum computer the energy comes from phase estimation and
the return needs the rewinding method of Marriott and Watrous.
Qubit 0 is the least significant bit and the first letter of a Pauli string acts on
qubit n-1, as in qsim.py.
"""

import math
import random

from qsim import (
    add,
    column,
    dagger,
    eigh,
    identity,
    inner,
    matvec,
    max_abs_diff,
    outer,
    pauli_matrix,
    sample_index,
    scale,
    zeros,
)

Matrix = list[list[complex]]


def eigenbasis(h: Matrix, gap_tol: float = 1e-6) -> tuple[list[float], list[list[complex]]]:
    """Sorted eigenvalues and eigenvectors of h. Raise ValueError if two eigenvalues are
    closer than gap_tol, because an energy measurement then does not fix the eigenvector."""
    vals, vecs = eigh(h)
    for a, b in zip(vals, vals[1:]):
        if b - a < gap_tol:
            raise ValueError("the spectrum is degenerate: an energy measurement does not select one eigenvector")
    return vals, [column(vecs, k) for k in range(len(vals))]


def gibbs_weights(values: list[float], beta: float) -> list[float]:
    """The Gibbs distribution e^(-beta E_i) / Z on the eigenvalues."""
    e0 = min(values)
    w = [math.exp(-beta * (e - e0)) for e in values]
    z = sum(w)
    return [x / z for x in w]


def density_from_weights(weights: list[float], basis: list[list[complex]]) -> Matrix:
    """sum_i w_i |E_i><E_i|."""
    rho = zeros(len(basis[0]))
    for w, v in zip(weights, basis):
        rho = add(rho, scale(w, outer(v, v)))
    return rho


def pauli_moves(n: int) -> list[Matrix]:
    """X, Y and Z on each qubit. Each one is its own inverse."""
    moves = []
    for q in range(n):
        for p in "XYZ":
            s = ["I"] * n
            s[n - 1 - q] = p
            moves.append(pauli_matrix("".join(s)))
    return moves


def rotation(n: int, string: str, theta: float) -> Matrix:
    """e^(-i theta P / 2) for the Pauli string P."""
    return add(scale(math.cos(theta / 2), identity(1 << n)), scale(-1j * math.sin(theta / 2), pauli_matrix(string)))


def is_balanced(moves: list[Matrix], probs: list[float], tol: float = 1e-12) -> bool:
    """True if for each move C the move C^dagger is in the set with the same probability."""
    for c, p in zip(moves, probs):
        cd = dagger(c)
        if not any(max_abs_diff(cd, c2) < tol and abs(p - p2) < tol for c2, p2 in zip(moves, probs)):
            return False
    return True


def transition_matrix(values, basis, moves, probs, beta) -> list[list[float]]:
    """T[k][i] = the probability that one step takes |E_i> to |E_k>."""
    d = len(values)
    t = [[0.0] * d for _ in range(d)]
    images = [[matvec(c, v) for v in basis] for c in moves]
    for i in range(d):
        for k in range(d):
            if k == i:
                continue
            a = sum(p * abs(inner(basis[k], img[i])) ** 2 for p, img in zip(probs, images))
            t[k][i] = a * min(1.0, math.exp(-beta * (values[k] - values[i])))
        t[i][i] = 1.0 - sum(t[k][i] for k in range(d) if k != i)
    return t


def step(t: list[list[float]], p: list[float]) -> list[float]:
    return [sum(t[k][i] * p[i] for i in range(len(p))) for k in range(len(p))]


def distribution_after(t: list[list[float]], p0: list[float], steps: int) -> list[float]:
    p = list(p0)
    for _ in range(steps):
        p = step(t, p)
    return p


def total_variation(p: list[float], q: list[float]) -> float:
    return 0.5 * sum(abs(a - b) for a, b in zip(p, q))


def spectral_gap(t: list[list[float]], pi: list[float]) -> float:
    """1 minus the second largest eigenvalue modulus of a chain that satisfies detailed
    balance for pi. Uses the symmetric matrix D^(-1/2) T D^(1/2), D = diag(pi)."""
    d = len(pi)
    s = [[complex(t[k][i] * math.sqrt(pi[i] / pi[k])) for i in range(d)] for k in range(d)]
    vals, _ = eigh(s)
    return 1.0 - max(abs(x) for x in vals[:-1])


def quantum_metropolis(values, basis, beta, moves, probs, start: int, steps: int, rng: random.Random):
    """One trajectory of the ideal walk. Returns (index of the final eigenvector, the final
    state, the number of accepted moves)."""
    i = start
    psi = list(basis[i])  # @line L1
    accepted = 0
    for _ in range(steps):  # @line L2
        c = moves[sample_index(probs, rng)]  # @line L3
        phi = matvec(c, psi)  # @line L4
        k = sample_index([abs(inner(v, phi)) ** 2 for v in basis], rng)  # @line L5
        if rng.random() < min(1.0, math.exp(-beta * (values[k] - values[i]))):  # @line L6
            i, psi = k, list(basis[k])
            accepted += 1
        else:
            psi = list(basis[i])  # @line L7
    return i, psi, accepted  # @line L8
