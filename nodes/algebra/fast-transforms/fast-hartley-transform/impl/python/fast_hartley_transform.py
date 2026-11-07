# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-hartley-transform/. The authors are listed in prov/JPR6KM.jsonl.

import math


def fht(x: list[float]) -> None:
    """Replace x by its discrete Hartley transform, H[k] = sum x[j] cas(2 pi j k / n).

    Precondition: n = len(x) is a power of two and the entries are real.
    Bracewell's radix-2 decimation-in-time algorithm, iterative and in place.
    Cost: n lg n - 3n + 4 multiplications and (3/2) n lg n - (3/2) n + 2
    additions for n >= 2, plus the n/2 cosine and sine evaluations.
    """
    n = len(x)  # @line L1
    if n < 1 or n & (n - 1):
        raise ValueError("the length must be a power of two")
    t = n.bit_length() - 1
    rev = [0] * n
    for j in range(1, n):
        rev[j] = (rev[j >> 1] >> 1) | ((j & 1) << (t - 1))
    for j in range(n):  # @line L2
        if j < rev[j]:
            x[j], x[rev[j]] = x[rev[j]], x[j]
    h = 1  # @line L3
    while h < n:  # @line L4
        for s in range(0, n, 2 * h):  # @line L5
            u, v = x[s], x[s + h]
            x[s], x[s + h] = u + v, u - v  # @line L6
            if h >= 2:  # @line L7
                q = h // 2
                u, v = x[s + q], x[s + h + q]
                x[s + q], x[s + h + q] = u + v, u - v
            for k in range(1, h // 2):  # @line L8
                c, sn = math.cos(math.pi * k / h), math.sin(math.pi * k / h)  # @line L9
                a, b = x[s + h + k], x[s + 2 * h - k]
                t1, t2 = c * a + sn * b, sn * a - c * b  # @line L10
                e1, e2 = x[s + k], x[s + h - k]  # @line L11
                x[s + k], x[s + h + k] = e1 + t1, e1 - t1  # @line L12
                x[s + h - k], x[s + 2 * h - k] = e2 + t2, e2 - t2  # @line L13
        h *= 2  # @line L14


def inverse_fht(y: list[float]) -> None:
    """Replace y by the x with fht(x) == y. Cost: one fht and n divisions."""
    fht(y)  # @line L15
    n = len(y)
    for j in range(n):  # @line L16
        y[j] /= n


def dft_from_dht(big_h: list[float]) -> list[complex]:
    """Return the DFT X[k] = sum x[j] exp(-2 pi i j k / n) from H = DHT(x). Cost: O(n)."""
    n = len(big_h)
    return [
        complex((big_h[k] + big_h[-k % n]) / 2, -(big_h[k] - big_h[-k % n]) / 2)
        for k in range(n)
    ]


def real_cyclic_convolution(a: list[float], b: list[float]) -> list[float]:
    """Cyclic convolution of two real vectors of the same power-of-two length by FHTs.

    Uses the Hartley convolution theorem. Cost: three FHTs and O(n) further operations.
    """
    n = len(a)
    if len(b) != n:
        raise ValueError("the vectors must have the same length")
    ha, hb = [float(v) for v in a], [float(v) for v in b]
    fht(ha)
    fht(hb)
    hz = [
        (ha[k] * (hb[k] + hb[-k % n]) + ha[-k % n] * (hb[k] - hb[-k % n])) / 2
        for k in range(n)
    ]
    inverse_fht(hz)
    return hz
