# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lidar-odometry-and-mapping/. The authors are listed in prov/GTC8AH.jsonl.

"""A planar toy of LOAM, the lidar odometry and mapping of Zhang and Singh.

This is a toy. The lidar is a 2D scanner, the scans are taken at one instant
(there is no motion distortion to remove), and the map is a flat list of
points in a hash grid. What the toy keeps from LOAM:

  - the smoothness value c of each point, from the points next to it on the
    same scan line, and the choice of sharp points (large c) and flat points
    (small c) in each sector, with points at depth jumps left out,
  - odometry at every scan: match the sharp and flat points of the new scan
    to the feature points of the previous scan and solve for the motion by
    Gauss-Newton with bisquare weights,
  - mapping at a lower rate: match the features to the map, with a line
    fitted to the nearby map points by an eigenvector, refine the pose, and
    add the features to the map.

What the toy leaves out: the 3D scan lines, the removal of the motion
distortion inside a sweep, the less sharp points, Levenberg-Marquardt, and the
cube of map points around the sensor.

In 3D, LOAM matches an edge point to a line and a planar point to a plane.
In the plane, a wall is a line and a corner is a point, so a flat point is
matched to a line and a sharp point to a point.
"""

import math

# ------------------------------------------------------------- planar poses


def wrap(a):
    return (a + math.pi) % (2.0 * math.pi) - math.pi


def compose(a, b):
    c, s = math.cos(a[2]), math.sin(a[2])
    return (a[0] + c * b[0] - s * b[1], a[1] + s * b[0] + c * b[1], wrap(a[2] + b[2]))


def inverse(a):
    c, s = math.cos(a[2]), math.sin(a[2])
    return (-c * a[0] - s * a[1], s * a[0] - c * a[1], -a[2])


def transform(pose, p):
    c, s = math.cos(pose[2]), math.sin(pose[2])
    return (pose[0] + c * p[0] - s * p[1], pose[1] + s * p[0] + c * p[1])


# ------------------------------------------------------------- features


def smoothness(points, i, k):
    """LOAM's c: |sum over the 2k neighbors j of (X_i - X_j)| / (2k |X_i|)."""
    n = len(points)
    xi, yi = points[i]
    sx = sy = 0.0
    for d in range(-k, k + 1):
        if d:
            xj, yj = points[(i + d) % n]
            sx += xi - xj
            sy += yi - yj
    return math.hypot(sx, sy) / (2 * k * math.hypot(xi, yi))


def reliable_points(points, k, jump):
    """ok[i] is False if the range jumps by more than the fraction `jump`
    between two consecutive beams within k + 1 beams of beam i.

    Such points lie at the edge of an occluded region, or next to it, and
    LOAM does not take them as features.
    """
    n = len(points)
    r = [math.hypot(x, y) for x, y in points]
    smooth = [abs(r[(a + 1) % n] - r[a]) <= jump * min(r[(a + 1) % n], r[a]) for a in range(n)]
    return [all(smooth[(i + d) % n] for d in range(-k - 1, k + 1)) for i in range(n)]


def extract_features(points, k=5, sectors=6, n_sharp=2, n_flat=8, c_edge=0.05, c_flat=0.01, jump=0.1):
    """Return (sharp, flat, less_flat) as lists of point indices.

    In each sector, the sharp points are the points with the largest c above
    c_edge and the flat points are the points with the smallest c below c_flat.
    A chosen point blocks its k neighbors on each side, so the features spread
    out. less_flat holds every reliable point with c below c_flat.
    """
    n = len(points)
    c = [smoothness(points, i, k) for i in range(n)]  # @line L1
    ok = reliable_points(points, k, jump)
    sharp, flat, less_flat = [], [], []
    taken = set()
    for s in range(sectors):
        idx = [i for i in range(s * n // sectors, (s + 1) * n // sectors) if ok[i]]
        got = 0
        for i in sorted(idx, key=lambda i: -c[i]):
            if c[i] <= c_edge or got == n_sharp:
                break
            if i not in taken:
                sharp.append(i)
                got += 1
                taken.update((i + d) % n for d in range(-k, k + 1))
        got = 0
        for i in sorted(idx, key=lambda i: c[i]):
            if c[i] >= c_flat or got == n_flat:
                break
            if i not in taken:
                flat.append(i)
                got += 1
                taken.update((i + d) % n for d in range(-k, k + 1))
        less_flat.extend(i for i in idx if c[i] < c_flat)  # @line L2
    return sorted(sharp), sorted(flat), less_flat


# ------------------------------------------------------------- neighbor search


class Grid:
    """Points in a hash grid with square cells, for nearest neighbor queries."""

    def __init__(self, points, cell=0.5):
        self.cell = cell
        self.points = list(points)
        self.cells = {}
        for idx, p in enumerate(self.points):
            self.cells.setdefault(self._key(p), []).append(idx)

    def _key(self, p):
        return (math.floor(p[0] / self.cell), math.floor(p[1] / self.cell))

    def near(self, q, radius):
        """Indices of the points within `radius` of q, nearest first."""
        cx, cy = self._key(q)
        r = int(math.ceil(radius / self.cell))
        found = []
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                for idx in self.cells.get((cx + dx, cy + dy), ()):
                    p = self.points[idx]
                    d = math.hypot(p[0] - q[0], p[1] - q[1])
                    if d <= radius:
                        found.append((d, idx))
        found.sort()
        return [idx for _, idx in found]


# ------------------------------------------------------------- residuals


def point_residual(pose, p, target):
    """Sharp point: q - target, two rows, with the Jacobian in (tx, ty, theta)."""
    q = transform(pose, p)
    c, s = math.cos(pose[2]), math.sin(pose[2])
    dqx, dqy = -s * p[0] - c * p[1], c * p[0] - s * p[1]
    return [q[0] - target[0], q[1] - target[1]], [[1.0, 0.0, dqx], [0.0, 1.0, dqy]]


def line_residual(pose, p, a, normal):
    """Flat point: signed distance n . (q - a) to a line, with its Jacobian."""
    q = transform(pose, p)
    c, s = math.cos(pose[2]), math.sin(pose[2])
    dqx, dqy = -s * p[0] - c * p[1], c * p[0] - s * p[1]
    r = normal[0] * (q[0] - a[0]) + normal[1] * (q[1] - a[1])
    return [r], [[normal[0], normal[1], normal[0] * dqx + normal[1] * dqy]]


def bisquare(d, tau):
    return (1.0 - (d / tau) ** 2) ** 2 if abs(d) < tau else 0.0


def solve3(h, g):
    """Solve a 3 x 3 system by Gaussian elimination with partial pivoting."""
    m = [list(h[i]) + [g[i]] for i in range(3)]
    for col in range(3):
        piv = max(range(col, 3), key=lambda r: abs(m[r][col]))
        if abs(m[piv][col]) < 1e-12:
            raise ValueError("degenerate: the features do not fix the motion")
        m[col], m[piv] = m[piv], m[col]
        for r in range(col + 1, 3):
            f = m[r][col] / m[col][col]
            for c in range(col, 4):
                m[r][c] -= f * m[col][c]
    x = [0.0] * 3
    for r in (2, 1, 0):
        x[r] = (m[r][3] - sum(m[r][c] * x[c] for c in range(r + 1, 3))) / m[r][r]
    return x


def gauss_newton(pose, make_terms, iterations=20, tau=0.3, tol=1e-6):
    """Minimize the sum of bisquare-weighted squared residuals over the pose.

    make_terms(pose) returns (residual rows, Jacobian rows, distance) per match;
    the matches are found again at every iteration.
    """
    for _ in range(iterations):
        h = [[0.0] * 3 for _ in range(3)]
        g = [0.0] * 3
        used = 0
        for rows, jac, dist in make_terms(pose):
            w = bisquare(dist, tau)
            if w == 0.0:
                continue
            used += 1
            for r, jr in zip(rows, jac):
                for a in range(3):
                    g[a] -= w * jr[a] * r
                    for b in range(3):
                        h[a][b] += w * jr[a] * jr[b]
        if used < 3:
            raise ValueError("too few matches")
        dx = solve3(h, g)  # @line L7
        pose = (pose[0] + dx[0], pose[1] + dx[1], wrap(pose[2] + dx[2]))
        if max(abs(v) for v in dx) < tol:  # @line L8
            break
    return pose


# ------------------------------------------------------------- matching


def line_through(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    norm = math.hypot(dx, dy)
    return (-dy / norm, dx / norm)


def scan_to_scan_terms(cur, sharp, flat, prev, prev_sharp, prev_less_flat, radius=1.0, sharp_radius=0.5):
    """Matches of the new features to the feature points of the previous scan.

    A flat point is matched to the line through the nearest less flat point a
    of the previous scan and the nearest less flat point b that is at most 3
    beams away from a. A sharp point is matched to the nearest sharp point.
    """
    flat_grid = Grid([prev[i] for i in prev_less_flat])
    sharp_grid = Grid([prev[i] for i in prev_sharp])

    def terms(pose):
        out = []
        for i in flat:
            near = flat_grid.near(transform(pose, cur[i]), radius)
            if not near:
                continue
            a_idx = prev_less_flat[near[0]]
            b_idx = next((prev_less_flat[m] for m in near[1:] if 0 < abs(prev_less_flat[m] - a_idx) <= 3), None)
            if b_idx is None:
                continue
            a = prev[a_idx]
            rows, jac = line_residual(pose, cur[i], a, line_through(a, prev[b_idx]))  # @line L5
            out.append((rows, jac, abs(rows[0])))
        for i in sharp:
            near = sharp_grid.near(transform(pose, cur[i]), sharp_radius)
            if near:
                rows, jac = point_residual(pose, cur[i], sharp_grid.points[near[0]])  # @line L6
                out.append((rows, jac, math.hypot(*rows)))
        return out

    return terms


def fit_line(points):
    """Mean and unit direction of the largest spread, and the two eigenvalues."""
    n = len(points)
    mx = sum(p[0] for p in points) / n
    my = sum(p[1] for p in points) / n
    sxx = sum((p[0] - mx) ** 2 for p in points) / n
    syy = sum((p[1] - my) ** 2 for p in points) / n
    sxy = sum((p[0] - mx) * (p[1] - my) for p in points) / n
    half = math.hypot((sxx - syy) / 2.0, sxy)
    big, small = (sxx + syy) / 2.0 + half, (sxx + syy) / 2.0 - half
    angle = 0.5 * math.atan2(2.0 * sxy, sxx - syy)
    return (mx, my), (math.cos(angle), math.sin(angle)), big, small


def scan_to_map_terms(cur, sharp, flat, map_sharp, map_flat, radius=1.0, sharp_radius=0.5, count=5, line_ratio=0.01):
    """Matches of the features to the map.

    A flat point is matched to the line fitted to its `count` nearest map flat
    points, if their spread is long and thin. A sharp point is matched to the
    mean of the map sharp points within 0.2 of the nearest one.
    """
    flat_grid = Grid(map_flat)
    sharp_grid = Grid(map_sharp)

    def terms(pose):
        out = []
        for i in flat:
            near = flat_grid.near(transform(pose, cur[i]), radius)[:count]
            if len(near) < count:
                continue
            mean, d, big, small = fit_line([flat_grid.points[m] for m in near])
            if small > line_ratio * big:  # the points do not lie on a line
                continue
            rows, jac = line_residual(pose, cur[i], mean, (-d[1], d[0]))
            out.append((rows, jac, abs(rows[0])))
        for i in sharp:
            near = sharp_grid.near(transform(pose, cur[i]), sharp_radius)
            if not near:
                continue
            pts = [sharp_grid.points[m] for m in sharp_grid.near(sharp_grid.points[near[0]], 0.2)]
            mean = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
            rows, jac = point_residual(pose, cur[i], mean)
            out.append((rows, jac, math.hypot(*rows)))
        return out

    return terms


# ------------------------------------------------------------- the toy system


def voxel_filter(points, cell):
    seen = {}
    for p in points:
        seen.setdefault((math.floor(p[0] / cell), math.floor(p[1] / cell)), p)
    return list(seen.values())


class ToyLoam:
    """Odometry at every scan and mapping at every `map_every`-th scan.

    Poses are relative to the pose of the first scan. `odom_path` is the chain
    of odometry motions alone. `path` is the output: the last mapped pose
    composed with the odometry motions since then.
    """

    def __init__(self, map_every=5, voxel=0.1):
        self.map_every = map_every
        self.voxel = voxel
        self.prev = None
        self.motion = (0.0, 0.0, 0.0)
        self.odom_pose = (0.0, 0.0, 0.0)
        self.pose = (0.0, 0.0, 0.0)
        self.map_sharp = []
        self.map_flat = []
        self.count = 0
        self.odom_path = []
        self.path = []

    def _add_to_map(self, pose, scan, sharp, less_flat):
        self.map_sharp = voxel_filter(self.map_sharp + [transform(pose, scan[i]) for i in sharp], self.voxel)
        self.map_flat = voxel_filter(self.map_flat + [transform(pose, scan[i]) for i in less_flat], self.voxel)

    def add_scan(self, scan):
        """Process one scan (points in the sensor frame, in beam order). Return the pose."""
        sharp, flat, less_flat = extract_features(scan)
        if self.prev is None:  # @line L3
            self._add_to_map(self.pose, scan, sharp, less_flat)
        else:
            prev, p_sharp, p_less_flat = self.prev
            terms = scan_to_scan_terms(scan, sharp, flat, prev, p_sharp, p_less_flat)
            self.motion = gauss_newton(self.motion, terms)  # @line L4
            self.odom_pose = compose(self.odom_pose, self.motion)
            self.pose = compose(self.pose, self.motion)
            self.count += 1
            if self.count % self.map_every == 0:
                terms = scan_to_map_terms(scan, sharp, less_flat, self.map_sharp, self.map_flat)
                self.pose = gauss_newton(self.pose, terms)  # @line L9
                self._add_to_map(self.pose, scan, sharp, less_flat)  # @line L10
        self.odom_path.append(self.odom_pose)
        self.path.append(self.pose)
        self.prev = (scan, sharp, less_flat)
        return self.pose
