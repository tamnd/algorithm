# SPDX-License-Identifier: MIT
# Shared helper of the recommender system pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Small rating sets for the tests of the recommender system pages.

A rating set is a dict that maps a pair (user, item) to a float rating.
Users are 0 to m - 1 and items are 0 to n - 1. No real data is used:
the tests plant a low-rank matrix from a seeded random generator, hide
some of its entries, and measure the error on the hidden entries.
"""

import math
import random

# The toy matrix of the pages: four users (rows), four items (columns).
# None marks a missing rating.
TOY = [
    [5, 4, None, 1],
    [4, 5, 4, 2],
    [1, 2, 2, 5],
    [None, 1, 1, 4],
]


def from_rows(rows):
    """Turn a list of rows (None for a missing entry) into a rating set."""
    return {
        (u, i): float(v)
        for u, row in enumerate(rows)
        for i, v in enumerate(row)
        if v is not None
    }


def toy():
    """The toy matrix as a rating set."""
    return from_rows(TOY)


def planted(m, n, r, seed, mean=3.0, noise=0.0, rounded=False):
    """A full m by n rating set mean + P Q^T (+ noise) with rank r factors.

    The factor entries are Gaussian with variance 1 / sqrt(r), so each
    product p_u . q_i has variance 1. With rounded=True each rating is
    rounded to the nearest integer and clipped to the scale 1 to 5.
    """
    rng = random.Random(seed)
    s = r ** -0.25
    p = [[rng.gauss(0.0, s) for _ in range(r)] for _ in range(m)]
    q = [[rng.gauss(0.0, s) for _ in range(r)] for _ in range(n)]
    ratings = {}
    for u in range(m):
        for i in range(n):
            v = mean + sum(a * b for a, b in zip(p[u], q[i]))
            if noise:
                v += rng.gauss(0.0, noise)
            if rounded:
                v = float(min(5, max(1, round(v))))
            ratings[(u, i)] = v
    return ratings


def split(ratings, frac, seed):
    """Hide about frac of the entries; return (train, hidden).

    An entry is hidden only if its user and its item keep at least one
    training entry, so each user and each item stays in the training set.
    """
    rng = random.Random(seed)
    keys = sorted(ratings)
    rng.shuffle(keys)
    left_u, left_i = {}, {}
    for u, i in keys:
        left_u[u] = left_u.get(u, 0) + 1
        left_i[i] = left_i.get(i, 0) + 1
    target = int(frac * len(keys))
    hidden = {}
    for u, i in keys:
        if len(hidden) >= target:
            break
        if left_u[u] > 1 and left_i[i] > 1:
            hidden[(u, i)] = ratings[(u, i)]
            left_u[u] -= 1
            left_i[i] -= 1
    train = {k: v for k, v in ratings.items() if k not in hidden}
    return train, hidden


def rmse(predict, hidden):
    """Root mean square error of predict(u, i) on the hidden entries."""
    if not hidden:
        raise ValueError("no hidden entries")
    total = sum((predict(u, i) - v) ** 2 for (u, i), v in hidden.items())
    return math.sqrt(total / len(hidden))


def global_mean(ratings):
    """The mean of all ratings."""
    return sum(ratings.values()) / len(ratings)


def by_user(ratings):
    """A dict user -> {item: rating}."""
    out = {}
    for (u, i), v in ratings.items():
        out.setdefault(u, {})[i] = v
    return out


def by_item(ratings):
    """A dict item -> {user: rating}."""
    out = {}
    for (u, i), v in ratings.items():
        out.setdefault(i, {})[u] = v
    return out
