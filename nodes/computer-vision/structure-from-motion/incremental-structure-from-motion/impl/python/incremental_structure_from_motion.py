# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incremental-structure-from-motion/. The authors are listed in prov/K15KYC.jsonl.

"""Incremental structure from motion with a known intrinsic matrix K.

The input is K and a list of tracks. A track is a dict {image: (u, v)}
of the pixels of one 3D point. The output is a pose (R, t) for every
image that could be registered, with X_c = R X + t, and a 3D point for
every track that could be triangulated. Image a of the first pair has
R = I and t = 0, and image b has ||t|| = 1; the reconstruction is fixed
only up to this similarity.

The pipeline: pick the image pair with the most common tracks, find its
relative pose from the essential matrix (RANSAC on the 8-point method),
triangulate, run bundle adjustment. Then repeat: register the image that
sees the most triangulated points by a RANSAC on the 6-point DLT,
triangulate the tracks that it makes visible in two images, run bundle
adjustment, and drop observations with a reprojection error above tau.
"""

import math
import random
from typing import Dict, List, Optional, Sequence, Tuple

from cvgeom import axis_angle_to_R
from cvla import det, dot, inv, matvec, mul, nullvec, solve, svd, transpose

Vector = List[float]
Matrix = List[List[float]]
Pose = Tuple[Matrix, Vector]
EYE3 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]


# ------------------------------------------------------------ geometry

def normalize(kinv: Matrix, p: Sequence[float]) -> Vector:
    """The normalized image point (x, y) of the pixel p: K^-1 (u, v, 1)."""
    q = matvec(kinv, [p[0], p[1], 1.0])
    return [q[0] / q[2], q[1] / q[2]]


def to_cam(pose: Pose, x: Sequence[float]) -> Vector:
    r, t = pose
    return [dot(r[a], x) + t[a] for a in range(3)]


def reproj_error(pose: Pose, x: Sequence[float], p: Sequence[float]) -> float:
    """Distance in normalized coordinates; infinite behind the camera."""
    c = to_cam(pose, x)
    if c[2] <= 0:
        return math.inf
    return math.hypot(c[0] / c[2] - p[0], c[1] / c[2] - p[1])


def triangulate(poses: Sequence[Pose], pts: Sequence[Sequence[float]]) -> Vector:
    """Linear (DLT) triangulation from two or more normalized points."""
    rows = []
    for (r, t), (x, y) in zip(poses, pts):
        p = [r[a] + [t[a]] for a in range(3)]
        rows.append([x * p[2][k] - p[0][k] for k in range(4)])
        rows.append([y * p[2][k] - p[1][k] for k in range(4)])
    h = nullvec(rows)
    if abs(h[3]) < 1e-12:
        return [math.inf] * 3
    return [h[k] / h[3] for k in range(3)]


def _conditioner(pts: Sequence[Vector]) -> Matrix:
    n = len(pts)
    cx, cy = sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n
    d = sum(math.hypot(p[0] - cx, p[1] - cy) for p in pts) / n or 1.0
    s = math.sqrt(2.0) / d
    return [[s, 0.0, -s * cx], [0.0, s, -s * cy], [0.0, 0.0, 1.0]]


def eight_point_essential(x1: Sequence[Vector], x2: Sequence[Vector]) -> Matrix:
    """E with x2^T E x1 = 0, projected to singular values (1, 1, 0). The
    points are conditioned first (Hartley normalization)."""
    t1, t2 = _conditioner(x1), _conditioner(x2)
    y1 = [matvec(t1, [p[0], p[1], 1.0]) for p in x1]
    y2 = [matvec(t2, [q[0], q[1], 1.0]) for q in x2]
    a = [[q[0] * p[0], q[0] * p[1], q[0], q[1] * p[0], q[1] * p[1], q[1], p[0], p[1], 1.0]
         for p, q in zip(y1, y2)]
    e = nullvec(a)
    e = mul(mul(transpose(t2), [e[0:3], e[3:6], e[6:9]]), t1)
    u, _, v = svd(e)
    return mul(mul(u, [[1.0, 0, 0], [0, 1.0, 0], [0, 0, 0.0]]), transpose(v))


def sampson(e: Matrix, p: Sequence[float], q: Sequence[float]) -> float:
    x1, x2 = [p[0], p[1], 1.0], [q[0], q[1], 1.0]
    ex1 = matvec(e, x1)
    etx2 = matvec(transpose(e), x2)
    num = dot(x2, ex1)
    den = ex1[0] ** 2 + ex1[1] ** 2 + etx2[0] ** 2 + etx2[1] ** 2
    return math.sqrt(num * num / den) if den > 0 else math.inf


def decompose_essential(e: Matrix, x1: Sequence[Vector], x2: Sequence[Vector]) -> Pose:
    """The (R, t) among the four candidates that puts the most points in
    front of both cameras; ||t|| = 1."""
    u, _, v = svd(e)
    if det(u) < 0:
        u = [[-c for c in row] for row in u]
    if det(v) < 0:
        v = [[-c for c in row] for row in v]
    w = [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    u3 = [u[a][2] for a in range(3)]
    best, best_count = None, -1
    for r in (mul(mul(u, w), transpose(v)), mul(mul(u, transpose(w)), transpose(v))):
        for t in (u3, [-c for c in u3]):
            count = 0
            for p, q in zip(x1, x2):
                x = triangulate([(EYE3, [0.0, 0.0, 0.0]), (r, t)], [p, q])
                if x[2] > 0 and to_cam((r, t), x)[2] > 0:
                    count += 1
            if count > best_count:
                best, best_count = (r, list(t)), count
    return best


def ransac_count(inlier_ratio: float, sample: int, cap: int) -> int:
    if inlier_ratio <= 0:
        return cap
    w = inlier_ratio ** sample
    if w >= 1:
        return 1
    return min(cap, int(math.ceil(math.log(0.01) / math.log(1 - w))))


def relative_pose_ransac(x1: Sequence[Vector], x2: Sequence[Vector], tau: float,
                         rng: random.Random, cap: int = 300) -> Tuple[Pose, List[int]]:
    """RANSAC on the 8-point method; returns the pose and the inlier indices."""
    n = len(x1)
    best: List[int] = []
    best_e = None
    it, need = 0, cap
    while it < need:
        it += 1
        s = rng.sample(range(n), 8)
        e = eight_point_essential([x1[k] for k in s], [x2[k] for k in s])
        inl = [k for k in range(n) if sampson(e, x1[k], x2[k]) < tau]
        if len(inl) > len(best):
            best, best_e = inl, e
            need = ransac_count(len(best) / n, 8, cap)
    e = eight_point_essential([x1[k] for k in best], [x2[k] for k in best])
    refit = [k for k in range(n) if sampson(e, x1[k], x2[k]) < tau]
    if len(refit) >= len(best):
        best = refit
    else:
        e = best_e
    pose = decompose_essential(e, [x1[k] for k in best], [x2[k] for k in best])
    return pose, best


def dlt_pnp(xs: Sequence[Vector], ps: Sequence[Sequence[float]]) -> Optional[Pose]:
    """Pose from six or more 3D points and normalized image points, by the
    DLT on a conditioned copy of the points, then the nearest rotation."""
    n = len(xs)
    c = [sum(x[a] for x in xs) / n for a in range(3)]
    s = sum(math.dist(x, c) for x in xs) / n or 1.0
    rows = []
    for x, p in zip(xs, ps):
        y = [(x[a] - c[a]) / s for a in range(3)] + [1.0]
        rows.append(y + [0.0] * 4 + [-p[0] * v for v in y])
        rows.append([0.0] * 4 + y + [-p[1] * v for v in y])
    h = nullvec(rows)
    pc = [h[0:4], h[4:8], h[8:12]]
    # undo the conditioning: P = P' [[I / s, -c / s], [0, 1]]
    m = [[pc[a][b] / s for b in range(3)] for a in range(3)]
    p4 = [pc[a][3] - sum(m[a][b] * c[b] for b in range(3)) for a in range(3)]
    if det(m) < 0:
        m = [[-v for v in row] for row in m]
        p4 = [-v for v in p4]
    u, sv, v = svd(m)
    r = mul(u, transpose(v))
    k = sum(sv) / 3.0
    if k <= 0:
        return None
    return r, [v_ / k for v_ in p4]


def pnp_ransac(xs: Sequence[Vector], ps: Sequence[Vector], tau: float,
               rng: random.Random, cap: int = 200) -> Tuple[Optional[Pose], List[int]]:
    """RANSAC on the 6-point DLT, each fit polished by Gauss-Newton on the
    pose. Returns the pose and the inlier indices, or (None, [])."""
    n = len(xs)
    best: List[int] = []
    best_pose = None
    it, need = 0, cap
    while it < need:
        it += 1
        s = rng.sample(range(n), 6)
        pose = dlt_pnp([xs[k] for k in s], [ps[k] for k in s])
        if pose is None:
            continue
        pose = refine_pose(pose, [xs[k] for k in s], [ps[k] for k in s])
        inl = [k for k in range(n) if reproj_error(pose, xs[k], ps[k]) < tau]
        if len(inl) > len(best):
            best, best_pose = inl, pose
            need = ransac_count(len(best) / n, 6, cap)
    if len(best) < 6:
        return None, []
    pose = refine_pose(best_pose, [xs[k] for k in best], [ps[k] for k in best])
    best = [k for k in range(n) if reproj_error(pose, xs[k], ps[k]) < tau]
    return pose, best


def refine_pose(pose: Pose, xs: Sequence[Vector], ps: Sequence[Vector], iters: int = 5) -> Pose:
    """A few Gauss-Newton steps on the reprojection error of one camera."""
    for _ in range(iters):
        h = [[0.0] * 6 for _ in range(6)]
        g = [0.0] * 6
        for x, p in zip(xs, ps):
            if to_cam(pose, x)[2] <= 0:
                return pose
            res, a, _ = _blocks(pose, x, p)
            for r in range(6):
                g[r] -= a[0][r] * res[0] + a[1][r] * res[1]
                for s in range(6):
                    h[r][s] += a[0][r] * a[0][s] + a[1][r] * a[1][s]
        try:
            d = solve(h, g)
        except ValueError:
            return pose
        r, t = pose
        pose = (mul(axis_angle_to_R(d[0:3]), r), [t[k] + d[3 + k] for k in range(3)])
        if max(abs(v) for v in d) < 1e-12:
            break
    return pose


# ---------------------------------------------------- bundle adjustment

def _blocks(pose: Pose, x: Sequence[float], p: Sequence[float]):
    r, t = pose
    rx = matvec(r, x)
    c = [rx[a] + t[a] for a in range(3)]
    iz = 1.0 / c[2]
    res = [c[0] * iz - p[0], c[1] * iz - p[1]]
    d = [[iz, 0.0, -c[0] * iz * iz], [0.0, iz, -c[1] * iz * iz]]
    # dX_c/dw = -[R X]_x, dX_c/dt = I, dX_c/dX = R
    sk = [[0.0, rx[2], -rx[1]], [-rx[2], 0.0, rx[0]], [rx[1], -rx[0], 0.0]]
    a = [[sum(d[i][k] * sk[k][j] for k in range(3)) for j in range(3)] + d[i] for i in range(2)]
    b = [[sum(d[i][k] * r[k][j] for k in range(3)) for j in range(3)] for i in range(2)]
    return res, a, b


def ba_cost(cams: Dict[int, Pose], pts: Dict[int, Vector], obs: Dict[Tuple[int, int], Vector]) -> float:
    total = 0.0
    for (i, j), p in obs.items():
        c = to_cam(cams[i], pts[j])
        if c[2] <= 0:
            return math.inf
        total += (c[0] / c[2] - p[0]) ** 2 + (c[1] / c[2] - p[1]) ** 2
    return 0.5 * total


def bundle_adjust(cams: Dict[int, Pose], pts: Dict[int, Vector],
                  obs: Dict[Tuple[int, int], Vector], fixed: int,
                  max_iter: int = 20) -> Tuple[Dict[int, Pose], Dict[int, Vector]]:
    """Levenberg-Marquardt on the normalized reprojection error, with the
    points eliminated by the Schur complement. Camera `fixed` is held."""
    free = sorted(i for i in cams if i != fixed)
    col = {i: 6 * k for k, i in enumerate(free)}
    f = ba_cost(cams, pts, obs)
    mu = 1e-3
    for _ in range(max_iter):
        nf = 6 * len(free)
        u = [[0.0] * nf for _ in range(nf)]
        ga = [0.0] * nf
        v: Dict[int, Matrix] = {j: [[0.0] * 3 for _ in range(3)] for j in pts}
        gb: Dict[int, Vector] = {j: [0.0] * 3 for j in pts}
        wb: Dict[int, Dict[int, Matrix]] = {j: {} for j in pts}
        for (i, j), p in obs.items():
            res, a, b = _blocks(cams[i], pts[j], p)
            for r in range(3):
                for s in range(3):
                    v[j][r][s] += b[0][r] * b[0][s] + b[1][r] * b[1][s]
                gb[j][r] += b[0][r] * res[0] + b[1][r] * res[1]
            if i in col:
                o = col[i]
                for r in range(6):
                    for s in range(6):
                        u[o + r][o + s] += a[0][r] * a[0][s] + a[1][r] * a[1][s]
                    ga[o + r] += a[0][r] * res[0] + a[1][r] * res[1]
                wb[j][i] = [[a[0][r] * b[0][s] + a[1][r] * b[1][s] for s in range(3)] for r in range(6)]
        while True:
            vinv = {j: inv([[v[j][r][s] + (mu if r == s else 0.0) for s in range(3)] for r in range(3)])
                    for j in pts}
            sm = [[u[r][s] + (mu if r == s else 0.0) for s in range(nf)] for r in range(nf)]
            rhs = [-g for g in ga]
            for j in pts:
                wv = {i: mul(wj, vinv[j]) for i, wj in wb[j].items()}
                vg = matvec(vinv[j], gb[j])
                for i, wvi in wv.items():
                    oi = col[i]
                    for r in range(6):
                        rhs[oi + r] += dot(wb[j][i][r], vg)
                    for k, wk in wb[j].items():
                        ok = col[k]
                        for r in range(6):
                            for s in range(6):
                                sm[oi + r][ok + s] -= dot(wvi[r], wk[s])
            da = solve(sm, rhs) if nf else []
            new_cams = dict(cams)
            for i in free:
                d = da[col[i]:col[i] + 6]
                r, t = cams[i]
                new_cams[i] = (mul(axis_angle_to_R(d[0:3]), r), [t[a] + d[3 + a] for a in range(3)])
            new_pts = {}
            for j in pts:
                g = list(gb[j])
                for i, wj in wb[j].items():
                    d = da[col[i]:col[i] + 6]
                    g = [g[r] + sum(wj[k][r] * d[k] for k in range(6)) for r in range(3)]
                db = matvec(vinv[j], [-x for x in g])
                new_pts[j] = [pts[j][a] + db[a] for a in range(3)]
            f_new = ba_cost(new_cams, new_pts, obs)
            if f_new < f:
                done = f - f_new < 1e-12 * f + 1e-30
                cams, pts, f = new_cams, new_pts, f_new
                mu = max(mu / 3.0, 1e-12)
                break
            mu *= 4.0
            if mu > 1e12:
                return cams, pts
        if done:
            break
    return cams, pts


# ------------------------------------------------------------ pipeline

def incremental_structure_from_motion(K: Matrix, tracks: Sequence[Dict[int, Sequence[float]]],
                                      tau_px: float = 3.0, seed: int = 0):
    """Returns (cams, pts, obs): cams[i] = (R, t), pts[j] = X for track j,
    and obs, the set of (image, track) pairs that were kept."""
    rng = random.Random(seed)
    kinv = inv(K)
    tau = tau_px / K[0][0]
    xn = [{i: normalize(kinv, p) for i, p in tr.items()} for tr in tracks]
    images = sorted({i for tr in tracks for i in tr})
    pair_count: Dict[Tuple[int, int], int] = {}
    for tr in tracks:
        ims = sorted(tr)
        for x in range(len(ims)):
            for y in range(x + 1, len(ims)):
                pair_count[(ims[x], ims[y])] = pair_count.get((ims[x], ims[y]), 0) + 1
    a, b = max(sorted(pair_count), key=lambda k: pair_count[k])  # @line L1
    common = [j for j, tr in enumerate(tracks) if a in tr and b in tr]
    pose_b, inl = relative_pose_ransac([xn[j][a] for j in common], [xn[j][b] for j in common],
                                       tau, rng)  # @line L2
    cams: Dict[int, Pose] = {a: (EYE3, [0.0, 0.0, 0.0]), b: pose_b}
    pts: Dict[int, Vector] = {}
    obs: Dict[Tuple[int, int], Vector] = {}
    for k in inl:  # @line L3
        j = common[k]
        x = triangulate([cams[a], cams[b]], [xn[j][a], xn[j][b]])
        if all(reproj_error(cams[i], x, xn[j][i]) < tau for i in (a, b)):
            pts[j] = x
            obs[(a, j)], obs[(b, j)] = xn[j][a], xn[j][b]
    cams, pts = bundle_adjust(cams, pts, obs, a)  # @line L4
    while True:  # @line L5
        left = [i for i in images if i not in cams]
        seen = {i: [j for j in pts if i in tracks[j]] for i in left}
        if not left or max(len(s) for s in seen.values()) < 6:
            break
        c = max(left, key=lambda i: (len(seen[i]), -i))  # @line L6
        js = seen[c]
        pose, inl = pnp_ransac([pts[j] for j in js], [xn[j][c] for j in js], tau, rng)  # @line L7
        if pose is None:
            break
        cams[c] = pose
        for k in inl:
            obs[(c, js[k])] = xn[js[k]][c]
        for j, tr in enumerate(tracks):  # @line L8
            views = [i for i in tr if i in cams]
            if j in pts or c not in tr or len(views) < 2:
                continue
            x = triangulate([cams[i] for i in views], [xn[j][i] for i in views])
            good = [i for i in views if reproj_error(cams[i], x, xn[j][i]) < tau]
            if 2 <= len(good) < len(views):
                x = triangulate([cams[i] for i in good], [xn[j][i] for i in good])
                good = [i for i in good if reproj_error(cams[i], x, xn[j][i]) < tau]
            if len(good) >= 2:
                pts[j] = x
                for i in good:
                    obs[(i, j)] = xn[j][i]
        cams, pts = bundle_adjust(cams, pts, obs, a)  # @line L9
        for key in [k for k in obs if reproj_error(cams[k[0]], pts[k[1]], obs[k]) > tau]:
            del obs[key]
        for j in list(pts):
            if sum(1 for (i, jj) in obs if jj == j) < 2:
                del pts[j]
                for key in [k for k in obs if k[1] == j]:
                    del obs[key]
    return cams, pts, set(obs)  # @line L10
