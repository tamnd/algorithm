# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-hard-thresholding/. The authors are listed in prov/M2CY6N.jsonl.
"""Iterative hard thresholding (IHT) for y = A x + e with an s-sparse x.

A is a list of m rows of length n. The iteration is
x <- H_s(x + mu A^T (y - A x)), where H_s keeps the s entries of largest
magnitude. The plain form of Blumensath and Davies uses mu = 1.
"""

from imgla import matvec, norm2, rmatvec


def hard_threshold(v, s):
    """H_s(v): keep the s entries of largest magnitude, set the others to 0.

    Ties are broken by the lower index, so the result is deterministic.
    """
    keep = sorted(range(len(v)), key=lambda i: (-abs(v[i]), i))[:s]
    out = [0.0] * len(v)
    for i in keep:
        out[i] = v[i]
    return out


def iht(a, y, s, iters=500, mu=1.0, x0=None, tol=0.0):
    """Run IHT and return (x, residual_norms).

    residual_norms[k] is ||y - A x^k|| for k = 0, 1, ..., so it has one more
    entry than the number of steps taken. The loop stops early when the
    residual is at most tol.
    """
    n = len(a[0])
    x = list(x0) if x0 is not None else [0.0] * n  # @line L1
    res = [norm2([yi - ai for yi, ai in zip(y, matvec(a, x))])]
    for _ in range(iters):  # @line L2
        if res[-1] <= tol:
            break
        r = [yi - ai for yi, ai in zip(y, matvec(a, x))]  # @line L3
        g = rmatvec(a, r)  # @line L4
        x = hard_threshold([xi + mu * gi for xi, gi in zip(x, g)], s)  # @line L5
        res.append(norm2([yi - ai for yi, ai in zip(y, matvec(a, x))]))
    return x, res  # @line L6
