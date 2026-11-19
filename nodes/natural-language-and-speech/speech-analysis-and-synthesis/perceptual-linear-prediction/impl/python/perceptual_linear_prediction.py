# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/perceptual-linear-prediction/. The authors are listed in prov/H7TRFV.jsonl.

"""Perceptual linear prediction (PLP) of one frame, after Hermansky (1990).

Steps: the power spectrum of the windowed frame; critical band integration with
the masking curve psi on the Bark scale Omega(f) = 6 asinh(f / 600); the equal
loudness weight E(omega) of the paper (the form for a band up to about 5 kHz);
the cube root law Phi = Xi^0.33; an all-pole model of order p fitted to Phi
through its autocorrelation (the inverse DFT of Phi) and the Levinson-Durbin
recursion; and the cepstrum of the all-pole model.

The integration sums over the FFT bins with the weight psi(Omega_i - Omega(f_k)),
in place of the paper's resampling of the warped spectrum. The band centers are
M = ceil(Omega(fs / 2)) + 1 points equally spaced from 0 to Omega(fs / 2), a little
under 1 Bark apart. The LPC sign convention is A(z) = 1 - sum a_k z^-k.
"""

import math
from typing import List, Optional, Sequence, Tuple

from nlsdsp import hamming, levinson, power_spectrum


def hz_to_bark(f: float) -> float:
    """Omega(f) = 6 ln(f / 600 + sqrt((f / 600)^2 + 1)) = 6 asinh(f / 600), f in Hz."""
    return 6.0 * math.asinh(f / 600.0)


def bark_to_hz(b: float) -> float:
    return 600.0 * math.sinh(b / 6.0)


def masking_curve(z: float) -> float:
    """The critical band curve psi of Hermansky (1990), z in Bark (target minus masker)."""
    if z < -1.3 or z > 2.5:
        return 0.0
    if z < -0.5:
        return 10.0 ** (2.5 * (z + 0.5))
    if z <= 0.5:
        return 1.0
    return 10.0 ** (-1.0 * (z - 0.5))


def equal_loudness(f: float) -> float:
    """E(omega) = (omega^2 + 56.8e6) omega^4 / ((omega^2 + 6.3e6)^2 (omega^2 + 0.38e9)), omega = 2 pi f."""
    w2 = (2.0 * math.pi * f) ** 2
    return (w2 + 56.8e6) * w2 * w2 / ((w2 + 6.3e6) ** 2 * (w2 + 0.38e9))


def band_centers(fs: float) -> List[float]:
    top = hz_to_bark(fs / 2.0)
    m = int(math.ceil(top)) + 1
    return [i * top / (m - 1) for i in range(m)]


def critical_band_weights(nfft: int, fs: float) -> Tuple[List[float], List[List[float]]]:
    """The band centers in Bark and the weights W[i][k] = psi(Omega_i - Omega(f_k))."""
    centers = band_centers(fs)
    barks = [hz_to_bark(k * fs / nfft) for k in range(nfft // 2 + 1)]
    return centers, [[masking_curve(c - b) for b in barks] for c in centers]


def autocorrelation_of_spectrum(phi: Sequence[float], max_lag: int) -> List[float]:
    """The inverse DFT of the even extension of phi_0 .. phi_{M-1} (a spectrum on 0 to pi):
    r[k] = phi_0 + 2 sum_{i=1}^{M-2} phi_i cos(pi k i / (M - 1)) + phi_{M-1} cos(pi k), over 2 (M - 1)."""
    m = len(phi)
    n = 2 * (m - 1)
    out = []
    for k in range(max_lag + 1):
        s = phi[0] + phi[-1] * math.cos(math.pi * k)
        s += 2.0 * sum(phi[i] * math.cos(math.pi * k * i / (m - 1)) for i in range(1, m - 1))
        out.append(s / n)
    return out


def lpc_to_cepstrum(a: Sequence[float], gain: float, n: int) -> List[float]:
    """The cepstrum c_0 .. c_{n-1} of the model spectrum gain / |A(e^{jw})|^2.

    c_0 = ln gain, and for m >= 1, c_m = a_m + sum_{k=1}^{m-1} (k / m) c_k a_{m-k},
    with a_m = 0 for m > p. This is the Fourier series of the log model spectrum."""
    p = len(a)
    c = [math.log(gain)] + [0.0] * (n - 1)
    for m in range(1, n):
        acc = a[m - 1] if m <= p else 0.0
        for k in range(max(1, m - p), m):
            acc += (k / m) * c[k] * a[m - k - 1]
        c[m] = acc
    return c


def plp_frame(
    frame: Sequence[float],
    fs: float = 8000.0,
    order: int = 5,
    num_ceps: Optional[int] = None,
    nfft: Optional[int] = None,
    weights=None,
) -> Tuple[List[float], List[float], float, List[float]]:
    """PLP of one frame. Returns (cepstrum, a, gain, phi): the cepstrum c_0 .. c_{num_ceps-1}
    of the all-pole model, the predictor a_1 .. a_p, the model gain and the auditory spectrum phi."""
    if nfft is None:
        nfft = 1 << max(1, (len(frame) - 1).bit_length())
    if num_ceps is None:
        num_ceps = order + 1
    win = hamming(len(frame))
    p = power_spectrum([s * w for s, w in zip(frame, win)], nfft)  # @line L1
    centers, w = weights if weights is not None else critical_band_weights(nfft, fs)  # @line L2
    theta = [sum(wi * pk for wi, pk in zip(row, p)) for row in w]  # @line L3
    xi = [equal_loudness(bark_to_hz(c)) * t for c, t in zip(centers, theta)]  # @line L4
    phi = [v ** 0.33 for v in xi]  # @line L5
    phi[0], phi[-1] = phi[1], phi[-2]  # @line L6
    r = autocorrelation_of_spectrum(phi, order)  # @line L7
    a, gain = levinson(r, order)  # @line L8
    return lpc_to_cepstrum(a, gain, num_ceps), a, gain, phi  # @line L9


def model_spectrum(a: Sequence[float], gain: float, omega: float) -> float:
    """gain / |A(e^{j omega})|^2 with A(z) = 1 - sum a_k z^-k."""
    re = 1.0 - sum(ak * math.cos(omega * (k + 1)) for k, ak in enumerate(a))
    im = sum(ak * math.sin(omega * (k + 1)) for k, ak in enumerate(a))
    return gain / (re * re + im * im)
