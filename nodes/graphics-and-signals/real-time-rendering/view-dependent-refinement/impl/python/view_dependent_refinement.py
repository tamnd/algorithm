# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/view-dependent-refinement/. The authors are listed in prov/TRTDD8.jsonl.

"""View-dependent refinement of a progressive mesh, after Hoppe (1997).

The mesh is a height field: vertex positions are (x, y, z) with y up and the
domain plane is (x, z). A face (a, b, c) is counterclockwise seen from +y.

Build: a progressive mesh by half-edge collapses (v_t, v_u) -> v_s, where v_s
is a new vertex at the position of v_t. The vertex hierarchy is the binary
forest of these collapses; its leaves are the vertices of the full mesh M^n
and its roots are the vertices of the base mesh M^0.

Run time: the active vertices form a front of the forest. A face of M^n is in
the selectively refined mesh when the active ancestors of its three corners
are distinct, and its corners are those active ancestors. A vsplit replaces
v_s by v_t and v_u; an ecol does the reverse. Hoppe's legality conditions
decide which of these may happen.
"""

from math import sqrt


def orient(a, b, c):
    """Twice the signed area of (a, b, c) in the domain plane, positive if counterclockwise from +y."""
    return (b[2] - a[2]) * (c[0] - a[0]) - (b[0] - a[0]) * (c[2] - a[2])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def grid_mesh(rng, g, amp=3):
    """A (g+1) x (g+1) height grid with integer heights. Returns positions, faces, border flags."""
    pos, border = [], []
    for i in range(g + 1):
        for j in range(g + 1):
            pos.append((i, rng.randint(0, amp), j))
            border.append(i in (0, g) or j in (0, g))
    faces = []
    for i in range(g):
        for j in range(g):
            a, b, c, d = i * (g + 1) + j, i * (g + 1) + j + 1, (i + 1) * (g + 1) + j + 1, (i + 1) * (g + 1) + j
            faces.append((a, b, c))
            faces.append((a, c, d))
    return pos, faces, border


class ProgressiveMesh:
    """The vertex hierarchy and the vsplit records, built by half-edge collapses."""

    def __init__(self, rng, pos, faces, border):
        self.pos = list(pos)
        self.faces = list(faces)
        self.n_leaves = len(pos)
        self.parent = {}
        self.children = {}
        self.rec = {}
        self.creator = {}
        bord = list(border)
        cur = {f: list(c) for f, c in enumerate(faces)}
        star = {v: set() for v in range(len(pos))}
        for f, c in cur.items():
            for v in c:
                star[v].add(f)
        order = []
        while True:
            cands = []
            for f, c in cur.items():
                for k in range(3):
                    t, u = c[k], c[(k + 1) % 3]
                    if not bord[u]:
                        rec = self._check(cur, star, t, u)
                        if rec is not None:
                            cands.append(rec)
            if not cands:
                break
            cands.sort()
            t, u, fl, fr, vl, vr, fn = rng.choice(cands)
            s = len(self.pos)
            self.pos.append(self.pos[t])
            bord.append(bord[t])
            self.parent[t] = self.parent[u] = s
            self.children[s] = (t, u)
            self.rec[s] = (fl, fr, fn)
            self.creator[fl] = self.creator[fr] = s
            star[s] = set()
            for f in star[t] | star[u]:
                if f in (fl, fr):
                    continue
                cur[f] = [s if v in (t, u) else v for v in cur[f]]
                star[s].add(f)
            for f in (fl, fr):
                for v in cur[f]:
                    star[v].discard(f)
                del cur[f]
            del star[t], star[u]
            order.append(s)
        self.order = order[::-1]  # vsplit order: coarse to fine
        self.index = {s: i for i, s in enumerate(self.order)}
        self.roots = sorted(star)
        self.base_faces = {f: tuple(c) for f, c in cur.items()}

    def _check(self, cur, star, t, u):
        both = [f for f in star[t] & star[u]]
        if len(both) != 2:
            return None
        fl = fr = None
        for f in both:
            c = cur[f]
            k = c.index(t)
            if c[(k + 1) % 3] == u:
                fl, vl = f, c[(k + 2) % 3]
            else:
                fr, vr = f, c[(k + 1) % 3]
        if fl is None or fr is None:
            return None
        nt = {v for f in star[t] for v in cur[f]} - {t}
        nu = {v for f in star[u] for v in cur[f]} - {u}
        if nt & nu != {vl, vr}:
            return None

        def across(a, b, skip):
            for f in star[a] & star[b]:
                if f != skip:
                    return f
            return None

        fn = (across(vl, t, fl), across(u, vl, fl), across(t, vr, fr), across(vr, u, fr))
        if None in fn or len(set(fn)) != 4:
            return None
        pt = self.pos[t]
        for f in star[u]:
            if f in (fl, fr):
                continue
            q = [pt if v == u else self.pos[v] for v in cur[f]]
            if orient(*q) <= 0:
                return None
        return (t, u, fl, fr, vl, vr, fn)

    def leaves(self, v):
        out, stack = [], [v]
        while stack:
            w = stack.pop()
            if w in self.children:
                stack.extend(self.children[w])
            else:
                out.append(w)
        return out


class SelectiveMesh:
    def __init__(self, pm):
        self.pm = pm
        self.active = set(pm.roots)

    def rep(self, w):
        while w not in self.active:
            w = self.pm.parent[w]
        return w

    def face(self, f):
        c = tuple(self.rep(w) for w in self.pm.faces[f])
        return c if len(set(c)) == 3 else None

    def faces(self):
        out = {}
        for f in range(len(self.pm.faces)):
            c = self.face(f)
            if c is not None:
                out[f] = c
        return out

    def is_split(self, v):
        w = v
        while True:
            if w in self.active:
                return False
            if w not in self.pm.parent:
                return True
            w = self.pm.parent[w]

    def vsplit_legal(self, v):
        if v not in self.active or v not in self.pm.children:
            return False
        return all(self.face(f) is not None for f in self.pm.rec[v][2])  # @line L1

    def ecol_legal(self, v):
        pm = self.pm
        if v not in pm.children:
            return False
        t, u = pm.children[v]
        if t not in self.active or u not in self.active:
            return False
        fl, fr, fn = pm.rec[v]
        cl, cr = self.face(fl), self.face(fr)
        x = next(w for w in cl if w not in (t, u))
        y = next(w for w in cr if w not in (t, u))
        want = (((x, t), fl, fn[0]), ((u, x), fl, fn[1]), ((t, y), fr, fn[2]), ((y, u), fr, fn[3]))
        for (a, b), own, other in want:  # @line L2
            got = [f for f in range(len(pm.faces)) if f != own and self._has_edge(f, a, b)]
            if got != [other]:
                return False
        return True

    def _has_edge(self, f, a, b):
        c = self.face(f)
        return c is not None and a in c and b in c

    def vsplit(self, v):
        self.active.remove(v)
        self.active.update(self.pm.children[v])

    def ecol(self, v):
        for w in self.pm.children[v]:
            self.active.remove(w)
        self.active.add(v)

    def force_vsplit(self, v0):
        pm = self.pm
        stack = [v0]  # @line L3
        while stack:  # @line L4
            v = stack[-1]
            if self.is_split(v):
                stack.pop()  # @line L5
            elif v not in self.active:
                stack.append(pm.parent[v])  # @line L6
            elif self.vsplit_legal(v):
                stack.pop()  # @line L7
                self.vsplit(v)
            else:
                for f in pm.rec[v][2]:  # @line L8
                    if self.face(f) is None:
                        stack.append(pm.creator[f])

    def adapt_refinement(self, qrefine):
        """One pass over the active vertices. Returns the number of changes."""
        pm = self.pm
        changes = 0
        for v in sorted(self.active):  # @line L9
            if v not in self.active:
                continue
            if v in pm.children and qrefine(v):
                self.force_vsplit(v)  # @line L10
                changes += 1
            elif v in pm.parent:
                p = pm.parent[v]
                if self.ecol_legal(p) and not qrefine(p):
                    self.ecol(p)  # @line L11
                    changes += 1
        return changes


def screen_error_exceeds(mu, delta, nhat, p, e, kappa):
    """Hoppe's test in squared form: does the deviation space project larger than kappa?"""
    w = sub(p, e)
    d2 = dot(w, w)
    return mu * mu >= kappa * kappa * d2 or delta * delta * (d2 - dot(w, nhat) ** 2) >= kappa * kappa * d2 * d2


def vertex_bounds(pm, delta_split):
    """Per vertex: bounding sphere radius, normal cone and deviation.

    r_v bounds the leaf positions below v (a heuristic). The cone covers the
    normals of the full-mesh faces that touch those leaves. delta_v is the
    largest height jump of a split below v (a heuristic, not a proved bound).
    """
    touch = {}
    for f, c in enumerate(pm.faces):
        for w in c:
            touch.setdefault(w, []).append(f)
    normals = []
    for c in pm.faces:
        a, b, d = (pm.pos[w] for w in c)
        n = cross(sub(b, a), sub(d, a))
        ln = sqrt(dot(n, n))
        normals.append((n[0] / ln, n[1] / ln, n[2] / ln))
    out = {}
    for v in range(len(pm.pos)):
        lv = pm.leaves(v)
        pv = pm.pos[v]
        r = max(sqrt(dot(sub(pm.pos[w], pv), sub(pm.pos[w], pv))) for w in lv)
        fs = {f for w in lv for f in touch[w]}
        s = [sum(normals[f][k] for f in fs) for k in range(3)]
        ls = sqrt(dot(s, s))
        nv = (s[0] / ls, s[1] / ls, s[2] / ls)
        cos_min = min(min(1.0, dot(nv, normals[f])) for f in fs)
        sin2 = 1.0 - cos_min * cos_min
        out[v] = (r, nv, sin2, delta_split.get(v, 0.0))
    return out


def deltas(pm):
    """delta_v = max(delta_t, delta_u, |y(v_u) - y(v_s)|), leaves have 0."""
    d = {}
    for s in reversed(pm.order):
        t, u = pm.children[s]
        d[s] = max(d.get(t, 0.0), d.get(u, 0.0), abs(pm.pos[u][1] - pm.pos[s][1]))
    return d


def make_qrefine(pm, bounds, eye, forward, fov, tau):
    """qrefine(v) for a square viewport with vertical field of view fov."""
    from math import tan

    lf = sqrt(dot(forward, forward))
    fw = (forward[0] / lf, forward[1] / lf, forward[2] / lf)
    up = (0.0, 1.0, 0.0)
    right = cross(fw, up)
    lr = sqrt(dot(right, right))
    right = (right[0] / lr, right[1] / lr, right[2] / lr)
    upv = cross(right, fw)
    t = tan(fov / 2)
    planes = []
    for axis in (right, upv):
        for sgn in (1.0, -1.0):
            n = tuple(fw[k] * t - sgn * axis[k] for k in range(3))
            ln = sqrt(dot(n, n))
            planes.append((n[0] / ln, n[1] / ln, n[2] / ln))
    kappa = tau * t / 2  # kappa^2 = (2 cot(fov/2))^-2 tau^2
    nhat = (0.0, 1.0, 0.0)

    def qrefine(v):
        r, nv, sin2, delta = bounds[v]
        w = sub(pm.pos[v], eye)
        if any(dot(w, n) < -r for n in planes) or dot(w, fw) < -r:  # @line L12
            return False
        a = dot(w, nv)
        if a > 0 and a * a > dot(w, w) * sin2:  # @line L13
            return False
        return screen_error_exceeds(0.0, delta, nhat, pm.pos[v], eye, kappa)  # @line L14

    return qrefine
