# SPDX-License-Identifier: MIT
# Shared helper of the computer vision pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Camera geometry and synthetic scenes for the computer vision pages.

Conventions (prompts of the area, also stated on the pages):
- The camera frame has X to the right, Y down and Z forward. A point is in
  front of the camera if Z > 0.
- K = [[fx, s, cx], [0, fy, cy], [0, 0, 1]] in pixels.
- A world point Xw maps to the camera frame by Xc = R Xw + t. The camera
  matrix is P = K [R | t], and the center is C = -R^T t.
- Rotations are active and right-handed. Quaternions are (w, x, y, z) in the
  Hamilton convention.

This module holds no algorithm of a computer vision page.
"""

from __future__ import annotations

import math
import random
from typing import Dict, List, Optional, Sequence, Tuple

from cvla import det, matvec, mul, solve, transpose

Matrix = List[List[float]]
Vector = List[float]


def to_h(x: Sequence[float]) -> Vector:
    """Append a 1: the homogeneous vector of a point."""
    return [float(v) for v in x] + [1.0]


def from_h(x: Sequence[float]) -> Vector:
    """Divide by the last entry and drop it. Raises ValueError if the last
    entry is zero (a point at infinity)."""
    w = x[-1]
    if w == 0:
        raise ValueError("from_h: point at infinity")
    return [v / w for v in x[:-1]]


def make_K(fx: float, fy: float, cx: float, cy: float, s: float = 0.0) -> Matrix:
    """The intrinsic matrix [[fx, s, cx], [0, fy, cy], [0, 0, 1]]."""
    return [[float(fx), float(s), float(cx)],
            [0.0, float(fy), float(cy)],
            [0.0, 0.0, 1.0]]


def camera_matrix(K: Sequence[Sequence[float]], R: Sequence[Sequence[float]],
                  t: Sequence[float]) -> Matrix:
    """The 3 x 4 camera matrix P = K [R | t]."""
    rt = [list(R[i]) + [t[i]] for i in range(3)]
    return mul(K, rt)


def project(P: Sequence[Sequence[float]], X):
    """Pixel coordinates (u, v) of a point X under the camera P.

    X is a 3D point (3 entries) or a homogeneous point (4 entries). If X is
    a list of points, the result is the list of their projections."""
    if len(X) > 0 and isinstance(X[0], (list, tuple)):
        return [project(P, x) for x in X]
    xh = to_h(X) if len(X) == 3 else list(X)
    return from_h(matvec(P, xh))


def camera_center(P: Sequence[Sequence[float]]) -> Vector:
    """The center C of a finite camera P = [M | p4]: C = -M^-1 p4, so that
    P (C, 1) = 0."""
    m = [list(row[:3]) for row in P]
    p4 = [row[3] for row in P]
    return [-v for v in solve(m, p4)]


def rot_x(a: float) -> Matrix:
    """Rotation by the angle a (radians) about the X axis."""
    c, s = math.cos(a), math.sin(a)
    return [[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]]


def rot_y(a: float) -> Matrix:
    """Rotation by the angle a (radians) about the Y axis."""
    c, s = math.cos(a), math.sin(a)
    return [[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]]


def rot_z(a: float) -> Matrix:
    """Rotation by the angle a (radians) about the Z axis."""
    c, s = math.cos(a), math.sin(a)
    return [[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]]


def axis_angle_to_R(axis: Sequence[float], theta: Optional[float] = None) -> Matrix:
    """Rotation by theta (radians) about the axis, by the right-hand rule
    (Rodrigues formula). The axis need not be a unit vector. If theta is
    None, axis is the rotation vector w = theta a, with theta = ||w||."""
    n = math.sqrt(sum(float(v) * float(v) for v in axis))
    if theta is None:
        theta = n
    if n == 0.0 or theta == 0.0:
        return [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    x, y, z = (float(v) / n for v in axis)
    c, s = math.cos(theta), math.sin(theta)
    d = 1.0 - c
    return [[c + x * x * d, x * y * d - z * s, x * z * d + y * s],
            [y * x * d + z * s, c + y * y * d, y * z * d - x * s],
            [z * x * d - y * s, z * y * d + x * s, c + z * z * d]]


def quat_to_R(q: Sequence[float]) -> Matrix:
    """Rotation matrix of the quaternion q = (w, x, y, z), Hamilton
    convention. q is normalized first; q and -q give the same matrix."""
    n = math.sqrt(sum(float(v) * float(v) for v in q))
    if n == 0.0:
        raise ValueError("quat_to_R: zero quaternion")
    w, x, y, z = (float(v) / n for v in q)
    return [[1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)]]


def random_rotation(rng: random.Random) -> Matrix:
    """A rotation drawn from the uniform (Haar) distribution: a uniform
    random unit quaternion by the method of Shoemake (1992)."""
    u1, u2, u3 = rng.random(), rng.random(), rng.random()
    a, b = math.sqrt(1.0 - u1), math.sqrt(u1)
    q = (b * math.cos(2 * math.pi * u3), a * math.sin(2 * math.pi * u2),
         a * math.cos(2 * math.pi * u2), b * math.sin(2 * math.pi * u3))
    return quat_to_R(q)


def _small_rotation(rng: random.Random, max_angle: float) -> Matrix:
    axis = [rng.gauss(0.0, 1.0) for _ in range(3)]
    return axis_angle_to_R(axis, rng.uniform(0.0, max_angle))


def random_scene(rng: random.Random, n: int = 20, n_cams: int = 2,
                 K: Optional[Sequence[Sequence[float]]] = None,
                 cams: Optional[Sequence[Tuple]] = None,
                 radius: float = 1.0, distance: float = 5.0,
                 max_angle: float = 0.3, planar: bool = False,
                 first_identity: bool = False,
                 size: Optional[Tuple[float, float]] = None,
                 min_depth: float = 0.1) -> Dict[str, list]:
    """A synthetic scene with known cameras and points.

    Cameras: if cams is given, it is a list of (K, R, t) and is used as it
    is. Otherwise n_cams cameras look at the world origin from the distance
    `distance`. Each one is the camera at center (0, 0, -distance) with
    R = I, turned about the origin by a random rotation of angle at most
    max_angle (radians). K defaults to make_K(800, 800, 320, 240). With
    first_identity, the world frame is moved to the frame of camera 0, so
    that camera 0 has R = I and t = 0 (the points move with it).

    Points: n points drawn uniformly in the cube [-radius, radius]^3 (with
    Z = 0 if planar, before any move of the world frame). A point is kept
    only if its depth is at least min_depth in every camera, and, if size =
    (W, H) is given, if its projection lies in [0, W] x [0, H] in every
    camera. Raises ValueError if 1000 n draws are not enough.

    Returns a dict with lists "K", "R", "t", "P" (one entry per camera),
    "X" (the 3D points) and "x" (x[i][j] is the pixel of point j in
    camera i, without noise)."""
    if cams is not None:
        Ks = [[list(r) for r in c[0]] for c in cams]
        Rs = [[list(r) for r in c[1]] for c in cams]
        ts = [list(c[2]) for c in cams]
    else:
        k0 = [list(r) for r in K] if K is not None else make_K(800, 800, 320, 240)
        Ks, Rs, ts = [], [], []
        c0 = [0.0, 0.0, -float(distance)]
        for _ in range(n_cams):
            q = _small_rotation(rng, max_angle)
            r = transpose(q)
            center = matvec(q, c0)
            Ks.append([list(row) for row in k0])
            Rs.append(r)
            ts.append([-v for v in matvec(r, center)])
    pts: List[Vector] = []
    tries = 0
    while len(pts) < n:
        tries += 1
        if tries > 1000 * max(n, 1):
            raise ValueError("random_scene: cannot place the points")
        x = [rng.uniform(-radius, radius) for _ in range(3)]
        if planar:
            x[2] = 0.0
        ok = True
        for k, r, t in zip(Ks, Rs, ts):
            xc = [a + b for a, b in zip(matvec(r, x), t)]
            if xc[2] < min_depth:
                ok = False
                break
            if size is not None:
                u = (k[0][0] * xc[0] + k[0][1] * xc[1]) / xc[2] + k[0][2]
                v = k[1][1] * xc[1] / xc[2] + k[1][2]
                if not (0.0 <= u <= size[0] and 0.0 <= v <= size[1]):
                    ok = False
                    break
        if ok:
            pts.append(x)
    if first_identity and Rs:
        r0, t0 = Rs[0], ts[0]
        pts = [[a + b for a, b in zip(matvec(r0, x), t0)] for x in pts]
        r0t = transpose(r0)
        newR, newt = [], []
        for r, t in zip(Rs, ts):
            rr = mul(r, r0t)
            newR.append(rr)
            newt.append([a - b for a, b in zip(t, matvec(rr, t0))])
        Rs, ts = newR, newt
        Rs[0] = [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
        ts[0] = [0.0, 0.0, 0.0]
    Ps = [camera_matrix(k, r, t) for k, r, t in zip(Ks, Rs, ts)]
    xs = [[project(p, x) for x in pts] for p in Ps]
    return {"K": Ks, "R": Rs, "t": ts, "P": Ps, "X": pts, "x": xs}


def add_noise(rng: random.Random, pts: Sequence[Sequence[float]], sigma: float) -> List[Vector]:
    """A copy of the points with independent Gaussian noise of standard
    deviation sigma added to every coordinate."""
    return [[float(v) + rng.gauss(0.0, sigma) for v in p] for p in pts]


def self_test() -> None:
    """Check random_scene and quat_to_R. Raises AssertionError."""
    rng = random.Random(11)
    scene = random_scene(rng, n=30, n_cams=4)
    for r, t in zip(scene["R"], scene["t"]):
        for x in scene["X"]:
            assert matvec(r, x)[2] + t[2] > 0.0
    for _ in range(5):
        q = [rng.gauss(0.0, 1.0) for _ in range(4)]
        r = quat_to_R(q)
        rtr = mul(transpose(r), r)
        assert all(abs(rtr[i][j] - (1.0 if i == j else 0.0)) <= 1e-12
                   for i in range(3) for j in range(3))
        assert abs(det(r) - 1.0) <= 1e-12


if __name__ == "__main__":
    self_test()
