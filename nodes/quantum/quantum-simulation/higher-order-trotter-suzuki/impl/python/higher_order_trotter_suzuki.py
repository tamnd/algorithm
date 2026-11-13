# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/higher-order-trotter-suzuki/. The authors are listed in prov/KW8GH0.jsonl.
"""Suzuki's recursive product formulas S_2k for H = sum_j c_j P_j (Pauli strings).

S_2(x) = e^(x H_1 / 2) ... e^(x H_(L-1) / 2) e^(x H_L) e^(x H_(L-1) / 2) ... e^(x H_1 / 2)
S_2k(x) = S_(2k-2)(p_k x)^2 S_(2k-2)((1 - 4 p_k) x) S_(2k-2)(p_k x)^2,
p_k = 1 / (4 - 4^(1/(2k-1))), with x = -i t for time evolution.

A sequence is a list of (string, theta) pairs. The circuit applies
e^(-i theta P) for each pair in list order, the first pair first.
Qubit 0 is the least significant bit of the basis index (see qsim.py).
"""

import math

from qsim import basis_state, pauli_rotation


def suzuki_p(k):
    """p_k = 1 / (4 - 4^(1/(2k - 1))) for k >= 2."""
    return 1.0 / (4.0 - 4.0 ** (1.0 / (2 * k - 1)))


def stage_weights(order):
    """The time fractions of the 5^(k-1) second order stages of S_order, order = 2k."""
    if order < 2 or order % 2:
        raise ValueError("order must be an even number >= 2")
    if order == 2:  # @line L1
        return [1.0]  # @line L2
    k = order // 2
    p = suzuki_p(k)  # @line L3
    inner = stage_weights(order - 2)  # @line L4
    q = 1.0 - 4.0 * p
    outer = [p * w for w in inner]
    return outer + outer + [q * w for w in inner] + outer + outer  # @line L5


def suzuki_sequence(terms, t, r, order, merge=True):
    """Pauli rotations of r steps of S_order(-i t / r)."""
    if r < 1:
        raise ValueError("r must be at least 1")
    weights = stage_weights(order)
    delta = t / r  # @line L6
    head = terms[:-1]
    c_last, p_last = terms[-1]
    seq = []
    for _ in range(r):  # @line L7
        for w in weights:  # @line L8
            h = w * delta
            for c, p in head:  # @line L9
                seq.append((p, c * h / 2))
            seq.append((p_last, c_last * h))  # @line L10
            for c, p in reversed(head):  # @line L11
                seq.append((p, c * h / 2))
    if merge:  # @line L12
        out = []
        for p, th in seq:
            if out and out[-1][0] == p:
                out[-1] = (p, out[-1][1] + th)
            else:
                out.append((p, th))
        seq = out
    return seq  # @line L13


def exponential_count(big_l, order, r):
    """The number of exponentials after merging: 2 (L - 1) 5^(k - 1) r + 1, for L >= 2 distinct neighbors."""
    k = order // 2
    return 2 * (big_l - 1) * 5 ** (k - 1) * r + 1


def apply_sequence(psi, seq):
    for p, th in seq:
        psi = pauli_rotation(psi, p, th)
    return psi


def sequence_unitary(seq, n):
    cols = [apply_sequence(basis_state(n, x), seq) for x in range(1 << n)]
    return [[cols[j][i] for j in range(1 << n)] for i in range(1 << n)]


def bacs_error_bound(big_l, lam, t, r, order):
    """Lemma 1 of Berry, Ahokas, Cleve and Sanders (2007): 5 (2 5^(k-1) L Lambda t)^(2k+1) / r^(2k).

    Lambda bounds the spectral norm of every term. The bound is proved for
    4 L 5^(k-1) Lambda t / r <= 1 and (16/3) (2 5^(k-1) L Lambda t)^(2k+1) / r^(2k) <= 1;
    the function returns None outside this range.
    """
    k = order // 2
    tau = lam * t
    a = (2 * 5 ** (k - 1) * big_l * tau) ** (2 * k + 1) / r ** (2 * k)
    if 4 * big_l * 5 ** (k - 1) * tau / r > 1 or 16.0 / 3.0 * a > 1:
        return None
    return 5 * a


def bacs_steps(big_l, lam, t, eps, order):
    """r = ceil(4 5^(k - 1/2) (L tau)^(1 + 1/2k) / eps^(1/2k)), eq. (8) of BACS, tau = Lambda t."""
    k = order // 2
    tau = lam * t
    return math.ceil(4 * 5 ** (k - 0.5) * (big_l * tau) ** (1 + 1 / (2 * k)) / eps ** (1 / (2 * k)))


def bacs_best_order(big_l, lam, t, eps):
    """The order 2k with k = round(sqrt(log_5(L tau / eps)) / 2 + 1), the choice of BACS."""
    tau = lam * t
    k = round(0.5 * math.sqrt(math.log(big_l * tau / eps, 5)) + 1)
    return 2 * max(1, k)
