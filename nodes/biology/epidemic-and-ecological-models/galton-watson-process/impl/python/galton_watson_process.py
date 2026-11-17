# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/galton-watson-process/. The authors are listed in prov/1ZKR7A.jsonl.
"""The Galton-Watson branching process.

An offspring distribution is a list p with p[k] = P(one individual has k
children), for k = 0, 1, ..., len(p) - 1. Its probability generating
function is f(s) = sum of p[k] s^k. The process starts with Z_0 individuals,
and Z_(t+1) is the sum of Z_t independent draws from p.

The functions take plain floats or fractions.Fraction values. With Fraction
input, offspring_mean, offspring_variance, pgf and generation_pmf are exact.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Callable, List, Sequence

from biostoch import categorical, poisson


def pgf(p: Sequence, s):
    """f(s) = sum of p[k] s^k, by Horner's rule."""
    acc = 0 * s
    for pk in reversed(p):
        acc = acc * s + pk
    return acc


def offspring_mean(p: Sequence):
    """m = sum of k p[k]."""
    return sum(k * pk for k, pk in enumerate(p))


def offspring_variance(p: Sequence):
    """sigma^2 = sum of k^2 p[k] - m^2."""
    m = offspring_mean(p)
    return sum(k * k * pk for k, pk in enumerate(p)) - m * m


def generation_mean(m, n: int, z0: int = 1):
    """E[Z_n] = z0 m^n."""
    return z0 * m ** n


def generation_variance(m, var, n: int, z0: int = 1):
    """Var(Z_n) for Z_0 = z0: z0 var m^(n-1) (m^n - 1) / (m - 1), or z0 n var if m = 1."""
    if n == 0:
        return 0 * var
    if m == 1:
        return z0 * n * var
    return z0 * var * m ** (n - 1) * (m ** n - 1) / (m - 1)


def extinction_probability(f: Callable[[float], float], eps: float = 1e-13,
                           max_iter: int = 10 ** 6) -> float:
    """The smallest root of f(s) = s in [0, 1], by q_(n+1) = f(q_n) from q_0 = 0.

    q_n = P(Z_n = 0) increases to the root. The loop stops when one step
    moves q by less than eps, or after max_iter steps. Near m = 1 the steps
    are small long before q is close to the root; see the page.
    """
    q = 0.0  # @line L1
    for _ in range(max_iter):  # @line L2
        q_old = q  # @line L3
        q = f(q_old)  # @line L4
        if q - q_old < eps:  # @line L5
            break
    return q  # @line L6


def poisson_pgf(m: float) -> Callable[[float], float]:
    """f(s) = exp(m (s - 1)) for Poisson(m) offspring."""
    return lambda s: math.exp(m * (s - 1.0))


def _poly_mul(a: List, b: List) -> List:
    out = [0 * a[0]] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def generation_pmf(p: Sequence, n: int, z0: int = 1) -> List:
    """The exact law of Z_n as a list: entry k is P(Z_n = k).

    The generating function of Z_n is f composed with itself n times, raised
    to the power z0. Each composition substitutes the current polynomial g
    into f, so the degree is (len(p) - 1)^n z0; use it for small cases.
    """
    one = p[0] - p[0] + 1
    g = [0 * one, one]  # g(s) = s
    for _ in range(n):
        # f(g(s)) by Horner's rule on polynomials.
        acc = [0 * one]
        for pk in reversed(p):
            acc = _poly_mul(acc, g)
            acc[0] += pk
        g = acc
    out = [one]
    for _ in range(z0):
        out = _poly_mul(out, g)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def simulate(rng, p: Sequence[float], generations: int, z0: int = 1,
             cap: int = 10 ** 6) -> List[int]:
    """One path Z_0, Z_1, ... of the process with offspring law p.

    Draw order: in each generation, one categorical draw per individual, in
    order. The path stops early at extinction (Z = 0) or when Z exceeds cap.
    """
    z = z0  # @line L7
    path = [z]
    weights = [float(x) for x in p]
    for _ in range(generations):  # @line L8
        z = sum(categorical(rng, weights) for _ in range(z))  # @line L9
        path.append(z)  # @line L10
        if z == 0 or z > cap:  # @line L11
            return path
    return path  # @line L12


def simulate_poisson(rng, m: float, generations: int, z0: int = 1,
                     cap: int = 10 ** 6) -> List[int]:
    """One path with Poisson(m) offspring.

    The sum of z independent Poisson(m) counts is Poisson(m z), so each
    generation takes one biostoch.poisson draw with mean m z.
    """
    z = z0
    path = [z]
    for _ in range(generations):
        z = poisson(rng, m * z)
        path.append(z)
        if z == 0 or z > cap:
            return path
    return path


def smallest_root_quadratic(p: Sequence[Fraction]) -> Fraction:
    """The exact extinction probability when p has length 3 (at most two children).

    f(s) = s is p2 s^2 + (p1 - 1) s + p0 = 0, with the root s = 1. The other
    root is p0 / p2 (the product of the roots), and q is the smaller of the
    two in [0, 1]. If p2 = 0 the process cannot grow, and q = 1 unless p1 = 1.
    """
    p0, p1, p2 = p
    if p1 == 1:
        return Fraction(0)
    if p2 == 0:
        return Fraction(1)
    return min(Fraction(1), Fraction(p0) / Fraction(p2))
