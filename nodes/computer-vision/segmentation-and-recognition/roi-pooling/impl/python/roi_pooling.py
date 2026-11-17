# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/roi-pooling/. The authors are listed in prov/BAJKQQ.jsonl.
"""RoI max pooling of Fast R-CNN, with the rounding of the original Caffe layer.

A feature map is a list of channels; a channel is a list of rows of numbers.
A box is (x1, y1, x2, y2) in image pixels, and scale is the ratio between the
feature map and the image (1/16 for VGG16 conv5). The box is rounded to
feature cells, with inclusive ends, and the H x W grid of bins uses floor for
the start and ceil for the end of each bin. The integer form below computes
floor(p h / H) and ceil((p + 1) h / H) exactly; the Caffe layer uses floats,
which can differ when p h / H is a whole number up to a rounding error.
Standard library only.
"""


def round_half_away(x):
    """C round(): halves go away from zero."""
    return int(x + 0.5) if x >= 0 else -int(-x + 0.5)


def ceil_div(a, b):
    return -((-a) // b)


def roi_box_cells(box, scale):
    """The box in feature cells: (c1, r1, c2, r2) with inclusive ends, and its size (h, w)."""
    c1, r1 = round_half_away(box[0] * scale), round_half_away(box[1] * scale)  # @line L1
    c2, r2 = round_half_away(box[2] * scale), round_half_away(box[3] * scale)
    h, w = max(r2 - r1 + 1, 1), max(c2 - c1 + 1, 1)  # @line L2
    return (c1, r1, c2, r2), (h, w)


def bins(box, scale, out_h, out_w, fh, fw):
    """For each bin (p, q), the half-open row range and column range it covers on the map."""
    (c1, r1, _, _), (h, w) = roi_box_cells(box, scale)
    out = {}
    for p in range(out_h):  # @line L3
        for q in range(out_w):
            rs = min(max(r1 + (p * h) // out_h, 0), fh)  # @line L4
            re = min(max(r1 + ceil_div((p + 1) * h, out_h), 0), fh)
            cs = min(max(c1 + (q * w) // out_w, 0), fw)  # @line L5
            ce = min(max(c1 + ceil_div((q + 1) * w, out_w), 0), fw)
            out[(p, q)] = (rs, re, cs, ce)
    return out


def roi_pool(feat, box, scale, out_h, out_w):
    """Return (Y, S): pooled values and argmax switches (row, col), or None for an empty bin.

    Ties go to the first cell in row-major order, as the strict > of the Caffe loop.
    """
    fh, fw = len(feat[0]), len(feat[0][0])
    grid = bins(box, scale, out_h, out_w, fh, fw)
    y, s = [], []
    for ch in feat:
        yc = [[0.0] * out_w for _ in range(out_h)]
        sc = [[None] * out_w for _ in range(out_h)]
        for (p, q), (rs, re, cs, ce) in grid.items():
            best, arg = None, None
            for r in range(rs, re):
                for c in range(cs, ce):
                    if best is None or ch[r][c] > best:
                        best, arg = ch[r][c], (r, c)
            if arg is not None:
                yc[p][q], sc[p][q] = best, arg  # @line L6
        y.append(yc)
        s.append(sc)
    return y, s  # @line L7


def roi_pool_backward(dy, switches, fh, fw):
    """Gradient on the feature map: each bin sends its gradient to its argmax cell."""
    out = []
    for dyc, sc in zip(dy, switches):
        g = [[0.0] * fw for _ in range(fh)]
        for p, row in enumerate(sc):
            for q, arg in enumerate(row):
                if arg is not None:
                    g[arg[0]][arg[1]] += dyc[p][q]  # @line L8
        out.append(g)
    return out


def roi_pool_many(feat, boxes, scale, out_h, out_w):
    """Pool every box of a list; the cost of each box is that of its own bins."""
    return [roi_pool(feat, b, scale, out_h, out_w)[0] for b in boxes]
