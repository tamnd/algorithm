# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interaction-picture-simulation/. The authors are listed in prov/514Y6M.jsonl.
"""Interaction picture simulation (Low and Wiebe 2018), with a midpoint Dyson series.

H = A + B, where e^(-iAs) is easy to apply and B = sum_l c_l P_l has 1-norm lambda_B. Then
e^(-iH tau) = e^(-iA tau) T exp(-i int_0^tau H_I(s) ds) with H_I(s) = e^(iAs) B e^(-iAs).
The time is cut into r segments with lambda_B tau <= ln 2. In each segment the Dyson series is
discretized at the midpoints s_q = (q + 1/2) tau / M of M cells and truncated at order K. All
index tuples are kept, also those with repeated cells, so the series is the truncation of the
product of the M exponentials e^(-i h H_I(s_q)) with h = tau / M.

The joint state of the index register and the system is a list of system vectors,
parts[j] = (<j| (x) I) |state>, one for each index value j. Qubit 0 is the least significant bit.
"""

import itertools
import math

from qsim import expm_hermitian, identity, matmul, matvec, norm, pauli_matrix, scale


def segments(lam_b, t):
    """r = ceil(lambda_B t / ln 2) segments of length tau = t / r, so that lambda_B tau <= ln 2."""
    r = max(1, math.ceil(lam_b * t / math.log(2) - 1e-12))
    return r, t / r


def midpoints(tau, big_m):
    return [(q + 0.5) * tau / big_m for q in range(big_m)]


def interaction_terms(a, b_terms, tau, big_m):
    """For each cell q and term l: (q, |c_l|, e^(iA s_q) sign(c_l) P_l e^(-iA s_q))."""
    out = []
    for q, s in enumerate(midpoints(tau, big_m)):
        rot, back = expm_hermitian(a, -s), expm_hermitian(a, s)
        for c, p in b_terms:
            out.append((q, abs(c), matmul(rot, matmul(scale(math.copysign(1, c), pauli_matrix(p)), back))))
    return out


def dyson_lcu(a, b_terms, tau, big_m, big_k):
    """Weights beta_j > 0 and unitaries V_j of the midpoint Dyson series to order K.

    A label j is a tuple of k (cell, term) pairs. Its weight is h^k |c_l1| ... |c_lk| / k!, and its
    unitary is (-i)^k times the product ordered by cell, later cells to the left; pairs in the same
    cell keep the order of the tuple.
    """
    d = len(a)
    h = tau / big_m
    terms = interaction_terms(a, b_terms, tau, big_m)
    betas, unitaries = [], []
    for k in range(big_k + 1):
        for tup in itertools.product(range(len(terms)), repeat=k):
            beta = h ** k / math.factorial(k)
            v = scale((-1j) ** k, identity(d))
            for idx in sorted(tup, key=lambda i: terms[i][0]):
                beta *= terms[idx][1]
                v = matmul(terms[idx][2], v)
            betas.append(beta)
            unitaries.append(v)
    return betas, unitaries


def pad_to_two(betas, unitaries):
    """Add +c I and -c I with 2c = 2 - s, so that the 1-norm is exactly 2 and the sum does not change."""
    s = sum(betas)
    if s > 2 + 1e-12:
        raise ValueError("segment too long: s > 2")
    c = (2 - s) / 2
    d = len(unitaries[0])
    return list(betas) + [c, c], list(unitaries) + [identity(d), scale(-1, identity(d))]


def prep_vector(betas):
    """The column B|0> = 2^(-1/2) sum_j sqrt(beta_j) |j>, padded to a power of two."""
    size = 1 << max(1, math.ceil(math.log2(len(betas))))
    s = sum(betas)
    return [complex(math.sqrt(b / s)) for b in betas] + [0j] * (size - len(betas))


def apply_prep(v, parts):
    """The Householder reflection B = I - 2 w w^dagger / (w^dagger w), w = |0> - v, on the index register."""
    w = [(1.0 if i == 0 else 0.0) - x for i, x in enumerate(v)]
    ww = sum(abs(x) ** 2 for x in w)
    dot = [0j] * len(parts[0])
    for wj, pj in zip(w, parts):
        if wj != 0:
            for x, y in enumerate(pj):
                dot[x] += wj.conjugate() * y
    return [[y - 2 * wj * dx / ww for y, dx in zip(pj, dot)] for wj, pj in zip(w, parts)]


def apply_w(v, unitaries, parts, inverse=False):
    """W = (B (x) I) SELECT (B (x) I), or W^dagger; B is Hermitian, SELECT is the identity on unused indices."""
    parts = apply_prep(v, parts)
    sel = []
    for j, p in enumerate(parts):
        if j < len(unitaries):
            u = unitaries[j]
            if inverse:
                u = [[u[k][i].conjugate() for k in range(len(u))] for i in range(len(u))]
            sel.append(matvec(u, p))
        else:
            sel.append(list(p))
    return apply_prep(v, sel)


def reflect(parts):
    """R = 2 |0><0| (x) I - I on the index register."""
    return [list(parts[0])] + [[-x for x in p] for p in parts[1:]]


def segment(v, unitaries, psi):
    """-W R W^dagger R W on |0>|psi>. Returns the index-0 part."""
    parts = [list(psi)] + [[0j] * len(psi) for _ in range(len(v) - 1)]
    parts = apply_w(v, unitaries, parts)
    parts = apply_w(v, unitaries, reflect(parts), inverse=True)
    parts = apply_w(v, unitaries, reflect(parts))
    return [-x for x in parts[0]]


def ip_simulate(a, b_terms, t, big_m, big_k, psi):
    """Approximate e^(-i(A + B)t)|psi>. Returns the unnormalized output, the product of the success probabilities and r."""
    lam_b = sum(abs(c) for c, _ in b_terms)  # @line L1
    r, tau = segments(lam_b, t)  # @line L2
    betas, unitaries = pad_to_two(*dyson_lcu(a, b_terms, tau, big_m, big_k))  # @line L3
    v = prep_vector(betas)  # @line L4
    free = expm_hermitian(a, tau)
    state, prob = list(psi), 1.0
    for _ in range(r):  # @line L5
        good = segment(v, unitaries, state)  # @line L6
        prob *= norm(good) ** 2 / norm(state) ** 2
        state = matvec(free, good)  # @line L7
    return state, prob, r  # @line L8


def midpoint_product(a, b, tau, big_m):
    """The product of e^(-i h H_I(s_q)) over the cells, later cells to the left: the series for K = infinity."""
    h = tau / big_m
    out = identity(len(a))
    for s in midpoints(tau, big_m):
        h_i = matmul(expm_hermitian(a, -s), matmul(b, expm_hermitian(a, s)))
        out = matmul(expm_hermitian(h_i, h), out)
    return out


def tail(x, big_k):
    """sum_{k > K} x^k / k!."""
    return sum(x ** j / math.factorial(j) for j in range(big_k + 1, big_k + 60))


def discretization_bound(lam_b, c1, c2, tau, big_m):
    """A bound on ||midpoint product - T exp(-i int H_I)|| with c1 >= ||[A, B]||, c2 >= ||[A, [A, B]]||."""
    return tau ** 3 / big_m ** 2 * (c2 / 24 + lam_b * c1 / 4) + tau ** 4 * c1 ** 2 / (16 * big_m ** 3)


def error_bound(lam_b, c1, c2, t, big_m, big_k):
    """(1 + e)^r - 1 with e = eta + 1.5 eta^2 + 0.5 eta^3 and eta = tail(lambda_B tau, K) + discretization."""
    r, tau = segments(lam_b, t)
    eta = tail(lam_b * tau, big_k) + discretization_bound(lam_b, c1, c2, tau, big_m)
    e = eta + 1.5 * eta ** 2 + 0.5 * eta ** 3
    x = r * math.log1p(e)
    return math.inf if x > 700 else math.expm1(x)
