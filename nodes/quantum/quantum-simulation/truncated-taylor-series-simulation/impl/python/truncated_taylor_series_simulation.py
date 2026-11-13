# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/truncated-taylor-series-simulation/. The authors are listed in prov/6TQGRV.jsonl.
"""Truncated Taylor series simulation (Berry, Childs, Cleve, Kothari and Somma 2015).

H = sum_l c_l P_l with Pauli strings P_l. The evolution for time t is cut into r segments of
length tau = t / r with lambda tau <= ln 2. In each segment the truncated series
sum_{k <= K} (-i tau H)^k / k! is a linear combination of the unitaries (-i)^k P_l1 ... P_lk,
padded to the 1-norm s = 2 and run with one round of oblivious amplitude amplification.

The joint state of the index register and the system is a list of system vectors,
parts[j] = (<j| (x) I) |state>, one for each index value j. Qubit 0 is the least significant bit.
"""

import itertools
import math

from qsim import householder, identity, matmul, matvec, norm, pauli_matrix, scale


def segments(lam, t):
    """r = ceil(lambda t / ln 2) segments of length tau = t / r, so that lambda tau <= ln 2."""
    r = max(1, math.ceil(lam * t / math.log(2) - 1e-12))
    return r, t / r


def taylor_lcu(terms, tau, big_k):
    """The weights beta_j > 0 and unitaries V_j with sum_j beta_j V_j = sum_{k <= K} (-i tau H)^k / k!."""
    d = 1 << len(terms[0][1])
    paulis = [scale(math.copysign(1, c), pauli_matrix(s)) for c, s in terms]
    betas, unitaries = [], []
    for k in range(big_k + 1):
        for ls in itertools.product(range(len(terms)), repeat=k):
            beta = tau ** k / math.factorial(k)
            v = scale((-1j) ** k, identity(d))
            for l in ls:
                beta *= abs(terms[l][0])
                v = matmul(v, paulis[l])
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


def prep_matrix(betas):
    """B with B|0> = s^(-1/2) sum_j sqrt(beta_j) |j>, padded to a power of two. B is Hermitian."""
    m = 1 << max(1, math.ceil(math.log2(len(betas))))
    s = sum(betas)
    v = [complex(math.sqrt(b / s)) for b in betas] + [0j] * (m - len(betas))
    return householder(v)


def apply_index_matrix(b, parts):
    out = []
    for row in b:
        v = [0j] * len(parts[0])
        for bij, pj in zip(row, parts):
            if bij != 0:
                for x, y in enumerate(pj):
                    v[x] += bij * y
        out.append(v)
    return out


def apply_w(b, unitaries, parts, inverse=False):
    """W = (B^dagger (x) I) SELECT (B (x) I), or W^dagger; B is Hermitian, SELECT is the identity on unused indices."""
    parts = apply_index_matrix(b, parts)
    sel = []
    for j, p in enumerate(parts):
        if j < len(unitaries):
            u = unitaries[j]
            if inverse:
                u = [[u[k][i].conjugate() for k in range(len(u))] for i in range(len(u))]
            sel.append(matvec(u, p))
        else:
            sel.append(list(p))
    return apply_index_matrix(b, sel)


def reflect(parts):
    """R = 2 |0><0| (x) I - I on the index register."""
    return [list(parts[0])] + [[-x for x in p] for p in parts[1:]]


def segment(b, unitaries, psi):
    """A = -W R W^dagger R W on |0>|psi>. Returns the index-0 part and its squared norm."""
    parts = [list(psi)] + [[0j] * len(psi) for _ in range(len(b) - 1)]
    parts = apply_w(b, unitaries, parts)
    parts = apply_w(b, unitaries, reflect(parts), inverse=True)
    parts = apply_w(b, unitaries, reflect(parts))
    good = [-x for x in parts[0]]
    return good, norm(good) ** 2


def taylor_simulate(terms, t, big_k, psi):
    """Approximate e^(-iHt)|psi>. Returns the unnormalized output, the product of the success probabilities and r."""
    lam = sum(abs(c) for c, _ in terms)  # @line L1
    r, tau = segments(lam, t)  # @line L2
    betas, unitaries = pad_to_two(*taylor_lcu(terms, tau, big_k))  # @line L3
    b = prep_matrix(betas)  # @line L4
    state, prob = list(psi), 1.0
    for _ in range(r):  # @line L5
        good, p = segment(b, unitaries, state)  # @line L6
        prob *= p / norm(state) ** 2
        state = good  # @line L7
    return state, prob, r  # @line L8


def tail(x, big_k):
    """delta = sum_{k > K} x^k / k!, the truncation error of one segment when lambda tau = x <= ln 2."""
    return sum(x ** j / math.factorial(j) for j in range(big_k + 1, big_k + 60))


def error_bound(lam, t, big_k):
    """The bound (1 + e)^r - 1 on ||output - e^(-iHt) psi||, with e = delta + 1.5 delta^2 + 0.5 delta^3."""
    r, tau = segments(lam, t)
    delta = tail(lam * tau, big_k)
    e = delta + 1.5 * delta ** 2 + 0.5 * delta ** 3
    x = r * math.log1p(e)
    return math.inf if x > 700 else math.expm1(x)


def order_for(lam, t, eps):
    """The least K whose bound is at most eps."""
    big_k = 0
    while error_bound(lam, t, big_k) > eps:
        big_k += 1
    return big_k
