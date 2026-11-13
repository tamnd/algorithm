# SPDX-License-Identifier: MIT
"""Data for Hamiltonian learning from Gibbs states, simulated with density matrices.

A learner of H = sum_a c_a P_a from Gibbs states rho = e^(-beta H)/Z usually starts from
estimates of the local expectation values Tr(P rho). This file computes Gibbs states,
estimates Pauli expectation values with classical shadows from random single-qubit Pauli
measurements (Huang, Kueng and Preskill 2020) combined by median of means, and gives the
number of snapshots of their theorem. It also has two small identifiability facts: for one
qubit, h = -artanh(<Z>)/beta, and at high temperature c_a = -Tr(P_a rho)/beta + O(beta)
for traceless H made of distinct Pauli strings.
Qubit 0 is the least significant bit and the first letter of a Pauli string acts on
qubit n-1, as in qsim.py.
"""

import math
import random
import statistics

from qsim import (
    dagger,
    identity,
    kron,
    matmul,
    matrix_function,
    pauli_matrix,
    pauli_sum_matrix,
    sample_index,
    scale,
    trace,
)

Matrix = list[list[complex]]
Terms = list[tuple[float, str]]

_S = 1 / math.sqrt(2)
# Measuring P in the Z basis after the rotation U_P: U_X = Hadamard, U_Y = Hadamard S^dagger.
ROTATION = {
    "X": [[_S + 0j, _S + 0j], [_S + 0j, -_S + 0j]],
    "Y": [[_S + 0j, -1j * _S], [_S + 0j, 1j * _S]],
    "Z": [[1 + 0j, 0j], [0j, 1 + 0j]],
}


def gibbs_state(terms: Terms, beta: float) -> Matrix:
    h = pauli_sum_matrix(terms)
    vals = [h[i][i].real for i in range(len(h))]
    shift = min(vals) - sum(abs(c) for c, _ in terms)  # keeps the exponentials bounded
    e = matrix_function(h, lambda x: math.exp(-beta * (x - shift)))
    return scale(1 / trace(e).real, e)


def pauli_expectation(rho: Matrix, s: str) -> float:
    return trace(matmul(pauli_matrix(s), rho)).real


def all_bases(n: int) -> list[str]:
    out = [""]
    for _ in range(n):
        out = [w + c for w in out for c in "XYZ"]
    return out


def basis_distribution(rho: Matrix, basis: str) -> list[float]:
    """Outcome probabilities when every qubit is measured in the Pauli basis given by its letter."""
    u = [[1 + 0j]]
    for ch in basis:
        u = kron(u, ROTATION[ch])
    r = matmul(matmul(u, rho), dagger(u))
    return [max(0.0, r[x][x].real) for x in range(len(r))]


def snapshots(rho: Matrix, count: int, rng: random.Random) -> list[tuple[str, int]]:
    """count independent random-Pauli-basis measurements of copies of rho."""
    n = len(rho).bit_length() - 1
    bases = all_bases(n)
    dist = {b: basis_distribution(rho, b) for b in bases}
    out = []
    for _ in range(count):
        b = bases[rng.randrange(len(bases))]
        out.append((b, sample_index(dist[b], rng)))
    return out


def single_estimate(s: str, basis: str, outcome: int) -> float:
    """The shadow estimate of Tr(P rho) from one snapshot: prod over the support of P of
    3 (-1)^bit if the measured letter matches, and 0 if any letter does not match."""
    n = len(s)
    v = 1.0
    for pos, ch in enumerate(s):
        if ch == "I":
            continue
        if basis[pos] != ch:
            return 0.0
        v *= -3.0 if (outcome >> (n - 1 - pos)) & 1 else 3.0
    return v


def median_of_means(values: list[float], batches: int) -> float:
    size = len(values) // batches
    return statistics.median(sum(values[j * size:(j + 1) * size]) / size for j in range(batches))


def shadow_sample_size(m: int, k: int, eps: float, delta: float) -> tuple[int, int]:
    """(K, N) of Huang-Kueng-Preskill for M Pauli observables of weight at most k:
    K = 2 ln(2M/delta) batches of N = 34 * 3^k / eps^2 snapshots."""
    return math.ceil(2 * math.log(2 * m / delta)), math.ceil(34 * 3**k / eps**2)


def shadow_estimates(rho: Matrix, strings: list[str], eps: float, delta: float, rng: random.Random) -> list[float]:
    k = max(sum(ch != "I" for ch in s) for s in strings)
    batches, size = shadow_sample_size(len(strings), k, eps, delta)
    snaps = snapshots(rho, batches * size, rng)
    return [median_of_means([single_estimate(s, b, x) for b, x in snaps], batches) for s in strings]


def field_from_z(z: float, beta: float) -> float:
    """For H = h Z on one qubit, <Z> = -tanh(beta h), so h = -artanh(<Z>)/beta."""
    return -math.atanh(z) / beta


def high_temperature_coefficients(rho: Matrix, strings: list[str], beta: float) -> list[float]:
    """First-order estimates c_a = -Tr(P_a rho)/beta, from rho = (I - beta H)/2^n + O(beta^2)."""
    return [-pauli_expectation(rho, s) / beta for s in strings]
