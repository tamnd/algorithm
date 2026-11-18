# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cascaded-shadow-maps/. The authors are listed in prov/SFEHPC.jsonl.

"""Cascaded shadow maps for a directional light.

The world is right handed with y up. The camera looks along the negative z
axis of its frame; a point's view depth d is its distance along the view
direction. The near plane is at d = n and the far plane at d = f. The light
frame has rows (lx, ly, lz); the light travels along -lz, so a point p has
light coordinates q = R p and light depth -q_z, larger is farther from the
light. Each cascade map stores the linear light depth of the nearest
occluder at each texel center. The scene for the shadow maps is a list of
spheres (center, radius), which keeps the depth render exact and small.
"""

from math import ceil, floor, sqrt, tan


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(a, s):
    return tuple(x * s for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def normalize(a):
    return scale(a, 1.0 / sqrt(dot(a, a)))


def splits(n, f, m, lam):
    """The practical split scheme: a blend of the logarithmic and the uniform split."""
    return [lam * n * (f / n) ** (i / m) + (1 - lam) * (n + (f - n) * i / m)  # @line L1
            for i in range(m + 1)]


class Camera:
    def __init__(self, pos, forward, fov_y, aspect):
        self.pos = pos
        self.fwd = normalize(forward)
        self.right = normalize(cross(self.fwd, (0.0, 1.0, 0.0)))
        self.up = cross(self.right, self.fwd)
        self.t = tan(fov_y / 2)
        self.aspect = aspect

    def depth(self, p):
        return dot(sub(p, self.pos), self.fwd)

    def slice_corners(self, d0, d1):
        out = []
        for d in (d0, d1):
            c = add(self.pos, scale(self.fwd, d))
            for sx in (-1, 1):
                for sy in (-1, 1):
                    out.append(add(c, add(scale(self.right, sx * d * self.t * self.aspect),
                                          scale(self.up, sy * d * self.t))))
        return out

    def point(self, d, a, b):
        """The point at view depth d and normalized screen position (a, b) in [-1, 1]^2."""
        c = add(self.pos, scale(self.fwd, d))
        return add(c, add(scale(self.right, a * d * self.t * self.aspect), scale(self.up, b * d * self.t)))


def light_frame(direction):
    """Rows (lx, ly, lz) of the light frame for a light that travels along direction."""
    lz = normalize(scale(direction, -1.0))
    hint = (0.0, 0.0, 1.0) if abs(lz[2]) < 0.9 else (1.0, 0.0, 0.0)
    lx = normalize(cross(hint, lz))
    ly = cross(lz, lx)
    return (lx, ly, lz)


def to_light(rows, p):
    return tuple(dot(r, p) for r in rows)


def fit_tight(cam, rows, d0, d1, size):
    """The crop of one cascade: the light-space bounds of the slice corners."""
    q = [to_light(rows, p) for p in cam.slice_corners(d0, d1)]  # @line L3
    lo = (min(v[0] for v in q), min(v[1] for v in q))  # @line L4
    hi = (max(v[0] for v in q), max(v[1] for v in q))
    return lo, ((hi[0] - lo[0]) / size, (hi[1] - lo[1]) / size)


def fit_stable(cam, rows, d0, d1, size, quantum=1.0 / 64):
    """A crop that does not change size when the camera turns and whose texel
    grid stays fixed in the world when the camera moves: a bounding sphere of
    the slice, with the radius rounded up and the origin snapped to texels."""
    pts = cam.slice_corners(d0, d1)
    c = scale(pts[0], 0.0)
    for p in pts:
        c = add(c, scale(p, 1.0 / len(pts)))
    r = max(sqrt(dot(sub(p, c), sub(p, c))) for p in pts)
    r = ceil(r / quantum) * quantum
    texel = 2 * r / (size - 1)
    q = to_light(rows, c)
    lo = (floor((q[0] - r) / texel) * texel, floor((q[1] - r) / texel) * texel)
    return lo, (texel, texel)


def render(spheres, rows, lo, texel, size):
    """The depth map of the spheres: the light depth of the nearest surface at
    each texel center, or infinity where no sphere covers the center."""
    lsph = [(to_light(rows, c), r) for c, r in spheres]
    out = []
    for j in range(size):
        y = lo[1] + (j + 0.5) * texel[1]
        row = []
        for i in range(size):
            x = lo[0] + (i + 0.5) * texel[0]
            best = float("inf")
            for c, r in lsph:
                e = r * r - (x - c[0]) ** 2 - (y - c[1]) ** 2
                if e >= 0:
                    best = min(best, -c[2] - sqrt(e))
            row.append(best)
        out.append(row)
    return out


class Cascades:
    def __init__(self, cam, light_dir, spheres, n, f, m, lam, size, stable=False):
        self.cam = cam
        self.rows = light_frame(light_dir)
        self.c = splits(n, f, m, lam)
        self.size = size
        self.maps = []
        for i in range(m):  # @line L2
            fit = fit_stable if stable else fit_tight
            lo, texel = fit(cam, self.rows, self.c[i], self.c[i + 1], size)
            s = render(spheres, self.rows, lo, texel, size)  # @line L5
            self.maps.append((lo, texel, s))

    def cascade_of(self, d):
        for i in range(len(self.c) - 1):  # @line L6
            if self.c[i] <= d < self.c[i + 1]:
                return i
        return None

    def shadowed(self, p, bias=1e-6):
        i = self.cascade_of(self.cam.depth(p))
        if i is None:
            return False
        lo, texel, s = self.maps[i]
        q = to_light(self.rows, p)  # @line L7
        a, b = floor((q[0] - lo[0]) / texel[0]), floor((q[1] - lo[1]) / texel[1])
        if not (0 <= a < self.size and 0 <= b < self.size):
            return False
        return s[b][a] < -q[2] - bias  # @line L8


def exact_shadowed(p, spheres, rows):
    """Does the ray from p toward the light meet a sphere?"""
    q = to_light(rows, p)
    for c, r in spheres:
        lc = to_light(rows, c)
        e = r * r - (q[0] - lc[0]) ** 2 - (q[1] - lc[1]) ** 2
        if e >= 0 and -lc[2] - sqrt(e) < -q[2]:
            return True
    return False
