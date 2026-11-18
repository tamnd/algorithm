# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cube-map/. The authors are listed in prov/M0T5ZN.jsonl.

"""A cube map: six square textures that store a function of direction.

The faces are in the OpenGL order +x, -x, +y, -y, +z, -z (indices 0 to 5).
A direction selects the face of its major axis, the axis of the largest
absolute component; ties go to x before y before z. The face coordinates
(sc, tc) come from the OpenGL table, and s = (sc / |ma| + 1) / 2,
t = (tc / |ma| + 1) / 2 are in [0, 1]. Texel (i, j) of a face of size N
covers s in [i / N, (i + 1) / N] and t in [j / N, (j + 1) / N], and it is
stored at faces[f][j][i].

Precondition: directions are not the zero vector; they need not be unit.
Cost: O(1) for lookup, store and the direction of a texel; Theta(N^2) memory
per face, 6 N^2 texels in all.
"""

import math

Vec = tuple[float, float, float]

POS_X, NEG_X, POS_Y, NEG_Y, POS_Z, NEG_Z = range(6)


def major_axis(d: Vec) -> int:
    """The face of the largest |component|, with ties to x, then y, then z."""
    x, y, z = d
    ax, ay, az = abs(x), abs(y), abs(z)
    if ax >= ay and ax >= az:
        return POS_X if x > 0 else NEG_X
    if ay >= az:
        return POS_Y if y > 0 else NEG_Y
    return POS_Z if z > 0 else NEG_Z


def face_coords(d: Vec) -> tuple[int, float, float]:
    """The face and the coordinates s, t in [0, 1] of a direction (OpenGL table)."""
    x, y, z = d
    face = major_axis(d)  # @line L1
    if face == POS_X:  # @line L2
        sc, tc, ma = -z, -y, x
    elif face == NEG_X:
        sc, tc, ma = z, -y, x
    elif face == POS_Y:
        sc, tc, ma = x, z, y
    elif face == NEG_Y:
        sc, tc, ma = x, -z, y
    elif face == POS_Z:
        sc, tc, ma = x, -y, z
    else:
        sc, tc, ma = -x, -y, z
    s = (sc / abs(ma) + 1.0) / 2.0  # @line L3
    t = (tc / abs(ma) + 1.0) / 2.0
    return face, s, t


def face_direction(face: int, s: float, t: float) -> Vec:
    """The inverse of face_coords: the unit direction of a point (s, t) of a face."""
    sc, tc = 2.0 * s - 1.0, 2.0 * t - 1.0  # @line L7
    if face == POS_X:  # @line L8
        d = (1.0, -tc, -sc)
    elif face == NEG_X:
        d = (-1.0, -tc, sc)
    elif face == POS_Y:
        d = (sc, 1.0, tc)
    elif face == NEG_Y:
        d = (sc, -1.0, -tc)
    elif face == POS_Z:
        d = (sc, -tc, 1.0)
    else:
        d = (-sc, -tc, -1.0)
    r = math.sqrt(d[0] * d[0] + d[1] * d[1] + d[2] * d[2])
    return (d[0] / r, d[1] / r, d[2] / r)  # @line L9


def _area(x: float, y: float) -> float:
    """The solid angle of the part of a face from its center to (x, y), x, y in [-1, 1]."""
    return math.atan2(x * y, math.sqrt(x * x + y * y + 1.0))


class CubeMap:
    """Six faces of size by size texels, each texel holding one float."""

    def __init__(self, size: int = 1) -> None:
        if size < 1:
            raise ValueError("size must be at least 1")
        self.size = size
        self.faces = [[[0.0] * size for _ in range(size)] for _ in range(6)]

    def texel_of(self, d: Vec) -> tuple[int, int, int]:
        """The face and the texel (i, j) that contain the direction d."""
        face, s, t = face_coords(d)
        n = self.size
        i = min(int(s * n), n - 1)  # @line L4
        j = min(int(t * n), n - 1)
        return face, i, j

    def lookup(self, d: Vec) -> float:
        """CUBE-LOOKUP: the value of the texel that contains d (nearest filter)."""
        face, i, j = self.texel_of(d)
        return self.faces[face][j][i]  # @line L5

    def store(self, face: int, i: int, j: int, value: float) -> None:
        """Set the value of texel (i, j) of a face."""
        self.faces[face][j][i] = value

    def texel_direction(self, face: int, i: int, j: int) -> Vec:
        """The unit direction of the center of texel (i, j)."""
        n = self.size
        return face_direction(face, (i + 0.5) / n, (j + 0.5) / n)  # @line L6

    def texel_solid_angle(self, face: int, i: int, j: int) -> float:
        """The exact solid angle of texel (i, j); it does not depend on the face."""
        n = self.size
        x0, x1 = 2.0 * i / n - 1.0, 2.0 * (i + 1) / n - 1.0
        y0, y1 = 2.0 * j / n - 1.0, 2.0 * (j + 1) / n - 1.0
        return _area(x1, y1) - _area(x0, y1) - _area(x1, y0) + _area(x0, y0)

    def fill(self, f) -> None:
        """Store f(direction) at the center of every texel."""
        n = self.size
        for face in range(6):
            for j in range(n):
                for i in range(n):
                    self.faces[face][j][i] = f(self.texel_direction(face, i, j))

    def lookup_bilinear(self, d: Vec) -> float:
        """Bilinear filter inside the face of d, clamped at the face edges.

        This is the simple filter that ignores the neighbour faces, so it
        shows a seam at the edges; see the page for seamless filtering.
        """
        face, s, t = face_coords(d)
        n = self.size
        u = min(max(s * n - 0.5, 0.0), n - 1.0)
        v = min(max(t * n - 0.5, 0.0), n - 1.0)
        i0, j0 = min(int(u), n - 1), min(int(v), n - 1)
        i1, j1 = min(i0 + 1, n - 1), min(j0 + 1, n - 1)
        fu, fv = u - i0, v - j0
        a = self.faces[face]
        top = a[j0][i0] * (1 - fu) + a[j0][i1] * fu
        bot = a[j1][i0] * (1 - fu) + a[j1][i1] * fu
        return top * (1 - fv) + bot * fv

    def check_invariant(self) -> None:
        """Six faces, each size by size, of floats."""
        assert len(self.faces) == 6
        for face in self.faces:
            assert len(face) == self.size
            for row in face:
                assert len(row) == self.size
                assert all(isinstance(x, float) for x in row)
