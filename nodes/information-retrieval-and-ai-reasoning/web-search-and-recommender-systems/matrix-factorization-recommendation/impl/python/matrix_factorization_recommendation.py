# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/matrix-factorization-recommendation/. The authors are listed in prov/99YS69.jsonl.

"""Matrix factorization for rating prediction, trained by SGD.

The model predicts r_ui by mu + b_u + b_i + p_u . q_i (biased=True) or
by p_u . q_i (biased=False, then mu, b_u and b_i stay 0). The objective
puts the penalty once on each rating:

    J = sum over (u, i) in K of [ e_ui^2 + lam (b_u^2 + b_i^2 + |p_u|^2 + |q_i|^2) ]

with e_ui = r_ui - prediction. One SGD step on the rating (u, i) is

    b_u <- b_u + g (e - lam b_u)        b_i <- b_i + g (e - lam b_i)
    p_u <- p_u + g (e q_i - lam p_u)    q_i <- q_i + g (e p_u - lam q_i)

with the old values on the right side. This is theta - (g / 2) times the
gradient of the term of (u, i) in J.
"""

import random


class Model:
    def __init__(self, m, n, r, mu=0.0, biased=True):
        self.m, self.n, self.r = m, n, r
        self.biased = biased
        self.mu = mu if biased else 0.0
        self.bu = [0.0] * m
        self.bi = [0.0] * n
        self.p = [[0.0] * r for _ in range(m)]
        self.q = [[0.0] * r for _ in range(n)]

    def predict(self, u, i):
        s = sum(a * b for a, b in zip(self.p[u], self.q[i]))
        if self.biased:
            s += self.mu + self.bu[u] + self.bi[i]
        return s  # @line L9

    def copy(self):
        c = Model(self.m, self.n, self.r, self.mu, self.biased)
        c.bu, c.bi = self.bu[:], self.bi[:]
        c.p = [row[:] for row in self.p]
        c.q = [row[:] for row in self.q]
        return c


def init(m, n, r, train, seed, scale=0.1, biased=True):
    """Small random factors, zero biases, mu = the mean of train."""
    rng = random.Random(seed)
    mu = sum(train.values()) / len(train)  # @line L1
    model = Model(m, n, r, mu, biased)
    model.p = [[rng.gauss(0.0, scale) for _ in range(r)] for _ in range(m)]  # @line L2
    model.q = [[rng.gauss(0.0, scale) for _ in range(r)] for _ in range(n)]
    return model


def objective(model, train, lam):
    """J with the penalty once per rating, as in the module docstring."""
    total = 0.0
    for (u, i), v in train.items():
        e = v - model.predict(u, i)
        reg = sum(a * a for a in model.p[u]) + sum(b * b for b in model.q[i])
        if model.biased:
            reg += model.bu[u] ** 2 + model.bi[i] ** 2
        total += e * e + lam * reg
    return total


def gradient(model, train, lam):
    """The exact gradient of J: (d bu, d bi, d p, d q)."""
    gbu = [0.0] * model.m
    gbi = [0.0] * model.n
    gp = [[0.0] * model.r for _ in range(model.m)]
    gq = [[0.0] * model.r for _ in range(model.n)]
    for (u, i), v in train.items():
        e = v - model.predict(u, i)
        if model.biased:
            gbu[u] += -2.0 * e + 2.0 * lam * model.bu[u]
            gbi[i] += -2.0 * e + 2.0 * lam * model.bi[i]
        for f in range(model.r):
            gp[u][f] += -2.0 * e * model.q[i][f] + 2.0 * lam * model.p[u][f]
            gq[i][f] += -2.0 * e * model.p[u][f] + 2.0 * lam * model.q[i][f]
    return gbu, gbi, gp, gq


def sgd_step(model, u, i, v, lam, gamma):
    """One SGD step on the rating r_ui = v, in place."""
    e = v - model.predict(u, i)  # @line L5
    if model.biased:
        model.bu[u] += gamma * (e - lam * model.bu[u])  # @line L6
        model.bi[i] += gamma * (e - lam * model.bi[i])
    pu, qi = model.p[u], model.q[i]
    for f in range(model.r):
        a, b = pu[f], qi[f]
        pu[f] = a + gamma * (e * b - lam * a)  # @line L7
        qi[f] = b + gamma * (e * a - lam * b)


def sgd_epoch(model, train, lam, gamma, order):
    """One pass of SGD over the keys of train in the given order."""
    for u, i in order:
        sgd_step(model, u, i, train[(u, i)], lam, gamma)


def fit(train, m, n, r, lam=0.05, gamma=0.01, epochs=50, seed=1, biased=True):
    """Train by SGD; each epoch visits the ratings in a new random order."""
    rng = random.Random(seed)
    model = init(m, n, r, train, seed, biased=biased)
    keys = sorted(train)
    for _ in range(epochs):  # @line L3
        rng.shuffle(keys)  # @line L4
        sgd_epoch(model, train, lam, gamma, keys)
    return model  # @line L8
