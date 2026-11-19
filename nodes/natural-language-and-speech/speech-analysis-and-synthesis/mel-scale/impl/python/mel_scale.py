# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mel-scale/. The authors are listed in prov/AJSQPY.jsonl.

"""Two mel scales and their inverses.

The O'Shaughnessy form, used by HTK, Kaldi and most speech toolkits:

    m(f) = 2595 log_10(1 + f / 700).

The Slaney form, used by the Auditory Toolbox and by librosa (its default) and
torchaudio when the "slaney" scale is asked for: linear below 1 kHz with a step
of f_sp = 200 / 3 Hz per mel, so 1 kHz is 15 mel; above 1 kHz a log step of
ln(6.4) / 27 per mel. The two scales use different units and agree only in shape.
"""

import math

F_SP = 200.0 / 3.0
MIN_LOG_HZ = 1000.0
MIN_LOG_MEL = MIN_LOG_HZ / F_SP  # 15
LOG_STEP = math.log(6.4) / 27.0


def hz_to_mel(f: float) -> float:
    """m = 2595 log_10(1 + f / 700), f in Hz and f >= 0."""
    if f < 0:
        raise ValueError("the frequency must be at least 0")
    return 2595.0 * math.log10(1.0 + f / 700.0)


def mel_to_hz(m: float) -> float:
    """f = 700 (10^(m / 2595) - 1), the inverse of hz_to_mel."""
    return 700.0 * (10.0 ** (m / 2595.0) - 1.0)


def hz_to_mel_slaney(f: float) -> float:
    """f / f_sp below 1 kHz, 15 + ln(f / 1000) / (ln(6.4) / 27) from 1 kHz up."""
    if f < 0:
        raise ValueError("the frequency must be at least 0")
    if f < MIN_LOG_HZ:
        return f / F_SP
    return MIN_LOG_MEL + math.log(f / MIN_LOG_HZ) / LOG_STEP


def mel_to_hz_slaney(m: float) -> float:
    """The inverse of hz_to_mel_slaney."""
    if m < MIN_LOG_MEL:
        return m * F_SP
    return MIN_LOG_HZ * math.exp(LOG_STEP * (m - MIN_LOG_MEL))
