# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-entropy-method-imaging/. The authors are listed in prov/DHVCDM.jsonl.
"""Maximum entropy image reconstruction.

The data are y = A x + e with a dense real matrix A (a list of rows),
Gaussian noise of standard deviation sigma_i per datum, and a positive
default image m. The entropy is Skilling's form

    S(x) = sum_j [x_j - m_j - x_j log(x_j / m_j)],

which is at most 0, with the maximum at x = m. The misfit is
chi2(x) = sum_i (y_i - (A x)_i)^2 / sigma_i^2. The method returns the
positive image of largest S with chi2(x) = target (default: the number of
data). For a fixed lambda it minimizes F(x) = -S(x) + (lambda / 2) chi2(x)
by damped Newton steps; an outer bisection on log(lambda) meets the target.
This is a small dense version: Skilling and Bryan (1984) search a subspace
of a few directions instead of taking full Newton steps.
"""

import math

from imgla import matvec, rmatvec, solve


def entropy(x, m):
    """Skilling's entropy S(x) = sum [x - m - x log(x / m)]."""
    return sum(xj - mj - (xj * math.log(xj / mj) if xj > 0 else 0.0) for xj, mj in zip(x, m))


def chi2(x, a, y, sigma):
    """sum_i ((A x)_i - y_i)^2 / sigma_i^2."""
    return sum(((p - q) / s) ** 2 for p, q, s in zip(matvec(a, x), y, sigma))


def objective(x, a, y, sigma, m, lam):
    """F(x) = -S(x) + (lam / 2) chi2(x)."""
    return -entropy(x, m) + 0.5 * lam * chi2(x, a, y, sigma)


def gradient(x, a, y, sigma, m, lam):
    """grad F = log(x / m) + lam A^T W (A x - y), with W = diag(1 / sigma^2)."""
    r = [(p - q) / (s * s) for p, q, s in zip(matvec(a, x), y, sigma)]
    g = rmatvec(a, r)
    return [math.log(xj / mj) + lam * gj for xj, mj, gj in zip(x, m, g)]


def solve_fixed_lambda(a, y, sigma, m, lam, x0=None, tol=1e-16, max_steps=200, history=None):
    """Minimize F for one lambda by Newton steps with backtracking. Returns x > 0.

    If history is a list, the value of F after each step is appended.
    """
    n = len(m)
    x = list(m) if x0 is None else list(x0)
    w = [1.0 / (s * s) for s in sigma]
    # A^T W A, formed once (it does not depend on x).
    atwa = [[sum(a[i][p] * w[i] * a[i][q] for i in range(len(a))) for q in range(n)] for p in range(n)]
    f = objective(x, a, y, sigma, m, lam)
    for _ in range(max_steps):
        g = gradient(x, a, y, sigma, m, lam)  # @line L5
        hess = [[lam * atwa[p][q] + (1.0 / x[p] if p == q else 0.0) for q in range(n)] for p in range(n)]  # @line L6
        d = solve(hess, [-v for v in g])  # @line L7
        dec = -sum(gi * di for gi, di in zip(g, d))
        if dec <= tol * max(1.0, abs(f)):
            break
        t = 1.0  # @line L8
        while True:
            xn = [xi + t * di for xi, di in zip(x, d)]
            if min(xn) > 0:
                fn = objective(xn, a, y, sigma, m, lam)
                if fn <= f - 0.25 * t * dec:
                    break
            t *= 0.5
            if t < 1e-14:
                return x
        x, f = xn, fn
        if history is not None:
            history.append(f)
    return x


def maximum_entropy(a, y, sigma, m, target=None, rel_tol=1e-6, lam_max=1e8, max_bisect=200):
    """The positive image of maximum entropy with chi2 = target (default len(y)).

    Returns (x, lam). Raises ValueError if the target is below the misfit
    reached at lam_max (no positive image fits the data that well).
    """
    if target is None:
        target = float(len(y))
    if chi2(m, a, y, sigma) <= target:
        return list(m), 0.0  # the default image already fits the data
    lo, hi = 0.0, 1.0  # @line L1
    x = solve_fixed_lambda(a, y, sigma, m, hi)
    while chi2(x, a, y, sigma) > target:  # grow the bracket by factors of 10
        if hi >= lam_max:
            raise ValueError("target misfit is below what any positive image reaches")
        lo, hi = hi, 10.0 * hi
        x = solve_fixed_lambda(a, y, sigma, m, hi, x0=x)
    if lo == 0.0:
        lo = hi / 1e6
    for _ in range(max_bisect):  # @line L2
        lam = math.sqrt(lo * hi)  # @line L3
        x = solve_fixed_lambda(a, y, sigma, m, lam, x0=x)  # @line L4
        c = chi2(x, a, y, sigma)
        if abs(c - target) <= rel_tol * target:
            break
        if c > target:  # @line L9
            lo = lam
        else:
            hi = lam
    return x, lam  # @line L10


def circulant_blur_matrix(h):
    """The n x n matrix of periodic convolution with h (h centered at index 0)."""
    n = len(h)
    return [[h[(i - j) % n] for j in range(n)] for i in range(n)]
