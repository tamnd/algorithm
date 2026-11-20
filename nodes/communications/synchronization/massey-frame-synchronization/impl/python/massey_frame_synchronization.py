# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/massey-frame-synchronization/. The authors are listed in prov/JTBTTM.jsonl.

"""Massey's optimum frame synchronization rule (1972) for binary data on the AWGN channel.

Model: a window of N received real symbols y[0..N-1], read cyclically, holds one
sync word s[0..L-1] (entries +1 or -1) that starts at an unknown position mu.
The other N - L symbols are independent, equally likely data in {+1, -1}. The
channel is y[i] = sqrt(Es) d[i] + n[i] with n[i] ~ N(0, N0/2), the real AWGN
channel with SNR Es/N0 per symbol. With mu equally likely, the maximum
likelihood (and MAP) rule picks the mu that maximizes

    M(mu) = sum_{i<L} s[i] y[mu+i] - (N0 / (2 sqrt(Es))) sum_{i<L} ln cosh(2 sqrt(Es) y[mu+i] / N0).

The first sum is the plain correlation; the second is Massey's correction.
"""

import math
from typing import Sequence


def ln_cosh(x: float) -> float:
    """ln cosh x without overflow: |x| + ln(1 + e^(-2|x|)) - ln 2."""
    ax = abs(x)
    return ax + math.log1p(math.exp(-2.0 * ax)) - math.log(2.0)


def massey_metric(y: Sequence[float], s: Sequence[int], mu: int, es: float, n0: float) -> float:
    """M(mu): the correlation minus Massey's correction term, with cyclic indices."""
    n, a = len(y), math.sqrt(es)
    corr, corr_term = 0.0, 0.0
    for i, si in enumerate(s):  # @line L3
        v = y[(mu + i) % n]
        corr += si * v  # @line L4
        corr_term += ln_cosh(2.0 * a * v / n0)  # @line L5
    return corr - n0 / (2.0 * a) * corr_term  # @line L6


def massey_sync(y: Sequence[float], s: Sequence[int], es: float, n0: float) -> int:
    """The maximum likelihood start position of the sync word in the cyclic window y."""
    best, best_mu = -math.inf, 0  # @line L1
    for mu in range(len(y)):  # @line L2
        m = massey_metric(y, s, mu, es, n0)
        if m > best:  # @line L7
            best, best_mu = m, mu  # @line L8
    return best_mu  # @line L9


def correlation_sync(y: Sequence[float], s: Sequence[int]) -> int:
    """The plain correlation rule: argmax of sum s[i] y[mu + i]."""
    n = len(y)
    scores = [sum(si * y[(mu + i) % n] for i, si in enumerate(s)) for mu in range(n)]
    return max(range(n), key=lambda mu: scores[mu])


def high_snr_sync(y: Sequence[float], s: Sequence[int]) -> int:
    """The high-SNR form of Massey's rule: argmax of sum (s[i] y[mu + i] - |y[mu + i]|)."""
    n = len(y)
    scores = [sum(si * y[(mu + i) % n] - abs(y[(mu + i) % n]) for i, si in enumerate(s)) for mu in range(n)]
    return max(range(n), key=lambda mu: scores[mu])


def hard_sync(y: Sequence[float], s: Sequence[int]) -> int:
    """The rule for hard decisions: the fewest disagreements between sign(y) and s."""
    n = len(y)
    dist = [sum(1 for i, si in enumerate(s) if (1 if y[(mu + i) % n] >= 0 else -1) != si) for mu in range(n)]
    return min(range(n), key=lambda mu: dist[mu])
