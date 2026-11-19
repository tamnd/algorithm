# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rabiner-sambur-endpoint-detection/. The authors are listed in prov/B6AHEG.jsonl.

"""The endpoint detector of Rabiner and Sambur (1975) for an isolated word.

The signal is cut into frames of 10 ms with no overlap and no padding. Each frame
gets an energy E (the sum of the magnitudes of its samples) and a zero-crossing
count Z. The first 100 ms (10 frames) are taken to be background silence.

Two energy thresholds, ITL below ITU, give a first estimate (N1, N2) of the
word: N1 is the first frame where E rises above ITL and then goes above ITU before
it falls back to ITL or below; N2 is the same from the end. Then the zero-crossing
threshold IZCT moves N1 back (and N2 forward) over at most 25 frames, to take in
weak fricatives, when 3 or more of those frames have Z above IZCT.

The constants 0.03, 4, 5, 25 crossings, 2 standard deviations, 25 frames and
3 frames are the heuristic values of the paper. IMN is taken here as the mean
energy of the silence frames. A frame index is 0 based; the word is the frames
N1 to N2, both included.
"""

import math
from typing import List, Optional, Sequence, Tuple

from nlsdsp import frames


def frame_energy(frame: Sequence[float]) -> float:
    """E = sum of |s[n]| over the frame."""
    return sum(abs(v) for v in frame)


def zero_crossings(frame: Sequence[float]) -> int:
    """The number of n with sgn(s[n]) != sgn(s[n - 1]) inside the frame, where sgn(0) = +1."""
    return sum(1 for a, b in zip(frame, frame[1:]) if (a >= 0.0) != (b >= 0.0))


def features(x: Sequence[float], fs: float = 16000.0) -> Tuple[List[float], List[int]]:
    """E and Z of each 10 ms frame. A signal of L samples gives floor(L / (fs / 100)) frames."""
    n = int(round(fs / 100.0))
    fr = frames(x, n, n)
    return [frame_energy(f) for f in fr], [zero_crossings(f) for f in fr]


def thresholds(
    energy: Sequence[float], zcr: Sequence[int], silence_frames: int = 10, zc_fixed: float = 25.0
) -> Tuple[float, float, float]:
    """(ITL, ITU, IZCT) from the energy and zero-crossing sequences."""
    if len(energy) < silence_frames or silence_frames < 1:
        raise ValueError("the signal must hold the silence frames")
    sil_z = list(zcr[:silence_frames])
    izc = sum(sil_z) / len(sil_z)
    sigma = math.sqrt(sum((z - izc) ** 2 for z in sil_z) / len(sil_z))
    izct = min(zc_fixed, izc + 2.0 * sigma)  # @line L2
    imx = max(energy)
    imn = sum(energy[:silence_frames]) / silence_frames
    itl = min(0.03 * (imx - imn) + imn, 4.0 * imn)
    itu = 5.0 * itl  # @line L3
    return itl, itu, izct


def first_crossing(energy: Sequence[float], order: Sequence[int], itl: float, itu: float) -> Optional[int]:
    """The first index, in the given order, where E goes above ITL and then above ITU
    before it falls to ITL or below. None if there is no such index."""
    cand: Optional[int] = None
    for i in order:
        if energy[i] <= itl:
            cand = None
            continue
        if cand is None:
            cand = i
        if energy[i] > itu:
            return cand
    return None


def refine(zcr: Sequence[int], start: int, step: int, izct: float, span: int = 25, need: int = 3) -> int:
    """Look at the span frames before start (step = -1) or after it (step = +1). If need or
    more of them have Z > IZCT, return the one of them farthest from start; else return start."""
    hits = []
    for d in range(1, span + 1):
        j = start + step * d
        if j < 0 or j >= len(zcr):
            break
        if zcr[j] > izct:
            hits.append(j)
    return hits[-1] if len(hits) >= need else start


def endpoints_from_features(
    energy: Sequence[float], zcr: Sequence[int], silence_frames: int = 10
) -> Optional[Tuple[int, int]]:
    """(N1, N2) as frame indices, or None when no frame goes above ITU."""
    if len(energy) != len(zcr):
        raise ValueError("energy and zcr must have the same length")
    itl, itu, izct = thresholds(energy, zcr, silence_frames)
    n = len(energy)
    n1 = first_crossing(energy, range(n), itl, itu)  # @line L4
    if n1 is None:
        return None
    n2 = first_crossing(energy, range(n - 1, -1, -1), itl, itu)  # @line L5
    n1 = refine(zcr, n1, -1, izct)  # @line L6
    n2 = refine(zcr, n2, +1, izct)  # @line L7
    return n1, n2  # @line L8


def detect_endpoints(x: Sequence[float], fs: float = 16000.0) -> Optional[Tuple[int, int]]:
    """The word boundaries (N1, N2) as frame indices of 10 ms, or None if no word is found."""
    energy, zcr = features(x, fs)  # @line L1
    return endpoints_from_features(energy, zcr)
