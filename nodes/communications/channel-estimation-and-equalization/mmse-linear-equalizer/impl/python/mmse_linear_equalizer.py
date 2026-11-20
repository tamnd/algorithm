# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mmse-linear-equalizer/. The authors are listed in prov/4T3X0R.jsonl.

"""The finite-length MMSE linear equalizer.

The channel is y[k] = sum_{l=0}^{L-1} h[l] x[k-l] + w[k] at one sample per
symbol. The symbols are independent with mean zero and E|x|^2 = Es, and the
noise is CN(0, N0), independent of the symbols. The equalizer is an FIR filter
c of N taps with output z[k] = sum_i c[i] y[k-i], and z[k] estimates
x[k - D] for a decision delay D. The regressor u = (y[k], ..., y[k-N+1]) is
u = H s + w with H[i][j] = h[j-i] (an N by N + L - 1 matrix) and
s = (x[k], ..., x[k-N-L+2]). With f = conj(c), so that z = f^H u, the
Wiener-Hopf equations are R f = r with R = Es H H^H + N0 I and r = Es H e_D.
The minimum mean squared error is J = Es - r^H f.
"""

import cbb


def channel_matrix(h: list[complex], n: int) -> list[list[complex]]:
    """The N by N + L - 1 matrix H with H[i][j] = h[j - i], so that u = H s + w."""
    taps = len(h)
    if taps < 1 or n < 1:
        raise ValueError("need L >= 1 and N >= 1")
    return [[complex(h[j - i]) if 0 <= j - i < taps else 0j for j in range(n + taps - 1)] for i in range(n)]


def mmse_equalizer(h: list[complex], n: int, delay: int, n0: float, es: float = 1.0) -> tuple[list[complex], float]:
    """The N taps c that minimize E|z[k] - x[k - delay]|^2, and that minimum J."""
    if n0 < 0 or es <= 0:
        raise ValueError("need N0 >= 0 and Es > 0")
    if not 0 <= delay <= n + len(h) - 2:
        raise ValueError("need 0 <= delay <= N + L - 2")
    hm = channel_matrix(h, n)  # @line L1
    m = len(hm[0])
    big_r = [[es * sum(hm[i][t] * hm[k][t].conjugate() for t in range(m)) + (n0 if i == k else 0) for k in range(n)] for i in range(n)]  # @line L2
    r = [es * hm[i][delay] for i in range(n)]  # @line L3
    try:
        f = cbb.solve(big_r, r)  # @line L4
    except ValueError:
        raise ValueError("R is singular: N0 = 0 and H does not have full row rank") from None
    c = [v.conjugate() for v in f]  # @line L5
    j = es - cbb.dot(r, f).real  # @line L6
    return c, j  # @line L7


def best_delay(h: list[complex], n: int, n0: float, es: float = 1.0) -> tuple[int, list[complex], float]:
    """The decision delay with the smallest MMSE, found by trying all N + L - 1 delays."""
    best = None
    for d in range(n + len(h) - 1):
        c, j = mmse_equalizer(h, n, d, n0, es)
        if best is None or j < best[2]:
            best = (d, c, j)
    return best


def mse(c: list[complex], h: list[complex], delay: int, n0: float, es: float = 1.0) -> float:
    """E|z[k] - x[k - delay]|^2 for any taps c: Es ||c * h - e_delay||^2 + N0 ||c||^2."""
    g = cbb.conv(c, h)
    return es * sum(abs(v - (1 if k == delay else 0)) ** 2 for k, v in enumerate(g)) + n0 * cbb.norm2(c)


def bias(j: float, es: float = 1.0) -> float:
    """The gain of the MMSE output on the wanted symbol: E[z | x[k - delay]] = (1 - J / Es) x[k - delay]."""
    return 1.0 - j / es


def unbiased_sinr(j: float, es: float = 1.0) -> float:
    """The signal to interference plus noise ratio after the bias is removed: Es / J - 1."""
    return es / j - 1.0


def equalize(c: list[complex], y: list[complex], delay: int, count: int) -> list[complex]:
    """The equalizer output z = c * y, read at the delay: the estimates of x[0], ..., x[count - 1]."""
    z = cbb.conv(c, y)
    if len(z) < delay + count:
        z = z + [0j] * (delay + count - len(z))
    return z[delay : delay + count]
