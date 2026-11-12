# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/predictive-coding/. The authors are listed in prov/5989T7.jsonl.

"""Predictive coding: the general template and the predictors used by
standard lossless and lossy coders.

predictive_encode(x, predict, step) is closed-loop prediction (DPCM). The
predictor sees only the reconstructed samples, which the decoder also has.
With step = 1 the quantizer is the identity and the code is lossless. With
step > 1 each reconstructed sample is within step / 2 of the input.
open_loop_encode predicts from the input samples instead; its decoder output
drifts away from the input when step > 1.

Predictors for 1-D signals: fixed_predictor(k), the polynomial predictors of
orders 0 to 4 of FLAC (RFC 9639), which send the first k samples verbatim.

Predictors for images, from the left neighbour a, the upper neighbour b and
the upper-left neighbour c:
- jpeg_lossless_encode / _decode: the seven predictors of lossless JPEG
  (ITU-T T.81, Annex H, Table H.1) with its boundary rules and residuals
  modulo 2^16. Restart intervals and the point transform are not handled.
- med: the median edge detector of LOCO-I and JPEG-LS. med_residuals uses it
  with samples outside the image taken as 0, which is not the exact
  boundary rule of JPEG-LS.
- paeth: the Paeth predictor of PNG filter type 4.
"""

from collections.abc import Callable, Sequence

Predictor = Callable[[list[int]], int]


def quantize(d: int, step: int) -> int:
    """Index of the nearest multiple of step to d (ties away from 0)."""
    if step == 1:
        return d
    q = (abs(d) + step // 2) // step
    return q if d >= 0 else -q


def predictive_encode(x: Sequence[int], predict: Predictor, step: int = 1) -> list[int]:
    """Closed-loop predictive coding. Returns the quantized residuals."""
    recon: list[int] = []
    out: list[int] = []
    for t in range(len(x)):  # @line L1
        p = predict(recon)  # @line L2
        q = quantize(x[t] - p, step)  # @line L3
        recon.append(p + q * step)  # @line L4
        out.append(q)  # @line L5
    return out  # @line L6


def predictive_decode(e: Sequence[int], predict: Predictor, step: int = 1) -> list[int]:
    recon: list[int] = []
    for q in e:
        recon.append(predict(recon) + q * step)
    return recon


def open_loop_encode(x: Sequence[int], predict: Predictor, step: int) -> list[int]:
    """Prediction from the input samples, which the decoder does not have."""
    past: list[int] = []
    out: list[int] = []
    for v in x:
        out.append(quantize(v - predict(past), step))
        past.append(v)
    return out


_FIXED = [[], [1], [2, -1], [3, -3, 1], [4, -6, 4, -1]]


def fixed_predictor(order: int) -> Predictor:
    """FLAC fixed predictor of the given order (0 to 4)."""
    coef = _FIXED[order]

    def predict(h: list[int]) -> int:
        if len(h) < order:  # warm-up samples are sent as they are
            return 0
        return sum(c * h[-1 - i] for i, c in enumerate(coef))

    return predict


def previous_sample(h: list[int]) -> int:
    return h[-1] if h else 0


# Lossless JPEG (T.81 Annex H)

def t81_predict(sel: int, a: int, b: int, c: int) -> int:
    if sel == 1:
        return a
    if sel == 2:
        return b
    if sel == 3:
        return c
    if sel == 4:
        return a + b - c
    if sel == 5:
        return a + ((b - c) >> 1)
    if sel == 6:
        return b + ((a - c) >> 1)
    if sel == 7:
        return (a + b) >> 1
    raise ValueError("selection value must be 1 to 7")


def _t81_px(img: list[list[int]], i: int, j: int, sel: int, precision: int) -> int:
    if i == 0 and j == 0:
        return 1 << (precision - 1)
    if i == 0:
        return img[0][j - 1]
    if j == 0:
        return img[i - 1][0]
    return t81_predict(sel, img[i][j - 1], img[i - 1][j], img[i - 1][j - 1])


def jpeg_lossless_encode(img: Sequence[Sequence[int]], sel: int, precision: int = 8) -> list[list[int]]:
    """Residuals (x - Px) mod 2^16 in raster order, one list per row."""
    rows = [list(r) for r in img]
    return [
        [(rows[i][j] - _t81_px(rows, i, j, sel, precision)) % 65536 for j in range(len(rows[i]))]
        for i in range(len(rows))
    ]


def jpeg_lossless_decode(res: Sequence[Sequence[int]], sel: int, precision: int = 8) -> list[list[int]]:
    out: list[list[int]] = []
    for i, r in enumerate(res):
        out.append([])
        for j, d in enumerate(r):
            out[i].append((_t81_px(out, i, j, sel, precision) + d) % 65536)
    return out


# LOCO-I / JPEG-LS and PNG

def med(a: int, b: int, c: int) -> int:
    """Median edge detector."""
    if c >= max(a, b):
        return min(a, b)
    if c <= min(a, b):
        return max(a, b)
    return a + b - c


def paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def _neighbours(img: list[list[int]], i: int, j: int) -> tuple[int, int, int]:
    a = img[i][j - 1] if j > 0 else 0
    b = img[i - 1][j] if i > 0 else 0
    c = img[i - 1][j - 1] if i > 0 and j > 0 else 0
    return a, b, c


def image_residuals(img: Sequence[Sequence[int]], pred: Callable[[int, int, int], int]) -> list[list[int]]:
    """Signed residuals x - pred(a, b, c), with outside samples taken as 0."""
    rows = [list(r) for r in img]
    return [[rows[i][j] - pred(*_neighbours(rows, i, j)) for j in range(len(rows[i]))] for i in range(len(rows))]


def image_from_residuals(res: Sequence[Sequence[int]], pred: Callable[[int, int, int], int]) -> list[list[int]]:
    out: list[list[int]] = []
    for i, r in enumerate(res):
        out.append([])
        for j, d in enumerate(r):
            out[i].append(pred(*_neighbours(out, i, j)) + d)
    return out


def med_residuals(img: Sequence[Sequence[int]]) -> list[list[int]]:
    return image_residuals(img, med)
