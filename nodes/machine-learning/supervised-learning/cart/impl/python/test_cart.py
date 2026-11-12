# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cart/. The authors are listed in prov/6A3KDC.jsonl.

import random
from fractions import Fraction

from cart import cart, find_surrogates, grow, number, predict, pruning_sequence, subtree


def gini(ys):
    n = len(ys)
    return 1 - sum(Fraction(ys.count(c), n) ** 2 for c in set(ys))


def sse(ys):
    m = Fraction(sum(ys), len(ys))
    return sum((Fraction(v) - m) ** 2 for v in ys)


def ref_tree(X, y, idx, task):
    """A naive builder from the definitions: try every feature and every midpoint."""
    ys = [y[i] for i in idx]
    if task == "classification":
        imp = lambda s: len(s) * gini(s)
        pure = len(set(ys)) == 1
    else:
        imp = sse
        pure = sse(ys) == 0
    if pure or len(idx) < 2:
        return "leaf"
    best = None
    for j in range(len(X[0])):
        vals = sorted(set(X[i][j] for i in idx))
        for a, b in zip(vals, vals[1:]):
            th = Fraction(a + b) / 2
            L = [y[i] for i in idx if X[i][j] <= th]
            R = [y[i] for i in idx if X[i][j] > th]
            dec = imp(ys) - imp(L) - imp(R)
            if best is None or dec > best[0]:
                best = (dec, j, th)
    if best is None:
        return "leaf"
    _, j, th = best
    return (j, th, ref_tree(X, y, [i for i in idx if X[i][j] <= th], task),
            ref_tree(X, y, [i for i in idx if X[i][j] > th], task))


def shape(t):
    return "leaf" if t.is_leaf() else (t.feature, t.threshold, shape(t.left), shape(t.right))


def test_grow_against_brute_force():
    rng = random.Random(1984)
    for trial in range(300):
        n, d = rng.randint(1, 10), rng.randint(1, 3)
        X = [tuple(rng.randint(0, 4) for _ in range(d)) for _ in range(n)]
        task = rng.choice(["classification", "regression"])
        y = [rng.choice("ab" if trial % 3 else "abc") for _ in range(n)] if task == "classification" \
            else [Fraction(rng.randint(-3, 3)) for _ in range(n)]
        t = grow(X, y, list(range(n)), task, n_min=2)
        assert shape(t) == ref_tree(X, y, list(range(n)), task)


def test_root_split_on_small_example():
    # x1 <= 2.5 separates the classes; the Gini decrease is 6 * (1/2) - 0 - 0 = 3.
    X = [(1, 5), (2, 3), (3, 6), (4, 1), (2, 2), (5, 4)]
    y = ["a", "a", "b", "b", "a", "b"]
    t = grow(X, y, list(range(6)), "classification", 2)
    assert (t.feature, t.threshold) == (0, Fraction(5, 2))
    assert t.left.is_leaf() and t.right.is_leaf()


def test_surrogates_against_brute_force():
    rng = random.Random(5)
    for trial in range(300):
        n, d = rng.randint(3, 10), 3
        X = [tuple(rng.randint(0, 3) for _ in range(d)) for _ in range(n)]
        idx = list(range(n))
        primary = rng.randrange(d)
        vals = sorted(set(x[primary] for x in X))
        if len(vals) < 2:
            continue
        theta = Fraction(vals[0] + vals[1]) / 2
        side = {i: X[i][primary] <= theta for i in idx}
        sur = {s[1]: s for s in find_surrogates(X, idx, primary, side)}
        n_left = sum(side.values())
        p_min = Fraction(min(n_left, n - n_left), n)
        for j in range(d):
            if j == primary:
                continue
            best = 0
            vj = sorted(set(x[j] for x in X))
            for a, b in zip(vj, vj[1:]):
                th = Fraction(a + b) / 2
                agree = sum(1 for i in idx if (X[i][j] <= th) == side[i])
                best = max(best, agree, n - agree)
            lam = (p_min - (1 - Fraction(best, n))) / p_min if len(vj) > 1 else None
            if lam is not None and lam > 0:
                assert sur[j][0] == lam
                _, _, th, le_left = sur[j]
                assert sum(1 for i in idx if ((X[i][j] <= th) == le_left) == side[i]) == best
            else:
                assert j not in sur


def test_missing_value_uses_surrogate():
    # Feature 1 is a copy of feature 0, so it is a perfect surrogate.
    X = [(1, 10, 0), (2, 20, 1), (3, 30, 0), (4, 40, 1), (5, 50, 0), (6, 60, 1)]
    y = ["a", "a", "a", "b", "b", "b"]
    t = grow(X, y, list(range(6)), "classification", 2)
    assert t.feature == 0 and t.surrogates[0][1] == 1 and t.surrogates[0][0] == 1
    assert predict(t, (None, 15, 1)) == "a"
    assert predict(t, (None, 55, 0)) == "b"
    assert predict(t, (None, None, 0)) in "ab"  # the majority side when every value is missing


def all_prunings(t):
    """Every pruned subtree of t as (R, number of leaves, set of internal node ids)."""
    if t.is_leaf():
        return [(t.risk, 1, frozenset())]
    out = [(t.risk, 1, frozenset())]
    for r1, k1, s1 in all_prunings(t.left):
        for r2, k2, s2 in all_prunings(t.right):
            out.append((r1 + r2, k1 + k2, s1 | s2 | {t.id}))
    return out


def internal_ids(t):
    return set() if t.is_leaf() else {t.id} | internal_ids(t.left) | internal_ids(t.right)


def test_pruning_sequence_against_all_prunings():
    rng = random.Random(1)
    for trial in range(150):
        n = rng.randint(4, 16)
        X = [(rng.randint(0, 6), rng.randint(0, 6)) for _ in range(n)]
        task = "classification" if trial % 2 else "regression"
        y = [rng.choice("ab") for _ in range(n)] if task == "classification" \
            else [Fraction(rng.randint(0, 5)) for _ in range(n)]
        root = grow(X, y, list(range(n)), task, 2, max_depth=3)
        seq = pruning_sequence(root)
        number(root)
        P = all_prunings(root)
        alphas = [a for a, _ in seq]
        assert alphas == sorted(alphas) and len(set(alphas)) == len(alphas)
        probes = alphas + [(a + b) / 2 for a, b in zip(alphas, alphas[1:])] + [alphas[-1] + 1]
        for al in probes:
            k = max(i for i, a in enumerate(alphas) if a <= al)
            tk = subtree(root, seq[k][1])
            kept = internal_ids(tk)
            cost = sum((tk_l.risk for tk_l in leaves_of(tk)), Fraction(0)) + al * len(leaves_of(tk))
            best = min(r + al * m for r, m, _ in P)
            assert cost == best
            minimizers = [s for r, m, s in P if r + al * m == best]
            assert all(kept <= s for s in minimizers)  # T(alpha) is the smallest minimizer
        assert internal_ids(subtree(root, seq[-1][1])) == set()


def leaves_of(t):
    return [t] if t.is_leaf() else leaves_of(t.left) + leaves_of(t.right)


def test_cross_validation_picks_from_the_sequence():
    rng = random.Random(2)
    X = [(rng.random(), rng.random()) for _ in range(150)]
    y = [("a" if x[0] < 0.5 else "b") if rng.random() < 0.7 else rng.choice("ab") for x in X]
    t, seq, cv = cart(X, y, folds=5, rng=random.Random(3))
    best = min(range(len(seq)), key=lambda k: (cv[k], -k))
    full = grow(X, y, list(range(150)), "classification", 2)
    assert shape(t) == shape(subtree(full, pruning_sequence(full)[best][1]))
    assert len(leaves_of(full)) == 30 and len(leaves_of(t)) == 2
    assert t.feature == 0 and abs(t.threshold - Fraction(1, 2)) < Fraction(1, 50)  # the true split


def test_regression_step():
    X = [(i,) for i in range(10)]
    y = [0, 0, 0, 0, 0, 10, 10, 10, 10, 10]
    t, seq, cv = cart(X, y, task="regression", folds=5)
    assert (t.feature, t.threshold) == (0, Fraction(9, 2))
    assert t.left.value == 0 and t.right.value == 10
