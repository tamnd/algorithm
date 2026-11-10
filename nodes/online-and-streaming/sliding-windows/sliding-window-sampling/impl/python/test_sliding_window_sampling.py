# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-sampling/. The authors are listed in prov/Z8FFSE.jsonl.

import itertools
import random
from collections import Counter
from fractions import Fraction

import pytest

from sliding_window_sampling import BucketSampler, PrioritySampler


class Scripted(random.Random):
    """randrange returns the next value of a fixed script."""

    def __init__(self, script):
        super().__init__(0)
        self.script = iter(script)

    def randrange(self, n):
        v = next(self.script)
        assert 0 <= v < n
        return v


def bucket_distributions(w, steps):
    """Exact distribution of the sample index after every step, over all random outcomes."""
    ranges = [range(((t - 1) % w) + 1) for t in range(1, steps + 1)]
    total = 1
    for r in ranges:
        total *= len(r)
    dists = [Counter() for _ in range(steps)]
    for script in itertools.product(*ranges):
        s = BucketSampler(w, Scripted(script))
        for t in range(steps):
            s.step(t + 1)
            dists[t][s.sample_index()] += 1
    return [{k: Fraction(v, total) for k, v in d.items()} for d in dists]


@pytest.mark.parametrize("w", [1, 2, 3, 4])
def test_bucket_sampler_exactly_uniform(w):
    for t, dist in enumerate(bucket_distributions(w, 3 * w), 1):
        n = min(t, w)
        assert dist == {i: Fraction(1, n) for i in range(t - n + 1, t + 1)}


def test_reservoir_sample_leaves_the_window():
    # a reservoir over the whole stream holds an expired item with probability 1 - W/t
    w, t, trials = 5, 50, 4000
    rng = random.Random(1)
    expired = 0
    for _ in range(trials):
        keep = None
        for i in range(1, t + 1):
            if rng.randrange(i) == 0:
                keep = i
        expired += keep <= t - w
    assert abs(expired / trials - (1 - w / t)) < 0.03


def test_priority_sampler_is_window_argmax():
    rng = random.Random(2)
    for case in range(200):
        seed = rng.randrange(10 ** 9)
        length = rng.choice([1, 2, 5])
        s = PrioritySampler(length, random.Random(seed))
        shadow = random.Random(seed)
        items = []
        t = 0
        for k in range(rng.randint(1, 40)):
            t += rng.choice([0, 0, 1, 2, 6])
            s.insert(t, k)
            items.append((t, k, shadow.random()))
            q = t + rng.choice([0, 1, 3])
            live = [(p, x) for ts, x, p in items if ts > q - length]
            want = max(live)[1] if live else None
            assert s.sample(q) == want
            t = q


def test_priority_sampler_uniform_in_trials():
    # 6 items in the window, 12000 trials: each count has mean 2000 and sd about 41
    counts = Counter()
    for seed in range(12000):
        s = PrioritySampler(6, random.Random(seed))
        for i in range(1, 15):
            s.insert(i, i)
        counts[s.sample(14)] += 1
    assert set(counts) == set(range(9, 15))
    assert all(abs(c - 2000) < 5 * 41 for c in counts.values())


def test_priority_deque_size_is_harmonic():
    n, trials, total = 30, 3000, 0
    rng = random.Random(4)
    for _ in range(trials):
        s = PrioritySampler(n, rng)
        for i in range(1, n + 1):
            s.insert(i, i)
        total += len(s.d)
    h = sum(1 / j for j in range(1, n + 1))
    assert abs(total / trials - h) < 0.15  # about 5 standard errors


def test_bad_arguments():
    with pytest.raises(ValueError):
        PrioritySampler(0)
    with pytest.raises(ValueError):
        BucketSampler(0)
    assert PrioritySampler(3).sample(0) is None
    assert BucketSampler(3).sample() is None
