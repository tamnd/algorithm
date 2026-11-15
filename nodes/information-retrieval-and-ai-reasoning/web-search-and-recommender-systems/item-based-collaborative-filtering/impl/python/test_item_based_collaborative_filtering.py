# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/item-based-collaborative-filtering/. The authors are listed in prov/Z4THKH.jsonl.

import math

import recs
from item_based_collaborative_filtering import ItemBasedCF

TOL = 1e-9


def dense(train, m, n):
    return [[train.get((u, i)) for i in range(n)] for u in range(m)]


def brute(rows, u, i, k=None):
    """Adjusted cosine and the weighted sum, written out on a dense matrix."""
    m, n = len(rows), len(rows[0])

    def mean(a):
        vals = [x for x in rows[a] if x is not None]
        return sum(vals) / len(vals)

    def sim(a, b):
        co = [v for v in range(m) if rows[v][a] is not None and rows[v][b] is not None]
        x = [rows[v][a] - mean(v) for v in co]
        y = [rows[v][b] - mean(v) for v in co]
        # The same float expression as the module, so that exact ties
        # (frequent with integer ratings) stay ties in the top-k choice.
        sx = sum(t * t for t in x)
        sy = sum(t * t for t in y)
        if sx == 0 or sy == 0:
            return 0.0
        return sum(p * q for p, q in zip(x, y)) / math.sqrt(sx * sy)

    cand = sorted(((sim(i, j), j) for j in range(n) if j != i), key=lambda t: (-t[0], t[1]))
    cand = [t for t in cand if t[0] > 0]
    if k is not None:
        cand = cand[:k]
    used = [(s, j) for s, j in cand if rows[u][j] is not None]
    den = sum(s for s, _ in used)
    if den == 0:
        return mean(u)
    return sum(s * rows[u][j] for s, j in used) / den


def test_toy():
    train = recs.toy()
    model = ItemBasedCF(train)
    rows = dense(train, 4, 4)
    for u, i in [(0, 2), (3, 0)]:
        assert abs(model.predict(u, i) - brute(rows, u, i)) < TOL
    # Items 1 and 3 (indices 0 and 2) are rated by users 2 and 3 (indices 1 and 2).
    a = [4 - 3.75, 1 - 2.5]
    b = [4 - 3.75, 2 - 2.5]
    exact = (a[0] * b[0] + a[1] * b[1]) / math.sqrt((a[0] ** 2 + a[1] ** 2) * (b[0] ** 2 + b[1] ** 2))
    assert abs(model.similarity(0, 2) - exact) < 1e-12
    assert abs(model.predict(0, 2) - 4.540284512670781) < TOL


def test_matches_brute_force_on_planted_matrices():
    for seed in range(5):
        full = recs.planted(10, 8, 2, seed, rounded=True)
        train, hidden = recs.split(full, 0.3, seed)
        rows = dense(train, 10, 8)
        for k in (None, 1, 3):
            model = ItemBasedCF(train, k=k)
            for u, i in hidden:
                assert abs(model.predict(u, i) - brute(rows, u, i, k)) < TOL


def test_prediction_inside_range_of_used_ratings():
    full = recs.planted(12, 9, 3, 7, noise=0.4)
    train, hidden = recs.split(full, 0.3, 7)
    model = ItemBasedCF(train, k=4)
    for u, i in hidden:
        row = {j: v for (w, j), v in train.items() if w == u}
        used = [row[j] for _, j in model.model[i] if j in row]
        p = model.predict(u, i)
        if used:
            assert min(used) - TOL <= p <= max(used) + TOL


def test_model_size_and_symmetry():
    full = recs.planted(10, 8, 2, 3, noise=0.3)
    train, _ = recs.split(full, 0.2, 3)
    model = ItemBasedCF(train, k=2)
    for i in range(8):
        assert len(model.model[i]) <= 2
        for j in range(8):
            if i != j:
                assert model.similarity(i, j) == model.similarity(j, i)
                assert -1 - TOL <= model.similarity(i, j) <= 1 + TOL
