# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-state-tomography/. The authors are listed in prov/JWVX4D.jsonl.
"""Pauli tomography of n qubits: sampling, linear inversion, projection and maximum likelihood.

A Pauli label is a string over "IXYZ" of length n whose character q acts on
qubit q (qubit 0 is the least significant bit, see qsim.py). A setting is a
string over "XYZ": each qubit is measured in that Pauli basis. The label with
every I replaced by Z is the setting that estimates it, so 3^n settings
estimate all 4^n expectations.
"""

import itertools
import math
import random
from typing import Dict, List, Sequence

from qsim import H, I2, S_DAG, X, Y, Z, Matrix, add, apply_1q, apply_to_density, dagger, eigh, identity
from qsim import kron, matmul, scale, trace, zeros

PAULI = {"I": I2, "X": X, "Y": Y, "Z": Z}
# Rotate each basis to the Z basis: H for X, H S^dagger for Y, nothing for Z.
ROTATION = {"X": H, "Y": matmul(H, S_DAG), "Z": I2}


def pauli_matrix(label: str) -> Matrix:
    """Tensor product with qubit n-1 on the left (the high-order part)."""
    m: Matrix = [[1]]
    for ch in reversed(label):
        m = kron(m, PAULI[ch])
    return m


def all_labels(n: int) -> List[str]:
    return ["".join(t) for t in itertools.product("IXYZ", repeat=n)]


def setting_for(label: str) -> str:
    return label.replace("I", "Z")


def outcome_probabilities(rho: Matrix, setting: str) -> List[float]:
    """Born probabilities of the basis outcomes after rotating each qubit to the Z basis."""

    def rotate(v):
        for q, ch in enumerate(setting):
            v = apply_1q(v, ROTATION[ch], q)
        return v

    rotated = apply_to_density(rho, rotate)
    return [max(0.0, rotated[i][i].real) for i in range(len(rho))]


def sample_counts(rho: Matrix, setting: str, shots: int, rng: random.Random) -> List[int]:
    """Measure `shots` fresh copies of rho in the setting and count each outcome."""
    probs = outcome_probabilities(rho, setting)
    counts = [0] * len(probs)
    for i in rng.choices(range(len(probs)), weights=probs, k=shots):
        counts[i] += 1
    return counts


def expectation_from_counts(label: str, counts: Sequence[int]) -> float:
    """Average of the product of (-1)^bit over the qubits where the label is not I."""
    mask = sum(1 << q for q, ch in enumerate(label) if ch != "I")
    total = sum(counts)
    return sum(c * (-1) ** bin(i & mask).count("1") for i, c in enumerate(counts)) / total


def measure_all(rho: Matrix, n: int, shots: int, rng: random.Random) -> Dict[str, List[int]]:
    """Counts for each of the 3^n settings, with `shots` copies per setting."""
    return {"".join(s): sample_counts(rho, "".join(s), shots, rng) for s in itertools.product("XYZ", repeat=n)}


def linear_inversion(expectations: Dict[str, float], n: int) -> Matrix:
    """rho = 2^-n sum_P <P> P. The result is Hermitian with trace 1, but it can have negative eigenvalues."""
    d = 2**n
    rho = zeros(d)
    for label, e in expectations.items():
        rho = add(rho, scale(e / d, pauli_matrix(label)))
    return rho


def estimate_expectations(data: Dict[str, List[int]], n: int) -> Dict[str, float]:
    out = {"I" * n: 1.0}
    for label in all_labels(n):
        if label != "I" * n:
            out[label] = expectation_from_counts(label, data[setting_for(label)])
    return out


def project_to_density(a: Matrix) -> Matrix:
    """The closest density matrix in Frobenius norm to a Hermitian matrix of trace 1.

    Smolin, Gambetta and Smith (2012): keep the eigenvectors, and move the
    eigenvalues to the closest probability vector, by setting the most negative
    ones to 0 and spreading their total over the others.
    """
    vals, vecs = eigh(a)
    d = len(a)
    mu = list(reversed(vals))  # descending
    acc = 0.0
    i = d
    while i > 0 and mu[i - 1] + acc / i < 0:
        acc += mu[i - 1]
        mu[i - 1] = 0.0
        i -= 1
    for j in range(i):
        mu[j] += acc / i
    lam = list(reversed(mu))
    return [[sum(vecs[r][k] * lam[k] * vecs[c][k].conjugate() for k in range(d)) for c in range(d)] for r in range(d)]


def maximum_likelihood(data: Dict[str, List[int]], n: int, iterations: int = 300) -> Matrix:
    """Hradil's R rho R iteration for the counts of all settings, from rho = I / d."""
    d = 2**n
    projectors = []  # (frequency, projector) for each setting and outcome
    total = sum(sum(c) for c in data.values())
    for setting, counts in data.items():
        for i, c in enumerate(counts):
            basis = [1 if k == i else 0 for k in range(d)]
            v = basis
            for q in range(n - 1, -1, -1):  # undo the rotation: v = U^dagger |i>
                v = apply_1q(v, dagger(ROTATION[setting[q]]), q)
            projectors.append((c / total, [[a * b.conjugate() for b in v] for a in v]))
    rho = scale(1 / d, identity(d))
    for _ in range(iterations):
        r = zeros(d)
        for f, proj in projectors:
            if f > 0:
                p = trace(matmul(proj, rho)).real
                r = add(r, scale(f / p, proj))
        rho = matmul(matmul(r, rho), r)
        rho = scale(1 / trace(rho).real, rho)
    return rho


def log_likelihood(data: Dict[str, List[int]], rho: Matrix) -> float:
    total = 0.0
    for setting, counts in data.items():
        probs = outcome_probabilities(rho, setting)
        total += sum(c * math.log(max(p, 1e-300)) for c, p in zip(counts, probs) if c)
    return total


def hoeffding_radius(shots: int, delta: float) -> float:
    """t with P(|mean - E| >= t) <= delta for the mean of `shots` independent values in [-1, 1]."""
    return math.sqrt(2 * math.log(2 / delta) / shots)
