# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gradient-clipping/. The authors are listed in prov/YBTGFW.jsonl.

import math
import random

from gradient_clipping import (clip_by_global_norm, clip_by_value, clip_each_tensor_by_norm,
                               global_norm, sgd_step)

EPS = 2.0 ** -52


def flat(gs):
    return [x for g in gs for x in g]


def cosine(a, b):
    dot = math.fsum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(math.fsum(x * x for x in a)) * math.sqrt(math.fsum(y * y for y in b)))


def test_worked_example():
    out, nu = clip_by_global_norm([[3.0, 4.0]], 1.0)
    assert nu == 5.0
    assert math.isclose(out[0][0], 0.6) and math.isclose(out[0][1], 0.8)
    assert clip_by_value([[3.0, 4.0]], 1.0) == [[1.0, 1.0]]
    # value clipping turns (10, 0.1) from 0.57 degrees to 5.71 degrees
    v = clip_by_value([[10.0, 0.1]], 1.0)[0]
    assert math.isclose(math.degrees(math.atan2(v[1], v[0])), 5.7106, abs_tol=1e-4)


def test_norm_clipping_keeps_direction_and_bounds_norm():
    rng = random.Random(31)
    for _ in range(300):
        gs = [[rng.gauss(0, rng.choice([0.1, 1, 100])) for _ in range(rng.randint(1, 6))]
              for _ in range(rng.randint(1, 4))]
        c = rng.choice([0.01, 0.5, 1.0, 10.0])
        out, nu = clip_by_global_norm(gs, c)
        assert math.isclose(nu, math.sqrt(math.fsum(x * x for x in flat(gs))), rel_tol=1e-14)
        new = global_norm(out)
        if nu > c:
            assert abs(new - c) <= 4 * EPS * c  # the norm is c, up to rounding
            assert cosine(flat(out), flat(gs)) > 1 - 1e-14
            # every entry is scaled by the same factor c / nu
            assert all(math.isclose(y, x * c / nu, rel_tol=1e-15, abs_tol=0) for x, y in
                       zip(flat(gs), flat(out)))
        else:
            assert out == [list(g) for g in gs]


def test_value_clipping_bounds_entries_but_turns_the_vector():
    rng = random.Random(32)
    turned = 0
    for _ in range(200):
        g = [rng.gauss(0, 3) for _ in range(5)]
        out = clip_by_value([g], 1.0)[0]
        assert all(-1.0 <= x <= 1.0 for x in out)
        if cosine(out, g) < 1 - 1e-6:
            turned += 1
    assert turned > 150
    # the norm after value clipping can exceed c: up to c * sqrt(n)
    assert math.isclose(global_norm(clip_by_value([[5.0] * 4], 1.0)), 2.0)


def test_global_versus_per_tensor():
    gs = [[30.0, 40.0], [0.3, 0.4]]
    glob, nu = clip_by_global_norm(gs, 1.0)
    each = clip_each_tensor_by_norm(gs, 1.0)
    assert math.isclose(nu, math.sqrt(2500.25))
    assert cosine(flat(glob), flat(gs)) > 1 - 1e-14
    # per-tensor clipping changes the overall direction: the norm ratio 100:1 becomes 2:1
    assert cosine(flat(each), flat(gs)) < 0.9
    assert each[1] == [0.3, 0.4]
    assert math.isclose(global_norm([each[0]]) / global_norm([each[1]]), 2.0)
    assert math.isclose(global_norm([glob[0]]) / global_norm([glob[1]]), 100.0)


def test_no_overflow_and_non_finite():
    out, nu = clip_by_global_norm([[1e200, 1e200]], 1.0)
    assert math.isclose(nu, math.sqrt(2) * 1e200)
    assert math.isclose(global_norm(out), 1.0)
    _, nu = clip_by_global_norm([[float("inf"), 1.0]], 1.0)
    assert nu == float("inf")
    out, nu = clip_by_global_norm([[1.0, float("nan")]], 1.0)
    assert math.isnan(nu) and out[0][0] == 1.0  # not finite: the caller skips the step
    assert global_norm([[0.0, 0.0]]) == 0.0


def test_cliff_step():
    # on a cliff with gradient 3^20, a plain step jumps by 3.5e8; a clipped step by eta * c
    g = [3.0 ** 20]
    assert sgd_step([0.0], g, 0.1)[0] == -0.1 * 3.0 ** 20
    assert math.isclose(sgd_step([0.0], g, 0.1, c=1.0)[0], -0.1)
