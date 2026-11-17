# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-r-cnn/. The authors are listed in prov/CTWF7A.jsonl.
"""Fast R-CNN around a given network.

The convolutional layers and the head are not part of this file. The caller
passes the feature map of the image (a list of channels, each a list of rows)
and `head`, a function from the pooled features of one RoI to the class
logits (K + 1 numbers, class 0 is background) and the box offsets (K lists of
4 numbers). The tests build both by hand. This file has the parts that are
not learned: RoI max pooling with its backward pass, the softmax, the
class-specific decoding, NMS for each class, the sampling of RoIs for a
mini-batch, and the multi-task loss with the smooth L1 term.

Boxes are (x1, y1, x2, y2) in image pixels; `scale` maps image pixels to
feature cells (1/16 for VGG16). Standard library only.
"""

import math
from fractions import Fraction


def area(b):
    return max(0, b[2] - b[0]) * max(0, b[3] - b[1])


def iou(a, b):
    """Intersection over union; exact Fractions on integer boxes."""
    iw = min(a[2], b[2]) - max(a[0], b[0])
    ih = min(a[3], b[3]) - max(a[1], b[1])
    if iw <= 0 or ih <= 0:
        return 0
    inter = iw * ih
    union = area(a) + area(b) - inter
    if isinstance(inter, int) and isinstance(union, int):
        return Fraction(inter, union)
    return inter / union


def _round(x):
    return int(x + 0.5) if x >= 0 else -int(-x + 0.5)


def roi_pool(feat, box, scale, out_h, out_w):
    """Max pool the cells under the box into out_h x out_w bins (the Caffe rounding).
    Returns (Y, S) with S the argmax cell of each bin, or None for an empty bin (value 0)."""
    fh, fw = len(feat[0]), len(feat[0][0])
    c1, r1 = _round(box[0] * scale), _round(box[1] * scale)
    c2, r2 = _round(box[2] * scale), _round(box[3] * scale)
    h, w = max(r2 - r1 + 1, 1), max(c2 - c1 + 1, 1)
    ys, ss = [], []
    for ch in feat:
        y = [[0.0] * out_w for _ in range(out_h)]
        s = [[None] * out_w for _ in range(out_h)]
        for p in range(out_h):
            rs = min(max(r1 + p * h // out_h, 0), fh)
            re = min(max(r1 - (-(p + 1) * h // out_h), 0), fh)
            for q in range(out_w):
                cs = min(max(c1 + q * w // out_w, 0), fw)
                ce = min(max(c1 - (-(q + 1) * w // out_w), 0), fw)
                for r in range(rs, re):
                    for c in range(cs, ce):
                        if s[p][q] is None or ch[r][c] > y[p][q]:
                            y[p][q], s[p][q] = ch[r][c], (r, c)
        ys.append(y)
        ss.append(s)
    return ys, ss


def roi_pool_backward(dy, switches, fh, fw):
    """Each bin sends its gradient to its argmax cell; gradients of several bins add up."""
    out = []
    for dyc, sc in zip(dy, switches):
        g = [[0.0] * fw for _ in range(fh)]
        for p, row in enumerate(sc):
            for q, arg in enumerate(row):
                if arg is not None:
                    g[arg[0]][arg[1]] += dyc[p][q]
        out.append(g)
    return out


def softmax(z):
    m = max(z)
    e = [math.exp(v - m) for v in z]
    s = sum(e)
    return [v / s for v in e]


def decode(r, t, mean=(0.0, 0.0, 0.0, 0.0), std=(1.0, 1.0, 1.0, 1.0)):
    """Undo the target normalization, then apply the offsets to the RoI r."""
    d = [ti * si + mi for ti, si, mi in zip(t, std, mean)]
    w, h = r[2] - r[0], r[3] - r[1]
    x, y = r[0] + w / 2, r[1] + h / 2
    gx, gy, gw, gh = x + w * d[0], y + h * d[1], w * math.exp(d[2]), h * math.exp(d[3])
    return (gx - gw / 2, gy - gh / 2, gx + gw / 2, gy + gh / 2)


def encode(r, g, mean=(0.0, 0.0, 0.0, 0.0), std=(1.0, 1.0, 1.0, 1.0)):
    w, h = r[2] - r[0], r[3] - r[1]
    gw, gh = g[2] - g[0], g[3] - g[1]
    d = ((g[0] + g[2] - r[0] - r[2]) / 2 / w, (g[1] + g[3] - r[1] - r[3]) / 2 / h,
         math.log(gw / w), math.log(gh / h))
    return tuple((di - mi) / si for di, mi, si in zip(d, mean, std))


def greedy_nms(boxes, scores, thr):
    order = sorted(range(len(boxes)), key=lambda i: (-scores[i], i))
    keep = []
    for i in order:
        if all(iou(boxes[i], boxes[k]) <= thr for k in keep):
            keep.append(i)
    return keep


def detect(feat, rois, scale, head, out_h=7, out_w=7, nms_thr=0.3, score_thr=0.0,
           mean=(0.0, 0.0, 0.0, 0.0), std=(1.0, 1.0, 1.0, 1.0)):
    """Fast R-CNN test time on a given feature map. Returns {class: [(score, box, roi index)]}."""
    # feat is the output of the convolutional layers, given by the caller.
    probs, offs = [], []  # @line L1
    for r in rois:  # @line L2
        pooled, _ = roi_pool(feat, r, scale, out_h, out_w)  # @line L3
        logits, t = head(pooled)  # @line L4
        probs.append(softmax(logits))
        offs.append(t)
    out = {}
    for k in range(1, len(probs[0]) if probs else 1):  # @line L5
        cand = [i for i in range(len(rois)) if probs[i][k] > score_thr]
        boxes = [decode(rois[i], offs[i][k - 1], mean, std) for i in cand]  # @line L6
        scores = [probs[i][k] for i in cand]
        keep = greedy_nms(boxes, scores, nms_thr)  # @line L7
        out[k] = [(scores[j], boxes[j], cand[j]) for j in keep]
    return out  # @line L8


def sample_rois(rois, gts, gt_classes, batch, rng, fg_fraction=0.25, fg_thr=0.5, bg_lo=0.1,
                bg_hi=0.5):
    """Pick a mini-batch of RoIs from one image: foreground (IoU >= fg_thr with its best
    truth) up to fg_fraction of the batch, the rest background (IoU in [bg_lo, bg_hi)).
    Returns a list of (roi index, class, truth index or None)."""
    fg, bg = [], []
    for i, r in enumerate(rois):
        best, j = 0, None
        for k, g in enumerate(gts):
            o = iou(r, g)
            if o > best:
                best, j = o, k
        if best >= fg_thr:
            fg.append((i, gt_classes[j], j))
        elif bg_lo <= best < bg_hi:
            bg.append((i, 0, None))
    n_fg = min(len(fg), int(round(fg_fraction * batch)))
    fg = rng.sample(fg, n_fg)
    bg = rng.sample(bg, min(len(bg), batch - n_fg))
    return fg + bg


def smooth_l1(x):
    a = abs(x)
    return 0.5 * x * x if a < 1 else a - 0.5


def smooth_l1_grad(x):
    return x if abs(x) < 1 else (1.0 if x > 0 else -1.0)


def multitask_loss(p, u, t_u, v, lam=1.0):
    """L = -log p_u + lam [u >= 1] sum_i smooth_L1(t_u[i] - v[i]) for one RoI."""
    loss = -math.log(p[u])
    if u >= 1:
        loss += lam * sum(smooth_l1(a - b) for a, b in zip(t_u, v))
    return loss
