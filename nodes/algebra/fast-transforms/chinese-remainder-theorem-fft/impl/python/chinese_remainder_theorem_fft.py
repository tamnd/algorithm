# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chinese-remainder-theorem-fft/. The authors are listed in prov/XHJRTQ.jsonl.

import math
from itertools import product
from typing import TypeVar

S = TypeVar("S", int, complex)


def _power(w: S, e: int, p: int | None) -> S:
    return pow(w, e, p) if p is not None else w**e


def good_thomas(x: list[S], factors: list[int], w: S, p: int | None = None) -> list[S]:
    """Return the DFT X[k] = sum of x[j] * w**(j*k) by the Good-Thomas prime-factor algorithm.

    Precondition: the factors are pairwise coprime positive integers whose
    product n equals len(x), and w is a principal n-th root of unity, a
    complex number such as exp(-2j*pi/n) when p is None, or an integer
    modulo the prime p (then all arithmetic is modulo p).
    The data are re-indexed by the Chinese remainder theorem so that the DFT
    becomes a multidimensional DFT of shape factors, with no twiddle factors.
    Each short DFT of length m is done directly here. Cost: n * sum(factors)
    ring multiplications and n * sum(factors - 1) additions, plus O(n r)
    index operations for r factors.
    """
    n = math.prod(factors)
    if n != len(x) or any(m < 1 for m in factors):
        raise ValueError("the product of the factors must equal len(x)")
    for i, a in enumerate(factors):
        for b in factors[i + 1:]:
            if math.gcd(a, b) != 1:
                raise ValueError("the factors must be pairwise coprime")
    big = [n // m for m in factors]  # @line L1
    e = [pow(big[i], -1, m) if m > 1 else 0 for i, m in enumerate(factors)]
    a = [x[sum(big_i * j_i for big_i, j_i in zip(big, js)) % n] for js in product(*map(range, factors))]  # @line L2
    stride = n
    for i, m in enumerate(factors):  # @line L3
        stride //= m
        if m == 1:
            continue
        r = [_power(w, big[i] * q, p) for q in range(m)]
        for hi in range(0, n, m * stride):
            for lo in range(stride):
                base = hi + lo
                line = [a[base + t * stride] for t in range(m)]
                for k in range(m):  # @line L4
                    acc = line[0]
                    for j in range(1, m):
                        acc += line[j] * r[(j * k) % m]
                    a[base + k * stride] = acc % p if p is not None else acc
    out: list[S] = [a[0]] * n
    for flat, ks in enumerate(product(*map(range, factors))):  # @line L5
        out[sum(big_i * e_i * k_i for big_i, e_i, k_i in zip(big, e, ks)) % n] = a[flat]
    return out  # @line L6


def inverse_good_thomas(big_x: list[S], factors: list[int], w: S, p: int | None = None) -> list[S]:
    """Return x with good_thomas(x, factors, w, p) == big_x.

    Same preconditions; n must be a unit (always true for complex numbers,
    and for a prime p not dividing n). Cost: one good_thomas and n scalings.
    """
    n = len(big_x)
    if p is not None:
        y = good_thomas(big_x, factors, pow(w, -1, p), p)
        inv_n = pow(n, -1, p)
        return [v * inv_n % p for v in y]
    y = good_thomas(big_x, factors, 1 / w)
    return [v / n for v in y]
