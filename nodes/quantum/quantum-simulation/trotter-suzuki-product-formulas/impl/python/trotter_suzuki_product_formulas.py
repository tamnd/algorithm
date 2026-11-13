# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trotter-suzuki-product-formulas/. The authors are listed in prov/B7XF2R.jsonl.
"""First and second order product formulas for H = sum_j c_j P_j (Pauli strings).

A sequence is a list of (string, theta) pairs. The circuit applies
e^(-i theta P) for each pair in list order, the first pair first, so the
unitary is the product of the factors from right (first) to left (last).
Qubit 0 is the least significant bit of the basis index (see qsim.py).
"""

import math

from qsim import (
    basis_state,
    commutator,
    mat_add,
    mat_scale,
    op_norm,
    pauli_matrix,
    pauli_rotation,
)


def trotter_sequence(terms, t, r, order=1, merge=True):
    """Pauli rotations of r steps of the first (order=1) or second (order=2) order formula."""
    if order not in (1, 2):
        raise ValueError("order must be 1 or 2")
    if r < 1:
        raise ValueError("r must be at least 1")
    big_l = len(terms)
    delta = t / r  # @line L1
    seq = []  # @line L2
    for _ in range(r):  # @line L3
        if order == 1:  # @line L4
            for c, p in terms:  # @line L5
                seq.append((p, c * delta))
        else:  # @line L6
            for c, p in terms[: big_l - 1]:  # @line L7
                seq.append((p, c * delta / 2))
            c, p = terms[-1]
            seq.append((p, c * delta))  # @line L8
            for c, p in reversed(terms[: big_l - 1]):  # @line L9
                seq.append((p, c * delta / 2))
    if merge:  # @line L10
        seq = merge_neighbors(seq)
    return seq  # @line L11


def merge_neighbors(seq):
    """Join neighbors with the same Pauli string: e^(-i a P) e^(-i b P) = e^(-i (a + b) P)."""
    out = []
    for p, th in seq:
        if out and out[-1][0] == p:
            out[-1] = (p, out[-1][1] + th)
        else:
            out.append((p, th))
    return out


def apply_sequence(psi, seq):
    for p, th in seq:
        psi = pauli_rotation(psi, p, th)
    return psi


def sequence_unitary(seq, n):
    """The 2^n x 2^n matrix of the circuit, column by column."""
    cols = [apply_sequence(basis_state(n, x), seq) for x in range(1 << n)]
    return [[cols[j][i] for j in range(1 << n)] for i in range(1 << n)]


def term_matrices(terms):
    return [mat_scale(pauli_matrix(p), c) for c, p in terms]


def first_order_constant(terms):
    """alpha_1 = sum_j || [H_j, H_(j+1) + ... + H_L] ||, the constant of the first order bound."""
    hs = term_matrices(terms)
    total = 0.0
    for j in range(len(hs) - 1):
        rest = hs[j + 1]
        for k in range(j + 2, len(hs)):
            rest = mat_add(rest, hs[k])
        total += op_norm(commutator(hs[j], rest))
    return total


def first_order_pair_constant(terms):
    """The weaker pairwise constant sum_(j<k) ||[c_j P_j, c_k P_k]|| = sum over anticommuting pairs of 2 |c_j c_k|."""
    total = 0.0
    for j in range(len(terms)):
        for k in range(j + 1, len(terms)):
            (cj, pj), (ck, pk) = terms[j], terms[k]
            n_diff = sum(1 for a, b in zip(pj, pk) if a != "I" and b != "I" and a != b)
            if n_diff % 2:
                total += 2 * abs(cj * ck)
    return total


def second_order_constant(terms):
    """beta_2 = sum_j ( ||[T, [T, H_j]]|| / 12 + ||[H_j, [H_j, T]]|| / 24 ), T = H_(j+1) + ... + H_L."""
    hs = term_matrices(terms)
    total = 0.0
    for j in range(len(hs) - 1):
        rest = hs[j + 1]
        for k in range(j + 2, len(hs)):
            rest = mat_add(rest, hs[k])
        inner_c = commutator(rest, hs[j])
        total += op_norm(commutator(rest, inner_c)) / 12
        total += op_norm(commutator(hs[j], commutator(hs[j], rest))) / 24
    return total


def error_bound(terms, t, r, order):
    """Upper bound on || S(t/r)^r - e^(-iHt) || in the spectral norm."""
    if order == 1:
        return t * t / (2 * r) * first_order_constant(terms)
    return t ** 3 / r ** 2 * second_order_constant(terms)


def steps_for_error(terms, t, eps, order):
    """The least r for which error_bound(terms, t, r, order) <= eps."""
    if order == 1:
        a = first_order_constant(terms)
        r = max(1, math.ceil(t * t * a / (2 * eps)))
    else:
        b = second_order_constant(terms)
        r = max(1, math.ceil(math.sqrt(t ** 3 * b / eps)))
    while r > 1 and error_bound(terms, t, r - 1, order) <= eps:
        r -= 1
    while error_bound(terms, t, r, order) > eps:
        r += 1
    return r


def trotterize(terms, t, eps, order=2):
    """The product formula circuit with a proven error of at most eps in the spectral norm."""
    r = steps_for_error(terms, t, eps, order)
    return r, trotter_sequence(terms, t, r, order)
