# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zero-forcing-equalizer/. The authors are listed in prov/2260NZ.jsonl.

"""The finite-length zero-forcing (ZF) linear equalizer of Lucky.

The channel is y[k] = sum_{l=0}^{L-1} h[l] x[k-l] + w[k] at one sample per
symbol. The equalizer is an FIR filter c of N taps, and the combined
response is g = c * h, of length N + L - 1. For a chosen decision delay D,
the ZF equalizer forces g[D] = 1 and g[k] = 0 at the other N - 1 indices of a
window of N consecutive indices that contains D. This is an N by N linear
system A c = e with A[k][i] = h[s + k - i]. The output noise is N0 ||c||^2.
"""

import cbb


def forcing_window(taps: int, n: int, delay: int) -> int:
    """The first index s of the window s..s+N-1 of the combined response, centered on the delay if possible."""
    if taps < 1 or n < 1 or not 0 <= delay <= n + taps - 2:
        raise ValueError("need L >= 1, N >= 1 and 0 <= delay <= N + L - 2")
    return min(max(delay - (n - 1) // 2, 0), taps - 1)


def zf_equalizer(h: list[complex], n: int, delay: int) -> list[complex]:
    """The N taps c that make the combined response c * h equal to 1 at the delay and 0 at N - 1 indices around it."""
    taps = len(h)
    s = forcing_window(taps, n, delay)  # @line L1
    hh = lambda t: complex(h[t]) if 0 <= t < taps else 0j
    a = [[hh(s + k - i) for i in range(n)] for k in range(n)]  # @line L2
    e = [0j] * n
    e[delay - s] = 1 + 0j  # @line L3
    try:
        c = cbb.solve(a, e)  # @line L4
    except ValueError:
        raise ValueError("the forcing system is singular for this channel, length and delay") from None
    return c  # @line L5


def equalize(c: list[complex], y: list[complex], delay: int, count: int) -> list[complex]:
    """The equalizer output z = c * y, read at the delay: the estimates of x[0], ..., x[count - 1]."""
    z = cbb.conv(c, y)
    if len(z) < delay + count:
        z = z + [0j] * (delay + count - len(z))
    return z[delay : delay + count]


def combined_response(c: list[complex], h: list[complex]) -> list[complex]:
    """g = c * h, the response from the symbols to the equalizer output."""
    return cbb.conv(c, h)


def peak_distortion(g: list[complex], delay: int) -> float:
    """Lucky's peak distortion: the sum of |g[k]| over k != delay, divided by |g[delay]|."""
    return sum(abs(v) for k, v in enumerate(g) if k != delay) / abs(g[delay])


def noise_gain(c: list[complex]) -> float:
    """||c||^2: white noise of variance N0 at the input has variance N0 ||c||^2 at the output."""
    return cbb.norm2(c)
