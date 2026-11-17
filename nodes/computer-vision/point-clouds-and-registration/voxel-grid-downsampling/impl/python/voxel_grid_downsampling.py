# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/voxel-grid-downsampling/. The authors are listed in prov/S76VBE.jsonl.
"""Voxel grid downsampling of a 3D point cloud.

The space is cut into cubes (voxels) of edge `size`, aligned with the axes and
with one corner at `origin`. Each occupied voxel is replaced by the centroid of
the points that fall in it. A dict (a hash table) maps the integer voxel index
to a running sum, so the cost is O(n) expected time for n points.
"""

from __future__ import annotations

import math
from typing import Dict, List, Sequence, Tuple

Point = Tuple[float, float, float]
Key = Tuple[int, int, int]


def voxel_index(p: Sequence[float], size: float, origin: Sequence[float] = (0.0, 0.0, 0.0)) -> Key:
    """The integer index (i, j, k) of the voxel that holds p.

    The voxel (i, j, k) is the half-open box [o + i s, o + (i + 1) s) x ... .
    floor, not int(), so that negative coordinates go to negative indices.
    """
    return (math.floor((p[0] - origin[0]) / size),
            math.floor((p[1] - origin[1]) / size),
            math.floor((p[2] - origin[2]) / size))


def voxel_grid_downsample(points: Sequence[Sequence[float]], size: float,
                          origin: Sequence[float] = (0.0, 0.0, 0.0)) -> List[Point]:
    """Replace the points of each occupied voxel by their centroid.

    Precondition: size > 0. The output has one point per occupied voxel, in the
    order in which the voxels are first met in the input. Entries may be floats
    or fractions.Fraction; with fractions and a Fraction size the result is
    exact. Cost: O(n) expected time and O(m) extra space for m occupied voxels.
    """
    if not size > 0:
        raise ValueError("the voxel size must be positive")
    cells: Dict[Key, list] = {}  # @line L1
    for p in points:  # @line L2
        key = voxel_index(p, size, origin)  # @line L3
        acc = cells.get(key)  # @line L4
        if acc is None:
            acc = [0, 0, 0, 0]
            cells[key] = acc
        acc[0] += p[0]  # @line L5
        acc[1] += p[1]
        acc[2] += p[2]
        acc[3] += 1
    out: List[Point] = []  # @line L6
    for acc in cells.values():  # @line L7
        c = acc[3]
        out.append((acc[0] / c, acc[1] / c, acc[2] / c))  # @line L8
    return out  # @line L9
