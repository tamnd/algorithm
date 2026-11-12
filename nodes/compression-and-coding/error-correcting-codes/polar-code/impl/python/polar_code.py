# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polar-code/. The authors are listed in prov/HJNNKN.jsonl.
"""Polar codes of length N = 2^n over GF(2): construction, encoding and list decoding.

Conventions. Vectors are lists of bits. The transform is x = u F^(kron n) with the kernel
F = [[1, 0], [1, 1]] and no bit reversal (the order of 3GPP TS 38.212). Arikan's matrix
G_N = B_N F^(kron n) only permutes the code bits, see arikan_encode.

Decoders take channel LLRs lambda_j = ln P(y_j | x_j = 0) / P(y_j | x_j = 1). The list
decoder uses the path metric of Balatsoukas-Stimming, Bastani Parizi and Burg (2015).
"""

import math
from typing import List, Optional, Sequence, Tuple

# 3GPP TS 38.212 V16.9.0 (2022-03), Table 5.3.1.2-1, the first 80 entries of the polar
# sequence Q_0^(Nmax - 1), Nmax = 1024, in ascending order of reliability W(Q_i).
# Copied by hand from the table. Entries 0 to 79 only.
NR_SEQUENCE_PREFIX = [
    0, 1, 2, 4, 8, 16, 32, 3, 5, 64, 9, 6, 17, 10, 18, 128, 12, 33, 65, 20,
    256, 34, 24, 36, 7, 129, 66, 512, 11, 40, 68, 130, 19, 13, 48, 14, 72, 257, 21, 132,
    35, 258, 26, 513, 80, 37, 25, 22, 136, 260, 264, 38, 514, 96, 67, 41, 144, 28, 69, 42,
    516, 49, 74, 272, 160, 520, 288, 528, 192, 544, 70, 44, 131, 81, 50, 73, 15, 320, 133, 52,
]


def polar_transform(u: Sequence[int]) -> List[int]:
    """Return x = u F^(kron n) over GF(2). len(u) is a power of two. Cost: (N/2) log2 N XORs."""
    x = list(u)
    n = len(x)
    h = 1
    while h < n:
        for start in range(0, n, 2 * h):
            for j in range(start, start + h):
                x[j] ^= x[j + h]
        h *= 2
    return x


def bit_reverse(i: int, n: int) -> int:
    """Reverse the n low bits of i."""
    r = 0
    for _ in range(n):
        r = (r << 1) | (i & 1)
        i >>= 1
    return r


def arikan_encode(u: Sequence[int]) -> List[int]:
    """Return x = u B_N F^(kron n), Arikan's G_N with the bit-reversal permutation B_N."""
    n = len(u).bit_length() - 1
    v = [u[bit_reverse(i, n)] for i in range(len(u))]
    return polar_transform(v)


def bec_bhattacharyya(n: int, eps):
    """Z(W_N^(i)) for i = 0..N-1 on BEC(eps): z -> 2z - z^2 (bit 0) and z -> z^2 (bit 1).

    The bits of i are read from the most significant one. eps may be a Fraction.
    """
    z = [eps]
    for _ in range(n):
        nxt = []
        for v in z:
            nxt.append(2 * v - v * v)
            nxt.append(v * v)
        z = nxt
    return z


def info_set_bec(n: int, k: int, eps) -> List[int]:
    """The k indices with the smallest Bhattacharyya parameter on BEC(eps), sorted.

    Ties go to the larger index.
    """
    z = bec_bhattacharyya(n, eps)
    order = sorted(range(len(z)), key=lambda i: (z[i], -i))
    return sorted(order[:k])


def info_set_nr(n: int, k: int) -> List[int]:
    """The k most reliable indices of the 5G NR sequence restricted to N = 2^n (N <= 16 here)."""
    big = 1 << n
    seq = [q for q in NR_SEQUENCE_PREFIX if q < big]
    if len(seq) != big:
        raise ValueError("the copied prefix does not cover this length")
    return sorted(seq[big - k:])


def encode(msg: Sequence[int], info: Sequence[int], n: int) -> List[int]:
    """Put the message bits on the information set, zeros on the frozen set, and transform."""
    u = [0] * (1 << n)
    for i, b in zip(info, msg):
        u[i] = b
    return polar_transform(u)


def f_exact(a: float, b: float) -> float:
    """2 atanh(tanh(a/2) tanh(b/2)), in a form that does not overflow."""
    s = math.copysign(1.0, a) * math.copysign(1.0, b)
    return (s * min(abs(a), abs(b)) + math.log1p(math.exp(-abs(a + b)))
            - math.log1p(math.exp(-abs(a - b))))


def g(a: float, b: float, u: int) -> float:
    """b + (1 - 2u) a."""
    return b + a if u == 0 else b - a


def sc_decode(llr: Sequence[float], frozen: Sequence[bool]) -> List[int]:
    """Successive cancellation decoding. Returns u_hat. Cost O(N log N); depth log2 N."""
    u, _ = _sc(list(llr), list(frozen))
    return u


def _sc(lam: List[float], frozen: List[bool]) -> Tuple[List[int], List[int]]:
    n = len(lam)
    if n == 1:
        b = 0 if frozen[0] or lam[0] >= 0 else 1
        return [b], [b]
    h = n // 2
    ua, xa = _sc([f_exact(lam[j], lam[j + h]) for j in range(h)], frozen[:h])
    ub, xb = _sc([g(lam[j], lam[j + h], xa[j]) for j in range(h)], frozen[h:])
    return ua + ub, [p ^ q for p, q in zip(xa, xb)] + xb


def _penalty(lam: float, b: int) -> float:
    """ln(1 + exp(-(1 - 2b) lam)): the path metric increase for decision b."""
    t = lam if b == 0 else -lam
    return math.log1p(math.exp(-abs(t))) + (0.0 if t >= 0 else -t)


Path = Tuple[int, List[int], List[int], float]


def _scl(lams: List[List[float]], frozen: List[bool], metrics: List[float], size: int) -> List[Path]:
    """List decoding of a subtree for all paths at once.

    Returns (parent path, u bits, x bits, metric) for at most size surviving paths.
    """
    n = len(lams[0])
    if n == 1:
        out: List[Path] = []
        for p, (lam, m) in enumerate(zip(lams, metrics)):
            for b in ((0,) if frozen[0] else (0, 1)):
                out.append((p, [b], [b], m + _penalty(lam[0], b)))
        out.sort(key=lambda t: t[3])
        return out[:size]
    h = n // 2
    left = [[f_exact(lam[j], lam[j + h]) for j in range(h)] for lam in lams]
    res1 = _scl(left, frozen[:h], metrics, size)
    right = [[g(lams[p][j], lams[p][j + h], xa[j]) for j in range(h)] for p, _, xa, _ in res1]
    res2 = _scl(right, frozen[h:], [t[3] for t in res1], size)
    out = []
    for q, ub, xb, m in res2:
        p, ua, xa, _ = res1[q]
        out.append((p, ua + ub, [s ^ t for s, t in zip(xa, xb)] + xb, m))
    return out


def scl_decode(llr: Sequence[float], frozen: Sequence[bool], size: int,
               check=None) -> Optional[List[int]]:
    """Successive cancellation list decoding with list size `size` (Tal and Vardy).

    Returns the u_hat of the path with the least metric, or, when `check` is given, of the
    best path for which check(u_hat) is true (None if no path passes). Cost O(size N log N).
    """
    paths = _scl([list(llr)], list(frozen), [0.0], size)
    paths.sort(key=lambda t: t[3])
    for _, u, _, _ in paths:
        if check is None or check(u):
            return u
    return None


def crc_remainder(bits: Sequence[int], poly: int, r: int) -> List[int]:
    """The r CRC bits of `bits` (first bit = highest power) for the generator poly of degree r."""
    reg = 0
    for b in list(bits) + [0] * r:
        reg = (reg << 1) | b
        if reg >> r & 1:
            reg ^= poly
    return [(reg >> (r - 1 - i)) & 1 for i in range(r)]
