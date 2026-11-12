# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xgboost/. The authors are listed in prov/57E0E8.jsonl.

import math
import random

from xgboost import best_split, boost, goes_left, grad_hess, grow_tree, leaf_objective, leaf_weight, predict, split_gain, tree_predict

EX_X = [(1.0,), (2.0,), (None,), (3.0,), (4.0,), (None,)]
EX_Y = [-3.0, -1.0, 4.0, 1.0, 3.0, 2.0]


def min_leaf_objective(g: list[float], h: list[float], lam: float, gamma: float) -> tuple[float, float]:
    """Brute force: minimize sum g_i w + (sum h_i + lam) w^2 / 2 by ternary search on w."""
    obj = lambda w: sum(gi * w + 0.5 * hi * w * w for gi, hi in zip(g, h)) + 0.5 * lam * w * w + gamma
    lo, hi = -100.0, 100.0
    for _ in range(300):
        a, b = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        lo, hi = (lo, b) if obj(a) < obj(b) else (a, hi)
    return lo, obj(lo)


def random_node(rng: random.Random, n: int, d: int, kind: str):
    xs = [tuple(None if rng.random() < 0.25 else float(rng.randrange(6)) for _ in range(d)) for _ in range(n)]
    ys = [rng.gauss(0, 2) if kind == "squared" else float(rng.random() < 0.5) for _ in range(n)]
    preds = [rng.gauss(0, 1) for _ in range(n)]
    gh = [grad_hess(kind, y, p) for y, p in zip(ys, preds)]
    return xs, [a for a, _ in gh], [b for _, b in gh]


def test_leaf_weight_minimizes_the_regularized_objective() -> None:
    rng = random.Random(1)
    for _ in range(30):
        kind = rng.choice(("squared", "logistic"))
        _, g, h = random_node(rng, rng.randrange(1, 8), 1, kind)
        lam, gamma = rng.choice((0.0, 0.5, 1.0, 3.0)), rng.choice((0.0, 0.2))
        if kind == "logistic" and lam == 0.0:
            lam = 0.1
        w_bf, obj_bf = min_leaf_objective(g, h, lam, gamma)
        w = leaf_weight(sum(g), sum(h), lam)
        assert abs(w - w_bf) < 1e-6
        assert abs(leaf_objective(sum(g), sum(h), lam, gamma) - obj_bf) < 1e-9


def test_split_gain_and_choice_against_brute_force() -> None:
    rng = random.Random(2)
    for _ in range(60):
        kind = rng.choice(("squared", "logistic"))
        n = rng.randrange(2, 9)
        xs, g, h = random_node(rng, n, 2, kind)
        lam, gamma = rng.choice((0.5, 1.0, 2.0)), rng.choice((0.0, 0.1))
        ids = list(range(n))
        _, parent = min_leaf_objective(g, h, lam, gamma)
        best_bf = 0.0
        for f in range(2):
            vals = sorted(set(x[f] for x in xs if x[f] is not None))
            for thr in [vals[0] - 1.0] + vals if vals else []:
                for ml in (False, True):
                    left = [i for i in ids if goes_left(xs[i], f, thr, ml)]
                    right = [i for i in ids if i not in left]
                    if not left or not right:
                        continue
                    _, ol = min_leaf_objective([g[i] for i in left], [h[i] for i in left], lam, gamma)
                    _, orr = min_leaf_objective([g[i] for i in right], [h[i] for i in right], lam, gamma)
                    gain_bf = parent - ol - orr
                    gl, hl = sum(g[i] for i in left), sum(h[i] for i in left)
                    assert abs(split_gain(gl, hl, sum(g) - gl, sum(h) - hl, lam, gamma) - gain_bf) < 1e-7
                    best_bf = max(best_bf, gain_bf)
        sp = best_split(xs, g, h, ids, lam, gamma)
        if best_bf <= 1e-9:
            assert sp is None
        else:
            assert sp is not None and abs(sp[0] - best_bf) < 1e-7


def test_default_direction_follows_the_gradient() -> None:
    # Missing rows have large negative g (they want a large w), like the present rows with small x.
    xs = [(1.0,), (2.0,), (8.0,), (9.0,), (None,), (None,)]
    g = [-2.0, -2.0, 2.0, 2.0, -2.0, -2.0]
    h = [1.0] * 6
    gain, f, thr, ml = best_split(xs, g, h, list(range(6)), 1.0, 0.0)
    assert (f, thr, ml) == (0, 5.0, True)
    assert abs(gain - 0.5 * (64 / 5 + 16 / 3 - 16 / 7)) < 1e-12
    g2 = [-2.0, -2.0, 2.0, 2.0, 2.0, 2.0]
    _, _, _, ml2 = best_split(xs, g2, h, list(range(6)), 1.0, 0.0)
    assert ml2 is False


def test_gamma_prunes_and_lambda_zero_gives_mean_residual() -> None:
    xs = [(float(i),) for i in range(6)]
    ys = [0.0, 0.1, 0.0, 0.2, 0.1, 0.0]
    g = [0.0 - y for y in ys]
    assert best_split(xs, g, [1.0] * 6, list(range(6)), 1.0, 10.0) is None
    tree = grow_tree(xs, g, [1.0] * 6, 0, 0.0, 0.0)
    assert abs(tree_predict(tree, (0.0,)) - sum(ys) / 6) < 1e-12


def test_worked_example() -> None:
    g = [0.0 - y for y in EX_Y]
    h = [1.0] * 6
    gain, f, thr, ml = best_split(EX_X, g, h, list(range(6)), 1.0, 0.0)
    assert (f, thr, ml) == (0, 2.5, False)
    assert abs(gain - 0.5 * (16 / 3 + 100 / 5 - 36 / 7)) < 1e-12
    tree = grow_tree(EX_X, g, h, 1, 1.0, 0.0)
    assert abs(tree_predict(tree, (1.0,)) - (-4 / 3)) < 1e-12
    assert abs(tree_predict(tree, (None,)) - 2.0) < 1e-12


def test_boosting_reduces_squared_loss() -> None:
    rng = random.Random(5)
    xs = [(rng.uniform(0, 1), None if rng.random() < 0.2 else rng.uniform(0, 1)) for _ in range(60)]
    ys = [math.sin(5 * a) + (b or 0.0) for a, b in xs]
    prev = sum(y * y for y in ys)
    for t in range(1, 6):
        trees = boost(xs, ys, "squared", t, eta=0.3, max_depth=2, lam=1.0)
        cur = sum((y - predict(trees, x, 0.3)) ** 2 for x, y in zip(xs, ys))
        assert cur < prev
        prev = cur
