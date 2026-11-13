# SPDX-License-Identifier: MIT
"""Density matrix exponentiation (Lloyd, Mohseni and Rebentrost 2014), simulated with density matrices.

Given copies of an m-qubit state rho, the technique applies e^(-i rho t) to a target state
sigma. One step takes a fresh copy of rho, applies e^(-i S delta) to the copy and the target,
where S is the SWAP of the two registers, and discards the copy. The target becomes
cos^2(delta) sigma + sin^2(delta) rho - i sin(delta) cos(delta) [rho, sigma],
which is e^(-i rho delta) sigma e^(i rho delta) up to O(delta^2). Then n steps with
delta = t/n give e^(-i rho t) up to O(t^2/n).
In the joint matrices the target is on the low m qubits and the copy on the high m qubits.
"""

import math
import random

from qsim import (
    add,
    commutator,
    dagger,
    expm_taylor,
    identity,
    kron,
    matmul,
    outer,
    partial_trace,
    scale,
    trace,
    trace_distance,
)

Matrix = list[list[complex]]


def swap_matrix(m: int) -> Matrix:
    """The SWAP of two m-qubit registers: |a>|b> -> |b>|a>, with |a> on the high qubits."""
    d = 1 << m
    s = [[0j] * (d * d) for _ in range(d * d)]
    for a in range(d):
        for b in range(d):
            s[b * d + a][a * d + b] = 1 + 0j
    return s


def partial_swap(m: int, delta: float) -> Matrix:
    """e^(-i delta S) = cos(delta) I - i sin(delta) S, since S^2 = I."""
    d = 1 << (2 * m)
    return add(scale(math.cos(delta), identity(d)), scale(-1j * math.sin(delta), swap_matrix(m)))


def dme_step(rho: Matrix, sigma: Matrix, delta: float) -> Matrix:
    """One step: Tr_copy[ e^(-i delta S) (rho (x) sigma) e^(i delta S) ]."""
    m = len(rho).bit_length() - 1
    joint = kron(rho, sigma)  # @line L3
    u = partial_swap(m, delta)
    joint = matmul(matmul(u, joint), dagger(u))  # @line L4
    return partial_trace(joint, list(range(m)))  # @line L5


def step_formula(rho: Matrix, sigma: Matrix, delta: float) -> Matrix:
    """The closed form of one step."""
    c, s = math.cos(delta), math.sin(delta)
    return add(add(scale(c * c, sigma), scale(s * s, rho)), scale(-1j * s * c, commutator(rho, sigma)))


def dme(rho: Matrix, sigma: Matrix, t: float, copies: int) -> Matrix:
    """Approximate e^(-i rho t) sigma e^(i rho t) with the given number of copies of rho."""
    delta = t / copies  # @line L1
    for _ in range(copies):  # @line L2
        sigma = dme_step(rho, sigma, delta)
    return sigma  # @line L6


def exact_evolution(rho: Matrix, sigma: Matrix, t: float) -> Matrix:
    u = expm_taylor(scale(-1j * t, rho))
    return matmul(matmul(u, sigma), dagger(u))


def random_state(m: int, rng: random.Random) -> list[complex]:
    v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(1 << m)]
    s = math.sqrt(sum(abs(x) ** 2 for x in v))
    return [x / s for x in v]


def random_density(m: int, rank: int, rng: random.Random) -> Matrix:
    """A random mixture of rank pure states with random weights."""
    w = [rng.random() + 0.1 for _ in range(rank)]
    z = sum(w)
    d = 1 << m
    rho = [[0j] * d for _ in range(d)]
    for wi in w:
        v = random_state(m, rng)
        rho = add(rho, scale(wi / z, outer(v, v)))
    return rho


def error(rho: Matrix, sigma: Matrix, t: float, copies: int) -> float:
    """Trace distance between the DME output and the exact evolution."""
    return trace_distance(dme(rho, sigma, t, copies), exact_evolution(rho, sigma, t))


def is_density(a: Matrix, tol: float = 1e-10) -> bool:
    if abs(trace(a) - 1) > tol:
        return False
    return all(abs(a[i][j] - a[j][i].conjugate()) < tol for i in range(len(a)) for j in range(len(a)))
