# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-likelihood-linear-regression/. The authors are listed in prov/TR4HQ1.jsonl.

"""Maximum likelihood linear regression (MLLR) of Gaussian means.

The model is a set of M Gaussians with diagonal covariances, given by the
speaker-independent means mu[m] (n numbers each), the variances var[m] and,
for the EM driver, the mixture weights w[m]. Each Gaussian belongs to one
regression class r(m). MLLR replaces each mean by

    mu'_m = W_r xi_m,   xi_m = (1, mu_m[0], ..., mu_m[n-1]),

where W_r = [b | A] is an n x (n + 1) matrix shared by all the Gaussians of
class r. With diagonal covariances the maximum of the EM auxiliary function
separates by rows: row i of W_r solves G_i w = k_i with

    G_i = sum_m (occ_m / var_m[i]) xi_m xi_m^T,   k_i = sum_m (s_m[i] / var_m[i]) xi_m,

where occ_m = sum_t gamma_m(t) and s_m = sum_t gamma_m(t) o_t are the
occupancy and the first-order statistic of Gaussian m (Leggetter and Woodland
1995). The posteriors gamma_m(t) here come from a Gaussian mixture; in an HMM
system they come from the forward-backward algorithm, and the M-step
(estimate_transforms) is the same. Every log is the natural log.
"""

import math
from typing import List, Optional, Sequence, Tuple

from nlslog import log_sum

Vector = List[float]
Matrix = List[List[float]]

LOG_2PI = math.log(2.0 * math.pi)


def log_gauss_diag(x: Sequence[float], mu: Sequence[float], var: Sequence[float]) -> float:
    """Return log N(x; mu, diag(var))."""
    s = 0.0
    for xi, mi, vi in zip(x, mu, var):
        s += LOG_2PI + math.log(vi) + (xi - mi) * (xi - mi) / vi
    return -0.5 * s


def extended(mu: Sequence[float]) -> Vector:
    """Return the extended mean vector xi = (1, mu)."""
    return [1.0] + [float(v) for v in mu]


def identity_transform(n: int) -> Matrix:
    """Return W = [0 | I], which leaves every mean unchanged."""
    return [[0.0] + [1.0 if j == i else 0.0 for j in range(n)] for i in range(n)]


def apply_transform(W: Matrix, mu: Sequence[float]) -> Vector:
    """Return W xi = A mu + b."""
    xi = extended(mu)
    return [math.fsum(a * x for a, x in zip(row, xi)) for row in W]


def solve(G: Matrix, k: Sequence[float]) -> Vector:
    """Solve G w = k by Gaussian elimination with partial pivoting.

    Raise ValueError if G is singular (relative pivot below 1e-12).
    """
    n = len(G)
    a = [list(map(float, G[i])) + [float(k[i])] for i in range(n)]
    scale = max((abs(v) for row in G for v in row), default=0.0)
    if scale == 0.0:
        raise ValueError("singular system: no data in this class")
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(a[r][c]))
        if abs(a[p][c]) <= 1e-12 * scale:
            raise ValueError("singular system: the class needs n + 1 affinely independent means with data")
        a[c], a[p] = a[p], a[c]
        for r in range(c + 1, n):
            f = a[r][c] / a[c][c]
            if f != 0.0:
                for j in range(c, n + 1):
                    a[r][j] -= f * a[c][j]
    w = [0.0] * n
    for c in range(n - 1, -1, -1):
        s = a[c][n] - math.fsum(a[c][j] * w[j] for j in range(c + 1, n))
        w[c] = s / a[c][c]
    return w


def posteriors(frame: Sequence[float], weights: Sequence[float], means: Sequence[Sequence[float]],
               variances: Sequence[Sequence[float]]) -> Tuple[Vector, float]:
    """Return (gamma, log p(frame)) for a diagonal Gaussian mixture, in log space."""
    lp = [math.log(w) + log_gauss_diag(frame, m, v) if w > 0 else float("-inf")
          for w, m, v in zip(weights, means, variances)]
    z = log_sum(lp)
    return [math.exp(x - z) for x in lp], z


def accumulate(frames: Sequence[Sequence[float]], weights: Sequence[float], means: Sequence[Sequence[float]],
               variances: Sequence[Sequence[float]]) -> Tuple[Vector, Matrix, float]:
    """E-step: return (occ, s, log likelihood) under the mixture with these means."""
    M, n = len(means), len(means[0])
    occ = [0.0] * M
    s = [[0.0] * n for _ in range(M)]
    total = 0.0
    for o in frames:
        g, z = posteriors(o, weights, means, variances)  # @line L4
        total += z
        for m in range(M):
            if g[m] > 0.0:
                occ[m] += g[m]  # @line L5
                sm = s[m]
                for i in range(n):
                    sm[i] += g[m] * o[i]
    return occ, s, total


def estimate_transforms(means: Sequence[Sequence[float]], variances: Sequence[Sequence[float]],
                        occ: Sequence[float], s: Sequence[Sequence[float]],
                        classes: Optional[Sequence[int]] = None) -> List[Matrix]:
    """M-step: return one n x (n + 1) transform per regression class.

    means are the speaker-independent means; classes[m] is the class of
    Gaussian m (all 0 when None, a global transform). Row i of W_r solves
    G_i w = k_i. Raise ValueError if a class has too little data.
    """
    M, n = len(means), len(means[0])
    if classes is None:
        classes = [0] * M
    R = max(classes) + 1
    Ws = []
    for r in range(R):  # @line L6
        members = [m for m in range(M) if classes[m] == r]
        xis = [extended(means[m]) for m in members]
        W = []
        for i in range(n):
            G = [[0.0] * (n + 1) for _ in range(n + 1)]
            k = [0.0] * (n + 1)
            for m, xi in zip(members, xis):
                c = occ[m] / variances[m][i]
                d = s[m][i] / variances[m][i]
                for p in range(n + 1):
                    k[p] += d * xi[p]  # @line L7
                    cp = c * xi[p]
                    row = G[p]
                    for q in range(n + 1):
                        row[q] += cp * xi[q]
            W.append(solve(G, k))  # @line L8
        Ws.append(W)
    return Ws


def adapt_means(means: Sequence[Sequence[float]], Ws: Sequence[Matrix],
                classes: Optional[Sequence[int]] = None) -> Matrix:
    """Return the adapted means mu'_m = W_{r(m)} xi_m."""
    if classes is None:
        classes = [0] * len(means)
    return [apply_transform(Ws[classes[m]], mu) for m, mu in enumerate(means)]  # @line L3


def mllr(frames: Sequence[Sequence[float]], weights: Sequence[float], means: Sequence[Sequence[float]],
         variances: Sequence[Sequence[float]], classes: Optional[Sequence[int]] = None,
         iterations: int = 5) -> Tuple[List[Matrix], Matrix, List[float]]:
    """Run MLLR by EM on unlabeled adaptation frames.

    Return (transforms, adapted means, log likelihoods), where the list of log
    likelihoods holds the value before each iteration and after the last one.
    The weights and variances stay fixed.
    """
    if classes is None:
        classes = [0] * len(means)
    n = len(means[0])
    R = max(classes) + 1
    Ws = [identity_transform(n) for _ in range(R)]  # @line L1
    history = []
    for _ in range(iterations):  # @line L2
        cur = adapt_means(means, Ws, classes)
        occ, s, ll = accumulate(frames, weights, cur, variances)
        history.append(ll)
        Ws = estimate_transforms(means, variances, occ, s, classes)
    cur = adapt_means(means, Ws, classes)
    history.append(accumulate(frames, weights, cur, variances)[2])
    return Ws, cur, history  # @line L9


def auxiliary(means: Sequence[Sequence[float]], variances: Sequence[Sequence[float]], occ: Sequence[float],
              s: Sequence[Sequence[float]], Ws: Sequence[Matrix], classes: Optional[Sequence[int]] = None) -> float:
    """Return the part of the EM auxiliary function that depends on the transforms.

    It is -1/2 sum_m sum_i (occ_m mu'_{m,i}^2 - 2 s_{m,i} mu'_{m,i}) / var_{m,i}.
    """
    adapted = adapt_means(means, Ws, classes)
    tot = 0.0
    for m, mu in enumerate(adapted):
        for i in range(len(mu)):
            tot += (occ[m] * mu[i] * mu[i] - 2.0 * s[m][i] * mu[i]) / variances[m][i]
    return -0.5 * tot
