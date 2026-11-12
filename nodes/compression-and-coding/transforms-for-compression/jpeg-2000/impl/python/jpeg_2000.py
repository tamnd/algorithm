# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jpeg-2000/. The authors are listed in prov/APJT1C.jsonl.

"""The transform and quantization stages of JPEG 2000 Part 1 (ITU-T T.800,
ISO/IEC 15444-1): DC level shift, the reversible colour transform (RCT),
tiling, the reversible 5/3 and irreversible 9/7 discrete wavelet transforms
by lifting with whole-sample symmetric extension, the multilevel 2D
decomposition, and the dead-zone scalar quantizer.

Not implemented: the irreversible colour transform, EBCOT tier 1 (code
blocks, the three coding passes and the MQ coder), rate control (PCRD),
tier 2 (packets and layers) and the codestream. Signals and tiles must
start at an even coordinate, which holds for an image at the origin of
the canvas cut into tiles of even size.

Each 1D transform of n samples costs O(n); the 2D transform of an
H x W tile with any number of levels costs O(HW).
"""

import math
from typing import List, Sequence, Tuple

Matrix = List[List[float]]

# Table F.4 of T.800: the lifting parameters of the 9/7 filter.
ALPHA = -1.586134342059924
BETA = -0.052980118572961
GAMMA = 0.882911075530934
DELTA = 0.443506852043971
KAPPA = 1.230174104914001


def _mirror(i: int, n: int) -> int:
    """Whole-sample symmetric extension of the index i into 0 .. n-1 (n >= 2)."""
    period = 2 * (n - 1)
    i %= period
    return period - i if i >= n else i


def lift53_forward(x: Sequence[int]) -> Tuple[List[int], List[int]]:
    """Reversible 5/3 analysis of integers: returns (low, high).

    low has ceil(n/2) samples and high floor(n/2). A signal of length 1
    is returned unchanged as the low band.
    """
    n = len(x)
    if n == 1:
        return [x[0]], []
    y = list(x)
    for i in range(1, n, 2):  # @line L7
        y[i] = x[i] - (x[_mirror(i - 1, n)] + x[_mirror(i + 1, n)]) // 2  # predict: odd from even
    for i in range(0, n, 2):  # @line L8
        y[i] = x[i] + (y[_mirror(i - 1, n)] + y[_mirror(i + 1, n)] + 2) // 4  # update: even from odd
    return y[0::2], y[1::2]  # @line L9


def lift53_inverse(low: Sequence[int], high: Sequence[int]) -> List[int]:
    """Inverse of lift53_forward: the same two steps, undone in reverse order."""
    n = len(low) + len(high)
    if n == 1:
        return [low[0]]
    y = [0] * n
    y[0::2] = low
    y[1::2] = high
    x = list(y)
    for i in range(0, n, 2):
        x[i] = y[i] - (y[_mirror(i - 1, n)] + y[_mirror(i + 1, n)] + 2) // 4
    for i in range(1, n, 2):
        x[i] = y[i] + (x[_mirror(i - 1, n)] + x[_mirror(i + 1, n)]) // 2
    return x


def lift97_forward(x: Sequence[float]) -> Tuple[List[float], List[float]]:
    """Irreversible 9/7 analysis by four lifting steps and scaling (Table F.4).

    The low band is divided by K and the high band multiplied by K, so the
    low-pass filter has gain 1 at frequency 0 and the high-pass filter has
    gain 2 at the Nyquist frequency.
    """
    n = len(x)
    if n == 1:
        return [float(x[0])], []
    y = [float(v) for v in x]
    for coef, start in ((ALPHA, 1), (BETA, 0), (GAMMA, 1), (DELTA, 0)):
        prev = list(y)
        for i in range(start, n, 2):
            y[i] = prev[i] + coef * (prev[_mirror(i - 1, n)] + prev[_mirror(i + 1, n)])
    return [v / KAPPA for v in y[0::2]], [v * KAPPA for v in y[1::2]]


def lift97_inverse(low: Sequence[float], high: Sequence[float]) -> List[float]:
    """Inverse of lift97_forward."""
    n = len(low) + len(high)
    if n == 1:
        return [float(low[0])]
    y = [0.0] * n
    y[0::2] = [v * KAPPA for v in low]
    y[1::2] = [v / KAPPA for v in high]
    for coef, start in ((DELTA, 0), (GAMMA, 1), (BETA, 0), (ALPHA, 1)):
        prev = list(y)
        for i in range(start, n, 2):
            y[i] = prev[i] - coef * (prev[_mirror(i - 1, n)] + prev[_mirror(i + 1, n)])
    return y


def _columns(a: Matrix) -> Matrix:
    return [list(c) for c in zip(*a)]


def dwt2_forward(tile: Matrix, levels: int, reversible: bool = True) -> Matrix:
    """Multilevel 2D DWT in place in the Mallat layout.

    At each level the current LL region is filtered along the columns
    (vertical) and then along the rows (horizontal); the low halves go to
    the top and to the left. The final LL band is the top-left corner.
    """
    fwd = lift53_forward if reversible else lift97_forward
    a = [list(r) for r in tile]
    h, w = len(a), len(a[0])
    for _ in range(levels):  # @line L4
        if h < 1 or w < 1:
            break
        for c in range(w):  # vertical: every column of the LL region
            lo, hi = fwd([a[r][c] for r in range(h)])
            for r, v in enumerate(lo + hi):
                a[r][c] = v
        for r in range(h):  # horizontal: every row of the LL region
            lo, hi = fwd(a[r][:w])
            a[r][:w] = lo + hi
        h, w = (h + 1) // 2, (w + 1) // 2
    return a


def dwt2_inverse(coeffs: Matrix, levels: int, reversible: bool = True) -> Matrix:
    """Inverse of dwt2_forward: undo the levels from the coarsest one."""
    inv = lift53_inverse if reversible else lift97_inverse
    a = [list(r) for r in coeffs]
    sizes = []
    h, w = len(a), len(a[0])
    for _ in range(levels):
        if h < 1 or w < 1:
            break
        sizes.append((h, w))
        h, w = (h + 1) // 2, (w + 1) // 2
    for h, w in reversed(sizes):
        hl, wl = (h + 1) // 2, (w + 1) // 2
        for r in range(h):
            a[r][:w] = inv(a[r][:wl], a[r][wl:w])
        for c in range(w):
            col = inv([a[r][c] for r in range(hl)], [a[r][c] for r in range(hl, h)])
            for r in range(h):
                a[r][c] = col[r]
    return a


def subbands(h: int, w: int, levels: int) -> List[Tuple[str, int, int, int, int]]:
    """The subbands of the Mallat layout as (name, row0, col0, rows, cols).

    Names follow T.800: HL is high horizontally and low vertically, LH the
    reverse. The list starts with the final LL band.
    """
    out = []
    for lev in range(1, levels + 1):
        hl, wl = (h + 1) // 2, (w + 1) // 2
        out.append((f"HL{lev}", 0, wl, hl, w - wl))
        out.append((f"LH{lev}", hl, 0, h - hl, wl))
        out.append((f"HH{lev}", hl, wl, h - hl, w - wl))
        h, w = hl, wl
    out.append((f"LL{levels}", 0, 0, h, w))
    return out[::-1]


def dc_shift(samples: Matrix, bits: int) -> Matrix:
    """DC level shift of unsigned samples: subtract 2^(bits-1)."""
    return [[v - (1 << (bits - 1)) for v in row] for row in samples]  # @line L1


def rct_forward(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """Reversible colour transform: (Y, U, V) = (floor((R+2G+B)/4), B-G, R-G)."""
    return (r + 2 * g + b) // 4, b - g, r - g  # @line L2


def rct_inverse(y: int, u: int, v: int) -> Tuple[int, int, int]:
    """Inverse RCT: G = Y - floor((U+V)/4), R = V + G, B = U + G."""
    g = y - (u + v) // 4
    return v + g, g, u + g


def tiles(image: Matrix, size: int) -> List[Tuple[int, int, Matrix]]:
    """Cut an image into tiles of size x size (smaller at the right and bottom)."""
    out = []
    for r0 in range(0, len(image), size):  # @line L3
        for c0 in range(0, len(image[0]), size):
            out.append((r0, c0, [row[c0:c0 + size] for row in image[r0:r0 + size]]))
    return out


def untile(parts: Sequence[Tuple[int, int, Matrix]], h: int, w: int) -> Matrix:
    """Inverse of tiles."""
    image = [[0] * w for _ in range(h)]
    for r0, c0, t in parts:
        for i, row in enumerate(t):
            image[r0 + i][c0:c0 + len(row)] = row
    return image


def step_size(exponent: int, mantissa: int, nominal_range: int) -> float:
    """Quantizer step of a subband (Annex E): 2^(R_b - e_b) (1 + mu_b / 2^11)."""
    return 2.0 ** (nominal_range - exponent) * (1 + mantissa / 2048)


def quantize(y: float, step: float) -> int:
    """Dead-zone quantizer: q = sign(y) floor(|y| / step)."""
    q = int(math.floor(abs(y) / step))  # @line L5
    return -q if y < 0 else q


def dequantize(q: int, step: float, r: float = 0.5) -> float:
    """Reconstruction (|q| + r) step with the sign of q, and 0 for q = 0."""
    if q == 0:
        return 0.0
    return math.copysign((abs(q) + r) * step, q)


def encode_reversible(rgb: Sequence[Matrix], bits: int, levels: int, tile_size: int) -> List[List[Tuple[int, int, Matrix]]]:
    """The lossless path up to tier 1: shift, RCT, tiles and the 5/3 DWT.

    rgb holds three H x W matrices of unsigned integers with `bits` bits.
    Returns, for each of Y, U and V, the list of (row0, col0, coefficients)
    of its tiles. With the reversible path the step is 1, so the integer
    coefficients are the quantization indices that tier 1 would code.
    """
    shifted = [dc_shift(c, bits) for c in rgb]
    h, w = len(rgb[0]), len(rgb[0][0])
    comps: List[Matrix] = [[[0] * w for _ in range(h)] for _ in range(3)]
    for i in range(h):
        for j in range(w):
            y, u, v = rct_forward(shifted[0][i][j], shifted[1][i][j], shifted[2][i][j])
            comps[0][i][j], comps[1][i][j], comps[2][i][j] = y, u, v
    out = []
    for c in comps:
        parts = []
        for r0, c0, t in tiles(c, tile_size):
            coeffs = dwt2_forward(t, levels)
            parts.append((r0, c0, [[quantize(v, 1.0) for v in row] for row in coeffs]))  # step 1: no loss
        out.append(parts)
    return out  # @line L6


def decode_reversible(coded: Sequence[List[Tuple[int, int, Matrix]]], bits: int, levels: int, h: int, w: int) -> List[Matrix]:
    """Inverse of encode_reversible."""
    comps = [untile([(r0, c0, dwt2_inverse(t, levels)) for r0, c0, t in parts], h, w) for parts in coded]
    out: List[Matrix] = [[[0] * w for _ in range(h)] for _ in range(3)]
    half = 1 << (bits - 1)
    for i in range(h):
        for j in range(w):
            r, g, b = rct_inverse(comps[0][i][j], comps[1][i][j], comps[2][i][j])
            out[0][i][j], out[1][i][j], out[2][i][j] = r + half, g + half, b + half
    return out
