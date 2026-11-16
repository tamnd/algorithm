# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiple-hypothesis-tracking/. The authors are listed in prov/XRTTYC.jsonl.
"""Multiple hypothesis tracking (MHT), hypothesis-oriented, after Reid (1979),
with the k-best assignments of Murty (1968) as proposed by Cox and Hingorani (1996).

A hypothesis is a full explanation of all measurements so far: a set of tracks,
each a Kalman filter, and a log weight. In each frame every hypothesis spawns
children, one per assignment of the new measurements to its tracks, to new
targets or to false alarms. The log weight of a child follows Reid's formula,
which turns into a cost matrix with one row per measurement, so the best
children of a hypothesis are the k best assignments of that matrix. The M
children of highest weight over all hypotheses are kept. Matrices are lists of
rows.
"""

import heapq
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


def inverse_and_det(a):
    """Inverse and determinant of a small nonsingular matrix by Gauss-Jordan elimination."""
    n = len(a)
    m = [list(map(float, r)) + [1.0 if i == j else 0.0 for j in range(n)] for i, r in enumerate(a)]
    det = 1.0
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if abs(m[p][c]) < 1e-300:
            raise ValueError("singular matrix")
        if p != c:
            m[c], m[p] = m[p], m[c]
            det = -det
        piv = m[c][c]
        det *= piv
        m[c] = [x / piv for x in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0.0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [r[n:] for r in m], det


def hungarian(cost):
    """Least-cost assignment of the rows of an r x c matrix (r <= c) to distinct columns.

    Entries may be INF. Returns (total, row_to_col), or None if every
    assignment has an INF entry. O(r^2 c) time.
    """
    r = len(cost)
    if r == 0:
        return 0.0, []
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
    return sum(cost[i][row_to_col[i]] for i in range(r)), row_to_col


def _constrained(cost, forced, forbidden):
    a = [list(row) for row in cost]
    for r, c in forbidden:
        a[r][c] = INF
    for r, c in forced:
        for k in range(len(a[0])):
            if k != c:
                a[r][k] = INF
        for k in range(len(a)):
            if k != r:
                a[k][c] = INF
    return a


def murty_k_best(cost, k):
    """The k assignments of least cost, in order of cost, by Murty's partitioning.

    Returns a list of (total, row_to_col). Each node of the search is the
    original problem with some pairs forced and some forbidden. Its best
    assignment is split into disjoint subproblems: for the t-th free row, the
    rows before it keep their columns and row t loses its column.
    """
    first = hungarian(cost)
    if first is None or k <= 0:
        return []
    tie = 0
    heap = [(first[0], tie, first[1], (), ())]
    out = []
    while heap and len(out) < k:
        total, _, sol, forced, forbidden = heapq.heappop(heap)
        out.append((total, sol))
        fixed = list(forced)
        forced_rows = {r for r, _ in forced}
        for row in range(len(cost)):
            if row in forced_rows:
                continue
            sub_forbidden = forbidden + ((row, sol[row]),)
            res = hungarian(_constrained(cost, fixed, sub_forbidden))
            if res is not None:
                tie += 1
                heapq.heappush(heap, (res[0], tie, res[1], tuple(fixed), sub_forbidden))
            fixed.append((row, sol[row]))
    return out


def cv_model(q, r):
    """Constant velocity model in 2D with a time step of 1: F, Q, H, R."""
    f = [[1.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 1.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    qm = [[q / 3, 0.0, q / 2, 0.0], [0.0, q / 3, 0.0, q / 2], [q / 2, 0.0, q, 0.0], [0.0, q / 2, 0.0, q]]
    h = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]]
    rm = [[r, 0.0], [0.0, r]]
    return f, qm, h, rm


class MHT:
    """Hypothesis-oriented MHT with M hypotheses, a gate, and deletion after max_misses misses in a row."""

    def __init__(self, p_d=0.9, beta_nt=0.001, beta_ft=0.01, gamma=9.21, m_best=5, q=0.01, r=0.25, p_vel=1.0, max_misses=3):
        self.p_d, self.beta_nt, self.beta_ft = p_d, beta_nt, beta_ft
        self.gamma, self.m_best, self.max_misses, self.p_vel = gamma, m_best, max_misses, p_vel
        self.model = cv_model(q, r)
        self.next_id = 0
        self.hyps = [(0.0, [])]  # (log weight, tracks); a track is (id, x, P, misses)

    def add_track(self, x, p):
        """Add a known track to every hypothesis (used to start from given targets)."""
        tid = self.next_id
        self.next_id += 1
        self.hyps = [(w, tracks + [(tid, x, p, 0)]) for w, tracks in self.hyps]
        return tid

    def _predict(self, tracks):
        f, q, h, r = self.model
        out = []
        for tid, x, p, misses in tracks:
            xp = mat_mul(f, x)
            pp = mat_add(mat_mul(mat_mul(f, p), transpose(f)), q)
            ph = mat_mul(pp, transpose(h))
            s = mat_add(mat_mul(h, ph), r)
            s_inv, det = inverse_and_det(s)
            z_hat = [row[0] for row in mat_mul(h, xp)]
            out.append((tid, xp, pp, misses, z_hat, s, s_inv, det, mat_mul(ph, s_inv)))
        return out

    def cost_matrix(self, pred, zs):
        """Rows: measurements. Columns: the n tracks, then m new-target and m false-alarm columns."""
        n, m = len(pred), len(zs)
        cost = [[INF] * (n + 2 * m) for _ in range(m)]
        for j, z in enumerate(zs):
            for i, (_, _, _, _, z_hat, s, s_inv, det, _) in enumerate(pred):
                nu = [[a - b] for a, b in zip(z, z_hat)]
                d2 = mat_mul(mat_mul(transpose(nu), s_inv), nu)[0][0]
                if d2 <= self.gamma:
                    dens = math.exp(-0.5 * d2) / math.sqrt((2 * math.pi) ** len(z) * det)
                    cost[j][i] = -math.log(self.p_d * dens / (1.0 - self.p_d))
            cost[j][n + j] = -math.log(self.beta_nt)
            cost[j][n + m + j] = -math.log(self.beta_ft)
        return cost

    def _child(self, pred, zs, row_to_col):
        h = self.model[2]
        n = len(pred)
        taken = {c: j for j, c in enumerate(row_to_col) if c < n}
        tracks, births = [], []
        for i, (tid, xp, pp, misses, z_hat, s, _, _, k) in enumerate(pred):
            if i in taken:
                z = zs[taken[i]]
                nu = [[a - b] for a, b in zip(z, z_hat)]
                x = mat_add(xp, mat_mul(k, nu))
                p = mat_sub(pp, mat_mul(mat_mul(k, s), transpose(k)))
                tracks.append((tid, x, p, 0))
            else:
                tracks.append((tid, xp, pp, misses + 1))
        for j, c in enumerate(row_to_col):
            if n <= c < n + len(zs):
                births.append(zs[j])
        return tracks, births

    def children_of(self, w, tracks, zs, k):
        """The k children of highest log weight of one hypothesis: (log weight, predicted tracks, assignment)."""
        pred = self._predict(tracks)  # @line L1
        cost = self.cost_matrix(pred, zs)  # @line L2
        out = []
        for total, row_to_col in murty_k_best(cost, k):  # @line L3
            lw = w + len(pred) * math.log(1.0 - self.p_d) - total  # @line L4
            out.append((lw, pred, row_to_col))
        return out

    def step(self, zs):
        """Process one frame. Returns {track id: (x, y)} of the best hypothesis."""
        children = []
        for w, tracks in self.hyps:
            children.extend(self.children_of(w, tracks, zs, self.m_best))
        children.sort(key=lambda c: -c[0])
        children = children[: self.m_best]  # @line L5
        top = children[0][0]
        norm = top + math.log(sum(math.exp(c[0] - top) for c in children))
        rr = self.model[3][0][0]
        new_hyps = []
        for lw, pred, row_to_col in children:
            tracks, births = self._child(pred, zs, row_to_col)
            tracks = [t for t in tracks if t[3] < self.max_misses]  # @line L6
            for z in births:
                tracks.append((self.next_id, [[z[0]], [z[1]], [0.0], [0.0]], [[rr, 0, 0, 0], [0, rr, 0, 0], [0, 0, self.p_vel, 0], [0, 0, 0, self.p_vel]], 0))
                self.next_id += 1
            new_hyps.append((lw - norm, tracks))
        self.hyps = new_hyps
        best = max(self.hyps, key=lambda h: h[0])  # @line L7
        return {t[0]: (t[1][0][0], t[1][1][0]) for t in best[1]}
