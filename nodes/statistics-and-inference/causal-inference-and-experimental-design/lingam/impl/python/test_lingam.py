# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lingam/. The authors are listed in prov/YZF859.jsonl.

import itertools
import random
from fractions import Fraction

from lingam import direct_lingam, gaussian_noise, simulate, uniform_noise

EX_ORDER = ["A", "B", "C", "D", "E"]
EX_WEIGHTS = {("A", "B"): 0.8, ("A", "C"): 0.7, ("B", "D"): 0.6, ("C", "D"): 0.6, ("D", "E"): 0.9}


def consistent(order, weights):
    pos = {v: k for k, v in enumerate(order)}
    return all(pos[a] < pos[b] for (a, b) in weights)


def random_model(rng, n, p):
    order = [chr(65 + i) for i in range(n)]
    rng.shuffle(order)
    w = {}
    for i, j in itertools.combinations(range(n), 2):
        if rng.random() < p:
            w[(order[i], order[j])] = rng.uniform(0.5, 1.5) * rng.choice((1, -1))
    return order, w


def test_worked_example():
    rng = random.Random(1)
    data = simulate(EX_ORDER, EX_WEIGHTS, 1000, rng, uniform_noise)
    data = {v: data[v] for v in ["E", "C", "A", "D", "B"]}
    res = direct_lingam(data)
    assert res.order == ["A", "C", "B", "D", "E"]
    assert set(res.b) == set(EX_WEIGHTS)
    assert all(abs(res.b[k] - w) < 0.05 for k, w in EX_WEIGHTS.items())


def test_two_point_noise_exact():
    # x = e1, y = x + e2 with e1, e2 independent and equal to -1 or 1.
    # Forward residual e2 is independent of x. The backward regression of x
    # on y has slope 1/2; its residual is uncorrelated with y but dependent.
    outcomes = [(e1, e2) for e1 in (-1, 1) for e2 in (-1, 1)]  # each with probability 1/4
    p = Fraction(1, 4)
    xs = [(e1, e1 + e2) for e1, e2 in outcomes]
    slope = sum(p * x * y for x, y in xs) / sum(p * y * y for x, y in xs)
    assert slope == Fraction(1, 2)
    pairs = [(x - slope * y, y) for x, y in xs]
    assert sum(p * r * y for r, y in pairs) == 0  # uncorrelated

    def prob(event):
        return sum(p for pr in pairs if event(pr))

    joint = prob(lambda t: t[0] == 0 and t[1] == 0)
    assert joint == 0 and prob(lambda t: t[0] == 0) * prob(lambda t: t[1] == 0) == Fraction(1, 4)
    # Forward: residual y - x = e2 and x = e1 factorize exactly.
    for a in (-1, 1):
        for b in (-1, 1):
            j = sum(p for e1, e2 in outcomes if e1 == a and e2 == b)
            assert j == Fraction(1, 2) * Fraction(1, 2)


def test_gaussian_every_order_fits_exactly():
    # For a Gaussian model, every order of the variables gives a linear model with
    # uncorrelated (so independent) errors and the same covariance.
    nodes = ["A", "B", "C"]
    w = {("A", "B"): Fraction(4, 5), ("A", "C"): Fraction(-1, 2), ("B", "C"): Fraction(3, 4)}
    cov = covariance(nodes, w, {v: Fraction(1) for v in nodes})
    for order in itertools.permutations(nodes):
        b, var = {}, {}
        for t, y in enumerate(order):
            preds = list(order[:t])
            coef = solve_exact([[cov[p][q] for q in preds] for p in preds], [cov[p][y] for p in preds])
            for p, c in zip(preds, coef):
                b[(p, y)] = c
            var[y] = cov[y][y] - sum(c * cov[p][y] for p, c in zip(preds, coef))
        assert covariance(list(order), b, var) == cov


def covariance(order, w, noise_var):
    cov = {u: {} for u in order}
    for i, v in enumerate(order):
        pas = [(p, x) for (p, c), x in w.items() if c == v]
        for u in order[:i]:
            cov[u][v] = cov[v][u] = sum((x * cov[p][u] for p, x in pas), Fraction(0))
        cov[v][v] = noise_var[v] + sum((x1 * x2 * cov[p1][p2] for p1, x1 in pas for p2, x2 in pas), Fraction(0))
    return cov


def solve_exact(a, rhs):
    k = len(rhs)
    m = [row[:] + [r] for row, r in zip(a, rhs)]
    for i in range(k):
        p = next(r for r in range(i, k) if m[r][i] != 0)
        m[i], m[p] = m[p], m[i]
        for r in range(i + 1, k):
            f = m[r][i] / m[i][i]
            for c in range(i, k + 1):
                m[r][c] -= f * m[i][c]
    out = [Fraction(0)] * k
    for i in reversed(range(k)):
        out[i] = (m[i][k] - sum(m[i][j] * out[j] for j in range(i + 1, k))) / m[i][i]
    return out


def test_residuals_of_a_source_follow_the_same_model():
    # Lemma: regress a source m out of every variable; the residuals satisfy
    # r_j = sum_{p != m} b_pj r_p + e_j. Checked exactly on coefficient vectors over e.
    rng = random.Random(2)
    for _ in range(30):
        order, wf = random_model(rng, 5, 0.6)
        w = {k: Fraction(round(v * 8), 8) or Fraction(1, 8) for k, v in wf.items()}
        coef = {}
        for v in order:
            vec = {v: Fraction(1)}
            for (p, c), x in w.items():
                if c == v:
                    for k, a in coef[p].items():
                        vec[k] = vec.get(k, 0) + x * a
            coef[v] = vec
        m = order[0]
        r = {}
        for j in order[1:]:
            cjm = coef[j].get(m, 0)  # Cov(x_j, x_m) / Var(x_m), unit noise variances
            r[j] = {k: a - cjm * coef[m].get(k, 0) for k, a in coef[j].items()}
            want = {j: Fraction(1)}
            for (p, c), x in w.items():
                if c == j and p != m:
                    for k, a in r[p].items():
                        want[k] = want.get(k, 0) + x * a
            assert {k: a for k, a in r[j].items() if a} == {k: a for k, a in want.items() if a}


def test_two_variables_uniform_noise():
    ok = 0
    for seed in range(50):
        rng = random.Random(seed)
        data = simulate(["X", "Y"], {("X", "Y"): 0.8}, 1000, rng, uniform_noise)
        ok += direct_lingam({"Y": data["Y"], "X": data["X"]}).order == ["X", "Y"]
    assert ok == 50


def test_two_variables_gaussian_noise():
    # With Gaussian noise the direction is not identified: about half right.
    ok = 0
    for seed in range(50):
        rng = random.Random(seed)
        data = simulate(["X", "Y"], {("X", "Y"): 0.8}, 1000, rng, gaussian_noise)
        ok += direct_lingam({"Y": data["Y"], "X": data["X"]}).order == ["X", "Y"]
    assert ok == 24  # measured: 24 of 50, close to a coin flip


def test_random_models_uniform_noise():
    order_ok = support_ok = 0
    for seed in range(50):
        rng = random.Random(seed)
        order, w = random_model(rng, 5, 0.5)
        data = simulate(order, w, 1000, rng, uniform_noise)
        res = direct_lingam({v: data[v] for v in sorted(data)})
        order_ok += consistent(res.order, w)
        support_ok += set(res.b) == set(w)
    assert order_ok == 50
    assert support_ok == 43


def test_random_models_gaussian_noise():
    order_ok = 0
    for seed in range(50):
        rng = random.Random(seed)
        order, w = random_model(rng, 5, 0.5)
        data = simulate(order, w, 1000, rng, gaussian_noise)
        res = direct_lingam({v: data[v] for v in sorted(data)})
        order_ok += consistent(res.order, w)
    assert order_ok == 3
