# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/global-structure-from-motion/. The authors are listed in prov/JSXC11.jsonl.

"""Global structure from motion with a known intrinsic matrix K.

The input is K and a list of tracks. A track is a dict {image: (u, v)}
of the pixels of one 3D point. The output is a pose (R, t) for every
image of the largest connected part of the view graph, with
X_c = R X + t, and a 3D point for every track that could be
triangulated. The first image of that part has R = I and t = 0; the
scale is arbitrary.

The pipeline solves for all cameras at once instead of one by one:
1. relative poses of all image pairs with enough common tracks (RANSAC
   on the 8-point method), which give the view graph;
2. robust rotation averaging in the Lie algebra (an l1 start, then
   Geman-McClure weights);
3. removal of the edges that disagree with the averaged rotations;
4. unit directions between the camera centers, from the relative
   translations and the averaged rotations;
5. linear translation averaging: the centers that best fit the
   directions, as the smallest eigenvector of a block Laplacian;
6. triangulation of all tracks, then one bundle adjustment and the
   removal of observations with a reprojection error above tau.
"""

import math
import random
from collections import deque
from typing import Dict, List, Sequence, Tuple

from cvgeom import axis_angle_to_R
from cvla import det, dot, inv, matvec, mul, nullvec, solve, svd, sym_eig, transpose

Vector = List[float]
Matrix = List[List[float]]
Pose = Tuple[Matrix, Vector]
Edge = Tuple[int, int, Matrix]
EYE3 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]


# ------------------------------------------------------------ two-view geometry

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
    """E with x2^T E x1 = 0, projected to singular values (1, 1, 0)."""
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
    """RANSAC on the 8-point method with a local refit: each new best model
    is fitted again to its inliers. Returns the pose and the inlier indices."""
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
            for _ in range(3):
                e2 = eight_point_essential([x1[k] for k in inl], [x2[k] for k in inl])
                inl2 = [k for k in range(n) if sampson(e2, x1[k], x2[k]) < tau]
                if len(inl2) < len(inl):
                    break
                e, inl = e2, inl2
            if len(inl) > len(best):
                best, best_e = inl, e
                need = ransac_count(len(best) / n, 8, cap)
    pose = decompose_essential(best_e, [x1[k] for k in best], [x2[k] for k in best])
    return pose, best


# ------------------------------------------------------------ rotation averaging

def so3_exp(w: Sequence[float]) -> Matrix:
    """exp([w]_x) by the Rodrigues formula."""
    th = math.sqrt(w[0] * w[0] + w[1] * w[1] + w[2] * w[2])
    if th < 1e-8:
        a, b = 1.0 - th * th / 6.0, 0.5 - th * th / 24.0
    else:
        a, b = math.sin(th) / th, (1.0 - math.cos(th)) / (th * th)
    x, y, z = w
    k = [[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]]
    k2 = mul(k, k)
    return [[(1.0 if i == j else 0.0) + a * k[i][j] + b * k2[i][j] for j in range(3)] for i in range(3)]


def so3_log(r: Sequence[Sequence[float]]) -> Vector:
    """The rotation vector w with exp([w]_x) = R and ||w|| <= pi."""
    c = max(-1.0, min(1.0, (r[0][0] + r[1][1] + r[2][2] - 1.0) / 2.0))
    v = [r[2][1] - r[1][2], r[0][2] - r[2][0], r[1][0] - r[0][1]]
    th = math.acos(c)
    if th < 1e-6:
        return [x * (0.5 + th * th / 12.0) for x in v]
    if th < math.pi - 1e-4:
        return [x * th / (2.0 * math.sin(th)) for x in v]
    b = [[(r[i][j] + r[j][i]) / 2.0 - (c if i == j else 0.0) for j in range(3)] for i in range(3)]
    k = max(range(3), key=lambda i: b[i][i])
    col = [b[i][k] for i in range(3)]
    nc = math.sqrt(sum(x * x for x in col))
    a = [x / nc for x in col]
    if sum(x * y for x, y in zip(a, v)) < 0:
        a = [-x for x in a]
    return [th * x for x in a]


def angle(r1: Sequence[Sequence[float]], r2: Sequence[Sequence[float]]) -> float:
    """The angle of R1^T R2, in radians."""
    tr = sum(r1[k][i] * r2[k][i] for i in range(3) for k in range(3))
    return math.acos(max(-1.0, min(1.0, (tr - 1.0) / 2.0)))


def _tree_init(n: int, edges: Sequence[Edge]) -> List[Matrix]:
    adj: Dict[int, List[Tuple[int, Matrix]]] = {k: [] for k in range(n)}
    for i, j, rij in edges:
        adj[i].append((j, rij))
        adj[j].append((i, transpose(rij)))
    rots: List = [None] * n
    rots[0] = [list(row) for row in EYE3]
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for j, rij in adj[i]:
            if rots[j] is None:
                rots[j] = mul(rij, rots[i])
                queue.append(j)
    if any(r is None for r in rots):
        raise ValueError("rotation averaging: the view graph is not connected")
    return rots


def _irls_rotations(n: int, edges: Sequence[Edge], rots: List[Matrix], loss: str,
                    sigma: float, iters: int) -> List[Matrix]:
    """Lie-algebraic iterations with the weights of the loss ("l1" or "gm")."""
    for _ in range(iters):
        lap = [[0.0] * n for _ in range(n)]
        b = [[0.0] * 3 for _ in range(n)]
        for i, j, rij in edges:
            r = so3_log(mul(mul(transpose(rots[j]), rij), rots[i]))
            rn = math.sqrt(dot(r, r))
            w = 1.0 / max(rn, 1e-6) if loss == "l1" else sigma * sigma / (rn * rn + sigma * sigma) ** 2
            lap[i][i] += w
            lap[j][j] += w
            lap[i][j] -= w
            lap[j][i] -= w
            for a in range(3):
                b[j][a] += w * r[a]
                b[i][a] -= w * r[a]
        omega = [[0.0, 0.0, 0.0]] + solve([row[1:] for row in lap[1:]], b[1:])
        rots = [mul(r, so3_exp(w)) for r, w in zip(rots, omega)]
        if max(math.sqrt(dot(w, w)) for w in omega) < 1e-10:
            break
    return rots


def average_rotations(n: int, edges: Sequence[Edge], sigma: float = 0.1) -> List[Matrix]:
    """Robust rotation averaging: tree start, l1 iterations, then
    Geman-McClure iterations. R_0 = I."""
    rots = _tree_init(n, edges)
    rots = _irls_rotations(n, edges, rots, "l1", sigma, 30)
    return _irls_rotations(n, edges, rots, "gm", sigma, 30)


# ------------------------------------------------------------ translation averaging

def directions(rots: Sequence[Matrix], rel: Dict[Tuple[int, int], Pose]) -> Dict[Tuple[int, int], Vector]:
    """v_ij = -R_j^T t_ij / ||t_ij||, the unit vector from c_i to c_j."""
    out = {}
    for (i, j), (_, t) in rel.items():
        d = [-x for x in matvec(transpose(rots[j]), t)]
        nd = math.sqrt(dot(d, d))
        out[(i, j)] = [x / nd for x in d]
    return out


def direction_matrix(n: int, dirs: Dict[Tuple[int, int], Vector]) -> Matrix:
    """The 3(n-1) x 3(n-1) matrix of sum ||(I - v v^T)(c_j - c_i)||^2 with
    c_0 = 0 removed."""
    m = [[0.0] * (3 * n) for _ in range(3 * n)]
    for (i, j), v in dirs.items():
        p = [[(1.0 if a == b else 0.0) - v[a] * v[b] for b in range(3)] for a in range(3)]
        for a in range(3):
            for b in range(3):
                m[3 * i + a][3 * i + b] += p[a][b]
                m[3 * j + a][3 * j + b] += p[a][b]
                m[3 * i + a][3 * j + b] -= p[a][b]
                m[3 * j + a][3 * i + b] -= p[a][b]
    return [row[3:] for row in m[3:]]


def translation_averaging(n: int, dirs: Dict[Tuple[int, int], Vector]) -> List[Vector]:
    """Centers c_i with c_0 = 0 and sum ||c_i||^2 = 1 that minimize the
    sum of ||(I - v_ij v_ij^T)(c_j - c_i)||^2, with the sign that makes
    the directions point the right way."""
    _, vecs = sym_eig(direction_matrix(n, dirs))
    x = [row[0] for row in vecs]
    cs = [[0.0, 0.0, 0.0]] + [x[3 * k:3 * k + 3] for k in range(n - 1)]
    s = sum(dot(v, [cs[j][a] - cs[i][a] for a in range(3)]) for (i, j), v in dirs.items())
    if s < 0:
        cs = [[-a for a in c] for c in cs]
    return cs


# ------------------------------------------------------------ bundle adjustment

def _blocks(pose: Pose, x: Sequence[float], p: Sequence[float]):
    r, t = pose
    rx = matvec(r, x)
    c = [rx[a] + t[a] for a in range(3)]
    iz = 1.0 / c[2]
    res = [c[0] * iz - p[0], c[1] * iz - p[1]]
    d = [[iz, 0.0, -c[0] * iz * iz], [0.0, iz, -c[1] * iz * iz]]
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

def build_view_graph(xn: Sequence[Dict[int, Vector]], tau: float, rng: random.Random,
                     min_pair: int = 12) -> Dict[Tuple[int, int], Tuple[Pose, int]]:
    """Relative pose and inlier count of every image pair (i < j) with at
    least min_pair common tracks and min_pair inliers."""
    common: Dict[Tuple[int, int], List[int]] = {}
    for j, tr in enumerate(xn):
        ims = sorted(tr)
        for x in range(len(ims)):
            for y in range(x + 1, len(ims)):
                common.setdefault((ims[x], ims[y]), []).append(j)
    graph = {}
    for (a, b) in sorted(common):
        js = common[(a, b)]
        if len(js) < min_pair:
            continue
        pose, inl = relative_pose_ransac([xn[j][a] for j in js], [xn[j][b] for j in js], tau, rng)
        if len(inl) >= min_pair:
            graph[(a, b)] = (pose, len(inl))
    return graph


def largest_component(images: Sequence[int], pairs) -> List[int]:
    adj: Dict[int, List[int]] = {i: [] for i in images}
    for a, b in pairs:
        adj[a].append(b)
        adj[b].append(a)
    seen, best = set(), []
    for s in sorted(images):
        if s in seen:
            continue
        comp, queue = [], deque([s])
        seen.add(s)
        while queue:
            i = queue.popleft()
            comp.append(i)
            for k in adj[i]:
                if k not in seen:
                    seen.add(k)
                    queue.append(k)
        if len(comp) > len(best):
            best = sorted(comp)
    return best


def filter_edges(rots: Sequence[Matrix], rel: Dict[Tuple[int, int], Pose],
                 max_angle: float) -> Dict[Tuple[int, int], Pose]:
    """Keep the edges with angle(R_ij, R_j R_i^T) <= max_angle."""
    return {(i, j): (r, t) for (i, j), (r, t) in rel.items()
            if angle(r, mul(rots[j], transpose(rots[i]))) <= max_angle}


def global_structure_from_motion(K: Matrix, tracks: Sequence[Dict[int, Sequence[float]]],
                                 tau_px: float = 3.0, max_angle: float = 0.1,
                                 min_pair: int = 12, seed: int = 0):
    """Returns (cams, pts, obs): cams[i] = (R, t), pts[j] = X for track j,
    and obs, the set of (image, track) pairs that were kept."""
    rng = random.Random(seed)
    kinv = inv(K)
    tau = tau_px / K[0][0]
    xn = [{i: normalize(kinv, p) for i, p in tr.items()} for tr in tracks]
    graph = build_view_graph(xn, tau, rng, min_pair)  # @line L1
    images = largest_component(sorted({i for tr in tracks for i in tr}), graph)
    idx = {im: k for k, im in enumerate(images)}
    n = len(images)
    rel = {(idx[a], idx[b]): pose for (a, b), (pose, _) in graph.items() if a in idx and b in idx}
    rots = average_rotations(n, [(i, j, r) for (i, j), (r, _) in rel.items()])  # @line L2
    rel = filter_edges(rots, rel, max_angle)  # @line L3
    if len(largest_component(range(n), rel)) < n:
        raise ValueError("global SfM: the filtered view graph is not connected")
    dirs = directions(rots, rel)  # @line L4
    centers = translation_averaging(n, dirs)  # @line L5
    cams: Dict[int, Pose] = {images[k]: (rots[k], [-x for x in matvec(rots[k], centers[k])])
                             for k in range(n)}  # @line L6
    pts: Dict[int, Vector] = {}
    obs: Dict[Tuple[int, int], Vector] = {}
    for j, tr in enumerate(xn):  # @line L7
        views = [i for i in tr if i in cams]
        if len(views) < 2:
            continue
        x = triangulate([cams[i] for i in views], [tr[i] for i in views])
        good = [i for i in views if reproj_error(cams[i], x, tr[i]) < 10 * tau]
        if 2 <= len(good) < len(views):
            x = triangulate([cams[i] for i in good], [tr[i] for i in good])
            good = [i for i in good if reproj_error(cams[i], x, tr[i]) < 10 * tau]
        if len(good) >= 2:
            pts[j] = x
            for i in good:
                obs[(i, j)] = tr[i]
    cams, pts = bundle_adjust(cams, pts, obs, images[0])  # @line L8
    for key in [k for k in obs if reproj_error(cams[k[0]], pts[k[1]], obs[k]) > tau]:  # @line L9
        del obs[key]
    for j in list(pts):
        if sum(1 for (_, jj) in obs if jj == j) < 2:
            del pts[j]
            for key in [k for k in obs if k[1] == j]:
                del obs[key]
    cams, pts = bundle_adjust(cams, pts, obs, images[0])
    return cams, pts, set(obs)  # @line L10
