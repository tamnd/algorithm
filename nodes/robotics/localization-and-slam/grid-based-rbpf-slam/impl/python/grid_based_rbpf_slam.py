# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grid-based-rbpf-slam/. The authors are listed in prov/X1GN8F.jsonl.

"""Grid-based Rao-Blackwellized SLAM with an improved proposal, kept small.

After Grisetti, Stachniss and Burgard (2007). Each particle holds a pose, a
log-odds occupancy grid and a log weight. One step does, for each particle:
scan matching of the new scan in the grid of the particle, starting from the
odometry guess; K points around the match, each scored by the scan
likelihood times the motion density; a Gaussian fitted to these points, from
which the new pose is drawn; the weight times the sum of the scores; and the
update of the grid. Resampling happens only when N_eff < N/2.

This is a teaching version on a small planar grid. It has none of the speed
tricks of a real implementation (no shared map tree, no lookup tables, no
multi-resolution matching) and its scan likelihood is a simple endpoint model.

  Params                                     grid size, sensor and noise settings
  grid_rbpf_step(particles, u, ranges, rng, p)   one step, lines L1 to L9
  scan_match, scan_loglik, integrate_scan    the parts of the step
  World                                      a simulated room for the tests
"""

import math

import robest

LOG_2PI = math.log(2.0 * math.pi)


class Params:
    def __init__(
        self,
        width=60,
        height=40,
        res=0.1,
        beams=16,
        max_range=5.0,
        l_occ=0.9,
        l_free=-0.4,
        l_max=6.0,
        sigma_hit=0.1,
        search=1,
        motion_sd=(0.03, 0.02, 0.03),
        k_points=8,
        delta=(0.05, 0.05, 0.03),
        min_match=0.5,
        match_step=(0.1, 0.1, 0.05),
        match_levels=3,
    ):
        self.width, self.height, self.res = width, height, res
        self.angles = [2.0 * math.pi * k / beams for k in range(beams)]
        self.max_range = max_range
        self.l_occ, self.l_free, self.l_max = l_occ, l_free, l_max
        self.sigma_hit = sigma_hit
        self.search = search
        self.motion_sd = motion_sd
        self.k_points = k_points
        self.delta = delta
        self.min_match = min_match
        self.match_step = match_step
        self.match_levels = match_levels


# ---------------------------------------------------------------- poses and motion


def compose(x, d):
    """Return x (+) d: the pose d, given in the frame of x, in the world frame."""
    c, s = math.cos(x[2]), math.sin(x[2])
    return [x[0] + c * d[0] - s * d[1], x[1] + s * d[0] + c * d[1], robest.wrap_angle(x[2] + d[2])]


def relative(a, b):
    """Return a^(-1) (+) b: the pose b in the frame of a."""
    c, s = math.cos(a[2]), math.sin(a[2])
    dx, dy = b[0] - a[0], b[1] - a[1]
    return [c * dx + s * dy, -s * dx + c * dy, robest.wrap_angle(b[2] - a[2])]


def motion_logpdf(prev, x, u, sd):
    """Log density of x given prev and the odometry step u (in the frame of prev)."""
    d = relative(prev, x)
    e = [d[0] - u[0], d[1] - u[1], robest.wrap_angle(d[2] - u[2])]
    return sum(-0.5 * (e[i] / sd[i]) ** 2 - math.log(sd[i]) - 0.5 * LOG_2PI for i in range(3))


def sample_motion(rng, prev, u, sd):
    return compose(prev, [u[i] + sd[i] * rng.gauss(0.0, 1.0) for i in range(3)])


# ---------------------------------------------------------------- the grid


def new_grid(p):
    return [0.0] * (p.width * p.height)


def ray_cells(c0, c1):
    """Return the cells from c0 up to c1, c1 excluded, by Bresenham's line algorithm."""
    x0, y0 = c0
    x1, y1 = c1
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    out = []
    while (x0, y0) != (x1, y1):
        out.append((x0, y0))
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy
    return out


def integrate_scan(grid, p, pose, ranges):
    """Add the scan to the log-odds grid: free cells along each beam, occupied at a hit."""
    res, w, h = p.res, p.width, p.height
    c0 = (int(pose[0] // res), int(pose[1] // res))
    for a, r in zip(p.angles, ranges):
        hit = r < p.max_range
        r = min(r, p.max_range)
        ex = pose[0] + r * math.cos(pose[2] + a)
        ey = pose[1] + r * math.sin(pose[2] + a)
        c1 = (int(ex // res), int(ey // res))
        for cx, cy in ray_cells(c0, c1):
            if 0 <= cx < w and 0 <= cy < h:
                i = cy * w + cx
                grid[i] = max(-p.l_max, grid[i] + p.l_free)
        if hit and 0 <= c1[0] < w and 0 <= c1[1] < h:
            i = c1[1] * w + c1[0]
            grid[i] = min(p.l_max, grid[i] + p.l_occ)


def scan_loglik(grid, p, pose, ranges):
    """Return (log likelihood, matched beams) of the scan at pose, by an endpoint model.

    Each hit endpoint scores -d^2 / (2 sigma^2), where d is the distance to the
    center of the nearest occupied cell within `search` cells, or a cap if
    there is none. Constants that are the same for every pose are dropped.
    """
    res, w, h, s = p.res, p.width, p.height, p.search
    cap2 = ((s + 0.5) * res) ** 2
    inv = 0.5 / (p.sigma_hit * p.sigma_hit)
    x, y, th = pose
    total, matched = 0.0, 0
    for a, r in zip(p.angles, ranges):
        if r >= p.max_range:
            continue
        ex = x + r * math.cos(th + a)
        ey = y + r * math.sin(th + a)
        cx, cy = int(ex // res), int(ey // res)
        best = cap2
        for yy in range(cy - s, cy + s + 1):
            if not 0 <= yy < h:
                continue
            row = yy * w
            ddy = (yy + 0.5) * res - ey
            for xx in range(cx - s, cx + s + 1):
                if 0 <= xx < w and grid[row + xx] > 0.0:
                    ddx = (xx + 0.5) * res - ex
                    d2 = ddx * ddx + ddy * ddy
                    if d2 < best:
                        best = d2
        if best < cap2:
            matched += 1
        total -= best * inv
    return total, matched


def scan_match(grid, p, start, ranges):
    """Hill climbing on scan_loglik from start, halving the steps match_levels times."""
    best = list(start)
    score = scan_loglik(grid, p, best, ranges)[0]
    step = list(p.match_step)
    for _ in range(p.match_levels):
        improved = True
        while improved:
            improved = False
            for k in range(3):
                for sign in (1.0, -1.0):
                    cand = list(best)
                    cand[k] += sign * step[k]
                    cand[2] = robest.wrap_angle(cand[2])
                    s = scan_loglik(grid, p, cand, ranges)[0]
                    if s > score:
                        best, score, improved = cand, s, True
        step = [v / 2.0 for v in step]
    return best, score


def log_sum_exp(values):
    top = max(values)
    return top + math.log(sum(math.exp(v - top) for v in values))


def gaussian_from_points(points, logw, center):
    """Fit a Gaussian to weighted poses: return (mean, cov, log of the sum of weights).

    The angle is averaged as an offset from center, so the poses must lie
    near it. A floor of 1e-8 on the diagonal keeps the covariance positive.
    """
    log_eta = log_sum_exp(logw)
    wts = [math.exp(v - log_eta) for v in logw]
    offs = [[q[0] - center[0], q[1] - center[1], robest.wrap_angle(q[2] - center[2])] for q in points]
    m = [sum(wt * o[i] for wt, o in zip(wts, offs)) for i in range(3)]
    cov = [[sum(wt * (o[i] - m[i]) * (o[j] - m[j]) for wt, o in zip(wts, offs)) for j in range(3)] for i in range(3)]
    for i in range(3):
        cov[i][i] += 1e-8
    mean = [center[0] + m[0], center[1] + m[1], robest.wrap_angle(center[2] + m[2])]
    return mean, cov, log_eta


def improved_proposal(rng, grid, p, prev, u, ranges):
    """Draw the new pose of one particle. Return (pose, log weight factor)."""
    guess = compose(prev, u)  # @line L2
    best, _ = scan_match(grid, p, guess, ranges)  # @line L3
    hits = sum(1 for r in ranges if r < p.max_range)
    if scan_loglik(grid, p, best, ranges)[1] < p.min_match * hits:  # @line L4
        x = sample_motion(rng, prev, u, p.motion_sd)
        return x, scan_loglik(grid, p, x, ranges)[0]
    points, logt = [], []
    for _ in range(p.k_points):  # @line L5
        q = [best[i] + (2.0 * rng.random() - 1.0) * p.delta[i] for i in range(3)]
        q[2] = robest.wrap_angle(q[2])
        points.append(q)
        logt.append(scan_loglik(grid, p, q, ranges)[0] + motion_logpdf(prev, q, u, p.motion_sd))
    mean, cov, log_eta = gaussian_from_points(points, logt, best)
    volume = 8.0 * p.delta[0] * p.delta[1] * p.delta[2]
    x = robest.gauss_sample(rng, mean, cov)  # @line L6
    x[2] = robest.wrap_angle(x[2])
    return x, log_eta + math.log(volume / p.k_points)


# ---------------------------------------------------------------- the filter


class Particle:
    __slots__ = ("pose", "grid", "logw")

    def __init__(self, pose, grid, logw):
        self.pose, self.grid, self.logw = pose, grid, logw


def initial_particles(n, pose, ranges, p):
    """n particles at a known start pose, each with the first scan in its grid."""
    out = []
    for _ in range(n):
        g = new_grid(p)
        integrate_scan(g, p, pose, ranges)
        out.append(Particle(list(pose), g, -math.log(n)))
    return out


def n_eff(logws):
    """Return 1 / sum(w^2) of the normalized weights."""
    top = log_sum_exp(logws)
    return 1.0 / sum(math.exp(2.0 * (v - top)) for v in logws)


def prior_proposal(rng, grid, p, prev, u, ranges):
    """The plain proposal, for comparison: draw from the motion model, weight by the scan."""
    x = sample_motion(rng, prev, u, p.motion_sd)
    return x, scan_loglik(grid, p, x, ranges)[0]


def grid_rbpf_step(particles, u, ranges, rng, p, improved=True):
    """One step with the odometry step u and a scan. Return (particles, resampled)."""
    propose = improved_proposal if improved else prior_proposal
    for q in particles:  # @line L1
        q.pose, factor = propose(rng, q.grid, p, q.pose, u, ranges)
        q.logw += factor
        integrate_scan(q.grid, p, q.pose, ranges)  # @line L7
    top = log_sum_exp([q.logw for q in particles])
    for q in particles:
        q.logw -= top
    n = len(particles)
    if n_eff([q.logw for q in particles]) >= n / 2.0:  # @line L8
        return particles, False
    idx = robest.low_variance_resample(rng, [math.exp(q.logw) for q in particles])
    return [Particle(list(particles[i].pose), list(particles[i].grid), -math.log(n)) for i in idx], True  # @line L9


def best_particle(particles):
    return max(particles, key=lambda q: q.logw)


# ---------------------------------------------------------------- a simulated room


class World:
    """A rectangular room with walls on the border cells and one box inside."""

    def __init__(self, p, box=(26, 16, 34, 24)):
        self.p = p
        self.occ = [False] * (p.width * p.height)
        for cy in range(p.height):
            for cx in range(p.width):
                border = cx in (0, p.width - 1) or cy in (0, p.height - 1)
                inside = box[0] <= cx < box[2] and box[1] <= cy < box[3]
                if border or inside:
                    self.occ[cy * p.width + cx] = True

    def occupied(self, cx, cy):
        p = self.p
        return not (0 <= cx < p.width and 0 <= cy < p.height) or self.occ[cy * p.width + cx]

    def scan(self, pose, rng=None, sd=0.0):
        """Ray cast each beam in steps of a quarter cell; add N(0, sd^2) noise to hits."""
        p = self.p
        step = p.res / 4.0
        out = []
        for a in p.angles:
            c, s = math.cos(pose[2] + a), math.sin(pose[2] + a)
            r = 0.0
            while r < p.max_range:
                if self.occupied(int((pose[0] + r * c) // p.res), int((pose[1] + r * s) // p.res)):
                    break
                r += step
            if r < p.max_range and rng is not None:
                r = max(0.0, r + sd * rng.gauss(0.0, 1.0))
            out.append(min(r, p.max_range))
        return out
