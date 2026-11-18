# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deepmimic/. The authors are listed in prov/MY80RM.jsonl.
"""Tests of the DeepMimic toy: reward, RSI and early termination.

The reward lies in [0, 1] and is 1 exactly on the reference. RSI states
lie on the reference clip and spread over its phases. With ET, the step of
the fall and every later step get reward 0; without ET a falling policy
keeps collecting reward while it lies on the ground. A tracking policy has
a higher return than zero torque (measured on this toy).
"""

import math
import random

import deepmimic as dm


def test_reward_range_and_maximum():
    rod, ref = dm.Rod(), dm.Reference()
    rng = random.Random(1)
    for _ in range(500):
        t = rng.uniform(0, 4)
        q, qd = rng.uniform(-1.5, 1.5), rng.uniform(-5, 5)
        r = dm.reward(rod, ref, t, q, qd)
        assert 0.0 < r < 1.0
        g = rng.random()
        rg = dm.reward(rod, ref, t, q, qd, r_goal=g)
        assert abs(rg - (0.7 * r + 0.3 * g)) < 1e-15
        assert dm.reward(rod, ref, t, ref.q(t), ref.qd(t)) == 1.0
    # the pose term has the largest weight
    t = 0.3
    near = dm.reward(rod, ref, t, ref.q(t) + 0.1, ref.qd(t))
    far = dm.reward(rod, ref, t, ref.q(t) + 0.5, ref.qd(t))
    assert far < near < 1.0


def test_rsi_states_lie_on_the_reference():
    ref = dm.Reference(amplitude=0.4, period=2.0)
    rng = random.Random(2)
    phases = []
    for _ in range(400):
        t0, q, qd = dm.initial_state(ref, rng)
        assert 0.0 <= t0 < ref.T
        assert q == ref.q(t0) and qd == ref.qd(t0)
        phases.append(t0 / ref.T)
    counts = [sum(1 for p in phases if k / 4 <= p < (k + 1) / 4) for k in range(4)]
    assert min(counts) > 60
    assert dm.initial_state(ref) == (0.0, 0.0, ref.qd(0.0))


def test_early_termination_zeroes_later_rewards():
    rod, ref = dm.Rod(), dm.Reference()
    with_et = dm.episode(rod, ref, dm.zero_policy, steps=60, early_termination=True)
    k = with_et["ended"]
    assert k is not None and k < 60
    assert all(r == 0.0 for r in with_et["rewards"][k:])
    assert all(r > 0.0 for r in with_et["rewards"][:k])
    without = dm.episode(rod, ref, dm.zero_policy, steps=60, early_termination=False)
    assert without["ended"] is None
    assert without["fallen_steps"] > 30
    # lying on the ground still earns reward without ET
    assert sum(without["rewards"][k:]) > 1.0
    assert without["return"] > with_et["return"]


def test_tracking_policy_beats_zero_torque():
    rod, ref = dm.Rod(), dm.Reference()
    rng = random.Random(3)
    pd = dm.pd_policy(rod, ref)
    for _ in range(5):
        seed = rng.randrange(10 ** 6)
        a = dm.episode(rod, ref, pd, steps=60, rng=random.Random(seed))
        b = dm.episode(rod, ref, dm.zero_policy, steps=60, rng=random.Random(seed))
        assert a["ended"] is None and a["fallen_steps"] == 0
        assert a["return"] > b["return"]
        assert sum(a["rewards"]) / 60 > 0.9


def test_rod_ground_stop():
    rod = dm.Rod()
    q, qd = 1.5, 3.0
    for _ in range(100):
        q, qd = rod.step(q, qd, 0.0, 1e-3)
    assert q == math.pi / 2 and qd == 0.0
