# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/svd-plus-plus/. The authors are listed in prov/87CAT3.jsonl.

"""SVD++ (Koren 2008), trained by SGD.

The prediction is

    mu + b_u + b_i + q_i . (p_u + |N(u)|^(-1/2) sum over j in N(u) of y_j)

where N(u) is the set of items with implicit feedback from user u (by
default the items that u rated in the training set). The objective puts
the penalties once on each rating:

    J = sum over (u, i) in K of [ e_ui^2 + lb (b_u^2 + b_i^2)
          + lf (|p_u|^2 + |q_i|^2 + sum over j in N(u) of |y_j|^2) ]

One SGD step on (u, i), with e = r_ui - prediction, z = p_u + |N(u)|^(-1/2) sum y_j
and the old values on the right side, is

    b_u <- b_u + g (e - lb b_u)          b_i <- b_i + g (e - lb b_i)
    q_i <- q_i + g (e z - lf q_i)        p_u <- p_u + g (e q_i - lf p_u)
    y_j <- y_j + g (e |N(u)|^(-1/2) q_i - lf y_j)   for each j in N(u)

This is theta - (g / 2) times the gradient of the term of (u, i) in J.
"""

import math
import random


class Model:
    def __init__(self, m, n, r, mu, implicit):
        self.m, self.n, self.r, self.mu = m, n, r, mu
        self.implicit = {u: sorted(set(js)) for u, js in implicit.items()}
        self.bu = [0.0] * m
        self.bi = [0.0] * n
        self.p = [[0.0] * r for _ in range(m)]
        self.q = [[0.0] * r for _ in range(n)]
        self.y = [[0.0] * r for _ in range(n)]

    def user_vector(self, u):
        """z_u = p_u + |N(u)|^(-1/2) times the sum of y_j over N(u)."""
        z = self.p[u][:]
        nu = self.implicit.get(u, [])
        if nu:
            s = 1.0 / math.sqrt(len(nu))
            for j in nu:
                yj = self.y[j]
                for f in range(self.r):
                    z[f] += s * yj[f]
        return z

    def predict(self, u, i):
        z = self.user_vector(u)
        return self.mu + self.bu[u] + self.bi[i] + sum(a * b for a, b in zip(self.q[i], z))  # @line L11


def implicit_from(train):
    """N(u) = the items that u rated in train."""
    out = {}
    for u, i in train:
        out.setdefault(u, []).append(i)
    return out


def init(m, n, r, train, seed, implicit=None, scale=0.1):
    rng = random.Random(seed)
    mu = sum(train.values()) / len(train)  # @line L1
    model = Model(m, n, r, mu, implicit_from(train) if implicit is None else implicit)
    model.p = [[rng.gauss(0.0, scale) for _ in range(r)] for _ in range(m)]
    model.q = [[rng.gauss(0.0, scale) for _ in range(r)] for _ in range(n)]
    model.y = [[rng.gauss(0.0, scale) for _ in range(r)] for _ in range(n)]
    return model


def objective(model, train, lb, lf):
    total = 0.0
    for (u, i), v in train.items():
        e = v - model.predict(u, i)
        reg_f = sum(a * a for a in model.p[u]) + sum(b * b for b in model.q[i])
        for j in model.implicit.get(u, []):
            reg_f += sum(c * c for c in model.y[j])
        total += e * e + lb * (model.bu[u] ** 2 + model.bi[i] ** 2) + lf * reg_f
    return total


def gradient(model, train, lb, lf):
    """The exact gradient of J: (d bu, d bi, d p, d q, d y)."""
    r = model.r
    gbu = [0.0] * model.m
    gbi = [0.0] * model.n
    gp = [[0.0] * r for _ in range(model.m)]
    gq = [[0.0] * r for _ in range(model.n)]
    gy = [[0.0] * r for _ in range(model.n)]
    for (u, i), v in train.items():
        z = model.user_vector(u)
        e = v - (model.mu + model.bu[u] + model.bi[i] + sum(a * b for a, b in zip(model.q[i], z)))
        gbu[u] += -2.0 * e + 2.0 * lb * model.bu[u]
        gbi[i] += -2.0 * e + 2.0 * lb * model.bi[i]
        nu = model.implicit.get(u, [])
        s = 1.0 / math.sqrt(len(nu)) if nu else 0.0
        for f in range(r):
            gq[i][f] += -2.0 * e * z[f] + 2.0 * lf * model.q[i][f]
            gp[u][f] += -2.0 * e * model.q[i][f] + 2.0 * lf * model.p[u][f]
            for j in nu:
                gy[j][f] += -2.0 * e * s * model.q[i][f] + 2.0 * lf * model.y[j][f]
    return gbu, gbi, gp, gq, gy


def sgd_step(model, u, i, v, lb, lf, gamma):
    z = model.user_vector(u)  # @line L4
    e = v - (model.mu + model.bu[u] + model.bi[i] + sum(a * b for a, b in zip(model.q[i], z)))  # @line L5
    model.bu[u] += gamma * (e - lb * model.bu[u])  # @line L6
    model.bi[i] += gamma * (e - lb * model.bi[i])
    nu = model.implicit.get(u, [])
    s = 1.0 / math.sqrt(len(nu)) if nu else 0.0
    qi_old = model.q[i][:]
    pu, qi = model.p[u], model.q[i]
    for f in range(model.r):
        qi[f] += gamma * (e * z[f] - lf * qi[f])  # @line L7
        pu[f] += gamma * (e * qi_old[f] - lf * pu[f])
    for j in nu:
        yj = model.y[j]
        for f in range(model.r):
            yj[f] += gamma * (e * s * qi_old[f] - lf * yj[f])  # @line L8


def sgd_epoch(model, train, lb, lf, gamma, order):
    for u, i in order:
        sgd_step(model, u, i, train[(u, i)], lb, lf, gamma)


def fit(train, m, n, r, lb=0.005, lf=0.015, gamma=0.007, epochs=30, seed=1, implicit=None, decay=0.9):
    """Train by SGD; the step size is multiplied by decay after each epoch."""
    rng = random.Random(seed)
    model = init(m, n, r, train, seed, implicit)
    keys = sorted(train)
    for _ in range(epochs):  # @line L2
        rng.shuffle(keys)  # @line L3
        sgd_epoch(model, train, lb, lf, gamma, keys)
        gamma *= decay  # @line L9
    return model  # @line L10
