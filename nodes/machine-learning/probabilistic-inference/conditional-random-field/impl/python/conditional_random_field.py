# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conditional-random-field/. The authors are listed in prov/1TRP6G.jsonl.

"""A linear chain conditional random field with k labels and binary observation features.

An input x is a list of positions; each position is a list of active feature indices in 0 .. F-1.
The parameters are a dict:
  S[b]     the weight of label b at the first position
  T[a][b]  the weight of the transition a -> b
  W[b][f]  the weight of feature f with label b
score(x, y) = S[y_1] + sum_t sum_{f in x_t} W[y_t][f] + sum_{t >= 2} T[y_{t-1}][y_t]
and P(y | x) = exp(score(x, y)) / Z(x).
"""

import itertools
import math
import random


def zeros(k, nfeat):
    return {"S": [0.0] * k, "T": [[0.0] * k for _ in range(k)], "W": [[0.0] * nfeat for _ in range(k)]}


def random_params(k, nfeat, rng: random.Random, scale=1.0):
    return {"S": [rng.gauss(0, scale) for _ in range(k)],
            "T": [[rng.gauss(0, scale) for _ in range(k)] for _ in range(k)],
            "W": [[rng.gauss(0, scale) for _ in range(nfeat)] for _ in range(k)]}


def logsumexp(vals):
    m = max(vals)
    if m == -math.inf:
        return m
    return m + math.log(sum(math.exp(v - m) for v in vals))


def emissions(theta, x):
    k = len(theta["S"])
    return [[sum(theta["W"][b][f] for f in xt) for b in range(k)] for xt in x]


def score(theta, x, y):
    e = emissions(theta, x)
    s = theta["S"][y[0]] + sum(e[t][y[t]] for t in range(len(x)))
    return s + sum(theta["T"][y[t - 1]][y[t]] for t in range(1, len(x)))


def forward(theta, x):
    """log alpha_t(b) for each position t and label b, and log Z."""
    k = len(theta["S"])
    e = emissions(theta, x)
    alpha = [[theta["S"][b] + e[0][b] for b in range(k)]]
    for t in range(1, len(x)):
        alpha.append([e[t][b] + logsumexp([alpha[t - 1][a] + theta["T"][a][b] for a in range(k)])
                      for b in range(k)])
    return alpha, logsumexp(alpha[-1])


def backward(theta, x):
    k = len(theta["S"])
    e = emissions(theta, x)
    n = len(x)
    beta = [[0.0] * k for _ in range(n)]
    for t in range(n - 2, -1, -1):
        beta[t] = [logsumexp([theta["T"][a][b] + e[t + 1][b] + beta[t + 1][b] for b in range(k)])
                   for a in range(k)]
    return beta


def log_likelihood_and_gradient(theta, x, y):
    """log P(y | x) and its gradient: the observed feature counts minus their expectations."""
    k = len(theta["S"])
    n = len(x)
    e = emissions(theta, x)  # @line L1
    alpha, logz = forward(theta, x)  # @line L2
    beta = backward(theta, x)  # @line L3
    g = zeros(k, len(theta["W"][0]))
    # observed counts
    g["S"][y[0]] += 1.0
    for t in range(n):
        for f in x[t]:
            g["W"][y[t]][f] += 1.0
        if t > 0:
            g["T"][y[t - 1]][y[t]] += 1.0
    # expected counts from the marginals
    for t in range(n):
        for b in range(k):
            mu = math.exp(alpha[t][b] + beta[t][b] - logz)  # @line L4
            if t == 0:
                g["S"][b] -= mu
            for f in x[t]:
                g["W"][b][f] -= mu  # @line L5
        if t > 0:
            for a in range(k):
                for b in range(k):
                    xi = math.exp(alpha[t - 1][a] + theta["T"][a][b] + e[t][b] + beta[t][b] - logz)  # @line L4
                    g["T"][a][b] -= xi  # @line L5
    return score(theta, x, y) - logz, g  # @line L6


def marginals(theta, x):
    alpha, logz = forward(theta, x)
    beta = backward(theta, x)
    k = len(theta["S"])
    return [[math.exp(alpha[t][b] + beta[t][b] - logz) for b in range(k)] for t in range(len(x))]


def viterbi(theta, x):
    """The most probable label sequence and its score."""
    k = len(theta["S"])
    e = emissions(theta, x)
    delta = [theta["S"][b] + e[0][b] for b in range(k)]  # @line L7
    back = []
    for t in range(1, len(x)):  # @line L8
        ptr, nd = [], []
        for b in range(k):
            a = max(range(k), key=lambda a: delta[a] + theta["T"][a][b])  # @line L9
            ptr.append(a)
            nd.append(delta[a] + theta["T"][a][b] + e[t][b])
        back.append(ptr)
        delta = nd
    best = max(range(k), key=lambda b: delta[b])  # @line L10
    path = [best]
    for ptr in reversed(back):  # @line L11
        path.append(ptr[path[-1]])
    path.reverse()
    return path, delta[best]  # @line L12


def train(data, k, nfeat, steps=200, eta=0.1, l2=0.01):
    """Gradient ascent on the mean conditional log likelihood minus (l2 / 2) |theta|^2.
    Return the parameters and the objective after each step."""
    theta = zeros(k, nfeat)
    history = []
    for _ in range(steps):
        total = 0.0
        acc = zeros(k, nfeat)
        for x, y in data:
            ll, g = log_likelihood_and_gradient(theta, x, y)
            total += ll
            for b in range(k):
                acc["S"][b] += g["S"][b]
                for a in range(k):
                    acc["T"][b][a] += g["T"][b][a]
                for f in range(nfeat):
                    acc["W"][b][f] += g["W"][b][f]
        m = len(data)
        pen = sum(v * v for v in flat(theta))
        history.append(total / m - 0.5 * l2 * pen)
        for b in range(k):
            theta["S"][b] += eta * (acc["S"][b] / m - l2 * theta["S"][b])
            for a in range(k):
                theta["T"][b][a] += eta * (acc["T"][b][a] / m - l2 * theta["T"][b][a])
            for f in range(nfeat):
                theta["W"][b][f] += eta * (acc["W"][b][f] / m - l2 * theta["W"][b][f])
    return theta, history


def flat(theta):
    return theta["S"] + [v for row in theta["T"] for v in row] + [v for row in theta["W"] for v in row]


def brute_force(theta, x):
    """All label sequences with their scores; for tests on short inputs."""
    k = len(theta["S"])
    return {y: score(theta, x, list(y)) for y in itertools.product(range(k), repeat=len(x))}
