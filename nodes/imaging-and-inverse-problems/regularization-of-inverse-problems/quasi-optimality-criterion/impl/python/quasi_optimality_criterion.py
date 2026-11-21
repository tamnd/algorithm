# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quasi-optimality-criterion/. The authors are listed in prov/4809JZ.jsonl.
"""The quasi-optimality criterion of Tikhonov and Glasko, in its discrete form.

Tikhonov: x_alpha minimizes ||A x - y||^2 + alpha ||x||^2. On the geometric
grid alpha_j = alpha_0 q^j (0 < q < 1, j = 0..N), the rule picks the alpha_j
for which ||x_{alpha_{j+1}} - x_{alpha_j}|| is smallest. With the thin SVD,
x_alpha = sum_i s_i b_i / (s_i^2 + alpha) v_i, so the distance needs only
the coefficients s_i b_i.
"""

import math

from imgla import norm2, svd


def coefficients(u, s, y):
    """b_i = <u_i, y> for the s_i > 0."""
    m = len(y)
    return [sum(u[i][k] * y[i] for i in range(m)) for k in range(len(s)) if s[k] > 0.0]


def step_norm(s, b, a1, a2):
    """||x_{a2} - x_{a1}|| from the SVD data."""
    tot = 0.0
    for si, bi in zip(s, b):
        d = si * bi * (1.0 / (si * si + a2) - 1.0 / (si * si + a1))
        tot += d * d
    return math.sqrt(tot)


def tikhonov_svd(s, v, b, alpha):
    """x_alpha = sum_i s_i b_i / (s_i^2 + alpha) v_i."""
    n = len(v)
    x = [0.0] * n
    for k, (si, bi) in enumerate(zip(s, b)):
        c = si * bi / (si * si + alpha)
        for j in range(n):
            x[j] += c * v[j][k]
    return x


def quasi_optimality(u, s, v, y, alpha0=None, q=0.5, count=None):
    """Return (alpha, x, j, d) for the discrete quasi-optimality rule.

    The grid is alpha_j = alpha0 q^j for j = 0..count. By default alpha0 = s_1^2
    and the grid stops at the first alpha_j below s_r^2. d[j] is
    ||x_{alpha_{j+1}} - x_{alpha_j}|| and j is the index of the smallest d[j].
    """
    s = [si for si in s if si > 0.0]
    b = coefficients(u, s, y)  # @line L1
    if alpha0 is None:
        alpha0 = s[0] ** 2
    if count is None:
        count = max(1, math.ceil(math.log(s[-1] ** 2 / alpha0) / math.log(q)))
    alphas = [alpha0 * q ** j for j in range(count + 1)]  # @line L2
    d = [step_norm(s, b, alphas[j], alphas[j + 1]) for j in range(count)]  # @line L3
    j = min(range(count), key=lambda i: d[i])  # @line L4
    alpha = alphas[j]
    return alpha, tikhonov_svd(s, v, b, alpha), j, d  # @line L5


def quasi_optimality_matrix(a, y, **kw):
    """The same for a dense matrix: compute the SVD, then call quasi_optimality."""
    u, s, v = svd(a)
    return quasi_optimality(u, s, v, y, **kw)


def continuous_measure(s, b, alpha):
    """alpha ||d x_alpha / d alpha||, the continuous form of the criterion.

    d x_alpha / d alpha = -(A^T A + alpha I)^(-1) x_alpha, so the measure is
    sqrt(sum_i (alpha s_i b_i / (s_i^2 + alpha)^2)^2).
    """
    tot = 0.0
    for si, bi in zip(s, b):
        t = alpha * si * bi / (si * si + alpha) ** 2
        tot += t * t
    return math.sqrt(tot)
