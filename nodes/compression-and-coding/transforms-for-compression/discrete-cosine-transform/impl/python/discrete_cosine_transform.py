# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrete-cosine-transform/. The authors are listed in prov/C2X14P.jsonl.

"""The discrete cosine transform (DCT-II) and its inverse (DCT-III), in pure Python.

dct and idct follow the definition with the orthonormal scaling, in
Theta(N^2) operations. dct_2d and idct_2d are the separable 2D transforms of
an N x N block, as in JPEG for N = 8. fast_dct and fast_idct are the
recursive split of B. G. Lee (1984), in Theta(N log N) operations for N a
power of two. aan_dct8 is the 8-point scaled DCT of Arai, Agui and Nakajima
(1988), with 5 multiplications, in the form of the IJG libjpeg float code.
"""

import math
from typing import List, Sequence

Vector = List[float]
Matrix = List[List[float]]


def _alpha(k: int, n: int) -> float:
    return math.sqrt(1.0 / n) if k == 0 else math.sqrt(2.0 / n)


def dct(x: Sequence[float]) -> Vector:
    """Orthonormal DCT-II: X[k] = a_k sum_n x[n] cos(pi (2n + 1) k / (2N)).

    a_0 = sqrt(1/N) and a_k = sqrt(2/N) for k >= 1. Cost Theta(N^2).
    """
    n = len(x)
    out = []
    for k in range(n):  # @line L1
        a = _alpha(k, n)  # @line L2
        out.append(a * sum(x[i] * math.cos(math.pi * (2 * i + 1) * k / (2 * n)) for i in range(n)))  # @line L3
    return out  # @line L4


def idct(c: Sequence[float]) -> Vector:
    """Orthonormal DCT-III, the inverse of dct. Cost Theta(N^2)."""
    n = len(c)
    out = []
    for i in range(n):  # @line L5
        out.append(sum(_alpha(k, n) * c[k] * math.cos(math.pi * (2 * i + 1) * k / (2 * n)) for k in range(n)))  # @line L6
    return out  # @line L7


def _transpose(b: Sequence[Sequence[float]]) -> Matrix:
    return [list(col) for col in zip(*b)]


def dct_2d(b: Sequence[Sequence[float]]) -> Matrix:
    """Separable 2D orthonormal DCT-II of a square block: rows, then columns.

    For an 8 x 8 block this is the FDCT of ITU-T T.81, Annex A.3.3.
    Cost Theta(N^3) with the direct 1D transform.
    """
    rows = [dct(r) for r in b]  # @line L8
    cols = [dct(c) for c in _transpose(rows)]  # @line L9
    return _transpose(cols)  # @line L10


def idct_2d(c: Sequence[Sequence[float]]) -> Matrix:
    """Inverse of dct_2d (the IDCT of T.81 for N = 8)."""
    rows = [idct(r) for r in c]
    cols = [idct(col) for col in _transpose(rows)]
    return _transpose(cols)


def dct_matrix(n: int) -> Matrix:
    """The N x N orthonormal DCT-II matrix; row k is the k-th basis vector."""
    return [[_alpha(k, n) * math.cos(math.pi * (2 * i + 1) * k / (2 * n)) for i in range(n)] for k in range(n)]


def _lee(x: Sequence[float]) -> Vector:
    """Unnormalized DCT-II, X[k] = sum_n x[n] cos(pi (2n + 1) k / (2N)), by Lee's split.

    Precondition: len(x) is a power of two. Recursion depth log2 N.
    """
    n = len(x)
    if n == 1:  # @line F1
        return [float(x[0])]
    h = n // 2
    u = [0.0] * h
    v = [0.0] * h
    for i in range(h):  # @line F2
        u[i] = x[i] + x[n - 1 - i]  # @line F3
        v[i] = (x[i] - x[n - 1 - i]) / (2.0 * math.cos(math.pi * (2 * i + 1) / (2 * n)))  # @line F4
    big_u = _lee(u)  # @line F5
    big_v = _lee(v) + [0.0]
    out = [0.0] * n
    for m in range(h):  # @line F6
        out[2 * m] = big_u[m]  # @line F7
        out[2 * m + 1] = big_v[m] + big_v[m + 1]  # @line F8
    return out  # @line F9


def _lee_inverse(c: Sequence[float]) -> Vector:
    """Inverse of _lee: undo each step of the split in reverse order."""
    n = len(c)
    if n == 1:
        return [float(c[0])]
    h = n // 2
    big_u = [c[2 * m] for m in range(h)]
    big_v = [0.0] * (h + 1)
    for m in range(h - 1, -1, -1):
        big_v[m] = c[2 * m + 1] - big_v[m + 1]
    u = _lee_inverse(big_u)
    v = _lee_inverse(big_v[:h])
    out = [0.0] * n
    for i in range(h):
        d = v[i] * 2.0 * math.cos(math.pi * (2 * i + 1) / (2 * n))
        out[i] = (u[i] + d) / 2.0
        out[n - 1 - i] = (u[i] - d) / 2.0
    return out


def _is_power_of_two(n: int) -> bool:
    return n >= 1 and n & (n - 1) == 0


def fast_dct(x: Sequence[float]) -> Vector:
    """Orthonormal DCT-II by Lee's algorithm. Same output as dct.

    Precondition: len(x) is a power of two. Cost: (N/2) log2 N multiplications
    by constants in the split, plus N for the scaling, and Theta(N log N) additions.
    """
    n = len(x)
    if not _is_power_of_two(n):
        raise ValueError("fast_dct needs a length that is a power of two")
    raw = _lee(x)
    return [_alpha(k, n) * raw[k] for k in range(n)]


def fast_idct(c: Sequence[float]) -> Vector:
    """Orthonormal DCT-III (inverse DCT) by the inverse of Lee's split."""
    n = len(c)
    if not _is_power_of_two(n):
        raise ValueError("fast_idct needs a length that is a power of two")
    return _lee_inverse([c[k] / _alpha(k, n) for k in range(n)])


# Scale factors of the AAN output: y[0] = sum x, and y[k] = 2 cos(k pi / 16) times
# sum_n x[n] cos((2n + 1) k pi / 16) for k >= 1.
AAN_SCALE = [1.0] + [2.0 * math.cos(k * math.pi / 16.0) for k in range(1, 8)]


def aan_dct8(d: Sequence[float]) -> Vector:
    """Scaled 8-point DCT of Arai, Agui and Nakajima, with 5 multiplications.

    Returns y with y[k] = AAN_SCALE[k] * sum_n d[n] cos((2n + 1) k pi / 16).
    A JPEG coder folds the scale into the quantization table.
    """
    if len(d) != 8:
        raise ValueError("aan_dct8 needs 8 samples")
    tmp0, tmp7 = d[0] + d[7], d[0] - d[7]
    tmp1, tmp6 = d[1] + d[6], d[1] - d[6]
    tmp2, tmp5 = d[2] + d[5], d[2] - d[5]
    tmp3, tmp4 = d[3] + d[4], d[3] - d[4]
    # Even part.
    tmp10, tmp13 = tmp0 + tmp3, tmp0 - tmp3
    tmp11, tmp12 = tmp1 + tmp2, tmp1 - tmp2
    y = [0.0] * 8
    y[0], y[4] = tmp10 + tmp11, tmp10 - tmp11
    z1 = (tmp12 + tmp13) * 0.707106781186547524  # cos(pi/4)
    y[2], y[6] = tmp13 + z1, tmp13 - z1
    # Odd part.
    tmp10 = tmp4 + tmp5
    tmp11 = tmp5 + tmp6
    tmp12 = tmp6 + tmp7
    z5 = (tmp10 - tmp12) * 0.382683432365089772  # cos(3 pi/8)
    z2 = 0.541196100146196984 * tmp10 + z5  # cos(pi/8) - cos(3 pi/8)
    z4 = 1.306562964876376527 * tmp12 + z5  # cos(pi/8) + cos(3 pi/8)
    z3 = tmp11 * 0.707106781186547524
    z11, z13 = tmp7 + z3, tmp7 - z3
    y[5], y[3] = z13 + z2, z13 - z2
    y[1], y[7] = z11 + z4, z11 - z4
    return y
