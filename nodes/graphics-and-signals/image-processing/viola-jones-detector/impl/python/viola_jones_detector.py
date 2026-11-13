# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/viola-jones-detector/. The authors are listed in prov/3QXCD1.jsonl.

"""A small Viola-Jones detector: Haar-like features, AdaBoost stumps, a cascade, a scan.

Model: one channel of integers (for example 0..255, used as given, no gamma
step); pixel (x, y) is img[y][x]. Windows lie fully inside the image, so no
border rule is needed. The base window is n x n (24 in the paper; tests use a
smaller n so that pure Python stays fast).

A feature is (kind, x, y, w, h): a pattern of equal cells of size w x h with
its top-left corner at (x, y) in the window. The kinds are "2h" (left minus
right), "2v" (top minus bottom), "3h" and "3v" (center minus the two outer
cells) and "4" (one diagonal pair minus the other).
"""

import math
from fractions import Fraction

KINDS = {"2h": (2, 1), "2v": (1, 2), "3h": (3, 1), "3v": (1, 3), "4": (2, 2)}


# ---------------------------------------------------------------- integral images and features

def integral_image(img):
    """S with (H + 1) x (W + 1) entries, S[y][x] = sum of img[j][i] for j < y and i < x."""
    h, w = len(img), len(img[0])
    s = [[0] * (w + 1) for _ in range(h + 1)]
    for y in range(h):
        run = 0
        for x in range(w):
            run += img[y][x]
            s[y + 1][x + 1] = s[y][x + 1] + run
    return s


def rects(feature):
    """The cells of a feature as (x0, y0, x1, y1, weight) with half-open bounds."""
    kind, x, y, w, h = feature
    if kind == "2h":
        return [(x, y, x + w, y + h, 1), (x + w, y, x + 2 * w, y + h, -1)]
    if kind == "2v":
        return [(x, y, x + w, y + h, 1), (x, y + h, x + w, y + 2 * h, -1)]
    if kind == "3h":
        return [(x, y, x + w, y + h, -1), (x + w, y, x + 2 * w, y + h, 1), (x + 2 * w, y, x + 3 * w, y + h, -1)]
    if kind == "3v":
        return [(x, y, x + w, y + h, -1), (x, y + h, x + w, y + 2 * h, 1), (x, y + 2 * h, x + w, y + 3 * h, -1)]
    if kind == "4":
        return [(x, y, x + w, y + h, 1), (x + w, y, x + 2 * w, y + h, -1),
                (x, y + h, x + w, y + 2 * h, -1), (x + w, y + h, x + 2 * w, y + 2 * h, 1)]
    raise ValueError(kind)


def corner_refs(feature):
    """Merge the corners of the cells into {(x, y): coefficient}. Shared corners collapse."""
    refs = {}
    for x0, y0, x1, y1, wt in rects(feature):
        for (cx, cy), sgn in (((x1, y1), 1), ((x0, y1), -1), ((x1, y0), -1), ((x0, y0), 1)):
            refs[(cx, cy)] = refs.get((cx, cy), 0) + sgn * wt
    return {k: v for k, v in refs.items() if v != 0}


def feature_value(s, feature, ox=0, oy=0):
    """The raw feature value of the window with corner (ox, oy), from the integral image s."""
    return sum(c * s[oy + y][ox + x] for (x, y), c in corner_refs(feature).items())


def enumerate_features(n, kinds=tuple(KINDS)):
    """Every feature that fits in an n x n window, for the given kinds."""
    out = []
    for kind in kinds:
        cw, ch = KINDS[kind]
        for w in range(1, n // cw + 1):
            for h in range(1, n // ch + 1):
                for y in range(n - ch * h + 1):
                    for x in range(n - cw * w + 1):
                        out.append((kind, x, y, w, h))
    return out


def scale_feature(feature, s):
    """Scale positions and cell sizes by s with floor, so the feature fits the scaled window."""
    kind, x, y, w, h = feature
    return (kind, int(x * s), int(y * s), max(1, int(w * s)), max(1, int(h * s)))


def window_sigma(s1, s2, ox, oy, size):
    """Standard deviation of the window from the integral images of f and f^2; 1.0 for a flat window."""
    a = size * size
    t1 = s1[oy + size][ox + size] - s1[oy][ox + size] - s1[oy + size][ox] + s1[oy][ox]
    t2 = s2[oy + size][ox + size] - s2[oy][ox + size] - s2[oy + size][ox] + s2[oy][ox]
    var_a2 = a * t2 - t1 * t1  # a^2 times the variance, an exact integer
    return math.sqrt(var_a2) / a if var_a2 > 0 else 1.0


def normalized_value(s1, sigma, feature, ox, oy, area_ratio=1):
    """Feature value divided by the window deviation and by the cell area ratio of the scaled feature."""
    return feature_value(s1, feature, ox, oy) / (sigma * area_ratio)


def window_values(win, features):
    """Normalized values of all features on one n x n training window."""
    s1 = integral_image(win)
    s2 = integral_image([[v * v for v in r] for r in win])
    sig = window_sigma(s1, s2, 0, 0, len(win))
    return [normalized_value(s1, sig, f, 0, 0) for f in features]


# ---------------------------------------------------------------- weak classifiers and AdaBoost

def stump_predict(v, p, theta):
    """h(x, f, p, theta) = 1 if p f(x) < p theta, else 0."""
    return 1 if p * v < p * theta else 0


def best_stump(values, labels, weights, order=None):
    """Return (error, p, theta) with the least weighted error, by one sweep over the sorted values.

    With S+ and S- the positive and negative weight below the threshold and T+, T- the totals,
    the error is S- + (T+ - S+) for p = 1 and S+ + (T- - S-) for p = -1.
    """
    if order is None:
        order = sorted(range(len(values)), key=lambda i: values[i])
    tp = sum(w for w, y in zip(weights, labels) if y == 1)
    tn = sum(w for w, y in zip(weights, labels) if y == 0)
    sp = sn = 0
    best = None
    k = 0
    m = len(order)
    while True:
        if k == 0:
            theta = values[order[0]] - 1
        elif k == m:
            theta = values[order[-1]] + 1
        else:
            theta = (values[order[k - 1]] + values[order[k]]) / 2
        for err, p in ((sn + (tp - sp), 1), (sp + (tn - sn), -1)):
            if best is None or err < best[0]:
                best = (err, p, theta)
        if k == m:
            break
        # Move every example with the next distinct value below the threshold.
        v = values[order[k]]
        while k < m and values[order[k]] == v:
            i = order[k]
            if labels[i] == 1:
                sp += weights[i]
            else:
                sn += weights[i]
            k += 1
    return best


def boost(table, labels, rows, orders=None):
    """AdaBoost as in Viola and Jones (2004), Table 1, with exact Fraction weights.

    table[f][i] is the value of feature f on example i; rows lists the examples
    in use. Yields after each round a dict with the weak classifiers so far,
    the error of the new one, and the normalized weights it was chosen with.
    """
    lab = [labels[i] for i in rows]
    l = sum(lab)
    m = len(lab) - l
    w = [Fraction(1, 2 * l) if y == 1 else Fraction(1, 2 * m) for y in lab]  # @line L10
    weak = []
    cols = [[col[i] for i in rows] for col in table]
    if orders is None:
        orders = [sorted(range(len(rows)), key=lambda i, c=c: c[i]) for c in cols]
    while True:  # @line L11
        total = sum(w)
        w = [x / total for x in w]  # @line L12
        best = None
        for f, c in enumerate(cols):
            err, p, theta = best_stump(c, lab, w, orders[f])  # @line L13
            if best is None or err < best[0]:
                best = (err, f, p, theta)
        eps, f, p, theta = best
        if eps == 0:
            # One stump separates the examples; it decides alone.
            weak = [(f, p, theta, 1.0)]
            yield {"weak": list(weak), "eps": eps, "weights": w}
            return
        if eps >= Fraction(1, 2):
            return
        beta = eps / (1 - eps)  # @line L14
        weak.append((f, p, theta, math.log(1 / beta)))
        yield {"weak": list(weak), "eps": eps, "weights": w}
        w = [x * beta if stump_predict(cols[f][i], p, theta) == lab[i] else x for i, x in enumerate(w)]


def stage_score(weak, value_of):
    """Sum of alpha h over the weak classifiers; value_of(f) gives the value of feature f."""
    return sum(a for f, p, theta, a in weak if stump_predict(value_of(f), p, theta))


# ---------------------------------------------------------------- cascade

def train_cascade(pos, neg, features, max_stages=4, max_rounds=8, stage_fp=Fraction(1, 2), stage_det=Fraction(1)):
    """Train stages until the negatives run out. Each stage adds stumps until its false positive
    rate on the negatives that reach it is at most stage_fp, keeping a detection rate of at least
    stage_det on the positives by lowering the stage threshold. Returns a list of stages."""
    examples = pos + neg
    labels = [1] * len(pos) + [0] * len(neg)
    vals = [window_values(win, features) for win in examples]
    table = [[vals[i][f] for i in range(len(examples))] for f in range(len(features))]
    findex = {f: k for k, f in enumerate(features)}
    pos_rows = list(range(len(pos)))
    neg_rows = list(range(len(pos), len(examples)))
    stages = []
    for _ in range(max_stages):
        if not neg_rows:
            break
        rows = pos_rows + neg_rows
        stage = None
        for t, state in enumerate(boost(table, labels, rows)):
            weak = [(features[f], p, theta, a) for f, p, theta, a in state["weak"]]
            fidx = {features[f]: f for f, _, _, _ in state["weak"]}

            def score(i, weak=weak, fidx=fidx):
                return stage_score(weak, lambda feat: table[fidx[feat]][i])

            ps = sorted(score(i) for i in pos_rows)
            keep = len(ps) - math.ceil(stage_det * len(ps))
            thr = min(sum(a for *_, a in weak) / 2, ps[keep])  # @line L15
            fp = sum(1 for i in neg_rows if score(i) >= thr)
            stage = {"weak": weak, "threshold": thr}
            if Fraction(fp, len(neg_rows)) <= stage_fp or t + 1 >= max_rounds:
                break
        if stage is None:
            break
        stages.append(stage)
        neg_rows = [i for i in neg_rows  # @line L16
                    if stage_score(stage["weak"], lambda feat, i=i: table[findex[feat]][i]) >= stage["threshold"]]
    return stages


def evaluate_cascade(stages, value_of):
    """Run the stages in order and stop at the first that rejects.

    Returns (accepted, stages_run). value_of(feature) is called only for the
    features of the stages that run."""
    for k, st in enumerate(stages):  # @line L6
        if stage_score(st["weak"], value_of) < st["threshold"]:  # @line L7
            return False, k + 1
    return True, len(stages)


def scan(img, stages, n, scale_factor=1.25, step=1.0):
    """Slide the detector over all scales s = 1, 1.25, 1.25^2, ... and positions with stride [s step].

    Returns (detections, stats) where detections are (x, y, size) and stats
    lists, per window, the number of features evaluated."""
    h, w = len(img), len(img[0])
    s1 = integral_image(img)
    s2 = integral_image([[v * v for v in r] for r in img])  # @line L1
    dets, cost = [], []
    s = 1.0
    while int(n * s) <= min(w, h):  # @line L2
        size = int(n * s)
        scaled = {}
        for st in stages:
            for f, *_ in st["weak"]:
                g = scale_feature(f, s)
                scaled[f] = (g, Fraction(g[3] * g[4], f[3] * f[4]))
        stride = max(1, int(s * step + 0.5))  # @line L3
        for oy in range(0, h - size + 1, stride):  # @line L4
            for ox in range(0, w - size + 1, stride):
                sig = window_sigma(s1, s2, ox, oy, size)  # @line L5
                count = [0]

                def value_of(f):
                    count[0] += 1
                    g, ratio = scaled[f]
                    return normalized_value(s1, sig, g, ox, oy, float(ratio))

                ok, _ = evaluate_cascade(stages, value_of)
                cost.append(count[0])
                if ok:
                    dets.append((ox, oy, size))  # @line L8
        s *= scale_factor
    return dets, cost


def merge_detections(dets):
    """Viola and Jones (2004), Section 5.6: group detections whose boxes overlap (transitively)
    and return one box per group with the average corners, as Fractions (x0, y0, x1, y1)."""
    parent = list(range(len(dets)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i, (xa, ya, sa) in enumerate(dets):
        for j in range(i):
            xb, yb, sb = dets[j]
            if xa < xb + sb and xb < xa + sa and ya < yb + sb and yb < ya + sa:
                parent[find(i)] = find(j)
    groups = {}
    for i in range(len(dets)):
        groups.setdefault(find(i), []).append(dets[i])
    out = []
    for g in groups.values():
        k = len(g)
        out.append((Fraction(sum(x for x, _, _ in g), k), Fraction(sum(y for _, y, _ in g), k),  # @line L9
                    Fraction(sum(x + s for x, _, s in g), k), Fraction(sum(y + s for _, y, s in g), k)))
    return sorted(out)
