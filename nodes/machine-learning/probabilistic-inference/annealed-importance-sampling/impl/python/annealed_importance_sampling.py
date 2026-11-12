# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/annealed-importance-sampling/. The authors are listed in prov/R9W3YJ.jsonl.

"""Annealed importance sampling (Neal 2001).

log_f(j, x) is the log of the unnormalized density f_j of the j-th distribution, j = 0 .. T.
sample_p0(rng) draws exactly from p_0 = f_0 / Z_0.
transition(j, x, rng) makes one Markov move that leaves p_j invariant.
Each run returns log w = sum_j [log f_j(x_{j-1}) - log f_{j-1}(x_{j-1})], and E[w] = Z_T / Z_0.
"""

import math
import random
from fractions import Fraction


def ais(log_f, sample_p0, transition, num_dists, s, rng: random.Random):
    """s independent AIS runs through f_0 .. f_T with T = num_dists. Return the log weights and
    the final states."""
    log_ws, xs = [], []
    for _ in range(s):  # @line L1
        x = sample_p0(rng)  # @line L2
        log_w = 0.0  # @line L3
        for j in range(1, num_dists + 1):  # @line L4
            log_w += log_f(j, x) - log_f(j - 1, x)  # @line L5
            x = transition(j, x, rng)  # @line L6
        log_ws.append(log_w)  # @line L7
        xs.append(x)
    return log_ws, xs


def log_mean_exp(log_ws):
    """log of the mean of the weights: the AIS estimate of log (Z_T / Z_0)."""
    m = max(log_ws)
    return m + math.log(sum(math.exp(v - m) for v in log_ws) / len(log_ws))  # @line L8


def weighted_expectation(log_ws, xs, h):
    """Self-normalized estimate of E_{p_T}[h(x)]."""
    m = max(log_ws)
    w = [math.exp(v - m) for v in log_ws]
    return sum(wi * h(x) for wi, x in zip(w, xs)) / sum(w)


def effective_sample_size(log_ws):
    m = max(log_ws)
    w = [math.exp(v - m) for v in log_ws]
    return sum(w) ** 2 / sum(v * v for v in w)


def geometric_path(log_f0, log_fT, betas):
    """f_j = f_0^(1 - beta_j) f_T^beta_j, for 0 = beta_0 < ... < beta_T = 1."""
    return lambda j, x: (1 - betas[j]) * log_f0(x) + betas[j] * log_fT(x)


def linear_betas(num_dists):
    return [j / num_dists for j in range(num_dists + 1)]


# ---- An Ising chain: a target with an exact partition function for checks ----

def ising_log_f(spins, coupling, field):
    return (coupling * sum(a * b for a, b in zip(spins, spins[1:]))
            + field * sum(spins))


def ising_log_z(n, coupling, field):
    """log Z by the transfer matrix, exact for an open chain of n spins."""
    vals = (-1, 1)
    v = [math.exp(field * a) for a in vals]
    for _ in range(n - 1):
        v = [sum(v[i] * math.exp(coupling * vals[i] * b + field * b) for i in range(2)) for b in vals]
    return math.log(sum(v))


def ising_ais(n, coupling, field, num_dists, s, rng: random.Random):
    """AIS from the uniform distribution on {-1, 1}^n (Z_0 = 2^n) to the Ising chain, along the
    geometric path, with one Gibbs sweep at each temperature. Return the estimate of log Z,
    the log weights and the final states."""
    betas = linear_betas(num_dists)
    log_f = geometric_path(lambda x: 0.0, lambda x: ising_log_f(x, coupling, field), betas)

    def sample_p0(r):
        return [r.choice((-1, 1)) for _ in range(n)]

    def gibbs_sweep(j, x, r):
        b = betas[j]
        x = list(x)
        for i in range(n):
            nb = (x[i - 1] if i > 0 else 0) + (x[i + 1] if i < n - 1 else 0)
            a = 2 * b * (coupling * nb + field)
            x[i] = 1 if r.random() < 1 / (1 + math.exp(-a)) else -1
        return x

    log_ws, xs = ais(log_f, sample_p0, gibbs_sweep, num_dists, s, rng)
    return n * math.log(2) + log_mean_exp(log_ws), log_ws, xs


# ---- Exact computation on a finite state space with Fractions ----

def linear_path_exact(f0, fT, betas):
    """f_j = (1 - beta_j) f_0 + beta_j f_T, as a list of value lists over the states."""
    return [[(1 - b) * a + b * c for a, c in zip(f0, fT)] for b in betas]


def metropolis_matrix(f):
    """Metropolis with a uniform proposal among the other states: an exact transition matrix
    that satisfies detailed balance with respect to f."""
    m = len(f)
    q = Fraction(1, m - 1)
    mat = [[Fraction(0)] * m for _ in range(m)]
    for x in range(m):
        for y in range(m):
            if y != x and f[x] > 0:
                mat[x][y] = q * min(Fraction(1), Fraction(f[y]) / f[x])
        mat[x][x] = 1 - sum(mat[x])
    return mat


def exact_mean_weight(fs, mats):
    """E[w] of AIS computed exactly: v_j(x) = E[w_j 1{x_j = x}], starting from p_0 = f_0 / Z_0.
    mats[j] is the kernel used after the j-th reweighting, for j = 1 .. T."""
    z0 = sum(fs[0])
    v = [Fraction(a) / z0 for a in fs[0]]
    for j in range(1, len(fs)):
        v = [vi * Fraction(fs[j][i]) / fs[j - 1][i] if vi else Fraction(0) for i, vi in enumerate(v)]
        mat = mats[j]
        v = [sum(v[x] * mat[x][y] for x in range(len(v))) for y in range(len(v))]
    return sum(v), v
