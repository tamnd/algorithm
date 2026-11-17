# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mask-r-cnn/. The authors are listed in prov/24WQPY.jsonl.

"""The non-learned parts of Mask R-CNN: RoIAlign sampling, mask pasting and the mask loss.

Coordinates follow one convention: the center of cell (u, v) of a grid is the
point (u, v), and grid values are g[v][u]. A box is (x1, y1, x2, y2) in
continuous coordinates. For a feature map of stride s, image coordinate x
maps to feature coordinate (x + 0.5) / s - 0.5 (see image_to_feature).
The network that makes the feature map and the mask logits is not here.
"""

import math


def bilinear(g, x, y, zero_outside=True):
    """Bilinear interpolation of grid g at (x, y).

    With zero_outside, a point with x < -1, x > W, y < -1 or y > H gives 0, as in
    the Detectron code. Other points are clamped to [0, W - 1] x [0, H - 1].
    """
    h, w = len(g), len(g[0])
    if zero_outside and (x < -1.0 or x > w or y < -1.0 or y > h):
        return 0.0
    x = min(max(x, 0.0), w - 1.0)
    y = min(max(y, 0.0), h - 1.0)
    x0, y0 = int(math.floor(x)), int(math.floor(y))
    x1, y1 = min(x0 + 1, w - 1), min(y0 + 1, h - 1)
    ax, ay = x - x0, y - y0
    top = (1 - ax) * g[y0][x0] + ax * g[y0][x1]
    bottom = (1 - ax) * g[y1][x0] + ax * g[y1][x1]
    return (1 - ay) * top + ay * bottom


def roi_align(feat, box, p, s):
    """Return the p x p output of RoIAlign on the feature map feat for box, with s x s samples per bin."""
    x1, y1, x2, y2 = box
    bw, bh = (x2 - x1) / p, (y2 - y1) / p  # @line L1
    out = [[0.0] * p for _ in range(p)]
    for r in range(p):  # @line L2
        for c in range(p):
            acc = 0.0  # @line L3
            for a in range(s):  # @line L4
                for b in range(s):
                    y = y1 + (r + (a + 0.5) / s) * bh  # @line L5
                    x = x1 + (c + (b + 0.5) / s) * bw
                    acc += bilinear(feat, x, y)  # @line L6
            out[r][c] = acc / (s * s)  # @line L7
    return out


def paste_mask(mask, box, w, h, thresh=0.5):
    """Paste an m x m mask of probabilities for box (image coordinates) into a w x h binary image."""
    m = len(mask)
    x1, y1, x2, y2 = box
    out = [[0] * w for _ in range(h)]
    for v in range(max(0, math.ceil(y1)), min(h, math.ceil(y2))):  # @line L8
        for u in range(max(0, math.ceil(x1)), min(w, math.ceil(x2))):
            mx = (u - x1) * m / (x2 - x1) - 0.5  # @line L9
            my = (v - y1) * m / (y2 - y1) - 0.5
            out[v][u] = 1 if bilinear(mask, mx, my, zero_outside=False) >= thresh else 0  # @line L10
    return out  # @line L11


def image_to_feature(box, stride):
    """Map a box from image coordinates to the coordinates of a feature map with the given stride."""
    return tuple((x + 0.5) / stride - 0.5 for x in box)


def mask_loss(logits, k, target):
    """Mean binary cross-entropy of the mask of class k against a binary target; the other K - 1 masks do not count."""
    m = len(target)
    total = 0.0
    for v in range(m):
        for u in range(m):
            z, t = logits[k][v][u], target[v][u]
            # log(1 + e^z) - t z, computed without overflow
            total += max(z, 0.0) - t * z + math.log1p(math.exp(-abs(z)))
    return total / (m * m)
