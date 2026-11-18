# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/motion-matching/. The authors are listed in prov/GYSR9F.jsonl.
"""Motion matching: play the database frame whose features best match the
current pose and the desired future trajectory.

The database has f frames. Each frame has a feature vector of d numbers,
split into named groups (for example foot positions, foot velocities, hip
velocity, future trajectory positions and directions). Every dimension is
normalized by its mean and standard deviation over the database, and each
group is multiplied by a weight (a tuning). The cost of a frame is the
squared Euclidean distance between its normalized feature vector and the
query.

Three exact searches return the same frame, with ties broken by the lower
frame number:
  * search_brute: a plain linear scan, O(f d);
  * search_scan: a linear scan that stops a sum once it passes the best cost;
  * KdTree.search: a k-d tree over the normalized features.

run() is the runtime loop: every `interval` frames, or when the input
changes, it builds a query from the current frame and the desired
trajectory, searches, and jumps if the best frame is not the frame that
would play next anyway.
"""

import math


class Database:
    def __init__(self, features, groups, weights, playable=None):
        """features: list of f vectors; groups: list of (name, start, stop);
        weights: dict name -> weight; playable: frames a search may return."""
        self.raw = [list(v) for v in features]
        self.f = len(features)
        self.d = len(features[0])
        self.groups = groups
        self.weights = weights
        self.mean = [sum(v[k] for v in features) / self.f for k in range(self.d)]
        self.std = []
        for k in range(self.d):
            var = sum((v[k] - self.mean[k]) ** 2 for v in features) / self.f
            self.std.append(math.sqrt(var) if var > 0.0 else 1.0)
        self.scale = [1.0] * self.d
        for name, a, b in groups:
            for k in range(a, b):
                self.scale[k] = weights[name] / self.std[k]
        self.X = [self.normalize(v) for v in features]
        self.playable = list(range(self.f)) if playable is None else list(playable)

    def normalize(self, v):
        return [(v[k] - self.mean[k]) * self.scale[k] for k in range(self.d)]  # @line L1


def cost(x, y):
    return sum((a - b) * (a - b) for a, b in zip(x, y))


def search_brute(db, query):
    q = db.normalize(query)
    return min(db.playable, key=lambda i: (cost(db.X[i], q), i))


def search_scan(db, query):
    q = db.normalize(query)
    best, best_i = math.inf, -1
    for i in db.playable:  # @line L2
        x = db.X[i]
        s = 0.0
        for k in range(db.d):  # @line L3
            t = x[k] - q[k]
            s += t * t
            if s > best:  # @line L4
                break
        if s < best:  # @line L5
            best, best_i = s, i
    return best_i  # @line L6


class KdTree:
    """A k-d tree over the normalized features of the playable frames."""

    def __init__(self, db, leaf=4):
        self.db = db
        self.leaf = leaf
        self.root = self._build(list(db.playable))

    def _build(self, idx):
        if len(idx) <= self.leaf:
            return ("leaf", idx)
        X = self.db.X
        d = self.db.d
        spread = [max(X[i][k] for i in idx) - min(X[i][k] for i in idx) for k in range(d)]
        k = max(range(d), key=lambda c: spread[c])
        if spread[k] == 0.0:
            return ("leaf", idx)
        idx.sort(key=lambda i: X[i][k])
        m = len(idx) // 2
        split = X[idx[m]][k]
        left = [i for i in idx if X[i][k] < split]
        right = [i for i in idx if X[i][k] >= split]
        if not left or not right:
            return ("leaf", idx)
        return ("node", k, split, self._build(left), self._build(right))

    def search(self, query):
        q = self.db.normalize(query)
        best = [math.inf, -1]
        self._search(self.root, q, best)
        return best[1]

    def _search(self, node, q, best):
        if node[0] == "leaf":
            for i in node[1]:
                c = cost(self.db.X[i], q)
                if c < best[0] or (c == best[0] and i < best[1]):
                    best[0], best[1] = c, i
            return
        _, k, split, left, right = node
        near, far = (left, right) if q[k] < split else (right, left)
        self._search(near, q, best)
        gap = q[k] - split
        if gap * gap <= best[0]:
            self._search(far, q, best)


def run(db, query_of, ticks, interval, start=0, search=None, next_frame=None):
    """Play `ticks` frames. query_of(t, frame) returns the query vector.

    next_frame(i) is the frame that plays after i without a jump (default
    i + 1). Return the list of played frames and the list of jumps.
    """
    if search is None:
        search = search_scan
    if next_frame is None:
        next_frame = lambda i: i + 1
    frame = start
    played, jumps = [frame], []
    for t in range(1, ticks):
        frame = next_frame(frame)
        if t % interval == 0:
            q = query_of(t, frame)
            best = search(db, q)
            if best != frame:
                jumps.append((t, frame, best))
                frame = best
        played.append(frame)
    return played, jumps
