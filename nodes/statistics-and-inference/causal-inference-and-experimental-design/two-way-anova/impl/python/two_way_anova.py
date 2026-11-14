# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-way-anova/. The authors are listed in prov/E9ZZA5.jsonl.
"""Two-way analysis of variance with sequential (type I), type II and type III sums of squares.

Each sum of squares is a difference of residual sums of squares of two nested
least squares fits, RSS(smaller) - RSS(larger). The factors are coded by
sum-to-zero (effect) columns: level j < L of a factor with L levels gets the
indicator of j minus the indicator of level L. With this coding the type III
hypotheses are the equal marginal means of the cell means, as in the
textbooks; with treatment (0/1) coding the "type III" main effect would test
a simple effect at the last level of the other factor instead.

Residual sums of squares come from modified Gram-Schmidt with one
reorthogonalization pass, so no normal equations X^T X are formed.
For balanced data all three types agree with the classical closed forms in
balanced_two_way.
"""

import math
from collections.abc import Hashable, Sequence
from typing import NamedTuple

from stdist import f_sf


class Row(NamedTuple):
    source: str
    ss: float
    df: int
    f: float
    p: float


def effect_columns(labels: Sequence[Hashable], levels: Sequence[Hashable]) -> list[list[float]]:
    """Sum-to-zero coding: one column per level except the last."""
    last = levels[-1]
    return [[1.0 if v == lev else (-1.0 if v == last else 0.0) for v in labels]
            for lev in levels[:-1]]


def rss(columns: list[list[float]], y: Sequence[float]) -> float:
    """Residual sum of squares of the least squares fit of y on the columns (full column rank)."""
    basis: list[list[float]] = []
    r = list(y)
    for col in columns:
        v = list(col)
        for _ in range(2):  # modified Gram-Schmidt, then one reorthogonalization pass
            for q in basis:
                c = math.fsum(a * b for a, b in zip(q, v))
                v = [a - c * b for a, b in zip(v, q)]
        norm = math.sqrt(math.fsum(a * a for a in v))
        if norm <= 1e-10 * math.sqrt(math.fsum(a * a for a in col)):
            raise ValueError("the columns are linearly dependent (an empty cell?)")
        q = [a / norm for a in v]
        basis.append(q)
        for _ in range(2):
            c = math.fsum(a * b for a, b in zip(q, r))
            r = [a - c * b for a, b in zip(r, q)]
    return math.fsum(a * a for a in r)


def two_way_anova(y: Sequence[float], a: Sequence[Hashable], b: Sequence[Hashable],
                  ss_type: int = 2, interaction: bool = True) -> list[Row]:
    """ANOVA table rows for A, B, (A:B,) and Error. Every cell must hold data."""
    n = len(y)
    if not (len(a) == len(b) == n):
        raise ValueError("y, a and b must have the same length")
    la, lb = sorted(set(a), key=str), sorted(set(b), key=str)
    cells = {(u, v) for u, v in zip(a, b)}
    if interaction and len(cells) < len(la) * len(lb):
        raise ValueError("a cell is empty; the interaction model is not estimable")
    one = [[1.0] * n]  # @line L1
    ca = effect_columns(a, la)
    cb = effect_columns(b, lb)
    cab = [[x * z for x, z in zip(u, v)] for u in ca for v in cb] if interaction else []
    full = one + ca + cb + cab
    df_e = n - len(full)
    if df_e < 1:
        raise ValueError("no degrees of freedom are left for the error")
    sse = rss(full, y)  # @line L2
    if ss_type == 1:  # sequential: A, then B given A, then A:B given both
        r1, ra, rab = rss(one, y), rss(one + ca, y), rss(one + ca + cb, y)
        ss = {"A": r1 - ra, "B": ra - rab}  # @line L3
    elif ss_type == 2:  # each main effect after the other main effect
        rab = rss(one + ca + cb, y)
        ss = {"A": rss(one + cb, y) - rab, "B": rss(one + ca, y) - rab}  # @line L4
    elif ss_type == 3:  # each term after all others, sum-to-zero coding
        ss = {"A": rss(one + cb + cab, y) - sse, "B": rss(one + ca + cab, y) - sse}  # @line L5
        rab = rss(one + ca + cb, y)
    else:
        raise ValueError("ss_type must be 1, 2 or 3")
    df = {"A": len(ca), "B": len(cb)}
    if interaction:
        ss["A:B"] = rab - sse  # @line L6
        df["A:B"] = len(cab)
    mse = sse / df_e
    rows = []
    for name in ss:
        f = (ss[name] / df[name]) / mse  # @line L7
        rows.append(Row(name, ss[name], df[name], f, f_sf(f, df[name], df_e)))
    rows.append(Row("Error", sse, df_e, math.nan, math.nan))
    return rows  # @line L8


def balanced_two_way(cells: Sequence[Sequence[Sequence[float]]]) -> dict[str, float]:
    """Closed-form sums of squares of a balanced a x b layout, cells[i][j] holding n values."""
    na, nb, n = len(cells), len(cells[0]), len(cells[0][0])
    cm = [[math.fsum(c) / n for c in row] for row in cells]
    am = [math.fsum(row) / nb for row in cm]
    bm = [math.fsum(cm[i][j] for i in range(na)) / na for j in range(nb)]
    g = math.fsum(am) / na
    return {
        "A": nb * n * math.fsum((m - g) ** 2 for m in am),
        "B": na * n * math.fsum((m - g) ** 2 for m in bm),
        "A:B": n * math.fsum((cm[i][j] - am[i] - bm[j] + g) ** 2 for i in range(na) for j in range(nb)),
        "Error": math.fsum((v - cm[i][j]) ** 2 for i in range(na) for j in range(nb)
                           for v in cells[i][j]),
    }
