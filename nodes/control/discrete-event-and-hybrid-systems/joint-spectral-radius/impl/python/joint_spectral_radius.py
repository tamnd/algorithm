# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/joint-spectral-radius/. The authors are listed in prov/5Q24WE.jsonl.

"""Bounds on the joint spectral radius by brute force over products.

For a finite set M of n by n real matrices, the joint spectral radius is

    rho(M) = lim_k max over products P of length k of ||P||^(1/k).

For every length k and every product P of length k,

    rho(P)^(1/k) <= rho(M) <= max over products Q of length k of ||Q||^(1/k),

so the products of length 1, ..., K give an interval that contains rho(M).
The number of products of length k is |M|^k, so K must stay small.

The norm is the induced 2-norm (ctlmat.norm2). The spectral radius of a
product is the largest modulus of a root of its characteristic polynomial.
"""

import math

from ctlmat import charpoly, eye, mul, norm2, polyroots

__all__ = ["spectral_radius", "products", "jsr_bounds"]


def spectral_radius(a):
    """Return the largest modulus of an eigenvalue of the square matrix a."""
    roots = polyroots(charpoly(a))
    return max((abs(z) for z in roots), default=0.0)


def products(mats, k):
    """Return all products A_(i_k) ... A_(i_1) of length k, as a list."""
    n = len(mats[0])
    out = [eye(n)]
    for _ in range(k):
        out = [mul(a, p) for p in out for a in mats]
    return out


def jsr_bounds(mats, kmax):
    """Return (lower, upper) with lower <= rho(mats) <= upper.

    The bounds use the products of length 1 to kmax. lower is the largest
    value of rho(P)^(1/k) and upper the smallest value of max ||P||^(1/k) found.
    """
    if not mats or kmax < 1:
        raise ValueError("need at least one matrix and kmax >= 1")
    n = len(mats[0])
    if any(len(a) != n or any(len(row) != n for row in a) for a in mats):
        raise ValueError("all matrices must be n by n")
    lo, hi = 0.0, math.inf  # @line L1
    prods = [eye(n)]  # @line L1
    for k in range(1, kmax + 1):  # @line L2
        prods = [mul(a, p) for p in prods for a in mats]  # @line L3
        lo = max(lo, max(spectral_radius(p) for p in prods) ** (1.0 / k))  # @line L4
        hi = min(hi, max(norm2(p) for p in prods) ** (1.0 / k))  # @line L5
    return lo, hi  # @line L6
