# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/map-side-join/. The authors are listed in prov/MES4WN.jsonl.

import random
from collections import Counter

import pytest

from map_side_join import (broadcast_join, co_partition, merge_join, merge_join_all, nested_loop_join,
                           split)

R = [("ann", 1), ("bob", 2), ("cid", 1), ("dan", 3)]
S = [(1, "x"), (2, "y"), (1, "z"), (4, "w")]
WANT = Counter([("ann", 1, "x"), ("ann", 1, "z"), ("cid", 1, "x"), ("cid", 1, "z"), ("bob", 2, "y")])


def zipf_keys(rng, n, keys):
    return rng.choices(range(1, keys + 1), weights=[1 / i for i in range(1, keys + 1)], k=n)


def test_page_example():
    out, st = broadcast_join(split(R, 2), S)
    assert Counter(out) == WANT
    assert st.tuples_copied == 8 and st.pairs_shuffled == 0 and st.task_memory == [4, 4]
    r_parts, s_parts = co_partition(R, 2, 1), co_partition(S, 2, 0)
    assert r_parts[1] == [("ann", 1), ("cid", 1), ("bob", 2), ("dan", 3)] and s_parts[0] == [(4, "w")]
    out, st = merge_join_all(r_parts, s_parts)
    assert Counter(out) == WANT and st.tuples_copied == 0 and st.task_memory == [0, 2]


def test_both_match_nested_loops_on_seeded_inputs():
    rng = random.Random(31)
    for _ in range(200):
        nk = rng.choice([1, 3, 20])
        r_rel = [(f"a{i}", rng.randrange(nk)) for i in range(rng.randrange(0, 30))]
        s_rel = [(rng.randrange(nk), f"c{i}") for i in range(rng.randrange(0, 30))]
        want = Counter(nested_loop_join(r_rel, s_rel))
        m, k = rng.randrange(1, 6), rng.randrange(1, 6)
        out, st = broadcast_join(split(r_rel, m), s_rel)
        assert Counter(out) == want and st.tuples_copied == m * len(s_rel)
        out, st = merge_join_all(co_partition(r_rel, k, 1), co_partition(s_rel, k, 0))
        assert Counter(out) == want and st.tuples_copied == 0


def test_empty_and_one_key():
    assert broadcast_join(split([], 3), S)[0] == [] and broadcast_join(split(R, 3), [])[0] == []
    assert merge_join([], S)[0] == [] and merge_join(R, [])[0] == []
    r_rel = [(i, 0) for i in range(30)]
    s_rel = [(0, j) for j in range(40)]
    out, st = merge_join_all(co_partition(r_rel, 4, 1), co_partition(s_rel, 4, 0))
    assert len(out) == 1200 and max(st.task_input) == 70 and max(st.task_memory) == 40
    out, st = broadcast_join(split(r_rel, 5), s_rel)
    assert len(out) == 1200 and st.task_input == [46] * 5


def test_merge_join_rejects_inputs_that_are_not_co_partitioned():
    with pytest.raises(ValueError):
        merge_join_all(co_partition(R, 2, 1), co_partition(S, 3, 0))
    with pytest.raises(ValueError):
        merge_join_all([list(reversed(co_partition(R, 1, 1)[0]))], co_partition(S, 1, 0))


def test_broadcast_balances_a_heavy_key_of_the_large_side():
    rng = random.Random(32)
    r_rel = [(i, b) for i, b in enumerate(zipf_keys(rng, 30000, 500))]
    s_rel = [(b, f"d{b}") for b in range(1, 501)]
    m = 10
    out, st = broadcast_join(split(r_rel, m), s_rel)
    assert sorted(out) == sorted(nested_loop_join(r_rel, s_rel)) and len(out) == 30000
    assert st.tuples_copied == 5000 < len(r_rel) + len(s_rel)
    assert max(st.task_input) == 3500
    heavy = Counter(b for _, b in r_rel).most_common(1)[0][1]
    assert heavy + 1 > 3500
