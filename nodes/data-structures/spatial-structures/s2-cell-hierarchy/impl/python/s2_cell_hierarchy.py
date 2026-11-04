# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/s2-cell-hierarchy/. The authors are listed in prov/MMDM7B.jsonl.
"""S2 cell ids: a hierarchy of cells on the sphere, numbered along a Hilbert curve.

The sphere is projected onto the six faces of a cube. Each face is a
quadtree of 30 levels. A cell is named by a 64-bit id: 3 bits for the
face, then 2 bits for each level, which give the position of the child
along a Hilbert curve, then a 1 bit, then zeros. The parent of a cell is
its id with the last two position bits cleared and the 1 bit moved up.
This file follows the conventions of the S2 library (face numbering, the
quadratic projection, and the Hilbert tables); it is a small model, not
the library.
"""

from __future__ import annotations

import math
from typing import List, Tuple

MAX_LEVEL = 30
POS_BITS = 2 * MAX_LEVEL + 1  # 61
MAX_SIZE = 1 << MAX_LEVEL
SWAP, INVERT = 1, 2
# Hilbert tables of the S2 library: for an orientation, the position (0..3)
# of the child with bits ij = (i << 1) | j, and the change of orientation
# for each position.
IJ_TO_POS = ((0, 1, 3, 2), (0, 3, 1, 2), (2, 3, 1, 0), (2, 1, 3, 0))
POS_TO_IJ = ((0, 1, 3, 2), (0, 2, 3, 1), (3, 2, 0, 1), (3, 1, 0, 2))
POS_TO_ORIENTATION = (SWAP, 0, 0, INVERT | SWAP)


def latlng_to_xyz(lat_deg: float, lng_deg: float) -> Tuple[float, float, float]:
    lat, lng = math.radians(lat_deg), math.radians(lng_deg)
    return (math.cos(lat) * math.cos(lng), math.cos(lat) * math.sin(lng), math.sin(lat))


def xyz_to_face_uv(p: Tuple[float, float, float]) -> Tuple[int, float, float]:
    x, y, z = p
    ax, ay, az = abs(x), abs(y), abs(z)
    face = 0 if ax >= ay and ax >= az else (1 if ay >= az else 2)  # @line L1
    if p[face] < 0:
        face += 3
    if face == 0:
        u, v = y / x, z / x
    elif face == 1:
        u, v = -x / y, z / y
    elif face == 2:
        u, v = -x / z, -y / z
    elif face == 3:
        u, v = z / x, y / x
    elif face == 4:
        u, v = z / y, -x / y
    else:
        u, v = -y / z, -x / z
    return face, u, v


def face_uv_to_xyz(face: int, u: float, v: float) -> Tuple[float, float, float]:
    return [(1, u, v), (-u, 1, v), (-u, -v, 1), (-1, -v, -u), (v, -1, -u), (v, u, -1)][face]


def uv_to_st(u: float) -> float:
    """The quadratic projection of S2, which makes cells of one level closer in area."""
    return 0.5 * math.sqrt(1 + 3 * u) if u >= 0 else 1 - 0.5 * math.sqrt(1 - 3 * u)  # @line L2


def st_to_uv(s: float) -> float:
    return (4 * s * s - 1) / 3 if s >= 0.5 else (1 - 4 * (1 - s) * (1 - s)) / 3


def st_to_ij(s: float) -> int:
    return max(0, min(MAX_SIZE - 1, int(math.floor(MAX_SIZE * s))))  # @line L3


def from_face_ij(face: int, i: int, j: int) -> int:
    """The leaf cell id (level 30) of the cell (i, j) of a face."""
    orientation = face & SWAP  # @line L4
    pos = 0
    for k in range(MAX_LEVEL - 1, -1, -1):  # @line L5
        ij = (((i >> k) & 1) << 1) | ((j >> k) & 1)
        p = IJ_TO_POS[orientation][ij]  # @line L6
        pos = (pos << 2) | p
        orientation ^= POS_TO_ORIENTATION[p]  # @line L7
    return (face << POS_BITS) | (pos << 1) | 1  # @line L8


def from_latlng(lat: float, lng: float, level: int = MAX_LEVEL) -> int:
    face, u, v = xyz_to_face_uv(latlng_to_xyz(lat, lng))
    leaf = from_face_ij(face, st_to_ij(uv_to_st(u)), st_to_ij(uv_to_st(v)))
    return parent(leaf, level)


def lsb(cid: int) -> int:
    return cid & -cid


def level(cid: int) -> int:
    return MAX_LEVEL - (lsb(cid).bit_length() - 1) // 2


def face(cid: int) -> int:
    return cid >> POS_BITS


def is_valid(cid: int) -> bool:
    return 0 < cid < (6 << POS_BITS) and (lsb(cid).bit_length() - 1) % 2 == 0


def parent(cid: int, lev: int) -> int:
    """The ancestor of cid at level lev (lev <= level(cid))."""
    if not 0 <= lev <= level(cid):
        raise ValueError("bad level")
    new_lsb = 1 << (2 * (MAX_LEVEL - lev))  # @line L9
    return (cid & -new_lsb) | new_lsb  # @line L10


def children(cid: int) -> List[int]:
    """The four children, in Hilbert order."""
    if level(cid) == MAX_LEVEL:
        raise ValueError("a leaf cell has no children")
    b = lsb(cid)
    nb = b >> 2  # @line L11
    first = cid - b + nb
    return [first + 2 * nb * k for k in range(4)]  # @line L12


def range_min(cid: int) -> int:
    return cid - (lsb(cid) - 1)


def range_max(cid: int) -> int:
    return cid + (lsb(cid) - 1)


def contains(a: int, b: int) -> bool:
    """Cell a contains cell b: b lies in the id range of the leaves of a."""
    return range_min(a) <= b <= range_max(a)  # @line L13


def to_face_ij(cid: int) -> Tuple[int, int, int, int]:
    """Face, i, j of the lower left leaf of cid, and the orientation there."""
    f = face(cid)
    orientation = f & SWAP
    leaf = range_min(cid)
    pos = (leaf >> 1) & ((1 << (2 * MAX_LEVEL)) - 1)
    i = j = 0
    for k in range(MAX_LEVEL - 1, -1, -1):
        p = (pos >> (2 * k)) & 3
        ij = POS_TO_IJ[orientation][p]
        i = (i << 1) | (ij >> 1)
        j = (j << 1) | (ij & 1)
        orientation ^= POS_TO_ORIENTATION[p]
    return f, i, j, orientation


def ij_bounds(cid: int) -> Tuple[int, int, int, int]:
    """The face and the range of leaf i and j that the cell covers: (face, i0, j0, size)."""
    f, i, j, _ = to_face_ij(cid)
    size = 1 << (MAX_LEVEL - level(cid))
    return f, i & -size, j & -size, size


def token(cid: int) -> str:
    """The hex form of the id without trailing zeros, as in S2."""
    h = "%016x" % cid
    return h.rstrip("0") or "X"


def from_token(tok: str) -> int:
    return int(tok.ljust(16, "0"), 16)
