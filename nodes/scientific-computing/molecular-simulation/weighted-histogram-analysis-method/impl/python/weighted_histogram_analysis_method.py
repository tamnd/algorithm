# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-histogram-analysis-method/. The authors are listed in prov/53HG7A.jsonl.
"""Weighted histogram analysis method (Kumar et al. 1992), one coordinate.

Window k has N_k samples, the histogram n_k(b) over bins b, and the bias
w_k(b) at the bin centres. WHAM finds the unbiased bin probabilities p(b) and
the window free energies f_k from the two coupled equations

    p(b) = sum_k n_k(b) / sum_k N_k exp(beta (f_k - w_k(b))),
    exp(-beta f_k) = sum_b p(b) exp(-beta w_k(b)).

The solution is the minimum of the convex function

    L(f) = sum_b n(b) ln sum_k N_k exp(beta (f_k - w_k(b))) - beta sum_k N_k f_k,

with n(b) = sum_k n_k(b). L does not change when every f_k moves by the same
constant, so p is normalised to sum 1 to fix that constant.

The plain fixed-point iteration below is the classic one. It can be slow when
windows overlap poorly; its speed here is a measurement, not a bound.
"""

import math
from typing import Callable, Sequence


def _logsumexp(xs: Sequence[float]) -> float:
    m = max(xs)
    if m == -math.inf:
        return m
    return m + math.log(sum(math.exp(x - m) for x in xs))


def wham(counts: Sequence[Sequence[float]], bias: Sequence[Sequence[float]], beta: float,
         tol: float = 1e-10, max_iter: int = 100000) -> tuple[list[float], list[float], int]:
    """Return (p, f, iterations). counts[k][b] = n_k(b), bias[k][b] = w_k(b)."""
    nwin, nbins = len(counts), len(counts[0])
    big_n = [sum(c) for c in counts]
    if min(big_n) <= 0:
        raise ValueError("every window needs samples")
    log_n = [math.log(x) for x in big_n]
    total = [sum(counts[k][b] for k in range(nwin)) for b in range(nbins)]
    f = [0.0] * nwin                                                    # @line L1
    for it in range(1, max_iter + 1):                                   # @line L2
        log_p = []
        for b in range(nbins):                                          # @line L3
            if total[b] == 0:
                log_p.append(-math.inf)
                continue
            den = _logsumexp([log_n[k] + beta * (f[k] - bias[k][b]) for k in range(nwin)])
            log_p.append(math.log(total[b]) - den)                      # @line L3
        z = _logsumexp(log_p)
        log_p = [x - z for x in log_p]                                  # @line L4
        new_f = [-_logsumexp([lp - beta * bias[k][b] for b, lp in enumerate(log_p)]) / beta
                 for k in range(nwin)]                                  # @line L5
        change = max(abs(a - c) for a, c in zip(new_f, f))
        f = new_f
        if change < tol:                                                # @line L6
            break
    p = [math.exp(x) for x in log_p]
    return p, f, it                                                     # @line L7


def objective(f: Sequence[float], counts: Sequence[Sequence[float]],
              bias: Sequence[Sequence[float]], beta: float) -> float:
    """The convex function L(f) whose minimum solves the WHAM equations."""
    nwin, nbins = len(counts), len(counts[0])
    big_n = [sum(c) for c in counts]
    val = -beta * sum(n * fk for n, fk in zip(big_n, f))
    for b in range(nbins):
        nb = sum(counts[k][b] for k in range(nwin))
        if nb:
            val += nb * _logsumexp([math.log(big_n[k]) + beta * (f[k] - bias[k][b])
                                    for k in range(nwin)])
    return val


def free_energy_profile(p: Sequence[float], beta: float) -> list:
    """F(b) = -kT ln p(b), shifted so that the minimum is 0; None for empty bins."""
    vals = [(-math.log(x) / beta) if x > 0 else None for x in p]
    m = min(v for v in vals if v is not None)
    return [v - m if v is not None else None for v in vals]


# Sampling helpers for the tests: biased Metropolis windows on s = x.

def double_well(height: float) -> Callable[[float], float]:
    return lambda x: height * (x * x - 1.0) ** 2


def metropolis(u: Callable[[float], float], beta: float, x0: float, step: float,
               n: int, rng, burn: int = 500) -> list[float]:
    x, ux = x0, u(x0)
    out = []
    for i in range(burn + n):
        y = x + step * (2.0 * rng.random() - 1.0)
        uy = u(y)
        if uy <= ux or rng.random() < math.exp(-beta * (uy - ux)):
            x, ux = y, uy
        if i >= burn:
            out.append(x)
    return out


def histogram(values: Sequence[float], lo: float, hi: float, nbins: int) -> list[int]:
    counts = [0] * nbins
    width = (hi - lo) / nbins
    for v in values:
        b = int((v - lo) // width)
        if 0 <= b < nbins:
            counts[b] += 1
    return counts
