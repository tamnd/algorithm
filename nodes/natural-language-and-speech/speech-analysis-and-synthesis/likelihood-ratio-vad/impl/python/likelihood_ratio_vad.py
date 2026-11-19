# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/likelihood-ratio-vad/. The authors are listed in prov/4HXQ9X.jsonl.

"""Statistical model voice activity detection (Sohn, Kim and Sung).

Each DFT bin X_k of a frame is complex Gaussian with variance lambda_k under H0
(noise only) and lambda_k (1 + xi_k) under H1 (speech plus noise), where
lambda_k is the noise power and xi_k the a priori SNR. With the a posteriori
SNR gamma_k = |X_k|^2 / lambda_k, the likelihood ratio of one bin is

    Lambda_k = p(X_k | H1) / p(X_k | H0) = exp(gamma_k xi_k / (1 + xi_k)) / (1 + xi_k).

The bins are independent under the model, so the frame ratio is the product.
The a priori SNR comes from the decision-directed rule, and an HMM of two states
(0 noise, 1 speech) smooths the decisions over time: G(n), the ratio of the two
forward variables, follows

    G(n) = Lambda(n) (a01 + a11 G(n - 1)) / (a00 + a10 G(n - 1)),

which is the posterior odds of speech in frame n given frames 1 to n. Everything
is computed in log space.
"""

import math
from typing import List, Sequence, Tuple

from nlsdsp import fft, frames, hamming
from nlslog import log_add


def log_lr_bin(gamma: float, xi: float) -> float:
    """log Lambda_k = gamma xi / (1 + xi) - log(1 + xi)."""
    return gamma * xi / (1.0 + xi) - math.log1p(xi)


def decision_directed(prev_amp2: float, noise: float, gamma: float, alpha: float, xi_min: float) -> float:
    """xi = max(alpha A^2 / lambda + (1 - alpha) max(gamma - 1, 0), xi_min), A^2 the previous clean power estimate."""
    return max(alpha * prev_amp2 / noise + (1.0 - alpha) * max(gamma - 1.0, 0.0), xi_min)


def hmm_log_odds(log_lambdas: Sequence[float], a01: float, a10: float) -> List[float]:
    """log G(n) for every frame, from the stationary prior odds a01 / a10."""
    a00, a11 = 1.0 - a01, 1.0 - a10
    la00, la01, la10, la11 = (math.log(v) for v in (a00, a01, a10, a11))
    lg = math.log(a01 / a10)
    out = []
    for ll in log_lambdas:
        lg = ll + log_add(la01, la11 + lg) - log_add(la00, la10 + lg)  # @line L6
        out.append(lg)
    return out


def vad(
    x: Sequence[float],
    frame_len: int = 256,
    hop: int = 128,
    init_frames: int = 10,
    alpha: float = 0.98,
    xi_min: float = 10 ** (-2.5),
    noise_update: float = 0.98,
    a01: float = 0.2,
    a10: float = 0.1,
    log_eta: float = 10.0,
) -> Tuple[List[int], List[float], List[float]]:
    """Return (decisions, log Lambda per frame, log G per frame). The first init_frames frames must be noise.

    frame_len must be a power of 2. The decision is 1 (speech) when log G(n) > log_eta. The
    default log_eta = 10 is tuned for frames of 256 samples (129 bins), not derived.
    """
    w = hamming(frame_len)
    spectra = []
    for fr in frames(x, frame_len, hop):  # @line L1
        spec = fft([v * wi for v, wi in zip(fr, w)])
        spectra.append([abs(spec[k]) ** 2 for k in range(frame_len // 2 + 1)])
    if len(spectra) < init_frames or init_frames < 1:
        raise ValueError("need at least init_frames frames, and init_frames >= 1")
    nbins = frame_len // 2 + 1
    noise = [sum(s[k] for s in spectra[:init_frames]) / init_frames for k in range(nbins)]  # @line L2
    noise = [max(v, 1e-12) for v in noise]
    prev_amp2 = [0.0] * nbins
    a00, a11 = 1.0 - a01, 1.0 - a10
    la00, la01, la10, la11 = (math.log(v) for v in (a00, a01, a10, a11))
    lg = math.log(a01 / a10)
    decisions, log_lambdas, log_odds = [], [], []
    for pw in spectra:
        total = 0.0
        xis = []
        for k in range(nbins):
            gamma = pw[k] / noise[k]  # @line L3
            xi = decision_directed(prev_amp2[k], noise[k], gamma, alpha, xi_min)  # @line L4
            xis.append(xi)
            total += log_lr_bin(gamma, xi)  # @line L5
        lg = total + log_add(la01, la11 + lg) - log_add(la00, la10 + lg)  # @line L6
        speech = 1 if lg > log_eta else 0  # @line L7
        for k in range(nbins):  # @line L8
            g = xis[k] / (1.0 + xis[k])
            prev_amp2[k] = g * g * pw[k]
            if not speech:
                noise[k] = noise_update * noise[k] + (1.0 - noise_update) * pw[k]
        decisions.append(speech)
        log_lambdas.append(total)
        log_odds.append(lg)
    return decisions, log_lambdas, log_odds
