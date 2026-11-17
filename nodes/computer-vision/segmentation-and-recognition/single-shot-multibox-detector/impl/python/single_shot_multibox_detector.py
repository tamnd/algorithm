# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/single-shot-multibox-detector/. The authors are listed in prov/TNJGM1.jsonl.
"""SSD around given network outputs.

The convolutional network is not part of this file. The caller passes, for
each default box, a list of C + 1 class scores (logits, background first) and
four offsets. The tests build them by hand or with a fixed seed. This file has
the parts that are not learned: the default boxes, the matching of default
boxes to ground truth boxes, hard negative mining, the training loss, and the
test-time decoding with non-maximum suppression (NMS) for each class.

Default boxes are (cx, cy, w, h) in coordinates relative to the image, so the
image is the unit square. Corner boxes are (x1, y1, x2, y2). Standard library only.
"""

import math
from fractions import Fraction


def ssd_scales(m, s_min=0.2, s_max=0.9):
    """The scales s_1, ..., s_m spaced evenly from s_min to s_max (m >= 2)."""
    return [s_min + (s_max - s_min) * k / (m - 1) for k in range(m)]


def default_boxes(fmap_sizes, ratios, s_min=0.2, s_max=0.9, scales=None, s_last=1.0):
    """Default boxes for square feature maps of the given sizes.

    ratios[k] is the list of aspect ratios (width / height) of map k. When 1 is
    in the list, one more box of scale sqrt(s_k s_{k+1}) and ratio 1 is added,
    with s_{m+1} = s_last. The order is map, row, column, then the shapes."""
    m = len(fmap_sizes)
    s = list(scales) if scales is not None else ssd_scales(m, s_min, s_max)
    s.append(s_last)
    out = []
    for k, f in enumerate(fmap_sizes):
        shapes = [(s[k] * math.sqrt(a), s[k] / math.sqrt(a)) for a in ratios[k]]
        if 1 in ratios[k]:
            e = math.sqrt(s[k] * s[k + 1])
            shapes.append((e, e))
        for i in range(f):
            for j in range(f):
                cx, cy = (j + 0.5) / f, (i + 0.5) / f
                for w, h in shapes:
                    out.append((cx, cy, w, h))
    return out


def corners(d):
    return (d[0] - d[2] / 2, d[1] - d[3] / 2, d[0] + d[2] / 2, d[1] + d[3] / 2)


def iou(a, b):
    """Intersection over union of corner boxes; exact Fractions on integer boxes."""
    iw = min(a[2], b[2]) - max(a[0], b[0])
    ih = min(a[3], b[3]) - max(a[1], b[1])
    if iw <= 0 or ih <= 0:
        return 0
    inter = iw * ih
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    if isinstance(inter, int) and isinstance(union, int):
        return Fraction(inter, union)
    return inter / union


def encode(d, g, var=(1.0, 1.0)):
    """Offsets of corner box g from default box d = (cx, cy, w, h)."""
    gw, gh = g[2] - g[0], g[3] - g[1]
    gx, gy = (g[0] + g[2]) / 2, (g[1] + g[3]) / 2
    return ((gx - d[0]) / d[2] / var[0], (gy - d[1]) / d[3] / var[0],
            math.log(gw / d[2]) / var[1], math.log(gh / d[3]) / var[1])


def decode(d, t, var=(1.0, 1.0)):
    """The corner box given by offsets t from default box d = (cx, cy, w, h)."""
    cx, cy = d[0] + t[0] * var[0] * d[2], d[1] + t[1] * var[0] * d[3]
    w, h = d[2] * math.exp(t[2] * var[1]), d[3] * math.exp(t[3] * var[1])
    return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)


def match(boxes, gts, thr=0.5):
    """The SSD matching. boxes are corner boxes. Returns, for each box, the index
    of its ground truth box or -1 for a negative.

    Step 1 (bipartite): repeatedly take the pair (box, truth) of largest positive
    IoU among the boxes and truths not matched yet, and match it, so each truth
    gets its own box. Step 2: every other box whose best IoU is above thr is
    matched to a truth of largest IoU. Ties go to the lower index."""
    res = [-1] * len(boxes)
    if not gts:
        return res
    ious = [[iou(b, g) for g in gts] for b in boxes]
    free_b, free_g = set(range(len(boxes))), set(range(len(gts)))
    while free_g and free_b:
        best, bi, gj = 0, -1, -1
        for j in sorted(free_g):
            for i in sorted(free_b):
                if ious[i][j] > best:
                    best, bi, gj = ious[i][j], i, j
        if best <= 0:
            break
        res[bi] = gj
        free_b.discard(bi)
        free_g.discard(gj)
    for i in free_b:
        j = max(range(len(gts)), key=lambda k: (ious[i][k], -k))
        if ious[i][j] > thr:
            res[i] = j
    return res


def hard_negatives(neg_losses, num_pos, ratio=3):
    """Indices into neg_losses of the min(ratio * num_pos, len) largest losses,
    ties by index, in that order."""
    order = sorted(range(len(neg_losses)), key=lambda i: (-neg_losses[i], i))
    return order[:min(ratio * num_pos, len(neg_losses))]


def softmax(z):
    m = max(z)
    e = [math.exp(v - m) for v in z]
    s = sum(e)
    return [v / s for v in e]


def smooth_l1(x):
    return 0.5 * x * x if abs(x) < 1 else abs(x) - 0.5


def ssd_loss(defaults, logits, locs, gts, labels, alpha=1.0, thr=0.5, ratio=3, var=(1.0, 1.0)):
    """The SSD training loss (L_conf + alpha L_loc) / N on given network outputs.

    labels[j] in 1..C is the class of truth j; class 0 is the background. N is the
    number of matched default boxes, and the loss is 0 when N = 0."""
    m = match([corners(d) for d in defaults], gts, thr)
    pos = [i for i, j in enumerate(m) if j >= 0]
    if not pos:
        return 0.0
    neg = [i for i, j in enumerate(m) if j < 0]
    bg_loss = [-math.log(softmax(logits[i])[0]) for i in neg]
    chosen = [neg[k] for k in hard_negatives(bg_loss, len(pos), ratio)]
    conf = -sum(math.log(softmax(logits[i])[labels[m[i]]]) for i in pos)
    conf += -sum(math.log(softmax(logits[i])[0]) for i in chosen)
    loc = sum(smooth_l1(a - b) for i in pos
              for a, b in zip(locs[i], encode(defaults[i], gts[m[i]], var)))
    return (conf + alpha * loc) / len(pos)


def greedy_nms(boxes, scores, thr):
    order = sorted(range(len(boxes)), key=lambda i: (-scores[i], i))
    keep = []
    for i in order:
        if all(iou(boxes[i], boxes[k]) <= thr for k in keep):
            keep.append(i)
    return keep


def detect(defaults, logits, locs, conf_thr=0.01, nms_thr=0.45, top_k=200, var=(1.0, 1.0)):
    """Test-time SSD on given network outputs. Returns a list of
    (score, class, corner box), best first, at most top_k long."""
    # logits and locs are the outputs of the network for every default box.
    assert len(defaults) == len(logits) == len(locs)  # @line L1
    num = len(defaults)  # @line L2
    probs = [softmax(z) for z in logits]  # @line L3
    boxes = [decode(defaults[i], locs[i], var) for i in range(num)]  # @line L4
    dets = []
    for c in range(1, len(logits[0]) if logits else 1):  # @line L5
        cand = [i for i in range(num) if probs[i][c] > conf_thr]
        keep = greedy_nms([boxes[i] for i in cand], [probs[i][c] for i in cand], nms_thr)  # @line L6
        dets.extend((probs[cand[k]][c], c, boxes[cand[k]]) for k in keep)  # @line L7
    dets.sort(key=lambda d: (-d[0], d[1]))
    return dets[:top_k]  # @line L8
