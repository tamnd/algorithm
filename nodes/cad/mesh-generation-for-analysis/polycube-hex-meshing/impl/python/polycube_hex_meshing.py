# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polycube-hex-meshing/. The authors are listed in prov/ZACEGX.jsonl.

"""The integer grid step of polycube hex meshing.

A polycube is a finite set C of unit voxels, each named by the integer point
(i, j, k) of its lowest corner. The map g from the polycube to the solid is
given by the images of the integer voxel corners and is trilinear on each
voxel, so it is continuous across shared faces. The step meshes the
polycube with the grid of spacing 1/s and maps every grid point by g. The
hexes are the images of the grid cells. Before that, it checks on each voxel
that all 27 Bernstein coefficients of det Dg are positive, which proves that
g has a positive Jacobian on the whole polycube, so every hex is valid at
every resolution s.

Grid points are keys (a, b, c) of integers that stand for (a/s, b/s, c/s).
With int or Fraction input every value and sign is exact.
"""

from fractions import Fraction
from itertools import product
from typing import Dict, Iterable, List, Sequence, Tuple

from mg4geom import REF, bernstein_certified, trilinear

Key = Tuple[int, int, int]


def voxel_hex(corner_image: Dict[Key, Sequence], c: Key) -> List:
    """The trilinear hex of g on voxel c, in the standard corner order."""
    return [corner_image[(c[0] + a, c[1] + b, c[2] + d)] for a, b, d in REF]


def polycube_grid(voxels: Iterable[Key], corner_image: Dict[Key, Sequence], s: int):
    """Mesh the polycube at resolution s and map the grid by g.

    Returns None if some voxel fails the Bernstein test. Otherwise returns
    (points, hexes): points maps each grid key to its image, and each hex is a
    list of 8 keys in the standard order. Cost: O(|C| s^3) after the O(|C|) test.
    """
    cells = sorted(set(voxels))
    for c in cells:  # @line L1
        if not bernstein_certified(voxel_hex(corner_image, c)):  # @line L2
            return None
    owner: Dict[Key, Key] = {}
    for c in cells:  # @line L3
        for a, b, d in product(range(s + 1), repeat=3):
            owner.setdefault((s * c[0] + a, s * c[1] + b, s * c[2] + d), c)
    points: Dict[Key, Tuple] = {}
    for key, c in owner.items():  # @line L4
        local = [Fraction(key[t] - s * c[t], s) for t in range(3)]
        points[key] = trilinear(voxel_hex(corner_image, c), *local)  # @line L5
    hexes: List[List[Key]] = []  # @line L6
    for c in cells:  # @line L7
        for q in product(range(s), repeat=3):
            hexes.append([(s * c[0] + q[0] + a, s * c[1] + q[1] + b, s * c[2] + q[2] + d) for a, b, d in REF])  # @line L8
    return points, hexes  # @line L9


def hex_points(points: Dict[Key, Tuple], hexes: Sequence[Sequence[Key]]) -> List[List[Tuple]]:
    """The hexes with their corner coordinates in place of their keys."""
    return [[points[k] for k in hx] for hx in hexes]


def identity_images(voxels: Iterable[Key]) -> Dict[Key, Tuple]:
    """The corner images of the identity map, as Fractions."""
    out: Dict[Key, Tuple] = {}
    for c in voxels:
        for a, b, d in REF:
            k = (c[0] + a, c[1] + b, c[2] + d)
            out[k] = tuple(Fraction(x) for x in k)
    return out


def boundary_faces(voxels: Iterable[Key]) -> int:
    """The number of unit faces of the polycube that belong to one voxel only."""
    cells = set(voxels)
    n = 0
    for c in cells:
        for t in range(3):
            for step in (-1, 1):
                nb = list(c)
                nb[t] += step
                if tuple(nb) not in cells:
                    n += 1
    return n


def all_voxels_certified(voxels: Iterable[Key], corner_image: Dict[Key, Sequence]) -> bool:
    """True when every voxel passes the Bernstein test of L1 and L2."""
    return all(bernstein_certified(voxel_hex(corner_image, c)) for c in set(voxels))
