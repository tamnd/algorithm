# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contact-map/. The authors are listed in prov/3YNAR9.jsonl.

"""Contact map of a known structure, one point per residue (for example the
C-beta atom, or C-alpha for glycine), coordinates in angstrom.

contact_pairs finds all pairs (i, j), i < j, j - i >= min_sep, whose distance is
below the cutoff, with a cell list: a uniform grid of cubes whose side is the
cutoff, so a contact can only join points in the same or in adjacent cells.
The cost is O(n + K) expected time for n residues and K pairs checked, which is
O(n) for protein-like densities, and O(n^2) in the worst case.

Standard library only.
"""

import math

Vec = tuple[float, float, float]


def contact_pairs(points: list[Vec], cutoff: float = 8.0, min_sep: int = 1) -> set[tuple[int, int]]:
    """All (i, j) with i < j, j - i >= min_sep and |p_i - p_j| < cutoff."""
    if cutoff <= 0:
        raise ValueError("cutoff must be positive")
    if min_sep < 1:
        raise ValueError("min_sep must be at least 1")
    cells: dict[tuple[int, int, int], list[int]] = {}
    keys = []
    for i, p in enumerate(points):
        key = (math.floor(p[0] / cutoff), math.floor(p[1] / cutoff), math.floor(p[2] / cutoff))
        keys.append(key)
        cells.setdefault(key, []).append(i)
    c2 = cutoff * cutoff
    out: set[tuple[int, int]] = set()
    for i, p in enumerate(points):
        kx, ky, kz = keys[i]
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for j in cells.get((kx + dx, ky + dy, kz + dz), ()):
                        if j - i < min_sep:  # also skips j <= i, since min_sep >= 1
                            continue
                        q = points[j]
                        d2 = (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2
                        if d2 < c2:
                            out.add((i, j))
    return out


def contact_matrix(n: int, pairs: set[tuple[int, int]]) -> list[list[int]]:
    """The symmetric 0/1 matrix C with C[i][j] = 1 for each contact; the diagonal is 0."""
    c = [[0] * n for _ in range(n)]
    for i, j in pairs:
        c[i][j] = c[j][i] = 1
    return c


def distance_matrix(points: list[Vec]) -> list[list[float]]:
    return [[math.dist(p, q) for q in points] for p in points]


def separation_class(i: int, j: int) -> str:
    """Sequence separation classes of CASP contact assessment: short 6-11, medium 12-23, long >= 24."""
    s = abs(i - j)
    if s >= 24:
        return "long"
    if s >= 12:
        return "medium"
    if s >= 6:
        return "short"
    return "local"


def relative_contact_order(pairs: set[tuple[int, int]], length: int) -> float:
    """Plaxco, Simons and Baker (1998): CO = (1 / (L * N_c)) * sum of |i - j| over the N_c contacts."""
    if not pairs or length <= 0:
        return 0.0
    return sum(j - i for i, j in pairs) / (length * len(pairs))
