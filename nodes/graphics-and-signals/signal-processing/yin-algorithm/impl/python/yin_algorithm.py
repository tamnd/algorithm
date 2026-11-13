# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yin-algorithm/. The authors are listed in prov/QXNECT.jsonl.

"""The YIN period estimator of de Cheveigne and Kawahara (2002), steps 2 to 5.

Lags tau and periods are in samples; the frequency is fs / period in Hz.
On integer input every quantity is an exact integer or Fraction.

  d(tau)  = sum_{j=t}^{t+W-1} (x[j] - x[j+tau])^2                 difference function
  d'(0)   = 1,  d'(tau) = d(tau) / ((1/tau) sum_{j=1}^{tau} d(j))  cumulative mean normalized
  step 4: the first tau with d'(tau) < threshold, moved on to the bottom of its dip;
          if no tau qualifies, the global minimum of d'
  step 5: a parabola through d(tau-1), d(tau), d(tau+1) refines tau
"""

from fractions import Fraction
from typing import Optional, Sequence


def difference_direct(x: Sequence[int], t: int, w: int, tau_max: int) -> list:
    """The sum straight from the definition. It needs x[t .. t + w + tau_max - 1]."""
    return [sum((x[j] - x[j + tau]) ** 2 for j in range(t, t + w)) for tau in range(tau_max + 1)]


def difference_fast(x: Sequence[int], t: int, w: int, tau_max: int) -> list:
    """d(tau) = e(t) + e(t + tau) - 2 r_t(tau), with windowed energies e from prefix sums.

    r_t(tau) = sum_{j=t}^{t+w-1} x[j] x[j+tau] is a cross-correlation, so an FFT
    gives all lags in O((w + tau_max) log(w + tau_max)); here it is the direct sum.
    """
    prefix = [0]
    for v in x[: t + w + tau_max]:
        prefix.append(prefix[-1] + v * v)

    def energy(s):
        return prefix[s + w] - prefix[s]

    out = []
    for tau in range(tau_max + 1):  # @line L1
        r = sum(x[j] * x[j + tau] for j in range(t, t + w))
        out.append(energy(t) + energy(t + tau) - 2 * r)
    return out


def cmndf(d: Sequence) -> list:
    """The cumulative mean normalized difference d'. A lag with no energy so far gets 1."""
    out = [Fraction(1)]  # @line L2
    running = 0
    for tau in range(1, len(d)):  # @line L3
        running += d[tau]  # @line L4
        out.append(Fraction(d[tau] * tau, running) if running else Fraction(1))  # @line L5
    return out


def absolute_threshold(dp: Sequence, threshold) -> int:
    """Step 4. The first lag below the threshold, then down to the local minimum; else the global minimum."""
    for tau in range(1, len(dp)):  # @line L6
        if dp[tau] < threshold:
            while tau + 1 < len(dp) and dp[tau + 1] < dp[tau]:  # @line L7
                tau += 1
            return tau
    return global_minimum(dp)  # @line L8


def global_minimum(dp: Sequence) -> int:
    """The lag of the smallest d'(tau), tau >= 1; ties go to the smallest lag."""
    return min(range(1, len(dp)), key=lambda tau: (dp[tau], tau))  # @line L8


def parabolic(d: Sequence, tau: int) -> Fraction:
    """Step 5. The abscissa of the vertex of the parabola through (tau-1, tau, tau+1) on d."""
    if tau < 1 or tau + 1 >= len(d):  # @line L9
        return Fraction(tau)
    a, b, c = d[tau - 1], d[tau], d[tau + 1]
    den = a - 2 * b + c
    if den == 0:
        return Fraction(tau)  # @line L11
    return tau + Fraction(a - c, 2 * den)  # @line L10


def yin(x: Sequence[int], t: int, w: int, tau_max: int, threshold=Fraction(1, 10), use_threshold: bool = True) -> tuple[Fraction, int, Optional[list]]:
    """The period estimate in samples, the integer lag before refinement, and d'."""
    d = difference_fast(x, t, w, tau_max)
    dp = cmndf(d)
    tau = absolute_threshold(dp, threshold) if use_threshold else global_minimum(dp)
    return parabolic(d, tau), tau, dp
