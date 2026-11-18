# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blendshape-model/. The authors are listed in prov/ENWK12.jsonl.
"""Tests of the blendshape model in the delta form.

They check that zero weights give the neutral mesh, that a unit weight gives
its target, that the delta form equals the whole-face form, that the model
is affine in the weights, the interference check value of the page, and the
optional clamp.
"""

import random
from fractions import Fraction as F

from blendshape_model import deltas, evaluate, evaluate_whole


def rand_mesh(rng, n):
    return [tuple(F(rng.randint(-20, 20), 8) for _ in range(3)) for _ in range(n)]


def rig(seed=1, n=12, k=4):
    rng = random.Random(seed)
    b0 = rand_mesh(rng, n)
    targets = []
    for _ in range(k):
        bk = list(b0)
        for i in rng.sample(range(n), 5):
            bk[i] = tuple(x + F(rng.randint(-8, 8), 16) for x in b0[i])
        targets.append(bk)
    return rng, b0, targets


def test_zero_weights_give_the_neutral():
    _, b0, targets = rig()
    assert evaluate(b0, deltas(b0, targets), [0] * len(targets)) == b0


def test_unit_weight_gives_the_target():
    _, b0, targets = rig()
    ds = deltas(b0, targets)
    for k, bk in enumerate(targets):
        w = [0] * len(targets)
        w[k] = 1
        assert evaluate(b0, ds, w) == [tuple(p) for p in bk]


def test_delta_form_equals_whole_face_form():
    rng, b0, targets = rig(seed=2)
    ds = deltas(b0, targets)
    for _ in range(20):
        w = [F(rng.randint(-4, 12), 8) for _ in targets]
        assert evaluate(b0, ds, w) == evaluate_whole(b0, targets, w)


def test_affine_in_the_weights():
    rng, b0, targets = rig(seed=3)
    ds = deltas(b0, targets)
    w1 = [F(rng.randint(0, 8), 8) for _ in targets]
    w2 = [F(rng.randint(0, 8), 8) for _ in targets]
    t = F(3, 7)
    wt = [(1 - t) * a + t * b for a, b in zip(w1, w2)]
    v1, v2, vt = evaluate(b0, ds, w1), evaluate(b0, ds, w2), evaluate(b0, ds, wt)
    for p, q, r in zip(v1, v2, vt):
        assert tuple((1 - t) * x + t * y for x, y in zip(p, q)) == r


def test_sparse_deltas_skip_still_vertices():
    _, b0, targets = rig()
    for d in deltas(b0, targets):
        assert len(d) <= 5


def test_interference_check_value():
    b0 = [(F(1), F(0), F(0))]
    smile = [(F(6, 5), F(3, 10), F(0))]
    jaw = [(F(1), F(-1, 2), F(0))]
    ds = deltas(b0, [smile, jaw])
    assert evaluate(b0, ds, [1, 1]) == [(F(6, 5), F(-1, 5), F(0))]
    assert evaluate(b0, ds, [F(1, 2), F(1, 2)]) == [(F(11, 10), F(-1, 10), F(0))]


def test_clamp_option():
    b0 = [(0.0, 0.0, 0.0)]
    t1 = [(1.0, 0.0, 0.0)]
    ds = deltas(b0, [t1])
    assert evaluate(b0, ds, [1.5])[0][0] == 1.5
    assert evaluate(b0, ds, [1.5], clamp=True)[0][0] == 1.0
    assert evaluate(b0, ds, [-0.5], clamp=True)[0][0] == 0.0
