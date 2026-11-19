# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-align/. The authors are listed in prov/NW40F8.jsonl.

"""Fast align: IBM Model 2 with a diagonal distortion (Dyer, Chahuneau and Smith 2013).

Notation of the page, not of the paper. A pair is (f, e) with the source
f = f_1 .. f_m and the target e = e_1 .. e_l, plus the null word e_0 = NULL.
The model generates f from e (the direction p(f | e)); each source position j
has one link a_j in {0, .., l}. The distortion is

    delta(0 | j, m, l) = p0,
    delta(i | j, m, l) = (1 - p0) exp(lam * h(i, j, m, l)) / Z(j, m, l, lam),  i >= 1,
    h(i, j, m, l) = -|i / l - j / m|.

Z is a sum of two geometric series, so it costs O(1) (lines L10 and L11).

Training is EM. The E step is exact. The M step for theta is a normalization.
The M step for lam maximizes the expected log likelihood, which is concave in
lam, by bisection on its derivative; the new lam is kept only if it does not
lower that objective, so the likelihood never decreases. The paper uses
variational Bayes for theta and gradient steps for lam; this file uses plain
EM, as the page says.
"""

import math
from collections import defaultdict
from typing import Dict, List, Sequence, Tuple

NULL = "<null>"
Pair = Tuple[Sequence[str], Sequence[str]]  # (f, e)


def h(i: int, j: int, m: int, l: int) -> float:
    """The feature -|i / l - j / m| of the link from source j to target i."""
    return -abs(i / l - j / m)


def geo(g: float, log_r: float, n: int) -> float:
    """g + g r + .. + g r^(n-1) with r = exp(log_r) <= 1.

    The form expm1(n log_r) / expm1(log_r) stays accurate when r is close to 1.
    """
    if n <= 0:
        return 0.0
    if log_r == 0.0:
        return g * n
    return g * math.expm1(n * log_r) / math.expm1(log_r)


def partition(j: int, m: int, l: int, lam: float) -> float:
    """Z(j, m, l, lam) = sum over i = 1 .. l of exp(lam h(i, j, m, l)), in O(1)."""
    i_up = (j * l) // m  # @line L10
    log_r = -lam / l
    lower = geo(math.exp(lam * h(i_up, j, m, l)), log_r, i_up) if i_up >= 1 else 0.0
    upper = geo(math.exp(lam * h(i_up + 1, j, m, l)), log_r, l - i_up) if i_up < l else 0.0
    return lower + upper  # @line L11


def partition_direct(j: int, m: int, l: int, lam: float) -> float:
    """The same sum, term by term, in O(l). For tests."""
    return sum(math.exp(lam * h(i, j, m, l)) for i in range(1, l + 1))


def _arith_geo(a: float, d: float, g: float, r: float, n: int) -> float:
    """sum over k = 0 .. n-1 of (a + k d) g r^k."""
    if n <= 0:
        return 0.0
    if 1.0 - r < 1e-4:
        # the closed form cancels badly near r = 1; n <= l, so add the terms
        return sum((a + k * d) * g * r**k for k in range(n))
    s0 = (1.0 - r**n) / (1.0 - r)
    s1 = r * (1.0 - n * r ** (n - 1) + (n - 1) * r**n) / (1.0 - r) ** 2
    return g * (a * s0 + d * s1)


def expected_h(j: int, m: int, l: int, lam: float) -> float:
    """E[h] under exp(lam h(i)) / Z over i = 1 .. l, in O(1). This is d ln Z / d lam."""
    i_up = (j * l) // m
    r = math.exp(-lam / l)
    num = 0.0
    if i_up >= 1:
        a = h(i_up, j, m, l)
        num += _arith_geo(a, -1.0 / l, math.exp(lam * a), r, i_up)
    if i_up < l:
        a = h(i_up + 1, j, m, l)
        num += _arith_geo(a, -1.0 / l, math.exp(lam * a), r, l - i_up)
    return num / partition(j, m, l, lam)


def distortion(i: int, j: int, m: int, l: int, lam: float, p0: float) -> float:
    """delta(i | j, m, l)."""
    if i == 0:
        return p0
    return (1.0 - p0) * math.exp(lam * h(i, j, m, l)) / partition(j, m, l, lam)


def _targets(e: Sequence[str]) -> List[str]:
    return [NULL] + list(e)


def log_likelihood(corpus: Sequence[Pair], theta: Dict[Tuple[str, str], float], lam: float, p0: float) -> float:
    """sum over pairs and j of ln sum over i = 0 .. l of delta(i | j, m, l) theta(f_j | e_i)."""
    total = 0.0
    for f, e in corpus:
        m, l, es = len(f), len(e), _targets(e)
        for j in range(1, m + 1):
            s = sum(distortion(i, j, m, l, lam, p0) * theta.get((f[j - 1], es[i]), 0.0) for i in range(l + 1))
            total += math.log(s)
    return total


def _lambda_objective(lam: float, s_h: float, mass: Dict[Tuple[int, int, int], float]) -> float:
    """The part of the expected log likelihood that depends on lam."""
    return lam * s_h - sum(n * math.log(partition(j, m, l, lam)) for (j, m, l), n in mass.items())


def _lambda_step(lam: float, s_h: float, mass: Dict[Tuple[int, int, int], float],
                 lam_max: float = 100.0, steps: int = 60) -> float:
    """Maximize lam * s_h - sum n ln Z over [0, lam_max] by bisection on the derivative."""

    def grad(x: float) -> float:
        return s_h - sum(n * expected_h(j, m, l, x) for (j, m, l), n in mass.items())

    if grad(0.0) <= 0.0:
        best = 0.0
    elif grad(lam_max) >= 0.0:
        best = lam_max
    else:
        lo, hi = 0.0, lam_max
        for _ in range(steps):
            mid = (lo + hi) / 2.0
            if grad(mid) > 0.0:
                lo = mid
            else:
                hi = mid
        best = (lo + hi) / 2.0
    # keep the old value unless the new one is at least as good (generalized EM)
    if _lambda_objective(best, s_h, mass) >= _lambda_objective(lam, s_h, mass):
        return best
    return lam


def em_step(corpus: Sequence[Pair], theta: Dict[Tuple[str, str], float], lam: float, p0: float,
            optimize_lambda: bool = True) -> Tuple[Dict[Tuple[str, str], float], float]:
    """One EM iteration. Returns the new (theta, lam)."""
    counts: Dict[Tuple[str, str], float] = defaultdict(float)
    totals: Dict[str, float] = defaultdict(float)
    s_h = 0.0
    mass: Dict[Tuple[int, int, int], float] = defaultdict(float)
    for f, e in corpus:  # @line L3
        m, l, es = len(f), len(e), _targets(e)
        for j in range(1, m + 1):
            z = partition(j, m, l, lam)  # @line L4
            w = [p0 * theta.get((f[j - 1], NULL), 0.0)]
            for i in range(1, l + 1):
                w.append((1.0 - p0) * math.exp(lam * h(i, j, m, l)) / z * theta.get((f[j - 1], es[i]), 0.0))  # @line L5
            total = sum(w)
            for i in range(l + 1):  # @line L6
                q = w[i] / total
                counts[(f[j - 1], es[i])] += q
                totals[es[i]] += q
                if i >= 1:
                    s_h += q * h(i, j, m, l)
                    mass[(j, m, l)] += q
    new_theta = {(x, y): c / totals[y] for (x, y), c in counts.items()}  # @line L7
    if optimize_lambda:
        lam = _lambda_step(lam, s_h, mass)  # @line L8
    return new_theta, lam


def train(corpus: Sequence[Pair], iterations: int = 5, lam: float = 4.0, p0: float = 0.08,
          optimize_lambda: bool = True) -> Tuple[Dict[Tuple[str, str], float], float, List[float]]:
    """Run EM. Returns theta, lam and the log likelihood before each iteration and at the end."""
    vf = sorted({x for f, _ in corpus for x in f})
    ve = sorted({y for _, e in corpus for y in e}) + [NULL]
    theta = {(x, y): 1.0 / len(vf) for x in vf for y in ve}  # @line L1
    history = [log_likelihood(corpus, theta, lam, p0)]
    for _ in range(iterations):  # @line L2
        theta, lam = em_step(corpus, theta, lam, p0, optimize_lambda)
        history.append(log_likelihood(corpus, theta, lam, p0))
    return theta, lam, history  # @line L9


def viterbi_alignment(f: Sequence[str], e: Sequence[str], theta: Dict[Tuple[str, str], float],
                      lam: float, p0: float = 0.08) -> List[int]:
    """The best a_j for each j, chosen independently; the smallest i wins a tie. 0 is NULL."""
    m, l, es = len(f), len(e), _targets(e)
    out = []
    for j in range(1, m + 1):
        scores = [distortion(i, j, m, l, lam, p0) * theta.get((f[j - 1], es[i]), 0.0) for i in range(l + 1)]
        out.append(max(range(l + 1), key=lambda i: (scores[i], -i)))
    return out
