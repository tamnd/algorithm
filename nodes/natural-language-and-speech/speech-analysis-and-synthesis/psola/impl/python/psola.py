# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/psola/. The authors are listed in prov/Z76XPX.jsonl.

"""Time-domain pitch-synchronous overlap-add (TD-PSOLA).

The input is a voiced signal x and its analysis pitch marks t_1 < ... < t_M, one
per pitch period (for example the glottal closure instants). Around each mark a
segment of two local periods is cut with a Hann window. The segments are added
again at synthesis marks whose spacing is the local period divided by beta, so
the pitch is multiplied by beta. The synthesis marks run over a time axis that is
alpha times longer, and each takes the segment of the analysis mark nearest to
its position on the original axis, so the duration is multiplied by alpha.
"""

from typing import List, Sequence

from nlsdsp import hann


def local_periods(marks: Sequence[int]) -> List[int]:
    """P_i = round((t_{i+1} - t_{i-1}) / 2) inside, and the one neighbor gap at the two ends."""
    m = len(marks)
    if m < 2:
        raise ValueError("need at least two pitch marks")
    out = []
    for i in range(m):
        if i == 0:
            p = marks[1] - marks[0]
        elif i == m - 1:
            p = marks[m - 1] - marks[m - 2]
        else:
            p = round((marks[i + 1] - marks[i - 1]) / 2)
        if p <= 0:
            raise ValueError("the pitch marks must be strictly increasing")
        out.append(p)
    return out


def segment(x: Sequence[float], center: int, period: int) -> List[float]:
    """Hann window of length 2 period + 1 times x[center - period .. center + period]; 0 outside x."""
    w = hann(2 * period + 1)
    out = []
    for j in range(2 * period + 1):
        n = center - period + j
        out.append(w[j] * x[n] if 0 <= n < len(x) else 0.0)
    return out


def synthesis_marks(marks: Sequence[int], beta: float, alpha: float) -> List[tuple]:
    """The list of (synthesis position, analysis index) pairs of TD-PSOLA."""
    if beta <= 0 or alpha <= 0:
        raise ValueError("beta and alpha must be positive")
    periods = local_periods(marks)
    out = []
    s = alpha * marks[0]
    i = 0
    while s <= alpha * marks[-1] + 1e-9:  # @line L3
        tau = s / alpha
        while i + 1 < len(marks) and abs(marks[i + 1] - tau) <= abs(marks[i] - tau):  # @line L4
            i += 1
        out.append((round(s), i))
        s += periods[i] / beta  # @line L7
    return out


def psola(x: Sequence[float], marks: Sequence[int], beta: float = 1.0, alpha: float = 1.0) -> List[float]:
    """Multiply the pitch by beta and the duration by alpha. Returns round(alpha len(x)) samples."""
    periods = local_periods(marks)  # @line L1
    y = [0.0] * round(alpha * len(x))  # @line L2
    for pos, i in synthesis_marks(marks, beta, alpha):
        seg = segment(x, marks[i], periods[i])  # @line L5
        for j, v in enumerate(seg):  # @line L6
            n = pos - periods[i] + j
            if 0 <= n < len(y):
                y[n] += v
    return y  # @line L8
