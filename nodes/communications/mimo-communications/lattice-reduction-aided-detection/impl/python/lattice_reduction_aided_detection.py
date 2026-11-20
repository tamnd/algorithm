# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lattice-reduction-aided-detection/. The authors are listed in prov/YKT7T0.jsonl.

"""Lattice reduction aided MIMO detection with LLL, in the real-valued model.

The model is y = H x + w with H an m by n complex matrix and x a vector of
points of square M-QAM (constel.qam) or M-PAM (constel.pam). The real-valued
model has the real channel Hr and the real symbol vector xr. Each real
symbol takes q equally spaced values (2 z - (q - 1)) / s with z in
{0, ..., q - 1}, so the shifted and scaled vector y' = (s yr + (q - 1) Hr 1) / 2
satisfies y' = Hr z + w' with an integer vector z. The detector reduces the
basis Hr to B = Hr T with LLL (T unimodular), estimates the integer vector
u = T^-1 z by rounding (ZF) or by Babai nearest plane (SIC) in the basis B,
maps back with z = T u, clips each entry of z to {0, ..., q - 1}, and returns
constellation indices.
"""

import math

import cbb
import constel


def _round(v: float) -> int:
    return math.floor(v + 0.5)


def _grid(points: list[complex]) -> tuple[str, int, float]:
    """(kind, q, s) for constel.qam(M) or constel.pam(M)."""
    m = len(points)
    if all(abs(p.imag) < 1e-12 for p in points):
        ref, kind, q, s = constel.pam(m), "pam", m, math.sqrt((m * m - 1) / 3.0)
    else:
        q = math.isqrt(m)
        if q * q != m:
            raise ValueError("points must be square QAM or PAM from constel")
        ref, kind, s = constel.qam(m), "qam", math.sqrt(2.0 * (m - 1) / 3.0)
    if any(abs(a - b) > 1e-9 for a, b in zip(points, ref)):
        raise ValueError("points must be square QAM or PAM from constel")
    return kind, q, s


def real_model(y: list[complex], h: list[list[complex]], kind: str) -> tuple[list[float], list[list[float]]]:
    """(yr, Hr): yr = (Re y, Im y); Hr = [[Re H, -Im H], [Im H, Re H]] for QAM, [[Re H], [Im H]] for PAM."""
    yr = [complex(v).real for v in y] + [complex(v).imag for v in y]
    if kind == "qam":
        top = [[complex(a).real for a in row] + [-complex(a).imag for a in row] for row in h]
        bot = [[complex(a).imag for a in row] + [complex(a).real for a in row] for row in h]
    else:
        top = [[complex(a).real for a in row] for row in h]
        bot = [[complex(a).imag for a in row] for row in h]
    return yr, top + bot


def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def gram_schmidt(b: list[list[float]]) -> tuple[list[list[float]], list[list[float]], list[float]]:
    """(bstar, mu, norms) of the basis vectors b[0], ..., b[n-1] (no normalization)."""
    n = len(b)
    bstar: list[list[float]] = []
    mu = [[0.0] * n for _ in range(n)]
    norms = [0.0] * n
    for i in range(n):
        v = list(b[i])
        for j in range(i):
            mu[i][j] = _dot(b[i], bstar[j]) / norms[j]
            v = [a - mu[i][j] * c for a, c in zip(v, bstar[j])]
        mu[i][i] = 1.0
        bstar.append(v)
        norms[i] = _dot(v, v)
        if norms[i] <= 1e-24 * max(1.0, _dot(b[i], b[i])):
            raise ValueError("the basis vectors are linearly dependent")
    return bstar, mu, norms


def lll(cols: list[list[float]], delta: float = 0.75) -> tuple[list[list[float]], list[list[int]], int]:
    """LLL reduction of the basis vectors cols[0], ..., cols[n-1].

    Returns (b, t, swaps): the reduced vectors, the integer matrix t with
    b[k] = sum_j t[k][j] cols[j] (so the matrix T with columns t[k] is
    unimodular and B = Hr T), and the number of swaps.
    """
    if not 0.25 < delta < 1.0:
        raise ValueError("delta must be in (1/4, 1)")
    n = len(cols)
    b = [list(c) for c in cols]
    t = [[1 if i == k else 0 for i in range(n)] for k in range(n)]
    _, mu, norms = gram_schmidt(b)
    swaps = 0
    k = 1
    while k < n:
        for j in range(k - 1, -1, -1):  # size reduction
            qq = _round(mu[k][j])
            if qq:
                b[k] = [a - qq * c for a, c in zip(b[k], b[j])]
                t[k] = [a - qq * c for a, c in zip(t[k], t[j])]
                for l in range(j + 1):
                    mu[k][l] -= qq * mu[j][l]
        if norms[k] >= (delta - mu[k][k - 1] ** 2) * norms[k - 1]:  # Lovasz condition
            k += 1
        else:
            b[k], b[k - 1] = b[k - 1], b[k]  # swap
            t[k], t[k - 1] = t[k - 1], t[k]
            swaps += 1
            _, mu, norms = gram_schmidt(b)
            k = max(k - 1, 1)
    return b, t, swaps


def lr_detect(
    y: list[complex],
    h: list[list[complex]],
    points: list[complex],
    method: str = "sic",
    n0: float = 0.0,
    reduce: bool = True,
    delta: float = 0.75,
    stats: dict | None = None,
) -> list[int]:
    """Constellation indices from LR-aided ZF (method="zf") or SIC (method="sic").

    n0 > 0 uses the MMSE form: the extended channel [Hr; sigma I] and
    y' extended by sigma times the mean of z, with sigma^2 the ratio of the
    noise variance to the symbol variance per real dimension.
    reduce=False skips LLL (T = I), which gives plain ZF or SIC in a fixed order.
    """
    if method not in ("zf", "sic"):
        raise ValueError("method must be zf or sic")
    kind, q, s = _grid(points)
    yr, hr = real_model(y, h, kind)  # @line L1
    nr = len(hr[0])
    yp = [(s * v + (q - 1) * sum(row)) / 2.0 for v, row in zip(yr, hr)]  # @line L2
    hp = [list(row) for row in hr]
    if n0 > 0:  # MMSE extension
        sig = math.sqrt(3.0 * s * s * n0 / (2.0 * (q * q - 1)))
        hp += [[sig if i == k else 0.0 for k in range(nr)] for i in range(nr)]
        yp += [sig * (q - 1) / 2.0] * nr
    cols = [[row[k] for row in hp] for k in range(nr)]
    if reduce:
        b, t, swaps = lll(cols, delta)  # @line L3
    else:
        b, t, swaps = cols, [[1 if i == k else 0 for i in range(nr)] for k in range(nr)], 0
    if stats is not None:
        stats["swaps"] = swaps
    if method == "zf":  # @line L4
        g = [[_dot(bi, bk) for bk in b] for bi in b]
        rhs = [_dot(bi, yp) for bi in b]
        u = [_round(v.real) for v in cbb.solve(g, rhs)]
    else:  # Babai nearest plane: SIC in the reduced basis
        bstar, _, norms = gram_schmidt(b)
        r = list(yp)
        u = [0] * nr
        for i in range(nr - 1, -1, -1):  # @line L5
            u[i] = _round(_dot(r, bstar[i]) / norms[i])
            r = [a - u[i] * c for a, c in zip(r, b[i])]
    z = [sum(t[k][i] * u[k] for k in range(nr)) for i in range(nr)]  # z = T u  # @line L6
    z = [min(max(v, 0), q - 1) for v in z]  # @line L7
    xr = [(2 * v - (q - 1)) / s for v in z]
    n = len(h[0])
    x = [complex(xr[k], xr[n + k]) for k in range(n)] if kind == "qam" else [complex(v) for v in xr]
    return [constel.ml_detect(v, points) for v in x]  # @line L8
