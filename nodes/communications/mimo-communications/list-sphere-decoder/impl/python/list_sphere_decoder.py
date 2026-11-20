# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/list-sphere-decoder/. The authors are listed in prov/C5A1BF.jsonl.

"""The list sphere decoder and the bit LLRs computed from its list.

The model is y = H x + w with H an m by n complex matrix of full column rank
(m >= n), x a vector of n points of a constellation S of size M, and
w ~ CN(0, N0 I). After the triangular form ||y - H x||^2 = ||yb - R x||^2 + c,
a depth-first search visits the tree of partial vectors (x_i, ..., x_(n-1)),
level n - 1 first, children in order of their level term (the
Schnorr-Euchner order). It keeps the L best full vectors found so far and
prunes every node whose partial metric is not below the L-th best metric.
At the end the list holds L vectors with the smallest metrics of all M^n.

The bit LLRs use L(b) = ln P(b = 0 | y) / P(b = 1 | y) with equal priors.
The bits of stream k are constel.bits(index, log2 M), most significant first.
"""

import math

import cbb
import constel


def triangularize(y: list[complex], h: list[list[complex]]) -> tuple[list[list[complex]], list[complex], float]:
    """(R, yb, c) with R upper triangular, R^H R = H^H H, and ||y - H x||^2 = ||yb - R x||^2 + c."""
    if len(h) < len(h[0]):
        raise ValueError("the sphere decoder here needs m >= n")
    hh = cbb.herm(h)
    try:
        low = cbb.cholesky(cbb.matmul(hh, h))
    except ValueError:
        raise ValueError("H must have full column rank") from None
    b = cbb.matvec(hh, y)
    n = len(b)
    yb = [0j] * n
    for i in range(n):
        yb[i] = (b[i] - sum(low[i][c] * yb[c] for c in range(i))) / low[i][i]
    return cbb.herm(low), yb, cbb.norm2(y) - cbb.norm2(yb)


def list_sphere(
    y: list[complex], h: list[list[complex]], points: list[complex], size: int, stats: dict | None = None
) -> list[tuple[float, list[int]]]:
    """The size best vectors as (metric, indices), smallest metric first.

    The metric is the full ||y - H x||^2. If stats is a dict, stats["nodes"]
    receives the number of tree nodes whose partial metric was computed.
    """
    if size < 1:
        raise ValueError("the list size must be at least 1")
    r, yb, c = triangularize(y, h)  # @line L1
    n = len(yb)
    best: list[tuple[float, list[int]]] = []  # sorted list of at most size entries  # @line L2
    radius = [math.inf]
    nodes = [0]
    x = [0j] * n
    idx = [0] * n

    def search(i: int, d: float) -> None:
        u = yb[i] - sum(r[i][j] * x[j] for j in range(i + 1, n))  # @line L5
        terms = sorted((abs(u - r[i][i] * p) ** 2, j) for j, p in enumerate(points))  # @line L6
        for t, j in terms:
            nodes[0] += 1
            dd = d + t  # @line L7
            if dd >= radius[0]:  # @line L8
                break
            x[i], idx[i] = points[j], j
            if i == 0:  # @line L9
                best.append((dd, list(idx)))
                best.sort(key=lambda e: e[0])
                if len(best) > size:
                    best.pop()
                if len(best) == size:
                    radius[0] = best[-1][0]
            else:
                search(i - 1, dd)  # @line L10

    search(n - 1, 0.0)  # @line L3
    if stats is not None:
        stats["nodes"] = nodes[0]
    return [(d + c, v) for d, v in best]  # @line L4


def _logsumexp(vals: list[float]) -> float:
    top = max(vals)
    return top + math.log(sum(math.exp(v - top) for v in vals))


def list_llrs(
    cands: list[tuple[float, list[int]]], m_bits: int, n0: float, maxlog: bool = True, clip: float = 20.0
) -> list[float]:
    """The bit LLRs from a candidate list, stream by stream, most significant bit first.

    maxlog=True gives (min metric with b = 1 - min metric with b = 0) / N0.
    maxlog=False gives the log-sum-exp form over the list. A bit value that no
    candidate has gives the LLR +clip (all candidates have 0) or -clip.
    """
    if n0 <= 0:
        raise ValueError("N0 must be positive")
    n = len(cands[0][1])
    labels = [[constel.bits(i, m_bits) for i in v] for _, v in cands]
    out = []
    for k in range(n):
        for b in range(m_bits):
            zero = [-d / n0 for (d, _), lab in zip(cands, labels) if lab[k][b] == 0]
            one = [-d / n0 for (d, _), lab in zip(cands, labels) if lab[k][b] == 1]
            if not one:
                out.append(clip)
            elif not zero:
                out.append(-clip)
            elif maxlog:
                out.append(max(zero) - max(one))
            else:
                out.append(_logsumexp(zero) - _logsumexp(one))
    return out
