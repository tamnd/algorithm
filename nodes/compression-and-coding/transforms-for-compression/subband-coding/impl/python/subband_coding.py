# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subband-coding/. The authors are listed in prov/WGFYEV.jsonl.

"""Subband coding of a one-dimensional signal with a dyadic (octave) tree of
orthonormal two-channel Haar filter banks, bit allocation across the bands,
and a uniform midtread quantizer in each band.

The filter bank here is the simplest one with perfect reconstruction: the
orthonormal Haar pair. Any other two-channel bank can take its place in
split and merge. The analysis and synthesis of a signal of length n cost
O(n) time, and the bit allocation over K bands costs O(K log(1/eps)).
"""

import math
import random
from typing import Dict, List, Sequence, Tuple, Union

R2 = math.sqrt(2.0)


def split(x: Sequence[float]) -> Tuple[List[float], List[float]]:
    """Two-channel orthonormal Haar analysis with decimation by 2 (len(x) even)."""
    low = [(x[2 * k] + x[2 * k + 1]) / R2 for k in range(len(x) // 2)]
    high = [(x[2 * k] - x[2 * k + 1]) / R2 for k in range(len(x) // 2)]
    return low, high


def merge(low: Sequence[float], high: Sequence[float]) -> List[float]:
    """Synthesis: the inverse of split."""
    out: List[float] = []
    for a, d in zip(low, high):
        out.append((a + d) / R2)
        out.append((a - d) / R2)
    return out


def analyze(x: Sequence[float], levels: int, full: bool = False) -> List[List[float]]:
    """Split x into subbands.

    full=False: the dyadic tree. Only the low band is split again, which
    gives levels+1 bands, ordered from the lowest frequency up:
    [L_levels, H_levels, H_levels-1, ..., H_1]; band H_j has n/2^j samples.
    full=True: the full tree, every band is split, 2^levels equal bands in
    the natural (not frequency) order of the Haar packet tree.
    len(x) must be a multiple of 2^levels.
    """
    if len(x) % (1 << levels):
        raise ValueError("the length must be a multiple of 2^levels")
    if full:
        bands = [list(x)]
        for _ in range(levels):
            bands = [b for band in bands for b in split(band)]
        return bands
    low = list(x)
    highs: List[List[float]] = []
    for _ in range(levels):  # @line L7
        low, high = split(low)  # @line L8
        highs.append(high)
    return [low] + highs[::-1]  # @line L9


def synthesize(bands: Sequence[Sequence[float]], full: bool = False) -> List[float]:
    """Inverse of analyze."""
    if full:
        cur = [list(b) for b in bands]
        while len(cur) > 1:
            cur = [merge(cur[2 * i], cur[2 * i + 1]) for i in range(len(cur) // 2)]
        return cur[0]
    low = list(bands[0])
    for high in bands[1:]:
        low = merge(low, high)
    return low


def weights(bands: Sequence[Sequence[float]]) -> List[float]:
    """The fraction of the samples in each band, w_k = n_k / n."""
    n = sum(len(b) for b in bands)
    return [len(b) / n for b in bands]


def ar1_band_variances(rho: float, levels: int, full: bool = False) -> List[float]:
    """Exact variances of the bands of a unit-variance AR(1) source.

    Each band sample is the inner product of x with the synthesis vector of
    that band (a Haar function of length 2^levels); its variance is h' R h
    with R[a][b] = rho^|a-b|.
    """
    n = 1 << levels
    zero = [[0.0] * len(b) for b in analyze([0.0] * n, levels, full)]
    out = []
    for k in range(len(zero)):
        unit = [list(b) for b in zero]
        unit[k][0] = 1.0
        h = synthesize(unit, full)
        out.append(sum(h[a] * h[b] * rho ** abs(a - b) for a in range(n) for b in range(n)))
    return out


def coding_gain(variances: Sequence[float], w: Sequence[float]) -> float:
    """Weighted arithmetic over weighted geometric mean of the band variances."""
    am = sum(wk * v for wk, v in zip(w, variances))
    gm = math.exp(sum(wk * math.log(v) for wk, v in zip(w, variances)))
    return am / gm


def allocate(variances: Sequence[float], w: Sequence[float], rate: float, clip: bool = True) -> List[float]:
    """Bits per sample for each band at an average of `rate` bits per sample.

    clip=False: the Huang and Schultheiss rule b_k = rate + 1/2 lg(var_k / GM),
    which can be negative. clip=True: reverse water-filling, the optimum
    under D_k(b) = var_k 2^(-2b) with b_k >= 0: find theta with
    sum w_k max(0, 1/2 lg(var_k / theta)) = rate by bisection.
    """
    if not clip:
        lg_gm = sum(wk * math.log2(v) for wk, v in zip(w, variances))
        return [rate + 0.5 * (math.log2(v) - lg_gm) for v in variances]
    lo, hi = 1e-300, max(variances)
    for _ in range(200):  # @line L10
        mid = math.sqrt(lo * hi)  # bisection on log(theta)
        r = sum(wk * max(0.0, 0.5 * math.log2(v / mid)) for wk, v in zip(w, variances))
        lo, hi = (mid, hi) if r > rate else (lo, mid)
    theta = math.sqrt(lo * hi)
    return [max(0.0, 0.5 * math.log2(v / theta)) for v in variances]  # @line L11


def model_distortion(variances: Sequence[float], w: Sequence[float], bits: Sequence[float]) -> float:
    """Mean squared error per sample under the model D_k = var_k 2^(-2 b_k)."""
    return sum(wk * v * 2.0 ** (-2 * b) for wk, v, b in zip(w, variances, bits))


def quantize(band: Sequence[float], step: float) -> List[int]:
    """Uniform midtread quantizer: round half away from zero."""
    return [int(math.copysign(math.floor(abs(v) / step + 0.5), v)) for v in band]


def entropy(indices: Sequence[int]) -> float:
    """First-order empirical entropy in bits per index."""
    counts: Dict[int, int] = {}
    for q in indices:
        counts[q] = counts.get(q, 0) + 1
    n = len(indices)
    return -sum(c / n * math.log2(c / n) for c in counts.values())


def subband_code(x: Sequence[float], levels: int, steps: Union[float, Sequence[float]]) -> Tuple[List[float], float]:
    """Encode and decode x with the dyadic tree and a quantizer step per band.

    steps is one step for every band or a list with one step per band, in
    the order of analyze. Returns the decoded signal and the rate in bits
    per sample, measured as the first-order entropy of the indices of each
    band weighted by the band size. For an orthonormal bank, equal steps
    give equal distortion in every band, which is the high-rate optimal
    bit allocation for entropy-coded quantizers. Cost O(n).
    """
    bands = analyze(x, levels)  # @line L1
    if isinstance(steps, (int, float)):
        steps = [float(steps)] * len(bands)
    rate = 0.0
    decoded = []
    for band, step in zip(bands, steps):  # @line L2
        q = quantize(band, step)  # @line L3
        rate += len(band) * entropy(q)  # @line L4
        decoded.append([step * i for i in q])  # @line L5
    return synthesize(decoded), rate / len(x)  # @line L6


def ar1(n: int, rho: float, seed: int) -> List[float]:
    """A unit-variance Gaussian AR(1) sequence: x[t] = rho x[t-1] + sqrt(1-rho^2) e[t]."""
    rng = random.Random(seed)
    s = math.sqrt(1 - rho * rho)
    x = [rng.gauss(0, 1)]
    for _ in range(n - 1):
        x.append(rho * x[-1] + s * rng.gauss(0, 1))
    return x
