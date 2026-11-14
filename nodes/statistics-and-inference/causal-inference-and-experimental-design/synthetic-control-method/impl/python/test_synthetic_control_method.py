# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/synthetic-control-method/. The authors are listed in prov/1N66SX.jsonl.

import random
from fractions import Fraction as Fr

import pytest

from synthetic_control_method import (
    fw_gap,
    gaps,
    gradient,
    loss,
    placebo_pvalue,
    project_simplex,
    synth,
)


def fr_matrix(rows):
    return [[Fr(a) for a in r] for r in rows]


def test_worked_example():
    x1 = [Fr(7), Fr(4), Fr(4)]
    x0 = fr_matrix([[5, 7, 8], [5, 9, 6], [3, 0, 3]])  # rows are periods, columns donors
    r = synth(x1, x0)
    assert r.polished and r.w == [Fr(1, 2), 0, Fr(1, 2)] and r.loss == Fr(7, 2)
    assert gradient(x1, x0, r.w) == [4, 20, 4]
    assert gaps([Fr(10)], fr_matrix([[6, 8, 7]]), r.w) == [Fr(7, 2)]


def kkt_holds(x1, x0, w):
    g = gradient(x1, x0, w)
    nu = min(g)
    return (
        all(a >= 0 for a in w)
        and sum(w) == 1
        and all(g[j] == nu for j in range(len(w)) if w[j] > 0)
        and all(g[j] >= nu for j in range(len(w)))
    )


def test_kkt_conditions_hold_exactly():
    rng = random.Random(1)
    polished = 0
    for _ in range(60):
        k, jn = rng.randint(2, 8), rng.randint(2, 7)
        x1 = [Fr(rng.randint(-10, 10)) for _ in range(k)]
        x0 = [[Fr(rng.randint(-10, 10)) for _ in range(jn)] for _ in range(k)]
        r = synth(x1, x0)
        if r.polished:
            polished += 1
            assert kkt_holds(x1, x0, r.w)
            assert fw_gap(gradient(x1, x0, r.w), r.w) == 0
    assert polished >= 55


def test_three_donors_against_a_simplex_grid():
    """No point of the grid {(a, b, c) / 120} has a smaller loss, and the grid minimum is close."""
    rng = random.Random(2)
    m = 120
    grid = [(a / m, b / m, (m - a - b) / m) for a in range(m + 1) for b in range(m + 1 - a)]
    for _ in range(12):
        k = rng.randint(3, 6)
        x1 = [rng.uniform(0, 10) for _ in range(k)]
        x0 = [[rng.uniform(0, 10) for _ in range(3)] for _ in range(k)]
        r = synth(x1, x0)
        best = min(loss(x1, x0, w) for w in grid)
        assert r.loss <= best + 1e-9
        g = gradient(x1, x0, r.w)
        # f(grid point) - f(w*) <= g.(q - w*) + L |q - w*|^2 / 2 with |q - w*| <= 1/m from the nearest grid point
        lip = 2 * sum(a * a for row in x0 for a in row)
        assert best - r.loss <= max(abs(a) for a in g) * 2 / m + lip / m**2


def test_gap_bounds_the_suboptimality_exactly():
    rng = random.Random(3)
    for _ in range(30):
        k, jn = rng.randint(2, 6), rng.randint(2, 6)
        x1 = [Fr(rng.randint(-5, 5)) for _ in range(k)]
        x0 = [[Fr(rng.randint(-5, 5)) for _ in range(jn)] for _ in range(k)]
        r = synth(x1, x0)
        if not r.polished:
            continue
        for _ in range(10):
            raw = [Fr(rng.randint(0, 9)) for _ in range(jn)]
            if sum(raw) == 0:
                continue
            w = [a / sum(raw) for a in raw]
            assert loss(x1, x0, w) - r.loss <= fw_gap(gradient(x1, x0, w), w)


def test_projection_onto_the_simplex():
    rng = random.Random(4)
    for _ in range(100):
        n = rng.randint(1, 6)
        v = [Fr(rng.randint(-20, 20), rng.randint(1, 5)) for _ in range(n)]
        p = project_simplex(v)
        assert sum(p) == 1 and all(a >= 0 for a in p)
        d = sum((a - b) ** 2 for a, b in zip(v, p))
        for _ in range(20):
            raw = [Fr(rng.randint(0, 9)) for _ in range(n)]
            if sum(raw) == 0:
                continue
            q = [a / sum(raw) for a in raw]
            assert sum((a - b) ** 2 for a, b in zip(v, q)) >= d


def test_placebo_pvalue():
    """Factor model: unit u has loading l_u on a common trend. The treated unit gets an effect of
    5 after the intervention: it ranks first, p = 1/(J+1). Without the effect, the units are
    exchangeable and p is uniform on {1, ..., J+1}/(J+1): over 40 samples the share with p <= 0.25
    is within 0.25 +- 4 SE."""
    rng = random.Random(2026)

    def panel(effect):
        units, t_pre, t_post = 8, 10, 4
        load = [rng.uniform(0.5, 1.5) for _ in range(units)]
        trend = [rng.gauss(0, 1) for _ in range(t_pre + t_post)]
        y = [[load[u] * trend[t] + rng.gauss(0, 0.3) for u in range(units)] for t in range(t_pre + t_post)]
        for t in range(t_pre, t_pre + t_post):
            y[t][0] += effect
        return y[:t_pre], y[t_pre:]

    p, ratios = placebo_pvalue(*panel(5.0))
    assert p == 1 / 8 and ratios[0] == max(ratios)
    small = 0
    for _ in range(40):
        p, _ = placebo_pvalue(*panel(0.0))
        small += p <= 0.25
    se = (0.25 * 0.75 / 40) ** 0.5
    assert abs(small / 40 - 0.25) < 4 * se


def test_input_checks():
    with pytest.raises(ValueError):
        synth([1, 2], [[1, 2], [3]])
    with pytest.raises(ValueError):
        synth([1, 2, 3], [[1, 2], [3, 4]])
