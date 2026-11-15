# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slope-one/. The authors are listed in prov/2RYX1J.jsonl.

import random
from fractions import Fraction

import recs
from slope_one import SlopeOne, fit

TOL = 1e-9


def closed_form(train, u, j, weighted=False):
    """The Slope One formulas computed from scratch, in exact arithmetic."""
    rows = recs.by_user(train)
    row = rows.get(u, {})
    num = den = Fraction(0)
    for i, r in row.items():
        if i == j:
            continue
        both = [w for w, rw in rows.items() if i in rw and j in rw]
        if not both:
            continue
        dev = sum(Fraction(rows[w][j]) - Fraction(rows[w][i]) for w in both) / len(both)
        c = len(both) if weighted else 1
        num += (dev + Fraction(r)) * c
        den += c
    if den == 0:
        return float(sum(row.values()) / len(row))
    return float(num / den)


def test_toy():
    model = fit(recs.toy())
    assert abs(model.dev(2, 3) - (-4 / 3)) < 1e-12
    # u1 rated items 1, 2, 4: (0.5 + 5) + (-1/3 + 4) + (-4/3 + 1) over 3.
    assert abs(model.predict(0, 2) - 53 / 18) < 1e-12
    # Weighted: counts 2, 3, 3.
    assert abs(model.predict(0, 2, weighted=True) - 2.625) < 1e-12


def test_matches_closed_form():
    for seed in range(6):
        full = recs.planted(9, 7, 2, seed, rounded=True)
        train, hidden = recs.split(full, 0.4, seed)
        model = fit(train)
        for u, j in hidden:
            for weighted in (False, True):
                assert abs(model.predict(u, j, weighted) - closed_form(train, u, j, weighted)) < TOL


def test_incremental_order_and_removal():
    rng = random.Random(4)
    full = recs.planted(8, 6, 2, 9, noise=0.3)
    train, hidden = recs.split(full, 0.3, 9)
    keys = list(train)
    rng.shuffle(keys)
    model = SlopeOne()
    for k in keys:
        model.add(k[0], k[1], train[k])
    for (u, i), v in hidden.items():  # add the hidden ratings, then take them out again
        model.add(u, i, v)
    for u, i in hidden:
        model.remove(u, i)
    first = keys[0]  # replace a rating, then restore it
    model.add(first[0], first[1], 1.0)
    model.add(first[0], first[1], train[first])
    batch = fit(train)
    assert set(model.count) == set(batch.count)
    for key in batch.count:
        assert model.count[key] == batch.count[key]
        assert abs(model.diff[key] - batch.diff[key]) < TOL
    for u, j in hidden:
        assert abs(model.predict(u, j, True) - batch.predict(u, j, True)) < TOL


def test_offset_is_least_squares_fit():
    rng = random.Random(2)
    v = [rng.uniform(1, 5) for _ in range(7)]
    w = [rng.uniform(1, 5) for _ in range(7)]
    b = sum(y - x for x, y in zip(v, w)) / len(v)

    def loss(c):
        return sum((x + c - y) ** 2 for x, y in zip(v, w))

    for d in (1e-3, 0.1, 1.0):
        assert loss(b) < loss(b + d) and loss(b) < loss(b - d)
    # The derivative 2 sum (v + b - w) is zero at b.
    assert abs(sum(x + b - y for x, y in zip(v, w))) < TOL


def test_fallback_to_means():
    model = fit({(0, 0): 4.0, (1, 1): 2.0})
    assert model.predict(0, 1) == 4.0
    assert model.predict(5, 1) == 3.0
