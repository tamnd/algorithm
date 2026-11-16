# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rootsift/. The authors are listed in prov/5CC4QY.jsonl.

import math
import random

import pytest

from rootsift import hellinger_kernel, nearest_by_rootsift, rootsift


def l2_normalized(x):
    n = math.sqrt(sum(t * t for t in x))
    return [t / n for t in x]


def test_worked_example():
    q, p1, p2 = (9.0, 16.0), (0.0, 25.0), (16.0, 9.0)
    assert rootsift(q) == pytest.approx([0.6, 0.8])
    assert hellinger_kernel(q, p1) == pytest.approx(0.8)
    assert hellinger_kernel(q, p2) == pytest.approx(0.96)
    assert math.dist(rootsift(q), rootsift(p1)) == pytest.approx(math.sqrt(0.4))
    assert math.dist(rootsift(q), rootsift(p2)) == pytest.approx(math.sqrt(0.08))
    # plain SIFT matching with L2 normalization picks p1, RootSIFT picks p2
    e1 = math.dist(l2_normalized(q), l2_normalized(p1))
    e2 = math.dist(l2_normalized(q), l2_normalized(p2))
    assert e1 == pytest.approx(0.5068, abs=1e-4) and e2 == pytest.approx(0.5393, abs=1e-4)
    assert nearest_by_rootsift(q, [p1, p2]) == 1


def test_identity_and_unit_norm_on_many_inputs():
    rng = random.Random(1)
    for _ in range(600):
        d = rng.randint(1, 16)
        x = [float(rng.randint(0, 20)) for _ in range(d)]
        y = [float(rng.randint(0, 20)) for _ in range(d)]
        x[rng.randrange(d)] += 1.0
        y[rng.randrange(d)] += 1.0
        rx, ry = rootsift(x), rootsift(y)
        assert sum(t * t for t in rx) == pytest.approx(1.0)
        h = hellinger_kernel(x, y)
        assert 0.0 <= h <= 1.0 + 1e-12
        assert math.dist(rx, ry) ** 2 == pytest.approx(2.0 - 2.0 * h, abs=1e-12)
        assert sum(a * b for a, b in zip(rx, ry)) == pytest.approx(h)


def test_nearest_neighbor_is_the_largest_hellinger_kernel():
    rng = random.Random(2)
    for _ in range(200):
        d = rng.randint(2, 8)
        db = [[rng.random() for _ in range(d)] for _ in range(rng.randint(1, 10))]
        q = [rng.random() for _ in range(d)]
        j = nearest_by_rootsift(q, db)
        assert hellinger_kernel(q, db[j]) == pytest.approx(max(hellinger_kernel(q, p) for p in db))


def test_scale_invariance_zero_vector_and_bad_input():
    x = [3.0, 0.0, 1.0, 12.0]
    assert rootsift([7.5 * t for t in x]) == pytest.approx(rootsift(x))
    assert rootsift([0.0, 0.0, 0.0]) == [0.0, 0.0, 0.0]
    assert rootsift([5.0]) == [1.0]
    with pytest.raises(ValueError):
        rootsift([1.0, -0.5])
