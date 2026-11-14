# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/difference-in-differences/. The authors are listed in prov/XKDP5H.jsonl.

"""Difference in differences.

did_panel: two periods, a panel of units, some treated in the second period. The estimate
is the mean change of the treated minus the mean change of the controls, with a standard
error built from the unit changes (so it allows any correlation within a unit).

did_means and did_regression: the same contrast for repeated cross-sections, from the four
cell means and from OLS of y on (1, treat, post, treat * post). The two agree exactly.

twfe, twfe_weights and att_gt: a balanced panel with staggered adoption. twfe is the
two-way fixed effects coefficient, twfe_weights gives the exact weights it puts on each
treated cell's effect (some can be negative), and att_gt is the group-time effect against
never-treated units.

Everything is exact for Fraction inputs except the standard errors.
"""

import math
from collections.abc import Sequence
from fractions import Fraction
from statistics import NormalDist
from typing import NamedTuple


class DidResult(NamedTuple):
    tau: object  # the estimate
    se: float  # standard error from the unit changes (Welch form, equal to HC2)
    change_treated: object  # mean change of the treated units
    change_control: object  # mean change of the control units
    n_treated: int
    n_control: int


def _mean(v):
    return sum(v) / len(v)


def _var(v):
    m = _mean(v)
    return sum((a - m) * (a - m) for a in v) / (len(v) - 1)


def did_panel(y_pre: Sequence, y_post: Sequence, treated: Sequence) -> DidResult:
    """Two-period panel. Cost: Theta(n)."""
    n = len(y_pre)
    if len(y_post) != n or len(treated) != n:
        raise ValueError("y_pre, y_post and treated need the same length")
    change = [b - a for a, b in zip(y_pre, y_post)]  # @line L1
    ct = [c for c, t in zip(change, treated) if t]
    cc = [c for c, t in zip(change, treated) if not t]
    if len(ct) < 2 or len(cc) < 2:
        raise ValueError("need at least 2 treated and 2 control units")
    tau = _mean(ct) - _mean(cc)  # @line L2
    se = math.sqrt(float(_var(ct)) / len(ct) + float(_var(cc)) / len(cc))  # @line L3
    return DidResult(tau, se, _mean(ct), _mean(cc), len(ct), len(cc))  # @line L4


def interval(res: DidResult, alpha: float = 0.05) -> tuple[float, float]:
    """Large-sample normal interval."""
    z = NormalDist().inv_cdf(1 - alpha / 2)
    return float(res.tau) - z * res.se, float(res.tau) + z * res.se


def did_means(y: Sequence, treat: Sequence, post: Sequence) -> object:
    """(mean y11 - mean y10) - (mean y01 - mean y00) over the four treat/post cells."""
    cells = {(a, b): [] for a in (0, 1) for b in (0, 1)}
    for v, a, b in zip(y, treat, post):
        cells[(int(a), int(b))].append(v)
    if any(not c for c in cells.values()):
        raise ValueError("every treat/post cell needs at least one observation")
    m = {k: _mean(c) for k, c in cells.items()}
    return (m[(1, 1)] - m[(1, 0)]) - (m[(0, 1)] - m[(0, 0)])


def solve(a: list[list], b: list) -> list:
    """Solve a x = b by Gauss-Jordan elimination with partial pivoting (exact for Fractions)."""
    k = len(a)
    m = [list(r) + [v] for r, v in zip(a, b)]
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0:
            raise ValueError("singular matrix")
        m[c], m[p] = m[p], m[c]
        for r in range(k):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                for j in range(c, k + 1):
                    m[r][j] -= f * m[c][j]
    return [m[r][k] / m[r][r] for r in range(k)]


def ols(x: list[list], y: Sequence) -> list:
    k = len(x[0])
    xtx = [[sum(r[i] * r[j] for r in x) for j in range(k)] for i in range(k)]
    xty = [sum(r[i] * v for r, v in zip(x, y)) for i in range(k)]
    return solve(xtx, xty)


def did_regression(y: Sequence, treat: Sequence, post: Sequence) -> list:
    """OLS coefficients of y on (1, treat, post, treat * post); the last one is the estimate."""
    one = y[0] * 0 + 1
    x = [[one, one * a, one * b, one * a * b] for a, b in zip(treat, post)]
    return ols(x, y)


def _double_demean(m: list[list]) -> list[list]:
    """m[i][t] - row mean - column mean + grand mean. Integer entries (0/1 treatment) become
    Fractions so the result stays exact."""
    m = [[Fraction(v) if isinstance(v, int) else v for v in r] for r in m]
    n, t = len(m), len(m[0])
    row = [sum(r) / t for r in m]
    col = [sum(m[i][j] for i in range(n)) / n for j in range(t)]
    grand = sum(row) / n
    return [[m[i][j] - row[i] - col[j] + grand for j in range(t)] for i in range(n)]


def twfe(y: list[list], d: list[list]) -> object:
    """Coefficient of d in OLS of y on d plus unit and period dummies, balanced panel y[i][t].
    By Frisch-Waugh-Lovell it is sum(dd * y) / sum(dd * dd), dd the double-demeaned d."""
    dd = _double_demean(d)
    den = sum(v * v for r in dd for v in r)
    if den == 0:
        raise ValueError("the treatment is collinear with the fixed effects")
    return sum(a * b for ra, rb in zip(dd, y) for a, b in zip(ra, rb)) / den


def twfe_weights(d: list[list]) -> dict:
    """Weights w[(i, t)] on the treated cells with twfe = sum w[(i, t)] * tau[i][t] whenever
    y[i][t] = a_i + b_t + tau[i][t] d[i][t]. They sum to 1 and can be negative."""
    dd = _double_demean(d)
    den = sum(a * b for ra, rb in zip(dd, d) for a, b in zip(ra, rb))
    return {(i, t): dd[i][t] / den for i in range(len(d)) for t in range(len(d[0])) if d[i][t]}


def twfe_dummies(y: list[list], d: list[list]) -> object:
    """The same coefficient from the full OLS with dummies, for checking."""
    n, t = len(y), len(y[0])
    one = y[0][0] * 0 + 1
    x, yy = [], []
    for i in range(n):
        for s in range(t):
            unit = [one if i == j else one - one for j in range(n)]
            period = [one if s == j else one - one for j in range(1, t)]
            x.append([one * d[i][s]] + unit + period)
            yy.append(y[i][s])
    return ols(x, yy)[0]


def att_gt(y: list[list], first: Sequence, g: int, t: int) -> object:
    """Effect at period t for the units first treated at period g (g >= 1), against the units
    never treated (first[i] is None), with base period g - 1:
    (mean y[t] - mean y[g-1]) over group g minus the same over never-treated units."""
    grp = [i for i, f in enumerate(first) if f == g]
    never = [i for i, f in enumerate(first) if f is None]
    if not grp or not never or g < 1:
        raise ValueError("need units in group g, never-treated units, and g >= 1")
    ch = [y[i][t] - y[i][g - 1] for i in grp]
    cn = [y[i][t] - y[i][g - 1] for i in never]
    return _mean(ch) - _mean(cn)
