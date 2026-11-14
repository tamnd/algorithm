# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fine-gray-model/. The authors are listed in prov/YSYJCC.jsonl.

import math
import random
from fractions import Fraction

from fine_gray_model import (
    _left_limit, baseline, censoring_survival, fit, predict_cif, weighted_sums,
)


def random_data(rng, n, p, censor=0.3, ties=True):
    times = [rng.randint(1, 8) if ties else rng.random() for _ in range(n)]
    causes = [0 if rng.random() < censor else rng.randint(1, 2) for _ in range(n)]
    X = [[rng.choice([0, 1, 2]) if ties else rng.gauss(0, 1) for _ in range(p)] for _ in range(n)]
    return times, causes, X


def direct_terms(times, causes, X, beta, cause=1):
    """Weighted risk set sums by a fresh O(n) loop at every event time."""
    G = censoring_survival(times, causes)
    exact = all(b == 0 for b in beta)
    out = []
    for t in sorted(set(y for y, c in zip(times, causes) if c == cause)):
        S0 = 0
        for y, c, x in zip(times, causes, X):
            w = 1 if exact else math.exp(sum(a * b for a, b in zip(x, beta)))
            if y >= t:
                S0 += w
            elif c not in (0, cause):
                S0 += w * _left_limit(G, t) / _left_limit(G, y)
        out.append(S0)
    return out


def cox_direct(times, events, X):
    """Breslow-ties Cox fit by Newton with O(n^2) direct sums; infinite times never die."""
    p = len(X[0])
    beta = [0.0] * p
    for _ in range(100):
        U = [0.0] * p
        I = [[0.0] * p for _ in range(p)]
        for t, e, x in zip(times, events, X):
            if not e:
                continue
            S0, S1, S2 = 0.0, [0.0] * p, [[0.0] * p for _ in range(p)]
            for y, z in zip(times, X):
                if y >= t:
                    w = math.exp(sum(a * b for a, b in zip(z, beta)))
                    S0 += w
                    for a in range(p):
                        S1[a] += w * z[a]
                        for b in range(p):
                            S2[a][b] += w * z[a] * z[b]
            for a in range(p):
                U[a] += x[a] - S1[a] / S0
                for b in range(p):
                    I[a][b] += S2[a][b] / S0 - S1[a] * S1[b] / S0 ** 2
        if p == 1:
            step = [U[0] / I[0][0]]
        else:
            det = I[0][0] * I[1][1] - I[0][1] * I[1][0]
            step = [(I[1][1] * U[0] - I[0][1] * U[1]) / det, (I[0][0] * U[1] - I[1][0] * U[0]) / det]
        beta = [b + s for b, s in zip(beta, step)]
        if max(abs(s) for s in step) < 1e-13:
            break
    return beta


def aalen_johansen(times, causes, cause=1):
    out, S, F = [], Fraction(1), Fraction(0)
    for t in sorted(set(y for y, c in zip(times, causes) if c)):
        n_j = sum(1 for y in times if y >= t)
        d = sum(1 for y, c in zip(times, causes) if y == t and c)
        dk = sum(1 for y, c in zip(times, causes) if y == t and c == cause)
        F += S * Fraction(dk, n_j)
        S *= Fraction(n_j - d, n_j)
        out.append((t, F))
    return out


def test_risk_sums_match_direct_summation() -> None:
    rng = random.Random(1)
    for trial in range(30):
        times, causes, X = random_data(rng, rng.randint(2, 15), 2)
        if 1 not in causes:
            continue
        exact = weighted_sums(times, causes, X, [0, 0], exact=True)
        assert exact.risk_sums == direct_terms(times, causes, X, [0, 0])
        beta = [rng.uniform(-1, 1), rng.uniform(-1, 1)]
        got = weighted_sums(times, causes, X, beta)
        m = max(sum(a * b for a, b in zip(x, beta)) for x in X)
        for a, b in zip(got.risk_sums, direct_terms(times, causes, X, beta)):
            assert abs(a * math.exp(m) - float(b)) < 1e-10 * float(b)


def test_without_censoring_equals_cox_with_competing_times_at_infinity() -> None:
    rng = random.Random(2)
    for _ in range(10):
        n = rng.randint(15, 40)
        times, causes, X = random_data(rng, n, 2, censor=0.0, ties=False)
        if causes.count(1) < 3 or causes.count(2) < 1:
            continue
        r = fit(times, causes, X)
        assert r.converged
        t2 = [y if c == 1 else math.inf for y, c in zip(times, causes)]
        b = cox_direct(t2, [int(c == 1) for c in causes], X)
        assert max(abs(u - v) for u, v in zip(r.beta, b)) < 1e-8


def test_score_and_information_are_derivatives() -> None:
    rng = random.Random(3)
    times, causes, X = random_data(rng, 30, 2, ties=False)
    beta = [0.3, -0.4]
    s = weighted_sums(times, causes, X, beta)
    h = 1e-6
    for a in range(2):
        up = beta[:]
        up[a] += h
        dn = beta[:]
        dn[a] -= h
        su, sd = weighted_sums(times, causes, X, up), weighted_sums(times, causes, X, dn)
        assert abs((su.loglik - sd.loglik) / (2 * h) - s.score[a]) < 1e-6
        for b in range(2):
            assert abs(-(su.score[b] - sd.score[b]) / (2 * h) - s.information[a][b]) < 1e-5
    r = fit(times, causes, X)
    assert r.converged and max(abs(u) for u in weighted_sums(times, causes, X, r.beta).score) < 1e-9


def test_censoring_km_factorizes_the_risk_set() -> None:
    # n_j / n = S(t_j-) G(t_j-) exactly, where S is the all-cause Kaplan-Meier estimate.
    rng = random.Random(4)
    for _ in range(40):
        times, causes, _ = random_data(rng, rng.randint(1, 20), 1, censor=0.4)
        n = len(times)
        G = censoring_survival(times, causes)
        S = Fraction(1)
        for t in sorted(set(times)):
            n_t = sum(1 for y in times if y >= t)
            assert Fraction(n_t, n) == S * _left_limit(G, t)
            d = sum(1 for y, c in zip(times, causes) if y == t and c)
            S *= Fraction(n_t - d, n_t)


def test_weighted_product_limit_at_beta_zero_is_aalen_johansen() -> None:
    rng = random.Random(5)
    for _ in range(40):
        times, causes, X = random_data(rng, rng.randint(1, 20), 1, censor=0.35)
        if 1 not in causes:
            continue
        steps = baseline(times, causes, X, [0])
        aj = dict(aalen_johansen(times, causes))
        prod = Fraction(1)
        for t, jump, _ in steps:
            prod *= 1 - jump
            assert 1 - prod == aj[t]


def simulate(rng, n, b1, b2, p):
    """The design of Fine and Gray (1999): F_1(t | x) = 1 - (1 - p (1 - e^(-t)))^exp(x b1)."""
    times, causes, X = [], [], []
    for _ in range(n):
        x = rng.choice([0.0, 1.0])
        r1 = math.exp(b1 * x)
        u = rng.random()
        if u < 1 - (1 - p) ** r1:
            t = -math.log(1 - (1 - (1 - u) ** (1 / r1)) / p)
            c = 1
        else:
            t = rng.expovariate(math.exp(b2 * x))
            c = 2
        cens = rng.uniform(0, 3)
        if cens < t:
            t, c = cens, 0
        times.append(t)
        causes.append(c)
        X.append([x])
    return times, causes, X


def test_simulation_recovers_beta() -> None:
    rng = random.Random(6)
    b1, b2, p = 0.5, -0.5, 0.6
    est = []
    for _ in range(40):
        times, causes, X = simulate(rng, 200, b1, b2, p)
        est.append(fit(times, causes, X).beta[0])
    mean = sum(est) / len(est)
    sd = math.sqrt(sum((e - mean) ** 2 for e in est) / (len(est) - 1))
    assert abs(mean - b1) < 4 * sd / math.sqrt(len(est)) + 0.02
    # The predicted cumulative incidence at t = 1 for x = 1 against the truth.
    times, causes, X = simulate(rng, 2000, b1, b2, p)
    r = fit(times, causes, X)
    steps = baseline(times, causes, X, r.beta)
    true = 1 - (1 - p * (1 - math.exp(-1.0))) ** math.exp(b1)
    assert abs(predict_cif(steps, [1.0], r.beta, 1.0) - true) < 0.04
