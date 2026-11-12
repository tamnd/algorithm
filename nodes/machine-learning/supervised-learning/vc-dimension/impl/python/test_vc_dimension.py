# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vc-dimension/. The authors are listed in prov/08SW3R.jsonl.

import random
from itertools import combinations, product
from math import floor, log2

from vc_dimension import (
    finite_class, halfspace_realizable, homogeneous_halfspace_realizable,
    interval_realizable, is_shattered, rectangle_realizable, sine_label, sine_points,
    sine_realizable, sine_theta_over_pi, vc_dimension_on,
)


def test_intervals_have_vc_dimension_two():
    domain = [0, 1, 2, 3, 4, 5]
    assert vc_dimension_on(domain, interval_realizable) == 2
    assert not interval_realizable([0, 1, 2], (1, 0, 1))


def test_rectangles_have_vc_dimension_four():
    diamond = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    assert is_shattered(diamond, rectangle_realizable)
    grid = [(x, y) for x in range(-1, 2) for y in range(-1, 2)] + [(2, 0), (0, 2), (2, 2)]
    assert vc_dimension_on(grid, rectangle_realizable) == 4
    assert not any(is_shattered(list(c), rectangle_realizable) for c in combinations(grid, 5))


def test_halfspaces_with_bias_have_vc_dimension_d_plus_one():
    line = [(0,), (1,), (2,), (3,)]
    assert vc_dimension_on(line, halfspace_realizable) == 2
    plane = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 1), (1, 3)]
    assert vc_dimension_on(plane, halfspace_realizable) == 3
    assert not halfspace_realizable([(0, 0), (1, 1), (1, 0), (0, 1)], (1, 1, 0, 0))
    space = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1), (2, 1, 0), (1, 2, 3)]
    assert vc_dimension_on(space, halfspace_realizable) == 4


def test_homogeneous_halfspaces_have_vc_dimension_d():
    plane = [(1, 0), (0, 1), (1, 1), (2, 1), (-1, 2), (3, -1)]
    assert vc_dimension_on(plane, homogeneous_halfspace_realizable) == 2


def test_finite_classes_have_vc_dimension_at_most_log2_size():
    rng = random.Random(7)
    n = 6
    for _ in range(40):
        size = rng.randint(1, 20)
        hyps = {tuple(rng.randint(0, 1) for _ in range(n)) for _ in range(size)}
        vc = vc_dimension_on(list(range(n)), finite_class(list(hyps)))
        assert vc <= floor(log2(len(hyps)))
    k = 3
    full = [tuple(list(lab) + [0] * (n - k)) for lab in product((0, 1), repeat=k)]
    assert vc_dimension_on(list(range(n)), finite_class(full)) == k


def test_sine_class_shatters_every_finite_prefix():
    for k in range(1, 7):
        pts = sine_points(k)
        assert is_shattered(pts, sine_realizable)
    labels = (1, 0, 0, 1)
    t = sine_theta_over_pi(labels)
    assert t == 1 + 100 + 1000
    assert [sine_label(t, x) for x in sine_points(4)] == list(labels)
