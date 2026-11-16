# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sort-tracker/. The authors are listed in prov/2C1PFP.jsonl.
"""SORT: simple online and realtime tracking (Bewley et al. 2016).

Each track is a constant velocity Kalman filter on the state
(u, v, s, r, du, dv, ds): the box center (u, v), the area s, the aspect ratio
r = width / height (taken as constant), and the velocities of u, v and s.
In each frame the tracks are predicted, the IoU between every predicted box
and every detection is computed, and the Hungarian algorithm finds the
assignment of largest total IoU. Pairs with IoU below iou_min are dropped.
Matched tracks are corrected, unmatched detections start new tracks, and
tracks that miss more than max_age frames in a row are deleted.

Boxes are (x1, y1, x2, y2) in continuous image coordinates with x1 < x2 and
y1 < y2; the area is (x2 - x1)(y2 - y1), with no +1 term. The noise matrices
follow the released code of the paper. Matrices are lists of rows.
Cost of one frame with n tracks and m detections: O(n m) for the IoU matrix,
O(min(n, m)^2 max(n, m)) for the assignment, and O(n) Kalman steps of fixed size.
"""

import math


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


def box_to_z(box):
    """(x1, y1, x2, y2) to the measurement (u, v, s, r)."""
    w = box[2] - box[0]
    h = box[3] - box[1]
    return [box[0] + w / 2.0, box[1] + h / 2.0, float(w * h), w / float(h)]


def z_to_box(z):
    """(u, v, s, r) to (x1, y1, x2, y2); s and r must be positive."""
    w = math.sqrt(z[2] * z[3])
    h = z[2] / w
    return (z[0] - w / 2.0, z[1] - h / 2.0, z[0] + w / 2.0, z[1] + h / 2.0)


# ---------------------------------------------------------------- assignment


def hungarian_min(cost):
    """Minimum cost assignment for a rectangular matrix of finite costs.

    Returns the sorted list of pairs (row, column); its size is min(rows, columns).
    The potentials method takes O(r^2 c) time for r <= c.
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


def associate(pred_boxes, det_boxes, iou_min):
    """Lines L2 to L4: IoU matrix, assignment of largest total IoU, then the IoU_min filter.

    Returns (matches, unmatched_tracks, unmatched_detections, iou_matrix).
    """
    n, m = len(pred_boxes), len(det_boxes)
    ious = [[iou(p, d) for d in det_boxes] for p in pred_boxes]  # @line L2
    pairs = hungarian_min([[-x for x in row] for row in ious]) if n and m else []  # @line L3
    matches = [(i, j) for i, j in pairs if ious[i][j] >= iou_min]  # @line L4
    mt = {i for i, _ in matches}
    md = {j for _, j in matches}
    return matches, [i for i in range(n) if i not in mt], [j for j in range(m) if j not in md], ious


# ---------------------------------------------------------------- Kalman filter of one track

F7 = [[1.0 if (i == j or j == i + 4) else 0.0 for j in range(7)] for i in range(7)]
H7 = [[1.0 if i == j else 0.0 for j in range(7)] for i in range(4)]
Q7 = diag([1, 1, 1, 1, 0.01, 0.01, 0.0001])
R4 = diag([1, 1, 10, 10])
P0 = diag([10, 10, 10, 10, 10000, 10000, 10000])


class Track:
    """One SORT track: a Kalman filter on (u, v, s, r, du, dv, ds) and its counters."""

    def __init__(self, box, track_id):
        self.x = box_to_z(box) + [0.0, 0.0, 0.0]  # zero velocity
        self.P = [row[:] for row in P0]  # large velocity variance
        self.id = track_id
        self.time_since_update = 0
        self.hits = 0
        self.hit_streak = 0
        self.age = 0

    def predict(self):
        if self.x[2] + self.x[6] <= 0:  # the area must stay positive
            self.x[6] = 0.0
        self.x = mat_vec(F7, self.x)
        self.P = mat_add(mat_mul(mat_mul(F7, self.P), transpose(F7)), Q7)
        self.age += 1
        if self.time_since_update > 0:
            self.hit_streak = 0
        self.time_since_update += 1
        return self.box()

    def update(self, box):
        z = box_to_z(box)
        y = [a - b for a, b in zip(z, mat_vec(H7, self.x))]
        ph = mat_mul(self.P, transpose(H7))
        s = mat_add(mat_mul(H7, ph), R4)
        k = mat_mul(ph, inverse(s))
        self.x = [a + b for a, b in zip(self.x, mat_vec(k, y))]
        ikh = mat_sub(eye(7), mat_mul(k, H7))
        # Joseph form keeps P symmetric and positive definite.
        self.P = mat_add(mat_mul(mat_mul(ikh, self.P), transpose(ikh)), mat_mul(mat_mul(k, R4), transpose(k)))
        self.time_since_update = 0
        self.hits += 1
        self.hit_streak += 1

    def box(self):
        if self.x[2] <= 0 or self.x[3] <= 0:
            return None
        return z_to_box(self.x)


class SortTracker:
    """The SORT tracker. Call step(detections) once per frame."""

    def __init__(self, iou_min=0.3, max_age=1, min_hits=3):
        self.iou_min = iou_min
        self.max_age = max_age
        self.min_hits = min_hits
        self.tracks = []
        self.frame_count = 0
        self.next_id = 1

    def step(self, detections):
        """detections: list of boxes. Returns a list of (track_id, box) for this frame."""
        self.frame_count += 1
        alive = []
        for t in self.tracks:  # @line L1
            if t.predict() is not None:
                alive.append(t)
        self.tracks = alive
        preds = [t.box() for t in self.tracks]
        matches, _, unmatched_dets, _ = associate(preds, detections, self.iou_min)
        for i, j in matches:  # @line L5
            self.tracks[i].update(detections[j])
        for j in unmatched_dets:  # @line L6
            self.tracks.append(Track(detections[j], self.next_id))
            self.next_id += 1
        self.tracks = [t for t in self.tracks if t.time_since_update <= self.max_age]  # @line L7
        out = []
        for t in self.tracks:  # @line L8
            if t.time_since_update == 0 and (t.hit_streak >= self.min_hits or self.frame_count <= self.min_hits):
                out.append((t.id, t.box()))
        return out
