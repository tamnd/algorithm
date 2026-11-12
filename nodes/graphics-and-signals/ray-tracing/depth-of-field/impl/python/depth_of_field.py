# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/depth-of-field/. The authors are listed in prov/KB8FWQ.jsonl.

"""Depth of field of a thin lens.

Lengths are in one unit, for example millimeters. The lens has the focal length f and the
f-number N, so the aperture diameter is f / N. It is focused at the distance s > f in front of
the lens, and c is the largest circle of confusion on the film that still counts as sharp.

The module gives the circle of confusion of a point at any distance, the hyperfocal distance and
the near and far limits of the depth of field, and a Monte Carlo estimate of the image of a
defocused edge through a sampled lens disk.
"""

import math
import random
from typing import Optional, Tuple


def image_distance(f: float, z: float) -> float:
    """Distance behind the lens of the image of a point at the distance z > f (1/f = 1/z + 1/zi)."""
    return f * z / (z - f)


def circle_of_confusion(z: float, f: float, n: float, s: float) -> float:
    """Diameter on the film of the blur disk of a point at the distance z > f.

    The film is at the image distance of the focus distance s > f. Cost O(1).
    """
    aperture = f / n
    return aperture * f * abs(z - s) / (z * (s - f))


def hyperfocal_distance(f: float, n: float, c: float) -> float:
    """The focus distance H = f^2 / (N c) + f at which the far limit of sharpness is infinity."""
    return f * f / (n * c) + f


def depth_of_field_limits(f: float, n: float, c: float, s: float) -> Tuple[float, Optional[float]]:
    """Near and far limits of the depth of field when the lens is focused at s > f.

    The far limit is None (infinity) when s >= H. Both limits solve circle_of_confusion(z) = c
    exactly. Cost O(1).
    """
    h = hyperfocal_distance(f, n, c)
    near = s * (h - f) / (h + s - 2.0 * f)
    far = None if s >= h else s * (h - f) / (h - s)
    return near, far


def sample_disk(rng: random.Random, radius: float) -> Tuple[float, float]:
    """A uniform point of the disk of the given radius, by the inverse of the radial CDF."""
    r = radius * math.sqrt(rng.random())
    phi = 2.0 * math.pi * rng.random()
    return r * math.cos(phi), r * math.sin(phi)


def edge_image(p_focus: float, z_edge: float, f: float, n: float, s: float,
               rng: random.Random, samples: int) -> float:
    """Fraction of the lens through which one film point sees a bright half-plane.

    The scene has a bright half-plane x > 0 at the distance z_edge > 0 and nothing else. The film
    point is named by the point (p_focus, 0) of the plane of focus that it images sharply, as in
    the renderer's form of the thin lens. The lens disk is sampled uniformly, and each ray from a
    lens point through the point in focus is followed to the plane of the edge. Returns the
    fraction of rays that hit the bright side, an unbiased estimate of the pixel value.
    Requires samples >= 1. Cost O(samples).
    """
    radius = 0.5 * f / n
    hits = 0
    for _ in range(samples):
        lx, _ = sample_disk(rng, radius)
        # The ray from (lx, 0) at depth 0 through (p_focus, s), at depth z_edge.
        x_at_edge = lx + (p_focus - lx) * z_edge / s
        if x_at_edge > 0.0:
            hits += 1
    return hits / samples
