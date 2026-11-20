# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mmse-mimo-detector/. The authors are listed in prov/ZA2PHJ.jsonl.

"""The linear MMSE MIMO detector.

The model is y = H x + w, with H an m by n complex matrix, x a vector of n
points of a constellation with average energy Es and w ~ CN(0, N0 I).
With a = N0 / Es and P = (H^H H + a I)^(-1), the linear filter that
minimizes E||W y - x||^2 is W = P H^H. Its error covariance is N0 P.
The output W y is biased: E[(W y)_k | x_k] = beta_k x_k with
beta_k = (W H)_kk = 1 - a P_kk. The detector divides by beta_k before it
slices, which matters for constellations with more than one amplitude.
Stream k then has the SINR 1 / (a P_kk) - 1.
"""

import cbb


def nearest(z: complex, points: list[complex]) -> int:
    """The index of the point nearest to z (the lowest index on a tie)."""
    best, arg = float("inf"), -1
    for i, p in enumerate(points):
        d = abs(z - p) ** 2
        if d < best:
            best, arg = d, i
    return arg


def mmse_parts(h: list[list[complex]], n0: float, es: float = 1.0) -> tuple[list[list[complex]], list[list[complex]]]:
    """(P, W) with P = (H^H H + (N0/Es) I)^(-1) and W = P H^H."""
    if n0 < 0 or es <= 0:
        raise ValueError("need N0 >= 0 and Es > 0")
    n = len(h[0])
    a = n0 / es
    hh = cbb.herm(h)
    g = cbb.matmul(hh, h)
    for k in range(n):
        g[k][k] += a
    try:
        p = cbb.inv(g)  # @line L1
    except ValueError:
        raise ValueError("H^H H + (N0/Es) I is singular: N0 = 0 and H has dependent columns") from None
    w = cbb.matmul(p, hh)  # @line L2
    return p, w


def mmse_matrix(h: list[list[complex]], n0: float, es: float = 1.0) -> list[list[complex]]:
    """The n by m MMSE filter W = (H^H H + (N0/Es) I)^(-1) H^H."""
    return mmse_parts(h, n0, es)[1]


def bias(h: list[list[complex]], n0: float, es: float = 1.0) -> list[float]:
    """beta_k = (W H)_kk = 1 - (N0/Es) P_kk, the gain of stream k in the output W y."""
    p, _ = mmse_parts(h, n0, es)
    return [1.0 - (n0 / es) * p[k][k].real for k in range(len(p))]


def mmse_outputs(y: list[complex], h: list[list[complex]], n0: float, es: float = 1.0, unbiased: bool = True) -> list[complex]:
    """The filter outputs W y, divided by beta_k if unbiased is true."""
    p, w = mmse_parts(h, n0, es)
    z = cbb.matvec(w, y)
    if not unbiased:
        return z
    return [z[k] / (1.0 - (n0 / es) * p[k][k].real) for k in range(len(z))]


def mmse_detect(y: list[complex], h: list[list[complex]], points: list[complex], n0: float, es: float = 1.0, unbiased: bool = True) -> list[int]:
    """The MMSE decisions: the nearest point to each output, after the bias correction if unbiased is true."""
    p, w = mmse_parts(h, n0, es)
    a = n0 / es
    z = cbb.matvec(w, y)  # @line L3
    out = []
    for k in range(len(z)):  # @line L4
        beta = 1.0 - a * p[k][k].real if unbiased else 1.0  # @line L5
        out.append(nearest(z[k] / beta, points))  # @line L6
    return out  # @line L7


def error_covariance(h: list[list[complex]], n0: float, es: float = 1.0) -> list[list[complex]]:
    """E[(W y - x)(W y - x)^H] = N0 (H^H H + (N0/Es) I)^(-1), for x with covariance Es I."""
    p, _ = mmse_parts(h, n0, es)
    return cbb.scale(n0, p)


def sinr(h: list[list[complex]], n0: float, es: float = 1.0) -> list[float]:
    """The SINR of each stream at the unbiased MMSE output: 1 / ((N0/Es) P_kk) - 1."""
    if n0 <= 0:
        raise ValueError("the SINR is infinite or undefined for N0 = 0")
    p, _ = mmse_parts(h, n0, es)
    return [1.0 / ((n0 / es) * p[k][k].real) - 1.0 for k in range(len(p))]
