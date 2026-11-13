# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-hamiltonian-simulation/. The authors are listed in prov/WBXH9G.jsonl.
"""Optimal Hamiltonian simulation by quantum signal processing (Low and Chuang 2017), in the eigenvalue
transformation form of Gilyen, Su, Low and Wiebe (2019).

Input: a Hermitian block encoding U of H/alpha (U = U^dagger, U^2 = I) on a ancillas and n system qubits.
1. Jacobi-Anger: cos(tau x) and sin(tau x) with tau = alpha t, truncated to degrees 2R and 2R + 1.
2. QET of kappa cos and kappa sin, kappa = 2 sin(pi/10), as two unitaries Q_c and Q_s.
3. V = an LCU of Q_c and -i Q_s with one more qubit: its block is about sin(pi/10) e^(-iHt).
4. Two rounds of oblivious amplitude amplification turn sin(pi/10) into sin(5 pi/10) = 1.

All ancillas are high qubits; the target is the top-left 2^n block. Qubit 0 is the least significant bit.
"""

import math

from qsim import (
    bessel_j,
    chebyshev_t,
    dagger,
    householder,
    identity,
    kron,
    matmul,
    pauli_matrix,
    qsp_real_phases,
    scale,
)

HAD = [[1 / math.sqrt(2) + 0j, 1 / math.sqrt(2) + 0j], [1 / math.sqrt(2) + 0j, -1 / math.sqrt(2) + 0j]]
KAPPA = 2 * math.sin(math.pi / 10)


def lcu_block_encoding(terms):
    """(U, alpha, a) for H = sum_j c_j P_j: U = PREP SELECT PREP with a Householder PREP, so U = U^dagger, U^2 = I."""
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


def jacobi_anger(tau, big_r):
    """Chebyshev coefficients of cos(tau x) to degree 2R and of sin(tau x) to degree 2R + 1."""
    cos_c = [0.0] * (2 * big_r + 1)
    sin_c = [0.0] * (2 * big_r + 2)
    cos_c[0] = bessel_j(0, tau)
    for k in range(1, big_r + 1):
        cos_c[2 * k] = 2 * (-1) ** k * bessel_j(2 * k, tau)
    for k in range(big_r + 1):
        sin_c[2 * k + 1] = 2 * (-1) ** k * bessel_j(2 * k + 1, tau)
    return cos_c, sin_c


def chebyshev_sum(coeffs):
    return lambda x: sum(c * chebyshev_t(k, x) for k, c in enumerate(coeffs) if c != 0)


def truncation_error(tau, big_r):
    """2 sum_{k > 2R} |J_k(tau)|: a bound on both truncation errors on [-1, 1]."""
    return 2 * sum(abs(bessel_j(k, tau)) for k in range(2 * big_r + 1, 2 * big_r + 60))


def degree_for(tau, eps):
    """The least R whose truncation error is at most eps."""
    big_r = 0
    while truncation_error(tau, big_r) > eps:
        big_r += 1
    return big_r


def _phase_rows(m, phi, k):
    a, b = complex(math.cos(phi), math.sin(phi)), complex(math.cos(phi), -math.sin(phi))
    return [[x * (a if i < k else b) for x in row] for i, row in enumerate(m)]


def _reflection_phases(phases):
    d = len(phases) - 1
    if d == 0:
        return list(phases)
    return [phases[0] - math.pi / 4] + [p - math.pi / 2 for p in phases[1:d]] + [phases[d] - math.pi / 4]


def _phased_sequence(u, k, psi):
    m = _phase_rows(identity(len(u)), psi[-1], k)
    for ph in reversed(psi[:-1]):
        m = _phase_rows(matmul(u, m), ph, k)
    return m


def select_two(a, b):
    """(Had (x) I)(|0><0| (x) A + |1><1| (x) B)(Had (x) I): its top-left block is (A + B)/2 on the top-left blocks."""
    d = len(a)
    sel = [[0j] * (2 * d) for _ in range(2 * d)]
    for i in range(d):
        for j in range(d):
            sel[i][j] = a[i][j]
            sel[d + i][d + j] = b[i][j]
    had = kron(HAD, identity(d))
    return matmul(had, matmul(sel, had))


def qet_real(u, k, f, deg):
    """A unitary with one more qubit whose top-left k x k block is f(H/alpha) (see quantum-eigenvalue-transformation)."""
    phases = qsp_real_phases(f, deg)
    plus = _phased_sequence(u, k, _reflection_phases(phases))
    minus = _phased_sequence(u, k, _reflection_phases([-p for p in phases]))
    return scale(1j ** deg, select_two(plus, minus))


def reflect_rows(m, k):
    """(2 Pi - I) M with Pi the projector on the first k basis states."""
    return [list(row) if i < k else [-x for x in row] for i, row in enumerate(m)]


def simulate(u, alpha, n, t, big_r):
    """A unitary on 2 + a + n qubits whose top-left 2^n block approximates e^(-iHt)."""
    tau = alpha * t  # @line L1
    cos_c, sin_c = jacobi_anger(tau, big_r)  # @line L2
    p_c = chebyshev_sum([KAPPA * c for c in cos_c])  # @line L3
    p_s = chebyshev_sum([KAPPA * c for c in sin_c])
    k = 1 << n
    q_c = qet_real(u, k, p_c, 2 * big_r)  # @line L4
    q_s = qet_real(u, k, p_s, 2 * big_r + 1)
    v = select_two(q_c, scale(-1j, q_s))  # @line L5
    g = v
    for _ in range(2):  # @line L6
        g = scale(-1, matmul(v, reflect_rows(matmul(dagger(v), reflect_rows(g, k)), k)))
    return g  # @line L7


def amplified_block(z):
    """5 Z - 20 Z Z^dagger Z + 16 Z Z^dagger Z Z^dagger Z: the block after two rounds, as a function of the block Z."""
    zz = matmul(z, matmul(dagger(z), z))
    zzz = matmul(zz, matmul(dagger(z), z))
    d = len(z)
    return [[5 * z[i][j] - 20 * zz[i][j] + 16 * zzz[i][j] for j in range(d)] for i in range(d)]


def error_bound(tau, big_r):
    """delta (5 + 60 rho^2 + 80 rho^4) with delta = (kappa/2)(e_c + e_s) and rho = sin(pi/10) + delta."""
    delta = KAPPA * truncation_error(tau, big_r)
    rho = math.sin(math.pi / 10) + delta
    return delta * (5 + 60 * rho ** 2 + 80 * rho ** 4)
