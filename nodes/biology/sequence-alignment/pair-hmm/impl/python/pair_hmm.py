# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pair-hmm/. The authors are listed in prov/RM3ZE9.jsonl.
"""The pair HMM of Durbin et al. (1998), Chapter 4, with states M, X and Y.

M emits an aligned pair (a, b) with probability p[(a, b)], X emits a residue of x
alone and Y emits a residue of y alone, each with probability q[a]. The transitions are

    Begin, M -> M: 1 - 2 delta - tau,   -> X: delta,   -> Y: delta,   -> End: tau
    X -> X: eps,   X -> M: 1 - eps - tau,   X -> End: tau   (Y is the mirror of X)

There is no transition between X and Y. A state path is a string over "MXY".
All functions work with float or Fraction parameters; with Fractions the results are exact.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Optional, Tuple, Union

Num = Union[float, Fraction]
Table = List[List[Num]]


@dataclass(frozen=True)
class PairHMM:
    delta: Num
    eps: Num
    tau: Num
    p: Dict[Tuple[str, str], Num]
    q: Dict[str, Num]

    def a_mm(self) -> Num:
        """Probability of M -> M (also Begin -> M)."""
        return 1 - 2 * self.delta - self.tau

    def a_gm(self) -> Num:
        """Probability of X -> M and of Y -> M."""
        return 1 - self.eps - self.tau


def _zeros(n: int, m: int, zero: Num) -> Table:
    return [[zero] * (m + 1) for _ in range(n + 1)]


def joint(h: PairHMM, x: str, y: str, path: str) -> Num:
    """P(x, y, path) for a state path over "MXY". Cost O(len(path))."""
    prob: Num = h.tau * 0 + 1
    prev, i, j = "M", 0, 0  # Begin behaves like M
    for s in path:
        if s == "M":
            t = h.a_mm() if prev == "M" else h.a_gm()
            prob *= t * h.p[(x[i], y[j])]
            i, j = i + 1, j + 1
        elif s == "X":
            if prev == "Y":
                return prob * 0
            t = h.delta if prev == "M" else h.eps
            prob *= t * h.q[x[i]]
            i += 1
        else:
            if prev == "X":
                return prob * 0
            t = h.delta if prev == "M" else h.eps
            prob *= t * h.q[y[j]]
            j += 1
        prev = s
    if (i, j) != (len(x), len(y)):
        return prob * 0
    return prob * h.tau


def viterbi(h: PairHMM, x: str, y: str) -> Tuple[Num, str]:
    """Most probable state path and its probability P(x, y, path). Cost O(nm) time and space."""
    n, m = len(x), len(y)
    zero = h.tau * 0
    v = {s: _zeros(n, m, zero) for s in "MXY"}
    ptr: Dict[str, List[List[Optional[str]]]] = {s: [[None] * (m + 1) for _ in range(n + 1)] for s in "MXY"}
    v["M"][0][0] = zero + 1  # the Begin state
    amm, agm = h.a_mm(), h.a_gm()
    for i in range(n + 1):
        for j in range(m + 1):
            if i == 0 and j == 0:
                continue
            if i > 0 and j > 0:
                c = max([(amm * v["M"][i - 1][j - 1], "M"), (agm * v["X"][i - 1][j - 1], "X"), (agm * v["Y"][i - 1][j - 1], "Y")], key=lambda t: t[0])
                v["M"][i][j] = h.p[(x[i - 1], y[j - 1])] * c[0]
                ptr["M"][i][j] = c[1]
            if i > 0:
                c = max([(h.delta * v["M"][i - 1][j], "M"), (h.eps * v["X"][i - 1][j], "X")], key=lambda t: t[0])
                v["X"][i][j] = h.q[x[i - 1]] * c[0]
                ptr["X"][i][j] = c[1]
            if j > 0:
                c = max([(h.delta * v["M"][i][j - 1], "M"), (h.eps * v["Y"][i][j - 1], "Y")], key=lambda t: t[0])
                v["Y"][i][j] = h.q[y[j - 1]] * c[0]
                ptr["Y"][i][j] = c[1]
    best = max("MXY", key=lambda s: v[s][n][m])
    prob = h.tau * v[best][n][m]
    path: List[str] = []
    s, i, j = best, n, m
    while (i, j) != (0, 0):
        path.append(s)
        prev = ptr[s][i][j]
        if s == "M":
            i, j = i - 1, j - 1
        elif s == "X":
            i -= 1
        else:
            j -= 1
        s = prev if prev is not None else "M"
    return prob, "".join(reversed(path))


def forward(h: PairHMM, x: str, y: str) -> Tuple[Num, Dict[str, Table]]:
    """P(x, y), the sum over all state paths, and the forward tables. Cost O(nm)."""
    n, m = len(x), len(y)
    zero = h.tau * 0
    f = {s: _zeros(n, m, zero) for s in "MXY"}
    f["M"][0][0] = zero + 1
    amm, agm = h.a_mm(), h.a_gm()
    for i in range(n + 1):
        for j in range(m + 1):
            if i == 0 and j == 0:
                continue
            if i > 0 and j > 0:
                f["M"][i][j] = h.p[(x[i - 1], y[j - 1])] * (amm * f["M"][i - 1][j - 1] + agm * (f["X"][i - 1][j - 1] + f["Y"][i - 1][j - 1]))
            if i > 0:
                f["X"][i][j] = h.q[x[i - 1]] * (h.delta * f["M"][i - 1][j] + h.eps * f["X"][i - 1][j])
            if j > 0:
                f["Y"][i][j] = h.q[y[j - 1]] * (h.delta * f["M"][i][j - 1] + h.eps * f["Y"][i][j - 1])
    total = h.tau * (f["M"][n][m] + f["X"][n][m] + f["Y"][n][m])
    return total, f


def backward(h: PairHMM, x: str, y: str) -> Dict[str, Table]:
    """Backward tables: b[s][i][j] = P(x[i:], y[j:] | state s at (i, j)). Cost O(nm)."""
    n, m = len(x), len(y)
    zero = h.tau * 0
    b = {s: _zeros(n, m, zero) for s in "MXY"}
    amm, agm = h.a_mm(), h.a_gm()
    for i in range(n, -1, -1):
        for j in range(m, -1, -1):
            pm = h.p[(x[i], y[j])] * b["M"][i + 1][j + 1] if i < n and j < m else zero
            qx = h.q[x[i]] * b["X"][i + 1][j] if i < n else zero
            qy = h.q[y[j]] * b["Y"][i][j + 1] if j < m else zero
            end = h.tau if (i, j) == (n, m) else zero
            b["M"][i][j] = end + amm * pm + h.delta * (qx + qy)
            b["X"][i][j] = end + agm * pm + h.eps * qx
            b["Y"][i][j] = end + agm * pm + h.eps * qy
    return b


def posterior_match(h: PairHMM, x: str, y: str) -> Table:
    """post[i][j] = P(x_i is aligned to y_j | x, y) for 1 <= i <= n, 1 <= j <= m. Cost O(nm)."""
    total, f = forward(h, x, y)
    b = backward(h, x, y)
    n, m = len(x), len(y)
    post = _zeros(n, m, h.tau * 0)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            post[i][j] = f["M"][i][j] * b["M"][i][j] / total
    return post


def log_odds_parameters(h: PairHMM, eta: float) -> Tuple[Dict[Tuple[str, str], float], float, float, float, float]:
    """Durbin's mapping to an affine gap score, in bits, against the random model with end probability eta.

    Returns (s, d, e, c, const): substitution scores s(a, b), gap open d, gap extend e,
    the end correction c for an alignment that ends in a gap, and the constant log2(tau / eta^2).
    """
    amm, agm = float(h.a_mm()), float(h.a_gm())
    s = {ab: math.log2(float(pab) / (float(h.q[ab[0]]) * float(h.q[ab[1]]))) + math.log2(amm / (1 - eta) ** 2) for ab, pab in h.p.items()}
    d = -math.log2(float(h.delta) * agm / ((1 - eta) * amm))
    e = -math.log2(float(h.eps) / (1 - eta))
    c = math.log2(amm / agm)
    const = math.log2(float(h.tau) / eta ** 2)
    return s, d, e, c, const


def affine_score(h: PairHMM, eta: float, x: str, y: str) -> float:
    """Best affine-gap alignment score, in bits, with no X column next to a Y column.

    By Durbin's mapping this equals log2(Viterbi probability / P(x, y | random)). Cost O(nm).
    """
    s, d, e, c, const = log_odds_parameters(h, eta)
    n, m = len(x), len(y)
    ninf = -math.inf
    sm = [[ninf] * (m + 1) for _ in range(n + 1)]
    sx = [[ninf] * (m + 1) for _ in range(n + 1)]
    sy = [[ninf] * (m + 1) for _ in range(n + 1)]
    sm[0][0] = 0.0
    for i in range(n + 1):
        for j in range(m + 1):
            if i > 0 and j > 0:
                sm[i][j] = s[(x[i - 1], y[j - 1])] + max(sm[i - 1][j - 1], sx[i - 1][j - 1], sy[i - 1][j - 1])
            if i > 0:
                sx[i][j] = max(sm[i - 1][j] - d, sx[i - 1][j] - e)
            if j > 0:
                sy[i][j] = max(sm[i][j - 1] - d, sy[i][j - 1] - e)
    return max(sm[n][m], sx[n][m] + c, sy[n][m] + c) + const


def random_model_prob(h: PairHMM, eta: Num, x: str, y: str) -> Num:
    """P(x, y | R) for the random model that emits x and then y, each with end probability eta."""
    prob: Num = eta * eta * (1 - eta) ** (len(x) + len(y))
    for a in x + y:
        prob *= h.q[a]
    return prob
