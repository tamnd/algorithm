# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-gradient-autofocus/. The authors are listed in prov/Y2C9T3.jsonl.
"""Phase gradient autofocus (PGA) for a complex SAR image.

Layout: img[m][j], row m a range bin, column j a cross-range (azimuth) pixel.
The azimuth phase history of row m is H_m = DFT(img[m]) (the Fourier sign is
exp(-i 2 pi f t), the sign of the DFT). An unknown phase error phi(k) of the
aperture, the same for every range bin, multiplies every H_m(k) by
exp(i phi(k)) and blurs the image in azimuth. PGA estimates phi from the
image itself and removes it. A constant and a linear part of phi only shift
the image, so PGA estimates phi up to a + b k and removes that part.
"""

import cmath
import math

from imgkit import dft, idft


def apply_phase(img, phi):
    """Multiply the azimuth phase history of every row by exp(i phi(k))."""
    rot = [cmath.exp(1j * p) for p in phi]
    return [idft([h * r for h, r in zip(dft(row), rot)]) for row in img]


def remove_linear(phi):
    """phi minus its least-squares line a + b k."""
    n = len(phi)
    km = (n - 1) / 2.0
    pm = sum(phi) / n
    skk = sum((k - km) ** 2 for k in range(n))
    b = sum((k - km) * (p - pm) for k, p in enumerate(phi)) / skk
    return [p - pm - b * (k - km) for k, p in enumerate(phi)]


def _window_width(rows, min_width):
    """Twice the distance from the center to the edge of the -10 dB region of the summed intensity."""
    n = len(rows[0])
    c = n // 2
    s = [sum(abs(r[j]) ** 2 for r in rows) for j in range(n)]
    top = s[c]
    half = 0
    while half < c and s[c - half - 1] >= 0.1 * top and s[(c + half + 1) % n] >= 0.1 * top:
        half += 1
    return max(min_width, int(1.5 * (2 * half + 1)))


def pga_once(img, width=None, min_width=16):
    """One PGA iteration. Returns (phase estimate, window width used).

    width=None picks the window from the -10 dB width of the summed
    intensity; width=n keeps whole rows.
    """
    n = len(img[0])
    c = n // 2
    shifted = []
    for row in img:
        jmax = max(range(n), key=lambda j: abs(row[j]))
        shifted.append([row[(j + jmax - c) % n] for j in range(n)])  # @line L1
    w = _window_width(shifted, min_width) if width is None else width
    lo, hi = c - w // 2, c - w // 2 + w
    windowed = [[v if lo <= j < hi else 0j for j, v in enumerate(row)] for row in shifted]  # @line L2
    hist = [dft(row) for row in windowed]  # @line L3
    grad = [cmath.phase(sum(h[k] * h[k - 1].conjugate() for h in hist)) for k in range(1, n)]  # @line L4
    # The mean gradient is a linear phase (a shift). Remove it on the circle
    # first, so that the integration does not pick up 2 pi jumps.
    mean = cmath.phase(sum(cmath.exp(1j * g) for g in grad))
    phi = [0.0]
    for g in grad:
        phi.append(phi[-1] + cmath.phase(cmath.exp(1j * (g - mean))))  # @line L5
    return remove_linear(phi), w  # @line L5


def pga(img, iterations=8, width=None, tol=0.01, min_width=16):
    """Iterate PGA: estimate, correct, repeat. Returns (focused image, total phase estimate)."""
    n = len(img[0])
    total = [0.0] * n
    cur = img
    for _ in range(iterations):
        est, _ = pga_once(cur, width, min_width)
        cur = apply_phase(cur, [-p for p in est])  # @line L6
        total = [t + p for t, p in zip(total, est)]
        rms = math.sqrt(sum(p * p for p in est) / n)
        if rms < tol:  # @line L7
            break
    return cur, remove_linear(total)
