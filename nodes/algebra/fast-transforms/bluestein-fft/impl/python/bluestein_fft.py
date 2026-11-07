# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bluestein-fft/. The authors are listed in prov/GDR6AH.jsonl.

import cmath
import math


def _fft(a: list, w, p: int | None) -> None:
    """Replace a by its DFT with the principal len(a)-th root w, in place.

    Iterative radix-2 Cooley-Tukey; len(a) must be a power of two.
    Modulo p, w is the root itself. Over the complex numbers, w is the sign
    -1 or +1 of the exponent, w = exp(sign 2 pi i / len(a)), and each twiddle
    factor is computed directly so that its error does not grow with its index.
    """
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    h = 1
    while h < n:
        if p is None:
            table = [cmath.exp(w * 1j * math.pi * k / h) for k in range(h)]
        else:
            step = pow(w, n // (2 * h), p)
            table = [1] * h
            for k in range(1, h):
                table[k] = table[k - 1] * step % p
        for s in range(0, n, 2 * h):
            for k in range(h):
                u = a[s + k]
                v = a[s + h + k] * table[k]
                if p is None:
                    a[s + k], a[s + h + k] = u + v, u - v
                else:
                    a[s + k], a[s + h + k] = (u + v) % p, (u - v) % p
        h *= 2


def _chirp_dft(x: list, zeta, zeta_inv, root_m, p: int | None) -> list:
    """Return X[k] = sum_j x[j] zeta^(2jk) by Bluestein's chirp convolution.

    Modulo p, zeta must satisfy zeta^(2n) = 1 with zeta^2 a principal n-th root of
    unity, zeta_inv is its inverse, and root_m is a principal M-th root of unity for
    the power of two M chosen below. Over the complex numbers, zeta is the sign -1
    or +1 of zeta = exp(sign pi i / n), and zeta_inv and root_m are unused; each
    chirp value is computed directly from m^2 mod 2n.
    """
    n = len(x)  # @line L1
    big_m = 1
    while big_m < 2 * n - 1:
        big_m *= 2
    if p is None:  # @line L2
        c = [cmath.exp(zeta * 1j * math.pi * (m * m % (2 * n)) / n) for m in range(n)]
        cb = [c[m].conjugate() for m in range(n)]
        root_m = -1
    else:
        c = [pow(zeta, m * m % (2 * n), p) for m in range(n)]
        cb = [pow(zeta_inv, m * m % (2 * n), p) for m in range(n)]
    a = [0] * big_m  # @line L3
    for j in range(n):
        a[j] = x[j] * c[j] if p is None else x[j] * c[j] % p
    b = [0] * big_m  # @line L4
    for m in range(n):
        b[m] = cb[m]
        if m:
            b[big_m - m] = cb[m]
    _fft(a, root_m, p)  # @line L5
    _fft(b, root_m, p)
    for r in range(big_m):  # @line L6
        a[r] = a[r] * b[r] if p is None else a[r] * b[r] % p
    if p is None:  # @line L7
        _fft(a, 1, None)
        z = [v / big_m for v in a]
    else:
        _fft(a, pow(root_m, -1, p), p)
        inv_m = pow(big_m, -1, p)
        z = [v * inv_m % p for v in a]
    if p is None:  # @line L8
        return [c[k] * z[k] for k in range(n)]
    return [c[k] * z[k] % p for k in range(n)]  # @line L9


def _modular_roots(n: int, p: int, g: int) -> tuple[int, int, int]:
    """Return (zeta, zeta_inv, root_m) modulo the prime p from a primitive root g."""
    big_m = 1
    while big_m < 2 * n - 1:
        big_m *= 2
    if (p - 1) % (2 * n) or (p - 1) % big_m:
        raise ValueError("p - 1 must be divisible by 2n and by the convolution length")
    zeta = pow(g, (p - 1) // (2 * n), p)
    return zeta, pow(zeta, -1, p), pow(g, (p - 1) // big_m, p)


def bluestein(x: list, p: int | None = None, g: int | None = None) -> list:
    """Return the DFT X[k] = sum_j x[j] w^(jk) of x, for any length n >= 1.

    Over the complex numbers (p is None), w = exp(-2 pi i / n). Modulo a prime p
    with primitive root g, w = g^((p - 1) / n); then p - 1 must be divisible by 2n
    and by the power of two M >= 2n - 1 used for the convolution.
    Cost: three FFTs of length M plus 2n + 2M multiplications, Theta(n log n).
    """
    n = len(x)
    if n < 1:
        raise ValueError("the length must be positive")
    if p is None:
        return _chirp_dft(x, -1, None, None, None)
    zeta, zeta_inv, root_m = _modular_roots(n, p, g)
    return _chirp_dft([v % p for v in x], zeta, zeta_inv, root_m, p)


def inverse_bluestein(big_x: list, p: int | None = None, g: int | None = None) -> list:
    """Return the x with bluestein(x, p, g) == big_x, by the conjugate chirp and 1/n."""
    n = len(big_x)
    if n < 1:
        raise ValueError("the length must be positive")
    if p is None:
        y = _chirp_dft(big_x, 1, None, None, None)  # @line L10
        return [v / n for v in y]  # @line L11
    zeta, zeta_inv, root_m = _modular_roots(n, p, g)
    y = _chirp_dft([v % p for v in big_x], zeta_inv, zeta, root_m, p)
    inv_n = pow(n, -1, p)
    return [v * inv_n % p for v in y]
