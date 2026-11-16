# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bytetrack/. The authors are listed in prov/0E34WD.jsonl.
"""ByteTrack: the BYTE association of Zhang et al. (ECCV 2022), with IoU as the similarity.

A detection is (box, score). The detections of a frame are split by the
score threshold tau into high ones (score > tau) and low ones
(low_min < score <= tau); boxes with score <= low_min are dropped.

One frame:
  1. predict every track with a Kalman filter on (u, v, a, h) and velocities;
  2. first association: the confirmed tracks (tracked and lost) with the high
     detections, by IoU, rejecting pairs with IoU below 0.2;
  3. second association: the tracked tracks still unmatched with the low
     detections, by IoU, rejecting pairs with IoU below 0.5;
  4. tracked tracks still unmatched become lost; lost tracks older than
     max_lost frames are removed; low detections still unmatched are dropped;
  5. tracks started in the previous frame (unconfirmed) with the high
     detections left, IoU at least 0.3; unconfirmed tracks that miss are removed;
  6. each high detection left with score >= tau + 0.1 starts an unconfirmed track.

Each association is a largest weight matching with weight IoU - bound, which
is what the released code gets from lapjv with a cost limit. The thresholds
are the ones of the paper and its released code.
Boxes are (x1, y1, x2, y2), area (x2 - x1)(y2 - y1). Matrices are lists of rows.
"""

# ---------------------------------------------------------------- small linear algebra


def mat_mul(a, b):
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def transpose(a):
    return [list(r) for r in zip(*a)]


def mat_add(a, b):
    return [[x + y for x, y in zip(r, s)] for r, s in zip(a, b)]


def mat_sub(a, b):
    return [[x - y for x, y in zip(r, s)] for r, s in zip(a, b)]


def mat_vec(a, x):
    return [sum(p * q for p, q in zip(row, x)) for row in a]


def eye(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def diag(values):
    n = len(values)
    return [[float(values[i]) if i == j else 0.0 for j in range(n)] for i in range(n)]


def inverse(a):
    """Inverse of a small nonsingular matrix by Gauss-Jordan elimination with partial pivoting."""
    n = len(a)
    m = [list(map(float, r)) + [1.0 if i == j else 0.0 for j in range(n)] for i, r in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if abs(m[p][c]) < 1e-300:
            raise ValueError("singular matrix")
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        m[c] = [x / piv for x in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0.0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [r[n:] for r in m]


# ---------------------------------------------------------------- boxes


def iou(a, b):
    """Intersection over union of two boxes (x1, y1, x2, y2). Exact on Fractions."""
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    if w <= 0 or h <= 0:
        return 0 * w
    inter = w * h
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / union


def box_to_xyah(box):
    w = box[2] - box[0]
    h = box[3] - box[1]
    return [box[0] + w / 2.0, box[1] + h / 2.0, w / float(h), float(h)]


def xyah_to_box(z):
    w = z[2] * z[3]
    return (z[0] - w / 2.0, z[1] - z[3] / 2.0, z[0] + w / 2.0, z[1] + z[3] / 2.0)


# ---------------------------------------------------------------- Kalman filter on (u, v, a, h)

STD_POS = 1.0 / 20.0
STD_VEL = 1.0 / 160.0
F8 = [[1.0 if (i == j or j == i + 4) else 0.0 for j in range(8)] for i in range(8)]
H8 = [[1.0 if i == j else 0.0 for j in range(8)] for i in range(4)]


def kf_initiate(z):
    h = z[3]
    std = [2 * STD_POS * h, 2 * STD_POS * h, 1e-2, 2 * STD_POS * h,
           10 * STD_VEL * h, 10 * STD_VEL * h, 1e-5, 10 * STD_VEL * h]
    return list(z) + [0.0, 0.0, 0.0, 0.0], diag([s * s for s in std])


def kf_predict(mean, cov):
    h = mean[3]
    std = [STD_POS * h, STD_POS * h, 1e-2, STD_POS * h, STD_VEL * h, STD_VEL * h, 1e-5, STD_VEL * h]
    q = diag([s * s for s in std])
    return mat_vec(F8, mean), mat_add(mat_mul(mat_mul(F8, cov), transpose(F8)), q)


def kf_update(mean, cov, z):
    h = mean[3]
    r = diag([s * s for s in (STD_POS * h, STD_POS * h, 1e-1, STD_POS * h)])
    ph = mat_mul(cov, transpose(H8))
    s = mat_add(mat_mul(H8, ph), r)
    k = mat_mul(ph, inverse(s))
    mean = [a + b for a, b in zip(mean, mat_vec(k, [x - y for x, y in zip(z, mean[:4])]))]
    ikh = mat_sub(eye(8), mat_mul(k, H8))
    cov = mat_add(mat_mul(mat_mul(ikh, cov), transpose(ikh)), mat_mul(mat_mul(k, r), transpose(k)))
    return mean, cov


# ---------------------------------------------------------------- matching


def hungarian_min(cost):
    """Minimum cost assignment for a rectangular matrix of finite costs.

    Returns the sorted list of pairs (row, column); its size is min(rows, columns).
    """
    r = len(cost)
    if r == 0 or len(cost[0]) == 0:
        return []
    c = len(cost[0])
    flip = r > c
    if flip:
        cost = transpose(cost)
        r, c = c, r
    inf = float("inf")
    u, v = [0.0] * (r + 1), [0.0] * (c + 1)
    p, way = [0] * (c + 1), [0] * (c + 1)
    for i in range(1, r + 1):
        p[0], j0 = i, 0
        minv, used = [inf] * (c + 1), [False] * (c + 1)
        while True:
            used[j0] = True
            i0, delta, j1 = p[j0], inf, 0
            for j in range(1, c + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j], way[j] = cur, j0
                    if minv[j] < delta:
                        delta, j1 = minv[j], j
            for j in range(c + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    pairs = [(p[j] - 1, j - 1) for j in range(1, c + 1) if p[j] != 0]
    if flip:
        pairs = [(b, a) for a, b in pairs]
    return sorted(pairs)


def iou_matching(boxes_a, boxes_b, rows, cols, iou_min):
    """A matching of rows to cols of largest total weight IoU - iou_min, using only
    pairs with IoU >= iou_min. Returns (matches, free rows, free cols)."""
    if not rows or not cols:
        return [], list(rows), list(cols)
    w = [[iou(boxes_a[i], boxes_b[j]) - iou_min for j in cols] for i in rows]
    picked = hungarian_min([[-max(0.0, x) for x in row] for row in w])
    matches = [(rows[a], cols[b]) for a, b in picked if w[a][b] >= 0]
    mr = {i for i, _ in matches}
    mc = {j for _, j in matches}
    return matches, [i for i in rows if i not in mr], [j for j in cols if j not in mc]


# ---------------------------------------------------------------- tracks and tracker

NEW, TRACKED, LOST, REMOVED = 0, 1, 2, 3


class Track:
    def __init__(self, box, score, track_id, frame, confirmed):
        self.mean, self.cov = kf_initiate(box_to_xyah(box))
        self.id = track_id
        self.score = score
        self.state = TRACKED
        self.confirmed = confirmed
        self.last_frame = frame

    def box(self):
        return xyah_to_box(self.mean[:4])


class ByteTracker:
    """Call step(detections) once per frame; a detection is (box, score)."""

    def __init__(self, tau=0.6, low_min=0.1, iou_first=0.2, iou_second=0.5,
                 iou_unconfirmed=0.3, new_track_min=0.7, max_lost=30, use_low=True):
        self.tau = tau
        self.low_min = low_min
        self.iou_first = iou_first
        self.iou_second = iou_second
        self.iou_unconfirmed = iou_unconfirmed
        self.new_track_min = new_track_min
        self.max_lost = max_lost
        self.use_low = use_low  # False gives the baseline that drops the low boxes
        self.tracks = []
        self.frame = 0
        self.next_id = 1

    def _update(self, t, det):
        t.mean, t.cov = kf_update(t.mean, t.cov, box_to_xyah(det[0]))
        t.score = det[1]
        t.state = TRACKED
        t.confirmed = True
        t.last_frame = self.frame

    def step(self, detections):
        self.frame += 1
        tr = self.tracks
        boxes = [d[0] for d in detections]
        high = [j for j, d in enumerate(detections) if d[1] > self.tau]  # @line L1
        low = [j for j, d in enumerate(detections) if self.low_min < d[1] <= self.tau]
        for t in tr:  # @line L2
            if t.state != TRACKED:
                t.mean[7] = 0.0  # a lost track keeps its height, as in the released code
            t.mean, t.cov = kf_predict(t.mean, t.cov)
        pred = [t.box() for t in tr]
        pool = [i for i, t in enumerate(tr) if t.confirmed]
        m1, rest, high_left = iou_matching(pred, boxes, pool, high, self.iou_first)  # @line L3
        for i, j in m1:
            self._update(tr[i], detections[j])
        second = [i for i in rest if tr[i].state == TRACKED]
        m2 = []
        if self.use_low:
            m2, _, _ = iou_matching(pred, boxes, second, low, self.iou_second)  # @line L4
            for i, j in m2:
                self._update(tr[i], detections[j])
        done = {i for i, _ in m1 + m2}
        for i in second:  # @line L5
            if i not in done:
                tr[i].state = LOST
        for t in tr:
            if t.state == LOST and self.frame - t.last_frame > self.max_lost:
                t.state = REMOVED
        new = [i for i, t in enumerate(tr) if not t.confirmed]
        m3, miss, high_left = iou_matching(pred, boxes, new, high_left, self.iou_unconfirmed)  # @line L6
        for i, j in m3:
            self._update(tr[i], detections[j])
        for i in miss:
            tr[i].state = REMOVED
        for j in high_left:  # @line L7
            if detections[j][1] >= self.new_track_min:
                tr.append(Track(boxes[j], detections[j][1], self.next_id, self.frame, self.frame == 1))
                self.next_id += 1
        self.tracks = [t for t in tr if t.state != REMOVED]
        # @line L8
        return [(t.id, t.box()) for t in self.tracks if t.state == TRACKED and t.confirmed]
