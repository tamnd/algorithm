# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polyphase-decomposition/. The authors are listed in prov/AYGB1S.jsonl.

"""Polyphase decomposition of an FIR filter and the decimator and interpolator built on it.

H(z) = sum_(j=0..M-1) z^(-j) E_j(z^M) with e_j[i] = h[iM + j]. Signals start
at index 0 and are zero before it. The filter h has K taps.
"""

from typing import Sequence


def polyphase_components(h: Sequence, m: int) -> list[list]:
    """The M components e_j = h[j], h[j + M], h[j + 2M], ..."""
    return [list(h[j::m]) for j in range(m)]


def convolve(h: Sequence, x: Sequence) -> list:
    """Full linear convolution, length len(h) + len(x) - 1."""
    if not h or not x:
        return []
    y = [0] * (len(h) + len(x) - 1)
    for i, a in enumerate(h):
        for j, b in enumerate(x):
            y[i + j] += a * b
    return y


def downsample(x: Sequence, m: int) -> list:
    return list(x[::m])


def upsample(x: Sequence, l: int) -> list:
    y = [0] * (len(x) * l)
    y[::l] = list(x)
    return y


def polyphase_decimate(h: Sequence, x: Sequence, m: int) -> list:
    """y[n] = sum_k h[k] x[nM - k] for n with nM < len(h) + len(x) - 1, at the low rate.

    Branch j filters the phase x_j[n] = x[nM - j] with e_j, and the branches add.
    Each output costs K multiplies in total, not K M.
    """
    total = len(h) + len(x) - 1
    count = (total - 1) // m + 1 if total > 0 else 0
    e = polyphase_components(h, m)  # @line L1
    y = [0] * count
    for j in range(m):  # @line L2
        for n in range(count):  # @line L3
            acc = 0
            for i, c in enumerate(e[j]):  # @line L4
                idx = (n - i) * m - j  # x_j[n - i] = x[(n - i) M - j]
                if 0 <= idx < len(x):
                    acc += c * x[idx]  # @line L5
            y[n] += acc  # @line L6
    return y


def polyphase_interpolate(h: Sequence, x: Sequence, l: int) -> list:
    """y[n] = sum_k h[k] u[n - k] with u the L-fold upsampled x, computed from x directly.

    Output n = qL + r uses only e_r: y[qL + r] = sum_i h[iL + r] x[q - i].
    Each output costs about K / L multiplies.
    """
    total = len(h) + len(x) * l - 1
    e = polyphase_components(h, l)  # @line L7
    y = [0] * max(total, 0)
    for n in range(len(y)):  # @line L8
        q, r = divmod(n, l)  # @line L9
        acc = 0
        for i, c in enumerate(e[r]):  # @line L10
            if 0 <= q - i < len(x):
                acc += c * x[q - i]
        y[n] = acc  # @line L11
    return y
