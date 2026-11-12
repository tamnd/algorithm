# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conditional-independence/. The authors are listed in prov/VZMJS0.jsonl.

"""Exact tests of conditional independence on a finite joint table.

A joint is a dict that maps a tuple of values (one per variable, by
position) to a nonnegative weight. The weights need not sum to 1: the
test X _||_ Y | Z is invariant under scaling, so integer counts and
Fractions both work and the arithmetic stays exact.

X, Y and Z are tuples of variable positions. The test uses the product
form  p(x, y, z) p(z) = p(x, z) p(y, z)  for all x, y, z, which needs no
division and is correct also when some p(z) = 0.
"""

from itertools import product
from typing import Dict, Sequence, Tuple

Joint = Dict[Tuple[int, ...], object]


def marginal(joint: Joint, keep: Sequence[int]) -> Dict[Tuple[int, ...], object]:
    out: Dict[Tuple[int, ...], object] = {}
    for assignment, w in joint.items():
        key = tuple(assignment[i] for i in keep)
        out[key] = out.get(key, 0) + w
    return out


def is_ci(joint: Joint, x: Sequence[int], y: Sequence[int], z: Sequence[int]) -> bool:
    """True when X is independent of Y given Z under the joint."""
    x, y, z = tuple(x), tuple(y), tuple(z)
    pxyz = marginal(joint, x + y + z)
    pxz = marginal(joint, x + z)
    pyz = marginal(joint, y + z)
    pz = marginal(joint, z)
    nx, ny = len(x), len(y)
    for kx in {k[:nx] for k in pxyz} | {k[:nx] for k in pxz}:
        for ky in {k[nx:nx + ny] for k in pxyz} | {k[:ny] for k in pyz}:
            for kz in pz:
                lhs = pxyz.get(kx + ky + kz, 0) * pz[kz]
                rhs = pxz.get(kx + kz, 0) * pyz.get(ky + kz, 0)
                if lhs != rhs:
                    return False
    return True


def table(weights: Sequence[object], nvars: int, card: int = 2) -> Joint:
    """A joint over nvars variables with values 0..card-1 from a flat list."""
    cells = list(product(range(card), repeat=nvars))
    if len(weights) != len(cells):
        raise ValueError("wrong number of weights")
    return {c: w for c, w in zip(cells, weights)}


# The semi-graphoid axioms and the intersection property, for the roles
# X = (0,), Y = (1,), W = (2,), Z = (3,) or Z = () as given.

def symmetry_holds(j: Joint, X, Y, Z) -> bool:
    return (not is_ci(j, X, Y, Z)) or is_ci(j, Y, X, Z)


def decomposition_holds(j: Joint, X, Y, W, Z) -> bool:
    return (not is_ci(j, X, Y + W, Z)) or is_ci(j, X, Y, Z)


def weak_union_holds(j: Joint, X, Y, W, Z) -> bool:
    return (not is_ci(j, X, Y + W, Z)) or is_ci(j, X, Y, Z + W)


def contraction_holds(j: Joint, X, Y, W, Z) -> bool:
    if is_ci(j, X, Y, Z) and is_ci(j, X, W, Z + Y):
        return is_ci(j, X, Y + W, Z)
    return True


def intersection_holds(j: Joint, X, Y, W, Z) -> bool:
    if is_ci(j, X, Y, Z + W) and is_ci(j, X, W, Z + Y):
        return is_ci(j, X, Y + W, Z)
    return True
