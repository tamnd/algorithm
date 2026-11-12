# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conditional-random-field/. The authors are listed in prov/1TRP6G.jsonl.

import math
import random

from conditional_random_field import (brute_force, flat, forward, log_likelihood_and_gradient,
                                      logsumexp, marginals, random_params, score, train, viterbi)


def random_input(rng, n, nfeat):
    return [rng.sample(range(nfeat), rng.randint(0, min(3, nfeat))) for _ in range(n)]


def example():
    # labels A = 0, B = 1; one feature per position
    theta = {"S": [0.0, 0.0], "T": [[1.0, 0.0], [0.0, 1.0]], "W": [[2.0, 0.0, 0.0], [0.0, 1.0, 2.0]]}
    return theta, [[0], [1], [2]]


def test_example_of_the_page():
    theta, x = example()
    _, logz = forward(theta, x)
    e = math.e
    assert abs(math.exp(logz) - (e ** 6 + 2 * e ** 5 + e ** 4 + e ** 3 + 2 * e ** 2 + e)) < 1e-9
    assert abs(math.exp(logz) - 792.4352) < 1e-4
    path, best = viterbi(theta, x)
    assert path == [0, 1, 1] and abs(best - 6.0) < 1e-12
    mu = marginals(theta, x)
    assert abs(mu[0][0] - 0.7906) < 1e-4 and abs(mu[1][1] - 0.7311) < 1e-4 and abs(mu[2][1] - 0.8930) < 1e-4
    assert abs(math.exp(score(theta, x, [0, 1, 1]) - logz) - 0.5091) < 1e-4


def test_partition_function_matches_enumeration():
    rng = random.Random(1)
    for _ in range(40):
        k, nfeat, n = rng.randint(1, 4), rng.randint(1, 5), rng.randint(1, 5)
        theta = random_params(k, nfeat, rng)
        x = random_input(rng, n, nfeat)
        _, logz = forward(theta, x)
        assert abs(logz - logsumexp(list(brute_force(theta, x).values()))) < 1e-9


def test_marginals_match_enumeration():
    rng = random.Random(2)
    for _ in range(30):
        k, nfeat, n = rng.randint(2, 3), rng.randint(1, 4), rng.randint(1, 5)
        theta = random_params(k, nfeat, rng)
        x = random_input(rng, n, nfeat)
        table = brute_force(theta, x)
        logz = logsumexp(list(table.values()))
        mu = marginals(theta, x)
        for t in range(n):
            for b in range(k):
                want = sum(math.exp(s - logz) for y, s in table.items() if y[t] == b)
                assert abs(mu[t][b] - want) < 1e-9
            assert abs(sum(mu[t]) - 1.0) < 1e-9


def test_gradient_matches_finite_differences():
    rng = random.Random(3)
    h = 1e-5
    for _ in range(15):
        k, nfeat, n = rng.randint(2, 3), rng.randint(1, 4), rng.randint(1, 5)
        theta = random_params(k, nfeat, rng)
        x = random_input(rng, n, nfeat)
        y = [rng.randrange(k) for _ in range(n)]
        ll, g = log_likelihood_and_gradient(theta, x, y)
        logz = logsumexp(list(brute_force(theta, x).values()))
        assert abs(ll - (score(theta, x, y) - logz)) < 1e-9
        for key in ("S", "T", "W"):
            rows = [theta[key]] if key == "S" else theta[key]
            grows = [g[key]] if key == "S" else g[key]
            for row, grow in zip(rows, grows):
                for j in range(len(row)):
                    old = row[j]
                    row[j] = old + h
                    up, _ = log_likelihood_and_gradient(theta, x, y)
                    row[j] = old - h
                    down, _ = log_likelihood_and_gradient(theta, x, y)
                    row[j] = old
                    assert abs((up - down) / (2 * h) - grow[j]) < 1e-6


def test_viterbi_matches_brute_force():
    rng = random.Random(4)
    for _ in range(60):
        k, nfeat, n = rng.randint(1, 4), rng.randint(1, 5), rng.randint(1, 6)
        theta = random_params(k, nfeat, rng)
        x = random_input(rng, n, nfeat)
        table = brute_force(theta, x)
        best = max(table.values())
        path, s = viterbi(theta, x)
        assert abs(s - best) < 1e-9 and abs(score(theta, x, path) - best) < 1e-9


def test_training_increases_the_objective_and_fits_the_data():
    # Hidden labels follow a sticky chain; each position shows a noisy copy of its label as a feature.
    rng = random.Random(5)
    data = []
    for _ in range(30):
        n = rng.randint(3, 7)
        y = [rng.randrange(2)]
        for _ in range(n - 1):
            y.append(y[-1] if rng.random() < 0.8 else 1 - y[-1])
        x = [[yt if rng.random() < 0.75 else 1 - yt] for yt in y]
        data.append((x, y))
    # The objective is concave, and with a small enough step plain gradient ascent never goes down.
    theta, hist = train(data, 2, 2, steps=300, eta=0.2, l2=0.01)
    for a, b in zip(hist, hist[1:]):
        assert b >= a - 1e-12
    assert hist[-1] > hist[0] + 0.5
    assert theta["T"][0][0] > theta["T"][0][1] and theta["W"][1][1] > theta["W"][1][0]
    assert all(math.isfinite(v) for v in flat(theta))
