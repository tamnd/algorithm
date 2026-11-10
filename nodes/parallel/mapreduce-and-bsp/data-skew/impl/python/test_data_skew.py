# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/data-skew/. The authors are listed in prov/95KA9B.jsonl.

import random
from collections import Counter

from data_skew import hash_loads, lpt_partition, salted_sum, skew_join, skew_join_bound, zipf_keys


def nested_loop_join(r_rel, s_rel):
    return [(a, b, c) for a, b in r_rel for b2, c in s_rel if b == b2]


def test_page_example_loads():
    rng = random.Random(51)
    n, r = 100000, 16
    keys = zipf_keys(rng, n, 10000)
    counts = Counter(keys)
    assert counts.most_common(1) == [(1, 10022)]
    assert max(hash_loads(keys, r)) == 14523
    _, loads = lpt_partition(counts, r)
    assert max(loads) == 10022 == max(counts.values())
    heavy = {k for k, c in counts.items() if c >= n / (4 * r)}
    result, st = salted_sum([(k, 1) for k in keys], r, heavy, r, random.Random(1))
    assert len(heavy) == 6 and result == dict(counts)
    assert max(st.round1_input) == 8083 and max(st.round2_input) <= 16


def test_salted_sum_matches_a_plain_sum_on_seeded_inputs():
    rng = random.Random(52)
    for _ in range(100):
        n = rng.randrange(0, 300)
        keys = zipf_keys(rng, n, rng.choice([1, 5, 200])) if n else []
        pairs = [(k, rng.randrange(1, 10)) for k in keys]
        want = Counter()
        for k, v in pairs:
            want[k] += v
        r, salts = rng.randrange(1, 9), rng.randrange(1, 9)
        heavy = {k for k, c in Counter(keys).items() if c * r >= max(n, 1)}
        result, st = salted_sum(pairs, r, heavy, salts, rng)
        assert result == dict(want)
        assert st.pairs_sent - n == sum(st.round2_input) <= len(heavy) * salts


def test_one_key():
    keys = [7] * 8000
    assert max(hash_loads(keys, 8)) == 8000
    _, loads = lpt_partition(Counter(keys), 8)
    assert max(loads) == 8000
    result, st = salted_sum([(7, 1)] * 8000, 8, {7}, 8, random.Random(3))
    assert result == {7: 8000} and max(st.round1_input) < 4000 and sum(st.round2_input) == 8


def test_lpt_meets_the_list_scheduling_bound():
    rng = random.Random(53)
    for _ in range(100):
        counts = Counter(zipf_keys(rng, rng.randrange(1, 2000), rng.choice([3, 50, 500])))
        r = rng.randrange(1, 20)
        assign, loads = lpt_partition(counts, r)
        n, c_max = sum(counts.values()), max(counts.values())
        assert sum(loads) == n and len(assign) == len(counts)
        assert max(n / r, c_max) <= max(loads) <= n / r + c_max


def test_skew_join_matches_nested_loops_on_seeded_inputs():
    rng = random.Random(54)
    for _ in range(60):
        nk = rng.choice([1, 3, 30])
        r_rel = [(f"a{i}", b) for i, b in enumerate(zipf_keys(rng, rng.randrange(0, 60), nk))]
        s_rel = [(b, f"c{j}") for j, b in enumerate(zipf_keys(rng, rng.randrange(0, 60), nk))]
        p = rng.randrange(1, 9)
        out, _ = skew_join(r_rel, s_rel, p)
        assert Counter(out) == Counter(nested_loop_join(r_rel, s_rel))


def test_skew_join_on_heavy_zipf_keys():
    rng = random.Random(55)
    r_rel = [(i, b) for i, b in enumerate(zipf_keys(rng, 4000, 1000))]
    s_rel = [(b, j) for j, b in enumerate(zipf_keys(rng, 4000, 1000))]
    p = 16
    out, st = skew_join(r_rel, s_rel, p)
    c1, c2 = Counter(b for _, b in r_rel), Counter(b for b, _ in s_rel)
    assert len(out) == sum(c1[b] * c2[b] for b in c1) == 460500
    bound = skew_join_bound(r_rel, s_rel, p)
    assert bound == 250 and max(st.server_load[p:]) == 261 <= 2 * bound + 2  # the heavy part is within 2L + 2
    assert st.largest_load == 751 and len(st.server_load) == 38 and st.pairs_sent == 11908
    group = max(c1[b] + c2[b] for b in c1)
    assert group == 535 + 508 > st.largest_load
