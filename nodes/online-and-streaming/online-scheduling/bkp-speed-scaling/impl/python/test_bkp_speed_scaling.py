# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bkp-speed-scaling/. The authors are listed in prov/Z0T4F5.jsonl.

import math
import random
from fractions import Fraction

from bkp_speed_scaling import bkp_schedule, bkp_speed


def yds(jobs):
    """Return the optimal energy profile by the YDS algorithm, exactly, as (density, length) pairs."""
    rest = [(Fraction(r), Fraction(w), Fraction(d)) for r, w, d in jobs]
    out = []
    while rest:
        best = None
        for a in {r for r, _, _ in rest}:
            for b in {d for _, _, d in rest}:
                if b <= a:
                    continue
                work = sum(w for r, w, d in rest if a <= r and d <= b)
                if work > 0 and (best is None or work / (b - a) > best[0]):
                    best = (work / (b - a), a, b)
        g, a, b = best
        out.append((g, b - a))
        length = b - a

        def squeeze(t):
            return t if t <= a else (a if t < b else t - length)

        rest = [(squeeze(r), w, squeeze(d)) for r, w, d in rest if not (a <= r and d <= b)]
    return out


def yds_energy(jobs, alpha):
    return sum(g ** alpha * length for g, length in yds(jobs))


def bound(alpha):
    return 2 * (alpha / (alpha - 1)) ** alpha * math.e ** alpha


def test_speed_of_one_job():
    # Job (0, w, d): speed w / (d - t) until (1 - 1/e) d, then w (e - 1) / t.
    w, d = 2.0, 3.0
    turn = (1 - 1 / math.e) * d
    for t in (0.1, 0.9, 1.5, turn - 1e-6):
        assert math.isclose(bkp_speed([(0, w, d)], t), w / (d - t), rel_tol=1e-12)
    for t in (turn + 1e-6, 2.5, 4.0):
        assert math.isclose(bkp_speed([(0, w, d)], t), w * (math.e - 1) / t, rel_tol=1e-12)


def test_one_job_finishes_at_one_minus_one_over_e():
    w, d, h = 2.0, 3.0, 1e-3
    for alpha in (2, 3):
        total, done, _ = bkp_schedule([(0, w, d)], h, alpha)
        assert abs(done[0] - (1 - 1 / math.e) * d) <= 2 * h
        ratio = total / float(yds_energy([(0, w, d)], alpha))
        assert math.isclose(ratio, (math.e ** (alpha - 1) - 1) / (alpha - 1), rel_tol=5e-3)


def test_example():
    jobs = [(0, 4, 4), (1, 3, 3), (2, 2, 6)]
    speeds = [bkp_speed(jobs, t) for t in (0.5, 1.5, 2.5, 3.5)]
    assert all(math.isclose(x, y, rel_tol=1e-12) for x, y in zip(speeds, [8 / 7, 14 / 5, 14 / 3, 18 / 5]))
    h = 1e-3
    for alpha, low, high in ((2, 2.0, 2.3), (3, 4.5, 5.2)):
        total, done, _ = bkp_schedule(jobs, h, alpha)
        assert all(c <= d + h for c, (_, _, d) in zip(done, jobs))
        assert low < total / float(yds_energy(jobs, alpha)) < high


def test_random_inputs_are_feasible_and_within_the_bounds():
    rng = random.Random(2004)
    h = 0.01
    for alpha in (2, 3):
        for _ in range(60):
            jobs = []
            for _ in range(rng.randint(1, 4)):
                r = rng.randint(0, 5)
                jobs.append((r, rng.randint(1, 6), r + rng.randint(1, 4)))
            total, done, top = bkp_schedule(jobs, h, alpha)
            assert all(c <= d + 3 * h for c, (_, _, d) in zip(done, jobs))
            ratio = total / float(yds_energy(jobs, alpha))
            assert 0.99 <= ratio <= bound(alpha)
            assert top <= math.e * float(yds(jobs)[0][0]) + 1e-9
