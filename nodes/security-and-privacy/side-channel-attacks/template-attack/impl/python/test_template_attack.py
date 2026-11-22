# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/template-attack/. The authors are listed in prov/9Z5T63.jsonl.

import math
import random
import statistics

import pytest
from template_attack import (
    PRESENT_SBOX,
    attack_set,
    build_templates,
    cholesky,
    leakage_mean,
    profiling_set,
    quadratic_form,
    template_attack,
)


def det(a):
    if len(a) == 1:
        return a[0][0]
    return sum(
        (-1) ** c * a[0][c] * det([row[:c] + row[c + 1:] for row in a[1:]])
        for c in range(len(a))
    )


def inverse(a):
    """Inverse by cofactors, independent of the Cholesky code."""
    t = len(a)
    if t == 1:
        return [[1.0 / a[0][0]]]
    d = det(a)
    return [
        [
            (-1) ** (i + j) * det([row[:i] + row[i + 1:] for k, row in enumerate(a) if k != j]) / d
            for j in range(t)
        ]
        for i in range(t)
    ]


def random_spd(rng, t):
    b = [[rng.uniform(-1, 1) for _ in range(t)] for _ in range(t)]
    return [[sum(b[i][q] * b[j][q] for q in range(t)) + (0.5 if i == j else 0.0) for j in range(t)] for i in range(t)]


def oracle_scores(attack, means, covs):
    invs = [inverse(c) for c in covs]
    logdets = [math.log(det(c)) for c in covs]
    out = []
    for g in range(16):
        s = 0.0
        for p, tr in attack:
            v = PRESENT_SBOX[p ^ g]
            inv = invs[v]
            d = [tr[j] - means[v][j] for j in range(len(tr))]
            q = sum(d[i] * inv[i][j] * d[j] for i in range(len(d)) for j in range(len(d)))
            s += -0.5 * (q + logdets[v])
        out.append(s)
    return out


def exact_templates(sigma, rho):
    cov = [[sigma * sigma, rho * sigma * sigma], [rho * sigma * sigma, sigma * sigma]]
    low = cholesky(cov)
    logdet = math.log(det(cov))
    return [leakage_mean(v) for v in range(16)], [low] * 16, [logdet] * 16


def test_cholesky_and_quadratic_form() -> None:
    rng = random.Random(1)
    for _ in range(200):
        t = rng.randrange(1, 4)
        a = random_spd(rng, t)
        low = cholesky(a)
        for i in range(t):
            for j in range(t):
                assert sum(low[i][q] * low[j][q] for q in range(t)) == pytest.approx(a[i][j], abs=1e-9)
        x = [rng.uniform(-2, 2) for _ in range(t)]
        inv = inverse(a)
        want = sum(x[i] * inv[i][j] * x[j] for i in range(t) for j in range(t))
        assert quadratic_form(low, x) == pytest.approx(want, rel=1e-9, abs=1e-9)
    with pytest.raises(ValueError):
        cholesky([[1.0, 2.0], [2.0, 1.0]])


def test_worked_example() -> None:
    means, lows, _ = exact_templates(0.5, 0.8)
    tpl = (means, lows, [0.0] * 16)
    attack = [(0, [1.47, 1.96]), (5, [0.66, 0.84]), (9, [1.49, 0.32])]
    best, scores = template_attack(attack[:1], tpl)
    assert best == 0x6 and 1 + sum(s > scores[0xB] for s in scores) == 3
    best, scores = template_attack(attack, tpl)
    assert best == 0xB
    assert scores[0xB] == pytest.approx(-2.23, abs=0.005)
    assert sorted(scores, reverse=True)[1] == pytest.approx(-13.02, abs=0.005)


def test_against_oracle_random() -> None:
    rng = random.Random(20240504)
    for _ in range(500):
        t = rng.randrange(1, 4)
        means = [[rng.uniform(-2, 2) for _ in range(t)] for _ in range(16)]
        covs = [random_spd(rng, t) for _ in range(16)]
        lows = [cholesky(c) for c in covs]
        logdets = [2.0 * sum(math.log(low[i][i]) for i in range(t)) for low in lows]
        attack = [(rng.randrange(16), [rng.uniform(-3, 3) for _ in range(t)]) for _ in range(rng.randrange(1, 5))]
        best, scores = template_attack(attack, (means, lows, logdets))
        want = oracle_scores(attack, means, covs)
        assert scores == pytest.approx(want, rel=1e-9, abs=1e-9)
        assert want[best] == pytest.approx(max(want), abs=1e-9)


def test_build_templates_against_statistics() -> None:
    rng = random.Random(2)
    prof = profiling_set(rng, 400, 1.0, 0.8)
    means, lows, logdets = build_templates(prof)
    for v in range(16):
        rows = [tr for u, tr in prof if u == v]
        assert means[v] == pytest.approx([statistics.mean(r[j] for r in rows) for j in range(2)])
    resid = [[tr[j] - means[u][j] for j in range(2)] for u, tr in prof]
    dof = len(prof) - 16
    pooled = [[sum(r[a] * r[b] for r in resid) / dof for b in range(2)] for a in range(2)]
    low = lows[0]
    for a in range(2):
        for b in range(2):
            assert sum(low[a][q] * low[b][q] for q in range(2)) == pytest.approx(pooled[a][b])
    assert logdets[0] == pytest.approx(math.log(det(pooled)))
    with pytest.raises(ValueError):
        build_templates([(0, [1.0, 2.0]), (0, [1.5, 2.5])])


def test_low_noise_recovers_every_key() -> None:
    tpl = exact_templates(0.05, 0.8)
    rng = random.Random(3)
    for key in range(16):
        attack = attack_set(rng, key, 4, 0.05, 0.8)
        assert template_attack(attack, tpl)[0] == key


def test_ignoring_the_covariance_costs_success() -> None:
    # The maximum likelihood rule beats the rule that assumes independent noise.
    rng = random.Random(4)
    exact = exact_templates(1.0, 0.8)
    ident = ([leakage_mean(v) for v in range(16)], [cholesky([[1.0, 0.0], [0.0, 1.0]])] * 16, [0.0] * 16)
    runs = 300
    he = hi = 0
    for _ in range(runs):
        key = rng.randrange(16)
        attack = attack_set(rng, key, 5, 1.0, 0.8)
        he += template_attack(attack, exact)[0] == key
        hi += template_attack(attack, ident)[0] == key
    assert he / runs > 0.75
    assert he - hi >= 0.05 * runs


def test_estimated_templates() -> None:
    rng = random.Random(5)
    hits_pooled = hits_class = 0
    runs = 20
    for _ in range(runs):
        prof = profiling_set(rng, 1600, 1.0, 0.8)
        key = rng.randrange(16)
        attack = attack_set(rng, key, 12, 1.0, 0.8)
        hits_pooled += template_attack(attack, build_templates(prof))[0] == key
        hits_class += template_attack(attack, build_templates(prof, pooled=False))[0] == key
    assert hits_pooled >= runs - 2
    assert hits_class >= runs - 3


def test_edges() -> None:
    with pytest.raises(ValueError):
        template_attack([], exact_templates(1.0, 0.0))
