# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/condensation-algorithm/. The authors are listed in prov/SEFHQG.jsonl.

import math
import random

from condensation_algorithm import (
    Condensation,
    clutter_density,
    contour,
    draw_circle,
    features_on_normal,
    log_likelihood,
    nearest_feature_log_likelihood,
    select,
)

N = 60


def edge_map(*circles, clutter=()):
    e = [[False] * N for _ in range(N)]
    for u, v in clutter:
        e[v][u] = True
    for c in circles:
        draw_circle(e, c, 8)
    return e


def test_select_is_the_smallest_index_reaching_r():
    rng = random.Random(1)
    w = [rng.random() for _ in range(50)]
    c, acc = [], 0.0
    for t in w:
        acc += t
        c.append(acc)
    for _ in range(500):
        r = rng.random() * c[-1]
        j = select(c, r)
        assert c[j] >= r and (j == 0 or c[j - 1] < r)
    assert select(c, c[-1]) == 49 and select(c, 0.0) == 0


def test_selection_frequencies_follow_the_weights():
    rng = random.Random(2)
    c = [0.1, 0.3, 0.6, 1.0]
    counts = [0, 0, 0, 0]
    for _ in range(20000):
        counts[select(c, rng.random())] += 1
    for k, p in enumerate((0.1, 0.2, 0.3, 0.4)):
        assert abs(counts[k] / 20000 - p) < 0.012


def test_clutter_density_and_nearest_feature():
    c = 1 / (math.sqrt(2 * math.pi) * 1.0 * 0.05)
    assert clutter_density([], 1.0, 0.05) == 1.0
    assert abs(clutter_density([0], 1.0, 0.05) - (1 + c)) < 1e-12
    assert abs(clutter_density([0, 2], 1.0, 0.05) - (1 + c + c * math.exp(-2))) < 1e-12
    assert abs(nearest_feature_log_likelihood([0, 1, -3, None], 2.0, 2.0)
                - (-(0 + 1 + 4 + 4) / (2 * 2.0 * 4))) < 1e-12


def test_normals_find_the_circle():
    e = edge_map((30, 30))
    for p, n in contour((30, 30), 8, 16):
        assert 0 in features_on_normal(e, p, n, 3)
    for p, n in contour((30, 30), 5, 16):  # a smaller circle sees the edge 3 pixels out
        got = features_on_normal(e, p, n, 4)  # the drawn edge can be two pixels thick
        assert 3 in got and set(got) <= {2, 3, 4}


def test_no_features_give_likelihood_one_and_equal_weights():
    empty = edge_map()
    assert log_likelihood(empty, (30, 30), 8, 16, 6, 1.0, 0.05) == 0.0
    tracker = Condensation((30, 30), 8, n=50, seed=3)
    tracker.step(empty)
    assert max(tracker.weights) - min(tracker.weights) < 1e-15


def test_prediction_is_the_second_order_model():
    tracker = Condensation((30, 30), 8, n=20, noise=0.0, seed=4)
    tracker.samples = [((10.0, 10.0), (12.0, 11.0))] * 20
    assert math.dist(tracker.step(edge_map()), (14.0, 12.0)) < 1e-9
    assert math.dist(tracker.step(edge_map()), (16.0, 13.0)) < 1e-9


def test_likelihood_has_one_peak_per_circle():
    e = edge_map((20, 30), (42, 30))
    left = log_likelihood(e, (20, 30), 8, 16, 6, 1.0, 0.05)
    right = log_likelihood(e, (42, 30), 8, 16, 6, 1.0, 0.05)
    mid = log_likelihood(e, (31, 30), 8, 16, 6, 1.0, 0.05)
    assert abs(left - right) < 1e-9
    assert left > mid + 10


def test_tracks_through_clutter_and_a_short_occlusion():
    rng = random.Random(3)
    clutter = [(rng.randrange(N), rng.randrange(N)) for _ in range(144)]  # 4% of the pixels
    path = [(16 + 2 * t, 18 + 1.5 * t) for t in range(12)]
    hidden = {5, 6}
    tracker = Condensation(path[0], 8, seed=0)
    for k in range(1, len(path)):
        e = edge_map(clutter=clutter) if k in hidden else edge_map(path[k], clutter=clutter)
        est = tracker.step(e)
        err = math.dist(est, path[k])
        if k in hidden:
            assert err < 4.0
        elif k == 7:
            assert err < 2.5
        else:
            assert err < 1.0
