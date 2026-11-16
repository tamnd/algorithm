# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/global-nearest-neighbor-association/. The authors are listed in prov/VW85MF.jsonl.
"""Global nearest neighbor (GNN) data association with Kalman filter tracks.

Each frame, every track predicts its measurement z_hat with the innovation
covariance S. The cost of the pair (track i, measurement j) is the squared
Mahalanobis distance d2 = (z_j - z_hat_i)^T S_i^-1 (z_j - z_hat_i), and a pair
with d2 above the gate gamma is forbidden. A track may stay unassigned at the
cost c_miss, and a measurement at the cost c_new. The one-to-one assignment of
least total cost is found by the Hungarian algorithm on an augmented square
matrix. Matrices are lists of rows. Cost of one step: O((n + m)^3) time for n
tracks and m measurements, and O((n + m)^2) space.
"""

import math

INF = float("inf")


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(r) for r in zip(*a)]


def mat_add(a, b):
    return [[x + y for x, y in zip(r, s)] for r, s in zip(a, b)]


def mat_sub(a, b):
    return [[x - y for x, y in zip(r, s)] for r, s in zip(a, b)]


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


def mahalanobis2(z, z_hat, s):
    """Squared Mahalanobis distance of the innovation z - z_hat under the covariance s."""
    nu = [[a - b] for a, b in zip(z, z_hat)]
    return mat_mul(mat_mul(transpose(nu), inverse(s)), nu)[0][0]


def hungarian(cost):
    """Minimum cost assignment of the rows of an r x c matrix (r <= c) to distinct columns.

    Entries may be INF (forbidden). Returns (row_to_col, total), or None when no
    assignment of finite cost exists. The potentials method takes O(r^2 c) time.
    """
    r = len(cost)
    if r == 0:
        return [], 0.0
    c = len(cost[0])
    u, v = [0.0] * (r + 1), [0.0] * (c + 1)
    p, way = [0] * (c + 1), [0] * (c + 1)
    for i in range(1, r + 1):
        p[0], j0 = i, 0
        minv, used = [INF] * (c + 1), [False] * (c + 1)
        while True:
            used[j0] = True
            i0, delta, j1 = p[j0], INF, 0
            for j in range(1, c + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j], way[j] = cur, j0
                    if minv[j] < delta:
                        delta, j1 = minv[j], j
            if delta == INF:
                return None
            for j in range(c + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while j0:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
    row_to_col = [-1] * r
    for j in range(1, c + 1):
        if p[j]:
            row_to_col[p[j] - 1] = j - 1
    return row_to_col, sum(cost[i][row_to_col[i]] for i in range(r))


def gnn_assign(z_hats, covs, zs, gamma, c_miss=None, c_new=None):
    """GNN association of one frame (lines L2 to L6 of the page).

    z_hats, covs: the predicted measurement and innovation covariance of each track.
    zs: the measurements. gamma: the gate on the squared Mahalanobis distance.
    c_miss, c_new: the costs of an unassigned track and of an unassigned
    measurement, gamma / 2 each by default, so that a gated pair is always
    worth taking. Returns (pairs, missed_tracks, new_measurements, total_cost)
    with pairs a dict from track to measurement.
    """
    if c_miss is None:
        c_miss = gamma / 2
    if c_new is None:
        c_new = gamma / 2
    n, m = len(z_hats), len(zs)
    c = [[INF] * m for _ in range(n)]
    for i in range(n):  # @line L2
        for j in range(m):
            d2 = mahalanobis2(zs[j], z_hats[i], covs[i])  # @line L3
            c[i][j] = d2 if d2 <= gamma else INF  # @line L4
    size = n + m
    a = [[INF] * size for _ in range(size)]  # @line L5
    for i in range(n):
        for j in range(m):
            a[i][j] = c[i][j]
        a[i][m + i] = c_miss
    for j in range(m):
        a[n + j][j] = c_new
        for i in range(n):
            a[n + j][m + i] = 0.0
    row_to_col, total = hungarian(a)  # @line L6
    pairs = {i: row_to_col[i] for i in range(n) if row_to_col[i] < m}
    missed = [i for i in range(n) if i not in pairs]
    taken = set(pairs.values())
    new = [j for j in range(m) if j not in taken]
    return pairs, missed, new, total


def cv_model(q, r):
    """Constant velocity model in 2D with a time step of 1: F, Q, H, R."""
    f = [[1.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 1.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    qm = [[q / 3, 0.0, q / 2, 0.0], [0.0, q / 3, 0.0, q / 2], [q / 2, 0.0, q, 0.0], [0.0, q / 2, 0.0, q]]
    h = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]]
    rm = [[r, 0.0], [0.0, r]]
    return f, qm, h, rm


class GNNTracker:
    """A multi-target tracker: Kalman prediction, GNN association, Kalman update, births."""

    def __init__(self, gamma=9.21, q=0.05, r=0.25, p_vel=4.0, max_misses=3):
        self.gamma, self.p_vel, self.max_misses = gamma, p_vel, max_misses
        self.f, self.q, self.h, self.r = cv_model(q, r)
        self.tracks = []  # each: {"id", "x" (4 x 1), "p" (4 x 4), "misses"}
        self.next_id = 0

    def _birth(self, z):
        rr = self.r[0][0]
        p = [[rr, 0, 0, 0], [0, rr, 0, 0], [0, 0, self.p_vel, 0], [0, 0, 0, self.p_vel]]
        self.tracks.append({"id": self.next_id, "x": [[z[0]], [z[1]], [0.0], [0.0]], "p": p, "misses": 0})
        self.next_id += 1

    def step(self, zs):
        """Process the measurements of one frame. Returns {track id: (x, y)} after the update."""
        z_hats, covs, gains = [], [], []
        for t in self.tracks:  # @line L1
            t["x"] = mat_mul(self.f, t["x"])
            t["p"] = mat_add(mat_mul(mat_mul(self.f, t["p"]), transpose(self.f)), self.q)
            ph = mat_mul(t["p"], transpose(self.h))
            s = mat_add(mat_mul(self.h, ph), self.r)
            z_hats.append([row[0] for row in mat_mul(self.h, t["x"])])
            covs.append(s)
            gains.append(mat_mul(ph, inverse(s)))
        pairs, missed, new, _ = gnn_assign(z_hats, covs, zs, self.gamma)
        for i, j in pairs.items():  # @line L7
            t, k = self.tracks[i], gains[i]
            nu = [[zs[j][0] - z_hats[i][0]], [zs[j][1] - z_hats[i][1]]]
            t["x"] = mat_add(t["x"], mat_mul(k, nu))
            t["p"] = mat_sub(t["p"], mat_mul(mat_mul(k, covs[i]), transpose(k)))
            t["misses"] = 0
        for i in missed:  # @line L8
            self.tracks[i]["misses"] += 1
        self.tracks = [t for t in self.tracks if t["misses"] < self.max_misses]
        for j in new:
            self._birth(zs[j])
        return {t["id"]: (t["x"][0][0], t["x"][1][0]) for t in self.tracks}


def greedy_nearest_neighbor(z_hats, covs, zs, gamma):
    """The local rule for comparison: take the gated pair of least distance, remove both, repeat."""
    cand = []
    for i in range(len(z_hats)):
        for j in range(len(zs)):
            d2 = mahalanobis2(zs[j], z_hats[i], covs[i])
            if d2 <= gamma:
                cand.append((d2, i, j))
    cand.sort()
    pairs, used_t, used_m = {}, set(), set()
    for _, i, j in cand:
        if i not in used_t and j not in used_m:
            pairs[i] = j
            used_t.add(i)
            used_m.add(j)
    return pairs
