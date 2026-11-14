# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/taubin-smoothing/. The authors are listed in prov/Y17GAM.jsonl.

"""Taubin's lambda-mu smoothing (SIGGRAPH 1995) with the uniform weights.

Each pass does two Laplacian steps, x <- x + f (c - x), first with the
shrinking factor f = lam > 0 and then with the inflating factor f = mu < -lam,
where c_i is the centroid of the neighbours of vertex i. A frequency k of
the graph Laplacian I - D^-1 A is multiplied by (1 - lam k)(1 - mu k) per pass.
The steps work on any graph, given by its neighbour lists, so that a test can
use a cycle, whose eigenvectors are known.
"""

from fractions import Fraction
from typing import Iterable, Optional, Sequence

from mp2mesh import boundary_vertices, neighbours

Point = tuple


def taubin_graph(points: Sequence[Sequence], nb: Sequence[Sequence[int]], lam, mu, passes: int,
                 fixed: Iterable[int] = ()) -> list[Point]:
    """Taubin smoothing on a graph with neighbour lists nb."""
    stay = set(fixed)
    x = [tuple(p) for p in points]
    for _ in range(passes):                                   # @line L2
        for f in (lam, mu):                                   # @line L3
            y = list(x)                                       # @line L5
            for i in range(len(x)):                           # @line L4
                if i in stay or not nb[i]:
                    continue
                d = len(nb[i])
                c = tuple(sum(x[j][k] for j in nb[i]) / d for k in range(len(x[i])))
                y[i] = tuple(x[i][k] + f * (c[k] - x[i][k]) for k in range(len(x[i])))
            x = y                                             # @line L6
    return x


def taubin_smoothing(points: Sequence[Sequence], faces: Sequence[Sequence[int]], lam=Fraction(33, 100),
                     mu=Fraction(-34, 100), passes: int = 1, fixed: Optional[Iterable[int]] = None) -> list[Point]:
    """Taubin smoothing of a triangle mesh. The border vertices are fixed unless `fixed` is given."""
    if not (lam > 0 and mu < -lam):
        raise ValueError("need lam > 0 and mu < -lam")
    nb = neighbours(len(points), faces)                       # @line L1
    stay = boundary_vertices(faces) if fixed is None else set(fixed)
    return taubin_graph(points, nb, lam, mu, passes, stay)


def transfer(k, lam, mu):
    """The factor (1 - lam k)(1 - mu k) of one pass on the frequency k."""
    return (1 - lam * k) * (1 - mu * k)


def pass_band(lam, mu):
    """The frequency k_PB = 1/lam + 1/mu > 0 where the transfer function is 1 again."""
    return 1 / lam + 1 / mu
