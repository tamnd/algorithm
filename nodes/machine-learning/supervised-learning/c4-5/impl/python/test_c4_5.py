# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/c4-5/. The authors are listed in prov/MDWZEM.jsonl.

import random
from math import comb, log2

from c4_5 import (c45, class_probs, estimated_errors, eval_categorical, eval_numeric,
                  predict, prune, upper_limit)

# The golf data of Quinlan (1993), Chapter 1: outlook, temperature, humidity, windy.
GOLF = """sunny 75 70 true Play
sunny 80 90 true Dont
sunny 85 85 false Dont
sunny 72 95 false Dont
sunny 69 70 false Play
overcast 72 90 true Play
overcast 83 78 false Play
overcast 64 65 true Play
overcast 81 75 false Play
rain 71 80 true Dont
rain 65 70 true Dont
rain 75 80 false Play
rain 68 80 false Play
rain 70 96 false Play"""
ROWS = [r.split() for r in GOLF.splitlines()]
X = [(r[0], int(r[1]), int(r[2]), r[3]) for r in ROWS]
Y = [r[4] for r in ROWS]
KINDS = ["cat", "num", "num", "cat"]


def leaves(t):
    if t.is_leaf():
        return [t]
    return [l for c in t.branches.values() for l in leaves(c)]


def count_internal(t):
    return 0 if t.is_leaf() else 1 + sum(count_internal(c) for c in t.branches.values())


def test_golf_tree():
    t = c45(X, Y, KINDS)
    assert t.attr == 0
    sunny, rain, overcast = t.branches["sunny"], t.branches["rain"], t.branches["overcast"]
    assert (sunny.attr, sunny.theta) == (2, 75)  # humidity <= 75, a value of the training set
    assert rain.attr == 3 and overcast.is_leaf() and overcast.label == "Play"
    assert all(predict(t, x) == y for x, y in zip(X, Y))


def test_missing_value_example():
    # Quinlan (1993), Chapter 3: the outlook of case 6 is unknown.
    X2 = list(X)
    X2[5] = (None,) + X[5][1:]
    cases = [(x, y, 1.0) for x, y in zip(X2, Y)]
    g, s, _ = eval_categorical(cases, 0, 2)
    assert abs(g - 13 / 14 * (0.961 - 0.747)) < 1e-3 and abs(g - 0.199) < 1e-3
    assert abs(s - 1.809) < 1e-3
    t = c45(X2, Y, KINDS)
    hi = t.branches["sunny"].branches[False]
    assert abs(hi.dist["Dont"] - 3) < 1e-12 and abs(hi.dist["Play"] - 5 / 13) < 1e-12
    assert abs(t.branches["overcast"].dist["Play"] - (3 + 3 / 13)) < 1e-12
    pr = class_probs(t, ("sunny", 75, None, "false"))
    assert abs(pr["Play"] - (2 + 5 / 13) / (5 + 5 / 13)) < 1e-12
    assert predict(t, ("sunny", 75, None, "false")) == "Dont"


def test_upper_limit():
    assert abs(upper_limit(0, 6) - 0.206) < 5e-4
    assert abs(upper_limit(0, 9) - 0.143) < 5e-4
    assert upper_limit(0, 1) == 0.75
    assert abs(upper_limit(1, 16) - 0.1596) < 1e-4  # the book prints 0.157 from its approximation
    rng = random.Random(25)
    for _ in range(200):
        n = rng.randint(1, 40)
        e = rng.randint(0, n - 1)
        cf = rng.choice([0.1, 0.25, 0.5])
        u = upper_limit(e, n, cf)
        tail = sum(comb(n, i) * u ** i * (1 - u) ** (n - i) for i in range(e + 1))
        assert abs(tail - cf) < 1e-9
        assert upper_limit(e + 0.5, n, cf) > u - 1e-12  # increasing in E


def test_pruning_book_example():
    # Subtree leaves of 6, 9 and 1 cases with no errors, against one leaf of 16 cases with 1 error.
    Xp = [("a",)] * 6 + [("b",)] * 9 + [("c",)]
    Yp = ["d"] * 15 + ["r"]
    grown = c45(Xp, Yp, ["cat"], pruning=False)
    assert grown.attr == 0
    cases = [(x, y, 1.0) for x, y in zip(Xp, Yp)]
    assert abs(estimated_errors(grown, cases) - 3.273) < 1e-3
    t = c45(Xp, Yp, ["cat"])
    assert t.is_leaf() and t.label == "d"
    assert abs(estimated_errors(t, cases) - 16 * 0.1596) < 2e-3


def ref_scores(cases, side):
    """Gain and split info from the definitions; side(x) is the outcome or None."""
    def h(ws):
        tot = sum(ws.values())
        return -sum(v / tot * log2(v / tot) for v in ws.values() if v > 0)
    W = sum(w for _, _, w in cases)
    known = [(x, y, w) for x, y, w in cases if side(x) is not None]
    WK = sum(w for _, _, w in known)
    outs = sorted({side(x) for x, _, _ in known}, key=str)
    def dist(cs):
        d = {}
        for _, y, w in cs:
            d[y] = d.get(y, 0) + w
        return d
    rem = 0.0
    sizes = []
    for o in outs:
        cs = [c for c in known if side(c[0]) == o]
        wo = sum(w for _, _, w in cs)
        sizes.append(wo)
        rem += wo / WK * h(dist(cs))
    sizes.append(W - WK)
    gain = WK / W * (h(dist(known)) - rem)
    split = -sum(s / W * log2(s / W) for s in sizes if s > 0)
    return gain, split, sizes[:-1]


def test_root_selection_against_brute_force():
    rng = random.Random(1993)
    for trial in range(300):
        n = rng.randint(4, 14)
        kinds = [rng.choice(["cat", "num"]) for _ in range(3)]
        Xr = []
        for _ in range(n):
            row = tuple((rng.choice("pqr") if k == "cat" else rng.randint(0, 5)) if rng.random() > 0.15 else None
                        for k in kinds)
            Xr.append(row)
        yr = [rng.choice("+-") for _ in range(n)]
        wr = [rng.choice([1.0, 0.5, 2.0]) for _ in range(n)]
        cases = list(zip(Xr, yr, wr))
        cand = []
        for a, k in enumerate(kinds):
            if k == "cat":
                g, s, sizes = ref_scores(cases, lambda x: x[a]) if any(x[a] is not None for x in Xr) else (0, 0, [])
                if sum(1 for z in sizes if z >= 2 - 1e-9) >= 2:
                    cand.append((a, g, s))
            else:
                best = None
                for t in sorted({x[a] for x in Xr if x[a] is not None})[:-1]:
                    g, s, sizes = ref_scores(cases, lambda x: None if x[a] is None else x[a] <= t)
                    if min(sizes) >= 2 - 1e-9 and (best is None or g > best[1] + 1e-9):
                        best = (a, g, s)
                if best:
                    cand.append(best)
        tree = c45(Xr, yr, kinds, wr, pruning=False)
        labels = {y for y, w in zip(yr, wr)}
        if not cand or len(labels) == 1 or sum(wr) < 4:
            continue
        avg = sum(c[1] for c in cand) / len(cand)
        ok = [c for c in cand if c[1] >= avg - 1e-9 and c[2] > 1e-9]
        top = max((c[1] / c[2] for c in ok), default=None)
        if top is None or max(c[1] for c in ok if abs(c[1] / c[2] - top) < 1e-9) <= 1e-9:
            assert tree.is_leaf()
            continue
        assert not tree.is_leaf()
        chosen = [c for c in ok if c[0] == tree.attr]
        assert chosen and abs(chosen[0][1] / chosen[0][2] - top) < 1e-7


def check_weights(t, cases):
    """The case weights that reach the children add up to the weight at the node."""
    tot = sum(t.dist.values())
    assert abs(tot - sum(w for _, _, w in cases)) < 1e-9
    if t.is_leaf():
        return
    assert abs(sum(t.probs.values()) - 1) < 1e-9
    for o, c in t.branches.items():
        sub = []
        for x, y, w in cases:
            v = x[t.attr]
            out = None if v is None else (v <= t.theta if t.theta is not None else v)
            if out is None:
                sub.append((x, y, w * t.probs[o]))
            elif out == o:
                sub.append((x, y, w))
        check_weights(c, sub)


def test_fractional_cases_and_pruning():
    rng = random.Random(7)
    for trial in range(100):
        n = rng.randint(10, 40)
        Xr = [(rng.choice("abc") if rng.random() > 0.2 else None,
               rng.randint(0, 9) if rng.random() > 0.2 else None) for _ in range(n)]
        yr = [("+" if (x[0] == "a" or (x[1] or 0) > 6) else "-") if rng.random() < 0.85 else rng.choice("+-")
              for x in Xr]
        cases = [(x, y, 1.0) for x, y in zip(Xr, yr)]
        grown = c45(Xr, yr, ["cat", "num"], pruning=False)
        check_weights(grown, cases)
        before = estimated_errors(grown, cases)
        n_leaves = len(leaves(grown))
        internal = count_internal(grown)
        # Subtree replacement only: the estimate grows by at most 0.1 per internal node.
        t1, e1 = prune(c45(Xr, yr, ["cat", "num"], pruning=False), cases, raising=False)
        assert abs(e1 - estimated_errors(t1, cases)) < 1e-9
        assert e1 <= before + 0.1 * internal + 1e-9
        assert len(leaves(t1)) <= n_leaves
        # With subtree raising: the returned value is the estimate of the returned tree.
        t2, e2 = prune(c45(Xr, yr, ["cat", "num"], pruning=False), cases)
        assert abs(e2 - estimated_errors(t2, cases)) < 1e-9
        assert len(leaves(t2)) <= n_leaves
        for x in Xr:
            for t in (t1, t2):
                pr = class_probs(t, x)
                assert abs(sum(pr.values()) - 1) < 1e-9


def test_numeric_threshold_is_a_training_value():
    # Mitchell (1997), Section 3.7.2: temperature 40 48 60 72 80 90, PlayTennis No No Yes Yes Yes No.
    cases = [((t,), c, 1.0) for t, c in zip([40, 48, 60, 72, 80, 90], "NNYYYN")]
    vals = [40, 48, 60, 72, 80, 90]
    g, _, theta = eval_numeric(cases, 0, 1, vals)
    assert theta == 48  # midpoint 54, and 48 is the largest value not above it
    g2, _, theta2 = eval_numeric(cases, 0, 2, vals)
    assert theta2 == 48  # the cut at 85 leaves one case on the right
