# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-eigenvalue-transformation/. The authors are listed in prov/6TMH0A.jsonl.
"""The quantum eigenvalue transformation: P(H/alpha) from a Hermitian block encoding of H/alpha.

The ancillas are the high qubits; the encoded matrix is the top-left block. Pi = |0^a><0^a| (x) I.
The control qubits added here (for the real part and for mixed parity) are again the highest qubits.
"""

import math

from qsim import householder, identity, kron, matmul, pauli_matrix, qsp_real_phases, scale

HAD = [[1 / math.sqrt(2) + 0j, 1 / math.sqrt(2) + 0j], [1 / math.sqrt(2) + 0j, -1 / math.sqrt(2) + 0j]]


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


def phase_rows(m, phi, k):
    """e^(i phi (2 Pi - I)) M: multiply the first k rows by e^(i phi) and the other rows by e^(-i phi)."""
    a, b = complex(math.cos(phi), math.sin(phi)), complex(math.cos(phi), -math.sin(phi))
    return [[x * (a if i < k else b) for x in row] for i, row in enumerate(m)]


def reflection_phases(phases):
    """Convert QSP phases of the W(x) convention to the reflection convention (see quantum-signal-processing)."""
    d = len(phases) - 1
    if d == 0:
        return list(phases)
    return [phases[0] - math.pi / 4] + [p - math.pi / 2 for p in phases[1:d]] + [phases[d] - math.pi / 4]


def phased_sequence(u, k, psi):
    """e^(i psi_0 (2Pi - I)) U e^(i psi_1 (2Pi - I)) U ... U e^(i psi_d (2Pi - I)), with k = 2^n rows in Pi.

    On each invariant plane of qubitization this is e^(i psi_0 Z) R(x) ... R(x) e^(i psi_d Z), so its block is
    (-i)^d P(H/alpha) where P is the QSP polynomial of the W(x) phases."""
    d = len(u)
    m = phase_rows(identity(d), psi[-1], k)
    for ph in reversed(psi[:-1]):
        m = phase_rows(matmul(u, m), ph, k)
    return m


def qet_real(u, a, n, f, deg):
    """A unitary on 1 + a + n qubits whose top-left 2^n block is f(H/alpha), for real f of parity deg mod 2, |f| < 1."""
    phases = qsp_real_phases(f, deg)  # @line L1
    k = 1 << n
    plus = phased_sequence(u, k, reflection_phases(phases))  # @line L2
    minus = phased_sequence(u, k, reflection_phases([-p for p in phases]))  # @line L3
    d = len(u)
    sel = [[0j] * (2 * d) for _ in range(2 * d)]
    for i in range(d):
        for j in range(d):
            sel[i][j] = plus[i][j]
            sel[d + i][d + j] = minus[i][j]
    had = kron(HAD, identity(d))
    out = matmul(had, matmul(sel, had))  # @line L4
    return scale(1j ** deg, out)  # @line L5


def even_part(f):
    return lambda x: f(x) + f(-x)


def odd_part(f):
    return lambda x: f(x) - f(-x)


def qet_any_parity(u, a, n, f, deg):
    """f of no fixed parity with |f| <= 1/2 (Theorem 56 of Gilyen, Su, Low and Wiebe): mix the even and odd parts.

    Returns a unitary on 2 + a + n qubits whose top-left 2^n block is (f_even + f_odd)/2 = f(H/alpha)."""
    de = deg if deg % 2 == 0 else deg - 1
    do = deg if deg % 2 == 1 else deg - 1
    ue = qet_real(u, a, n, even_part(f), de)
    uo = qet_real(u, a, n, odd_part(f), do)
    d = len(ue)
    sel = [[0j] * (2 * d) for _ in range(2 * d)]
    for i in range(d):
        for j in range(d):
            sel[i][j] = ue[i][j]
            sel[d + i][d + j] = uo[i][j]
    had = kron(HAD, identity(d))
    return matmul(had, matmul(sel, had))
