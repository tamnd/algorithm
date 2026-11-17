# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dalal-triggs-detector/. The authors are listed in prov/7BC4KB.jsonl.
"""The Dalal-Triggs detector: HOG features, a linear SVM, a sliding window
over an image pyramid, hard-negative mining, and greedy non-maximum
suppression.

An image is a list of rows of floats (gray levels). The HOG part follows the
default chain of Dalal and Triggs (2005): centred [-1, 0, 1] gradients,
unsigned orientation in `bins` bins over 0 to 180 degrees, each pixel voting
with its gradient magnitude bilinearly in orientation and in position into
the four nearest cells, blocks of 2 x 2 cells with a stride of one cell, and
L2-Hys normalization of each block. Two simplifications: one gray channel
instead of the colour channel with the largest gradient, and no Gaussian
weight inside a block. The cell grid of a pyramid level is computed once,
and every window reads its blocks from it, so windows move in steps of one
cell. The SVM is trained by dual coordinate descent on the hinge loss.
Standard library only.
"""

import math
import random


# ----------------------------------------------------------------- HOG part

def gradients(img):
    """Centred differences with the border pixel repeated."""
    h, w = len(img), len(img[0])
    gx = [[img[y][min(x + 1, w - 1)] - img[y][max(x - 1, 0)] for x in range(w)] for y in range(h)]
    gy = [[img[min(y + 1, h - 1)][x] - img[max(y - 1, 0)][x] for x in range(w)] for y in range(h)]
    return gx, gy


def cell_histograms(img, cell=8, bins=9):
    """Orientation histograms of the cells of the image (whole cells only).

    A pixel at (x, y) has its centre at (x + 0.5, y + 0.5); it votes its
    gradient magnitude into the two nearest orientation bins and the four
    nearest cell centres with bilinear weights. Votes for cells outside the
    grid are dropped.
    """
    h, w = len(img), len(img[0])
    ny, nx = h // cell, w // cell
    hist = [[[0.0] * bins for _ in range(nx)] for _ in range(ny)]
    gx, gy = gradients(img)  # @line L2
    width = 180.0 / bins
    for y in range(ny * cell):
        ty = (y + 0.5) / cell - 0.5
        cy0 = math.floor(ty)
        fy = ty - cy0
        for x in range(nx * cell):
            dx, dy = gx[y][x], gy[y][x]
            mag = math.hypot(dx, dy)
            if mag == 0.0:
                continue
            ang = math.degrees(math.atan2(dy, dx)) % 180.0
            t = ang / width - 0.5
            b0 = math.floor(t)
            fb = t - b0
            b1 = (b0 + 1) % bins
            b0 %= bins
            tx = (x + 0.5) / cell - 0.5
            cx0 = math.floor(tx)
            fx = tx - cx0
            for cy, wy in ((cy0, 1.0 - fy), (cy0 + 1, fy)):
                if wy == 0.0 or not 0 <= cy < ny:
                    continue
                row = hist[cy]
                for cx, wx in ((cx0, 1.0 - fx), (cx0 + 1, fx)):
                    if wx == 0.0 or not 0 <= cx < nx:
                        continue
                    v = mag * wy * wx
                    hc = row[cx]
                    hc[b0] += v * (1.0 - fb)  # @line L3
                    hc[b1] += v * fb
    return hist


def l2_hys(v, clip=0.2, eps=1e-3):
    """L2 norm, clip every entry at `clip`, L2 norm again."""
    n = math.sqrt(sum(a * a for a in v) + eps * eps)
    u = [min(a / n, clip) for a in v]
    n = math.sqrt(sum(a * a for a in u) + eps * eps)
    return [a / n for a in u]


def block_grid(hist, clip=0.2, eps=1e-3):
    """Normalized 2 x 2 blocks of cells with a stride of one cell."""
    ny, nx = len(hist), len(hist[0]) if hist else 0
    return [[l2_hys(hist[by][bx] + hist[by][bx + 1] + hist[by + 1][bx] + hist[by + 1][bx + 1], clip, eps)
             for bx in range(nx - 1)] for by in range(ny - 1)]


def window_vector(blocks, by, bx, wcells, hcells):
    """The HOG vector of the window whose top-left cell is (by, bx)."""
    v = []
    for i in range(hcells - 1):
        row = blocks[by + i]
        for j in range(wcells - 1):
            v.extend(row[bx + j])
    return v


def hog_descriptor(img, cell=8, bins=9):
    """HOG vector of a whole window image."""
    blocks = block_grid(cell_histograms(img, cell, bins))
    return window_vector(blocks, 0, 0, len(img[0]) // cell, len(img) // cell)


def descriptor_length(width, height, cell=8, bins=9):
    return (width // cell - 1) * (height // cell - 1) * 4 * bins


# --------------------------------------------------------------- images

def mirror(img):
    return [list(reversed(row)) for row in img]


def downscale(img, s):
    """Resize by 1/s with bilinear sampling at pixel centres."""
    h, w = len(img), len(img[0])
    nh, nw = int(round(h / s)), int(round(w / s))
    out = []
    for y in range(nh):
        sy = min(max((y + 0.5) * s - 0.5, 0.0), h - 1.0)
        y0 = int(sy)
        y1 = min(y0 + 1, h - 1)
        fy = sy - y0
        r0, r1 = img[y0], img[y1]
        row = []
        for x in range(nw):
            sx = min(max((x + 0.5) * s - 0.5, 0.0), w - 1.0)
            x0 = int(sx)
            x1 = min(x0 + 1, w - 1)
            fx = sx - x0
            top = r0[x0] * (1 - fx) + r0[x1] * fx
            bot = r1[x0] * (1 - fx) + r1[x1] * fx
            row.append(top * (1 - fy) + bot * fy)
        out.append(row)
    return out


def pyramid(img, min_w, min_h, step=1.2):
    """Yield (scale, image) from scale 1 up, while the window still fits."""
    s = 1.0
    while True:
        level = img if s == 1.0 else downscale(img, s)
        if not level or len(level) < min_h or len(level[0]) < min_w:
            return
        yield s, level
        s *= step


# ------------------------------------------------------------ linear SVM

def dot(a, b):
    return sum(p * q for p, q in zip(a, b))


def train_linear_svm(X, y, C=0.01, bias=1.0, tol=1e-6, max_epochs=2000, seed=0):
    """Hinge-loss linear SVM, min 0.5 |w|^2 + C sum max(0, 1 - y (w.x + b)),
    with the bias as an extra feature of value `bias` (so it is regularized),
    by dual coordinate descent. Returns (w, b, alpha).
    """
    Xa = [list(x) + [bias] for x in X]
    n = len(Xa)
    d = len(Xa[0]) if n else 1
    q = [dot(x, x) for x in Xa]
    alpha = [0.0] * n
    w = [0.0] * d
    rng = random.Random(seed)
    order = list(range(n))
    for _ in range(max_epochs):
        rng.shuffle(order)
        lo, hi = math.inf, -math.inf
        for i in order:
            g = y[i] * dot(w, Xa[i]) - 1.0
            a = alpha[i]
            pg = min(g, 0.0) if a == 0.0 else (max(g, 0.0) if a == C else g)
            lo, hi = min(lo, pg), max(hi, pg)
            if pg != 0.0 and q[i] > 0.0:
                new = min(max(a - g / q[i], 0.0), C)
                if new != a:
                    step = (new - a) * y[i]
                    xi = Xa[i]
                    for k in range(d):
                        w[k] += step * xi[k]
                    alpha[i] = new
        if n == 0 or hi - lo < tol:
            break
    return w[:-1], w[-1] * bias, alpha


def primal_objective(w, b, X, y, C, bias=1.0):
    reg = 0.5 * (dot(w, w) + (b / bias) ** 2)
    return reg + C * sum(max(0.0, 1.0 - yi * (dot(w, x) + b)) for x, yi in zip(X, y))


def dual_objective(alpha, X, y, bias=1.0):
    d = len(X[0]) + 1
    v = [0.0] * d
    for a, x, yi in zip(alpha, X, y):
        for k, xk in enumerate(list(x) + [bias]):
            v[k] += a * yi * xk
    return sum(alpha) - 0.5 * dot(v, v)


def train_with_mining(pos, neg_pool, start, C=0.01, rounds=None, tol=1e-6):
    """Train on the positives and a cache of negatives; add every negative of
    the pool that violates the margin (score above -1) and is not cached;
    repeat until there is none (or for `rounds` rounds). Returns (w, b, cache).
    """
    cache = sorted(set(start))
    r = 0
    while True:
        X = pos + [neg_pool[i] for i in cache]
        y = [1] * len(pos) + [-1] * len(cache)
        w, b, _ = train_linear_svm(X, y, C, tol=tol)
        if rounds is not None and r == rounds:
            return w, b, cache
        have = set(cache)
        hard = [i for i, x in enumerate(neg_pool) if i not in have and dot(w, x) + b > -1.0]
        if not hard:
            return w, b, cache
        cache = sorted(have | set(hard))
        r += 1


# -------------------------------------------------------------- detection

def iou(a, b):
    iw = min(a[2], b[2]) - max(a[0], b[0])
    ih = min(a[3], b[3]) - max(a[1], b[1])
    inter = iw * ih if iw > 0 and ih > 0 else 0
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / union if union > 0 else 0


def greedy_nms(boxes, scores, threshold=0.5):
    order = sorted(range(len(boxes)), key=lambda i: (-scores[i], i))
    keep, removed = [], [False] * len(boxes)
    for pos, i in enumerate(order):
        if removed[i]:
            continue
        keep.append(i)
        for j in order[pos + 1:]:
            if not removed[j] and iou(boxes[i], boxes[j]) > threshold:
                removed[j] = True
    return keep


class Model:
    def __init__(self, w, b, wcells, hcells, cell=8, bins=9):
        self.w, self.b = w, b
        self.wcells, self.hcells, self.cell, self.bins = wcells, hcells, cell, bins


def scan_level(level, model):
    """Scores of every window position of one pyramid level, as a dict
    (cell row, cell column) -> score."""
    hist = cell_histograms(level, model.cell, model.bins)
    blocks = block_grid(hist)
    out = {}
    ny, nx = len(hist), len(hist[0]) if hist else 0
    for by in range(ny - model.hcells + 1):
        for bx in range(nx - model.wcells + 1):
            v = window_vector(blocks, by, bx, model.wcells, model.hcells)
            out[(by, bx)] = dot(model.w, v) + model.b
    return out


def detect(img, model, threshold=0.0, step=1.2, nms_threshold=0.5):
    """Return a list of (box, score), box = (x1, y1, x2, y2) in the input image."""
    cw, ch = model.wcells * model.cell, model.hcells * model.cell
    boxes, scores = [], []
    for s, level in pyramid(img, cw, ch, step):  # @line L1
        hist = cell_histograms(level, model.cell, model.bins)
        blocks = block_grid(hist)  # @line L4
        ny, nx = len(hist), len(hist[0])
        for by in range(ny - model.hcells + 1):  # @line L5
            for bx in range(nx - model.wcells + 1):
                v = window_vector(blocks, by, bx, model.wcells, model.hcells)
                f = dot(model.w, v) + model.b  # @line L6
                if f > threshold:  # @line L7
                    x1, y1 = bx * model.cell * s, by * model.cell * s
                    boxes.append((x1, y1, x1 + cw * s, y1 + ch * s))
                    scores.append(f)
    keep = greedy_nms(boxes, scores, nms_threshold)  # @line L8
    return [(boxes[i], scores[i]) for i in keep]  # @line L9


def negative_windows(images, model, rng, count):
    """Random windows of the negative images, at random pyramid levels."""
    cw, ch = model.wcells * model.cell, model.hcells * model.cell
    out = []
    levels = [lv for img in images for _, lv in pyramid(img, cw, ch)]
    for _ in range(count):
        lv = rng.choice(levels)
        y = rng.randrange(len(lv) - ch + 1)
        x = rng.randrange(len(lv[0]) - cw + 1)
        out.append(hog_descriptor([row[x:x + cw] for row in lv[y:y + ch]], model.cell, model.bins))
    return out


def hard_negatives(images, model, step=1.2):
    """HOG vectors of all windows of the negative images with a score above -1."""
    cw, ch = model.wcells * model.cell, model.hcells * model.cell
    out = []
    for img in images:
        for _, level in pyramid(img, cw, ch, step):
            hist = cell_histograms(level, model.cell, model.bins)
            blocks = block_grid(hist)
            for by in range(len(hist) - model.hcells + 1):
                for bx in range(len(hist[0]) - model.wcells + 1):
                    v = window_vector(blocks, by, bx, model.wcells, model.hcells)
                    if dot(model.w, v) + model.b > -1.0:
                        out.append(v)
    return out


def train_detector(pos_windows, neg_images, cell=8, bins=9, C=0.01, n_random=100,
                   rounds=1, seed=0, tol=1e-3):
    """Train a detector from positive window images and negative images.

    Positives are used with their mirror images. The first SVM sees random
    negative windows; each round then adds every window of the negative
    images with a score above -1 and trains again.
    """
    rng = random.Random(seed)
    hc, wc = len(pos_windows[0]) // cell, len(pos_windows[0][0]) // cell
    model = Model(None, 0.0, wc, hc, cell, bins)
    pos = [hog_descriptor(p, cell, bins) for p in pos_windows]  # @line L10
    pos += [hog_descriptor(mirror(p), cell, bins) for p in pos_windows]
    neg = negative_windows(neg_images, model, rng, n_random)  # @line L11
    X, y = pos + neg, [1] * len(pos) + [-1] * len(neg)
    model.w, model.b, _ = train_linear_svm(X, y, C, tol=tol)  # @line L12
    for _ in range(rounds):  # @line L13
        hard = hard_negatives(neg_images, model)  # @line L14
        if not hard:
            break
        X, y = X + hard, y + [-1] * len(hard)  # @line L15
        model.w, model.b, _ = train_linear_svm(X, y, C, tol=tol)
    return model  # @line L16
