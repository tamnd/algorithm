# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transform-coding/. The authors are listed in prov/H7K4T6.jsonl.

"""Transform coding of blocks: an orthogonal transform, scalar quantization and
the measures that predict its gain, in pure Python.

The entropy coder is left out: the rate is measured as the empirical entropy
of the quantization indices, which is what a good entropy coder reaches.
"""

import math
from collections import Counter
from typing import Hashable, List, Sequence, Tuple

Vector = List[float]
Matrix = List[List[float]]


def apply(t: Matrix, x: Sequence[float]) -> Vector:
    """y = T x."""
    return [sum(r[i] * x[i] for i in range(len(x))) for r in t]


def apply_transpose(t: Matrix, y: Sequence[float]) -> Vector:
    """x = T^T y."""
    n = len(t[0])
    return [sum(t[k][i] * y[k] for k in range(len(y))) for i in range(n)]


def encode_block(t: Matrix, steps: Sequence[float], x: Sequence[float]) -> List[int]:
    """Transform one block and quantize each coefficient with its own step.

    The entropy coder of the template (line L4) is not part of this function:
    it returns the integer indices that the coder would compress.
    """
    y = apply(t, x)  # @line L1
    q = []
    for k in range(len(y)):  # @line L2
        q.append(int(math.floor(y[k] / steps[k] + 0.5)))  # @line L3
    return q  # @line L4


def decode_block(t: Matrix, steps: Sequence[float], q: Sequence[int]) -> Vector:
    """Dequantize the indices and apply the inverse (transposed) transform."""
    q = list(q)  # @line L5
    y_hat = [q[k] * steps[k] for k in range(len(q))]  # @line L6
    return apply_transpose(t, y_hat)  # @line L7


def coefficient_variances(t: Matrix, r: Matrix) -> Vector:
    """Diagonal of T R T^T: the variances of the coefficients of a zero-mean source with covariance R."""
    n = len(r)
    out = []
    for row in t:
        rv = [sum(r[i][j] * row[j] for j in range(n)) for i in range(n)]
        out.append(sum(row[i] * rv[i] for i in range(n)))
    return out


def coding_gain(variances: Sequence[float]) -> float:
    """High-rate gain of transform coding over PCM: arithmetic over geometric mean of the variances."""
    n = len(variances)
    am = sum(variances) / n
    gm = math.exp(sum(math.log(v) for v in variances) / n)
    return am / gm


def high_rate_allocation(variances: Sequence[float], b: float) -> Vector:
    """b_k = b + (1/2) log2(var_k / GM). The mean of b_k is b. Some b_k can be negative."""
    n = len(variances)
    log_gm = sum(math.log2(v) for v in variances) / n
    return [b + 0.5 * (math.log2(v) - log_gm) for v in variances]


def reverse_water_filling(variances: Sequence[float], b: float) -> Tuple[float, Vector, Vector]:
    """Rate-distortion allocation for independent Gaussian components at mean rate b > 0.

    Finds the water level theta with sum_k max(0, (1/2) log2(var_k / theta)) = N b.
    Returns (theta, rates, distortions) with D_k = min(theta, var_k).
    The level is found by bisection on log2(theta), 200 steps.
    """
    n = len(variances)

    def total_rate(log_theta: float) -> float:
        return sum(max(0.0, 0.5 * (math.log2(v) - log_theta)) for v in variances)

    lo = min(math.log2(v) for v in variances) - 2.0 * b - 1.0
    hi = max(math.log2(v) for v in variances)
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if total_rate(mid) > n * b:
            lo = mid
        else:
            hi = mid
    log_theta = (lo + hi) / 2.0
    theta = 2.0 ** log_theta
    rates = [max(0.0, 0.5 * (math.log2(v) - log_theta)) for v in variances]
    dist = [min(theta, v) for v in variances]
    return theta, rates, dist


def empirical_entropy(symbols: Sequence[Hashable]) -> float:
    """Empirical entropy in bits per symbol of a list of symbols."""
    m = len(symbols)
    return -sum(c / m * math.log2(c / m) for c in Counter(symbols).values())
