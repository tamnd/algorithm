# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tensor-cores/. The authors are listed in prov/65S74S.jsonl.
"""Models of tensor core arithmetic and cost, with exact Fractions.

round_to rounds a rational number to a binary floating-point format with
round to nearest, ties to even.  mma computes D = A x B + C: the inputs are
rounded to the input format, each product is exact, and each addition is
rounded to the accumulator format in a fixed order.  This is a model of mixed
precision, not a bit-exact model of any GPU: real tensor cores may add several
products at once and may round in other ways.  No CUDA code is run.
"""
from fractions import Fraction as F

# (significand bits p including the hidden bit, smallest normal exponent, largest exponent)
FP16 = (11, -14, 15)
BF16 = (8, -126, 127)
TF32 = (11, -126, 127)
FP32 = (24, -126, 127)


def unit_roundoff(fmt):
    return F(1, 2 ** fmt[0])


def max_finite(fmt):
    p, _, emax = fmt
    return (2 - F(1, 2 ** (p - 1))) * F(2) ** emax


def round_to(x, fmt):
    """Round x to the nearest value of fmt (ties to even); overflow gives +-inf."""
    x = F(x)
    if x == 0:
        return F(0)
    p, emin, emax = fmt
    s, a = (1, x) if x > 0 else (-1, -x)
    e = a.numerator.bit_length() - a.denominator.bit_length()
    if F(2) ** e > a:
        e -= 1
    e = max(e, emin)                                   # subnormals share the quantum of emin
    q = F(2) ** (e - p + 1)
    m = a / q
    n = m.numerator // m.denominator
    r = m - n
    if r > F(1, 2) or (r == F(1, 2) and n % 2 == 1):
        n += 1
    v = n * q
    if v > max_finite(fmt):
        return s * float("inf")
    return s * v


def mma(A, B, C, in_fmt, acc_fmt):
    """D = A x B + C with inputs in in_fmt and a sequential accumulation in acc_fmt."""
    m, k, n = len(A), len(B), len(B[0])
    A = [[round_to(v, in_fmt) for v in row] for row in A]
    B = [[round_to(v, in_fmt) for v in row] for row in B]
    D = []
    for i in range(m):
        row = []
        for j in range(n):
            acc = round_to(C[i][j], acc_fmt)
            for t in range(k):
                acc = round_to(acc + A[i][t] * B[t][j], acc_fmt)   # exact product, one rounding
            row.append(acc)
        D.append(row)
    return D


def dot(x, y, in_fmt, acc_fmt):
    return mma([list(x)], [[v] for v in y], [[0]], in_fmt, acc_fmt)[0][0]


def mma_count(M, N, K, shape=(16, 16, 16)):
    """Number of warp-level mma_sync calls for an M x N x K product with one fragment shape."""
    m, n, k = shape
    return (-(-M // m)) * (-(-N // n)) * (-(-K // k))


def padding_efficiency(M, N, K, shape=(16, 16, 16)):
    """Useful multiply-adds over the multiply-adds done on padded tiles."""
    m, n, k = shape
    return F(M * N * K, mma_count(M, N, K, shape) * m * n * k)


def peak_flops(units, fma_per_clock, clock_hz):
    """Peak rate: each fused multiply-add counts as 2 floating-point operations."""
    return units * fma_per_clock * 2 * F(clock_hz)


def tile_intensity(b, in_bytes=2):
    """Flops per byte of a b x b output tile that reads its A and B panels once.

    Per step of depth kk: 2 b^2 kk flops and 2 b kk in_bytes bytes, so b / in_bytes.
    """
    return F(2 * b * b, 2 * b * in_bytes)


def ridge_point(peak, bandwidth):
    """The roofline ridge: the intensity needed to reach the peak rate."""
    return F(peak) / F(bandwidth)
