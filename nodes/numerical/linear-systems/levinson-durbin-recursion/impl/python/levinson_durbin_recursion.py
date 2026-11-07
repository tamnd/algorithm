# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/levinson-durbin-recursion/. The authors are listed in prov/XXKK03.jsonl.

"""The Levinson-Durbin recursion for symmetric Toeplitz systems.

T is the symmetric Toeplitz matrix with first row (r[0], r[1], ..., r[n-1]),
so T[i][j] = r[|i - j|]. durbin() solves the Yule-Walker equations
T_n y = -(r[1], ..., r[n]) and levinson() solves T x = b; both run in
O(n^2) flops and O(n) storage. Entries may be floats or Fractions.
Standard library only.
"""


class NotPositiveDefinite(ValueError):
    """Some reflection coefficient has |alpha| >= 1, so T is not positive definite."""


class Breakdown(ZeroDivisionError):
    """A leading principal minor is zero, so the recursion cannot continue."""


def _check(beta, check_pd, k):
    if check_pd and beta <= 0:
        raise NotPositiveDefinite("leading minor of order %d is not positive" % (k + 1))
    if beta == 0:
        raise Breakdown("leading minor of order %d is zero" % (k + 1))


def durbin(r, check_pd=True, stats=None):
    """Solve T_n y = -(r[1], ..., r[n]) where T_n has first row r[0..n-1], r[0] = 1.

    r has length n + 1. Returns (y, alphas, betas): alphas[k] is the reflection
    coefficient (the last entry of the order k+1 solution) and
    betas[k] = det T_{k+1} / det T_k for k = 0..n-1. Cost 2 n^2 + 2 n - 4 flops.
    """
    n = len(r) - 1
    if n <= 0:
        return [], [], []
    if r[0] != 1:
        raise ValueError("normalize so that r[0] = 1")
    one = r[0]
    flops = 0
    y = [-r[1]]  # @line L1
    alpha, beta = -r[1], one
    alphas, betas = [alpha], [beta]
    for k in range(1, n):  # @line L2
        beta = (one - alpha * alpha) * beta  # @line L3
        flops += 3
        _check(beta, check_pd, k)
        s = r[k + 1]
        for j in range(k):  # @line L4
            s = s + r[k - j] * y[j]
        alpha = -s / beta
        flops += 2 * k + 1
        y = [y[j] + alpha * y[k - 1 - j] for j in range(k)] + [alpha]  # @line L5
        flops += 2 * k
        alphas.append(alpha)
        betas.append(beta)
    if stats is not None:
        stats["flops"] = flops
    return y, alphas, betas


def levinson(r, b, check_pd=True, stats=None):
    """Solve T x = b with T[i][j] = r[|i - j|], T of order n = len(b), r of length >= n.

    Any r[0] != 0 is allowed (the system is scaled by 1/r[0]). With check_pd,
    raise NotPositiveDefinite unless T is positive definite; otherwise raise
    Breakdown only at an exactly zero leading minor. Cost 4 n^2 + O(n) flops.
    With integer entries and r[0] != 1 the scaling produces floats; pass
    Fractions for exact results.
    """
    n = len(b)
    if n == 0:
        return []
    r0 = r[0]
    if check_pd and r0 <= 0:
        raise NotPositiveDefinite("r[0] must be positive")
    if r0 == 0:
        raise Breakdown("r[0] is zero")
    if r0 == 1:  # @line L6
        rr, bb, flops = list(r[:n]), list(b), 0
    else:
        rr = [r0 / r0] + [v / r0 for v in r[1:n]]
        bb = [v / r0 for v in b]
        flops = 2 * n - 1
    one = rr[0]
    x = [bb[0]]  # @line L7
    if n == 1:
        if stats is not None:
            stats["flops"] = flops
        return x
    y = [-rr[1]]
    alpha, beta = -rr[1], one
    for k in range(1, n):  # @line L8
        beta = (one - alpha * alpha) * beta  # @line L9
        flops += 3
        _check(beta, check_pd, k)
        s = bb[k]
        for j in range(k):  # @line L10
            s = s - rr[j + 1] * x[k - 1 - j]
        mu = s / beta
        flops += 2 * k + 1
        x = [x[j] + mu * y[k - 1 - j] for j in range(k)] + [mu]  # @line L11
        flops += 2 * k
        if k < n - 1:  # @line L12
            s = rr[k + 1]
            for j in range(k):
                s = s + rr[j + 1] * y[k - 1 - j]
            alpha = -s / beta
            y = [y[j] + alpha * y[k - 1 - j] for j in range(k)] + [alpha]  # @line L13
            flops += 4 * k + 1
    if stats is not None:
        stats["flops"] = flops
    return x  # @line L14


def toeplitz_from_reflections(alphas, one=1):
    """Return r[0..n] with r[0] = 1 whose Durbin reflection coefficients are alphas.

    Any alphas with |alpha| < 1 give a positive definite Toeplitz matrix
    (the step-up recursion of linear prediction). Exact with Fractions.
    """
    n = len(alphas)
    r = [one]
    if n == 0:
        return r
    r.append(-alphas[0])
    y, beta = [alphas[0]], one
    for k in range(1, n):
        a = alphas[k]
        beta = (one - y[-1] * y[-1]) * beta
        s = sum(r[k - j] * y[j] for j in range(k))
        r.append(-a * beta - s)
        y = [y[j] + a * y[k - 1 - j] for j in range(k)] + [a]
    return r


def toeplitz(r, n):
    return [[r[abs(i - j)] for j in range(n)] for i in range(n)]
