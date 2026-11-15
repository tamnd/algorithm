# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayesian-personalized-ranking/. The authors are listed in prov/JYHKHX.jsonl.

"""Bayesian personalized ranking with a matrix factorization model (BPR-MF).

Rendle, Freudenthaler, Gantner and Schmidt-Thieme (UAI 2009). The data is a
set of positive (user, item) pairs. A training triple (u, i, j) has i a
positive item of u and j an item that u has not used. The model scores
x_ui = w_u . h_i and x_uij = x_ui - x_uj. BPR-Opt is

    sum over triples of ln sigma(x_uij) - (regularization),

and LearnBPR does stochastic gradient ascent on it with triples drawn
uniformly with replacement. This module minimizes the negative of the
per-triple term,

    loss(u, i, j) = -ln sigma(x_uij)
                    + (lam_u |w_u|^2 + lam_i |h_i|^2 + lam_j |h_j|^2) / 2,

so a step moves against the gradient. The factor 1/2 on the penalty only
rescales the constants.
"""

import math
import random

Matrix = list[list[float]]


def sigmoid(z: float) -> float:
    """The logistic function, computed without overflow."""
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def log_sigmoid(z: float) -> float:
    """ln sigma(z) = -ln(1 + e^(-z)), computed without overflow."""
    if z >= 0:
        return -math.log1p(math.exp(-z))
    return z - math.log1p(math.exp(z))


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def triple_loss(w: Matrix, h: Matrix, u: int, i: int, j: int, regs: tuple[float, float, float]) -> float:
    """loss(u, i, j) as in the module docstring. Cost O(r)."""
    lu, li, lj = regs
    x = dot(w[u], h[i]) - dot(w[u], h[j])
    pen = lu * dot(w[u], w[u]) + li * dot(h[i], h[i]) + lj * dot(h[j], h[j])
    return -log_sigmoid(x) + 0.5 * pen


def triple_grad(
    w: Matrix, h: Matrix, u: int, i: int, j: int, regs: tuple[float, float, float]
) -> tuple[list[float], list[float], list[float]]:
    """Gradients of loss(u, i, j) with respect to w_u, h_i and h_j.

    Precondition: i != j. With e = sigma(-x_uij), d(-ln sigma(x))/dx = -e,
    and dx/dw_u = h_i - h_j, dx/dh_i = w_u, dx/dh_j = -w_u. Cost O(r).
    """
    lu, li, lj = regs
    wu, hi, hj = w[u], h[i], h[j]
    x = dot(wu, hi) - dot(wu, hj)
    e = sigmoid(-x)
    gw = [-e * (a - b) + lu * c for a, b, c in zip(hi, hj, wu)]
    gi = [-e * a + li * b for a, b in zip(wu, hi)]
    gj = [e * a + lj * b for a, b in zip(wu, hj)]
    return gw, gi, gj


def by_user(pairs: set[tuple[int, int]], m: int) -> list[set[int]]:
    """The set I_u^+ of positive items of each user."""
    pos: list[set[int]] = [set() for _ in range(m)]
    for u, i in pairs:
        pos[u].add(i)
    return pos


def learn_bpr(
    pairs: set[tuple[int, int]],
    m: int,
    n: int,
    r: int,
    steps: int,
    rate: float,
    regs: tuple[float, float, float],
    seed: int = 1,
) -> tuple[Matrix, Matrix]:
    """LearnBPR with bootstrap sampling of triples.

    A draw takes a positive pair (u, i) uniformly and an item j uniformly,
    and starts again when u has used j. The accepted triple is uniform on
    D_S. Precondition: every user with a positive pair has at least one item
    it has not used. Cost O(r) per step, so O(steps r) in total, plus
    O((m + n) r) to start, if the expected number of draws per step is O(1),
    which holds when the users use a small part of the catalog.
    """
    rng = random.Random(seed)
    w = [[rng.gauss(0.0, 0.1) for _ in range(r)] for _ in range(m)]  # @line L1
    h = [[rng.gauss(0.0, 0.1) for _ in range(r)] for _ in range(n)]
    pos = by_user(pairs, m)
    plist = sorted(pairs)
    for u in range(m):
        if pos[u] and len(pos[u]) == n:
            raise ValueError("a user has used every item, so no triple exists")
    for _ in range(steps):  # @line L2
        while True:
            u, i = plist[rng.randrange(len(plist))]  # @line L3
            j = rng.randrange(n)  # @line L4
            if j not in pos[u]:
                break
        gw, gi, gj = triple_grad(w, h, u, i, j, regs)  # @line L5
        for f in range(r):  # @line L6
            w[u][f] -= rate * gw[f]
            h[i][f] -= rate * gi[f]
            h[j][f] -= rate * gj[f]
    return w, h  # @line L7


def auc(
    w: Matrix, h: Matrix, train: set[tuple[int, int]], test: set[tuple[int, int]], m: int, n: int
) -> float:
    """The mean over users of the fraction of correctly ordered pairs (Rendle et al., Equation 2).

    For user u, the pairs are (i, j) with i a test item of u and j an item in
    neither the training nor the test set of u. Ties count one half.
    Users with no test item are skipped. Cost O(m n^2 r) at most.
    """
    tr, te = by_user(train, m), by_user(test, m)
    total, users = 0.0, 0
    for u in range(m):
        if not te[u]:
            continue
        others = [j for j in range(n) if j not in tr[u] and j not in te[u]]
        if not others:
            continue
        good = 0.0
        for i in te[u]:
            xi = dot(w[u], h[i])
            for j in others:
                xj = dot(w[u], h[j])
                good += 1.0 if xi > xj else 0.5 if xi == xj else 0.0
        total += good / (len(te[u]) * len(others))
        users += 1
    return total / users if users else 0.5


def rank(w: Matrix, h: Matrix, u: int, used: set[int], k: int) -> list[int]:
    """The k unused items with the highest score for user u. Cost O(n r + n log n)."""
    scored = sorted((-dot(w[u], h[i]), i) for i in range(len(h)) if i not in used)
    return [i for _, i in scored[:k]]
