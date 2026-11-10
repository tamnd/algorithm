# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reduce-side-join/. The authors are listed in prov/2FMSJX.jsonl.

import random
from collections import Counter

from reduce_side_join import join_size, nested_loop_join, reduce_side_join

R = [("ann", 1), ("bob", 2), ("cid", 1), ("dan", 3)]
S = [(1, "x"), (2, "y"), (1, "z"), (4, "w")]


def zipf_keys(rng, n, keys):
    return rng.choices(range(1, keys + 1), weights=[1 / i for i in range(1, keys + 1)], k=n)


def test_page_example():
    out, st = reduce_side_join(R, S, 2)
    assert Counter(out) == Counter([("ann", 1, "x"), ("ann", 1, "z"), ("cid", 1, "x"), ("cid", 1, "z"),
                                    ("bob", 2, "y")])
    assert st.pairs_sent == 8 and sum(st.reducer_input) == 8
    out2, st2 = reduce_side_join(R, S, 2, buffer_r_only=True)
    assert Counter(out2) == Counter(out) and st2.largest_buffer == 2 and st.largest_buffer == 4


def test_matches_nested_loops_on_seeded_inputs():
    rng = random.Random(21)
    for _ in range(200):
        nk = rng.choice([1, 3, 20])
        r_rel = [(f"a{i}", rng.randrange(nk)) for i in range(rng.randrange(0, 30))]
        s_rel = [(rng.randrange(nk), f"c{i}") for i in range(rng.randrange(0, 30))]
        k = rng.randrange(1, 6)
        want = Counter(nested_loop_join(r_rel, s_rel))
        for flag in (False, True):
            out, st = reduce_side_join(r_rel, s_rel, k, buffer_r_only=flag)
            assert Counter(out) == want
            assert len(out) == join_size(r_rel, s_rel)
            assert st.pairs_sent == len(r_rel) + len(s_rel)


def test_empty_and_one_key():
    assert reduce_side_join([], S, 3)[0] == []
    assert reduce_side_join(R, [], 3)[0] == []
    r_rel = [(i, 0) for i in range(30)]
    s_rel = [(0, j) for j in range(40)]
    out, st = reduce_side_join(r_rel, s_rel, 8)
    assert len(out) == 1200 and st.largest_reducer_input == 70
    assert sorted(st.reducer_input)[:7] == [0] * 7


def test_heavy_zipf_key_sets_the_largest_reducer_input():
    rng = random.Random(22)
    r_rel = [(i, b) for i, b in enumerate(zipf_keys(rng, 3000, 500))]
    s_rel = [(b, j) for j, b in enumerate(zipf_keys(rng, 3000, 500))]
    out, st = reduce_side_join(r_rel, s_rel, 16)
    assert len(out) == join_size(r_rel, s_rel)
    group = Counter(b for _, b in r_rel) + Counter(b for b, _ in s_rel)
    assert st.largest_reducer_input >= max(group.values()) > 6000 / 16
