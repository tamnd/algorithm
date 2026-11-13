# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rls-algorithm/. The authors are listed in prov/BJHGVT.jsonl.

"""The recursive least squares (RLS) adaptive filter.

After the samples 0..n, the taps w minimize the exponentially weighted cost

    sum_{i=0}^{n} lam^(n-i) (d[i] - w^T u_i)^2 + lam^(n+1) delta |w|^2,

where u_i = (x[i], ..., x[i-M+1]), lam in (0, 1] is the forgetting factor and
delta > 0 sets the start value P = I / delta. The matrix P is the inverse of
the weighted correlation matrix, kept up to date by the Sherman-Morrison
formula, so each sample costs O(M^2). With Fraction inputs every value is
exact.
"""

from typing import Sequence


def rls_update(w: Sequence, p: Sequence[Sequence], u: Sequence, d, lam) -> tuple[list, list, object]:
    """One RLS step on regressor u and desired value d. Returns (w_new, P_new, a priori error)."""
    m = len(u)
    pi = [sum(p[i][j] * u[j] for j in range(m)) for i in range(m)]  # @line L4
    denom = lam + sum(u[i] * pi[i] for i in range(m))
    k = [v / denom for v in pi]  # @line L5
    xi = d - sum(w[i] * u[i] for i in range(m))  # @line L6
    w_new = [w[i] + k[i] * xi for i in range(m)]  # @line L7
    p_new = [[(p[i][j] - k[i] * pi[j]) / lam for j in range(m)] for i in range(m)]  # @line L8
    return w_new, p_new, xi


def rls(x: Sequence, d: Sequence, m: int, lam, delta) -> tuple[list, list, list]:
    """Run an M-tap RLS filter. Samples before x[0] are zero.

    Returns the final taps, the final P and the a priori errors.
    """
    if m < 1 or len(x) != len(d):
        raise ValueError("need m >= 1 and len(x) == len(d)")
    if not (0 < lam <= 1) or not delta > 0:
        raise ValueError("need 0 < lam <= 1 and delta > 0")
    zero = 0 * delta
    w = [zero] * m  # @line L1
    p = [[(1 / delta if i == j else zero) for j in range(m)] for i in range(m)]
    errors = []
    for n in range(len(x)):  # @line L2
        u = [x[n - k] if n - k >= 0 else zero for k in range(m)]  # @line L3
        w, p, xi = rls_update(w, p, u, d[n], lam)
        errors.append(xi)
    return w, p, errors  # @line L9
