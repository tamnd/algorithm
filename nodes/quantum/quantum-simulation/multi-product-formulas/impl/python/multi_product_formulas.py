# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-product-formulas/. The authors are listed in prov/M9S5CZ.jsonl.
"""Multi-product formulas: M(t) = sum_q C_q S2(t/k_q)^(k_q) with the symmetric second order formula S2.

The coefficients come from Lagrange interpolation in x = k^(-2): C_q = prod_{p != q} k_q^2 / (k_q^2 - k_p^2).
They cancel the error terms of S2 of orders t^3, t^5, ..., so M has error O(t^(2m+1)) for m step numbers.
The quantum circuit is a linear combination of unitaries with the weights |C_q| and the unitaries
sign(C_q) S2(t/k_q)^(k_q). The index register is on the high qubits. Qubit 0 is the least significant bit.
"""

import math

from qsim import add, householder, identity, matmul, matvec, norm, pauli_matrix, scale


def pauli_exp(c, s, theta):
    """e^(-i theta c P) = cos(theta c) I - i sin(theta c) P for a Pauli string P."""
    p = pauli_matrix(s)
    d = len(p)
    a, b = math.cos(theta * c), math.sin(theta * c)
    return [[(a if i == j else 0) - 1j * b * p[i][j] for j in range(d)] for i in range(d)]


def strang(terms, t):
    """S2(t) = e^(-i A_1 t/2) ... e^(-i A_L t/2) e^(-i A_L t/2) ... e^(-i A_1 t/2), the symmetric formula."""
    d = 1 << len(terms[0][1])
    half = [pauli_exp(c, s, t / 2) for c, s in terms]
    m = identity(d)
    for u in half + half[::-1]:
        m = matmul(u, m)
    return m


def product_formula(terms, t, k):
    """S2(t/k)^k: k steps of the symmetric formula."""
    step = strang(terms, t / k)
    m = identity(len(step))
    for _ in range(k):
        m = matmul(step, m)
    return m


def mpf_coefficients(ks):
    """C_q = prod_{p != q} k_q^2 / (k_q^2 - k_p^2). Then sum_q C_q = 1 and sum_q C_q k_q^(-2j) = 0 for 1 <= j < m."""
    out = []
    for q, kq in enumerate(ks):
        c = 1.0
        for p, kp in enumerate(ks):
            if p != q:
                c *= kq * kq / (kq * kq - kp * kp)
        out.append(c)
    return out


def mpf_matrix(terms, t, ks):
    """M(t) = sum_q C_q S2(t/k_q)^(k_q) as a matrix."""
    d = 1 << len(terms[0][1])
    m = [[0j] * d for _ in range(d)]
    for c, k in zip(mpf_coefficients(ks), ks):
        m = add(m, scale(c, product_formula(terms, t, k)))
    return m


def _index_matrix(b, parts):
    out = []
    for row in b:
        v = [0j] * len(parts[0])
        for bij, pj in zip(row, parts):
            if bij != 0:
                for x, y in enumerate(pj):
                    v[x] += bij * y
        out.append(v)
    return out


def _w(b, unitaries, parts, inverse=False):
    parts = _index_matrix(b, parts)
    sel = []
    for j, p in enumerate(parts):
        if j < len(unitaries):
            u = unitaries[j]
            if inverse:
                u = [[u[k][i].conjugate() for k in range(len(u))] for i in range(len(u))]
            sel.append(matvec(u, p))
        else:
            sel.append(list(p))
    return _index_matrix(b, sel)


def _reflect(parts):
    return [list(parts[0])] + [[-x for x in p] for p in parts[1:]]


def mpf_lcu(terms, t, ks, psi, amplify=False):
    """Apply M(t) to psi with a linear combination of unitaries.

    Returns the index-0 part of the final state, its squared norm (the success probability) and the 1-norm s.
    With amplify=True and s <= 2, the weights are padded to s = 2 with +cI and -cI and one round of
    oblivious amplitude amplification is applied; the index-0 part is then (3/2 M - 1/2 M M^dagger M) psi."""
    cs = mpf_coefficients(ks)  # @line L1
    s = sum(abs(c) for c in cs)  # @line L2
    weights = [abs(c) for c in cs]
    unitaries = [scale(math.copysign(1, c), product_formula(terms, t, k)) for c, k in zip(cs, ks)]  # @line L3
    if amplify:
        if s > 2 + 1e-12:
            raise ValueError("one round of amplification needs s <= 2")
        d = len(psi)
        pad = (2 - s) / 2
        weights += [pad, pad]
        unitaries += [identity(d), scale(-1, identity(d))]
    m = 1 << max(1, math.ceil(math.log2(len(weights))))
    total = sum(weights)
    b = householder([complex(math.sqrt(w / total)) for w in weights] + [0j] * (m - len(weights)))  # @line L4
    parts = [list(psi)] + [[0j] * len(psi) for _ in range(m - 1)]
    parts = _w(b, unitaries, parts)  # @line L5
    if amplify:
        parts = _w(b, unitaries, _reflect(parts), inverse=True)
        parts = _w(b, unitaries, _reflect(parts))
        parts = [[-x for x in p] for p in parts]
    good = parts[0]
    return good, norm(good) ** 2, s  # @line L6
