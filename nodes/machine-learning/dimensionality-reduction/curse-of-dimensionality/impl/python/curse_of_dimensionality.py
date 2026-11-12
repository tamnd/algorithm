# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/curse-of-dimensionality/. The authors are listed in prov/QWKNH3.jsonl.

"""Numbers that show the curse of dimensionality.

ball_volume            volume of the unit ball in R^d, pi^(d/2) / Gamma(d/2 + 1)
ball_volume_exact      the same volume as (c, j) with V_d = c * pi^j and c rational
shell_fraction         fraction of the unit ball within distance eps of its surface
edge_for_fraction      edge of a subcube that holds a fraction p of the unit cube
median_nn_distance     median distance from the origin to the nearest of n uniform points in the unit ball
grid_cells             number of cells of a grid with k cells per axis
relative_contrast      (D_max - D_min) / D_min for one query
contrast_experiment    mean relative contrast of uniform data in the unit cube
stone_rate             Stone's optimal rate n^(-2s/(2s+d)) for estimating an s-smooth regression function
samples_for_error      n such that the rate n^(-2s/(2s+d)) equals a target error
"""

from fractions import Fraction
import math
import random


def ball_volume(d: int, r: float = 1.0) -> float:
    """Volume of the Euclidean ball of radius r in R^d."""
    if d < 0:
        raise ValueError("d must be nonnegative")
    return math.pi ** (d / 2) / math.gamma(d / 2 + 1) * r ** d


def ball_volume_exact(d: int) -> tuple[Fraction, int]:
    """(c, j) with V_d = c * pi^j, from V_0 = 1, V_1 = 2 and V_d = (2 pi / d) V_(d-2)."""
    if d < 0:
        raise ValueError("d must be nonnegative")
    c, j = (Fraction(1), 0) if d % 2 == 0 else (Fraction(2), 0)
    for m in range(2 + d % 2, d + 1, 2):
        c, j = c * Fraction(2, m), j + 1
    return c, j


def shell_fraction(d: int, eps: float) -> float:
    """Fraction of the volume of the unit ball with norm greater than 1 - eps."""
    return 1.0 - (1.0 - eps) ** d


def edge_for_fraction(p: float, d: int) -> float:
    """Edge length of a cube inside [0, 1]^d that holds the fraction p of the volume."""
    return p ** (1.0 / d)


def median_nn_distance(n: int, d: int) -> float:
    """Median distance from the origin to the nearest of n points uniform in the unit ball of R^d.

    P(all n points farther than r) = (1 - r^d)^n; setting this to 1/2 gives the median.
    """
    return (1.0 - 0.5 ** (1.0 / n)) ** (1.0 / d)


def grid_cells(k: int, d: int) -> int:
    """A grid with k cells along each of d axes has k^d cells."""
    return k ** d


def _dist(p: list[float], q: list[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p, q)))


def relative_contrast(points: list[list[float]], query: list[float]) -> float:
    """(D_max - D_min) / D_min over the distances from the query to the points."""
    ds = [_dist(p, query) for p in points]
    lo, hi = min(ds), max(ds)
    if lo == 0:
        raise ValueError("a point coincides with the query")
    return (hi - lo) / lo


def contrast_experiment(d: int, n: int, trials: int, rng: random.Random) -> float:
    """Mean relative contrast of n uniform points in [0, 1]^d for a uniform query."""
    total = 0.0
    for _ in range(trials):
        pts = [[rng.random() for _ in range(d)] for _ in range(n)]
        q = [rng.random() for _ in range(d)]
        total += relative_contrast(pts, q)
    return total / trials


def stone_rate(n: float, s: float, d: int) -> float:
    """Stone's optimal convergence rate n^(-2s/(2s+d)) for the squared error."""
    return n ** (-2.0 * s / (2.0 * s + d))


def samples_for_error(err: float, s: float, d: int) -> float:
    """The n with stone_rate(n, s, d) = err, that is err^(-(2s+d)/(2s))."""
    return err ** (-(2.0 * s + d) / (2.0 * s))
