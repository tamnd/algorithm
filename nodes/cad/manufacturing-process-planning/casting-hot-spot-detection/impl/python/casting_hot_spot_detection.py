# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/casting-hot-spot-detection/. The authors are listed in prov/NAYQYF.jsonl.

"""Hot spot candidates of a voxel casting from an exact distance transform.

The casting is a grid of cells in k dimensions (k = 2 for a section, k = 3
for a solid), stored as a flat list in row-major order with a shape tuple.
A cell is 1 for metal and 0 for mold. The grid must contain at least one mold
cell; pad the casting with a layer of mold cells to model the mold around it.

`squared_edt` returns, for each cell, the squared Euclidean distance from its
centre to the centre of the nearest mold cell. It uses the lower envelope of
parabolas of Felzenszwalb and Huttenlocher, one axis at a time, with integer
arithmetic only, so the result is exact.

`hot_spots` returns the regional maxima of this distance over the metal cells:
connected plateaus of equal value whose neighbours all have smaller values.
They are a geometric proxy for the places that freeze last, not a solution of
the heat equation.
"""

from itertools import product
from typing import List, Optional, Sequence, Tuple

Shape = Tuple[int, ...]
Cell = Tuple[int, ...]


def _check(mask: Sequence[int], shape: Shape) -> None:
    if not shape or any(s <= 0 for s in shape):
        raise ValueError("shape must be a non-empty tuple of positive sizes")
    size = 1
    for s in shape:
        size *= s
    if len(mask) != size:
        raise ValueError("mask length does not match the shape")
    if any(m not in (0, 1) for m in mask):
        raise ValueError("mask cells must be 0 (mold) or 1 (metal)")
    if all(m == 1 for m in mask):
        raise ValueError("the grid has no mold cell")


def _strides(shape: Shape) -> List[int]:
    strides = [1] * len(shape)
    for a in range(len(shape) - 2, -1, -1):
        strides[a] = strides[a + 1] * shape[a + 1]
    return strides


def lower_envelope_1d(f: Sequence[Optional[int]]) -> List[Optional[int]]:
    """Return d[q] = min over p with f[p] not None of (q - p)^2 + f[p].

    None stands for an infinite value. If every f[p] is None, every d[q] is
    None. The parabola of p is (q - p)^2 + f[p]; the parabolas of the stack v
    form the lower envelope, and parabola v[j] is lowest on the interval that
    starts at the breakpoint z[j], stored as an exact fraction num / den with
    den > 0.
    """
    n = len(f)
    # @line L3
    v: List[int] = []
    znum: List[int] = []
    zden: List[int] = []
    for q in range(n):
        if f[q] is None:
            continue
        while v:
            p = v[-1]
            num = (f[q] + q * q) - (f[p] + p * p)
            den = 2 * (q - p)
            # The parabolas of p and q cross at s = num / den. If s is at or
            # before the start of the interval of p, then p is never lowest.
            if len(v) > 1 and num * zden[-1] <= znum[-1] * den:
                v.pop()
                znum.pop()
                zden.pop()
                continue
            break
        if v:
            p = v[-1]
            znum.append((f[q] + q * q) - (f[p] + p * p))
            zden.append(2 * (q - p))
        else:
            znum.append(0)  # unused: the first interval starts at -infinity
            zden.append(1)
        v.append(q)
    if not v:
        return [None] * n
    d: List[Optional[int]] = [None] * n
    j = 0
    for q in range(n):
        # Move right while the next interval starts before q (z < q).
        while j + 1 < len(v) and znum[j + 1] < q * zden[j + 1]:
            j += 1
        p = v[j]
        d[q] = (q - p) * (q - p) + f[p]
    return d


def squared_edt(mask: Sequence[int], shape: Shape) -> List[int]:
    """Squared Euclidean distance from each cell to the nearest mold cell."""
    _check(mask, shape)
    # @line L1
    f: List[Optional[int]] = [0 if m == 0 else None for m in mask]
    strides = _strides(shape)
    # @line L2
    for a, n in enumerate(shape):
        other = [range(s) for b, s in enumerate(shape) if b != a]
        for rest in product(*other):
            base = 0
            k = 0
            for b in range(len(shape)):
                if b == a:
                    continue
                base += rest[k] * strides[b]
                k += 1
            idx = [base + i * strides[a] for i in range(n)]
            line = lower_envelope_1d([f[i] for i in idx])
            for i, val in zip(idx, line):
                f[i] = val
    # @line L4
    # Every cell now has a finite value, since some mold cell exists and the
    # passes reach it along the axes one after another.
    return [int(x) for x in f]


def _unravel(i: int, shape: Shape) -> Cell:
    out = []
    for s in reversed(shape):
        out.append(i % s)
        i //= s
    return tuple(reversed(out))


def _neighbours(cell: Cell, shape: Shape):
    for off in product((-1, 0, 1), repeat=len(shape)):
        if not any(off):
            continue
        nb = tuple(c + o for c, o in zip(cell, off))
        if all(0 <= x < s for x, s in zip(nb, shape)):
            yield nb


def hot_spots(mask: Sequence[int], shape: Shape) -> List[Tuple[int, List[Cell]]]:
    """Regional maxima of the squared distance over the metal cells.

    Returns a list of (squared distance, sorted cells of the plateau), with
    the largest distance first and ties in the order of the first cell.
    Plateaus are connected under the full neighbourhood (8 cells in 2D, 26
    in 3D).
    """
    dist = squared_edt(mask, shape)
    strides = _strides(shape)

    def flat(c: Cell) -> int:
        return sum(x * s for x, s in zip(c, strides))

    seen = [False] * len(mask)
    result: List[Tuple[int, List[Cell]]] = []
    # @line L5
    for start in range(len(mask)):
        if mask[start] != 1 or seen[start]:
            continue
        value = dist[start]
        seen[start] = True
        stack = [_unravel(start, shape)]
        plateau: List[Cell] = []
        is_max = True
        while stack:
            cell = stack.pop()
            plateau.append(cell)
            for nb in _neighbours(cell, shape):
                j = flat(nb)
                # @line L6
                if dist[j] > value:
                    is_max = False
                elif dist[j] == value and mask[j] == 1 and not seen[j]:
                    seen[j] = True
                    stack.append(nb)
        if is_max:
            result.append((value, sorted(plateau)))
    # @line L7
    result.sort(key=lambda r: (-r[0], r[1][0]))
    return result


def from_rows(rows: Sequence[str]) -> Tuple[List[int], Shape]:
    """Read a 2D grid from strings, '#' for metal and '.' for mold."""
    if not rows or any(len(r) != len(rows[0]) for r in rows):
        raise ValueError("rows must be non-empty and of equal length")
    mask = []
    for r in rows:
        for ch in r:
            if ch == "#":
                mask.append(1)
            elif ch == ".":
                mask.append(0)
            else:
                raise ValueError("unknown cell character")
    return mask, (len(rows), len(rows[0]))
