# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monte-carlo-localization/. The authors are listed in prov/GRKHHG.jsonl.

import math
import random

import pytest

import robest
from monte_carlo_localization import Recovery, mcl

# A ring of 30 cells. Each cell has a color in {0, 1, 2, 3}. The sensor reads
# the right color with probability 0.85, and each other color with 0.05.
# A control moves the robot 1 cell ahead with probability 0.8, 0 cells
# with 0.1 and 2 cells with 0.1.
C = 30
_R = random.Random(3)
COLORS = [_R.randrange(4) for _ in range(C)]
P_RIGHT = 0.85
MOVE = {0: 0.1, 1: 0.8, 2: 0.1}


def ring_likelihood(z, x):
    return P_RIGHT if COLORS[x] == z else (1.0 - P_RIGHT) / 3.0


def ring_motion(rng, x, u):
    r = rng.random()
    s = 0 if r < 0.1 else (1 if r < 0.9 else 2)
    return (x + u * s) % C


def ring_sense(rng, x):
    if rng.random() < P_RIGHT:
        return COLORS[x]
    return rng.choice([c for c in range(4) if c != COLORS[x]])


def histogram_step(bel, u, z):
    """The exact Bayes filter on the ring, for comparison."""
    pred = [0.0] * C
    for x in range(C):
        for s, p in MOVE.items():
            pred[(x + u * s) % C] += bel[x] * p
    post = [pred[x] * ring_likelihood(z, x) for x in range(C)]
    total = sum(post)
    return [p / total for p in post]


def counts(particles):
    c = [0] * C
    for x in particles:
        c[x] += 1
    return c


def test_mcl_approximates_the_exact_filter():
    rng = random.Random(0)
    n = 3000
    truth = 0
    bel = [1.0 / C] * C
    particles = [rng.randrange(C) for _ in range(n)]
    for _ in range(8):
        truth = ring_motion(rng, truth, 1)
        z = ring_sense(rng, truth)
        bel = histogram_step(bel, 1, z)
        particles, _ = mcl(particles, 1, z, ring_motion, ring_likelihood, rng)
        emp = [c / n for c in counts(particles)]
        tv = 0.5 * sum(abs(a - b) for a, b in zip(bel, emp))
        assert tv < 0.1
    assert max(bel) > 0.8  # the colors make the pose unique after 8 steps


def run_kidnapping(seed, recovery, n=300, steps=70, kidnap_at=20, jump=13):
    rng = random.Random(seed)
    truth = 0
    particles = [rng.randrange(C) for _ in range(n)]
    right = []
    p_random = []
    for t in range(steps):
        if t == kidnap_at:
            truth = (truth + jump) % C
        truth = ring_motion(rng, truth, 1)
        z = ring_sense(rng, truth)
        particles, _ = mcl(particles, 1, z, ring_motion, ring_likelihood, rng, recovery)
        c = counts(particles)
        right.append(max(range(C), key=lambda i: c[i]) == truth)
        if recovery is not None:
            p_random.append(recovery.p_random())
    return right, p_random


def test_augmented_mcl_recovers_from_a_kidnapping_and_plain_mcl_does_not():
    rec = Recovery(0.05, 0.5, lambda rng: rng.randrange(C))
    aug, p_random = run_kidnapping(0, rec)
    plain, _ = run_kidnapping(0, None)
    assert sum(aug[10:20]) >= 7 and sum(plain[10:20]) >= 7  # both track before the kidnapping
    assert sum(aug[40:]) >= 15  # of 30 steps
    assert sum(plain[40:]) <= 3
    assert max(p_random[20:25]) > 0.3  # the drop of the weights starts the injection
    # while it tracks, one wrong color can give a short burst, but few random particles on average
    assert sum(p_random[12:20]) / 8 < 0.05


def test_recovery_probability():
    rec = Recovery(0.1, 0.5, None)
    assert rec.p_random() == 0.0
    rec.observe(0.8)
    assert rec.w_slow == pytest.approx(0.08) and rec.w_fast == pytest.approx(0.4)
    assert rec.p_random() == 0.0  # w_fast > w_slow
    for _ in range(200):
        rec.observe(0.8)
    rec.observe(0.2)
    w_slow = 0.8 - 0.1 * 0.6
    w_fast = 0.8 - 0.5 * 0.6
    assert rec.p_random() == pytest.approx(1.0 - w_fast / w_slow, abs=1e-9)
    with pytest.raises(ValueError):
        Recovery(0.5, 0.1, None)


def test_plain_mcl_rejects_all_zero_weights():
    rng = random.Random(1)
    with pytest.raises(ValueError):
        mcl([0, 1, 2], 1, 0, ring_motion, lambda z, x: 0.0, rng)
    rec = Recovery(0.1, 0.5, lambda r: 99)
    rec.w_slow = rec.w_fast = 0.5
    new, w_avg = mcl([0, 1, 2], 1, 0, ring_motion, lambda z, x: 0.0, rng, rec)
    assert w_avg == 0.0 and len(new) == 3


# Global localization in a 10 m by 10 m room with 4 range beacons.
BEACONS = [(0.0, 0.0), (10.0, 0.0), (0.0, 10.0), (10.0, 10.0)]
SIGMA_R = 0.3


def plane_motion(rng, x, u):
    rot, trans = u
    th = robest.wrap_angle(x[2] + rot + rng.gauss(0.0, 0.05 + 0.05 * abs(rot)))
    d = trans + rng.gauss(0.0, 0.05 + 0.1 * abs(trans))
    return (x[0] + d * math.cos(th), x[1] + d * math.sin(th), th)


def plane_likelihood(z, x):
    p = 1.0
    for r, (bx, by) in zip(z, BEACONS):
        e = r - math.hypot(bx - x[0], by - x[1])
        p *= math.exp(-0.5 * e * e / (SIGMA_R * SIGMA_R))
    return p


def test_global_localization_with_range_beacons():
    rng = random.Random(7)
    n = 3000
    particles = [(rng.uniform(0, 10), rng.uniform(0, 10), rng.uniform(-math.pi, math.pi)) for _ in range(n)]
    truth = (2.0, 3.0, 0.0)
    controls = [(0.0, 1.0)] * 5 + [(math.pi / 2, 1.0)] + [(0.0, 1.0)] * 4
    for u in controls:
        rot, trans = u
        th = truth[2] + rot
        truth = (truth[0] + trans * math.cos(th), truth[1] + trans * math.sin(th), th)
        z = [math.hypot(bx - truth[0], by - truth[1]) + rng.gauss(0.0, SIGMA_R) for bx, by in BEACONS]
        particles, _ = mcl(particles, u, z, plane_motion, plane_likelihood, rng)
    mx = sum(p[0] for p in particles) / n
    my = sum(p[1] for p in particles) / n
    mth = math.atan2(sum(math.sin(p[2]) for p in particles), sum(math.cos(p[2]) for p in particles))
    assert math.hypot(mx - truth[0], my - truth[1]) < 0.4
    assert abs(robest.wrap_angle(mth - truth[2])) < 0.2
