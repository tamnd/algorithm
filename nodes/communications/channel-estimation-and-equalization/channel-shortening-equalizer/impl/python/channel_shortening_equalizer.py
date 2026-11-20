# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/channel-shortening-equalizer/. The authors are listed in prov/B8R7HN.jsonl.

"""The maximum shortening SNR (MSSNR) channel shortening equalizer.

A multicarrier receiver needs the channel to fit in the cyclic prefix of nu
samples. A time-domain equalizer (TEQ) w of Lw taps makes the effective channel
c = h * w, of length L + Lw - 1. For a delay d, the window is the nu + 1 taps
c[d], ..., c[d + nu], and the wall is the rest. With the full convolution matrix
Hc (Hc[k][j] = h[k - j]), the window energy is w^T B w and the wall energy is
w^T A w, where B and A sum the outer products of the rows of Hc inside and
outside the window. MSSNR (Melsa, Younce and Rohrs) maximizes the shortening
SNR w^T B w / w^T A w, so w is the eigenvector of the pencil A w = mu B w with
the smallest mu. It is found here by inverse iteration, followed by a few
Rayleigh quotient steps. The channel and the filter are real, as in DMT.
"""

import math


def conv_matrix(h: list[float], lw: int) -> list[list[float]]:
    n = len(h) + lw - 1
    return [[h[k - j] if 0 <= k - j < len(h) else 0.0 for j in range(lw)] for k in range(n)]


def window_wall(h: list[float], lw: int, nu: int, d: int) -> tuple[list[list[float]], list[list[float]]]:
    """The matrices A (wall) and B (window) for the delay d."""
    hc = conv_matrix(h, lw)
    if not 0 <= d <= len(hc) - nu - 1:
        raise ValueError("the window must lie inside the effective channel")
    a = [[0.0] * lw for _ in range(lw)]
    b = [[0.0] * lw for _ in range(lw)]
    for k, row in enumerate(hc):
        m = b if d <= k <= d + nu else a
        for i in range(lw):
            for j in range(lw):
                m[i][j] += row[i] * row[j]
    return a, b


def _solve(m: list[list[float]], v: list[float]) -> list[float]:
    n = len(m)
    t = [row[:] + [v[i]] for i, row in enumerate(m)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(t[r][c]))
        if abs(t[p][c]) < 1e-300:
            raise ValueError("singular matrix")
        t[c], t[p] = t[p], t[c]
        for r in range(c + 1, n):
            f = t[r][c] / t[c][c]
            for k in range(c, n + 1):
                t[r][k] -= f * t[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (t[r][n] - sum(t[r][k] * x[k] for k in range(r + 1, n))) / t[r][r]
    return x


def _mv(m: list[list[float]], v: list[float]) -> list[float]:
    return [sum(a * b for a, b in zip(row, v)) for row in m]


def _dot(u: list[float], v: list[float]) -> float:
    return sum(a * b for a, b in zip(u, v))


def mssnr_teq(h: list[float], lw: int, nu: int, d: int, iters: int = 500, tol: float = 1e-15) -> tuple[list[float], float]:
    """The MSSNR filter w (scaled so that w^T B w = 1) and the shortening SNR 1/mu."""
    a, b = window_wall(h, lw, nu, d)  # @line L1
    w = [1.0] * lw  # @line L2
    mu = math.inf
    for _ in range(iters):  # @line L3
        v = _solve(a, _mv(b, w))  # @line L4
        nb = math.sqrt(_dot(v, _mv(b, v)))
        if nb == 0:
            raise ValueError("the window gets no energy")
        w = [x / nb for x in v]  # @line L5
        new = _dot(w, _mv(a, w))  # @line L6
        done = abs(new - mu) <= tol * max(1.0, abs(new))
        mu = new
        if done:
            break
    for _ in range(3):  # Rayleigh quotient steps polish the vector
        try:
            v = _solve([[a[i][j] - mu * b[i][j] for j in range(lw)] for i in range(lw)], _mv(b, w))
        except ValueError:
            break
        nb = math.sqrt(abs(_dot(v, _mv(b, v))))
        if nb == 0 or not math.isfinite(nb):
            break
        cand = [x / nb for x in v]
        new = _dot(cand, _mv(a, cand))
        if new > mu * (1 + 1e-9) + 1e-300:
            break  # never move away from the smallest eigenvalue
        w, mu = cand, new
    if w[max(range(lw), key=lambda i: abs(w[i]))] < 0:
        w = [-x for x in w]
    return w, 1.0 / mu  # @line L7


def shortening_snr(h: list[float], w: list[float], nu: int, d: int) -> float:
    """Window energy over wall energy of c = h * w."""
    c = [0.0] * (len(h) + len(w) - 1)
    for i, x in enumerate(h):
        for j, y in enumerate(w):
            c[i + j] += x * y
    win = sum(v * v for v in c[d:d + nu + 1])
    wall = sum(v * v for v in c) - win
    return win / wall


def best_delay(h: list[float], lw: int, nu: int) -> tuple[int, list[float], float]:
    """Try every delay and keep the one with the largest shortening SNR."""
    best = None
    for d in range(len(h) + lw - 1 - nu):
        try:
            w, s = mssnr_teq(h, lw, nu, d)
        except ValueError:
            continue
        if best is None or s > best[2]:
            best = (d, w, s)
    if best is None:
        raise ValueError("no delay works")
    return best
