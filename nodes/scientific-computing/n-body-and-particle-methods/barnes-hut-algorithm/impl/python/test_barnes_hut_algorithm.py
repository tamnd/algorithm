# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/barnes-hut-algorithm/. The authors are listed in prov/RQH8DT.jsonl.
import math
import random

import pytest

from barnes_hut_algorithm import barnes_hut, build_tree, leaves


def direct(m, x, eps=0.0, G=1.0):
    """Reference: direct summation over all other bodies."""
    n, dim = len(m), len(x[0])
    out = []
    for i in range(n):
        a = [0.0] * dim
        for j in range(n):
            if j != i:
                d = [x[j][k] - x[i][k] for k in range(dim)]
                s = sum(c * c for c in d) + eps * eps
                for k in range(dim):
                    a[k] += G * m[j] * d[k] / s ** 1.5
        out.append(a)
    return out


def bodies(n, dim, seed):
    rng = random.Random(seed)
    m = [rng.uniform(0.5, 1.5) for _ in range(n)]
    x = [tuple(rng.uniform(-1.0, 1.0) for _ in range(dim)) for _ in range(n)]
    return m, x


def rel_errors(a, b):
    return [math.dist(p, q) / math.hypot(*q) for p, q in zip(a, b)]


@pytest.mark.parametrize("dim", [2, 3])
def test_theta_zero_is_direct_summation(dim):
    m, x = bodies(120, dim, 5)
    a, count = barnes_hut(m, x, theta=0.0, eps=0.01)
    assert count == 120 * 119
    for e in rel_errors(a, direct(m, x, eps=0.01)):
        assert e < 1e-12


def test_error_falls_with_theta():
    m, x = bodies(300, 3, 1)
    ref = direct(m, x)
    med = []
    for theta in (1.0, 0.7, 0.5, 0.3):
        a, _ = barnes_hut(m, x, theta=theta)
        e = sorted(rel_errors(a, ref))
        med.append(e[len(e) // 2])
    assert med == sorted(med, reverse=True)
    assert med[2] < 1e-2  # theta = 0.5: median relative force error below 1 percent


def test_fewer_interactions_than_direct():
    m, x = bodies(400, 3, 2)
    _, count = barnes_hut(m, x, theta=0.7)
    assert count < 400 * 399 // 2


def test_tree_invariants():
    m, x = bodies(200, 3, 9)
    root = build_tree(m, x)
    assert root.mass == pytest.approx(sum(m), rel=1e-14)
    for k in range(3):
        want = sum(mi * p[k] for mi, p in zip(m, x)) / sum(m)
        assert root.com[k] == pytest.approx(want, abs=1e-14)
    seen = []
    for leaf in leaves(root):
        for i in leaf.bodies:
            assert leaf.contains(x[i])
        seen.extend(leaf.bodies)
    assert sorted(seen) == list(range(200))


def test_monopole_error_bound_for_accepted_cells():
    # For theta < 1 / sqrt(3), each accepted cell obeys the a priori bound of the proof file.
    m, x = bodies(200, 3, 4)
    root = build_tree(m, x)
    theta = 0.4
    stack, checked = [root], 0
    target = (3.0, 0.2, -0.1)
    while stack:
        c = stack.pop()
        if c.children is None:
            continue
        d = math.dist(c.com, target)
        if c.side < theta * d and not c.contains(target):
            idx = [i for leaf in leaves(c) for i in leaf.bodies]
            exact = -sum(m[i] / math.dist(x[i], target) for i in idx)
            mono = -c.mass / d
            b = max(math.dist(x[i], c.com) for i in idx)
            assert abs(exact - mono) <= c.mass * b * b / (d * d * (d - b)) + 1e-15
            checked += 1
        else:
            stack.extend(ch for ch in c.children if ch is not None)
    assert checked > 0


def test_coincident_bodies_with_softening():
    m = [1.0, 1.0, 1.0]
    x = [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (1.0, 0.0, 0.0)]
    a, _ = barnes_hut(m, x, theta=0.5, eps=0.1)
    ref = direct(m, x, eps=0.1)
    for e in rel_errors(a, ref):
        assert e < 1e-12
