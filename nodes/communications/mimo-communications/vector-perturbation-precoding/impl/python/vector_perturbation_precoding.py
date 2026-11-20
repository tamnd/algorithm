# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vector-perturbation-precoding/. The authors are listed in prov/RSA6ZS.jsonl.

"""Vector perturbation (VP) precoding for the multiuser MISO downlink.

User k receives y_k = h_k^H x + w_k with w_k ~ CN(0, N0). The K by M matrix H
has row k equal to h_k^H and full row rank. For a data vector s of QAM
symbols with real and imaginary parts in [-tau/2, tau/2), the transmitter
sends

    x = sqrt(P / gamma) F (s + tau l),   F = H^H (H H^H)^(-1),
    gamma = ||F (s + tau l)||^2,

where l is the vector of Gaussian integers that makes gamma smallest. The
search for l is a closest vector problem. It is solved exactly here: the
quadratic form (s + tau l)^H (H H^H)^(-1) (s + tau l) is written in real
form, factored by Cholesky as ||R v||^2 with R upper triangular, and searched
by Schnorr-Euchner enumeration. User k multiplies its sample by
sqrt(gamma / P) and reduces it modulo tau.
"""

import math

import cbb


def mod_tau(z: complex, tau: float) -> complex:
    """Reduce the real and imaginary parts of z into [-tau/2, tau/2)."""
    re = z.real - tau * math.floor(z.real / tau + 0.5)
    im = z.imag - tau * math.floor(z.imag / tau + 0.5)
    return complex(re, im)


def real_form(a: list[list[complex]]) -> list[list[float]]:
    """The 2K by 2K real matrix [[Re A, -Im A], [Im A, Re A]], so u^H A u = v^T A_r v for v = [Re u; Im u]."""
    k = len(a)
    out = [[0.0] * (2 * k) for _ in range(2 * k)]
    for i in range(k):
        for j in range(k):
            z = complex(a[i][j])
            out[i][j] = z.real
            out[i][j + k] = -z.imag
            out[i + k][j] = z.imag
            out[i + k][j + k] = z.real
    return out


def closest_point(r: list[list[float]], v: list[float], tau: float) -> tuple[list[int], float]:
    """Minimize ||R (v + tau l)||^2 over integer vectors l, for upper triangular R with a positive diagonal.

    Schnorr-Euchner enumeration: a depth-first search from the last
    coordinate to the first. At each level the candidates for l_i are visited
    in the order of their distance from the real center, and a branch stops
    as soon as its partial sum reaches the best value found so far.
    Returns (l, value).
    """
    n = len(r)
    best = [math.inf]
    best_l: list[list[int]] = [[0] * n]
    lv = [0] * n

    def search(i: int, partial: float) -> None:
        if i < 0:
            if partial < best[0]:
                best[0] = partial
                best_l[0] = lv[:]
            return
        tail = sum(r[i][j] * (v[j] + tau * lv[j]) for j in range(i + 1, n))
        center = (-tail / r[i][i] - v[i]) / tau
        step = r[i][i] * tau
        c0 = math.floor(center + 0.5)
        sign = 1 if center >= c0 else -1
        t = 0
        while True:
            if t == 0:
                cand = c0
            elif t % 2 == 1:
                cand = c0 + sign * ((t + 1) // 2)
            else:
                cand = c0 - sign * (t // 2)
            d = partial + (step * (cand - center)) ** 2
            if d >= best[0]:
                break  # the zigzag order makes d grow, so no later candidate is better
            lv[i] = cand
            search(i - 1, d)
            t += 1

    search(n - 1, 0.0)
    return best_l[0], best[0]


def vp_precode(h: list[list[complex]], s: list[complex], p_total: float, tau: float):
    """Precode one data vector s. Returns (x, l, gamma)."""
    k_users = len(h)
    g = cbb.matmul(h, cbb.herm(h))
    f = cbb.herm(cbb.solve(g, h))  # @line L1
    a = cbb.inv(g)  # @line L2
    low = cbb.cholesky(real_form(a))  # @line L3
    r = [[low[j][i].real for j in range(2 * k_users)] for i in range(2 * k_users)]
    v = [complex(z).real for z in s] + [complex(z).imag for z in s]
    li, _ = closest_point(r, v, tau)  # @line L4
    l_vec = [complex(li[i], li[i + k_users]) for i in range(k_users)]
    u = [complex(s[i]) + tau * l_vec[i] for i in range(k_users)]  # @line L5
    xt = cbb.matvec(f, u)
    gamma = cbb.norm2(xt)  # @line L6
    x = cbb.scale(math.sqrt(p_total / gamma), xt)  # @line L7
    return x, l_vec, gamma


def vp_receive(y: complex, gamma: float, p_total: float, tau: float) -> complex:
    """The receiver of one user: undo the common scale, then reduce modulo tau."""
    return mod_tau(y * math.sqrt(gamma / p_total), tau)  # @line L8
