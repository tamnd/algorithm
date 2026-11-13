# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lieb-robinson-bound/. The authors are listed in prov/TYMAXR.jsonl.
"""Measure the spread of a commutator on small spin chains and compare it with the Lieb-Robinson bound.

The chain has sites 0, ..., n - 1 and H = sum_x h_x with h_x on the sites x and x + 1
and ||h_x|| <= J. The bound proved on the page is
  ||[tau_t(A), B]|| <= (4/3) ||A|| ||B|| sum_{k >= d} (6 J t)^k / k!
                     <= (4/3) ||A|| ||B|| exp(-(d - 6 e J t)),
for A on site 0 and B at distance d >= 1, where tau_t(A) = e^(iHt) A e^(-iHt).
"""

import cmath
import math

from qsim import (
    commutator,
    dagger,
    eigh,
    expm_taylor,
    matmul,
    op_norm,
    pauli_on,
    qop_add,
    qop_matrix,
    zeros,
)


def bound_series(d: int, j: float, t: float) -> float:
    """(4/3) sum_{k >= d} (6 J t)^k / k!, for ||A|| = ||B|| = 1."""
    x = 6 * j * abs(t)
    term = x**d / math.factorial(d)
    total = 0.0
    k = d
    while True:
        total += term
        k += 1
        term *= x / k
        if term < 1e-17 * total or term == 0.0:
            break
    return 4.0 / 3.0 * total


def bound_exponential(d: int, j: float, t: float) -> float:
    """(4/3) exp(-(d - v t)) with the velocity v = 6 e J, from sum_{k >= d} x^k / k! <= e^(e x - d)."""
    return 4.0 / 3.0 * math.exp(-(d - 6 * math.e * j * abs(t)))


def chain_hamiltonian(n: int, bond) -> dict:
    """sum over x of bond(n, x), where bond returns a qubit operator on the sites x and x + 1."""
    h: dict = {}
    for x in range(n - 1):
        h = qop_add(h, bond(n, x))
    return h


def xx_bond(j: float):
    """J (sigma+ sigma- + sigma- sigma+) = (J/2)(X X + Y Y), norm J."""
    def bond(n, x):
        return {pauli_on(n, {x: "X", x + 1: "X"}): j / 2, pauli_on(n, {x: "Y", x + 1: "Y"}): j / 2}
    return bond


def heisenberg_bond(j: float):
    """J S_x . S_{x+1} = (J/4)(XX + YY + ZZ), norm 3J/4."""
    def bond(n, x):
        return {pauli_on(n, {x: p, x + 1: p}): j / 4 for p in "XYZ"}
    return bond


def evolve_operator(vals, v, a, t):
    """tau_t(A) = e^(iHt) A e^(-iHt), with H = V diag(vals) V^dagger."""
    d = len(vals)
    vd = dagger(v)
    a_e = matmul(vd, matmul(a, v))  # A in the eigenbasis
    ph = [cmath.exp(1j * lam * t) for lam in vals]
    a_t = [[ph[i] * a_e[i][k] * ph[k].conjugate() for k in range(d)] for i in range(d)]
    return matmul(v, matmul(a_t, vd))


def commutator_norm(n, h_qop, a_qop, b_qop, times):
    """||[tau_t(A), B]|| for every t in times, by exact diagonalization of H."""
    hm = qop_matrix(h_qop, n)
    am = qop_matrix(a_qop, n)
    bm = qop_matrix(b_qop, n)
    vals, v = eigh(hm)
    return [op_norm(commutator(evolve_operator(vals, v, am, t), bm)) for t in times]


def hopping_matrix(n: int, j: float):
    h = zeros(n)
    for x in range(n - 1):
        h[x][x + 1] = h[x + 1][x] = complex(j)
    return h


def free_propagator(n: int, j: float, t: float):
    """e^(-i h t) for the n x n hopping matrix h of the XX chain."""
    h = hopping_matrix(n, j)
    return expm_taylor([[-1j * t * x for x in row] for row in h])


def free_commutator_norms(n: int, j: float, t: float) -> list[float]:
    """||[tau_t(sigma-_0), Z_d]|| = 2 |U_0d(t)| for d = 0, ..., n - 1, by the Jordan-Wigner map."""
    u = free_propagator(n, j, t)
    return [2 * abs(u[0][d]) for d in range(n)]


def bessel_j(m: int, x: float) -> float:
    """J_m(x) for an integer m >= 0, by its power series."""
    term = (x / 2) ** m / math.factorial(m)
    total = term
    k = 0
    while abs(term) > 1e-18 * max(1.0, abs(total)):
        k += 1
        term *= -((x / 2) ** 2) / (k * (k + m))
        total += term
    return total


def semi_infinite_norm(d: int, j: float, t: float) -> float:
    """2 |U_0d(t)| on the half-infinite XX chain: 2 (d + 1) |J_{d+1}(2 J t)| / (J t)."""
    if t == 0:
        return 2.0 if d == 0 else 0.0
    return 2 * (d + 1) * abs(bessel_j(d + 1, 2 * j * t)) / (j * t)


def first_time_above(f, eps: float, step: float, t_max: float = 50.0) -> float | None:
    """The first t >= 0 with f(t) >= eps: a scan with the given step, then 40 bisection steps."""
    t = 0.0
    while t <= t_max:
        if f(t) >= eps:
            lo, hi = max(0.0, t - step), t
            for _ in range(40):
                mid = (lo + hi) / 2
                if f(mid) >= eps:
                    hi = mid
                else:
                    lo = mid
            return hi
        t += step
    return None
