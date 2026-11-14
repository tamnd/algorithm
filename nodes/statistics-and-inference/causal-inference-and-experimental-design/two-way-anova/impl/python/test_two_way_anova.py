# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-way-anova/. The authors are listed in prov/E9ZZA5.jsonl.

import math
import random
from fractions import Fraction

import pytest

from two_way_anova import balanced_two_way, two_way_anova

UNBALANCED = {("a1", "b1"): [3, 5], ("a1", "b2"): [7], ("a2", "b1"): [6], ("a2", "b2"): [10, 12, 11]}
BALANCED = [[[12, 14], [18, 16], [21, 23]], [[15, 13], [24, 22], [30, 28]]]


def flatten(cells: dict) -> tuple[list, list, list]:
    y, a, b = [], [], []
    for (u, v), vals in cells.items():
        for x in vals:
            y.append(x)
            a.append(u)
            b.append(v)
    return y, a, b


def rss_exact(cols: list[list[int]], y: list[int]) -> Fraction:
    """RSS by solving the normal equations X^T X beta = X^T y in exact arithmetic."""
    k = len(cols)
    m = [[sum(Fraction(p) * q for p, q in zip(cols[i], cols[j])) for j in range(k)]
         + [sum(Fraction(p) * v for p, v in zip(cols[i], y))] for i in range(k)]
    for c in range(k):
        piv = next(r for r in range(c, k) if m[r][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        for r in range(k):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * z for x, z in zip(m[r], m[c])]
    beta = [m[i][k] / m[i][i] for i in range(k)]
    return sum((v - sum(beta[i] * cols[i][t] for i in range(k))) ** 2 for t, v in enumerate(y))


def brute_force(y: list[int], a: list, b: list) -> dict[int, dict[str, Fraction]]:
    """Types I, II and III as explicit comparisons of nested models, in exact arithmetic."""
    la, lb = sorted(set(a), key=str), sorted(set(b), key=str)
    one = [[1] * len(y)]
    ca = [[1 if v == l else (-1 if v == la[-1] else 0) for v in a] for l in la[:-1]]
    cb = [[1 if v == l else (-1 if v == lb[-1] else 0) for v in b] for l in lb[:-1]]
    cab = [[p * q for p, q in zip(u, v)] for u in ca for v in cb]
    r = lambda cols: rss_exact(cols, y)
    full, add = r(one + ca + cb + cab), r(one + ca + cb)
    inter = add - full
    return {
        1: {"A": r(one) - r(one + ca), "B": r(one + ca) - add, "A:B": inter},
        2: {"A": r(one + cb) - add, "B": r(one + ca) - add, "A:B": inter},
        3: {"A": r(one + cb + cab) - full, "B": r(one + ca + cab) - full, "A:B": inter},
        0: {"Error": full},
    }


def table(rows) -> dict[str, float]:
    return {row.source: row.ss for row in rows}


def test_unbalanced_example_exact() -> None:
    y, a, b = flatten(UNBALANCED)
    exact = brute_force(y, a, b)
    assert exact[1] == {"A": Fraction(1083, 28), "B": Fraction(1587, 68), "A:B": Fraction(24, 17)}
    assert exact[2]["A"] == Fraction(676, 51) and exact[2]["B"] == Fraction(1587, 68)
    assert exact[3] == {"A": Fraction(216, 17), "B": Fraction(384, 17), "A:B": Fraction(24, 17)}
    assert exact[0]["Error"] == 4
    for t in (1, 2, 3):
        got = table(two_way_anova(y, a, b, t))
        for name, value in exact[t].items():
            assert abs(got[name] - float(value)) < 1e-10
        assert abs(got["Error"] - 4.0) < 1e-10


def test_type_three_is_the_marginal_mean_contrast() -> None:
    # Type III SS of A tests (mu11 + mu12)/2 = (mu21 + mu22)/2: psi_hat^2 / sum(c^2 / n).
    y, a, b = flatten(UNBALANCED)
    mean = {key: Fraction(sum(v), len(v)) for key, v in UNBALANCED.items()}
    size = {key: len(v) for key, v in UNBALANCED.items()}
    for factor, sign in (("A", lambda u, v: 1 if u == "a1" else -1),
                         ("B", lambda u, v: 1 if v == "b1" else -1),
                         ("A:B", lambda u, v: 1 if (u == "a1") == (v == "b1") else -1)):
        c = {key: Fraction(sign(*key), 1 if factor == "A:B" else 2) for key in mean}
        psi = sum(c[key] * mean[key] for key in mean)
        ss = psi ** 2 / sum(c[key] ** 2 / size[key] for key in mean)
        assert ss == brute_force(y, a, b)[3][factor]


def test_random_unbalanced_layouts() -> None:
    rng = random.Random(5)
    for _ in range(25):
        la, lb = rng.randint(2, 3), rng.randint(2, 3)
        y, a, b = [], [], []
        for i in range(la):
            for j in range(lb):
                for _ in range(rng.randint(1, 3)):
                    y.append(rng.randint(-20, 20))
                    a.append(f"a{i}")
                    b.append(f"b{j}")
        if len(y) <= la * lb:
            y.append(1)
            a.append("a0")
            b.append("b0")
        exact = brute_force(y, a, b)
        for t in (1, 2, 3):
            got = table(two_way_anova(y, a, b, t))
            for name, value in exact[t].items():
                assert abs(got[name] - float(value)) <= 1e-9 * max(1.0, float(value))


def test_balanced_types_agree_with_closed_form() -> None:
    y, a, b = [], [], []
    for i, row in enumerate(BALANCED):
        for j, cell in enumerate(row):
            for v in cell:
                y.append(v)
                a.append(f"A{i + 1}")
                b.append(f"B{j + 1}")
    closed = balanced_two_way(BALANCED)
    assert abs(closed["A"] - 196 / 3) < 1e-12 and abs(closed["B"] - 866 / 3) < 1e-12
    assert abs(closed["A:B"] - 62 / 3) < 1e-12 and closed["Error"] == 12.0
    grand = sum(y) / len(y)
    assert abs(sum(closed.values()) - sum((v - grand) ** 2 for v in y)) < 1e-9
    for t in (1, 2, 3):
        got = table(two_way_anova(y, a, b, t))
        for name in closed:
            assert abs(got[name] - closed[name]) < 1e-9
    rows = {row.source: row for row in two_way_anova(y, a, b)}
    assert abs(rows["A:B"].f - 31 / 6) < 1e-12 and rows["A:B"].df == 2
    assert abs(rows["A:B"].p - 0.04957118207549574) < 1e-10


def test_sequential_order_matters_when_unbalanced() -> None:
    y, a, b = flatten(UNBALANCED)
    ab = table(two_way_anova(y, a, b, 1))
    ba = table(two_way_anova(y, b, a, 1))  # B entered first
    assert abs(ba["A"] - 1024 / 21) < 1e-10 and abs(ab["A"] - 1083 / 28) < 1e-10
    assert abs((ab["A"] + ab["B"]) - (ba["A"] + ba["B"])) < 1e-10  # the joint SS does not depend on order


def test_additive_model_size() -> None:
    # One observation per cell, no interaction: the F-test of A has size alpha under the null.
    rng = random.Random(6)
    reps, alpha, rej = 2000, 0.05, 0
    a = [f"t{i}" for i in range(4) for _ in range(5)]
    b = [f"k{j}" for _ in range(4) for j in range(5)]
    for _ in range(reps):
        y = [rng.gauss(0.0, 1.0) + 3.0 * j for _ in range(4) for j in range(5)]
        rej += two_way_anova(y, a, b, 1, interaction=False)[0].p <= alpha
    assert abs(rej / reps - alpha) < 4.0 * math.sqrt(alpha * (1 - alpha) / reps)


def test_errors() -> None:
    with pytest.raises(ValueError):
        two_way_anova([1.0, 2.0, 3.0], ["a", "a", "b"], ["x", "y", "x"])  # empty cell
    with pytest.raises(ValueError):
        two_way_anova([1.0, 2.0, 3.0, 4.0], ["a", "a", "b", "b"], ["x", "y", "x", "y"])  # no error df
    with pytest.raises(ValueError):
        two_way_anova([1.0] * 8, ["a", "b"] * 4, ["x"] * 4 + ["y"] * 4, ss_type=4)
