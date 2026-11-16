# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/joint-compatibility-branch-and-bound/. The authors are listed in prov/V4AT33.jsonl.

import random

import pytest

import rbm
import robest
from joint_compatibility_branch_and_bound import (
    Problem,
    brute_force,
    chi2_quantile,
    jcbb,
    nearest_neighbor,
    pairs_of,
)

MINUS_I = [[-1.0, 0.0], [0.0, -1.0]]


def scene(features, x_hat, readings, p, r):
    """A robot at estimate x_hat reads features of a known map: h_j = m_j - x_hat, H_j = -I."""
    h = [rbm.sub(m, x_hat) for m in features]
    return readings, h, [MINUS_I] * len(features), p, r


def random_scene(rng, m, n):
    features = [[rng.uniform(0.0, 3.0), rng.uniform(0.0, 3.0)] for _ in range(n)]
    a = [[rng.uniform(-0.4, 0.4) for _ in range(2)] for _ in range(2)]
    p = rbm.add(rbm.mul(a, rbm.transpose(a)), [[0.02, 0.0], [0.0, 0.02]])
    r = [[0.01, 0.0], [0.0, 0.01]]
    x_true = robest.gauss_sample(rng, [0.0, 0.0], p)
    readings = []
    for _ in range(m):
        if rng.random() < 0.2:
            readings.append([rng.uniform(-1.0, 4.0), rng.uniform(-1.0, 4.0)])  # clutter
        else:
            f = features[rng.randrange(n)]
            readings.append(robest.gauss_sample(rng, rbm.sub(f, x_true), r))
    return scene(features, [0.0, 0.0], readings, p, r)


@pytest.mark.parametrize("dof,level", sorted(robest.CHI2))
def test_chi2_quantile_against_the_table(dof, level):
    assert abs(chi2_quantile(level, dof) - robest.CHI2[(dof, level)]) < 1e-3


@pytest.mark.parametrize("dof,want", [(4, 9.488), (6, 12.592), (10, 18.307)])
def test_chi2_quantile_for_more_degrees_of_freedom(dof, want):
    assert abs(chi2_quantile(0.95, dof) - want) < 1e-3


@pytest.mark.parametrize("unique", [False, True])
def test_jcbb_equals_brute_force_over_all_hypotheses(unique):
    rng = random.Random(11 if unique else 12)
    for trial in range(12):
        m, n = 3 + trial % 3, 2 + trial % 3
        args = random_scene(rng, m, n)
        hyp, d2, _ = jcbb(*args, unique=unique)
        want, want_d2 = brute_force(*args, unique=unique)
        assert hyp == want
        assert abs(d2 - want_d2) < 1e-9
        paper, _, _ = jcbb(*args, unique=unique, tie_break=False)
        assert len(pairs_of(paper)) == len(pairs_of(want))


def test_joint_distance_never_decreases_when_a_pairing_is_added():
    rng = random.Random(13)
    for _ in range(30):
        args = random_scene(rng, 5, 4)
        prob = Problem(*args)
        pairs = [(i, rng.randrange(4)) for i in range(5)]
        d = [prob.d2(pairs[:k]) for k in range(6)]
        assert all(b >= a - 1e-12 for a, b in zip(d, d[1:]))


def test_every_prefix_of_the_result_is_jointly_compatible():
    rng = random.Random(14)
    for _ in range(20):
        args = random_scene(rng, 5, 4)
        prob = Problem(*args)
        hyp, _, _ = jcbb(*args)
        pairs = pairs_of(hyp)
        for k in range(1, len(pairs) + 1):
            assert prob.jointly_compatible(pairs[:k])
        assert all(prob.individually_compatible(i, j) for i, j in pairs)


def example():
    """The example of the page: three features on a line and a robot that is 0.7 m off."""
    features = [[0.0, 2.0], [1.0, 2.0], [2.5, 2.0]]
    p = [[0.25, 0.0], [0.0, 0.25]]
    r = [[0.01, 0.0], [0.0, 0.01]]
    readings = [[0.72, 2.01], [1.69, 1.98], [3.21, 2.02]]  # the true robot is at (-0.7, 0)
    return scene(features, [0.0, 0.0], readings, p, r)


def test_example_nearest_neighbor_fails_and_jcbb_succeeds():
    args = example()
    assert nearest_neighbor(*args) == [1, 1, 2]
    hyp, d2, _ = jcbb(*args)
    assert hyp == [0, 1, 2]
    assert d2 < chi2_quantile(0.95, 6)
    prob = Problem(*args)
    assert not prob.jointly_compatible([(0, 1), (1, 1), (2, 2)])


def test_clutter_reading_stays_unpaired():
    features = [[0.0, 0.0], [2.0, 0.0], [0.0, 2.0]]
    p = [[0.04, 0.0], [0.0, 0.04]]
    r = [[0.01, 0.0], [0.0, 0.01]]
    readings = [[0.1, 0.0], [2.1, 0.02], [5.0, 5.0], [0.08, 2.01]]
    hyp, _, _ = jcbb(*scene(features, [0.0, 0.0], readings, p, r))
    assert hyp == [0, 1, None, 2]


def test_pruning_visits_fewer_nodes_than_the_full_tree():
    rng = random.Random(15)
    for _ in range(5):
        args = random_scene(rng, 5, 4)
        _, _, nodes = jcbb(*args)
        full = sum(5 ** k for k in range(6))
        assert nodes < full
