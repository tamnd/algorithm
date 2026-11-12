# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quadratic-discriminant-analysis/. The authors are listed in prov/GZK9TB.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from quadratic_discriminant_analysis import (
    QDA,
    back_solve_transpose,
    cholesky,
    forward_solve,
    lda_linear,
    log_det_from_cholesky,
)

X = [(0, 0), (2, 0), (0, 2), (2, 2), (4, 1), (6, 1), (5, 0), (5, 2)]
Y = ["A"] * 4 + ["B"] * 4


def exact_det_and_inverse(a):
    """Gauss-Jordan elimination over Fractions."""
    d = len(a)
    m = [[F(a[i][j]) for j in range(d)] + [F(int(i == j)) for j in range(d)] for i in range(d)]
    det = F(1)
    for col in range(d):
        piv = next(r for r in range(col, d) if m[r][col] != 0)
        if piv != col:
            m[col], m[piv] = m[piv], m[col]
            det = -det
        det *= m[col][col]
        p = m[col][col]
        m[col] = [v / p for v in m[col]]
        for r in range(d):
            if r != col and m[r][col] != 0:
                f = m[r][col]
                m[r] = [m[r][j] - f * m[col][j] for j in range(2 * d)]
    return det, [row[d:] for row in m]


def random_spd(rng, d):
    b = [[rng.randint(-3, 3) for _ in range(d)] for _ in range(d)]
    return [[sum(b[i][p] * b[j][p] for p in range(d)) + (i == j) for j in range(d)] for i in range(d)]


def test_cholesky_solve_and_log_det() -> None:
    rng = random.Random(1)
    for d in range(1, 6):
        for _ in range(20):
            a = random_spd(rng, d)
            low = cholesky(a)
            for i in range(d):
                for j in range(d):
                    assert sum(low[i][p] * low[j][p] for p in range(d)) == pytest.approx(a[i][j])
            det, inv = exact_det_and_inverse(a)
            assert log_det_from_cholesky(low) == pytest.approx(math.log(det))
            b = [rng.randint(-5, 5) for _ in range(d)]
            v = back_solve_transpose(low, forward_solve(low, b))
            want = [sum(inv[i][j] * b[j] for j in range(d)) for i in range(d)]
            assert v == pytest.approx([float(t) for t in want])


def test_cholesky_rejects_singular() -> None:
    with pytest.raises(ValueError):
        cholesky([[1.0, 1.0], [1.0, 1.0]])


def test_hand_example() -> None:
    q = QDA().fit(X, Y)
    assert q.mean == {"A": [1.0, 1.0], "B": [5.0, 1.0]}
    assert q.cov["A"] == [[1.0, 0.0], [0.0, 1.0]]
    assert q.cov["B"] == [[0.5, 0.0], [0.0, 0.5]]
    # The boundary is the circle |x - (9, 1)|^2 = 32 + 2 ln 2; class B is inside.
    r = math.sqrt(32 + 2 * math.log(2))
    for t in (0.0, 1.0, 2.5, 4.0):
        p = (9 + r * math.cos(t), 1 + r * math.sin(t))
        s = q.discriminants(p)
        assert s["A"] == pytest.approx(s["B"], abs=1e-9)
    assert [q.predict((x, 1)) for x in (3, 3.5, 14, 16)] == ["A", "B", "B", "A"]


def test_discriminant_against_exact_gaussian() -> None:
    rng = random.Random(2)
    for _ in range(30):
        d = rng.randint(1, 3)
        xs = [tuple(rng.randint(-4, 4) for _ in range(d)) for _ in range(12)]
        ys = [i % 3 for i in range(12)]
        try:
            q = QDA().fit(xs, ys)
        except ValueError:
            continue
        x = [rng.uniform(-5, 5) for _ in range(d)]
        for c in q.classes:
            det, inv = exact_det_and_inverse(q.cov[c])
            dev = [x[j] - q.mean[c][j] for j in range(d)]
            quad = sum(dev[i] * float(inv[i][j]) * dev[j] for i in range(d) for j in range(d))
            want = -0.5 * math.log(det) - 0.5 * quad + math.log(4 / 12)
            assert q.discriminants(x)[c] == pytest.approx(want, rel=1e-9, abs=1e-9)


def test_pooled_covariance_gives_the_lda_boundary() -> None:
    rng = random.Random(3)
    for _ in range(30):
        xs = [(rng.uniform(-3, 3), rng.uniform(-3, 3)) for _ in range(10)]
        ys = ["n"] * 4 + ["p"] * 6
        q = QDA(lam=1.0).fit(xs, ys)
        w, c = lda_linear(xs, ys, "p", "n")
        for _ in range(10):
            x = (rng.uniform(-9, 9), rng.uniform(-9, 9))
            s = q.discriminants(x)
            assert s["p"] - s["n"] == pytest.approx(w[0] * x[0] + w[1] * x[1] + c, abs=1e-9)


def test_equal_class_covariances_give_the_lda_boundary() -> None:
    # Class p is a translate of class n, so both sample covariances are equal
    # and plain QDA (lam = 0) has the same linear boundary as LDA.
    rng = random.Random(4)
    for _ in range(20):
        base = [(rng.uniform(-2, 2), rng.uniform(-2, 2)) for _ in range(5)]
        shift = (rng.uniform(-3, 3), rng.uniform(-3, 3))
        xs = base + [(a + shift[0], b + shift[1]) for a, b in base]
        ys = ["n"] * 5 + ["p"] * 5
        q = QDA().fit(xs, ys)
        w, c = lda_linear(xs, ys, "p", "n")
        for _ in range(10):
            x = (rng.uniform(-9, 9), rng.uniform(-9, 9))
            s = q.discriminants(x)
            assert s["p"] - s["n"] == pytest.approx(w[0] * x[0] + w[1] * x[1] + c, abs=1e-8)


def test_rda_regularization() -> None:
    q = QDA(lam=0.5).fit(X, Y)
    assert q.cov["A"][0][0] == pytest.approx(5 / 6) and q.cov["B"][0][0] == pytest.approx(2 / 3)
    g = QDA(gam=1.0).fit([(0, 0), (2, 0), (0, 1), (2, 1), (9, 9), (9, 8)], [0, 0, 0, 0, 1, 1])
    assert g.cov[0] == [[0.625, 0.0], [0.0, 0.625]]
    # Two points per class on a line: the class covariance is singular,
    # and pooling with lam > 0 makes it invertible.
    xs = [(0, 0), (1, 1), (5, 0), (6, 2)]
    ys = [0, 0, 1, 1]
    with pytest.raises(ValueError):
        QDA().fit(xs, ys)
    assert QDA(lam=0.5).fit(xs, ys).predict((0.5, 0.5)) == 0


def test_probabilities_sum_to_one() -> None:
    q = QDA().fit(X, Y)
    for p in [(1, 1), (5, 1), (100, -40)]:
        pr = q.predict_proba(p)
        assert sum(pr.values()) == pytest.approx(1.0)
