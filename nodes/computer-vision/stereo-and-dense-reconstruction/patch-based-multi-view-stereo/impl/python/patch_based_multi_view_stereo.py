# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/patch-based-multi-view-stereo/. The authors are listed in prov/22G2KD.jsonl.

"""Patch-based multi-view stereo (PMVS): match, expand, filter.

A camera is (K, R, t): a world point X maps to the camera frame by
Xc = R X + t, and to the pixel K Xc divided by its third entry. Images are
lists of rows of gray values, img[v][u]. A patch is a small square in space
with a center c, a unit normal n pointing toward its reference camera, a
reference image ref, a list V of images where it may be visible and a list
Vs of images where it is photo-consistent (Vs holds ref).

The steps follow Furukawa and Ponce (2010). The values of the parameters
and two details are choices of this code: the refinement is a pattern
search instead of conjugate gradient, and the filter is one rule of the
regularization kind (see the page).
"""

import math

INF = float("inf")


# ------------------------------------------------------------ 3D vectors

def add(a, b):
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]


def sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def mul(a, s):
    return [a[0] * s, a[1] * s, a[2] * s]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def unit(a):
    s = math.sqrt(dot(a, a))
    return [a[0] / s, a[1] / s, a[2] / s]


def rmul(R, x):
    return [dot(R[0], x), dot(R[1], x), dot(R[2], x)]


def rtmul(R, x):
    """R^T x."""
    return [R[0][i] * x[0] + R[1][i] * x[1] + R[2][i] * x[2] for i in range(3)]


# --------------------------------------------------------------- cameras

def to_camera(cam, X):
    K, R, t = cam
    return add(rmul(R, X), t)


def project(cam, X):
    """Pixel (u, v) of X, or None if X is not in front of the camera."""
    K = cam[0]
    x = to_camera(cam, X)
    if x[2] <= 1e-12:
        return None
    a, b = x[0] / x[2], x[1] / x[2]
    return (K[0][0] * a + K[0][1] * b + K[0][2], K[1][1] * b + K[1][2])


def camera_matrix(cam):
    """The rows of P = K [R | t]."""
    K, R, t = cam
    Rt = [list(R[i]) + [t[i]] for i in range(3)]
    return [[sum(K[i][k] * Rt[k][j] for k in range(3)) for j in range(4)] for i in range(3)]


def center(cam):
    """C = -R^T t."""
    return mul(rtmul(cam[1], cam[2]), -1.0)


def ray(cam, u, v):
    """Unit direction, in the world, of the ray through the pixel (u, v)."""
    K, R, _ = cam
    y = (v - K[1][2]) / K[1][1]
    x = (u - K[0][2] - K[0][1] * y) / K[0][0]
    return unit(rtmul(R, [x, y, 1.0]))


def depth(cam, X):
    return to_camera(cam, X)[2]


def midpoint_triangulate(c1, d1, c2, d2):
    """Midpoint of the common perpendicular of two rays c + s d, or None if
    they are parallel or meet behind a camera."""
    w = sub(c1, c2)
    a, b, c = dot(d1, d1), dot(d1, d2), dot(d2, d2)
    d, e = dot(d1, w), dot(d2, w)
    den = a * c - b * b
    if abs(den) < 1e-12:
        return None
    s = (b * e - c * d) / den
    r = (a * e - b * d) / den
    if s <= 0 or r <= 0:
        return None
    return mul(add(add(c1, mul(d1, s)), add(c2, mul(d2, r))), 0.5)


# --------------------------------------------------------------- patches

class Patch:
    __slots__ = ("c", "n", "ref", "V", "Vs", "g")

    def __init__(self, c, n, ref):
        self.c, self.n, self.ref = c, n, ref
        self.V, self.Vs, self.g = [], [], INF


class Params:
    def __init__(self, mu=5, beta=3, gamma=2, alpha=0.3, max_angle=60.0, epipolar=2.0,
                 rounds=3, min_fraction=0.25, max_evals=30):
        self.mu = mu                  # the patch grid is mu x mu
        self.beta = beta              # cells are beta x beta pixels
        self.gamma = gamma            # least size of Vs
        self.alpha = alpha            # h <= alpha means photo-consistent (NCC >= 1 - alpha)
        self.max_angle = max_angle    # largest angle between n and the viewing ray, in degrees
        self.epipolar = epipolar      # largest distance to the epipolar line, in pixels
        self.rounds = rounds          # rounds of expansion and filtering
        self.min_fraction = min_fraction
        self.max_evals = max_evals


class Model:
    """The images, the cameras, the cells and the patches."""

    def __init__(self, images, cams, prm):
        self.images, self.cams, self.prm = images, cams, prm
        self.centers = [center(c) for c in cams]
        self.P = [camera_matrix(c) for c in cams]
        self.patches = []
        self.cells = [dict() for _ in images]   # cells[i][(cx, cy)] = list of patches

    def cell_of(self, i, X):
        p = project(self.cams[i], X)
        if p is None:
            return None
        h, w = len(self.images[i]), len(self.images[i][0])
        if not (0.0 <= p[0] < w and 0.0 <= p[1] < h):
            return None
        b = self.prm.beta
        return (int(p[0]) // b, int(p[1]) // b)

    def cell_count(self, i):
        h, w = len(self.images[i]), len(self.images[i][0])
        b = self.prm.beta
        return (w + b - 1) // b, (h + b - 1) // b

    def register(self, p):
        for i in p.Vs:
            cell = self.cell_of(i, p.c)
            if cell is not None:
                self.cells[i].setdefault(cell, []).append(p)
        self.patches.append(p)

    def unregister(self, p):
        for i in p.Vs:
            cell = self.cell_of(i, p.c)
            if cell is not None and cell in self.cells[i]:
                lst = self.cells[i][cell]
                lst[:] = [q for q in lst if q is not p]
                if not lst:
                    del self.cells[i][cell]

    # ---------------------------------------------- photometric discrepancy

    def spacing(self, p):
        """Size of one grid step: one pixel of the reference image at c."""
        K = self.cams[p.ref][0]
        return depth(self.cams[p.ref], p.c) / K[0][0]

    def grid(self, p):
        cam = self.cams[p.ref]
        yaxis = rtmul(cam[1], [0.0, 1.0, 0.0])
        ex = cross(yaxis, p.n)
        if dot(ex, ex) < 1e-12:
            ex = cross([1.0, 0.0, 0.0], p.n)
        ex = unit(ex)
        ey = cross(p.n, ex)
        s = self.spacing(p)
        m = self.prm.mu
        half = (m - 1) / 2.0
        return [add(p.c, add(mul(ex, (a - half) * s), mul(ey, (b - half) * s)))
                for b in range(m) for a in range(m)]

    def samples(self, i, pts):
        """Bilinear samples of image i at the projections of pts, or None
        if one of them falls outside the image."""
        out = []
        img = self.images[i]
        h, w = len(img), len(img[0])
        (a0, a1, a2, a3), (b0, b1, b2, b3), (c0, c1, c2, c3) = self.P[i]
        for x, y, z in pts:
            zc = c0 * x + c1 * y + c2 * z + c3
            if zc <= 1e-12:
                return None
            u = (a0 * x + a1 * y + a2 * z + a3) / zc
            v = (b0 * x + b1 * y + b2 * z + b3) / zc
            if not (0.0 <= u <= w - 1 and 0.0 <= v <= h - 1):
                return None
            iu, jv = min(int(u), w - 2), min(int(v), h - 2)
            fu, fv = u - iu, v - jv
            r0, r1 = img[jv], img[jv + 1]
            out.append((1 - fu) * (1 - fv) * r0[iu] + fu * (1 - fv) * r0[iu + 1]
                       + (1 - fu) * fv * r1[iu] + fu * fv * r1[iu + 1])
        return out

    def h(self, p, i, pts=None, ref_samples=None):
        """1 - NCC of the patch grid in image i and in the reference image."""
        pts = pts if pts is not None else self.grid(p)
        a = ref_samples if ref_samples is not None else self.samples(p.ref, pts)
        b = self.samples(i, pts)
        if a is None or b is None:
            return 2.0
        m = len(a)
        ma, mb = sum(a) / m, sum(b) / m
        sab = sum((x - ma) * (y - mb) for x, y in zip(a, b))
        saa = sum((x - ma) ** 2 for x in a)
        sbb = sum((y - mb) ** 2 for y in b)
        if saa < 1e-9 or sbb < 1e-9:
            return 1.0
        return 1.0 - sab / math.sqrt(saa * sbb)

    def g_star(self, p, views):
        """Mean discrepancy over the views other than the reference."""
        others = [i for i in views if i != p.ref]
        if not others:
            return INF
        pts = self.grid(p)
        a = self.samples(p.ref, pts)
        if a is None:
            return INF
        return sum(self.h(p, i, pts, a) for i in others) / len(others)

    def visible(self, p):
        """V(p): images that see c inside the image at an angle below max_angle."""
        out = []
        cosmax = math.cos(math.radians(self.prm.max_angle))
        for i, cam in enumerate(self.cams):
            if self.cell_of(i, p.c) is None:
                continue
            if dot(p.n, unit(sub(self.centers[i], p.c))) >= cosmax or i == p.ref:
                out.append(i)
        return out

    def consistent(self, p):
        """V*(p): the reference and the images of V(p) with h <= alpha."""
        pts = self.grid(p)
        a = self.samples(p.ref, pts)
        if a is None:
            return []
        return [i for i in p.V if i == p.ref or self.h(p, i, pts, a) <= self.prm.alpha]

    # ------------------------------------------------------------ refine

    def refine(self, p):
        """Minimize g* over the depth of c along the reference ray and the
        two slopes of n in the reference frame, by pattern search."""
        cam = self.cams[p.ref]
        C = self.centers[p.ref]
        d = unit(sub(p.c, C))
        nc = rmul(cam[1], p.n)             # the normal in the reference frame
        if nc[2] >= -1e-6:
            return
        x = [math.sqrt(dot(sub(p.c, C), sub(p.c, C))), -nc[0] / nc[2], -nc[1] / nc[2]]

        def place(v):
            return add(C, mul(d, v[0])), unit(rtmul(cam[1], [v[1], v[2], -1.0]))

        def cost(v):
            if v[0] <= 0:
                return INF
            p.c, p.n = place(v)
            return self.g_star(p, p.Vs)

        best = cost(x)
        steps = [2.0 * self.spacing(p), 0.25, 0.25]
        evals = 1
        while evals < self.prm.max_evals and steps[1] > 0.01:
            moved = False
            for k in range(3):
                for sgn in (1.0, -1.0):
                    y = list(x)
                    y[k] += sgn * steps[k]
                    cy = cost(y)
                    evals += 1
                    if cy < best:
                        x, best, moved = y, cy, True
                        break
            if not moved:
                steps = [s / 2.0 for s in steps]
        p.c, p.n = place(x)
        p.g = best

    def accept(self, p):
        """Refine p, recompute V and V*, and decide."""
        p.V = self.visible(p)
        p.Vs = self.consistent(p)
        if len(p.Vs) < 2:
            return False
        self.refine(p)
        p.V = self.visible(p)
        if p.ref not in p.V:
            return False
        p.Vs = self.consistent(p)
        p.g = self.g_star(p, p.Vs)
        return len(p.Vs) >= self.prm.gamma


# ------------------------------------------------------------- the steps

def match(model, features):
    """Initial matching. features[i] is a list of pixels (u, v) of image i."""
    prm = model.prm
    for i, feats in enumerate(features):                          # @line L1
        cam_i = model.cams[i]
        for (u, v) in feats:
            b = prm.beta
            if model.cells[i].get((int(u) // b, int(v) // b)):     # @line L2
                continue
            Ci, di = model.centers[i], ray(cam_i, u, v)
            cands = []
            for j, feats_j in enumerate(features):
                if j == i:
                    continue
                e0 = project(model.cams[j], add(Ci, mul(di, 1.0)))
                e1 = project(model.cams[j], add(Ci, mul(di, 100.0)))
                if e0 is None or e1 is None:
                    continue
                lx, ly = e1[0] - e0[0], e1[1] - e0[1]
                ln = math.hypot(lx, ly)
                for (u2, v2) in feats_j:
                    if ln > 0 and abs((u2 - e0[0]) * ly - (v2 - e0[1]) * lx) / ln > prm.epipolar:
                        continue                                   # @line L3
                    X = midpoint_triangulate(Ci, di, model.centers[j], ray(model.cams[j], u2, v2))
                    if X is not None:
                        cands.append(X)
            cands.sort(key=lambda X: dot(sub(X, Ci), sub(X, Ci)))   # @line L4
            for X in cands:
                p = Patch(X, unit(sub(Ci, X)), i)                  # @line L5
                if model.accept(p):                                # @line L6
                    model.register(p)                              # @line L7
                    break


def neighbors(p, q, rho):
    """The relation of the paper: q lies near the plane of p and p near the plane of q."""
    w = sub(p.c, q.c)
    return abs(dot(w, p.n)) + abs(dot(w, q.n)) < 2.0 * rho


def expand(model, start):
    """Expand from the patches in start, then from every new patch."""
    queue = list(start)
    k = 0
    while k < len(queue):                                          # @line L9
        p = queue[k]
        k += 1
        if p not in model.patches:
            continue
        for i in list(p.Vs):
            cell = model.cell_of(i, p.c)
            if cell is None:
                continue
            nx, ny = model.cell_count(i)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                tgt = (cell[0] + dx, cell[1] + dy)
                if not (0 <= tgt[0] < nx and 0 <= tgt[1] < ny):
                    continue
                if model.cells[i].get(tgt):                        # @line L10
                    continue
                b = model.prm.beta
                u = min(tgt[0] * b + (b - 1) / 2.0, len(model.images[i][0]) - 1)
                v = min(tgt[1] * b + (b - 1) / 2.0, len(model.images[i]) - 1)
                Ci, di = model.centers[i], ray(model.cams[i], u, v)
                den = dot(di, p.n)
                if abs(den) < 1e-9:
                    continue
                s = dot(sub(p.c, Ci), p.n) / den                   # @line L11
                if s <= 0:
                    continue
                q = Patch(add(Ci, mul(di, s)), list(p.n), p.ref)  # @line L12
                if model.cell_of(p.ref, q.c) is None:
                    continue
                if model.accept(q) and i in q.Vs and model.cell_of(i, q.c) == tgt:  # @line L13
                    model.register(q)                              # @line L14
                    queue.append(q)


def filter_patches(model):
    """Remove p when few patches in the cells around it in the images of
    V*(p) are its neighbors. Returns the number removed."""
    remove = []
    for p in model.patches:                                        # @line L15
        rho = 2.0 * model.spacing(p)
        seen, near = 0, 0
        others = set()
        for i in p.Vs:
            cell = model.cell_of(i, p.c)
            if cell is None:
                continue
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for q in model.cells[i].get((cell[0] + dx, cell[1] + dy), ()):
                        if q is not p and id(q) not in others:
                            others.add(id(q))
                            seen += 1
                            near += neighbors(p, q, rho)
        if seen > 0 and near < model.prm.min_fraction * seen:      # @line L16
            remove.append(p)
    gone = set(id(p) for p in remove)
    for p in remove:
        model.unregister(p)
    model.patches = [p for p in model.patches if id(p) not in gone]
    return len(remove)


def pmvs(images, cams, features, prm=None):
    """Run match, then rounds of expand and filter. Returns the model."""
    prm = prm or Params()
    model = Model(images, cams, prm)
    match(model, features)
    for _ in range(prm.rounds):                                    # @line L8
        expand(model, model.patches)
        filter_patches(model)
    return model                                                   # @line L17
