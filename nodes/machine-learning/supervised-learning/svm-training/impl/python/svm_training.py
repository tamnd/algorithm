# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/svm-training/. The authors are listed in prov/WT03MH.jsonl.

"""Two solvers for the linear SVM without a bias term, which are not SMO.

The problem is

    min_w  P(w) = 1/2 |w|^2 + C * sum_i max(0, 1 - y_i w.x_i)

with dual

    max_a  D(a) = sum_i a_i - 1/2 |sum_i a_i y_i x_i|^2,   0 <= a_i <= C.

There is no equality constraint because there is no bias; add a constant
feature to get a (regularized) bias, as LIBLINEAR does.

* dual_coordinate_descent: the dual coordinate descent method of Hsieh, Chang,
  Lin, Keerthi and Sundararajan (ICML 2008), with the projected gradient
  stopping rule and the optional shrinking of LIBLINEAR. It also solves the
  L2-loss (squared hinge) SVM.
* pegasos: the primal estimated sub-gradient solver of Shalev-Shwartz, Singer
  and Srebro (ICML 2007) for  lam/2 |w|^2 + 1/n sum_i hinge_i, which is the
  problem above with C = 1/(lam n), divided by C n.

Vectors are plain lists of floats.
"""

import math
import random


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def hinge(w, xs, ys):
    return [max(0.0, 1.0 - y * dot(w, x)) for x, y in zip(xs, ys)]


def primal_objective(w, xs, ys, c, loss="l1"):
    h = hinge(w, xs, ys)
    if loss == "l2":
        return 0.5 * dot(w, w) + c * sum(t * t for t in h)
    return 0.5 * dot(w, w) + c * sum(h)


def dual_objective(alpha, xs, ys, c, loss="l1"):
    d = len(xs[0])
    w = [0.0] * d
    for a, x, y in zip(alpha, xs, ys):
        for k in range(d):
            w[k] += a * y * x[k]
    extra = 0.0
    if loss == "l2":
        extra = sum(a * a for a in alpha) / (4.0 * c)
    return sum(alpha) - 0.5 * dot(w, w) - extra


def kkt_violation(w, alpha, xs, ys, c, loss="l1"):
    """Largest projected gradient of the dual, in absolute value.

    For the L1 loss this is the largest violation of the conditions
    a_i = 0 => y_i w.x_i >= 1, 0 < a_i < C => y_i w.x_i = 1 and
    a_i = C => y_i w.x_i <= 1. It is 0 exactly at the optimum.
    """
    dii = 1.0 / (2.0 * c) if loss == "l2" else 0.0
    upper = math.inf if loss == "l2" else c
    worst = 0.0
    for a, x, y in zip(alpha, xs, ys):
        g = y * dot(w, x) - 1.0 + dii * a
        if a <= 0.0:
            pg = min(g, 0.0)
        elif a >= upper:
            pg = max(g, 0.0)
        else:
            pg = g
        worst = max(worst, abs(pg))
    return worst


def dual_coordinate_descent(xs, ys, c, loss="l1", tol=1e-8, max_epochs=10000,
                            shrinking=True, seed=0, shuffle=True):
    """Dual coordinate descent for the linear SVM (Hsieh et al. 2008).

    Returns (w, alpha, epochs). Each step solves the one-variable dual
    subproblem in a_i exactly and keeps w = sum_i a_i y_i x_i up to date, so
    one step costs O(d). The run stops when the spread of the projected
    gradients over one pass is below tol.
    """
    n, d = len(xs), len(xs[0])
    if loss == "l2":
        upper, dii = math.inf, 1.0 / (2.0 * c)
    else:
        upper, dii = c, 0.0
    qii = [dot(x, x) + dii for x in xs]
    alpha = [0.0] * n
    w = [0.0] * d
    rng = random.Random(seed)
    active = list(range(n))
    pg_max_old, pg_min_old = math.inf, -math.inf
    epoch = 0
    while epoch < max_epochs:
        epoch += 1
        if shuffle:
            rng.shuffle(active)
        pg_max, pg_min = -math.inf, math.inf
        keep = []
        for i in active:
            x, y = xs[i], ys[i]
            g = y * dot(w, x) - 1.0 + dii * alpha[i]
            pg = 0.0
            if alpha[i] == 0.0:
                if shrinking and g > pg_max_old:
                    continue  # shrink: i will most likely stay at 0
                if g < 0.0:
                    pg = g
            elif alpha[i] == upper:
                if shrinking and g < pg_min_old:
                    continue  # shrink: i will most likely stay at C
                if g > 0.0:
                    pg = g
            else:
                pg = g
            keep.append(i)
            pg_max, pg_min = max(pg_max, pg), min(pg_min, pg)
            if pg != 0.0 and qii[i] > 0.0:
                old = alpha[i]
                alpha[i] = min(max(old - g / qii[i], 0.0), upper)
                delta = (alpha[i] - old) * y
                for k in range(d):
                    w[k] += delta * x[k]
        if not keep:
            pg_max, pg_min = 0.0, 0.0
        if pg_max - pg_min < tol:
            if len(keep) == n:
                break
            # Converged on the shrunken set: check again on all variables.
            active = list(range(n))
            pg_max_old, pg_min_old = math.inf, -math.inf
            continue
        active = keep
        pg_max_old = pg_max if pg_max > 0.0 else math.inf
        pg_min_old = pg_min if pg_min < 0.0 else -math.inf
    return w, alpha, epoch


def pegasos(xs, ys, lam, iters, k=1, project=True, seed=0):
    """Pegasos: stochastic sub-gradient descent on the primal SVM objective.

    Minimizes lam/2 |w|^2 + 1/n sum_i max(0, 1 - y_i w.x_i) with step size
    1/(lam t) on a random batch of k points per step, followed by the
    optional projection onto the ball of radius 1/sqrt(lam), which contains
    the optimum. Returns the last iterate.
    """
    n, d = len(xs), len(xs[0])
    rng = random.Random(seed)
    w = [0.0] * d
    radius = 1.0 / math.sqrt(lam)
    for t in range(1, iters + 1):
        batch = [rng.randrange(n) for _ in range(k)]
        eta = 1.0 / (lam * t)
        violators = [i for i in batch if ys[i] * dot(w, xs[i]) < 1.0]
        scale = 1.0 - eta * lam
        w = [scale * v for v in w]
        for i in violators:
            f = eta / k * ys[i]
            for j in range(d):
                w[j] += f * xs[i][j]
        if project:
            norm = math.sqrt(dot(w, w))
            if norm > radius:
                w = [v * radius / norm for v in w]
    return w


def pegasos_objective(w, xs, ys, lam):
    return 0.5 * lam * dot(w, w) + sum(hinge(w, xs, ys)) / len(xs)
