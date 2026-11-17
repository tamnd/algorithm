# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/particle-level-set/. The authors are listed in prov/S6VHF6.jsonl.

"""The particle level set method of Enright, Fedkiw, Ferziger and Mitchell (2002) in 2D.

phi < 0 inside the liquid and phi > 0 outside, sampled at the cell centers
of a square grid (the p layout of macgrid.py). Marker particles sit on both
sides of the interface, within a band of a few cells. A particle has a sign
s (+1 outside, -1 inside) and a radius r in [r_min, r_max] = [0.1 dx, 0.5 dx].
It has escaped when it is on the wrong side of the interface by more than its
radius: s phi(x_p) < 0 and |phi(x_p)| > r. Each escaped particle defines the
small signed distance function phi_p(x) = s (r - |x - x_p|), and the level
set is rebuilt near it from the union of these circles:

    phi+ = max(phi, phi_p over the positive escaped particles),
    phi- = min(phi, phi_p over the negative escaped particles),
    phi  = phi+ if |phi+| <= |phi-| else phi-.

The level set is moved by semi-Lagrangian advection (bilinear sampling at the
backtraced point), which the 2005 paper of Enright, Losasso and Fedkiw also
uses; the 2002 paper uses fifth order HJ-WENO. The caller gives the flow as
a map trace(x, y, t, dt) from a point at time t to its position at time
t + dt; a negative dt traces backward.
"""

import math
import random

import macgrid


class ParticleLevelSet:
    """A level set on an n by n grid of cells of size dx, with marker particles."""

    def __init__(self, n, dx, phi0, rng=None, per_cell=4, band=3.0, max_particles=400, use_particles=True):
        if n < 2 or dx <= 0.0 or per_cell < 0 or max_particles < 0:
            raise ValueError("need n >= 2, dx > 0, per_cell >= 0 and max_particles >= 0")
        self.n, self.dx = n, float(dx)
        self.phi = [[float(phi0((i + 0.5) * dx, (j + 0.5) * dx)) for j in range(n)] for i in range(n)]
        self.r_min, self.r_max = 0.1 * dx, 0.5 * dx
        self.b_min, self.b_max = 0.1 * dx, band * dx
        self.particles = []  # [x, y, s, r]
        self.use_particles = use_particles
        reinitialize(self)
        if use_particles:
            self.seed(rng if rng is not None else random.Random(0), per_cell, max_particles)

    def value(self, x, y):
        """phi at (x, y), by bilinear interpolation."""
        return macgrid.sample(self.phi, x, y, self.dx, 0.5, 0.5)

    def normal(self, x, y):
        """grad phi / |grad phi| at (x, y), by central differences of the interpolated phi."""
        h = 0.5 * self.dx
        gx = (self.value(x + h, y) - self.value(x - h, y)) / (2.0 * h)
        gy = (self.value(x, y + h) - self.value(x, y - h)) / (2.0 * h)
        m = math.hypot(gx, gy)
        return (gx / m, gy / m) if m > 0.0 else (0.0, 0.0)

    def seed(self, rng, per_cell, max_particles):
        """Put per_cell particles of each sign in every cell near the interface, and attract each to its side.

        A particle of sign s gets a goal phi_goal = s U[b_min, b_max]. As in
        section 2.3.1 of the paper, it tries x + lam (phi_goal - phi(x)) N(x)
        with lam = 1, halves lam while the point is outside the domain, and
        accepts the point if it is in the band. Otherwise it moves with lam / 2
        and tries again. A particle that is not in the band after 15 tries is
        dropped. At most max_particles are kept, chosen at random.
        """
        n, dx = self.n, self.dx
        L = n * dx

        def in_band(s, x, y):
            return self.b_min <= s * self.value(x, y) <= self.b_max

        cells = [(i, j) for i in range(n) for j in range(n) if abs(self.phi[i][j]) < self.b_max]
        out = []
        for (i, j) in cells:
            for k in range(2 * per_cell):
                s = 1.0 if k % 2 == 0 else -1.0
                x, y = (i + rng.random()) * dx, (j + rng.random()) * dx
                goal = s * rng.uniform(self.b_min, self.b_max)
                ok = in_band(s, x, y)
                for _ in range(15):
                    if ok:
                        break
                    ph = self.value(x, y)
                    nx, ny = self.normal(x, y)
                    lam = 1.0
                    while lam > 1e-6 and not (0.0 <= x + lam * (goal - ph) * nx <= L and 0.0 <= y + lam * (goal - ph) * ny <= L):
                        lam *= 0.5
                    xn, yn = x + lam * (goal - ph) * nx, y + lam * (goal - ph) * ny
                    if in_band(s, xn, yn):
                        x, y, ok = xn, yn, True
                    else:
                        x, y = x + 0.5 * lam * (goal - ph) * nx, y + 0.5 * lam * (goal - ph) * ny
                        ok = in_band(s, x, y)
                if ok:
                    out.append([x, y, s, min(max(s * self.value(x, y), self.r_min), self.r_max)])
        rng.shuffle(out)
        self.particles = out[:max_particles]

    def escaped(self):
        """The particles on the wrong side of the interface by more than their radius."""
        out = []
        for p in self.particles:
            ph = self.value(p[0], p[1])
            if p[2] * ph < 0.0 and abs(ph) > p[3]:  # @line L2
                out.append(p)
        return out

    def correct(self):
        """Rebuild phi near the escaped particles. Returns the number of escaped particles."""
        if not self.use_particles:
            return 0
        esc = self.escaped()
        n, dx = self.n, self.dx
        plus = [list(c) for c in self.phi]
        minus = [list(c) for c in self.phi]
        for (x, y, s, r) in esc:
            i0 = min(max(int(math.floor(x / dx - 0.5)), 0), n - 2)
            j0 = min(max(int(math.floor(y / dx - 0.5)), 0), n - 2)
            for i in (i0, i0 + 1):
                for j in (j0, j0 + 1):
                    php = s * (r - math.hypot((i + 0.5) * dx - x, (j + 0.5) * dx - y))
                    if s > 0.0:
                        plus[i][j] = max(plus[i][j], php)  # @line L3
                    else:
                        minus[i][j] = min(minus[i][j], php)
        for i in range(n):
            for j in range(n):
                a, b = plus[i][j], minus[i][j]
                self.phi[i][j] = a if abs(a) <= abs(b) else b  # @line L4
        return len(esc)

    def adjust_radii(self):
        """r = clamp(s phi(x_p), r_min, r_max); an escaped particle gets r_min."""
        for p in self.particles:
            p[3] = min(max(p[2] * self.value(p[0], p[1]), self.r_min), self.r_max)  # @line L7

    def step(self, trace, t, dt):
        """One step of the method from time t to t + dt."""
        n, dx = self.n, self.dx
        old = self.phi
        new = macgrid.zeros(n, n)
        for i in range(n):
            for j in range(n):
                xb, yb = trace((i + 0.5) * dx, (j + 0.5) * dx, t + dt, -dt)
                new[i][j] = macgrid.sample(old, xb, yb, dx, 0.5, 0.5)
        self.phi = new
        for p in self.particles:
            p[0], p[1] = trace(p[0], p[1], t, dt)  # @line L1
        self.correct()
        reinitialize(self)  # @line L5
        self.correct()  # @line L6
        self.adjust_radii()


def crossings(phi, dx):
    """The points where phi changes sign between two neighboring cell centers, by linear interpolation."""
    n = len(phi)
    pts = []
    for i in range(n):
        for j in range(n):
            a = phi[i][j]
            for (k, l) in ((i + 1, j), (i, j + 1)):
                if k < n and l < n:
                    b = phi[k][l]
                    if (a < 0.0) != (b < 0.0):
                        t = a / (a - b)
                        pts.append(((i + 0.5 + t * (k - i)) * dx, (j + 0.5 + t * (l - j)) * dx))
    return pts


def reinitialize(st, width=5.0):
    """Make phi a signed distance near the interface, without moving it much.

    A cell next to a sign change keeps its value. Any other cell with
    |phi| < width dx gets its sign times the distance to the nearest crossing
    point. Cells farther away are left alone. This brute force search stands
    in for the PDE or fast marching reinitialization of the papers.
    """
    phi, dx, n = st.phi, st.dx, st.n
    pts = crossings(phi, dx)
    if not pts:
        return
    lim = width * dx
    near = set()
    for i in range(n):
        for j in range(n):
            for (k, l) in ((i + 1, j), (i, j + 1)):
                if k < n and l < n and (phi[i][j] < 0.0) != (phi[k][l] < 0.0):
                    near.add((i, j))
                    near.add((k, l))
    new = [list(c) for c in phi]
    for i in range(n):
        for j in range(n):
            if (i, j) in near or abs(phi[i][j]) >= lim:
                continue
            x, y = (i + 0.5) * dx, (j + 0.5) * dx
            d = min(math.hypot(x - px, y - py) for (px, py) in pts)
            new[i][j] = math.copysign(d, phi[i][j])
    st.phi = new


def rotation(cx, cy, omega):
    """The exact trace of a rigid rotation about (cx, cy) with angular speed omega."""
    def trace(x, y, t, dt):
        c, s = math.cos(omega * dt), math.sin(omega * dt)
        dx, dy = x - cx, y - cy
        return (cx + c * dx - s * dy, cy + s * dx + c * dy)
    return trace


def inside_area(phi_at, L, m):
    """The area where phi_at < 0 in [0, L]^2, counted on an m by m grid of sample points."""
    h = L / m
    cnt = 0
    for a in range(m):
        for b in range(m):
            if phi_at((a + 0.5) * h, (b + 0.5) * h) < 0.0:
                cnt += 1
    return cnt * h * h


def area_of_difference(phi_at, exact_at, L, m):
    """The area where phi_at and exact_at have different signs, counted on an m by m grid of samples."""
    h = L / m
    cnt = 0
    for a in range(m):
        for b in range(m):
            x, y = (a + 0.5) * h, (b + 0.5) * h
            if (phi_at(x, y) < 0.0) != (exact_at(x, y) < 0.0):
                cnt += 1
    return cnt * h * h


def zalesak(cx, cy, R, w, depth):
    """A disk of radius R about (cx, cy) with a slot of width w cut up from its bottom to the height depth.

    Returns phi(x, y) = max(disk, -slot), negative inside the shape.
    """
    def phi(x, y):
        d_disk = math.hypot(x - cx, y - cy) - R
        qx, qy = abs(x - cx) - 0.5 * w, max((cy - R) - y, y - (cy - R + depth))
        if qx > 0.0 and qy > 0.0:
            d_slot = math.hypot(qx, qy)
        else:
            d_slot = max(qx, qy)
        return max(d_disk, -d_slot)
    return phi
