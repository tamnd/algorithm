# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conditional-entropy/. The authors are listed in prov/70YZ8M.jsonl.
"""Joint, marginal and conditional entropy and mutual information from a joint table p[x][y]."""

from math import log2
from typing import Sequence

Table = Sequence[Sequence[float]]


def _h(ps) -> float:
    return -sum(p * log2(p) for p in ps if p > 0)


def check_table(p: Table) -> None:
    if any(v < 0 for row in p for v in row):
        raise ValueError("a probability is negative")
    if abs(sum(v for row in p for v in row) - 1.0) > 1e-9:
        raise ValueError("the table does not sum to 1")


def marginal_x(p: Table) -> list[float]:
    return [sum(row) for row in p]


def marginal_y(p: Table) -> list[float]:
    return [sum(row[j] for row in p) for j in range(len(p[0]))]


def joint_entropy(p: Table) -> float:
    check_table(p)
    return _h(v for row in p for v in row)


def entropy_x(p: Table) -> float:
    return _h(marginal_x(p))


def entropy_y(p: Table) -> float:
    return _h(marginal_y(p))


def entropy_x_given_y_equals(p: Table, j: int) -> float:
    """H(X | Y = y_j), the entropy of the column j after normalization."""
    col = [row[j] for row in p]
    s = sum(col)
    if s == 0:
        raise ValueError("P(Y = y_j) is 0")
    return _h(v / s for v in col)


def conditional_entropy(p: Table) -> float:
    """H(X | Y) = sum over (x, y) of p(x, y) log2(p(y) / p(x, y)), computed from the definition."""
    check_table(p)
    py = marginal_y(p)
    return sum(v * log2(py[j] / v) for row in p for j, v in enumerate(row) if v > 0)


def mutual_information(p: Table) -> float:
    """I(X; Y) = sum p(x, y) log2(p(x, y) / (p(x) p(y)))."""
    check_table(p)
    px, py = marginal_x(p), marginal_y(p)
    return sum(v * log2(v / (px[i] * py[j])) for i, row in enumerate(p) for j, v in enumerate(row) if v > 0)
