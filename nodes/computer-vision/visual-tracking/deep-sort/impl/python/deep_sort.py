# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deep-sort/. The authors are listed in prov/Q69QVS.jsonl.
"""Deep SORT: SORT with a deep association metric (Wojke, Bewley and Paulus 2017).

The appearance network is not part of this file: each detection comes with
its embedding vector, as the output of some re-identification network.

Each track is a constant velocity Kalman filter on (u, v, a, h, du, dv, da, dh):
the box center, the aspect ratio a = width / height, the height, and their
velocities. The noise is scaled by the height, as in the released code.
A track keeps a gallery of the last `budget` embeddings of its detections.

One frame:
  1. predict every track;
  2. matching cascade: for n = 1, 2, ..., max_age, match the confirmed tracks
     whose time since the last update is n with the detections still free,
     by a minimum cost assignment on c = lam * d1 + (1 - lam) * d2, where d1 is
     the squared Mahalanobis distance and d2 the smallest cosine distance to
     the gallery; a pair is allowed only if d1 <= t1 and d2 <= t2;
  3. IoU stage: tentative tracks and confirmed tracks missed only in this
     frame are matched with the free detections on 1 - IoU, allowed if
     1 - IoU <= max_iou_distance;
  4. update the matched tracks, delete tentative tracks that miss, delete
     confirmed tracks missed more than max_age frames, and start a tentative
     track for each free detection.

Boxes are (x1, y1, x2, y2), area (x2 - x1)(y2 - y1). Matrices are lists of rows.
"""

import math

CHI2_95_4DOF = 9.4877  # 95 percent quantile of the chi-square law with 4 degrees of freedom


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


# ---------------------------------------------------------------- boxes and embeddings


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


def cosine_distance(a, b):
    """1 - cos(angle between a and b)."""
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return 1.0 - sum(x * y for x, y in zip(a, b)) / (na * nb)


def gallery_distance(gallery, e):
    """d2: the smallest cosine distance from e to the embeddings of a track."""
    return min(cosine_distance(g, e) for g in gallery)


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


def kf_measurement_noise(mean):
    h = mean[3]
    std = [STD_POS * h, STD_POS * h, 1e-1, STD_POS * h]
    return diag([s * s for s in std])


def kf_project(mean, cov):
    """Predicted measurement and its covariance S = H P H^T + R."""
    s = mat_add(mat_mul(mat_mul(H8, cov), transpose(H8)), kf_measurement_noise(mean))
    return mean[:4], s


def kf_update(mean, cov, z):
    zp, s = kf_project(mean, cov)
    ph = mat_mul(cov, transpose(H8))
    k = mat_mul(ph, inverse(s))
    mean = [a + b for a, b in zip(mean, mat_vec(k, [x - y for x, y in zip(z, zp)]))]
    ikh = mat_sub(eye(8), mat_mul(k, H8))
    r = kf_measurement_noise(zp)
    cov = mat_add(mat_mul(mat_mul(ikh, cov), transpose(ikh)), mat_mul(mat_mul(k, r), transpose(k)))
    return mean, cov


def mahalanobis_sq(mean, cov, z):
    """d1: squared Mahalanobis distance of a measurement z = (u, v, a, h) to the track."""
    zp, s = kf_project(mean, cov)
    d = [x - y for x, y in zip(z, zp)]
    return sum(p * q for p, q in zip(d, mat_vec(inverse(s), d)))


# ---------------------------------------------------------------- assignment


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


def min_cost_matching(cost, allowed, rows, cols):
    """Minimum cost assignment of rows to cols that keeps only allowed pairs.

    cost(i, j) and allowed(i, j) are functions. Pairs that are not allowed get
    one cost above every allowed cost before the assignment, as in the released
    code, and are removed after it. Returns (matches, free rows, free cols).
    """
    if not rows or not cols:
        return [], list(rows), list(cols)
    vals = {(i, j): cost(i, j) for i in rows for j in cols if allowed(i, j)}
    top = max(vals.values(), default=0.0) + 1.0
    mat = [[vals.get((i, j), top) for j in cols] for i in rows]
    matches = [(rows[a], cols[b]) for a, b in hungarian_min(mat) if (rows[a], cols[b]) in vals]
    mr = {i for i, _ in matches}
    mc = {j for _, j in matches}
    return matches, [i for i in rows if i not in mr], [j for j in cols if j not in mc]


def matching_cascade(ages, cost, allowed, cols, max_age):
    """Lines L2 to L4. ages maps each confirmed track to its time since the last update."""
    matches, free = [], list(cols)
    for n in range(1, max_age + 1):  # @line L2
        level = [i for i in sorted(ages) if ages[i] == n]
        if not level or not free:
            continue
        # @line L3 (the cost and the gate are the functions cost and allowed)
        found, _, free = min_cost_matching(cost, allowed, level, free)  # @line L4
        matches += found
    matched = {i for i, _ in matches}
    return matches, [i for i in sorted(ages) if i not in matched], free


# ---------------------------------------------------------------- tracks and tracker

TENTATIVE, CONFIRMED, DELETED = 0, 1, 2


class Track:
    def __init__(self, box, embedding, track_id):
        self.mean, self.cov = kf_initiate(box_to_xyah(box))
        self.id = track_id
        self.hits = 1
        self.age = 1
        self.time_since_update = 0
        self.state = TENTATIVE
        self.gallery = [list(embedding)]

    def box(self):
        return xyah_to_box(self.mean[:4])


class DeepSortTracker:
    """Call step(detections) once per frame; a detection is (box, embedding)."""

    def __init__(self, max_age=30, n_init=3, t1=CHI2_95_4DOF, t2=0.2, lam=0.0,
                 max_iou_distance=0.7, budget=100):
        self.max_age = max_age
        self.n_init = n_init
        self.t1 = t1
        self.t2 = t2
        self.lam = lam
        self.max_iou_distance = max_iou_distance
        self.budget = budget
        self.tracks = []
        self.next_id = 1

    def step(self, detections):
        tr = self.tracks
        for t in tr:  # @line L1
            t.mean, t.cov = kf_predict(t.mean, t.cov)
            t.age += 1
            t.time_since_update += 1
        zs = [box_to_xyah(b) for b, _ in detections]
        d1 = {}
        d2 = {}

        def dist(i, j):
            if (i, j) not in d1:
                d1[(i, j)] = mahalanobis_sq(tr[i].mean, tr[i].cov, zs[j])
                d2[(i, j)] = gallery_distance(tr[i].gallery, detections[j][1])
            return d1[(i, j)], d2[(i, j)]

        def cost(i, j):
            a, b = dist(i, j)
            return self.lam * a + (1.0 - self.lam) * b

        def allowed(i, j):
            a, b = dist(i, j)
            return a <= self.t1 and b <= self.t2

        ages = {i: t.time_since_update for i, t in enumerate(tr) if t.state == CONFIRMED}
        m_a, um_a, free = matching_cascade(ages, cost, allowed, list(range(len(detections))), self.max_age)
        cand = [i for i, t in enumerate(tr) if t.state == TENTATIVE]  # @line L5
        cand += [i for i in um_a if tr[i].time_since_update == 1]
        cand.sort()
        boxes = [t.box() for t in tr]
        m_b, _, free = min_cost_matching(
            lambda i, j: 1.0 - iou(boxes[i], detections[j][0]),
            lambda i, j: 1.0 - iou(boxes[i], detections[j][0]) <= self.max_iou_distance,
            cand, free)
        matched = set()
        for i, j in m_a + m_b:  # @line L6
            t = tr[i]
            t.mean, t.cov = kf_update(t.mean, t.cov, zs[j])
            t.gallery = (t.gallery + [list(detections[j][1])])[-self.budget:]
            t.hits += 1
            t.time_since_update = 0
            if t.state == TENTATIVE and t.hits >= self.n_init:
                t.state = CONFIRMED
            matched.add(i)
        for i, t in enumerate(tr):  # @line L7
            if i not in matched and (t.state == TENTATIVE or t.time_since_update > self.max_age):
                t.state = DELETED
        for j in free:  # @line L8
            tr.append(Track(detections[j][0], detections[j][1], self.next_id))
            self.next_id += 1
        self.tracks = [t for t in tr if t.state != DELETED]
        # @line L9
        return [(t.id, t.box()) for t in self.tracks if t.state == CONFIRMED and t.time_since_update == 0]
