# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brief-descriptor/. The authors are listed in prov/BQH47W.jsonl.

"""BRIEF: binary robust independent elementary features.

An image is a list of H rows of W integers; pixel (u, v) is img[v][u], with u
the column (to the right) and v the row (down).

The patch is smoothed with the separable 9 x 9 binomial kernel
(1, 8, 28, 56, 70, 56, 28, 8, 1). This is the distribution of a sum of 8 fair
coin flips, so its variance is 2 in each direction, the value that Calonder et
al. use for the Gaussian. The weights are integers and the code does not
divide by 256 * 256, so the smoothed image is an exact integer image and every
comparison is exact.

The tests follow the sampling G II of the paper: both points of a pair are
i.i.d. Gaussian with variance S^2 / 25 around the keypoint, here rounded to the
nearest pixel and clamped to the patch [-S/2, S/2]^2. Bit i - 1 of the
descriptor is 1 when J(k + x_i) < J(k + y_i). A descriptor is a Python int
with n_d bits, which is n_d / 64 words of 64 bits.
"""

import random
from typing import List, Optional, Sequence, Tuple

Image = Sequence[Sequence[int]]
Pair = Tuple[Tuple[int, int], Tuple[int, int]]

BINOMIAL9 = (1, 8, 28, 56, 70, 56, 28, 8, 1)
M1 = 0x5555555555555555
M2 = 0x3333333333333333
M4 = 0x0F0F0F0F0F0F0F0F
H01 = 0x0101010101010101
MASK64 = (1 << 64) - 1


def smooth(img: Image) -> List[List[int]]:
    """Separable binomial smoothing with replicated borders, integer output."""
    h, w = len(img), len(img[0])
    tmp = [[0] * w for _ in range(h)]
    for v in range(h):
        row = img[v]
        for u in range(w):
            s = 0
            for k, wt in enumerate(BINOMIAL9):
                uu = min(max(u + k - 4, 0), w - 1)
                s += wt * row[uu]
            tmp[v][u] = s
    out = [[0] * w for _ in range(h)]
    for v in range(h):
        for u in range(w):
            s = 0
            for k, wt in enumerate(BINOMIAL9):
                vv = min(max(v + k - 4, 0), h - 1)
                s += wt * tmp[vv][u]
            out[v][u] = s
    return out


def sample_pairs(n_d: int = 256, patch: int = 32, seed: int = 0) -> List[Pair]:
    """n_d test pairs by the G II sampling, clamped to the patch."""
    rng = random.Random(seed)
    half = patch // 2
    sigma = patch / 5.0

    def coord() -> int:
        return max(-half, min(half, int(round(rng.gauss(0.0, sigma)))))

    return [((coord(), coord()), (coord(), coord())) for _ in range(n_d)]


def describe(smoothed: Sequence[Sequence[int]], u: int, v: int, pairs: Sequence[Pair]) -> int:
    """The descriptor of the keypoint (u, v) as an int of len(pairs) bits."""
    d = 0  # @line L4
    for i, ((xu, xv), (yu, yv)) in enumerate(pairs):  # @line L5
        if smoothed[v + xv][u + xu] < smoothed[v + yv][u + yu]:  # @line L6
            d |= 1 << i
    return d  # @line L7


def brief(img: Image, keypoints: Sequence[Tuple[int, int]], n_d: int = 256, patch: int = 32,
          seed: int = 0, pairs: Optional[Sequence[Pair]] = None) -> List[Optional[int]]:
    """BRIEF descriptors of the keypoints; None for a keypoint too close to the border."""
    j = smooth(img)  # @line L1
    if pairs is None:
        pairs = sample_pairs(n_d, patch, seed)  # @line L2
    h, w = len(img), len(img[0])
    half = patch // 2
    out: List[Optional[int]] = []
    for u, v in keypoints:  # @line L3
        if half <= u < w - half and half <= v < h - half:
            out.append(describe(j, u, v, pairs))
        else:
            out.append(None)
    return out


def popcount64(x: int) -> int:
    """SWAR popcount of a 64-bit word."""
    x = x - ((x >> 1) & M1)
    x = (x & M2) + ((x >> 2) & M2)
    x = (x + (x >> 4)) & M4
    return ((x * H01) & MASK64) >> 56


def hamming(a: int, b: int, n_d: int = 256) -> int:
    """Hamming distance of two n_d-bit descriptors, one 64-bit word at a time."""
    x = a ^ b  # @line L8
    total = 0
    for k in range(0, n_d, 64):
        total += popcount64((x >> k) & MASK64)
    return total


def match(desc1: Sequence[int], desc2: Sequence[int], n_d: int = 256) -> List[Tuple[int, int]]:
    """For each descriptor of the first list: (index of the nearest in the second, distance)."""
    out = []
    for a in desc1:
        best, best_j = n_d + 1, -1
        for j, b in enumerate(desc2):
            d = hamming(a, b, n_d)
            if d < best:
                best, best_j = d, j
        out.append((best_j, best))
    return out
