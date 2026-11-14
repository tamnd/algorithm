# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/witness-configuration-method/. The authors are listed in prov/JK8AA5.jsonl.

"""The witness configuration method for distance constraints between points.

A witness is a random placement of the points. The squared distance constraints hold at the witness by
construction, if the dimension values are measured from it. The rank of the Jacobian at the witness, computed
exactly with fractions, gives the rank at a generic placement with high probability. It is never larger."""

import random
from fractions import Fraction
from typing import Optional, Sequence

Edge = tuple[int, int]
Point = Sequence[int]


def jacobian_rows(edges: Sequence[Edge], p: Sequence[Point]) -> list[list[Fraction]]:
    """Half the Jacobian of the squared distances |p_i - p_j|^2: the rigidity matrix, one row per edge."""
    d = len(p[0]) if p else 0
    rows = []
    for i, j in edges:
        row = [Fraction(0)] * (d * len(p))
        for k in range(d):
            row[d * i + k] = Fraction(p[i][k] - p[j][k])
            row[d * j + k] = Fraction(p[j][k] - p[i][k])
        rows.append(row)
    return rows


class RowSpace:
    """An echelon basis of the rows seen so far; add() reports whether a new row is independent of them."""

    def __init__(self) -> None:
        self.basis: list[tuple[int, list[Fraction]]] = []

    def reduce(self, row: list[Fraction]) -> list[Fraction]:
        row = list(row)
        for c, b in self.basis:
            if row[c] != 0:
                f = row[c] / b[c]
                row = [x - f * y for x, y in zip(row, b)]
        return row

    def add(self, row: list[Fraction]) -> bool:
        row = self.reduce(row)
        for c, x in enumerate(row):
            if x != 0:
                self.basis.append((c, row))
                return True
        return False


def rank(rows: Sequence[list[Fraction]]) -> int:
    space = RowSpace()
    return sum(1 for r in rows if space.add(r))


def random_witness(n: int, d: int, rng: random.Random, box: int) -> list[list[int]]:
    """A placement with independent uniform integer coordinates in 1..box."""
    return [[rng.randint(1, box) for _ in range(d)] for _ in range(n)]


def trivial_dimension(d: int, n: int) -> int:
    """The dimension of the infinitesimal rigid motions of n points in general position in R^d.

    The points span an s-flat with s = min(n - 1, d). The rotations that fix the flat pointwise act on the
    (d - s)-dimensional complement and move no point, so they are subtracted."""
    if n == 0:
        return 0
    s = min(n - 1, d)
    return d * (d + 1) // 2 - (d - s) * (d - s - 1) // 2


def analyze(n: int, edges: Sequence[Edge], d: int = 2, rng: Optional[random.Random] = None,
            box: int = 10**6, witness: Optional[Sequence[Point]] = None) -> dict:
    """Witness analysis of a distance constraint system on n points in R^d.

    Returns the witness, the rank, the redundant edges (each depends on the earlier ones), the number of
    internal degrees of freedom, and a verdict. 'well' means rigid and no redundant edge; 'under' means the
    witness shows a flex; 'over' means some edge is redundant. A 'well' verdict and a rigid verdict are always
    correct; 'under' and 'over' can be wrong with probability at most rank / box for a random witness."""
    rng = rng or random.Random(0)
    p = witness if witness is not None else random_witness(n, d, rng, box)  # @line L1
    rows = jacobian_rows(edges, p)  # @line L2
    space = RowSpace()
    redundant = []
    for e, row in zip(edges, rows):  # @line L3
        if not space.add(row):  # @line L4
            redundant.append(e)  # @line L4
    r = len(space.basis)  # @line L5
    full = d * n - trivial_dimension(d, n)  # @line L6
    flex = full - r  # @line L6
    if flex == 0 and not redundant:  # @line L7
        verdict = "well"
    elif flex > 0:
        verdict = "under"
    else:
        verdict = "over"
    return {"witness": p, "rank": r, "redundant": redundant, "flex": flex, "verdict": verdict}  # @line L8


def generic_rank(n: int, edges: Sequence[Edge], d: int = 2, rng: Optional[random.Random] = None,
                 box: int = 10**6, trials: int = 2) -> int:
    """The largest witness rank over independent witnesses. It never exceeds the generic rank."""
    rng = rng or random.Random(0)
    return max(rank(jacobian_rows(edges, random_witness(n, d, rng, box))) for _ in range(trials))
