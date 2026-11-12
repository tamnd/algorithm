# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/error-correcting-output-codes/. The authors are listed in prov/05H9N7.jsonl.
"""Error-correcting output codes. A k x l code matrix M with entries in {-1, 0, +1} gives one
binary problem per column (0 = the class is left out). Prediction decodes the vector of the
l binary outputs to the nearest row, by Hamming decoding or by loss-based decoding
(Allwein, Schapire and Singer 2000). Includes the exhaustive code of Dietterich and Bakiri
(1995), row distances, and the bound of Allwein, Schapire and Singer on the training error."""

from math import exp, log
from typing import Callable

Score = Callable[[list[float]], float]
BinaryLearner = Callable[[list[list[float]], list[int]], Score]


def exhaustive_code(k: int) -> list[list[int]]:
    """Dietterich and Bakiri: row 1 is all +1; row i (i >= 2) alternates runs of 2^(k-i)
    entries -1 and +1, starting with -1. There are 2^(k-1) - 1 columns."""
    if k < 3:
        raise ValueError("k must be at least 3")
    width = 2 ** (k - 1) - 1
    rows = [[1] * width]
    for i in range(2, k + 1):
        run = 2 ** (k - i)
        rows.append([-1 if (c // run) % 2 == 0 else 1 for c in range(width)])
    return rows


def one_vs_rest_code(k: int) -> list[list[int]]:
    return [[1 if r == c else -1 for c in range(k)] for r in range(k)]


def all_pairs_code(k: int) -> list[list[int]]:
    cols = [(i, j) for i in range(k) for j in range(i + 1, k)]
    return [[1 if r == i else -1 if r == j else 0 for i, j in cols] for r in range(k)]


def hamming_distance(u: list[int], v: list[int]) -> int:
    return sum(1 for a, b in zip(u, v) if a != b)


def min_row_distance(M: list[list[int]]) -> int:
    """Minimum Hamming distance between two rows of a {-1, +1} code."""
    return min(hamming_distance(M[r], M[s]) for r in range(len(M)) for s in range(r + 1, len(M)))


def generalized_distance(u: list[int], v: list[int]) -> float:
    """sum_s (1 - u_s v_s) / 2: 1 for opposite entries, 1/2 if either entry is 0, 0 if equal."""
    return sum((1 - a * b) / 2 for a, b in zip(u, v))


def rho(M: list[list[int]]) -> float:
    return min(generalized_distance(M[r], M[s]) for r in range(len(M)) for s in range(r + 1, len(M)))


def train(X: list[list[float]], y: list[int], M: list[list[int]], binary: BinaryLearner) -> list[Score]:
    """One binary learner per column s, on the examples whose class has a nonzero entry."""
    fs = []
    for s in range(len(M[0])):  # @line L1
        idx = [i for i, c in enumerate(y) if M[c][s] != 0]  # @line L2
        fs.append(binary([X[i] for i in idx], [M[y[i]][s] for i in idx]))  # @line L3
    return fs  # @line L4


def _sign(z: float) -> int:
    return (z > 0) - (z < 0)


def hamming_decode(M: list[list[int]], z: list[float]) -> int:
    """argmin_r sum_s (1 - sign(M[r][s] z_s)) / 2, with sign(0) = 0; smallest r on a tie."""
    d = [sum((1 - _sign(m * zs)) / 2 for m, zs in zip(row, z)) for row in M]
    return d.index(min(d))


def loss_decode(M: list[list[int]], z: list[float], loss: Callable[[float], float]) -> int:
    """argmin_r sum_s L(M[r][s] z_s); smallest r on a tie."""
    d = [sum(loss(m * zs) for m, zs in zip(row, z)) for row in M]
    return d.index(min(d))


def predict(fs: list[Score], M: list[list[int]], x: list[float],
            loss: Callable[[float], float] | None = None) -> int:
    z = [f(x) for f in fs]  # @line L5
    if loss is None:  # @line L6
        return hamming_decode(M, z)  # @line L7
    return loss_decode(M, z, loss)


def exp_loss(z: float) -> float:
    return exp(-z)


def logistic_loss(z: float) -> float:
    """log(1 + e^{-2z}), the scaling used by Allwein, Schapire and Singer."""
    t = -2 * z
    return max(t, 0.0) + log(1 + exp(-abs(t)))


def hinge_loss(z: float) -> float:
    return max(0.0, 1 - z)


def training_error_bound(M: list[list[int]], eps: float, loss: Callable[[float], float]) -> float:
    """Allwein, Schapire and Singer, Theorem 1: error <= l * eps / (rho * L(0))."""
    return len(M[0]) * eps / (rho(M) * loss(0.0))
