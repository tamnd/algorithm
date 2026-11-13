# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/qdrift/. The authors are listed in prov/D4KBEW.jsonl.
"""qDRIFT (Campbell 2019) for H = sum_j c_j P_j with Pauli strings P_j.

Each of the N steps draws a term j with probability |c_j| / lambda,
lambda = sum_j |c_j|, and applies e^(-i sign(c_j) tau P_j) with
tau = lambda t / N. The average over the random draws is the channel
E(rho) = sum_j p_j U_j rho U_j^dagger applied N times.

A sequence is a list of (string, theta) pairs. The circuit applies
e^(-i theta P) for each pair in list order, the first pair first.
Qubit 0 is the least significant bit of the basis index (see qsim.py).
"""

import math

from qsim import (
    dagger,
    identity,
    mat_add,
    mat_mul,
    mat_scale,
    pauli_matrix,
    pauli_rotation,
    trace_norm_hermitian,
)


def qdrift_sequence(terms, t, big_n, rng):
    """N random Pauli rotations whose average channel approximates e^(-iHt)."""
    weights = [abs(c) for c, _ in terms]
    lam = sum(weights)  # @line L1
    tau = lam * t / big_n  # @line L2
    cumulative = []
    acc = 0.0
    for w in weights:
        acc += w
        cumulative.append(acc)
    seq = []  # @line L3
    for _ in range(big_n):  # @line L4
        u = rng.random() * lam  # @line L5
        j = 0
        while j < len(terms) - 1 and u >= cumulative[j]:
            j += 1
        c, p = terms[j]
        seq.append((p, math.copysign(tau, c)))  # @line L6
    return seq  # @line L7


def apply_sequence(psi, seq):
    for p, th in seq:
        psi = pauli_rotation(psi, p, th)
    return psi


def qdrift_bound(lam, t, big_n):
    """Campbell's bound (2 lambda^2 t^2 / N) e^(2 lambda t / N) on half the diamond norm distance."""
    return 2 * lam * lam * t * t / big_n * math.exp(2 * lam * t / big_n)


def samples_for_error(lam, t, eps):
    """The least N with qdrift_bound(lam, t, N) <= eps; it starts from ceil(2 lambda^2 t^2 / eps)."""
    big_n = max(1, math.ceil(2 * lam * lam * t * t / eps))
    while qdrift_bound(lam, t, big_n) > eps:
        big_n += 1
    while big_n > 1 and qdrift_bound(lam, t, big_n - 1) <= eps:
        big_n -= 1
    return big_n


# ---------------------------------------------------------------- density matrices


def outer(psi):
    return [[a * b.conjugate() for b in psi] for a in psi]


def conjugate(u, rho):
    return mat_mul(mat_mul(u, rho), dagger(u))


def rotation_matrix(p, theta):
    """e^(-i theta P) = cos(theta) I - i sin(theta) P."""
    m = pauli_matrix(p)
    return mat_add(mat_scale(identity(len(m)), math.cos(theta)), m, -1j * math.sin(theta))


def qdrift_channel(terms, t, big_n, rho):
    """The averaged qDRIFT channel, (sum_j p_j U_j . U_j^dagger)^N, applied to rho."""
    lam = sum(abs(c) for c, _ in terms)
    tau = lam * t / big_n
    steps = [(abs(c) / lam, rotation_matrix(p, math.copysign(tau, c))) for c, p in terms]
    steps = [(w, u, dagger(u)) for w, u in steps]
    d = len(rho)
    for _ in range(big_n):
        out = [[0j] * d for _ in range(d)]
        for w, u, ud in steps:
            out = mat_add(out, mat_mul(mat_mul(u, rho), ud), w)
        rho = out
    return rho


def trace_distance(a, b):
    """Half the trace norm of a - b."""
    return 0.5 * trace_norm_hermitian(mat_add(a, b, -1.0))
