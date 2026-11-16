# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semi-direct-visual-odometry/. The authors are listed in prov/BR51JE.jsonl.
"""Semi-direct visual odometry (Forster, Pizzoli and Scaramuzza, ICRA 2014),
small form.

Motion thread, for each new frame:
1. Sparse model-based image alignment: the relative pose to the previous
   frame minimizes the photometric error of 4 x 4 patches around the
   projected map points, by inverse compositional Gauss-Newton, coarse to
   fine.
2. Feature alignment (relaxation): each visible map point gets a 2D
   position by aligning an affinely warped 8 x 8 patch of a keyframe with
   the new frame. This step breaks the epipolar constraints on purpose.
3. Motion-only bundle adjustment: Gauss-Newton on the pose with the
   reprojection errors of the aligned positions.
4. Structure-only bundle adjustment: Gauss-Newton on each point.

Mapping: a seed (a pixel of a keyframe) has a depth filter on its inverse
depth with the Gaussian times Beta model of Vogiatzis and Hernandez. Each
new frame gives one measurement by a search along the epipolar line. A
converged seed becomes a map point. A new keyframe is made when the frame is
far from all keyframes compared with the mean scene depth.

What is left out: the homography bootstrap (the caller gives the depths of
the first frame), FAST corners (a Shi-Tomasi score per cell is used), the
robust weights, the brightness offset in sparse alignment, and the
threads. Images are objects with sample(u, v) -> (value, d/du, d/dv) or
None near the border. Poses map world points into the camera: X_c = R X + t.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

from cvla import cross, dot, eye, matvec, mul, norm, skew, solve, transpose

Matrix = List[List[float]]
Vector = List[float]
Pose = Tuple[Matrix, Vector]

PATCH4 = [(du - 1.5, dv - 1.5) for dv in range(4) for du in range(4)]
PATCH8 = [(du - 3.5, dv - 3.5) for dv in range(8) for du in range(8)]


# ------------------------------------------------------------------ images

class GridImage:
    """A gray image img[v][u], read with bilinear interpolation of the values
    and of central-difference gradients. None within one pixel of the border."""

    def __init__(self, rows: Sequence[Sequence[float]]):
        self.h, self.w = len(rows), len(rows[0])
        self.val = [[float(x) for x in row] for row in rows]
        self.gx = [[0.0] * self.w for _ in range(self.h)]
        self.gy = [[0.0] * self.w for _ in range(self.h)]
        for v in range(1, self.h - 1):
            for u in range(1, self.w - 1):
                self.gx[v][u] = 0.5 * (self.val[v][u + 1] - self.val[v][u - 1])
                self.gy[v][u] = 0.5 * (self.val[v + 1][u] - self.val[v - 1][u])

    def sample(self, u: float, v: float) -> Optional[Tuple[float, float, float]]:
        if not (1.0 <= u <= self.w - 2.0 and 1.0 <= v <= self.h - 2.0):
            return None
        u0, v0 = min(int(u), self.w - 3), min(int(v), self.h - 3)
        fu, fv = u - u0, v - v0
        w00, w01, w10, w11 = (1 - fu) * (1 - fv), fu * (1 - fv), (1 - fu) * fv, fu * fv
        out = []
        for a in (self.val, self.gx, self.gy):
            out.append(w00 * a[v0][u0] + w01 * a[v0][u0 + 1] + w10 * a[v0 + 1][u0] + w11 * a[v0 + 1][u0 + 1])
        return out[0], out[1], out[2]

    def half(self) -> "GridImage":
        return GridImage([[0.25 * (self.val[2 * v][2 * u] + self.val[2 * v][2 * u + 1] +
                                   self.val[2 * v + 1][2 * u] + self.val[2 * v + 1][2 * u + 1])
                           for u in range(self.w // 2)] for v in range(self.h // 2)])


def pyramid(img: GridImage, levels: int) -> List[GridImage]:
    out = [img]
    for _ in range(levels - 1):
        out.append(out[-1].half())
    return out


def level_K(K: Sequence[float], level: int) -> Tuple[float, float, float, float]:
    """(fx, fy, cx, cy) at a pyramid level made by 2 x 2 means."""
    fx, fy, cx, cy = K
    for _ in range(level):
        fx, fy, cx, cy = fx / 2.0, fy / 2.0, (cx - 0.5) / 2.0, (cy - 0.5) / 2.0
    return fx, fy, cx, cy


# ------------------------------------------------------------ rigid motion

def so3_exp(w: Sequence[float]) -> Matrix:
    th = norm(w)
    k = skew(w)
    kk = mul(k, k)
    if th < 1e-12:
        a, b = 1.0, 0.5
    else:
        a, b = math.sin(th) / th, (1.0 - math.cos(th)) / (th * th)
    i3 = eye(3)
    return [[i3[r][c] + a * k[r][c] + b * kk[r][c] for c in range(3)] for r in range(3)]


def transform(pose: Pose, X: Sequence[float]) -> Vector:
    R, t = pose
    return [R[r][0] * X[0] + R[r][1] * X[1] + R[r][2] * X[2] + t[r] for r in range(3)]


def compose(a: Pose, b: Pose) -> Pose:
    """a after b."""
    return mul(a[0], b[0]), [x + y for x, y in zip(matvec(a[0], b[1]), a[1])]


def inverse(p: Pose) -> Pose:
    Rt = transpose(p[0])
    return Rt, [-x for x in matvec(Rt, p[1])]


def increment(delta: Sequence[float]) -> Pose:
    """The small motion X -> exp(w) X + v for delta = (w, v)."""
    return so3_exp(delta[:3]), list(delta[3:6])


def center(pose: Pose) -> Vector:
    return [-x for x in matvec(transpose(pose[0]), pose[1])]


def project(K, Xc: Sequence[float]) -> Optional[Tuple[float, float]]:
    if Xc[2] <= 1e-9:
        return None
    fx, fy, cx, cy = K
    return fx * Xc[0] / Xc[2] + cx, fy * Xc[1] / Xc[2] + cy


def backproject(K, u: float, v: float, z: float) -> Vector:
    fx, fy, cx, cy = K
    return [(u - cx) / fx * z, (v - cy) / fy * z, z]


def proj_jacobian(K, Xc: Sequence[float]) -> Tuple[Vector, Vector]:
    """Rows of d pi / d X_c."""
    fx, fy = K[0], K[1]
    z = Xc[2]
    return [fx / z, 0.0, -fx * Xc[0] / (z * z)], [0.0, fy / z, -fy * Xc[1] / (z * z)]


def point_motion_rows(X: Sequence[float]) -> List[Vector]:
    """d(exp(w) X + v)/d(w, v) at 0: [-[X]_x | I], as 3 rows of 6."""
    s = skew(X)
    return [[-s[r][0], -s[r][1], -s[r][2]] + [1.0 if c == r else 0.0 for c in range(3)] for r in range(3)]


# ------------------------------------------- 1. sparse image alignment

def sparse_alignment_setup(ref_img, K, feats):
    """The fixed data of inverse compositional alignment at one level: for
    each patch pixel the 3D point in the reference camera (all pixels of a
    patch take the depth of its feature), the reference value and the
    Jacobian row with respect to a motion of the reference point."""
    rows = []
    for (u, v, z) in feats:
        for o in PATCH4:
            q = (u + o[0], v + o[1])
            s = ref_img.sample(q[0], q[1])
            if s is None:
                continue
            X = backproject(K, q[0], q[1], z)
            gu, gv = proj_jacobian(K, X)
            gX = [s[1] * gu[k] + s[2] * gv[k] for k in range(3)]
            M = point_motion_rows(X)
            J = [sum(gX[r] * M[r][c] for r in range(3)) for c in range(6)]
            rows.append((X, s[0], J))
    return rows


def sparse_image_alignment(ref_pyr, cur_pyr, K, feats, init: Pose, min_level: int = 0, iters: int = 30):
    """The relative pose T (reference camera -> current camera) that
    minimizes sum (I_cur(pi(T X)) - I_ref(u))^2 over the 4 x 4 patches.
    feats are (u, v, depth) at level 0 of the reference. Inverse
    compositional: the Jacobian and H come from the reference image and are
    computed once per level; the update is T <- T exp(xi)^-1."""
    T = init
    for lev in range(len(cur_pyr) - 1, min_level - 1, -1):
        Kl = level_K(K, lev)
        f = 0.5 ** lev
        lf = [((u + 0.5) * f - 0.5, (v + 0.5) * f - 0.5, z) for (u, v, z) in feats]
        rows = sparse_alignment_setup(ref_pyr[lev], Kl, lf)

        def residuals(Tc):
            out = []
            for X, iref, J in rows:
                p = project(Kl, transform(Tc, X))
                s = cur_pyr[lev].sample(p[0], p[1]) if p else None
                out.append(None if s is None else s[0] - iref)
            return out

        def cost(rs):
            vals = [r for r in rs if r is not None]
            return sum(r * r for r in vals) / max(1, len(vals))

        rs = residuals(T)
        c0 = cost(rs)
        for _ in range(iters):
            H = [[0.0] * 6 for _ in range(6)]
            g = [0.0] * 6
            for (X, iref, J), r in zip(rows, rs):
                if r is None:
                    continue
                for a in range(6):
                    g[a] += J[a] * r
                    for b in range(6):
                        H[a][b] += J[a] * J[b]
            try:
                xi = solve(H, g)
            except ValueError:
                break
            cand = compose(T, inverse(increment(xi)))
            rs1 = residuals(cand)
            c1 = cost(rs1)
            if not c1 < c0:
                break
            T, rs, c0 = cand, rs1, c1
            if norm(xi) < 1e-12:
                break
    return T


# ---------------------------------------------------- 2. feature alignment

def affine_warp(K, ref_pose: Pose, cur_pose: Pose, u: Sequence[float], z: float, h: float = 2.0) -> Matrix:
    """The 2 x 2 matrix A that maps a small offset of pixel u in the
    reference keyframe to the offset in the current frame, for a patch on a
    plane parallel to the reference image at depth z (finite differences of
    the exact warp with step h)."""
    rel = compose(cur_pose, inverse(ref_pose))

    def warp(du, dv):
        return project(K, transform(rel, backproject(K, u[0] + du, u[1] + dv, z)))
    pu1, pu0, pv1, pv0 = warp(h, 0), warp(-h, 0), warp(0, h), warp(0, -h)
    return [[(pu1[0] - pu0[0]) / (2 * h), (pv1[0] - pv0[0]) / (2 * h)],
            [(pu1[1] - pu0[1]) / (2 * h), (pv1[1] - pv0[1]) / (2 * h)]]


def feature_alignment(cur_img, ref_img, u_ref: Sequence[float], A: Matrix, u0: Sequence[float],
                      iters: int = 20) -> Optional[Tuple[Tuple[float, float], float]]:
    """Gauss-Newton on (u, v, beta) for sum (I_cur(u + A o) - I_ref(u_ref + o) - beta)^2
    over the 8 x 8 patch. Returns the position and the RMS residual, or None."""
    ref = []
    for o in PATCH8:
        s = ref_img.sample(u_ref[0] + o[0], u_ref[1] + o[1])
        if s is None:
            return None
        ref.append((A[0][0] * o[0] + A[0][1] * o[1], A[1][0] * o[0] + A[1][1] * o[1], s[0]))

    def evaluate(p, with_j):
        out = []
        for du, dv, iv in ref:
            s = cur_img.sample(p[0] + du, p[1] + dv)
            if s is None:
                return None
            out.append((s[0] - iv - p[2], s[1], s[2]) if with_j else s[0] - iv - p[2])
        return out

    p = [u0[0], u0[1], 0.0]
    res = evaluate(p, True)
    if res is None:
        return None
    c0 = sum(r[0] ** 2 for r in res)
    for _ in range(iters):
        H = [[0.0] * 3 for _ in range(3)]
        g = [0.0] * 3
        for r, gx, gy in res:
            J = (gx, gy, -1.0)
            for a in range(3):
                g[a] -= J[a] * r
                for b in range(3):
                    H[a][b] += J[a] * J[b]
        try:
            step = solve(H, g)
        except ValueError:
            break
        cand = [p[k] + step[k] for k in range(3)]
        r1 = evaluate(cand, True)
        if r1 is None:
            break
        c1 = sum(r[0] ** 2 for r in r1)
        if not c1 < c0:
            break
        p, res, c0 = cand, r1, c1
        if norm(step) < 1e-12:
            break
    return (p[0], p[1]), math.sqrt(c0 / len(ref))


# ------------------------------------------- 3 and 4. bundle adjustment steps

def reprojection(K, pose: Pose, X, u) -> Optional[Vector]:
    p = project(K, transform(pose, X))
    return None if p is None else [p[0] - u[0], p[1] - u[1]]


def motion_only_ba(K, pose: Pose, obs, iters: int = 10) -> Tuple[Pose, List[float]]:
    """Gauss-Newton on the pose, with left updates, for the reprojection
    errors of obs = [(X world, u)]. A step is kept only if the cost goes
    down. Returns the pose and the costs of the kept steps."""
    def cost(p):
        s = 0.0
        for X, u in obs:
            e = reprojection(K, p, X, u)
            s += 1e18 if e is None else e[0] ** 2 + e[1] ** 2
        return s
    hist = [cost(pose)]
    for _ in range(iters):
        H = [[0.0] * 6 for _ in range(6)]
        g = [0.0] * 6
        for X, u in obs:
            Xc = transform(pose, X)
            e = reprojection(K, pose, X, u)
            gu, gv = proj_jacobian(K, Xc)
            M = point_motion_rows(Xc)
            for row, ei in ((gu, e[0]), (gv, e[1])):
                J = [sum(row[r] * M[r][c] for r in range(3)) for c in range(6)]
                for a in range(6):
                    g[a] -= J[a] * ei
                    for b in range(6):
                        H[a][b] += J[a] * J[b]
        try:
            step = solve(H, g)
        except ValueError:
            break
        cand = compose(increment(step), pose)
        c = cost(cand)
        if not c < hist[-1]:
            break
        pose = cand
        hist.append(c)
    return pose, hist


def structure_only_ba(K, X: Sequence[float], obs, iters: int = 5) -> Vector:
    """Gauss-Newton on one point for its observations [(pose, u)]."""
    X = list(X)

    def cost(P):
        s = 0.0
        for pose, u in obs:
            e = reprojection(K, pose, P, u)
            s += 1e18 if e is None else e[0] ** 2 + e[1] ** 2
        return s
    c0 = cost(X)
    for _ in range(iters):
        H = [[0.0] * 3 for _ in range(3)]
        g = [0.0] * 3
        for pose, u in obs:
            e = reprojection(K, pose, X, u)
            gu, gv = proj_jacobian(K, transform(pose, X))
            for row, ei in ((gu, e[0]), (gv, e[1])):
                J = [sum(row[r] * pose[0][r][c] for r in range(3)) for c in range(3)]
                for a in range(3):
                    g[a] -= J[a] * ei
                    for b in range(3):
                        H[a][b] += J[a] * J[b]
        try:
            step = solve(H, g)
        except ValueError:
            break
        cand = [X[k] + step[k] for k in range(3)]
        c1 = cost(cand)
        if not c1 < c0:
            break
        X, c0 = cand, c1
    return X


# ------------------------------------------------------------ depth filter

def gauss_pdf(x: float, mu: float, s: float) -> float:
    return math.exp(-0.5 * ((x - mu) / s) ** 2) / (s * math.sqrt(2.0 * math.pi))


class Seed:
    """The posterior of the inverse depth Z and the inlier ratio pi of one
    pixel, approximated by N(Z | mu, sigma2) Beta(pi | a, b)."""

    def __init__(self, kf: int, u: float, v: float, mu: float, z_range: float, a: float = 10.0, b: float = 10.0):
        self.kf, self.u, self.v = kf, u, v
        self.mu, self.sigma2, self.a, self.b = mu, z_range * z_range / 36.0, a, b
        self.z_range = z_range

    def update(self, x: float, tau2: float) -> None:
        """One measurement x with variance tau2, from the model
        pi N(x | Z, tau2) + (1 - pi) U(x). The new parameters match the first
        and second moments of Z and of pi under the exact posterior."""
        a, b, mu, s2 = self.a, self.b, self.mu, self.sigma2
        sn = 1.0 / (1.0 / s2 + 1.0 / tau2)
        m = sn * (mu / s2 + x / tau2)
        c1 = a / (a + b) * gauss_pdf(x, mu, math.sqrt(s2 + tau2))
        c2 = b / (a + b) / self.z_range
        c1, c2 = c1 / (c1 + c2), c2 / (c1 + c2)
        f = c1 * (a + 1.0) / (a + b + 1.0) + c2 * a / (a + b + 1.0)
        e = (c1 * (a + 1.0) * (a + 2.0) / ((a + b + 1.0) * (a + b + 2.0))
             + c2 * a * (a + 1.0) / ((a + b + 1.0) * (a + b + 2.0)))
        mu_new = c1 * m + c2 * mu
        self.sigma2 = c1 * (sn + m * m) + c2 * (s2 + mu * mu) - mu_new * mu_new
        self.mu = mu_new
        self.a = (e - f) / (f - e / f)
        self.b = self.a * (1.0 - f) / f


def depth_along_ray(f_ref: Sequence[float], f_cur: Sequence[float], rel: Pose) -> float:
    """The depth z of the reference point z f_ref (f with third entry 1)
    whose image in the current camera lies along f_cur: least squares on
    (R z f_ref + t) x f_cur = 0."""
    a = cross(matvec(rel[0], f_ref), f_cur)
    c = cross(rel[1], f_cur)
    return -dot(a, c) / dot(a, a)


def epipolar_measurement(K, ref_img, cur_img, ref_pose: Pose, cur_pose: Pose, seed: Seed, steps: int = 25,
                         px_sigma: float = 1.0):
    """Search the inverse depths in mu +- 2 sigma for the best zero-mean SSD of
    an 8 x 8 patch, refine the position by feature alignment, and
    triangulate. Returns (inverse depth, tau2) or None. tau is the change of
    the inverse depth for px_sigma pixels of error along the epipolar line."""
    rel = compose(cur_pose, inverse(ref_pose))
    sig = math.sqrt(seed.sigma2)
    lo, hi = max(1e-3, seed.mu - 2.0 * sig), seed.mu + 2.0 * sig
    ref = []
    for o in PATCH8:
        s = ref_img.sample(seed.u + o[0], seed.v + o[1])
        if s is None:
            return None
        ref.append(s[0])
    mref = sum(ref) / len(ref)
    best, best_c = None, math.inf
    for k in range(steps):
        x = lo + (hi - lo) * k / (steps - 1)
        p = project(K, transform(rel, backproject(K, seed.u, seed.v, 1.0 / x)))
        if p is None:
            continue
        vals = []
        for o in PATCH8:
            s = cur_img.sample(p[0] + o[0], p[1] + o[1])
            if s is None:
                break
            vals.append(s[0])
        if len(vals) < len(PATCH8):
            continue
        mv = sum(vals) / len(vals)
        c = sum((q - mv - r + mref) ** 2 for q, r in zip(vals, ref))
        if c < best_c:
            best, best_c = (x, p), c
    if best is None:
        return None
    x, p = best
    A = affine_warp(K, ref_pose, cur_pose, (seed.u, seed.v), 1.0 / x)
    got = feature_alignment(cur_img, ref_img, (seed.u, seed.v), A, p)
    if got is None:
        return None
    q = got[0]
    fx, fy, cx, cy = K
    f_ref = [(seed.u - cx) / fx, (seed.v - cy) / fy, 1.0]
    z = depth_along_ray(f_ref, [(q[0] - cx) / fx, (q[1] - cy) / fy, 1.0], rel)
    if z <= 0:
        return None
    # one pixel along the epipolar direction
    p_far = project(K, transform(rel, backproject(K, seed.u, seed.v, 1e6)))
    d = [q[0] - p_far[0], q[1] - p_far[1]] if p_far else [1.0, 0.0]
    nd = math.hypot(d[0], d[1]) or 1.0
    q1 = (q[0] + px_sigma * d[0] / nd, q[1] + px_sigma * d[1] / nd)
    z1 = depth_along_ray(f_ref, [(q1[0] - cx) / fx, (q1[1] - cy) / fy, 1.0], rel)
    tau = abs(1.0 / z - 1.0 / z1) if z1 > 0 else 1.0 / z
    return 1.0 / z, tau * tau


# -------------------------------------------------------- feature selection

def shi_tomasi_cells(img: GridImage, cell: int, min_score: float, margin: int = 5,
                     taken: Sequence[Tuple[float, float]] = ()) -> List[Tuple[int, int]]:
    """In each cell of size cell, the pixel with the highest Shi-Tomasi score
    (the smaller eigenvalue of the 3 x 3 structure tensor), if it is above
    min_score. Cells that already hold a point of taken are skipped."""
    busy = {(int(u) // cell, int(v) // cell) for u, v in taken}
    best: Dict[Tuple[int, int], Tuple[float, int, int]] = {}
    for v in range(margin, img.h - margin):
        for u in range(margin, img.w - margin):
            key = (u // cell, v // cell)
            if key in busy:
                continue
            sxx = syy = sxy = 0.0
            for dv in (-1, 0, 1):
                for du in (-1, 0, 1):
                    gx, gy = img.gx[v + dv][u + du], img.gy[v + dv][u + du]
                    sxx += gx * gx
                    syy += gy * gy
                    sxy += gx * gy
            tr, dt = sxx + syy, sxx * syy - sxy * sxy
            score = 0.5 * tr - math.sqrt(max(0.0, 0.25 * tr * tr - dt))
            if score > min_score and (key not in best or score > best[key][0]):
                best[key] = (score, u, v)
    return [(u, v) for _, u, v in sorted(best.values(), key=lambda t: (t[2], t[1]))]


def needs_keyframe(cur_pose: Pose, kf_poses: Sequence[Pose], mean_depth: float, ratio: float = 0.12) -> bool:
    """True if the camera center is farther than ratio * mean_depth from the
    center of every keyframe."""
    c = center(cur_pose)
    return all(norm([a - b for a, b in zip(c, center(p))]) > ratio * mean_depth for p in kf_poses)


# ------------------------------------------------------------------ system

class MapPoint:
    def __init__(self, X: Vector, obs: List[Tuple[int, Tuple[float, float]]]):
        self.X, self.obs = X, obs  # obs: (keyframe id, pixel)


def run_svo(frames: Sequence[GridImage], K, first_depth, levels: int = 2, cell: int = 8,
            min_score: float = 20.0, max_kfs: int = 4, kf_ratio: float = 0.12,
            converge: float = 200.0, d_range: Tuple[float, float] = (0.1, 0.5), px_sigma: float = 1.0) -> Dict:
    """Run the pipeline. first_depth(u, v) gives the depth of a pixel of
    frame 0 (the bootstrap). Returns the poses, the keyframe ids and the map."""
    poses: List[Pose] = [(eye(3), [0.0, 0.0, 0.0])]
    kfs: Dict[int, Pose] = {0: poses[0]}  # @line L1
    pyrs = [pyramid(frames[0], levels)]
    points: List[MapPoint] = []
    for (u, v) in shi_tomasi_cells(frames[0], cell, min_score):
        points.append(MapPoint(backproject(K, u, v, first_depth(u, v)), [(0, (float(u), float(v)))]))  # @line L1
    seeds: List[Seed] = []
    added = 0
    for k in range(1, len(frames)):  # @line L2
        pyrs.append(pyramid(frames[k], levels))
        prev = poses[-1]
        feats = []
        for P in points:
            Xc = transform(prev, P.X)
            p = project(K, Xc)
            if p and 5 <= p[0] <= frames[0].w - 6 and 5 <= p[1] <= frames[0].h - 6:
                feats.append((p[0], p[1], Xc[2]))
        rel = sparse_image_alignment(pyrs[k - 1], pyrs[k], K, feats, (eye(3), [0.0, 0.0, 0.0]))  # @line L3
        pose = compose(rel, prev)  # @line L3
        obs, used = [], []
        for P in points:  # @line L4
            p = project(K, transform(pose, P.X))
            if not p or not (5 <= p[0] <= frames[k].w - 6 and 5 <= p[1] <= frames[k].h - 6):
                continue
            cdir = center(pose)
            view = [a - b for a, b in zip(P.X, cdir)]
            best = None
            for fid, uref in P.obs:  # the keyframe with the closest viewing direction
                kdir = [a - b for a, b in zip(P.X, center(kfs[fid]))]
                ang = dot(view, kdir) / (norm(view) * norm(kdir))
                if best is None or ang > best[0]:
                    best = (ang, fid, uref)
            _, fid, uref = best
            z = transform(kfs[fid], P.X)[2]
            A = affine_warp(K, kfs[fid], pose, uref, z)
            got = feature_alignment(frames[k], frames[fid], uref, A, p)  # @line L4
            if got is None or got[1] > 10.0:
                continue
            obs.append((P.X, got[0]))
            used.append((P, got[0]))
        if len(obs) >= 6:
            pose, _ = motion_only_ba(K, pose, obs)  # @line L5
        for P, u in used:  # @line L6
            P.X = structure_only_ba(K, P.X, [(kfs[f], q) for f, q in P.obs] + [(pose, u)])  # @line L6
        poses.append(pose)
        keep = []
        for s in seeds:  # @line L7
            m = epipolar_measurement(K, frames[s.kf], frames[k], kfs[s.kf], pose, s, px_sigma=px_sigma)  # @line L7
            if m is not None:
                s.update(*m)  # @line L7
            if math.sqrt(s.sigma2) < s.z_range / converge:  # @line L7
                X = transform(inverse(kfs[s.kf]), backproject(K, s.u, s.v, 1.0 / s.mu))
                points.append(MapPoint(X, [(s.kf, (s.u, s.v))]))
                added += 1
            else:
                keep.append(s)
        seeds = keep
        depths = [transform(pose, P.X)[2] for P, _ in used] or [1.0]
        if needs_keyframe(pose, list(kfs.values()), sum(depths) / len(depths), kf_ratio):  # @line L8
            kfs[k] = pose  # @line L9
            for P, u in used:
                P.obs.append((k, u))
            if len(kfs) > max_kfs:  # @line L9
                c = center(pose)
                far = max((f for f in kfs if f != k), key=lambda f: norm([a - b for a, b in zip(center(kfs[f]), c)]))
                del kfs[far]
                for P in points:
                    P.obs = [o for o in P.obs if o[0] != far]
                points = [P for P in points if P.obs]
                seeds = [s for s in seeds if s.kf != far]
            taken = [u for _, u in used] + [(s.u, s.v) for s in seeds if s.kf == k]
            mu0 = 0.5 * (d_range[0] + d_range[1])
            for (u, v) in shi_tomasi_cells(frames[k], cell, min_score, taken=taken):  # @line L9
                seeds.append(Seed(k, float(u), float(v), mu0, d_range[1]))
    return {"poses": poses, "keyframes": sorted(kfs), "points": points, "added": added}  # @line L10
