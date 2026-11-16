# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nister-visual-odometry/. The authors are listed in prov/RM5DZP.jsonl.
"""Visual odometry of Nister, Naroditsky and Bergen (CVPR 2004).

The input is a set of feature tracks: for each frame, a dict from a track id
to a point (x, y) in normalized image coordinates x = K^-1 (u, v, 1). The
corner detection and the matching that build the tracks are outside this
file. A pose (R, t) maps world points into the camera: X_c = R X_w + t. The
world frame is the camera of frame 0.

Monocular: preemptive RANSAC over five-point hypotheses between frames 0
and 2 gives the first motion with |t| = 1. Points are triangulated, and
every later frame is placed by preemptive RANSAC over P3P hypotheses,
followed by Gauss-Newton on the reprojection error. A firewall every f
frames stops old frames from being used in new triangulations.

Stereo: each rectified stereo pair gives 3D points with a metric scale, and
P3P against the next left image gives the motion between two frames.

The five-point solver is the method of the five-point-algorithm page,
repeated here in short form so that this file is complete.
"""

from __future__ import annotations

import math
import random
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from cvla import cross, det, dot, eye, matvec, mul, norm, nullvec, polyroots_real, scale, skew, solve, svd, transpose

Matrix = List[List[float]]
Vector = List[float]
Pose = Tuple[Matrix, Vector]
Point2 = Tuple[float, float]

# ------------------------------------------------------------ rigid motion


def so3_exp(w: Sequence[float]) -> Matrix:
    """The rotation exp([w]_x), by the Rodrigues formula."""
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
    """R X + t."""
    R, t = pose
    return [a + b for a, b in zip(matvec(R, X), t)]


def compose(a: Pose, b: Pose) -> Pose:
    """The pose that applies b first and then a."""
    return mul(a[0], b[0]), transform(a, b[1])


def rotation_angle(R1: Matrix, R2: Matrix) -> float:
    """The angle of R1^T R2 in radians. It equals arccos((tr(R1^T R2) - 1) / 2),
    but the form 2 asin(|R1 - R2|_F / sqrt(8)) keeps small angles accurate."""
    d = math.sqrt(sum((R1[r][c] - R2[r][c]) ** 2 for r in range(3) for c in range(3)))
    return 2.0 * math.asin(min(1.0, d / math.sqrt(8.0)))


def kabsch(src: Sequence[Sequence[float]], dst: Sequence[Sequence[float]]) -> Pose:
    """The rotation R and translation t that minimize sum |R src_i + t - dst_i|^2,
    with the sign correction that keeps det R = 1."""
    n = len(src)
    cs = [sum(p[k] for p in src) / n for k in range(3)]
    cd = [sum(p[k] for p in dst) / n for k in range(3)]
    h = [[sum((src[i][r] - cs[r]) * (dst[i][c] - cd[c]) for i in range(n)) for c in range(3)] for r in range(3)]
    u, _, v = svd(h)
    d = 1.0 if det(mul(v, transpose(u))) > 0 else -1.0
    R = mul(mul(v, [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, d]]), transpose(u))
    return R, [cd[k] - dot(R[k], cs) for k in range(3)]


def project(pose: Pose, X: Sequence[float]) -> Optional[Point2]:
    """The normalized image point of X, or None if X is not in front."""
    xc = transform(pose, X)
    if xc[2] <= 1e-12:
        return None
    return xc[0] / xc[2], xc[1] / xc[2]


def reproj_err2(pose: Pose, X: Sequence[float], x: Point2) -> float:
    """The squared reprojection error, or infinity behind the camera."""
    p = project(pose, X)
    if p is None:
        return math.inf
    return (p[0] - x[0]) ** 2 + (p[1] - x[1]) ** 2


# --------------------------------------------------------- triangulation


def triangulate(poses: Sequence[Pose], obs: Sequence[Point2]) -> Vector:
    """Linear triangulation: the null vector of the rows x P3 - P1 and
    y P3 - P2 of every view, with P = [R | t]."""
    rows = []
    for (R, t), (x, y) in zip(poses, obs):
        p = [R[0] + [t[0]], R[1] + [t[1]], R[2] + [t[2]]]
        rows.append([x * p[2][k] - p[0][k] for k in range(4)])
        rows.append([y * p[2][k] - p[1][k] for k in range(4)])
    h = nullvec(rows)
    if abs(h[3]) < 1e-15:
        return [math.inf, math.inf, math.inf]
    return [h[0] / h[3], h[1] / h[3], h[2] / h[3]]


def checked_point(poses: Sequence[Pose], obs: Sequence[Point2], tau: float) -> Optional[Vector]:
    """Triangulate, and keep the point only if it is in front of every view
    with a reprojection error of at most tau."""
    X = triangulate(poses, obs)
    if not all(math.isfinite(c) for c in X):
        return None
    for pose, x in zip(poses, obs):
        if reproj_err2(pose, X, x) > tau * tau:
            return None
    return X


# ---------------------------------------------------- five-point solver

_MONO = [(3, 0, 0), (0, 3, 0), (2, 1, 0), (1, 2, 0), (2, 0, 1), (2, 0, 0),
         (0, 2, 1), (0, 2, 0), (1, 1, 1), (1, 1, 0),
         (1, 0, 2), (1, 0, 1), (1, 0, 0), (0, 1, 2), (0, 1, 1), (0, 1, 0),
         (0, 0, 3), (0, 0, 2), (0, 0, 1), (0, 0, 0)]


def _padd(p, q, c=1.0):
    out = dict(p)
    for k, v in q.items():
        out[k] = out.get(k, 0.0) + c * v
    return out


def _pmul(p, q):
    out = {}
    for (a, b, c), u in p.items():
        for (d, e, f), v in q.items():
            k = (a + d, b + e, c + f)
            out[k] = out.get(k, 0.0) + u * v
    return out


def _pmat(A, B):
    return [[_padd(_padd(_pmul(A[i][0], B[0][j]), _pmul(A[i][1], B[1][j])), _pmul(A[i][2], B[2][j]))
             for j in range(3)] for i in range(3)]


def _zadd(p, q, c=1.0):
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else 0.0) + c * (q[i] if i < len(q) else 0.0) for i in range(n)]


def _zmul(p, q):
    out = [0.0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def _zeval(p, z):
    s = 0.0
    for c in reversed(p):
        s = s * z + c
    return s


def _cubic_residual(M, x, y, z):
    m = [x ** a * y ** b * z ** c for a, b, c in _MONO]
    return [sum(p * q for p, q in zip(row, m)) for row in M]


def _polish(M, x, y, z):
    r = _cubic_residual(M, x, y, z)
    for _ in range(4):
        cols = []
        for k in range(3):
            d = []
            for e in _MONO:
                if e[k] == 0:
                    d.append(0.0)
                    continue
                f = list(e)
                f[k] -= 1
                d.append(e[k] * x ** f[0] * y ** f[1] * z ** f[2])
            cols.append([sum(p * q for p, q in zip(row, d)) for row in M])
        jtj = [[dot(cols[i], cols[j]) for j in range(3)] for i in range(3)]
        try:
            s = solve(jtj, [-dot(cols[i], r) for i in range(3)])
        except ValueError:
            break
        nr = _cubic_residual(M, x + s[0], y + s[1], z + s[2])
        if norm(nr) >= norm(r):
            break
        x, y, z, r = x + s[0], y + s[1], z + s[2], nr
    return x, y, z


def canonical(E: Matrix) -> Matrix:
    """E with Frobenius norm 1 and its largest entry (in absolute value) positive."""
    big = max((v for row in E for v in row), key=abs)
    return scale(E, (1.0 if big > 0 else -1.0) / norm(E))


def five_point(x1: Sequence[Point2], x2: Sequence[Point2]) -> List[Matrix]:
    """Every essential matrix E with x2^T E x1 = 0 on 5 point pairs."""
    a = [[q * p for q in (b[0], b[1], 1.0) for p in (c[0], c[1], 1.0)] for c, b in zip(x1, x2)]
    a += [[0.0] * 9 for _ in range(9 - len(a))]
    _, _, v = svd(a)
    X, Y, Z, W = [[[v[3 * i + j][col] for j in range(3)] for i in range(3)] for col in range(5, 9)]
    E = [[{(1, 0, 0): X[i][j], (0, 1, 0): Y[i][j], (0, 0, 1): Z[i][j], (0, 0, 0): W[i][j]}
          for j in range(3)] for i in range(3)]
    eet = _pmat(E, [[E[j][i] for j in range(3)] for i in range(3)])
    tr = _padd(_padd(eet[0][0], eet[1][1]), eet[2][2])
    eete = _pmat(eet, E)
    d = _padd(_padd(_pmul(E[0][0], _padd(_pmul(E[1][1], E[2][2]), _pmul(E[1][2], E[2][1]), -1.0)),
                    _pmul(E[0][1], _padd(_pmul(E[1][2], E[2][0]), _pmul(E[1][0], E[2][2]), -1.0))),
              _pmul(E[0][2], _padd(_pmul(E[1][0], E[2][1]), _pmul(E[1][1], E[2][0]), -1.0)))
    rows = [d] + [_padd({k: 2.0 * w for k, w in eete[i][j].items()}, _pmul(tr, E[i][j]), -1.0)
                  for i in range(3) for j in range(3)]
    M = [[r.get(m, 0.0) for m in _MONO] for r in rows]
    try:
        C = solve([row[:10] for row in M], [row[10:] for row in M])
    except ValueError:
        return []

    def parts(c):
        return [[c[2], c[1], c[0]], [c[5], c[4], c[3]], [c[9], c[8], c[7], c[6]]]

    B = []
    for r in range(3):
        top, bot = parts(C[4 + 2 * r]), parts(C[5 + 2 * r])
        B.append([_zadd(top[k], [0.0] + bot[k], -1.0) for k in range(3)])

    def minor(p, q, r, s):
        return _zadd(_zmul(p, s), _zmul(q, r), -1.0)

    detb = _zadd(_zadd(_zmul(B[0][0], minor(B[1][1], B[1][2], B[2][1], B[2][2])),
                       _zmul(B[0][1], minor(B[1][0], B[1][2], B[2][0], B[2][2])), -1.0),
                 _zmul(B[0][2], minor(B[1][0], B[1][1], B[2][0], B[2][1])))
    out = []
    for z in polyroots_real(list(reversed(detb))):
        bz = [[_zeval(p, z) for p in row] for row in B]
        w = max([cross(bz[0], bz[1]), cross(bz[0], bz[2]), cross(bz[1], bz[2])], key=norm)
        if abs(w[2]) <= 1e-12 * norm(w):
            continue
        x, y, z = _polish(M, w[0] / w[2], w[1] / w[2], z)
        out.append(canonical([[x * X[i][j] + y * Y[i][j] + z * Z[i][j] + W[i][j] for j in range(3)]
                              for i in range(3)]))
    return out


def sampson_err2(E: Matrix, x1: Point2, x2: Point2) -> float:
    """The squared Sampson distance of a pair to the epipolar constraint."""
    p, q = [x1[0], x1[1], 1.0], [x2[0], x2[1], 1.0]
    ep, etq = matvec(E, p), matvec(transpose(E), q)
    den = ep[0] ** 2 + ep[1] ** 2 + etq[0] ** 2 + etq[1] ** 2
    return dot(q, ep) ** 2 / den if den > 0 else math.inf


def decompose_essential(E: Matrix, x1: Sequence[Point2], x2: Sequence[Point2]) -> Pose:
    """The pair (R, t), |t| = 1, of the four candidates that puts the most
    pairs in front of both cameras (a majority vote)."""
    u, _, v = svd(E)
    if det(u) < 0:
        u = scale(u, -1.0)
    if det(v) < 0:
        v = scale(v, -1.0)
    w = [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    t = [u[0][2], u[1][2], u[2][2]]
    cands = []
    for R in (mul(mul(u, w), transpose(v)), mul(mul(u, transpose(w)), transpose(v))):
        for s in (1.0, -1.0):
            cands.append((R, scale(t, s)))
    first = (eye(3), [0.0, 0.0, 0.0])
    best, best_count = cands[0], -1
    for cand in cands:
        count = 0
        for p, q in zip(x1, x2):
            X = triangulate([first, cand], [p, q])
            if all(math.isfinite(c) for c in X) and X[2] > 0 and transform(cand, X)[2] > 0:
                count += 1
        if count > best_count:
            best, best_count = cand, count
    return best


# ------------------------------------------------------------------ P3P


def _lmul(p, q):
    return _zmul(p, q)


def p3p(bearings: Sequence[Sequence[float]], points: Sequence[Sequence[float]]) -> List[Pose]:
    """Grunert's P3P: every pose (R, t) with R X_i + t on the ray of bearing
    f_i at a positive distance, for 3 points. At most 4 solutions."""
    f = [scale(b, 1.0 / norm(b)) for b in bearings]
    X = [list(map(float, p)) for p in points]
    a2 = norm([X[1][k] - X[2][k] for k in range(3)]) ** 2
    b2 = norm([X[0][k] - X[2][k] for k in range(3)]) ** 2
    c2 = norm([X[0][k] - X[1][k] for k in range(3)]) ** 2
    ca, cb, cg = dot(f[1], f[2]), dot(f[0], f[2]), dot(f[0], f[1])
    q = [1.0, -2.0 * cb, 1.0]
    num = _zadd([b2, 0.0, -b2], q, a2 - c2)
    den = [2.0 * b2 * cg, -2.0 * b2 * ca]
    quartic = _zadd(_zadd(scale(_lmul(num, num), b2), scale(_lmul(num, den), -2.0 * b2 * cg)),
                    _lmul([b2 - c2, 2.0 * c2 * cb, -c2], _lmul(den, den)))
    out = []
    for v in polyroots_real(list(reversed(quartic))):
        dv = _zeval(den, v)
        qv = _zeval(q, v)
        if v <= 0 or abs(dv) < 1e-14 or qv <= 0:
            continue
        u = _zeval(num, v) / dv
        if u <= 0:
            continue
        s1 = math.sqrt(b2 / qv)
        cam = [scale(f[0], s1), scale(f[1], u * s1), scale(f[2], v * s1)]
        out.append(kabsch(X, cam))
    return out


# ------------------------------------------- preemptive scoring and refinement


def preemptive_select(hyps: Sequence, n_obs: int, err2: Callable[[object, int], float],
                      tau: float, block: int, rng: random.Random):
    """Preemptive scoring: the observations are taken in a random order, in
    blocks; after each block only the better half of the hypotheses is kept.
    The score is the truncated quadratic sum of min(e^2, tau^2)."""
    if not hyps:
        return None
    order = list(range(n_obs))
    rng.shuffle(order)
    alive = list(range(len(hyps)))
    score = [0.0] * len(hyps)
    pos = 0
    while pos < n_obs and len(alive) > 1:
        for i in order[pos:pos + block]:
            for h in alive:
                score[h] += min(err2(hyps[h], i), tau * tau)
        pos += block
        alive.sort(key=lambda h: score[h])
        alive = alive[:max(1, len(alive) // 2)]
    return hyps[min(alive, key=lambda h: score[h])]


def pose_residual(pose: Pose, X: Sequence[float], x: Point2) -> Vector:
    xc = transform(pose, X)
    return [xc[0] / xc[2] - x[0], xc[1] / xc[2] - x[1]]


def pose_jacobian(pose: Pose, X: Sequence[float]) -> Matrix:
    """The 2 x 6 Jacobian of the residual for the update of apply_update,
    with the parameters (w, dt)."""
    xc = transform(pose, X)
    z = xc[2]
    dp = [[1.0 / z, 0.0, -xc[0] / (z * z)], [0.0, 1.0 / z, -xc[1] / (z * z)]]
    dw = scale(skew(xc), -1.0)
    return [[dot(dp[r], [dw[0][c], dw[1][c], dw[2][c]]) for c in range(3)] + dp[r] for r in range(2)]


def apply_update(pose: Pose, delta: Sequence[float]) -> Pose:
    """(exp(w) R, exp(w) t + dt) for delta = (w, dt)."""
    E = so3_exp(delta[:3])
    R, t = pose
    return mul(E, R), [a + b for a, b in zip(matvec(E, t), delta[3:])]


def refine_pose(pose: Pose, pts: Sequence[Sequence[float]], obs: Sequence[Point2],
                iters: int = 10) -> Tuple[Pose, List[float]]:
    """Gauss-Newton on sum |pi(R X + t) - x|^2. A step is kept only if it
    lowers the cost. Returns the pose and the cost after each kept step."""
    def cost(p):
        return sum(sum(r * r for r in pose_residual(p, X, x)) for X, x in zip(pts, obs))
    c = cost(pose)
    history = [c]
    for _ in range(iters):
        h = [[0.0] * 6 for _ in range(6)]
        g = [0.0] * 6
        for X, x in zip(pts, obs):
            j = pose_jacobian(pose, X)
            r = pose_residual(pose, X, x)
            for a in range(6):
                g[a] -= j[0][a] * r[0] + j[1][a] * r[1]
                for b in range(6):
                    h[a][b] += j[0][a] * j[0][b] + j[1][a] * j[1][b]
        try:
            step = solve(h, g)
        except ValueError:
            break
        cand = apply_update(pose, step)
        cc = cost(cand)
        if not cc < c:
            break
        pose, c = cand, cc
        history.append(c)
    return pose, history


def resection(pts: Sequence[Sequence[float]], obs: Sequence[Point2], tau: float,
              n_hyp: int, block: int, rng: random.Random) -> Optional[Pose]:
    """Preemptive RANSAC over P3P hypotheses, then Gauss-Newton on the inliers."""
    n = len(pts)
    if n < 4:
        return None
    hyps: List[Pose] = []
    for _ in range(n_hyp):
        idx = rng.sample(range(n), 3)
        hyps += p3p([[obs[i][0], obs[i][1], 1.0] for i in idx], [pts[i] for i in idx])
    best = preemptive_select(hyps, n, lambda h, i: reproj_err2(h, pts[i], obs[i]), tau, block, rng)  # @line L6
    if best is None:
        return None
    inl = [i for i in range(n) if reproj_err2(best, pts[i], obs[i]) <= tau * tau]
    if len(inl) < 3:
        return best
    pose, _ = refine_pose(best, [pts[i] for i in inl], [obs[i] for i in inl])  # @line L7
    return pose


# ------------------------------------------------------------- the systems


def mono_vo(tracks: Sequence[Dict[int, Point2]], firewall_every: int = 4, tau: float = 0.004,
            n_hyp: int = 20, block: int = 10, seed: int = 0) -> List[Pose]:
    """Monocular visual odometry. tracks[k] maps a track id to its normalized
    point in frame k. Returns one pose per frame; the first is (I, 0) and the
    second camera of the start triplet (frame 2) is at distance 1."""
    rng = random.Random(seed)
    n = len(tracks)
    poses: List[Optional[Pose]] = [None] * n
    poses[0] = (eye(3), [0.0, 0.0, 0.0])  # @line L1
    ids = sorted(set(tracks[0]) & set(tracks[2]))
    x1 = [tracks[0][i] for i in ids]
    x2 = [tracks[2][i] for i in ids]
    hyps: List[Matrix] = []
    for _ in range(n_hyp):
        s = rng.sample(range(len(ids)), 5)
        hyps += five_point([x1[i] for i in s], [x2[i] for i in s])  # @line L2
    E = preemptive_select(hyps, len(ids), lambda h, i: sampson_err2(h, x1[i], x2[i]), tau, block, rng)  # @line L2
    inl = [i for i in range(len(ids)) if sampson_err2(E, x1[i], x2[i]) <= tau * tau]
    poses[2] = decompose_essential(E, [x1[i] for i in inl], [x2[i] for i in inl])  # @line L3
    world: Dict[int, Vector] = {}
    for i in inl:
        X = checked_point([poses[0], poses[2]], [x1[i], x2[i]], tau)  # @line L4
        if X is not None:
            world[ids[i]] = X  # @line L4
    firewall = 0  # @line L4
    for k in [1] + list(range(3, n)):  # @line L5
        seen = [i for i in tracks[k] if i in world]
        pose = resection([world[i] for i in seen], [tracks[k][i] for i in seen], tau, n_hyp, block, rng)  # @line L6
        if pose is None:
            raise ValueError("frame %d could not be placed" % k)
        poses[k] = pose  # @line L7
        for tid, x in tracks[k].items():  # @line L8
            first = next((j for j in range(firewall, k) if poses[j] is not None and tid in tracks[j]), None)  # @line L9
            if first is not None and k - first >= 2:  # @line L10
                X = checked_point([poses[first], pose], [tracks[first][tid], x], tau)
                if X is not None:
                    world[tid] = X  # @line L10
        if k % firewall_every == 0:  # @line L11
            firewall = k  # @line L11
    return poses  # @line L12


def stereo_vo(left: Sequence[Dict[int, Point2]], right: Sequence[Dict[int, Point2]], baseline: float,
              tau: float = 0.004, n_hyp: int = 15, block: int = 10, seed: int = 0) -> List[Pose]:
    """Stereo visual odometry on a rectified pair: the right camera is the left
    one moved by baseline along +x. Points from the pair at frame k - 1 and
    P3P in the left image k give the motion; the poses are chained."""
    rng = random.Random(seed)
    rig = [(eye(3), [0.0, 0.0, 0.0]), (eye(3), [-baseline, 0.0, 0.0])]
    poses: List[Pose] = [(eye(3), [0.0, 0.0, 0.0])]
    for k in range(1, len(left)):
        pts, obs = [], []
        for tid, xl in left[k - 1].items():
            if tid in right[k - 1] and tid in left[k]:
                X = checked_point(rig, [xl, right[k - 1][tid]], tau)
                if X is not None:
                    pts.append(X)
                    obs.append(left[k][tid])
        rel = resection(pts, obs, tau, n_hyp, block, rng)
        if rel is None:
            raise ValueError("frame %d could not be placed" % k)
        poses.append(compose(rel, poses[-1]))
    return poses
