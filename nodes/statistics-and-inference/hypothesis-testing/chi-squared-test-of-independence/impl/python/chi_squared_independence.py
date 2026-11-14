# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chi-squared-test-of-independence/. The authors are listed in prov/E5V169.jsonl.

import math
from collections.abc import Sequence

from stdist import chi2_sf


def chi_squared_independence(
    table: Sequence[Sequence[int]],
    statistic: str = "pearson",
    yates: bool = False,
) -> tuple[float, int, float]:
    """Pearson's chi-squared test of independence for an r x c contingency table.

    The expected count of cell (i, j) is (row total i)(column total j)/n.
    statistic "pearson" gives X^2 = sum (O - E)^2 / E; "g" gives the
    likelihood-ratio statistic G = 2 sum O log(O / E). yates=True applies
    Yates's continuity correction, (|O - E| - 1/2)^2 / E with |O - E| - 1/2
    floored at 0, and is allowed only for a 2 x 2 table with statistic "pearson".
    Returns (statistic, (r - 1)(c - 1), upper chi-square tail p-value).
    """
    r = len(table)
    if r < 2 or any(len(row) != len(table[0]) for row in table) or len(table[0]) < 2:
        raise ValueError("need a rectangular table with at least two rows and two columns")
    if any(not isinstance(o, int) or o < 0 for row in table for o in row):
        raise ValueError("counts must be non-negative integers")
    if statistic not in ("pearson", "g"):
        raise ValueError("unknown statistic")
    c = len(table[0])
    if yates and (r, c, statistic) != (2, 2, "pearson"):
        raise ValueError("the Yates correction is for the Pearson statistic of a 2 x 2 table")
    rows = [sum(row) for row in table]  # @line L1
    cols = [sum(table[i][j] for i in range(r)) for j in range(c)]
    n = sum(rows)
    if min(rows) == 0 or min(cols) == 0:
        raise ValueError("every row and column total must be positive")
    terms = []
    for i in range(r):  # @line L2
        for j in range(c):
            o, e = table[i][j], rows[i] * cols[j] / n  # @line L3
            if statistic == "g":  # @line L4
                if o > 0:
                    terms.append(2.0 * o * math.log(o * n / (rows[i] * cols[j])))
            else:
                d = abs(o - e)
                if yates:
                    d = max(0.0, d - 0.5)
                terms.append(d * d / e)
    x2 = math.fsum(terms)  # @line L5
    df = (r - 1) * (c - 1)  # @line L6
    return x2, df, chi2_sf(x2, df)  # @line L7
