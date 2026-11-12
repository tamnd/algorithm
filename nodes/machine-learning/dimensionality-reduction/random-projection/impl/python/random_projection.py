# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-projection/. The authors are listed in prov/R90KN4.jsonl.
"""Random projection of a data matrix: X (n x d, examples as rows) -> X R / sqrt(k).

The entries of the d x k matrix R are i.i.d. with mean 0 and variance 1:
"gaussian" N(0, 1), "rademacher" +-1 with probability 1/2 each, or
"achlioptas" sqrt(3) times +1, 0, -1 with probabilities 1/6, 2/3, 1/6.
"""

import math

DISTRIBUTIONS = ("gaussian", "rademacher", "achlioptas")


def draw_entry(kind, rng):
    if kind == "gaussian":
        return rng.gauss(0.0, 1.0)
    if kind == "rademacher":
        return 1.0 if rng.random() < 0.5 else -1.0
    if kind == "achlioptas":
        u = rng.random()
        if u < 1 / 6:
            return math.sqrt(3.0)
        if u < 2 / 6:
            return -math.sqrt(3.0)
        return 0.0
    raise ValueError("unknown distribution: " + kind)


def random_matrix(d, k, kind, rng):
    """A d x k matrix with i.i.d. entries of the named distribution."""
    return [[draw_entry(kind, rng) for _ in range(k)] for _ in range(d)]


def project_rows(x, r):
    """Return X R / sqrt(k) for a list of rows X."""
    k = len(r[0])
    c = 1.0 / math.sqrt(k)
    out = []
    for row in x:
        y = [0.0] * k
        for i, v in enumerate(row):
            if v:
                ri = r[i]
                for j in range(k):
                    y[j] += v * ri[j]
        out.append([c * t for t in y])
    return out


def fit_transform(x, k, kind, rng):
    """Draw R once, independent of the data, and project all rows with it."""
    r = random_matrix(len(x[0]), k, kind, rng)
    return project_rows(x, r), r


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def sq_dist(x, y):
    return sum((a - b) ** 2 for a, b in zip(x, y))
