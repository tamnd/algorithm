# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prosac/. The authors are listed in prov/B0M487.jsonl.
"""PROSAC (progressive sample consensus), Chum and Matas 2005.

The data come sorted by a quality score, best first. PROSAC draws its samples
from a growing prefix U_n of the sorted data: by the growth function, the t-th
sample is u_n (the n-th item) together with m - 1 items drawn from U_{n-1},
where n = g(t) = min{n : T'_n >= t}, as in eq. (6) of the paper. Once the
prefix stops growing at n*, samples are drawn from U_{n*} uniformly, as in
RANSAC. The stopping rule picks n* to minimize the number of samples needed
for the prefix, among prefixes whose inlier count passes a non-randomness test.

The model is a line in the plane, a x + b y + c = 0 with a^2 + b^2 = 1, from
m = 2 points. Standard library only.
"""

import math
import random


def line_through(sample):
    """The line through two points, as (a, b, c) with a^2 + b^2 = 1, or None if they coincide."""
    (x1, y1), (x2, y2) = sample
    a, b = y1 - y2, x2 - x1
    nrm = math.hypot(a, b)
    if nrm == 0.0:
        return None
    a, b = a / nrm, b / nrm
    if a < 0 or (a == 0 and b < 0):
        a, b = -a, -b
    return (a, b, -(a * x1 + b * y1))


def point_line_distance(line, pt):
    a, b, c = line
    return abs(a * pt[0] + b * pt[1] + c)


def growth_schedule(N, m, T_N):
    """Return {n: T'_n} for n = m..N, with T'_m = 1 and T'_{n+1} = T'_n + ceil(T_{n+1} - T_n)."""
    T = float(T_N)
    for i in range(m):
        T *= (m - i) / (N - i)  # T_m = T_N C(m, m) / C(N, m)
    Tp = {m: 1}
    for n in range(m, N):
        T_next = T * (n + 1) / (n + 1 - m)
        Tp[n + 1] = Tp[n] + math.ceil(T_next - T)
        T = T_next
    return Tp


def min_inliers_table(N, m, beta, psi):
    """I_n^min = min{j : sum_{i=j}^n P^R_n(i) < psi}, P^R_n(i) binomial(n - m, beta) at i - m."""
    table = {}
    for n in range(m, N + 1):
        tail = 0.0
        j = n + 1
        for i in range(n, m - 1, -1):
            tail += math.comb(n - m, i - m) * beta ** (i - m) * (1.0 - beta) ** (n - i)
            if tail >= psi:
                break
            j = i
        table[n] = j
    return table


def samples_needed(I_n, n, m, eta0):
    """k_n(eta0) = log(eta0) / log(1 - P_In), P_In = prod_{j<m} (I_n - j) / (n - j)."""
    if I_n < m:
        return math.inf
    P = 1.0
    for j in range(m):
        P *= (I_n - j) / (n - j)
    if P >= 1.0:
        return 1
    return math.ceil(math.log(eta0) / math.log1p(-P))


def choose_n_star(is_inlier, m, imin, eta0, max_trials):
    """Over prefixes n that pass the non-randomness test, minimize k_n. Returns (n*, k*)."""
    best_n, best_k = len(is_inlier), max_trials
    count = sum(is_inlier[:m - 1])
    for n in range(m, len(is_inlier) + 1):
        count += is_inlier[n - 1]
        if count >= imin[n]:
            k_n = samples_needed(count, n, m, eta0)
            if k_n < best_k:
                best_n, best_k = n, k_n
    return best_n, best_k


def prosac(data, eps, rng=None, m=2, T_N=200000, beta=0.05, psi=0.05, eta0=0.05,
           max_trials=10000, fit_minimal=line_through, residual=point_line_distance):
    """data sorted by quality, best first. Return (model, inliers, trials, n_star)."""
    rng = rng if rng is not None else random.Random()
    N = len(data)
    if N < m:
        return None, [], 0, N
    Tp = growth_schedule(N, m, T_N)
    imin = min_inliers_table(N, m, beta, psi)
    t, n, n_star, k_star = 0, m, N, max_trials  # @line L1
    best, best_inl = None, []
    while t < k_star:  # @line L2
        t += 1  # @line L3
        while t > Tp[n] and n < n_star:  # @line L4
            n += 1  # @line L5
        if t <= Tp[n]:  # @line L6
            idx = [n - 1] + rng.sample(range(n - 1), m - 1)  # @line L7
        else:
            idx = rng.sample(range(n), m)  # @line L8
        theta = fit_minimal([data[i] for i in idx])  # @line L9
        if theta is None:
            continue
        flags = [1 if residual(theta, x) <= eps else 0 for x in data]  # @line L10
        if sum(flags) > len(best_inl):  # @line L11
            best, best_inl = theta, [i for i in range(N) if flags[i]]  # @line L12
            n_star, k_star = choose_n_star(flags, m, imin, eta0, max_trials)  # @line L13
            n_star = max(n_star, n)
    return best, best_inl, t, n_star  # @line L14
