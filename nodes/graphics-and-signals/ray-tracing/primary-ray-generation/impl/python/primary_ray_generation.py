# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/primary-ray-generation/. The authors are listed in prov/NCFKVH.jsonl.

"""Primary ray generation for a pinhole or a thin-lens camera.

The camera sits at the eye point e with an orthonormal basis (u, v, w):
u points right, v points up, and the camera looks along -w. The image has
W columns and H rows; pixel (i, j) has its center at (i + 1/2, j + 1/2),
with row 0 at the top. The image plane is at distance 1 in front of the
eye, and tan_half_fov = tan(theta / 2) for the vertical field of view
theta. A thin lens has the radius lens_radius and focuses at the
distance focus_distance along -w.

The arithmetic is plain + - * /, so with fractions.Fraction inputs (and a
lens point given as Fractions) every ray is exact.
"""

import math
from fractions import Fraction
from typing import Sequence, Tuple

Vec = Sequence
Ray = Tuple[tuple, tuple]
HALF = Fraction(1, 2)       # the pixel center offset; exact, and a float input stays float


def _add(a: Vec, b: Vec) -> tuple:
    return tuple(a[k] + b[k] for k in range(3))


def _sub(a: Vec, b: Vec) -> tuple:
    return tuple(a[k] - b[k] for k in range(3))


def _scale(s, a: Vec) -> tuple:
    return tuple(s * a[k] for k in range(3))


def _normalize(a: Vec) -> tuple:
    n = math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])
    return (a[0] / n, a[1] / n, a[2] / n)


def _cross(a: Vec, b: Vec) -> tuple:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def look_at(eye: Vec, target: Vec, up: Vec) -> Tuple[tuple, tuple, tuple]:
    """The basis (u, v, w) of a camera at eye that looks at target."""
    w = _normalize(_sub(eye, target))
    u = _normalize(_cross(up, w))
    v = _cross(w, u)
    return u, v, w


class Camera:
    def __init__(self, eye: Vec, u: Vec, v: Vec, w: Vec, width: int, height: int,
                 tan_half_fov, lens_radius=0, focus_distance=1) -> None:
        self.eye, self.u, self.v, self.w = tuple(eye), tuple(u), tuple(v), tuple(w)
        self.width, self.height = width, height
        self.tan_half_fov = tan_half_fov
        self.lens_radius = lens_radius
        self.focus_distance = focus_distance

    def pinhole_direction(self, i, j, sx, sy) -> tuple:
        """The direction from the eye through the image point (i + sx, j + sy).

        x = (2 (i + sx) / W - 1) (W / H) tan(theta / 2) is written as
        (2 (i + sx) - W) / H tan(theta / 2), so that square pixels need
        no aspect ratio and Fraction inputs stay exact.
        """
        x = (2 * (i + sx) - self.width) / self.height * self.tan_half_fov    # @line L1
        y = (self.height - 2 * (j + sy)) / self.height * self.tan_half_fov   # @line L2
        return _sub(_add(_scale(x, self.u), _scale(y, self.v)), self.w)      # @line L3

    def primary_ray(self, i, j, sx=HALF, sy=HALF, lens_point=(0, 0)) -> Ray:
        """The ray for the sample (sx, sy) in pixel (i, j).

        lens_point is a point of the unit disk; it is scaled by the lens
        radius. With lens_radius = 0 the camera is a pinhole.
        """
        d = self.pinhole_direction(i, j, sx, sy)
        if self.lens_radius == 0:                                            # @line L4
            return self.eye, d
        lx = self.lens_radius * lens_point[0]                                # @line L5
        ly = self.lens_radius * lens_point[1]
        o = _add(self.eye, _add(_scale(lx, self.u), _scale(ly, self.v)))     # @line L6
        focus = _add(self.eye, _scale(self.focus_distance, d))               # @line L7
        return o, _sub(focus, o)                                             # @line L8


def concentric_disk(x1: float, x2: float) -> Tuple[float, float]:
    """Map a point of the unit square to the unit disk, preserving area
    (Shirley and Chiu). The radius is max(|a|, |b|) for a = 2 x1 - 1, b = 2 x2 - 1."""
    a, b = 2 * x1 - 1, 2 * x2 - 1
    if a == 0 and b == 0:
        return (0.0, 0.0)
    if abs(a) > abs(b):
        r, phi = a, (math.pi / 4) * (b / a)
    else:
        r, phi = b, math.pi / 2 - (math.pi / 4) * (a / b)
    return (r * math.cos(phi), r * math.sin(phi))


def generate_image_rays(cam: Camera, spp: int, rng) -> list:
    """All primary rays of a frame: spp jittered samples per pixel, each
    with its own lens sample. Returns a list of ((i, j), (o, d))."""
    rays = []
    for j in range(cam.height):
        for i in range(cam.width):
            for _ in range(spp):
                sx, sy = rng.random(), rng.random()
                lens = concentric_disk(rng.random(), rng.random())
                rays.append(((i, j), cam.primary_ray(i, j, sx, sy, lens)))
    return rays
