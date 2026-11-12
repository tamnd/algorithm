# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/supersampling-antialiasing/. The authors are listed in prov/DED02A.jsonl.

"""Supersampling antialiasing (SSAA) of a scene of triangles.

Coordinates are in pixel units: pixel (i, j) covers [i, i+1] x [j, j+1] and its
center is (i + 1/2, j + 1/2). The scene is a list of triangles in priority
order: a later triangle hides an earlier one. A sample point is inside a
triangle when all three edge functions are >= 0 after orienting the triangle
counterclockwise (an inclusive rule). Triangles of zero area are skipped.
Colors are tuples of linear values. Use fractions.Fraction coordinates for
exact results.
"""

import random
from fractions import Fraction
from typing import Callable, Optional, Sequence

Point = tuple
Color = tuple
Triangle = tuple  # (p0, p1, p2, color)
Shader = Callable[[int, Fraction, Fraction], Color]


def edge(a: Point, b: Point, p: Point) -> Fraction:
    """Twice the signed area of (a, b, p); positive when p is left of a -> b."""
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def inside(tri: Triangle, p: Point) -> bool:
    """Inclusive point-in-triangle test with exact edge functions."""
    p0, p1, p2 = tri[0], tri[1], tri[2]
    area = edge(p0, p1, p2)
    if area == 0:
        return False
    if area < 0:
        p1, p2 = p2, p1
    return edge(p0, p1, p) >= 0 and edge(p1, p2, p) >= 0 and edge(p2, p0, p) >= 0


def visible(scene: Sequence[Triangle], p: Point) -> Optional[int]:
    """Index of the frontmost triangle that contains p, or None."""
    for t in range(len(scene) - 1, -1, -1):
        if inside(scene[t], p):
            return t
    return None


def flat_shader(scene: Sequence[Triangle]) -> Shader:
    """The shader that returns the color stored with each triangle."""
    return lambda t, x, y: scene[t][3]


def supersampling_antialiasing(
    scene: Sequence[Triangle],
    width: int,
    height: int,
    k: int,
    background: Color,
    shade: Optional[Shader] = None,
    rng: Optional[random.Random] = None,
    jitter_steps: int = 1 << 16,
) -> list:
    """Render a W x H image with k x k samples per pixel and a box resolve.

    With rng=None the samples form an ordered grid at the centers of the k x k
    cells of each pixel. With an rng, each sample is placed uniformly at random
    on a fine grid of jitter_steps x jitter_steps points inside its cell
    (stratified, or jittered, sampling).
    Precondition: k >= 1. Cost: Theta(W H k^2 n) time for n triangles with
    this brute force visibility, and O(1) extra space besides the image.
    Returns rows of colors, image[j][i] for pixel (i, j).
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    if shade is None:
        shade = flat_shader(scene)
    image = []
    for j in range(height):
        row = []
        for i in range(width):  # @line L1
            total = [Fraction(0)] * len(background)  # @line L2
            for a in range(k):  # @line L3
                for b in range(k):
                    if rng is None:
                        ox, oy = Fraction(2 * a + 1, 2 * k), Fraction(2 * b + 1, 2 * k)
                    else:
                        ox = Fraction(2 * (a * jitter_steps + rng.randrange(jitter_steps)) + 1, 2 * k * jitter_steps)
                        oy = Fraction(2 * (b * jitter_steps + rng.randrange(jitter_steps)) + 1, 2 * k * jitter_steps)
                    x, y = i + ox, j + oy  # @line L4
                    t = visible(scene, (x, y))  # @line L5
                    color = background if t is None else shade(t, x, y)
                    total = [s + c for s, c in zip(total, color)]  # @line L6
            row.append(tuple(s / (k * k) for s in total))  # @line L7
        image.append(row)
    return image  # @line L8
