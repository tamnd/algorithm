# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-phase/. The authors are listed in prov/DG68QC.jsonl.

"""Zero flipping for FIR filters with real coefficients.

A filter is given as a list of real factors in w = z^(-1):
  (c0, c1)      the factor c0 + c1 w, one real zero z = -c1 / c0;
  (c0, c1, c2)  the factor c0 + c1 w + c2 w^2 with c1^2 < 4 c0 c2,
                a pair of complex zeros of modulus (c2 / c0)^(1/2).
Reversing the coefficients of a factor moves its zeros z to 1 / conj(z)
and keeps |H(e^(iw))|. The minimum-phase choice keeps every zero strictly
inside the unit circle. Coefficients may be int or Fraction; all is exact.
"""

from fractions import Fraction
from itertools import product
from typing import Sequence


def poly_mul(p: Sequence, q: Sequence) -> list:
    out = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, u in enumerate(p):
        for j, v in enumerate(q):
            out[i + j] += u * v
    return out


def flip(f: Sequence) -> tuple:
    """Reverse the coefficients: the zeros z go to 1 / conj(z)."""
    return tuple(reversed(f))


def zeros_inside(f: Sequence) -> bool:
    """True if the zeros of the factor are strictly inside the unit circle."""
    return abs(f[-1]) < abs(f[0])


def expand(factors: Sequence[Sequence]) -> list:
    h = [Fraction(1)]
    for f in factors:
        h = poly_mul(h, f)
    return h


def variants(factors: Sequence[Sequence]) -> list[tuple[tuple[bool, ...], list]]:
    """All 2^k filters obtained by flipping any subset of the k factors."""
    out = []
    for mask in product((False, True), repeat=len(factors)):
        chosen = [flip(f) if m else tuple(f) for f, m in zip(factors, mask)]
        out.append((mask, expand(chosen)))
    return out


def minimum_phase(factors: Sequence[Sequence]) -> list:
    """The variant with every zero inside the unit circle. Zeros on the circle are not allowed."""
    chosen = []
    for f in factors:
        if abs(f[-1]) == abs(f[0]):
            raise ValueError("a zero on the unit circle has no minimum-phase choice")
        chosen.append(tuple(f) if zeros_inside(f) else flip(f))
    return expand(chosen)


def autocorrelation(h: Sequence) -> list:
    """r[k] = sum_n h[n] h[n + k] for k = 0..len(h) - 1. It fixes |H|^2 for a real h."""
    return [sum(h[n] * h[n + k] for n in range(len(h) - k)) for k in range(len(h))]


def partial_energy(h: Sequence) -> list:
    """E[n] = h[0]^2 + ... + h[n]^2."""
    out, acc = [], Fraction(0)
    for v in h:
        acc += v * v
        out.append(acc)
    return out


def inverse_response(h: Sequence, count: int) -> list:
    """The first count samples of the causal inverse 1 / H."""
    g: list = []
    for n in range(count):
        acc = Fraction(1 if n == 0 else 0)
        acc -= sum(h[k] * g[n - k] for k in range(1, len(h)) if n - k >= 0)
        g.append(acc / h[0])
    return g
