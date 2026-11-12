# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sharpness-aware-minimization/. The authors are listed in prov/GSR20V.jsonl.

"""Sharpness-aware minimization (Foret, Kleiner, Mobahi and Neyshabur 2021).

SAM minimizes max_{||eps||_p <= rho} L(w + eps). It approximates the inner
maximizer by the maximizer of the first order Taylor expansion,
    eps_hat = rho sign(g) |g|^(q-1) / (||g||_q^q)^(1/p),   1/p + 1/q = 1,
which is rho g / ||g|| for p = 2, and uses grad L(w + eps_hat) as the
gradient at w (Eq. 3 of the paper drops the second order term). Each step
costs two gradient evaluations.
"""

import math
from fractions import Fraction


def _sqrt(x):
    """Square root; exact for a Fraction that is a perfect square."""
    if isinstance(x, Fraction):
        n, d = math.isqrt(x.numerator), math.isqrt(x.denominator)
        if n * n == x.numerator and d * d == x.denominator:
            return Fraction(n, d)
    return math.sqrt(x)


def p_norm(v, p):
    if p == math.inf:
        return max(abs(a) for a in v)
    if p == 2:
        return _sqrt(sum(a * a for a in v))
    return sum(abs(a) ** p for a in v) ** (1 / p)


def perturbation(g, rho, p=2):
    """eps_hat(w) of Eq. 2: the maximizer of g . eps over ||eps||_p <= rho."""
    if all(a == 0 for a in g):
        return [0 * a for a in g]
    if p == 2:
        n = p_norm(g, 2)
        return [rho * a / n for a in g]
    if p == math.inf:
        return [rho * ((a > 0) - (a < 0)) for a in g]
    q = p / (p - 1)
    s = sum(abs(a) ** q for a in g) ** (1 / p)
    return [rho * math.copysign(abs(a) ** (q - 1), a) / s for a in g]


def sam_gradient(grad, w, rho, p=2):
    """The SAM gradient: the gradient at w + eps_hat, eps_hat from the gradient at w."""
    g = grad(w)
    eps = perturbation(g, rho, p)
    return grad([a + e for a, e in zip(w, eps)])


def sam(grad, w, steps, lr=0.1, rho=0.05, momentum=0.0, p=2):
    """SAM with SGD (and optional heavy ball momentum) as the base optimizer.
    grad(w) is the minibatch gradient at w. Returns the iterates."""
    vel = [0 * a for a in w]  # @line L1
    path = [list(w)]
    for _ in range(steps):  # @line L2
        g = grad(w)  # @line L3
        eps = perturbation(g, rho, p)  # @line L4
        g_sam = grad([a + e for a, e in zip(w, eps)])  # @line L5
        vel = [momentum * v + gs for v, gs in zip(vel, g_sam)]  # @line L6
        w = [a - lr * v for a, v in zip(w, vel)]  # @line L7
        path.append(w)
    return path  # @line L8


def sharpness(loss, w, rho, directions):
    """An estimate from below of max_{||eps|| <= rho} L(w + eps) - L(w) over unit directions."""
    base = loss(w)
    return max(loss([a + rho * d for a, d in zip(w, u)]) - base for u in directions)
