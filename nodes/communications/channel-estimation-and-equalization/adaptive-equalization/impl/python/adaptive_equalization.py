# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-equalization/. The authors are listed in prov/FM2HQC.jsonl.

"""An adaptive linear equalizer with a training mode and a decision mode.

The equalizer is an FIR filter c of N taps with output
z[k] = sum_i c[i] y[k-i], which estimates the symbol a[k-d] for a fixed
delay d. While known training symbols remain, the target is the training
symbol. After that, the target is the constellation point nearest to z.
The update is the LMS step c <- c - mu (z - target) conj(u).

wiener_taps gives the MMSE taps for a known channel, the point that LMS in
training mode converges to on average.
"""

import cbb


def nearest(z: complex, points: list[complex]) -> complex:
    """The constellation point closest to z."""
    return min(points, key=lambda p: abs(z - p))


def adaptive_equalize(
    y: list[complex], train: list[complex], n: int, delay: int, mu: float, points: list[complex]
) -> tuple[list[complex], list[complex], list[complex]]:
    """Run the equalizer over y.

    train[t] is the known symbol a[t] for t < len(train). Returns the final
    taps, the outputs z[k] and the targets used, for k = N-1, ..., len(y)-1;
    output k estimates a[k - delay].
    """
    if n < 1 or not 0 <= delay <= n - 1 or mu <= 0 or not points:
        raise ValueError("need N >= 1, 0 <= delay <= N - 1, mu > 0 and a constellation")
    c = [0j] * n  # @line L1
    outs, targets = [], []
    for k in range(n - 1, len(y)):  # @line L2
        u = [complex(y[k - i]) for i in range(n)]  # @line L3
        z = sum(ci * ui for ci, ui in zip(c, u))  # @line L4
        if k - delay < len(train):  # @line L5
            target = complex(train[k - delay])  # @line L5
        else:
            target = nearest(z, points)  # @line L6
        e = z - target  # @line L7
        c = [ci - mu * e * ui.conjugate() for ci, ui in zip(c, u)]  # @line L8
        outs.append(z)
        targets.append(target)
    return c, outs, targets  # @line L9


def wiener_taps(h: list[complex], n: int, delay: int, n0: float, es: float = 1.0) -> list[complex]:
    """The MMSE taps c that minimize E|sum_i c[i] y[k-i] - a[k-delay]|^2 for a known channel.

    With u = H a + w, H[i][m] = h[m - i], R = es H H^H + n0 I and
    p = es H[:, delay], the optimum is c = conj(R^-1 p).
    """
    m = n + len(h) - 1
    hm = [[complex(h[col - i]) if 0 <= col - i < len(h) else 0j for col in range(m)] for i in range(n)]
    r = cbb.add(cbb.scale(es, cbb.matmul(hm, cbb.herm(hm))), cbb.scale(n0, cbb.eye(n)))
    p = [es * hm[i][delay] for i in range(n)]
    return [v.conjugate() for v in cbb.solve(r, p)]


def mse(c: list[complex], h: list[complex], delay: int, n0: float, es: float = 1.0) -> float:
    """The mean square error E|z - a[k-delay]|^2 of taps c on a known channel."""
    g = cbb.conv(c, h)
    isi = sum(abs(v) ** 2 for i, v in enumerate(g) if i != delay)
    cursor = g[delay] if delay < len(g) else 0j
    return es * (isi + abs(cursor - 1) ** 2) + n0 * cbb.norm2(c)
