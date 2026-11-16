# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orb-slam/. The authors are listed in prov/TY0PRT.jsonl.

"""A toy of the keyframe and loop closing core of ORB-SLAM, in the plane.

This is a toy. There are no images. A keyframe is a planar pose (x, y,
theta) and a list of features; a feature is a visual word (an integer, the
stand-in for a quantized ORB descriptor) and a 2D point in the frame of the
keyframe (the stand-in for a triangulated map point). The odometry between
keyframes stands in for the tracking thread, and there is no local bundle
adjustment. What the toy keeps from ORB-SLAM (Mur-Artal, Montiel and Tardos
2015) is the structure of the loop closing thread:

  - map points shared by keyframes, and the covisibility graph whose edge
    weight is the number of shared map points,
  - the spanning tree (each keyframe's parent shares the most points with it),
  - bag of words vectors with tf-idf weights, the L1 score of DBoW2, and an
    inverted index from words to keyframes,
  - loop candidates: score at least the least score of the covisible
    neighbors, and no shared map point,
  - the consistency check over three consecutive keyframes,
  - a geometric check (here a 2D rigid fit in place of the Sim(3) fit),
  - map point fusion, and pose graph optimization on the essential graph
    (spanning tree, strong covisibility edges, loop edges) by Gauss-Newton
    in SE(2) in place of Sim(3).
"""

import math

# ------------------------------------------------------------- SE(2) helpers


def wrap(a):
    return (a + math.pi) % (2.0 * math.pi) - math.pi


def compose(a, b):
    c, s = math.cos(a[2]), math.sin(a[2])
    return (a[0] + c * b[0] - s * b[1], a[1] + s * b[0] + c * b[1], wrap(a[2] + b[2]))


def inverse(a):
    c, s = math.cos(a[2]), math.sin(a[2])
    return (-c * a[0] - s * a[1], s * a[0] - c * a[1], -a[2])


def between(a, b):
    """The pose of b in the frame of a."""
    return compose(inverse(a), b)


def transform(pose, p):
    c, s = math.cos(pose[2]), math.sin(pose[2])
    return (pose[0] + c * p[0] - s * p[1], pose[1] + s * p[0] + c * p[1])


# ------------------------------------------------------------- bag of words


def bow_vector(words, idf):
    """tf-idf weights of a list of words, divided by their sum (L1 norm 1)."""
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    total = len(words)
    vec = {w: n / total * idf.get(w, 0.0) for w, n in counts.items()}
    vec = {w: x for w, x in vec.items() if x > 0.0}
    norm = sum(vec.values())
    return {w: x / norm for w, x in vec.items()} if norm > 0.0 else {}


def l1_score(u, v):
    """The DBoW2 score 1 - |u - v|_1 / 2 of two vectors with L1 norm 1."""
    keys = set(u) | set(v)
    return 1.0 - 0.5 * sum(abs(u.get(w, 0.0) - v.get(w, 0.0)) for w in keys)


class InvertedIndex:
    """Word -> list of (keyframe, weight). A query visits only shared words.

    For nonnegative vectors with L1 norm 1, 1 - |u - v|_1 / 2 equals the sum
    of min(u_w, v_w) over the shared words, so the index gives the exact score.
    """

    def __init__(self):
        self.lists = {}

    def add(self, k, vec):
        for w, x in vec.items():
            self.lists.setdefault(w, []).append((k, x))

    def query(self, vec):
        scores = {}
        for w, x in vec.items():
            for k, y in self.lists.get(w, ()):
                scores[k] = scores.get(k, 0.0) + min(x, y)
        return scores


# ------------------------------------------------------------- geometric check


def fit_rigid(pairs):
    """Least squares (R, t) with q = R p + t for pairs (p, q), as a pose."""
    n = len(pairs)
    px = sum(p[0] for p, _ in pairs) / n
    py = sum(p[1] for p, _ in pairs) / n
    qx = sum(q[0] for _, q in pairs) / n
    qy = sum(q[1] for _, q in pairs) / n
    sxx = sum((p[0] - px) * (q[0] - qx) + (p[1] - py) * (q[1] - qy) for p, q in pairs)
    sxy = sum((p[0] - px) * (q[1] - qy) - (p[1] - py) * (q[0] - qx) for p, q in pairs)
    th = math.atan2(sxy, sxx)
    c, s = math.cos(th), math.sin(th)
    return (qx - (c * px - s * py), qy - (s * px + c * py), th)


def inliers_of(pose, pairs, tol):
    out = []
    for idx, (p, q) in enumerate(pairs):
        r = transform(pose, p)
        if math.hypot(r[0] - q[0], r[1] - q[1]) < tol:
            out.append(idx)
    return out


def robust_rigid(pairs, tol):
    """Try every pair of matches as a minimal sample; refit on the best inlier set."""
    best = []
    for a in range(len(pairs)):
        for b in range(a + 1, len(pairs)):
            pa, pb = pairs[a][0], pairs[b][0]
            if math.hypot(pa[0] - pb[0], pa[1] - pb[1]) < 1e-6:
                continue
            ins = inliers_of(fit_rigid([pairs[a], pairs[b]]), pairs, tol)
            if len(ins) > len(best):
                best = ins
    if len(best) < 2:
        return None, []
    pose = fit_rigid([pairs[i] for i in best])
    return pose, inliers_of(pose, pairs, tol)


# ------------------------------------------------------------- pose graph


def edge_error_and_jacobians(xi, xj, z):
    """Error of the edge (i, j) with measurement z, and its Jacobians."""
    ci, si = math.cos(xi[2]), math.sin(xi[2])
    cz, sz = math.cos(z[2]), math.sin(z[2])
    dx, dy = xj[0] - xi[0], xj[1] - xi[1]
    # R_i^T (t_j - t_i)
    lx, ly = ci * dx + si * dy, -si * dx + ci * dy
    ex, ey = lx - z[0], ly - z[1]
    e = [cz * ex + sz * ey, -sz * ex + cz * ey, wrap(xj[2] - xi[2] - z[2])]
    # derivatives of (lx, ly) with respect to x_i
    dl = [[-ci, -si, -si * dx + ci * dy], [si, -ci, -ci * dx - si * dy]]
    a = [[cz * dl[0][k] + sz * dl[1][k] for k in range(3)], [-sz * dl[0][k] + cz * dl[1][k] for k in range(3)], [0.0, 0.0, -1.0]]
    rb = [[ci, si], [-si, ci]]
    b = [[cz * rb[0][0] + sz * rb[1][0], cz * rb[0][1] + sz * rb[1][1], 0.0], [-sz * rb[0][0] + cz * rb[1][0], -sz * rb[0][1] + cz * rb[1][1], 0.0], [0.0, 0.0, 1.0]]
    return e, a, b


def solve_spd(h, g):
    """Solve h x = g for a symmetric positive definite h by Cholesky."""
    n = len(h)
    lo = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = h[i][j] - sum(lo[i][k] * lo[j][k] for k in range(j))
            if i == j:
                if s <= 0.0:
                    raise ValueError("the system is not positive definite")
                lo[i][i] = math.sqrt(s)
            else:
                lo[i][j] = s / lo[j][j]
    y = [0.0] * n
    for i in range(n):
        y[i] = (g[i] - sum(lo[i][k] * y[k] for k in range(i))) / lo[i][i]
    x = [0.0] * n
    for i in reversed(range(n)):
        x[i] = (y[i] - sum(lo[k][i] * x[k] for k in range(i + 1, n))) / lo[i][i]
    return x


def graph_cost(poses, edges):
    total = 0.0
    for i, j, z in edges:
        e, _, _ = edge_error_and_jacobians(poses[i], poses[j], z)
        total += sum(x * x for x in e)
    return total


def optimize_pose_graph(poses, edges, iterations=10):
    """Gauss-Newton on SE(2) with unit information and pose 0 fixed."""
    poses = list(poses)
    n = len(poses) - 1
    for _ in range(iterations):
        h = [[0.0] * (3 * n) for _ in range(3 * n)]
        g = [0.0] * (3 * n)
        for i, j, z in edges:
            e, a, b = edge_error_and_jacobians(poses[i], poses[j], z)
            blocks = [(i, a), (j, b)]
            for u, ju in blocks:
                if u == 0:
                    continue
                for r in range(3):
                    g[3 * (u - 1) + r] -= sum(ju[k][r] * e[k] for k in range(3))
                for v, jv in blocks:
                    if v == 0:
                        continue
                    for r in range(3):
                        for c in range(3):
                            h[3 * (u - 1) + r][3 * (v - 1) + c] += sum(ju[k][r] * jv[k][c] for k in range(3))
        dx = solve_spd(h, g)
        for k in range(n):
            p = poses[k + 1]
            poses[k + 1] = (p[0] + dx[3 * k], p[1] + dx[3 * k + 1], wrap(p[2] + dx[3 * k + 2]))
        if max(abs(x) for x in dx) < 1e-10:
            break
    return poses


# ------------------------------------------------------------- the toy system


class ToyOrbSlam:
    def __init__(self, idf, covis_min=3, strong_min=8, window=4, match_radius=0.5, consistency=3, min_inliers=6, inlier_tol=0.15, skip=10):
        self.idf = idf
        self.covis_min = covis_min
        self.strong_min = strong_min
        self.window = window
        self.match_radius = match_radius
        self.consistency = consistency
        self.min_inliers = min_inliers
        self.inlier_tol = inlier_tol
        self.skip = skip
        self.poses = []  # keyframe poses
        self.obs = []  # keyframe -> list of [word, local point, map point]
        self.bow = []
        self.points = []  # map point -> (reference keyframe, local point, word)
        self.seen_by = []  # map point -> set of keyframes
        self.weights = []  # keyframe -> {keyframe: number of shared map points}
        self.parent = []
        self.index = InvertedIndex()
        self.groups = []  # (set of keyframes, consistency count) of the last keyframe
        self.loops = []  # (j, k, measured pose of k in the frame of j)
        self.last_loop = 0
        self.events = []

    # map points and covisibility

    def point_world(self, p):
        ref, local, _ = self.points[p]
        return transform(self.poses[ref], local)

    def neighbors(self, k):
        return {j for j, w in self.weights[k].items() if w >= self.covis_min}

    def _connect(self, k):
        counts = {}
        for _, _, p in self.obs[k]:
            for j in self.seen_by[p]:
                if j != k:
                    counts[j] = counts.get(j, 0) + 1
        for j in self.weights[k]:
            self.weights[j].pop(k, None)
        self.weights[k] = counts
        for j, w in counts.items():
            self.weights[j][k] = w
        return counts

    def _new_keyframe(self, motion, features):
        k = len(self.poses)
        pose = compose(self.poses[-1], motion) if k else motion
        self.poses.append(pose)
        local = set()
        for j in range(max(0, k - self.window), k):
            local.update(p for _, _, p in self.obs[j])
        obs = []
        used = set()
        for word, pt in features:
            w = transform(pose, pt)
            best, best_d = None, self.match_radius
            for p in local:
                if p in used or self.points[p][2] != word:
                    continue
                q = self.point_world(p)
                d = math.hypot(q[0] - w[0], q[1] - w[1])
                if d < best_d:
                    best, best_d = p, d
            if best is None:
                best = len(self.points)
                self.points.append((k, pt, word))
                self.seen_by.append(set())
            used.add(best)
            self.seen_by[best].add(k)
            obs.append([word, pt, best])
        self.obs.append(obs)
        self.bow.append(bow_vector([w for w, _, _ in obs], self.idf))
        self.weights.append({})
        return k

    # loop closing

    def _candidates(self, k):
        nbrs = self.neighbors(k)
        if not nbrs or k < self.last_loop + self.skip:
            return [], {}
        s_min = min(l1_score(self.bow[k], self.bow[j]) for j in nbrs)  # @line L3
        scores = self.index.query(self.bow[k])
        connected = set(self.weights[k])
        cands = [j for j, s in scores.items() if s >= s_min - 1e-12 and j not in connected and j != k]  # @line L4
        return cands, scores

    def _consistent(self, cands):
        new_groups = []
        accepted = []
        for j in cands:
            group = {j} | self.neighbors(j)
            count = 1
            for g, n in self.groups:
                if g & group:
                    count = max(count, n + 1)
            new_groups.append((group, count))  # @line L5
            if count >= self.consistency:
                accepted.append(j)
        self.groups = new_groups
        return accepted

    def _match(self, k, j):
        def unique(obs):
            seen = {}
            for idx, (w, _, _) in enumerate(obs):
                seen.setdefault(w, []).append(idx)
            return {w: v[0] for w, v in seen.items() if len(v) == 1}

        uk, uj = unique(self.obs[k]), unique(self.obs[j])
        return [(uk[w], uj[w]) for w in uk if w in uj]

    def _essential_edges(self):
        edges = []
        seen = set()
        for k in range(1, len(self.poses)):
            p = self.parent[k]
            edges.append((p, k, between(self.poses[p], self.poses[k])))
            seen.add((min(p, k), max(p, k)))
        for k in range(len(self.poses)):
            for j, w in self.weights[k].items():
                if j < k and w >= self.strong_min and (j, k) not in seen:
                    edges.append((j, k, between(self.poses[j], self.poses[k])))
                    seen.add((j, k))
        edges.extend(self.loops)
        return edges

    def _close_loop(self, k, j, rel, pairs):
        self.loops.append((j, k, rel))
        # The essential graph is taken before the fusion. The links that the
        # fusion creates join keyframes across the loop, and their relative
        # poses from the drifted estimates must not become constraints.
        edges = self._essential_edges()
        for a, b in pairs:
            old, new = self.obs[k][a][2], self.obs[j][b][2]
            if old != new:
                self.seen_by[old].discard(k)
                self.seen_by[new].add(k)
                self.obs[k][a][2] = new
        self._connect(k)
        self.poses = optimize_pose_graph(self.poses, edges)  # @line L9
        self.last_loop = k
        self.groups = []

    def add_keyframe(self, motion, features):
        """Insert a keyframe and run loop closing. Return (j, k) for a closed loop, else None."""
        k = self._new_keyframe(motion, features)  # @line L1
        counts = self._connect(k)
        earlier = {j: w for j, w in counts.items() if j < k}
        self.parent.append(max(earlier, key=lambda j: (earlier[j], -j)) if earlier else max(k - 1, 0))  # @line L2
        cands, scores = self._candidates(k)
        accepted = self._consistent(cands)
        result = None
        for j in sorted(accepted, key=lambda c: -scores[c]):
            matches = self._match(k, j)  # @line L6
            pairs = [(self.obs[k][a][1], self.obs[j][b][1]) for a, b in matches]
            if len(pairs) < self.min_inliers:
                continue
            rel, ins = robust_rigid(pairs, self.inlier_tol)
            if rel is not None and len(ins) >= self.min_inliers:  # @line L7
                self._close_loop(k, j, rel, [matches[i] for i in ins])  # @line L8
                self.events.append(("loop", j, k, len(ins)))
                result = (j, k)
                break
            self.events.append(("rejected", j, k, len(ins)))
        self.index.add(k, self.bow[k])  # @line L10
        return result
