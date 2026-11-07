# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/convolution-via-fft/. The authors are listed in prov/XX6TKR.jsonl.

import cmath
from typing import Callable, TypeVar

S = TypeVar("S", int, complex)


def _fft(x: list[S], w: S, red: Callable[[S], S]) -> None:
    """In-place iterative radix-2 FFT, X[k] = sum of x[j] * w**(j*k).

    len(x) must be a power of two and w**(len(x)/2) must be -1 (or len(x) = 1).
    Every ring result passes through red, the reduction of the ring.
    """
    n = len(x)
    t = n.bit_length() - 1
    table = [red(w**0)] * max(n // 2, 1)
    for k in range(1, n // 2):
        table[k] = red(table[k - 1] * w) if isinstance(w, int) else w**k
    rev = [0] * n
    for j in range(1, n):
        rev[j] = (rev[j >> 1] >> 1) | ((j & 1) << (t - 1))
    for j in range(n):
        if j < rev[j]:
            x[j], x[rev[j]] = x[rev[j]], x[j]
    h = 1
    while h < n:
        step = n // (2 * h)
        for s in range(0, n, 2 * h):
            for k in range(h):
                u = x[s + k]
                v = red(table[k * step] * x[s + k + h])
                x[s + k] = red(u + v)
                x[s + k + h] = red(u - v)
        h *= 2


def _sizes(m: int, l: int) -> tuple[int, int]:
    if m < 1 or l < 1:
        raise ValueError("both inputs must be non-empty")
    out = m + l - 1  # @line L1
    size = 1 << (out - 1).bit_length()  # @line L2
    return out, size


def convolve_mod(a: list[int], b: list[int], p: int, g: int) -> list[int]:
    """Return the linear convolution c[k] = sum of a[i] * b[k - i], modulo p.

    Precondition: p is a prime, g is a primitive root modulo p, and the
    power of two N >= len(a) + len(b) - 1 divides p - 1 (for p = 998244353
    and g = 3, N up to 2**23). Cost: three FFTs of length N and N products,
    (3/2) N lg N + 2N multiplications and 3 N lg N additions modulo p.
    """
    out, size = _sizes(len(a), len(b))
    if (p - 1) % size:
        raise ValueError("the transform length must divide p - 1")
    w = pow(g, (p - 1) // size, p)  # @line L3
    red: Callable[[int], int] = lambda v: v % p
    fa = [v % p for v in a] + [0] * (size - len(a))  # @line L4
    fb = [v % p for v in b] + [0] * (size - len(b))  # @line L5
    _fft(fa, w, red)  # @line L6
    _fft(fb, w, red)
    fc = [x * y % p for x, y in zip(fa, fb)]  # @line L7
    _fft(fc, pow(w, -1, p), red)  # @line L8
    n_inv = pow(size, -1, p)
    return [v * n_inv % p for v in fc[:out]]  # @line L9


def convolve_complex(a: list[complex], b: list[complex]) -> list[complex]:
    """Return the linear convolution of a and b, computed in floating point.

    Precondition: a and b are non-empty. The result has a rounding error
    bounded as on the page; round it when the exact result is an integer
    vector and the bound is below 1/2. Cost: three complex FFTs of length
    N, the least power of two >= len(a) + len(b) - 1, and N products.
    """
    out, size = _sizes(len(a), len(b))
    w = cmath.exp(-2j * cmath.pi / size)  # @line L3
    red: Callable[[complex], complex] = lambda v: v
    fa = [complex(v) for v in a] + [0j] * (size - len(a))  # @line L4
    fb = [complex(v) for v in b] + [0j] * (size - len(b))  # @line L5
    _fft(fa, w, red)  # @line L6
    _fft(fb, w, red)
    fc = [x * y for x, y in zip(fa, fb)]  # @line L7
    _fft(fc, w.conjugate(), red)  # @line L8
    return [v / size for v in fc[:out]]  # @line L9
