# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-gauss-transform/. The authors are listed in prov/PHV9XM.jsonl.
"""Fast Gauss transform of Greengard and Strain, in 2D.

Sources s[j] with weights q[j] and targets t[i] are points (complex numbers)
of the unit square. The output is

    G(t_i) = sum_j q_j exp(-|t_i - s_j|^2 / delta).

The square is cut into boxes of side sqrt(delta) / 2. In the scaled
coordinates x / sqrt(delta), each coordinate of the Gaussian has the
Hermite expansion about a source center and the Taylor expansion about a
target center,

    exp(-(u - v)^2) = sum_n v^n / n! h_n(u) = sum_n u^n / n! h_n(v),

with the Hermite functions h_n(x) = (-1)^n d^n/dx^n exp(-x^2). A pair of
boxes is handled in one of four ways, set by the number of sources and
targets in the boxes: direct, sources to Taylor, Hermite to targets, or
Hermite to Taylor. Boxes more than n_range boxes apart in a coordinate are
skipped; their terms are below exp(-n_range^2 / 4).
"""

import math
from typing import Optional, Sequence


def hermite_functions(n: int, x: float) -> list[float]:
    """h_0(x), ..., h_{n-1}(x) by h_{k+1} = 2 x h_k - 2 k h_{k-1}."""
    h = [math.exp(-x * x), 2 * x * math.exp(-x * x)][:n]
    while len(h) < n:
        k = len(h) - 1
        h.append(2 * x * h[k] - 2 * k * h[k - 1])
    return h


def powers_over_factorial(n: int, x: float) -> list[float]:
    """x^k / k! for k = 0..n-1."""
    out = [1.0]
    for k in range(1, n):
        out.append(out[-1] * x / k)
    return out[:n]


def direct(q: Sequence[float], s: Sequence[complex], t: Sequence[complex], delta: float) -> list[float]:
    """Direct summation over all source and target pairs: the reference."""
    return [sum(qj * math.exp(-abs(ti - sj) ** 2 / delta) for qj, sj in zip(q, s)) for ti in t]


def fgt(q: Sequence[float], s: Sequence[complex], t: Sequence[complex], delta: float, p: int = 8,
        n_range: int = 8, n_f: Optional[int] = None, m_l: Optional[int] = None):
    """G(t_i) with p terms per coordinate in every expansion.

    A source box is "big" if it holds more than n_f sources, a target box if
    it holds more than m_l targets (both default to p). Returns (G, stats)
    with the number of box pairs handled in each of the four ways.
    """
    if n_f is None:
        n_f = p
    if m_l is None:
        m_l = p
    sd = math.sqrt(delta)
    h = sd / 2
    nb = max(1, math.ceil(1 / h))

    def key(z: complex) -> tuple[int, int]:
        return (min(int(z.real / h), nb - 1), min(int(z.imag / h), nb - 1))

    def center(k: tuple[int, int]) -> complex:
        return complex((k[0] + 0.5) * h, (k[1] + 0.5) * h)

    src: dict[tuple[int, int], list[int]] = {}
    for j, z in enumerate(s):
        src.setdefault(key(z), []).append(j)
    tgt: dict[tuple[int, int], list[int]] = {}
    for i, z in enumerate(t):
        tgt.setdefault(key(z), []).append(i)
    fact = [math.factorial(k) for k in range(p)]
    herm: dict[tuple[int, int], list[float]] = {}
    for b, idx in src.items():
        if len(idx) > n_f:  # @line L1
            c = center(b)
            a = [0.0] * (p * p)
            for j in idx:
                px = powers_over_factorial(p, (s[j].real - c.real) / sd)
                py = powers_over_factorial(p, (s[j].imag - c.imag) / sd)
                for a1 in range(p):
                    for a2 in range(p):
                        a[a1 * p + a2] += q[j] * px[a1] * py[a2]
            herm[b] = a
    g = [0.0] * len(t)
    taylor: dict[tuple[int, int], list[float]] = {}
    stats = {"direct": 0, "s2l": 0, "h2t": 0, "h2l": 0}
    for cb, tidx in tgt.items():
        big_t = len(tidx) > m_l
        cc = center(cb)
        if big_t:
            taylor[cb] = [0.0] * (p * p)
        near = [(cb[0] + dx, cb[1] + dy) for dx in range(-n_range, n_range + 1)
                for dy in range(-n_range, n_range + 1)]
        for b in near:
            sidx = src.get(b)
            if sidx is None:
                continue
            big_s = b in herm
            if not big_s and not big_t:  # @line L2
                for i in tidx:
                    g[i] += sum(q[j] * math.exp(-abs(t[i] - s[j]) ** 2 / delta) for j in sidx)
                stats["direct"] += 1
            elif not big_s:  # @line L3
                bc = taylor[cb]
                for j in sidx:
                    hx = hermite_functions(p, (s[j].real - cc.real) / sd)
                    hy = hermite_functions(p, (s[j].imag - cc.imag) / sd)
                    for b1 in range(p):
                        for b2 in range(p):
                            bc[b1 * p + b2] += q[j] * hx[b1] * hy[b2] / (fact[b1] * fact[b2])
                stats["s2l"] += 1
            elif not big_t:  # @line L4
                a = herm[b]
                c = center(b)
                for i in tidx:
                    hx = hermite_functions(p, (t[i].real - c.real) / sd)
                    hy = hermite_functions(p, (t[i].imag - c.imag) / sd)
                    g[i] += sum(a[a1 * p + a2] * hx[a1] * hy[a2] for a1 in range(p) for a2 in range(p))
                stats["h2t"] += 1
            else:  # @line L5
                a = herm[b]
                w = (cc - center(b)) / sd
                hx = hermite_functions(2 * p - 1, w.real)
                hy = hermite_functions(2 * p - 1, w.imag)
                tmp = [[sum(hy[a2 + b2] * a[a1 * p + a2] for a2 in range(p)) for b2 in range(p)] for a1 in range(p)]
                bc = taylor[cb]
                for b1 in range(p):
                    for b2 in range(p):
                        val = sum(hx[a1 + b1] * tmp[a1][b2] for a1 in range(p))
                        bc[b1 * p + b2] += (-1) ** (b1 + b2) * val / (fact[b1] * fact[b2])
                stats["h2l"] += 1
    for cb, bc in taylor.items():
        cc = center(cb)
        for i in tgt[cb]:  # @line L6
            ux = (t[i].real - cc.real) / sd
            uy = (t[i].imag - cc.imag) / sd
            px = [ux ** k for k in range(p)]
            py = [uy ** k for k in range(p)]
            g[i] += sum(bc[b1 * p + b2] * px[b1] * py[b2] for b1 in range(p) for b2 in range(p))
    return g, stats  # @line L7
