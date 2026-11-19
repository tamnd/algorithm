# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ephraim-malah-estimator/. The authors are listed in prov/EV1Q5W.jsonl.

"""The Ephraim-Malah MMSE short-time spectral amplitude estimator.

Each DFT bin is Y = X + D, with X and D independent complex Gaussians of
variances lambda_x and lambda_d. The a priori SNR is xi = lambda_x / lambda_d and
the a posteriori SNR is gamma = |Y|^2 / lambda_d. The estimate of the clean
amplitude A = |X| that minimizes E[(A - A_hat)^2] is A_hat = G(xi, gamma) |Y| with

    v = xi gamma / (1 + xi)
    G = (sqrt(pi) / 2) (sqrt(v) / gamma) exp(-v / 2) [(1 + v) I0(v / 2) + v I1(v / 2)],

where I0 and I1 are modified Bessel functions of the first kind. The phase of Y
is kept. The a priori SNR comes from the decision-directed rule.
"""

import math
from typing import Callable, List, Sequence

from nlsdsp import fft


def bessel_ie(nu: int, x: float) -> float:
    """exp(-x) I_nu(x) for nu in {0, 1} and x >= 0: the power series below 50, the asymptotic series above."""
    if x < 0:
        raise ValueError("x must be nonnegative")
    if x == 0.0:
        return 1.0 if nu == 0 else 0.0
    if x < 50.0:
        # I_nu(x) = sum_k (x / 2)^(2k + nu) / (k! (k + nu)!), summed with the factor exp(-x) in log space
        lx = math.log(x / 2.0)
        total = 0.0
        k = 0
        while True:
            t = math.exp((2 * k + nu) * lx - math.lgamma(k + 1) - math.lgamma(k + nu + 1) - x)
            total += t
            if k > x and t < 1e-17 * total:
                return total
            k += 1
    mu = 4.0 * nu * nu
    s, term = 1.0, 1.0
    for j in range(1, 6):
        term *= -(mu - (2 * j - 1) ** 2) / (j * 8.0 * x)
        s += term
    return s / math.sqrt(2.0 * math.pi * x)


def mmse_stsa_gain(xi: float, gamma: float) -> float:
    """The Ephraim-Malah gain G(xi, gamma) for xi > 0 and gamma > 0."""
    if xi <= 0 or gamma <= 0:
        raise ValueError("xi and gamma must be positive")
    v = xi * gamma / (1.0 + xi)
    # exp(-v / 2) I_nu(v / 2) = bessel_ie(nu, v / 2), so no exponential overflows
    return 0.5 * math.sqrt(math.pi * v) / gamma * ((1.0 + v) * bessel_ie(0, v / 2.0) + v * bessel_ie(1, v / 2.0))


def periodic_hann(n: int) -> List[float]:
    """w[i] = 0.5 - 0.5 cos(2 pi i / n); its shifts by n / 2 add to 1."""
    return [0.5 - 0.5 * math.cos(2.0 * math.pi * i / n) for i in range(n)]


def ifft(spec: Sequence[complex]) -> List[complex]:
    """The inverse DFT by the forward FFT of the conjugate."""
    n = len(spec)
    return [v.conjugate() / n for v in fft([s.conjugate() for s in spec])]


def enhance(
    y: Sequence[float],
    n: int = 256,
    init_frames: int = 10,
    alpha: float = 0.98,
    xi_min: float = 10 ** (-2.5),
    gain: Callable[[float, float], float] = mmse_stsa_gain,
) -> List[float]:
    """Enhance y frame by frame. The first init_frames frames must be noise. n must be a power of 2.

    gain(xi, gamma) is the spectral gain; the default is the Ephraim-Malah gain.
    """
    hop = n // 2
    w = periodic_hann(n)
    starts = list(range(0, len(y) - n + 1, hop))
    spectra = [fft([y[s + i] * w[i] for i in range(n)]) for s in starts]  # @line L1
    if len(spectra) < init_frames or init_frames < 1:
        raise ValueError("need at least init_frames frames")
    noise = [max(sum(abs(sp[k]) ** 2 for sp in spectra[:init_frames]) / init_frames, 1e-20) for k in range(n)]  # @line L2
    prev_amp2 = [0.0] * n
    out = [0.0] * len(y)
    for s, spec in zip(starts, spectra):
        clean = []
        for k in range(n):
            gamma = max(abs(spec[k]) ** 2 / noise[k], 1e-12)  # @line L3
            xi = max(alpha * prev_amp2[k] / noise[k] + (1.0 - alpha) * max(gamma - 1.0, 0.0), xi_min)  # @line L4
            g = gain(xi, gamma)  # @line L5
            clean.append(g * spec[k])  # @line L6
            prev_amp2[k] = (g * abs(spec[k])) ** 2
        frame = ifft(clean)  # @line L7
        for i in range(n):
            out[s + i] += frame[i].real
    return out
