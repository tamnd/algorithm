# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rankboost/. The authors are listed in prov/FQ86DQ.jsonl.

"""RankBoost with threshold weak rankers (Freund, Iyer, Schapire, Singer 2003).

A crucial pair (x0, x1) says that x1 must rank above x0. The distribution D
over the pairs starts uniform. In each round the weak ranker is
h(x) = 1 if x[f] > theta else 0, chosen to maximize |r| with

    r = sum over pairs of D(x0, x1) (h(x1) - h(x0)),

and its weight is alpha = (1/2) ln((1 + r) / (1 - r)). The update is

    D'(x0, x1) = D(x0, x1) exp(alpha (h(x0) - h(x1))) / Z.

The final ranker is H(x) = sum of alpha_t h_t(x). The ranking loss counts a
pair as an error if H(x0) >= H(x1), so ties are errors. Theorem 1 of the
paper gives rloss(H) <= prod Z_t. If |r| = 1 the weight would be infinite;
the code clips r to 1 - 1e-10 in absolute value.
"""

import math

CLIP = 1.0 - 1e-10


def crucial_pairs(queries):
    """(x0, x1) for every pair of one query with y(x1) > y(x0)."""
    out = []
    for xs, y in queries:
        for i in range(len(xs)):
            for j in range(len(xs)):
                if y[i] > y[j]:
                    out.append((xs[j], xs[i]))
    return out


def weak(f, theta):
    return lambda x: 1.0 if x[f] > theta else 0.0


def candidates(pts):
    """All (f, theta) with theta a midpoint of two consecutive distinct values of x[f]."""
    out = []
    for f in range(len(pts[0][0])):
        vals = sorted(set(x[f] for p in pts for x in p))
        out += [(f, (a + b) / 2.0) for a, b in zip(vals, vals[1:])]
    return out


def r_value(h, pts, dist):
    return sum(d * (h(x1) - h(x0)) for d, (x0, x1) in zip(dist, pts))


def best_weak_ranker(pts, dist):
    """The (f, theta, r) with the largest |r|; ties keep the first candidate."""
    best = None
    for f, theta in candidates(pts):
        r = r_value(weak(f, theta), pts, dist)
        if best is None or abs(r) > abs(best[2]) + 1e-15:
            best = (f, theta, r)
    return best


def alpha_of(r):
    r = max(-CLIP, min(CLIP, r))
    return 0.5 * math.log((1.0 + r) / (1.0 - r))


def fit(queries, rounds):
    """Returns the list of (alpha, f, theta) and the list of Z_t."""
    pts = crucial_pairs(queries)
    dist = [1.0 / len(pts)] * len(pts)                                 # @line L1
    model, zs = [], []
    for _ in range(rounds):                                            # @line L2
        f, theta, r = best_weak_ranker(pts, dist)                      # @line L3
        a = alpha_of(r)                                                # @line L4
        h = weak(f, theta)
        new = [d * math.exp(a * (h(x0) - h(x1))) for d, (x0, x1) in zip(dist, pts)]
        z = sum(new)                                                   # @line L5
        dist = [v / z for v in new]                                    # @line L6
        model.append((a, f, theta))
        zs.append(z)
    return model, zs                                                   # @line L7


def score(model, x):
    return sum(a * weak(f, theta)(x) for a, f, theta in model)


def ranking_loss(model, pts, dist=None):
    """sum of D(x0, x1) over the pairs with H(x0) >= H(x1); D is uniform by default."""
    dist = [1.0 / len(pts)] * len(pts) if dist is None else dist
    return sum(d for d, (x0, x1) in zip(dist, pts) if score(model, x0) >= score(model, x1))


def w_values(h, pts, dist):
    """W_b = sum of D over the pairs with h(x0) - h(x1) = b, for b = -1, 0, +1."""
    w = {-1: 0.0, 0: 0.0, 1: 0.0}
    for d, (x0, x1) in zip(dist, pts):
        w[int(h(x0) - h(x1))] += d
    return w


def method2_alpha(w):
    """The alpha that minimizes Z = W_-1 e^-alpha + W_0 + W_+1 e^alpha (Section 3.2)."""
    return 0.5 * math.log(w[-1] / w[1])


def method2_z(w):
    return w[0] + 2.0 * math.sqrt(w[-1] * w[1])
