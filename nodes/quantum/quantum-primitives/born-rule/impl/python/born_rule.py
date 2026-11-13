# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/born-rule/. The authors are listed in prov/K1PK1V.jsonl.
"""The Born rule: p(m) = <psi|P_m|psi>, and in a basis p(k) = |<e_k|psi>|^2.

States are lists of 2**n complex amplitudes; qubit 0 is the least significant bit of the index.
"""

import random
from fractions import Fraction

from qsim import TOL, inner, matvec, measure, norm

Vector = list[complex]
Matrix = list[list[complex]]


def check_state(state: Vector) -> None:
    if abs(norm(state) - 1) > TOL:
        raise ValueError("the Born rule needs a unit vector")


def prob_basis(state: Vector, basis: list[Vector]) -> list[float]:
    """|<e_k|psi>|^2 for an orthonormal basis e_0, e_1, ..."""
    check_state(state)
    return [abs(inner(e, state)) ** 2 for e in basis]


def projector_onto(vectors: list[Vector]) -> Matrix:
    """P = sum_k |v_k><v_k| for orthonormal vectors v_k: the projector onto their span."""
    d = len(vectors[0])
    return [[sum(v[i] * v[j].conjugate() for v in vectors) for j in range(d)] for i in range(d)]


def prob_projector(state: Vector, p: Matrix) -> float:
    """<psi|P|psi>, the probability of the outcome whose projector is P."""
    check_state(state)
    return inner(state, matvec(p, state)).real


def expectation(state: Vector, a: Matrix) -> float:
    """<psi|A|psi> for a Hermitian A: the mean of the eigenvalues of A, weighted by the Born rule."""
    check_state(state)
    return inner(state, matvec(a, state)).real


def marginal(state: Vector, qubits: list[int]) -> list[float]:
    """The distribution of the values of the listed qubits. Outcome index y has bit i equal to the value of qubits[i]."""
    check_state(state)
    out = [0.0] * (1 << len(qubits))
    for x, a in enumerate(state):
        y = sum(((x >> q) & 1) << i for i, q in enumerate(qubits))
        out[y] += a.real * a.real + a.imag * a.imag
    return out


def exact_probabilities(amps: list[tuple[Fraction, Fraction]]) -> list[Fraction]:
    """Exact |re + i im|^2 for amplitudes with rational parts. Raises ValueError unless they sum to 1."""
    p = [re * re + im * im for re, im in amps]
    if sum(p) != 1:
        raise ValueError("the squared magnitudes must sum to 1")
    return p


def sample_counts(state: Vector, shots: int, rng: random.Random) -> list[int]:
    """Counts of each outcome x over the given number of measurements of fresh copies of the state."""
    check_state(state)
    counts = [0] * len(state)
    for _ in range(shots):
        x, _ = measure(state, rng)
        counts[x] += 1
    return counts
