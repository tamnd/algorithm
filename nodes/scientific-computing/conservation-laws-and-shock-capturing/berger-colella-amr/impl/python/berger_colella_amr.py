# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/berger-colella-amr/. The authors are listed in prov/64KT6D.jsonl.
"""Berger-Colella adaptive mesh refinement in one space dimension.

The equation is linear advection u_t + a u_x = 0 on the periodic domain [0, 1),
with the first-order upwind flux on every level. The hierarchy has levels
0, 1, ..., with refinement ratio r in space and time. Level 0 covers the
domain. A patch of level l + 1 covers a run of whole level-l cells, and it may
wrap around the periodic boundary. Values can be floats or Fractions; with
Fractions every step is exact.
"""

from fractions import Fraction


class Patch:
    """Cells lo, ..., hi - 1 of one level (taken modulo the number of cells)."""

    __slots__ = ("lo", "hi", "u", "old")

    def __init__(self, lo, hi, u):
        self.lo, self.hi, self.u, self.old = lo, hi, u, None


class Hierarchy:
    def __init__(self, f, n0, a, dt0, ratio=2, max_level=1, tol=0.1,
                 buffer=1, regrid_every=2, reflux=True):
        if n0 < 3 or ratio < 2 or max_level < 0 or buffer < 0:
            raise ValueError("bad hierarchy parameters")
        self.n0, self.a, self.dt0, self.r = n0, a, dt0, ratio
        self.max_level, self.tol, self.buffer = max_level, tol, buffer
        self.regrid_every, self.reflux = regrid_every, reflux
        one = Fraction(1) if isinstance(dt0, Fraction) else 1.0
        self.length = one
        self.t, self.steps = 0 * one, 0
        self.levels = [[Patch(0, n0, [f(self.centre(0, j)) for j in range(n0)])]]
        self.regrid(init=f)

    # geometry ---------------------------------------------------------------
    def n(self, l):
        return self.n0 * self.r ** l

    def dx(self, l):
        return self.length / self.n(l)

    def dt(self, l):
        return self.dt0 / self.r ** l

    def centre(self, l, j):
        return (j + self.length / 2) * self.dx(l)

    def finest(self):
        return len(self.levels) - 1

    def find(self, l, j):
        """Return (patch, offset) for cell j of level l, or None."""
        n = self.n(l)
        for p in self.levels[l]:
            k = (j - p.lo) % n
            if k < p.hi - p.lo:
                return p, k
        return None

    def flux(self, ul, ur):
        return self.a * ul if self.a >= 0 else self.a * ur

    # time stepping ----------------------------------------------------------
    def _ghost(self, l, j, theta):
        hit = self.find(l, j)
        if hit is not None:                                 # same-level neighbour
            p, k = hit
            return p.u[k]
        # @line L1: from level l - 1, linear in time between its old and new values
        q, k = self.find(l - 1, (j % self.n(l)) // self.r)
        return (1 - theta) * q.old[k] + theta * q.u[k]

    def _advance(self, l, theta, fine_reg):
        dt, dx = self.dt(l), self.dx(l)
        n = self.n(l)
        patches = self.levels[l]
        ext = [[self._ghost(l, p.lo - 1, theta)] + p.u + [self._ghost(l, p.hi, theta)]
               for p in patches]
        face_flux = {}
        for p, e in zip(patches, ext):
            m = p.hi - p.lo
            F = [self.flux(e[i], e[i + 1]) for i in range(m + 1)]
            p.old = p.u
            # @line L2: one upwind step on every patch of level l
            p.u = [p.old[i] - dt / dx * (F[i + 1] - F[i]) for i in range(m)]
            for i in range(m + 1):
                face_flux[(p.lo + i) % n] = F[i]
            if l > 0 and m < n:
                # @line L3: fine flux register at the two ends of the patch
                for face, Fi in ((p.lo, F[0]), (p.hi, F[m])):
                    cf = (face // self.r) % self.n(l - 1)
                    fine_reg[cf] = fine_reg.get(cf, 0) + dt * Fi
        if l == self.finest():
            return
        r, nf = self.r, self.n(l + 1)
        # @line L4: coarse fluxes at the faces where level l + 1 patches start or end
        ends = [(q.lo // r % n, q.hi // r % n) for q in self.levels[l + 1]
                if q.hi - q.lo < nf]
        coarse = {f: dt * face_flux[f] for pair in ends for f in pair}
        reg = {}
        for k in range(r):
            # @line L5: subcycle the finer level r times
            self._advance(l + 1, Fraction(k, r) if isinstance(dt, Fraction) else k / r, reg)
        if self.reflux:
            for left, right in ends:
                # @line L6: reflux the uncovered coarse cells next to the patch
                p, k = self.find(l, left - 1)
                p.u[k] -= (reg[left] - coarse[left]) / dx
                p, k = self.find(l, right)
                p.u[k] += (reg[right] - coarse[right]) / dx
        self._average_down(l)

    def _average_down(self, l):
        r = self.r
        for q in self.levels[l + 1]:
            for c in range(q.lo // r, q.hi // r):
                p, k = self.find(l, c)
                i = c * r - q.lo
                # @line L7: covered coarse cell = mean of its r fine cells
                p.u[k] = sum(q.u[i:i + r]) / r

    def step(self):
        self._advance(0, 0, {})
        self.t += self.dt0
        self.steps += 1
        if self.regrid_every and self.steps % self.regrid_every == 0:
            self.regrid()

    def run(self, steps):
        for _ in range(steps):
            self.step()
        return self

    # regridding -------------------------------------------------------------
    def _tags(self, l):
        n = self.n(l)
        tags = set()
        for p in self.levels[l]:
            m = p.hi - p.lo
            for k in range(m):
                j = (p.lo + k) % n
                for nb in (j - 1, j + 1):
                    hit = self.find(l, nb)
                    if hit is not None and abs(hit[0].u[hit[1]] - p.u[k]) > self.tol:
                        tags.add(j)
        grown = {(j + d) % n for j in tags for d in range(-self.buffer, self.buffer + 1)}
        if l > 0:
            grown = {j for j in grown
                     if all(self.find(l, j + d) is not None for d in (-1, 0, 1))}
        return grown

    def regrid(self, init=None):
        r = self.r
        for l in range(self.max_level):
            if l > self.finest():
                break
            n = self.n(l)
            # @line L8: tag, buffer, and keep only properly nested cells
            tags = self._tags(l)
            runs = cell_runs(tags, n)
            old = self.levels[l + 1] if l + 1 < len(self.levels) else []
            new = []
            for lo, hi in runs:
                vals = []
                for j in range(lo * r, hi * r):
                    if init is not None:
                        vals.append(init(self.centre(l + 1, j % self.n(l + 1))))
                        continue
                    hit = None
                    for q in old:
                        k = (j - q.lo) % self.n(l + 1)
                        if k < q.hi - q.lo:
                            hit = q.u[k]
                    if hit is None:
                        c, k = self.find(l, (j // r) % n)
                        hit = c.u[k]
                    vals.append(hit)
                # @line L9: new patch, filled from old fine data or from level l
                new.append(Patch(lo * r, hi * r, vals))
            if not new:
                del self.levels[l + 1:]
                break
            self.levels[l + 1:l + 2] = [new]
        del self.levels[self.max_level + 1:]
        for l in range(self.finest() - 1, -1, -1):
            self._average_down(l)

    # output -----------------------------------------------------------------
    def composite(self):
        """List of (left, width, value) for the finest cells covering [0, 1)."""
        out = []

        def walk(l, j):
            r = self.r
            if l < self.finest() and self.find(l + 1, j * r) is not None:
                for i in range(r):
                    walk(l + 1, j * r + i)
            else:
                p, k = self.find(l, j)
                out.append((j * self.dx(l), self.dx(l), p.u[k]))

        for j in range(self.n0):
            walk(0, j)
        return out

    def mass(self):
        return sum(w * v for _, w, v in self.composite())

    def cells(self):
        return len(self.composite())


def cell_runs(tags, n):
    """Maximal runs of tagged cells on a circle of n cells, as (lo, hi), hi <= lo + n."""
    if not tags:
        return []
    if len(tags) == n:
        return [(0, n)]
    start = next(j for j in range(n) if j in tags and (j - 1) % n not in tags)
    runs, j = [], start
    for _ in range(n):
        if j % n in tags and (j - 1) % n not in tags:
            lo = j
        if j % n in tags and (j + 1) % n not in tags:
            runs.append((lo % n, lo % n + (j - lo) + 1))
        j += 1
    return runs


def upwind_uniform(u, a, lam, steps):
    """Reference: single-grid periodic upwind with Courant number lam = a dt / dx."""
    m = len(u)
    for _ in range(steps):
        if a >= 0:
            u = [u[i] - lam * (u[i] - u[i - 1]) for i in range(m)]
        else:
            u = [u[i] - lam * (u[(i + 1) % m] - u[i]) for i in range(m)]
    return u
