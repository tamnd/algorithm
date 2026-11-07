# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goertzel-algorithm/. The authors are listed in prov/R480RJ.jsonl.

"""One DFT bin X_k = sum_j x_j w**(j*k) by Goertzel's second-order recurrence."""

from __future__ import annotations

import cmath
import math
from typing import TypeVar

S = TypeVar("S", int, complex)


def _unit(r: int, n: int) -> complex:
    """Return exp(2*pi*i*r/n), exact when r/n is a multiple of 1/4."""
    r %= n
    if (4 * r) % n == 0:
        return (1 + 0j, 1j, -1 + 0j, -1j)[4 * r // n]
    return cmath.exp(2j * math.pi * r / n)


def goertzel(x: list[S], k: int, w: int | None = None, p: int | None = None) -> S:
    """Return X_k = sum_j x[j] * w**(j*k) for one index k.

    Over C (p is None) the root is w = exp(-2*pi*i/n) and w is ignored.
    Modulo a prime p, w must be an element with w**n = 1 (mod p); the
    entries of x are residues. Any length n >= 1 is allowed.
    """
    n = len(x)
    if n == 0:
        raise ValueError("the input must not be empty")
    if p is None:
        z = _unit(k, n)  # @line L1  z = w**(-k) = exp(2*pi*i*k/n)
        c = 2.0 * z.real  # @line L2  c = z + 1/z = 2 cos(2*pi*k/n), a real number
        s1 = s2 = 0.0  # @line L3
        for xj in x:  # @line L4
            s = xj + c * s1 - s2  # @line L5
            s2, s1 = s1, s  # @line L6
        return z * s1 - s2  # @line L7
    if w is None or pow(w, n, p) != 1:
        raise ValueError("w must satisfy w**n = 1 modulo p")
    z = pow(w, (-k) % n, p)
    c = (z + pow(w, k % n, p)) % p
    s1 = s2 = 0
    for xj in x:
        s = (xj + c * s1 - s2) % p
        s2, s1 = s1, s
    return (z * s1 - s2) % p
