# SPDX-License-Identifier: MIT
"""Quantum imaginary-time evolution (QITE), simulated with exact state vectors.

The exact flow is |psi(tau)> = e^(-tau H)|psi(0)> / ||e^(-tau H)|psi(0)>||.
QITE (Motta et al. 2020) follows it with unitary steps only: for each term h_m of
H = sum_m h_m, it finds a Hermitian A = sum_I a_I sigma_I, a sum of Pauli strings on a
domain of qubits around the term, such that e^(-i dtau A)|psi> is close to the
normalized e^(-dtau h_m)|psi>, by a linear least-squares problem.
Qubit 0 is the least significant bit and the first letter of a Pauli string acts on
qubit n-1, as in qsim.py. Each term h_m here is one Pauli string with its coefficient.
"""

import math

from qsim import (
    all_pauli_strings,
    apply_pauli,
    inner,
    matrix_function,
    matvec,
    norm,
    normalize,
    pauli_sum_apply,
    pauli_sum_matrix,
    solve_symmetric,
)

Terms = list[tuple[float, str]]


def energy(terms: Terms, psi: list[complex]) -> float:
    return inner(psi, pauli_sum_apply(terms, psi)).real


def variance(terms: Terms, psi: list[complex]) -> float:
    hpsi = pauli_sum_apply(terms, psi)
    return inner(hpsi, hpsi).real - inner(psi, hpsi).real ** 2


def exact_ite(terms: Terms, psi0: list[complex], tau: float) -> list[complex]:
    """The normalized state e^(-tau H)|psi0> / ||e^(-tau H)|psi0>||."""
    g = matrix_function(pauli_sum_matrix(terms), lambda x: math.exp(-tau * x))
    return normalize(matvec(g, psi0))


def term_imaginary_step(c: float, s: str, psi: list[complex], dtau: float) -> list[complex]:
    """e^(-dtau c P)|psi> = cosh(dtau c)|psi> - sinh(dtau c) P|psi>, not normalized."""
    p = apply_pauli(psi, s)
    ch, sh = math.cosh(dtau * c), math.sinh(dtau * c)
    return [ch * a - sh * b for a, b in zip(psi, p)]


def domain_of(s: str, radius: int | None) -> list[int]:
    """The qubits within distance radius of the support of s on a line of qubits 0..n-1.
    radius None means all qubits."""
    n = len(s)
    if radius is None:
        return list(range(n))
    support = [n - 1 - pos for pos, ch in enumerate(s) if ch != "I"]
    return [q for q in range(n) if any(abs(q - t) <= radius for t in support)]


def domain_strings(n: int, domain: list[int]) -> list[str]:
    """All Pauli strings on n qubits that act as the identity outside the domain, without the identity."""
    out = []
    for w in all_pauli_strings(len(domain)):
        if set(w) == {"I"}:
            continue
        s = ["I"] * n
        for k, q in enumerate(sorted(domain, reverse=True)):
            s[n - 1 - q] = w[k]
        out.append("".join(s))
    return out


def _real(v: list[complex]) -> list[float]:
    """The real vector (Re v, Im v), so that the real inner product of two embeddings is Re<v|w>."""
    return [a.real for a in v] + [a.imag for a in v]


def solve_update(psi: list[complex], delta: list[complex], strings: list[str]) -> list[float]:
    """The minimum-norm real a that minimizes || delta - (-i sum_I a_I sigma_I)|psi> ||.

    The normal equations are Re(S) a = b with S_IJ = <psi|sigma_I sigma_J|psi> and
    b_I = Im <delta|sigma_I|psi>. Their minimum-norm solution is a = G^T (G G^T)^+ delta,
    where column I of the real matrix G is the embedding of -i sigma_I|psi>; this form
    solves a system of size 2^(n+1) instead of one of size len(strings).
    """
    cols = [_real([-1j * x for x in apply_pauli(psi, s)]) for s in strings]
    d = len(cols[0])
    gg = [[sum(col[i] * col[j] for col in cols) for j in range(d)] for i in range(d)]
    y = solve_symmetric(gg, _real(delta))
    return [sum(ci * yi for ci, yi in zip(col, y)) for col in cols]


def solve_update_normal_equations(psi: list[complex], delta: list[complex], strings: list[str]) -> list[float]:
    """The same solution from the normal equations Re(S) a = b directly (slow; for tests)."""
    vs = [apply_pauli(psi, s) for s in strings]
    s_re = [[inner(vi, vj).real for vj in vs] for vi in vs]
    b = [inner(delta, v).imag for v in vs]
    return solve_symmetric(s_re, b)


def apply_exp_minus_i(a_terms: Terms, psi: list[complex], dtau: float, tol: float = 1e-17) -> list[complex]:
    """e^(-i dtau A)|psi> for A = sum a_I sigma_I, by the Taylor series of the exponential on the vector."""
    out = list(psi)
    term = list(psi)
    for k in range(1, 200):
        term = [(-1j * dtau / k) * x for x in pauli_sum_apply(a_terms, term)]
        out = [x + y for x, y in zip(out, term)]
        if norm(term) < tol:
            break
    return out


def qite_step(terms: Terms, psi: list[complex], dtau: float, radius: int | None) -> list[complex]:
    """One step of QITE: one unitary for each term, in the order of the list."""
    n = len(terms[0][1])
    for c, s in terms:  # @line L3
        target = term_imaginary_step(c, s, psi, dtau)
        cm = inner(target, target).real  # @line L4
        delta = [(t / math.sqrt(cm) - p) / dtau for t, p in zip(target, psi)]  # @line L5
        strings = domain_strings(n, domain_of(s, radius))  # @line L6
        a = solve_update(psi, delta, strings)  # @line L7
        psi = apply_exp_minus_i(list(zip(a, strings)), psi, dtau)  # @line L8
    return psi


def qite(terms: Terms, psi0: list[complex], dtau: float, steps: int, radius: int | None = None) -> list[list[complex]]:
    """Run QITE for the given number of steps of size dtau. Returns the states after each step
    (the first entry is psi0). radius None uses the whole register as the domain of every term."""
    psi = list(psi0)  # @line L1
    states = [psi]
    for _ in range(steps):  # @line L2
        psi = qite_step(terms, psi, dtau, radius)
        states.append(psi)
    return states  # @line L9


def trotter_ite(terms: Terms, psi0: list[complex], dtau: float, steps: int) -> list[complex]:
    """The normalized product of e^(-dtau h_m) over the terms, repeated: the non-unitary
    target that QITE follows term by term."""
    psi = list(psi0)
    for _ in range(steps):
        for c, s in terms:
            psi = normalize(term_imaginary_step(c, s, psi, dtau))
    return psi
