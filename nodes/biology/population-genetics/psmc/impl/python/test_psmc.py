# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/psmc/. The authors are listed in prov/H1EZ3X.jsonl.

import itertools
import math
import random

import pytest

from biostoch import chi2_sf
from psmc import (
    History,
    forward_backward,
    log_likelihood,
    model_matrices,
    psmc_fit,
    simulate_pair,
    time_breaks,
    to_real_units,
    transition_joint,
)

BREAKS = [0.0, 0.3, 0.8, 1.8, math.inf]
SIZES = [1.0, 0.4, 2.0, 1.0]


def test_time_breaks():
    t = time_breaks(5, 15.0)
    assert t[0] == 0.0 and t[-1] == math.inf and len(t) == 6
    assert t[4] == pytest.approx(15.0)
    assert all(a < b for a, b in zip(t, t[1:]))
    assert time_breaks(1, 3.0) == [0.0, math.inf]


def test_history_rates():
    h = History(BREAKS, SIZES)
    # Lambda at 1.0: 0.3 / 1 + 0.5 / 0.4 + 0.2 / 2.
    assert h.cum_rate(1.0) == pytest.approx(0.3 + 1.25 + 0.1)
    for y in (0.0, 0.2, 1.0, 1.7, 5.0):
        assert h.cum_rate(h.inverse_cum_rate(y)) == pytest.approx(y)
    pi = h.interval_probs()
    assert sum(pi) == pytest.approx(1.0)
    flat = History([0.0, 0.5, 1.0, math.inf], [1.0, 1.0, 1.0]).interval_probs()
    assert flat == pytest.approx([1 - math.exp(-0.5), math.exp(-0.5) - math.exp(-1.0), math.exp(-1.0)])


def test_transition_margins():
    h = History(BREAKS, SIZES)
    pi = h.interval_probs()
    for rho in (0.5, 0.1, 0.01):
        joint = transition_joint(h, rho)
        for k in range(4):
            assert sum(joint[k]) == pytest.approx(pi[k], abs=1e-6)
            # With a recombination probability 1 - exp(-rho t) per bin, pi is
            # kept only up to an error of order rho squared.
            col = sum(joint[j][k] for j in range(4))
            assert abs(col - pi[k]) <= 0.15 * rho * rho
    _, a, _ = model_matrices(BREAKS, SIZES, 0.1, 0.0)
    assert a == [[1.0 if k == l else 0.0 for l in range(4)] for k in range(4)]


def test_transition_against_simulation():
    rng = random.Random(2011)
    h = History(BREAKS, SIZES)
    rho, reps = 0.8, 20000
    joint = transition_joint(h, rho)
    counts = [[0] * 4 for _ in range(4)]
    for _ in range(reps):
        t = h.inverse_cum_rate(rng.expovariate(1.0))
        k = h.piece(t)
        if rng.random() < -math.expm1(-rho * t):
            u = rng.random() * t
            t = h.inverse_cum_rate(h.cum_rate(u) + rng.expovariate(1.0))
        counts[k][h.piece(t)] += 1
    obs = [counts[k][l] for k in range(4) for l in range(4)]
    exp = [reps * joint[k][l] for k in range(4) for l in range(4)]
    assert min(exp) > 5
    stat = sum((o - x) ** 2 / x for o, x in zip(obs, exp))
    assert chi2_sf(stat, 15) > 0.001


def test_emission():
    h = History(BREAKS, SIZES)
    pi, _, e = model_matrices(BREAKS, SIZES, 0.1, 0.3)
    # Compare with a direct Simpson integral of p(t) (1 - exp(-theta t)).
    k, m = 1, 2000
    lo, hi = BREAKS[k], BREAKS[k + 1]
    step = (hi - lo) / m
    total = 0.0
    for i in range(m + 1):
        t = lo + i * step
        w = 1 if i in (0, m) else (4 if i % 2 else 2)
        total += w * math.exp(-h.cum_rate(t)) / h.lam[k] * -math.expm1(-0.1 * t)
    assert e[k] == pytest.approx(total * step / 3 / pi[k], rel=1e-9)
    assert all(0 < x < 1 for x in e)
    assert e == sorted(e)


def brute_force_loglik(obs, pi, a, e):
    k_n = len(pi)
    total = 0.0
    for path in itertools.product(range(k_n), repeat=len(obs)):
        p = pi[path[0]]
        for i, s in enumerate(path):
            if i:
                p *= a[path[i - 1]][s]
            if obs[i] == 1:
                p *= e[s]
            elif obs[i] == 0:
                p *= 1 - e[s]
        total += p
    return math.log(total)


def test_forward_backward_against_enumeration():
    breaks = [0.0, 0.4, 1.2, math.inf]
    pi, a, e = model_matrices(breaks, [1.0, 0.5, 2.0], 0.4, 0.6)
    obs = [0, 1, None, 1, 0, 0]
    loglik, post, xi, het, hom, first = forward_backward(obs, pi, a, e)
    assert loglik == pytest.approx(brute_force_loglik(obs, pi, a, e), rel=1e-12)
    for g in post:
        assert sum(g) == pytest.approx(1.0)
    assert sum(map(sum, xi)) == pytest.approx(len(obs) - 1)
    assert sum(het) == pytest.approx(2.0) and sum(hom) == pytest.approx(3.0)
    # The posterior at bin 2 against enumeration with the state fixed.
    k_n = 3
    joint = []
    for s in range(k_n):
        tot = 0.0
        for path in itertools.product(range(k_n), repeat=len(obs)):
            if path[2] != s:
                continue
            p = pi[path[0]]
            for i, q in enumerate(path):
                if i:
                    p *= a[path[i - 1]][q]
                p *= e[q] if obs[i] == 1 else (1 - e[q] if obs[i] == 0 else 1.0)
            tot += p
        joint.append(tot)
    z = sum(joint)
    assert post[2] == pytest.approx([x / z for x in joint], rel=1e-10)


def test_em_never_decreases_and_moves_toward_the_truth():
    rng = random.Random(7)
    breaks = [0.0, 0.5, 1.5, math.inf]
    truth = [0.3, 1.0, 1.0]
    theta, rho = 0.2, 0.05
    _, obs = simulate_pair(rng, 3000, breaks, truth, theta, rho)
    lam, logliks = psmc_fit(obs, breaks, theta, rho, [1.0, 1.0, 1.0], iterations=2, steps=16)
    assert all(b >= a - 1e-9 for a, b in zip(logliks, logliks[1:]))
    assert logliks[-1] > logliks[0]
    # The recent size starts at 1.0 and the truth is 0.3.
    assert lam[0] < 1.0


def test_real_units():
    n0, years, sizes = to_real_units([0.0, 0.5, math.inf], [1.0, 2.0], 0.06, 1.25e-8, 100, 25)
    assert n0 == pytest.approx(12000.0)
    assert years[1] == pytest.approx(2 * 12000 * 0.5 * 25)
    assert sizes == pytest.approx([12000.0, 24000.0])


def test_bad_input():
    with pytest.raises(ValueError):
        History([0.0, 1.0], [1.0])
    with pytest.raises(ValueError):
        History([0.0, 1.0, math.inf], [1.0, -1.0])
    pi, a, e = model_matrices([0.0, math.inf], [1.0], 0.1, 0.1)
    assert a == [[1.0]]
    assert log_likelihood([None, None], pi, a, e) == pytest.approx(0.0)
