# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/v-blast/. The authors are listed in prov/Z0RT80.jsonl.

"""The V-BLAST detector: ordered nulling and cancelling.

The model is y = H x + w with H an m by n complex matrix, x a vector of n
constellation points of energy Es and w ~ CN(0, N0 I). At each step the
detector looks at the streams not yet detected (the set K), computes
P = (H_K^H H_K + a I)^(-1), with a = 0 for ZF nulling and a = N0 / Es for
MMSE nulling, and picks the stream k in K with the smallest P_kk, which is
the stream with the largest post-detection SNR (ZF) or SINR (MMSE). It
nulls the other streams of K with row k of P H_K^H, slices the result,
subtracts h_k times the decision from the received vector and removes k
from K. With a = 0 this is the receiver of Wolniansky, Foschini, Golden and
Valenzuela (1998).
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


def _columns(h: list[list[complex]], cols: list[int]) -> list[list[complex]]:
    return [[row[c] for c in cols] for row in h]


def _nulling(h: list[list[complex]], cols: list[int], a: float) -> tuple[list[list[complex]], list[list[complex]]]:
    """(P, P H_K^H) for the columns cols of H, with P = (H_K^H H_K + a I)^(-1)."""
    hk = _columns(h, cols)
    hh = cbb.herm(hk)
    g = cbb.matmul(hh, hk)
    for i in range(len(cols)):
        g[i][i] += a
    try:
        p = cbb.inv(g)
    except ValueError:
        raise ValueError("the remaining columns of H are dependent; use MMSE nulling or fewer streams") from None
    return p, cbb.matmul(p, hh)


def vblast_detect(
    y: list[complex],
    h: list[list[complex]],
    points: list[complex],
    n0: float = 0.0,
    es: float = 1.0,
    mmse: bool = False,
) -> tuple[list[int], list[int]]:
    """The V-BLAST decisions and the detection order.

    Returns (indices, order): indices[k] is the point index decided for
    stream k, and order lists the streams in the order they were detected.
    mmse=False gives ZF nulling and needs m >= n; mmse=True needs N0 > 0.
    """
    n = len(h[0])
    if mmse and n0 <= 0:
        raise ValueError("MMSE nulling needs N0 > 0")
    if not mmse and len(h) < n:
        raise ValueError("ZF nulling needs at least as many receive antennas as streams")
    a = n0 / es if mmse else 0.0
    r = [complex(v) for v in y]
    remaining = list(range(n))  # @line L1
    out = [-1] * n
    order = []
    while remaining:  # @line L2
        p, w = _nulling(h, remaining, a)  # @line L3
        i = min(range(len(remaining)), key=lambda t: p[t][t].real)  # @line L4
        k = remaining[i]
        z = sum(c * v for c, v in zip(w[i], r))  # @line L5
        if mmse:
            z /= 1.0 - a * p[i][i].real  # remove the MMSE bias
        out[k] = nearest(z, points)  # @line L6
        s = points[out[k]]
        r = [rv - row[k] * s for rv, row in zip(r, h)]  # @line L7
        remaining.pop(i)  # @line L8
        order.append(k)
    return out, order  # @line L9


def post_detection_snr(h: list[list[complex]], order: list[int], es: float, n0: float, mmse: bool = False) -> list[float]:
    """The SNR (ZF) or unbiased SINR (MMSE) of each step, in detection order, assuming correct earlier decisions."""
    a = n0 / es
    remaining = list(range(len(h[0])))
    out = []
    for k in order:
        p, _ = _nulling(h, remaining, a if mmse else 0.0)
        i = remaining.index(k)
        out.append(1.0 / (a * p[i][i].real) - 1.0 if mmse else (es / n0) / p[i][i].real)
        remaining.pop(i)
    return out
