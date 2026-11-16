# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-sparse-odometry/. The authors are listed in prov/YH2YPH.jsonl.
"""Direct sparse odometry (Engel, Koltun and Cremers, TPAMI 2018), small form.

The model follows the paper:
- A point is a pixel p of its host keyframe i with one inverse depth d. Its
  residual pattern has 8 pixels q = p + o, all with the same inverse depth.
- The residual of a pattern pixel in a target frame j is
      r = (I_j[q'] - b_j) - exp(a_j - a_i) (I_i[q] - b_i),
  q' = Pi(R Pi^-1(q, d) + t), with (R, t) = T_j T_i^-1. Each residual has the
  weight w = c^2 / (c^2 + |grad I_i(q)|^2) and the Huber norm.
- A new frame is tracked against the newest keyframe by Gauss-Newton on its
  pose and its affine brightness (a, b), coarse to fine, from a constant
  motion guess.
- A new keyframe is made when w_f f + w_ft f_t + w_a a > T_kf.
- Points are chosen with a gradient threshold per block (the median of the
  block plus g_th). Their inverse depth is found by a search along the
  epipolar line and a few Gauss-Newton steps on the inverse depth.
- The window of keyframes is optimized by Gauss-Newton on all poses, affine
  terms and inverse depths, with the Schur complement on the inverse depths.
  A keyframe that leaves the window is marginalized by the Schur complement
  into a quadratic prior on the remaining keyframes.

What is left out: photometric calibration (the images are taken as already
corrected), the first estimate Jacobians, the recovery after a tracking
failure, the outlier rules for points, and the initialization of the first
depths (the caller gives them). An image is any object with a method
sample(u, v) that returns (value, d/du, d/dv), or None outside the image.
Poses map world points into the camera: X_c = R X + t.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

from cvla import dot, eye, matvec, mul, norm, skew, solve, transpose

Matrix = List[List[float]]
Vector = List[float]
Pose = Tuple[Matrix, Vector]

# The 8-pixel residual pattern (offsets du, dv) used by this code.
PATTERN = [(0, -2), (-1, -1), (1, -1), (-2, 0), (0, 0), (2, 0), (-1, 1), (0, 2)]


# ------------------------------------------------------------------ images

class GridImage:
    """A gray image img[v][u]. Values and central-difference gradients are
    read with bilinear interpolation. Samples closer than one pixel to the
    border return None."""

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
        """The next pyramid level: the mean of each 2 x 2 block."""
        return GridImage([[0.25 * (self.val[2 * v][2 * u] + self.val[2 * v][2 * u + 1] +
                                   self.val[2 * v + 1][2 * u] + self.val[2 * v + 1][2 * u + 1])
                           for u in range(self.w // 2)] for v in range(self.h // 2)])


def pyramid(img: GridImage, levels: int) -> List[GridImage]:
    out = [img]
    for _ in range(levels - 1):
        out.append(out[-1].half())
    return out


def level_K(K: Sequence[float], level: int) -> Tuple[float, float, float, float]:
    """(fx, fy, cx, cy) at a pyramid level. Pixel centers are integers, so a
    2 x 2 mean maps u to (u - 0.5) / 2."""
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


def so3_log(R: Matrix) -> Vector:
    tr = R[0][0] + R[1][1] + R[2][2]
    c = max(-1.0, min(1.0, (tr - 1.0) / 2.0))
    th = math.acos(c)
    v = [R[2][1] - R[1][2], R[0][2] - R[2][0], R[1][0] - R[0][1]]
    if th < 1e-7:
        return [0.5 * x for x in v]
    if math.pi - th < 1e-6:
        raise ValueError("so3_log: angle too close to pi")
    return [th / (2.0 * math.sin(th)) * x for x in v]


def apply_update(pose: Pose, delta: Sequence[float]) -> Pose:
    """(exp(w) R, exp(w) t + v) for delta = (w, v): the left update."""
    E = so3_exp(delta[:3])
    R, t = pose
    return mul(E, R), [a + b for a, b in zip(matvec(E, t), delta[3:6])]


def pose_delta(pose: Pose, ref: Pose) -> Vector:
    """The delta with apply_update(ref, delta) = pose."""
    Rd = mul(pose[0], transpose(ref[0]))
    w = so3_log(Rd)
    rt = matvec(Rd, ref[1])
    return w + [a - b for a, b in zip(pose[1], rt)]


def relative(tj: Pose, ti: Pose) -> Pose:
    """T_j T_i^-1, which maps host camera coordinates to target ones."""
    Rji = mul(tj[0], transpose(ti[0]))
    return Rji, [a - b for a, b in zip(tj[1], matvec(Rji, ti[1]))]


def center(pose: Pose) -> Vector:
    return [-x for x in matvec(transpose(pose[0]), pose[1])]


# ----------------------------------------------------- residual and weights

def huber_weight(r: float, k: float) -> float:
    a = abs(r)
    return 1.0 if a <= k else k / a


def huber(r: float, k: float) -> float:
    a = abs(r)
    return 0.5 * r * r if a <= k else k * (a - 0.5 * k)


def gradient_weight(g2: float, c: float) -> float:
    """c^2 / (c^2 + |grad I_i(q)|^2), from the squared gradient norm g2."""
    return c * c / (c * c + g2)


def warp(K, q: Sequence[float], d: float, rel: Pose):
    """Pi(R Pi^-1(q, d) + t): the target pixel and the target camera point."""
    fx, fy, cx, cy = K
    X = ((q[0] - cx) / fx / d, (q[1] - cy) / fy / d, 1.0 / d)
    R, t = rel
    Xt = [R[r][0] * X[0] + R[r][1] * X[1] + R[r][2] * X[2] + t[r] for r in range(3)]
    if Xt[2] <= 1e-9:
        return None, Xt
    return (fx * Xt[0] / Xt[2] + cx, fy * Xt[1] / Xt[2] + cy), Xt


def residual(host_img, tgt_img, K, q, d, host: Tuple[Pose, float, float], tgt: Tuple[Pose, float, float],
             with_jacobian: bool = False, rel: Optional[Pose] = None):
    """The photometric residual of one pattern pixel q of a point with inverse
    depth d, and its gradient weight. With with_jacobian, also the
    derivatives with respect to the target (6 pose, a_j, b_j), the host
    (6 pose, a_i, b_i) and d. rel may give T_j T_i^-1 when the caller has it.
    Returns None if a sample is outside an image."""
    (ti, ai, bi), (tj, aj, bj) = host, tgt
    hs = host_img.sample(q[0], q[1])
    if hs is None:
        return None
    if rel is None:
        rel = relative(tj, ti)
    qp, Xt = warp(K, q, d, rel)
    if qp is None:
        return None
    ts = tgt_img.sample(qp[0], qp[1])
    if ts is None:
        return None
    s = math.exp(aj - ai)
    r = (ts[0] - bj) - s * (hs[0] - bi)
    wp = hs[1] * hs[1] + hs[2] * hs[2]
    if not with_jacobian:
        return r, wp, qp
    fx, fy, cx, cy = K
    z = Xt[2]
    gu = [fx / z, 0.0, -fx * Xt[0] / (z * z)]
    gv = [0.0, fy / z, -fy * Xt[1] / (z * z)]
    dX = [ts[1] * gu[k] + ts[2] * gv[k] for k in range(3)]  # dr / dXt
    # target pose: dXt/dw = -[Xt]x, dXt/dv = I
    sx = skew(Xt)
    jt = [-sum(dX[r_] * sx[r_][c] for r_ in range(3)) for c in range(3)] + dX
    jt += [-s * (hs[0] - bi), -1.0]
    # host pose: dXt/dw_i = R_ji [Xh]x, dXt/dv_i = -R_ji
    Xh = [(q[0] - cx) / fx / d, (q[1] - cy) / fy / d, 1.0 / d]
    dXR = [sum(dX[r_] * rel[0][r_][c] for r_ in range(3)) for c in range(3)]  # dX^T R
    sh = skew(Xh)
    jh = [sum(dXR[r_] * sh[r_][c] for r_ in range(3)) for c in range(3)] + [-x for x in dXR]
    jh += [s * (hs[0] - bi), s]
    # inverse depth: dXh/dd = -Xh / d
    jd = -dot(dXR, Xh) / d
    return r, wp, qp, jt, jh, jd


# --------------------------------------------------------- point selection

def select_points(img: GridImage, block: int, g_th: float, passes: int = 3, factor: float = 0.75,
                  margin: int = 3) -> List[Tuple[int, int]]:
    """Region-adaptive gradient threshold. In each block of size block, the
    threshold is the median gradient norm of the block plus g_th, and the
    pixel with the largest gradient above it is chosen. Later passes use
    blocks of 2 and 4 times the size and a threshold multiplied by factor,
    and skip blocks that already hold a point."""
    g = [[math.hypot(img.gx[v][u], img.gy[v][u]) for u in range(img.w)] for v in range(img.h)]
    chosen: List[Tuple[int, int]] = []
    taken = set()
    size, scale_th = block, 1.0
    for _ in range(passes):
        for v0 in range(margin, img.h - margin, size):
            for u0 in range(margin, img.w - margin, size):
                cells = [(g[v][u], u, v) for v in range(v0, min(v0 + size, img.h - margin))
                         for u in range(u0, min(u0 + size, img.w - margin))]
                if not cells or any((u, v) in taken for _, u, v in cells):
                    continue
                vals = sorted(c[0] for c in cells)
                th = scale_th * (vals[len(vals) // 2] + g_th)
                best = max(cells)
                if best[0] > th:
                    chosen.append((best[1], best[2]))
                    taken.add((best[1], best[2]))
        size, scale_th = 2 * size, scale_th * factor
    return chosen


# -------------------------------------------------------------- tracking

def track_frame(points, host_pyr, tgt_pyr, K, host: Tuple[Pose, float, float], init: Tuple[Pose, float, float],
                huber_k: float = 9.0, grad_c: float = 50.0, iters: int = 20):
    """Two-frame direct alignment of a new frame against one keyframe:
    Gauss-Newton on the target pose and (a_j, b_j), coarse to fine, with the
    host and the inverse depths held fixed. points is a list of (u, v, d) in
    host pixels of level 0. Returns ((pose, a, b), RMSE)."""
    pose, aj, bj = init
    rmse = math.inf
    for lev in range(len(tgt_pyr) - 1, -1, -1):  # @line L3
        Kl = level_K(K, lev)
        f = 0.5 ** lev
        qs = []
        for (u, v, d) in points:
            pl = ((u + 0.5) * f - 0.5, (v + 0.5) * f - 0.5)
            for o in PATTERN:
                qs.append(((pl[0] + o[0], pl[1] + o[1]), d))

        def energy(state):
            e, n, sq = 0.0, 0, 0.0
            rel = relative(state[0], host[0])
            for q, d in qs:
                res = residual(host_pyr[lev], tgt_pyr[lev], Kl, q, d, host, state, rel=rel)
                if res is None:
                    continue
                e += gradient_weight(res[1], grad_c) * huber(res[0], huber_k)
                sq += res[0] ** 2
                n += 1
            return e, (math.sqrt(sq / n) if n else math.inf)

        state = (pose, aj, bj)
        e0, rmse = energy(state)
        for _ in range(iters):
            H = [[0.0] * 8 for _ in range(8)]
            b = [0.0] * 8
            rel = relative(state[0], host[0])
            for q, d in qs:
                res = residual(host_pyr[lev], tgt_pyr[lev], Kl, q, d, host, state, True, rel)
                if res is None:
                    continue
                r, wp, _, jt, _, _ = res
                w = gradient_weight(wp, grad_c) * huber_weight(r, huber_k)
                for x in range(8):
                    b[x] -= w * jt[x] * r
                    for y in range(8):
                        H[x][y] += w * jt[x] * jt[y]
            try:
                step = solve(H, b)
            except ValueError:
                break
            cand = (apply_update(state[0], step[:6]), state[1] + step[6], state[2] + step[7])
            e1, r1 = energy(cand)
            if not e1 < e0:
                break
            state, e0, rmse = cand, e1, r1
            if norm(step) < 1e-12:
                break
        pose, aj, bj = state
    return (pose, aj, bj), rmse


def keyframe_score(points, K, host: Tuple[Pose, float, float], tgt: Tuple[Pose, float, float],
                   wf: float, wft: float, wa: float) -> float:
    """w_f f + w_ft f_t + w_a a: f is the root mean square pixel shift of the
    points, f_t the same shift with the rotation set to I, and
    a = |a_j - a_i| (the log of exp(a_j - a_i) t_j / t_i with t = 1)."""
    rel = relative(tgt[0], host[0])
    rel_t = (eye(3), rel[1])
    sf, sft, n = 0.0, 0.0, 0
    for (u, v, d) in points:
        p1, _ = warp(K, (u, v), d, rel)
        p2, _ = warp(K, (u, v), d, rel_t)
        if p1 is None or p2 is None:
            continue
        sf += (p1[0] - u) ** 2 + (p1[1] - v) ** 2
        sft += (p2[0] - u) ** 2 + (p2[1] - v) ** 2
        n += 1
    if n == 0:
        return math.inf
    return wf * math.sqrt(sf / n) + wft * math.sqrt(sft / n) + wa * abs(tgt[1] - host[1])


# ----------------------------------------------- inverse depth of new points

def search_depth(host_img, tgt_img, K, p, host, tgt, d_min: float, d_max: float, steps: int = 40,
                 grad_c: float = 50.0, gn_iters: int = 10) -> Optional[Tuple[float, float]]:
    """The inverse depth of the pixel p of the host: the best of steps
    values in [d_min, d_max] (a discrete search along the epipolar line),
    then Gauss-Newton on d alone. Returns (d, RMSE) or None."""
    rel = relative(tgt[0], host[0])

    def cost(d):
        s, n = 0.0, 0
        for o in PATTERN:
            res = residual(host_img, tgt_img, K, (p[0] + o[0], p[1] + o[1]), d, host, tgt, rel=rel)
            if res is None:
                return math.inf
            s += res[0] ** 2
            n += 1
        return s / n
    best_d, best_c = None, math.inf
    for k in range(steps):
        d = d_min + (d_max - d_min) * k / (steps - 1)
        c = cost(d)
        if c < best_c:
            best_d, best_c = d, c
    if best_d is None:
        return None
    d = best_d
    for _ in range(gn_iters):
        h, g = 0.0, 0.0
        for o in PATTERN:
            res = residual(host_img, tgt_img, K, (p[0] + o[0], p[1] + o[1]), d, host, tgt, True, rel)
            if res is None:
                return None
            h += res[5] ** 2
            g -= res[5] * res[0]
        if h <= 0:
            break
        nd = d + g / h
        nc = cost(nd) if nd > 0 else math.inf
        if not nc < best_c:
            break
        d, best_c = nd, nc
    return d, math.sqrt(best_c)


# ------------------------------------------------------ window optimization

class Keyframe:
    def __init__(self, fid: int, img, pose: Pose, a: float = 0.0, b: float = 0.0, fixed: bool = False):
        self.fid, self.img, self.pose, self.a, self.b, self.fixed = fid, img, pose, a, b, fixed


class Point:
    def __init__(self, host: int, u: float, v: float, d: float, fixed: bool = False):
        self.host, self.u, self.v, self.d, self.fixed = host, u, v, d, fixed


class Prior:
    """A quadratic prior -b^T x + x^T H x / 2 on the deltas x of some
    keyframes from their linearization point (pose_delta, a - a0, b - b0)."""

    def __init__(self, fids: List[int], H: Matrix, b: Vector, ref: Dict[int, Tuple[Pose, float, float]]):
        self.fids, self.H, self.b, self.ref = fids, H, b, ref

    def delta(self, kfs: Dict[int, Keyframe]) -> Vector:
        x = []
        for f in self.fids:
            pose, a0, b0 = self.ref[f]
            kf = kfs[f]
            x += pose_delta(kf.pose, pose) + [kf.a - a0, kf.b - b0]
        return x

    def energy(self, kfs: Dict[int, Keyframe]) -> float:
        x = self.delta(kfs)
        return -dot(self.b, x) + 0.5 * dot(x, matvec(self.H, x))


def schur_marginalize(H: Matrix, b: Vector, keep: List[int], drop: List[int]) -> Tuple[Matrix, Vector]:
    """H_kk - H_kd H_dd^-1 H_dk and b_k - H_kd H_dd^-1 b_d."""
    if not drop:
        return [[H[i][j] for j in keep] for i in keep], [b[i] for i in keep]
    Hdd = [[H[i][j] for j in drop] for i in drop]
    Hdk = [[H[i][j] for j in keep] for i in drop]
    X = solve(Hdd, [row + [b[i]] for row, i in zip(Hdk, drop)])  # H_dd^-1 [H_dk | b_d]
    Hn = [[H[i][j] - sum(H[i][drop[m]] * X[m][c] for m in range(len(drop))) for c, j in enumerate(keep)]
          for i in keep]
    bn = [b[i] - sum(H[i][drop[m]] * X[m][len(keep)] for m in range(len(drop))) for i in keep]
    return Hn, bn


def _system(kfs: Dict[int, Keyframe], points: List[Point], K, prior: Optional[Prior], huber_k: float,
            grad_c: float, skip_target: Optional[int] = None):
    """The Gauss-Newton system H x = b over the free keyframe blocks (8 each)
    and the free inverse depths (1 each), and the energy."""
    fidx: Dict[int, int] = {}
    for f in sorted(kfs):
        if not kfs[f].fixed:
            fidx[f] = 8 * len(fidx)
    nf = 8 * len(fidx)
    pidx = {}
    for k, p in enumerate(points):
        if not p.fixed:
            pidx[k] = nf + len(pidx)
    n = nf + len(pidx)
    H = [[0.0] * n for _ in range(n)]
    b = [0.0] * n
    energy = 0.0
    rels = {(i, j): relative(kfs[j].pose, kfs[i].pose) for i in kfs for j in kfs if i != j}
    for k, p in enumerate(points):
        h = kfs[p.host]
        for f, t in kfs.items():
            if f == p.host or f == skip_target:
                continue
            for o in PATTERN:
                res = residual(h.img, t.img, K, (p.u + o[0], p.v + o[1]), p.d, (h.pose, h.a, h.b),
                               (t.pose, t.a, t.b), True, rels[(p.host, f)])
                if res is None:
                    continue
                r, wp, _, jt, jh, jd = res
                wg = gradient_weight(wp, grad_c)
                energy += wg * huber(r, huber_k)
                w = wg * huber_weight(r, huber_k)
                cols = []
                if f in fidx:
                    cols += [(fidx[f] + x, jt[x]) for x in range(8)]
                if p.host in fidx:
                    cols += [(fidx[p.host] + x, jh[x]) for x in range(8)]
                if k in pidx:
                    cols.append((pidx[k], jd))
                for i, ji in cols:
                    b[i] -= w * ji * r
                    for j, jj in cols:
                        H[i][j] += w * ji * jj
    if prior is not None:
        x = prior.delta(kfs)
        energy += -dot(prior.b, x) + 0.5 * dot(x, matvec(prior.H, x))
        hx = matvec(prior.H, x)
        for a, fa in enumerate(prior.fids):
            if fa not in fidx:
                continue
            for i in range(8):
                b[fidx[fa] + i] += prior.b[8 * a + i] - hx[8 * a + i]
                for c, fc in enumerate(prior.fids):
                    if fc in fidx:
                        for j in range(8):
                            H[fidx[fa] + i][fidx[fc] + j] += prior.H[8 * a + i][8 * c + j]
    return H, b, energy, fidx, pidx


def window_energy(kfs, points, K, prior, huber_k=9.0, grad_c=50.0) -> float:
    e = 0.0
    rels = {(i, j): relative(kfs[j].pose, kfs[i].pose) for i in kfs for j in kfs if i != j}
    for p in points:
        h = kfs[p.host]
        for f, t in kfs.items():
            if f == p.host:
                continue
            for o in PATTERN:
                res = residual(h.img, t.img, K, (p.u + o[0], p.v + o[1]), p.d, (h.pose, h.a, h.b), (t.pose, t.a, t.b),
                               rel=rels[(p.host, f)])
                if res is not None:
                    e += gradient_weight(res[1], grad_c) * huber(res[0], huber_k)
    if prior is not None:
        e += prior.energy(kfs)
    return e


def optimize_window(kfs: Dict[int, Keyframe], points: List[Point], K, prior: Optional[Prior] = None,
                    iters: int = 6, huber_k: float = 9.0, grad_c: float = 50.0) -> List[float]:
    """Gauss-Newton on the window; the inverse depths are removed by the
    Schur complement (their block of H is diagonal). A step is kept only if
    the energy goes down. Returns the energy after each kept step."""
    history = [window_energy(kfs, points, K, prior, huber_k, grad_c)]
    for _ in range(iters):
        H, b, _, fidx, pidx = _system(kfs, points, K, prior, huber_k, grad_c)  # @line L8
        nf = 8 * len(fidx)
        dep = sorted(pidx.values())
        for i in dep:
            if H[i][i] <= 0.0:
                H[i][i] = 1e-12
        # Each residual has one inverse depth, so the depth block is diagonal and
        # the Schur complement costs O(n (8 N_f)^2) for n points.
        Hr = [H[i][:nf] for i in range(nf)]  # @line L9
        br = b[:nf]
        for i in dep:
            col = [H[x][i] for x in range(nf)]
            if not any(col):
                continue
            for x in range(nf):
                if col[x] == 0.0:
                    continue
                f = col[x] / H[i][i]
                br[x] -= f * b[i]
                row = Hr[x]
                for y in range(nf):
                    row[y] -= f * col[y]
        try:
            dx = solve(Hr, br) if nf else []  # @line L9
        except ValueError:
            break
        dd = {i: (b[i] - sum(H[i][j] * dx[j] for j in range(nf))) / H[i][i] for i in dep}  # @line L9
        saved = ({f: (kf.pose, kf.a, kf.b) for f, kf in kfs.items()}, [p.d for p in points])
        for f, s in fidx.items():
            kf = kfs[f]
            kf.pose = apply_update(kf.pose, dx[s:s + 6])
            kf.a, kf.b = kf.a + dx[s + 6], kf.b + dx[s + 7]
        for k, i in pidx.items():
            points[k].d = max(1e-6, points[k].d + dd[i])
        e = window_energy(kfs, points, K, prior, huber_k, grad_c)
        if not e < history[-1]:
            for f, (pose, a, bb) in saved[0].items():
                kfs[f].pose, kfs[f].a, kfs[f].b = pose, a, bb
            for p, d in zip(points, saved[1]):
                p.d = d
            break
        history.append(e)
    return history


def marginalize_keyframe(kfs: Dict[int, Keyframe], points: List[Point], K, prior: Optional[Prior], m: int,
                         huber_k: float = 9.0, grad_c: float = 50.0) -> Tuple[List[Point], Optional[Prior]]:
    """Remove keyframe m. Residuals of points of other hosts into m are
    dropped; the points hosted in m and the block of m are marginalized by
    the Schur complement into a new prior on the other free keyframes."""
    H, b, _, fidx, pidx = _system(kfs, points, K, prior, huber_k, grad_c, skip_target=m)  # @line L11
    drop = [pidx[k] for k, p in enumerate(points) if p.host == m and k in pidx]
    if m in fidx:
        drop += list(range(fidx[m], fidx[m] + 8))
    keep_f = [f for f in sorted(fidx) if f != m]
    keep = [fidx[f] + x for f in keep_f for x in range(8)]
    for i in drop:
        if H[i][i] <= 0.0:
            H[i][i] = 1e-12
    Hn, bn = schur_marginalize(H, b, keep, drop)  # @line L11
    ref = {f: (kfs[f].pose, kfs[f].a, kfs[f].b) for f in keep_f}
    new_prior = Prior(keep_f, Hn, bn, ref) if keep_f else None
    del kfs[m]
    return [p for p in points if p.host != m], new_prior


def choose_marginalized(kfs: Dict[int, Keyframe], points: List[Point], K, n_max: int, eps: float = 1e-3) -> Optional[int]:
    """The rule of the paper: the two newest keyframes stay; a keyframe with
    less than 5 percent of its points visible in the newest one goes; if
    still more than n_max remain, the one that maximizes
    sqrt(d(i, 1)) sum_j (d(i, j) + eps)^-1 goes, d being the distance of the
    camera centers and keyframe 1 the newest."""
    order = sorted(kfs)
    if len(order) <= 2:
        return None
    newest = kfs[order[-1]]
    for f in order[:-2]:
        own = [p for p in points if p.host == f]
        if own:
            seen = 0
            for p in own:
                q, _ = warp(K, (p.u, p.v), p.d, relative(newest.pose, kfs[f].pose))
                if q is not None and newest.img.sample(q[0], q[1]) is not None:
                    seen += 1
            if seen < 0.05 * len(own):
                return f
    if len(order) <= n_max:
        return None
    c1 = center(newest.pose)
    best, best_s = None, -1.0
    for f in order[:-2]:
        ci = center(kfs[f].pose)
        s = math.sqrt(norm([a - b for a, b in zip(ci, c1)])) * sum(
            1.0 / (norm([a - b for a, b in zip(ci, center(kfs[j].pose))]) + eps) for j in order[:-1] if j != f)
        if s > best_s:
            best, best_s = f, s
    return best


# ------------------------------------------------------------------ system

def run_dso(frames: Sequence[GridImage], K, first_depth, levels: int = 2, n_max: int = 3, block: int = 4,
            g_th: float = 3.0, wf: float = 1.0, wft: float = 1.0, wa: float = 1.0, t_kf: float = 2.0,
            d_range: Tuple[float, float] = (0.05, 1.0), win_iters: int = 6) -> Dict:
    """Run the pipeline on a list of images. first_depth(u, v) gives the
    inverse depth of a pixel of frame 0, which fixes the scale. Returns the
    poses and affine terms of all frames and the keyframe ids."""
    kfs: Dict[int, Keyframe] = {0: Keyframe(0, frames[0], (eye(3), [0.0, 0.0, 0.0]), fixed=True)}  # @line L1
    pts0 = select_points(frames[0], block, g_th)
    points = [Point(0, u, v, first_depth(u, v), fixed=(k == 0)) for k, (u, v) in enumerate(pts0)]  # @line L1
    prior: Optional[Prior] = None
    pyrs = {0: pyramid(frames[0], levels)}
    states = [((eye(3), [0.0, 0.0, 0.0]), 0.0, 0.0)]
    immature = [(u, v) for (u, v) in select_points(frames[0], block, g_th) if (u, v) not in set(pts0)]
    depth_guess: Dict[Tuple[int, int], float] = {}
    for j in range(1, len(frames)):  # @line L2
        last = max(kfs)
        kf = kfs[last]
        pyr = pyramid(frames[j], levels)
        prev = states[-1]
        if len(states) >= 2:
            motion = relative(states[-1][0], states[-2][0])
            guess_pose = (mul(motion[0], prev[0][0]), [a + b for a, b in zip(matvec(motion[0], prev[0][1]), motion[1])])
        else:
            guess_pose = prev[0]
        own = [(p.u, p.v, p.d) for p in points if p.host == last]
        state, _ = track_frame(own, pyrs[last], pyr, K, (kf.pose, kf.a, kf.b), (guess_pose, prev[1], prev[2]))  # @line L3
        states.append(state)
        for (u, v) in immature:  # @line L4
            got = search_depth(kf.img, frames[j], K, (u, v), (kf.pose, kf.a, kf.b), state, d_range[0], d_range[1])
            if got is not None:
                depth_guess[(u, v)] = got[0]  # @line L4
        if keyframe_score(own, K, (kf.pose, kf.a, kf.b), state, wf, wft, wa) <= t_kf:  # @line L5
            continue
        for (u, v), d in depth_guess.items():  # @line L6
            points.append(Point(last, u, v, d))  # @line L6
        kfs[j] = Keyframe(j, frames[j], state[0], state[1], state[2])  # @line L7
        pyrs[j] = pyr
        optimize_window(kfs, points, K, prior, iters=win_iters)  # @line L8
        m = choose_marginalized(kfs, points, K, n_max)  # @line L10
        if m is not None:
            points, prior = marginalize_keyframe(kfs, points, K, prior, m)  # @line L11
        for f, k in kfs.items():
            states[f] = (k.pose, k.a, k.b)
        used = {(p.u, p.v) for p in points if p.host == j}
        immature = [q for q in select_points(frames[j], block, g_th) if q not in used]  # @line L12
        depth_guess = {}
    return {"states": states, "keyframes": sorted(kfs), "points": points, "prior": prior}  # @line L13
