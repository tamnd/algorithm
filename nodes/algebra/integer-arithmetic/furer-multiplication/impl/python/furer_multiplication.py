# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/furer-multiplication/. The authors are listed in prov/V5N955.jsonl.

"""A toy structural model of Fürer's multiplication, in exact arithmetic.

The ring is R = Z_q[x]/(x^m + 1) with the prime q = 998244353 = 119 * 2^23 + 1,
in the spirit of the modular variant of De, Kurur, Saha and Saptharishi. In R
the element x is a principal 2m-th root of unity, and multiplying by a power of
x is a negacyclic rotation of the coefficients: a cheap shift. The FFT of length
N = K^L, K = 2m, uses a principal N-th root rho with rho^(N/K) = x, so that all
its inner DFTs of length K need shifts only. General products in R, the
expensive operations, are needed only for the twiddle factors between levels
and for the pointwise products. In Fürer's algorithm those products are
recursive calls; here they are done by schoolbook negacyclic convolution.
"""

from dataclasses import dataclass

Q = 998244353
GENERATOR = 3  # a primitive root modulo Q
TWO_ADICITY = 23

Elem = list[int]  # m coefficients modulo Q, lowest degree first


@dataclass
class Counts:
    """Operations in R: cheap shifts and expensive general products."""

    shifts: int = 0
    twiddle_products: int = 0
    pointwise_products: int = 0


def shift(a: Elem, e: int) -> Elem:
    """a * x^e in Z_q[x]/(x^m + 1): a negacyclic rotation."""
    m = len(a)
    e %= 2 * m
    sign = 1
    if e >= m:
        e -= m
        sign = -1
    out = [0] * m
    for i, c in enumerate(a):
        j = i + e
        if j < m:
            out[j] = (sign * c) % Q
        else:
            out[j - m] = (-sign * c) % Q
    return out


def ring_mul(a: Elem, b: Elem) -> Elem:
    """A general product in R, by schoolbook negacyclic convolution."""
    m = len(a)
    out = [0] * m
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                k = i + j
                if k < m:
                    out[k] = (out[k] + x * y) % Q
                else:
                    out[k - m] = (out[k - m] - x * y) % Q
    return out


def _add(a: Elem, b: Elem) -> Elem:
    return [(x + y) % Q for x, y in zip(a, b)]


def _sub(a: Elem, b: Elem) -> Elem:
    return [(x - y) % Q for x, y in zip(a, b)]


def _interpolate(xs: list[int], ys: list[int]) -> Elem:
    """The polynomial of degree < len(xs) with the values ys at the points xs, mod Q."""
    n = len(xs)
    coeffs = [0] * n
    for i in range(n):
        basis = [1]
        denom = 1
        for j in range(n):
            if j != i:
                basis = [(c1 - xs[j] * c0) % Q for c0, c1 in zip(basis + [0], [0] + basis)]
                denom = denom * (xs[i] - xs[j]) % Q
        scale = ys[i] * pow(denom, Q - 2, Q) % Q
        for k in range(n):
            coeffs[k] = (coeffs[k] + scale * basis[k]) % Q
    return coeffs


def shift_dft(vec: list[Elem], e: int, sign: int, counts: Counts) -> list[Elem]:
    """Radix-2 DFT with the root x^(sign * e), len(vec) * e = 2m: shifts only."""
    size = len(vec)
    if size == 1:
        return [vec[0]]
    even = shift_dft(vec[0::2], 2 * e, sign, counts)
    odd = shift_dft(vec[1::2], 2 * e, sign, counts)
    half = size // 2
    out: list[Elem] = [[]] * size
    for k in range(half):
        t = shift(odd[k], sign * e * k)
        counts.shifts += 1
        out[k] = _add(even[k], t)
        out[k + half] = _sub(even[k], t)
    return out


class FurerRing:
    """Precomputed data for FFTs of length N = (2m)^L over R = Z_q[x]/(x^m + 1)."""

    def __init__(self, m: int, levels: int):
        if m < 2 or m & (m - 1) or levels < 1:
            raise ValueError("m must be a power of two at least 2, and levels at least 1")
        self.m, self.K, self.L = m, 2 * m, levels
        self.N = self.K**levels
        if self.N.bit_length() - 1 > TWO_ADICITY:
            raise ValueError("N too large for this prime")
        omega = pow(GENERATOR, (Q - 1) // self.N, Q)  # a primitive N-th root in Z_q
        zeta = pow(omega, self.N // self.K, Q)  # a primitive 2m-th root in Z_q
        points = [pow(zeta, 2 * i + 1, Q) for i in range(m)]  # the roots of x^m + 1
        values = [pow(omega, 2 * i + 1, Q) for i in range(m)]
        self.rho = _interpolate(points, values)  # rho(zeta^(2i+1)) = omega^(2i+1)
        self.powers = [[1] + [0] * (m - 1)]
        for _ in range(1, self.N):
            self.powers.append(ring_mul(self.powers[-1], self.rho))

    def root_power(self, e: int) -> Elem:
        """rho^e for an integer e."""
        return self.powers[e % self.N]

    def fft(self, vec: list[Elem], stride: int, sign: int, counts: Counts) -> list[Elem]:
        """DFT of vec with the root rho^(sign * stride), where len(vec) * stride = N."""
        K, size = self.K, len(vec)
        if size == K:  # @line L6
            return shift_dft(vec, 1, sign, counts)
        J = size // K
        rows = []
        for n1 in range(J):  # @line L7
            inner = self.fft([vec[J * n2 + n1] for n2 in range(K)], self.N // K, sign, counts)
            for k1 in range(K):  # @line L8
                e = stride * n1 * k1
                if e % self.N:
                    inner[k1] = ring_mul(inner[k1], self.root_power(sign * e))
                    counts.twiddle_products += 1
            rows.append(inner)
        out: list[Elem] = [[]] * size
        for k1 in range(K):  # @line L9
            col = self.fft([rows[n1][k1] for n1 in range(J)], stride * K, sign, counts)
            for k2 in range(J):
                out[k1 + K * k2] = col[k2]
        return out  # @line L10


def expected_counts(K: int, L: int) -> tuple[int, int]:
    """(shifts, twiddle products) of one FFT of length N = K^L."""
    N = K**L
    shifts = (N // 2) * L * (K.bit_length() - 1)
    twiddles = (L - 1) * (K - 1) * (N // K) - N // K + 1
    return shifts, twiddles


def capacity(ring: FurerRing, b: int) -> int:
    """The largest operand length, in binary digits, that the ring can multiply."""
    return (ring.N // 2) * (ring.m // 2) * b


def choose_ring(length: int, m: int = 4, b: int = 8) -> FurerRing:
    """The smallest ring of the form (m, L) that holds operands of the given length."""
    levels = 1
    while ((2 * m) ** levels // 2) * (m // 2) * b < length:
        levels += 1
    return FurerRing(m, levels)


def furer_multiply(u: int, v: int, ring: FurerRing | None = None, b: int = 8, counts: Counts | None = None) -> int:
    """Return u * v for u, v >= 0 by the toy Fürer scheme with b-bit digits."""
    if u < 0 or v < 0:
        raise ValueError("operands must be nonnegative")
    counts = counts if counts is not None else Counts()
    length = max(u.bit_length(), v.bit_length(), 1)
    ring = ring or choose_ring(length, b=b)
    m, N, half = ring.m, ring.N, ring.m // 2
    if length > capacity(ring, b):
        raise ValueError("operands too long for this ring")
    if (N // 2) * half * ((1 << b) - 1) ** 2 >= Q:
        raise ValueError("product coefficients could wrap modulo Q")
    mask = (1 << b) - 1

    def pack(z: int) -> list[Elem]:  # @line L1
        out = []
        for _ in range(N):
            el = [0] * m
            for t in range(half):
                el[t] = z & mask
                z >>= b
            out.append(el)
        return out

    fa = ring.fft(pack(u), 1, 1, counts)  # @line L2
    fb = ring.fft(pack(v), 1, 1, counts)
    prod = []
    for x, y in zip(fa, fb):  # @line L3
        prod.append(ring_mul(x, y))
        counts.pointwise_products += 1
    back = ring.fft(prod, 1, -1, counts)  # @line L4
    inv_n = pow(N, Q - 2, Q)
    result = 0
    for j in range(N - 1, -1, -1):  # @line L5
        value = 0
        for t in range(m - 1, -1, -1):
            value = (value << b) + back[j][t] * inv_n % Q
        result = (result << (half * b)) + value
    return result
