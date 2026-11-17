# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bounding-box-regression/. The authors are listed in prov/TRRBN0.jsonl.
"""Bounding box regression: the offset encoding of R-CNN and its inverse.

A box is (x1, y1, x2, y2) in continuous image coordinates with x1 < x2 and
y1 < y2, so its width is x2 - x1. The reference box a (an anchor or a
proposal) and the target box g give the four targets

    t_x = (x - x_a) / w_a,  t_y = (y - y_a) / h_a,
    t_w = log(w / w_a),     t_h = log(h / h_a),

where (x, y) is the center and (w, h) the size. decode is the inverse map.
The optional weights (w_x, w_y, w_w, w_h) multiply the targets, as in
Detectron and torchvision (10, 10, 5, 5 for the second stage). The flag
inclusive=True uses the old PASCAL VOC rule w = x2 - x1 + 1 of the
py-faster-rcnn code. Standard library only.
"""

import math
from fractions import Fraction

# torchvision and Detectron2 clip t_w and t_h at log(1000 / 16) before exp.
DEFAULT_CLIP = math.log(1000.0 / 16)


def center_form(box, inclusive=False):
    """Return (x, y, w, h): the center and the size of a corner box."""
    one = 1 if inclusive else 0
    w = box[2] - box[0] + one
    h = box[3] - box[1] + one
    if isinstance(w, int) and isinstance(h, int):
        return (box[0] + Fraction(w, 2), box[1] + Fraction(h, 2), w, h)
    return (box[0] + w / 2, box[1] + h / 2, w, h)


def encode_shift(a, g, inclusive=False):
    """The two center targets (t_x, t_y), exact on integer boxes."""
    xa, ya, wa, ha = center_form(a, inclusive)
    x, y, _, _ = center_form(g, inclusive)
    return ((x - xa) / wa, (y - ya) / ha)


def encode(a, g, weights=(1.0, 1.0, 1.0, 1.0), inclusive=False):
    """Targets t = (t_x, t_y, t_w, t_h) of the box g with respect to the box a."""
    xa, ya, wa, ha = center_form(a, inclusive)  # @line L1
    x, y, w, h = center_form(g, inclusive)  # @line L2
    if wa <= 0 or ha <= 0 or w <= 0 or h <= 0:
        raise ValueError("boxes need a positive width and height")
    return (weights[0] * float(x - xa) / float(wa),  # @line L3
            weights[1] * float(y - ya) / float(ha),
            weights[2] * math.log(float(w) / float(wa)),
            weights[3] * math.log(float(h) / float(ha)))


def decode(a, t, weights=(1.0, 1.0, 1.0, 1.0), clip=None, inclusive=False):
    """The box that the targets t give from the box a; clip caps t_w and t_h."""
    xa, ya, wa, ha = (float(v) for v in center_form(a, inclusive))  # @line L4
    tx, ty, tw, th = (t[i] / weights[i] for i in range(4))
    if clip is not None:
        tw, th = min(tw, clip), min(th, clip)
    x, y = xa + tx * wa, ya + ty * ha  # @line L5
    w, h = wa * math.exp(tw), ha * math.exp(th)  # @line L6
    one = 1.0 if inclusive else 0.0
    return (x - w / 2, y - h / 2, x + w / 2 - one, y + h / 2 - one)  # @line L7


def smooth_l1(x, beta=1.0):
    """Smooth L1 of Fast R-CNN: 0.5 x^2 / beta for |x| < beta, else |x| - 0.5 beta."""
    ax = abs(x)
    return 0.5 * x * x / beta if ax < beta else ax - 0.5 * beta


def smooth_l1_grad(x, beta=1.0):
    """Derivative of smooth_l1: x / beta inside, sign(x) outside; it is continuous."""
    if abs(x) < beta:
        return x / beta
    return 1.0 if x > 0 else -1.0


def box_loss(t_pred, t_true, beta=1.0):
    """The sum of smooth L1 over the four coordinates."""
    return sum(smooth_l1(p - q, beta) for p, q in zip(t_pred, t_true))


def area(b):
    return (b[2] - b[0]) * (b[3] - b[1])


def iou(a, b):
    """IoU of two boxes; a Fraction on integer boxes."""
    iw = min(a[2], b[2]) - max(a[0], b[0])
    ih = min(a[3], b[3]) - max(a[1], b[1])
    inter = iw * ih if iw > 0 and ih > 0 else 0
    union = area(a) + area(b) - inter
    if isinstance(inter, int) and isinstance(union, int):
        return Fraction(inter, union)
    return inter / union


def giou(a, b):
    """Generalized IoU of Rezatofighi et al.: IoU minus the empty share of the enclosing box."""
    c = (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))
    iw = min(a[2], b[2]) - max(a[0], b[0])
    ih = min(a[3], b[3]) - max(a[1], b[1])
    inter = iw * ih if iw > 0 and ih > 0 else 0
    union = area(a) + area(b) - inter
    ac = area(c)
    if all(isinstance(v, int) for v in (inter, union, ac)):
        return Fraction(inter, union) - Fraction(ac - union, ac)
    return inter / union - (ac - union) / ac


def solve(m, rhs):
    """Solve m x = rhs by Gaussian elimination with partial pivoting."""
    n = len(m)
    a = [list(map(float, row)) + [float(r)] for row, r in zip(m, rhs)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(a[r][c]))
        if abs(a[p][c]) < 1e-300:
            raise ValueError("singular system")
        a[c], a[p] = a[p], a[c]
        for r in range(c + 1, n):
            f = a[r][c] / a[c][c]
            for k in range(c, n + 1):
                a[r][k] -= f * a[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (a[r][n] - sum(a[r][k] * x[k] for k in range(r + 1, n))) / a[r][r]
    return x


def fit_ridge(features, targets, lam):
    """R-CNN regressor for one coordinate: argmin_w sum (t_i - w . phi_i)^2 + lam ||w||^2."""
    d = len(features[0])
    gram = [[sum(f[i] * f[j] for f in features) + (lam if i == j else 0.0) for j in range(d)]
            for i in range(d)]  # @line L8
    rhs = [sum(f[i] * t for f, t in zip(features, targets)) for i in range(d)]
    return solve(gram, rhs)
