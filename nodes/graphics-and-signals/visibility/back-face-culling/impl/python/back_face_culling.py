# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/back-face-culling/. The authors are listed in prov/CT7W19.jsonl.

"""Back-face culling in object space.

A face is a triangle (v0, v1, v2) of points (x, y, z), int or Fraction,
listed counterclockwise when seen from outside the solid, so the normal
(v1 - v0) x (v2 - v0) points out. The viewer is the point E. A face is
front facing when E is strictly on the outer side of its plane. The test
is exact with integers or fractions.
"""

from fractions import Fraction
from typing import Sequence, Union

Num = Union[int, Fraction]
Point = Sequence[Num]


def back_face_cull(faces: Sequence[Sequence[Point]], eye: Point) -> list[int]:
    """Return the indices of the front-facing faces, in input order.

    The faces that are dropped cannot be seen from `eye` when the faces
    form a closed surface with outward normals and `eye` is outside it.
    Cost: O(1) per face, so O(F) for F faces.
    """
    kept: list[int] = []  # @line L1
    for k, (v0, v1, v2) in enumerate(faces):  # @line L2
        ux, uy, uz = v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]
        wx, wy, wz = v2[0] - v0[0], v2[1] - v0[1], v2[2] - v0[2]
        nx, ny, nz = uy * wz - uz * wy, uz * wx - ux * wz, ux * wy - uy * wx  # @line L3
        if nx * (eye[0] - v0[0]) + ny * (eye[1] - v0[1]) + nz * (eye[2] - v0[2]) > 0:  # @line L4
            kept.append(k)
    return kept  # @line L5
