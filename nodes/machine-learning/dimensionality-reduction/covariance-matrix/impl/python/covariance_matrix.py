# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/covariance-matrix/. The authors are listed in prov/N5JYXB.jsonl.

"""Sample covariance matrices: two-pass, Welford updates and the pairwise merge.

The co-moment matrix of the points x_1, ..., x_n in R^d is
M = sum_i (x_i - mean)(x_i - mean)^T. The sample covariance is M / (n - 1),
and the maximum likelihood estimate is M / n. All functions work with float
or with fractions.Fraction entries, so the tests can check them exactly.
"""

from dataclasses import dataclass, field
from typing import Any

Matrix = list[list[Any]]
Vector = list[Any]


def two_pass_covariance(points: list[Vector], ddof: int = 1) -> Matrix:
    """Center first, then sum the outer products. Divide by n - ddof.

    ddof = 1 gives the unbiased sample covariance, ddof = 0 the MLE.
    Precondition: n > ddof. Cost: O(n d^2) operations, O(d^2) extra memory.
    """
    n, d = len(points), len(points[0])
    if n <= ddof:
        raise ValueError("need more points than ddof")
    mean = [sum(p[j] for p in points) / n for j in range(d)]
    c = [[0 * mean[0] for _ in range(d)] for _ in range(d)]
    for p in points:
        z = [p[j] - mean[j] for j in range(d)]
        for a in range(d):
            for b in range(d):
                c[a][b] += z[a] * z[b]
    return [[c[a][b] / (n - ddof) for b in range(d)] for a in range(d)]


def naive_covariance(points: list[Vector], ddof: int = 1) -> Matrix:
    """The one-pass textbook formula (sum x x^T - n mean mean^T) / (n - ddof).

    It is exact in exact arithmetic, but it loses precision in floating
    point when the mean is large compared with the spread. It is here only to
    show that pitfall.
    """
    n, d = len(points), len(points[0])
    s = [sum(p[j] for p in points) for j in range(d)]
    q = [[sum(p[a] * p[b] for p in points) for b in range(d)] for a in range(d)]
    return [[(q[a][b] - s[a] * s[b] / n) / (n - ddof) for b in range(d)] for a in range(d)]


@dataclass
class RunningCovariance:
    """Welford updates and the Chan, Golub and LeVeque merge.

    The state is the count n, the mean and the co-moment matrix m.
    Each update costs O(d^2) operations; the memory is O(d^2).
    """

    d: int
    n: int = 0
    mean: Vector = field(default_factory=list)
    m: Matrix = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.mean:
            self.mean = [0] * self.d
        if not self.m:
            self.m = [[0] * self.d for _ in range(self.d)]

    def add(self, x: Vector) -> None:
        """Welford: mean += delta / n, then m += delta (x - new mean)^T."""
        self.n += 1
        delta = [x[j] - self.mean[j] for j in range(self.d)]
        self.mean = [self.mean[j] + delta[j] / self.n for j in range(self.d)]
        after = [x[j] - self.mean[j] for j in range(self.d)]
        for a in range(self.d):
            for b in range(self.d):
                self.m[a][b] += delta[a] * after[b]

    def merge(self, other: "RunningCovariance") -> "RunningCovariance":
        """Combine two summaries of disjoint sets of points.

        m = m_A + m_B + delta delta^T n_A n_B / n, with delta = mean_B - mean_A.
        """
        if other.n == 0:
            return RunningCovariance(self.d, self.n, list(self.mean), [r[:] for r in self.m])
        if self.n == 0:
            return RunningCovariance(other.d, other.n, list(other.mean), [r[:] for r in other.m])
        n = self.n + other.n
        delta = [other.mean[j] - self.mean[j] for j in range(self.d)]
        mean = [self.mean[j] + delta[j] * other.n / n for j in range(self.d)]
        f = self.n * other.n
        m = [
            [self.m[a][b] + other.m[a][b] + delta[a] * delta[b] * f / n for b in range(self.d)]
            for a in range(self.d)
        ]
        return RunningCovariance(self.d, n, mean, m)

    def covariance(self, ddof: int = 1) -> Matrix:
        """Return m / (n - ddof). Precondition: n > ddof."""
        if self.n <= ddof:
            raise ValueError("need more points than ddof")
        return [[v / (self.n - ddof) for v in row] for row in self.m]
