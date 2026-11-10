# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dgim-algorithm/. The authors are listed in prov/KD0VWY.jsonl.

import itertools
import random
from fractions import Fraction

from dgim_algorithm import DGIM


def check_stream(bits, window, k, check_all_w=False):
    """Run DGIM and check the error bound, the bucket rule and the space bound at every step."""
    d = DGIM(window, k)
    cap = (k + 1) // 2
    ones = 0
    for t, b in enumerate(bits, 1):
        d.update(b)
        ones += b
        true = sum(bits[max(0, t - window):t])
        est = d.query()
        # Relative error less than 1/(2L), hence at most 1/k; exact when the count is 0.
        assert 2 * cap * abs(est - true) < true or est == true
        assert k * abs(est - true) <= true
        # The bucket rule: L or L + 1 buckets below the largest size, 1 to L + 1 at the largest.
        sizes = [len(lev) for lev in d.levels]
        for j, n in enumerate(sizes):
            if j < len(sizes) - 1:
                assert cap <= n <= cap + 1
            else:
                assert 1 <= n <= cap + 1
        # Every bucket is inside the window, and the space bound holds.
        assert all(ts > t - window for ts, _ in d.buckets())
        assert len(d.buckets()) <= d.bucket_bound()
        assert d.merges < ones or ones == 0
        if check_all_w:
            for w in range(1, window + 1):
                tw = sum(bits[max(0, t - w):t])
                ew = d.query(w)
                assert 2 * cap * abs(ew - tw) < tw or ew == tw


def test_page_example():
    bits = [int(c) for c in "110111011011"]
    d = DGIM(10, 2)
    for b in bits[:9]:
        d.update(b)
    assert d.buckets() == [(9, 1), (8, 2), (5, 4)]
    assert d.query() == Fraction(11, 2)
    for b in bits[9:]:
        d.update(b)
    assert d.buckets() == [(12, 1), (11, 2), (8, 2), (5, 4)]
    assert d.query() == Fraction(15, 2)
    assert d.merges == 5


def test_all_short_streams():
    # Every stream of 11 bits; each step is checked, so every shorter stream is covered too.
    for bits in itertools.product((0, 1), repeat=11):
        for k in (1, 2, 4):
            check_stream(list(bits), 6, k, check_all_w=(k == 2))


def test_seeded_random_streams():
    rng = random.Random(7)
    for _ in range(100):
        window = rng.randint(1, 60)
        k = rng.randint(1, 12)
        p = rng.choice((0.05, 0.3, 0.5, 0.9, 1.0))
        bits = [1 if rng.random() < p else 0 for _ in range(rng.randint(1, 250))]
        check_stream(bits, window, k, check_all_w=(window <= 12))


def test_adversarial_streams():
    for window in (1, 2, 7, 16, 33, 64):
        for k in (1, 2, 5, 6, 10):
            n = 3 * window + 5
            check_stream([1] * n, window, k)
            check_stream([i % 2 for i in range(n)], window, k)
            # Bursts that expire a large bucket while many small ones remain.
            burst = ([1] * window + [0] * (window // 2 + 1)) * 3
            check_stream(burst, window, k)
            check_stream([1 if i % window == 0 else 0 for i in range(n)], window, k)


def test_half_last_estimate_breaks_one_over_k():
    # Seven 1s with k = 10 (L = 5): five buckets of size 1 and one of size 2.
    d = DGIM(10, 10)
    for _ in range(7):
        d.update(1)
    assert sorted(size for _, size in d.buckets()) == [1, 1, 1, 1, 1, 2]
    half = d.total - Fraction(2, 2)  # TOTAL - LAST/2 = 6
    assert half == 6 and abs(half - 7) / 7 > Fraction(1, 10)
    assert abs(d.query() - 7) / 7 == Fraction(1, 14)


def test_bucket_count_grows_like_k_log_w():
    window, k = 1 << 12, 4
    d = DGIM(window, k)
    most = 0
    for _ in range(3 * window):
        d.update(1)
        most = max(most, len(d.buckets()))
    assert most <= d.bucket_bound() == 3 * 12
