# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/whitened-matched-filter/. The authors are listed in prov/35K4A5.jsonl.

"""Forney's whitened matched filter on a discrete-time ISI channel.

The channel is y[k] = sum_l h[l] x[k-l] + w[k] with w white CN(0, N0). The
matched filter output z = h~ * y (h~[l] = conj(h[-l])) has the folded spectrum
R(z) = H(z) H*(1/z*) of the channel autocorrelation, and colored noise.
Factor R(z) = F(z) F*(1/z*) with F minimum phase (all zeros inside or on the
unit circle). The whitening filter 1/F*(1/z*) after the matched filter gives
y' = f * x + n' with n' white CN(0, N0) again. The receiver can then run the
Viterbi equalizer on the causal, minimum-phase channel f.

Here the receiver knows h, so F is found by reflecting the zeros of H(z) that lie
outside the unit circle to their conjugate reciprocals, and scaling so that
|F| = |H| on the unit circle. The zeros come from the Durand-Kerner iteration.
"""

import cmath
import math


def autocorrelation(h: list[complex]) -> list[complex]:
    """R[k] = sum_l h[l + k] conj(h[l]) for k = 0..L-1; R[-k] = conj(R[k])."""
    n = len(h)
    return [sum(complex(h[l + k]) * complex(h[l]).conjugate() for l in range(n - k)) for k in range(n)]


def poly_roots(c: list[complex], iters: int = 500, tol: float = 1e-14) -> list[complex]:
    """The roots of c[0] z^d + c[1] z^(d-1) + ... + c[d] by the Durand-Kerner iteration."""
    while c and c[0] == 0:
        c = c[1:]
    d = len(c) - 1
    if d < 1:
        return []
    a = [complex(v) / c[0] for v in c]
    rad = 1.0 + max(abs(v) for v in a[1:])
    z = [rad * 0.9 * cmath.exp(2j * math.pi * (i + 0.25) / d) for i in range(d)]
    for _ in range(iters):
        move = 0.0
        for i in range(d):
            p = 0j
            for v in a:
                p = p * z[i] + v
            den = 1 + 0j
            for k in range(d):
                if k != i:
                    den *= z[i] - z[k]
            step = p / den if den != 0 else 1e-3
            z[i] -= step
            move = max(move, abs(step))
        if move < tol * rad:
            break
    return z


def min_phase_factor(h: list[complex]) -> list[complex]:
    """The minimum-phase f with |F| = |H| on the unit circle and f[0] real and positive."""
    while len(h) > 1 and h[-1] == 0:
        h = h[:-1]
    if not h or h[0] == 0:
        raise ValueError("need h[0] != 0")
    zeros = poly_roots(list(h))  # @line L2
    gain = abs(h[0])
    inside = []
    for r in zeros:  # @line L3
        if abs(r) > 1.0:
            gain *= abs(r)
            inside.append(1.0 / r.conjugate())
        else:
            inside.append(r)
    f = [complex(gain)]
    for r in inside:  # @line L4
        f = [(f[i] if i < len(f) else 0) - (r * f[i - 1] if i >= 1 else 0) for i in range(len(f) + 1)]
    return f


def all_spectral_factors(h: list[complex]) -> list[list[complex]]:
    """Every factor g with |G| = |H| on the unit circle, one per choice of reflected zeros (up to a phase)."""
    zeros = poly_roots(list(h))
    out = []
    for mask in range(1 << len(zeros)):
        gain = abs(h[0])
        rs = []
        for i, r in enumerate(zeros):
            if mask >> i & 1:
                gain *= abs(r)
                rs.append(1.0 / r.conjugate())
            else:
                rs.append(r)
        g = [complex(gain)]
        for r in rs:
            g = [(g[i] if i < len(g) else 0) - (r * g[i - 1] if i >= 1 else 0) for i in range(len(g) + 1)]
        out.append(g)
    return out


def freq(h: list[complex], w: float) -> complex:
    """H(e^{jw}) = sum_l h[l] e^{-jwl}."""
    return sum(complex(v) * cmath.exp(-1j * w * l) for l, v in enumerate(h))


def whitened_matched_filter(h: list[complex], y: list[complex]) -> tuple[list[complex], list[complex]]:
    """The minimum-phase channel f and the whitened samples y' with y' = f * x + white noise.

    y is the received block y[0..K-1]; samples after it are taken as 0. The
    output has the same length as y.
    """
    f = min_phase_factor(h)  # @line L1
    n, taps = len(y), len(h)
    z = [sum(complex(h[l]).conjugate() * y[k + l] for l in range(taps) if k + l < n) for k in range(n)]  # @line L5
    out = [0j] * n
    for k in range(n - 1, -1, -1):  # @line L6
        acc = z[k] - sum(f[l].conjugate() * out[k + l] for l in range(1, len(f)) if k + l < n)
        out[k] = acc / f[0].conjugate()  # @line L7
    return f, out  # @line L8
