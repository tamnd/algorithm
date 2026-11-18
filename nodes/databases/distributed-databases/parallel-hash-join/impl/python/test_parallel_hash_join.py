# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-hash-join/. The authors are listed in prov/XNDHHS.jsonl.

import random
from collections import Counter

import pytest

import dbrel
from dbrel import Relation
from parallel_hash_join import broadcast_join, parallel_hash_join, split_round_robin, stable_hash


def whole(parts):
    c = Counter()
    for part in parts:
        c.update(part.rows)
    return Relation(parts[0].schema, c)


def oracle_sent(r_parts, s_parts, key, h=stable_hash):
    """Count the tuples whose target node differs from their home node, directly."""
    p = len(r_parts)
    sent = 0
    pairs = set()
    for parts in (r_parts, s_parts):
        for i, part in enumerate(parts):
            for t in part.sorted_rows():
                j = h(tuple(t[part.index(a)] for a in key)) % p
                if j != i:
                    sent += 1
                    pairs.add((i, j))
    return sent, len(pairs)


def random_parts(rng, schema, n, p, domain, null_rate=0.0):
    rel = dbrel.random_relation(rng, schema, n, domain, null_rate=null_rate)
    if rng.random() < 0.5:
        return split_round_robin(rel, p)
    parts = [Counter() for _ in range(p)]
    for t in rel.sorted_rows():
        parts[rng.randrange(p)][t] += 1
    return [Relation(schema, c) for c in parts]


@pytest.mark.parametrize("seed", range(60))
def test_matches_natural_join(seed):
    rng = random.Random(seed)
    p = rng.randint(1, 8)
    r_parts = random_parts(rng, ("A", "B"), rng.randint(0, 40), p, {"A": 5, "B": 3}, 0.1 * (seed % 2))
    s_parts = random_parts(rng, ("A", "C"), rng.randint(0, 40), p, {"A": 5, "C": 4}, 0.1 * (seed % 2))
    out, stats = parallel_hash_join(r_parts, s_parts)
    expect = dbrel.natural_join(whole(r_parts), whole(s_parts))
    assert out == expect
    assert sum(stats.output) == len(expect)
    assert sum(stats.received) == len(whole(r_parts)) + len(whole(s_parts))
    sent, msgs = oracle_sent(r_parts, s_parts, ("A",))
    assert stats.tuples_sent == sent
    assert stats.messages == msgs <= p * (p - 1)
    assert stats.rounds == 1


@pytest.mark.parametrize("seed", range(20))
def test_two_key_attributes_and_partial_key(seed):
    rng = random.Random(100 + seed)
    p = rng.randint(2, 6)
    dom = {"A": 3, "B": 3, "C": 4, "D": 4}
    r_parts = random_parts(rng, ("A", "B", "C"), rng.randint(0, 30), p, dom)
    s_parts = random_parts(rng, ("B", "A", "D"), rng.randint(0, 30), p, dom)
    expect = dbrel.natural_join(whole(r_parts), whole(s_parts))
    for key in (None, ("A",), ("B",), ("A", "B")):
        out, _ = parallel_hash_join(r_parts, s_parts, key)
        assert out == expect


def test_hand_cases():
    empty_r = [Relation(("A", "B"), []) for _ in range(3)]
    empty_s = [Relation(("A", "C"), []) for _ in range(3)]
    out, stats = parallel_hash_join(empty_r, empty_s)
    assert len(out) == 0 and stats.tuples_sent == 0 and stats.messages == 0
    one_r = [Relation(("A", "B"), [(1, "x")])]
    one_s = [Relation(("A", "C"), [(1, "y"), (1, "y")])]
    out, stats = parallel_hash_join(one_r, one_s)
    assert out.rows == Counter({(1, "x", "y"): 2})
    assert stats.tuples_sent == 0
    nulls_r = [Relation(("A", "B"), [(None, 1), (2, 1)]), Relation(("A", "B"), [(2, 2)])]
    nulls_s = [Relation(("A", "C"), [(None, 5)]), Relation(("A", "C"), [(2, 6)])]
    out, _ = parallel_hash_join(nulls_r, nulls_s)
    assert out.rows == Counter({(2, 1, 6): 1, (2, 2, 6): 1})


def test_skew_sends_everything_to_one_node():
    p = 4
    r = Relation(("A", "B"), [(7, b) for b in range(12)])
    s = Relation(("A", "C"), [(7, c) for c in range(8)])
    out, stats = parallel_hash_join(split_round_robin(r, p), split_round_robin(s, p))
    assert len(out) == 96
    j = stable_hash((7,)) % p
    assert stats.received[j] == 20 and sum(stats.received) == 20
    assert stats.output[j] == 96
    assert stats.tuples_sent == 15  # 3 of 12 and 2 of 8 tuples already sit on node j


def test_co_partitioned_input_sends_nothing():
    rng = random.Random(7)
    p = 5
    r = dbrel.random_relation(rng, ("A", "B"), 50, {"A": 5, "B": 3})
    s = dbrel.random_relation(rng, ("A", "C"), 50, {"A": 5, "C": 3})

    def by_hash(rel):
        parts = [Counter() for _ in range(p)]
        for t, c in rel.rows.items():
            parts[stable_hash((t[0],)) % p][t] += c
        return [Relation(rel.schema, x) for x in parts]

    out, stats = parallel_hash_join(by_hash(r), by_hash(s))
    assert out == dbrel.natural_join(r, s)
    assert stats.tuples_sent == 0 and stats.messages == 0


def test_page_example():
    h = lambda k: k[0]
    r = [Relation(("A", "B"), [(3, "r0"), (1, "r3"), (2, "r6")]),
         Relation(("A", "B"), [(1, "r1"), (5, "r4"), (6, "r7")]),
         Relation(("A", "B"), [(4, "r2"), (9, "r5")])]
    s = [Relation(("A", "C"), [(1, "s0"), (8, "s3")]),
         Relation(("A", "C"), [(4, "s1"), (5, "s4")]),
         Relation(("A", "C"), [(1, "s2"), (3, "s5")])]
    out, stats = parallel_hash_join(r, s, h=h)
    assert out == dbrel.natural_join(whole(r), whole(s))
    assert len(out) == 7
    assert stats.received == [4, 6, 4]
    assert stats.output == [1, 5, 1]
    assert stats.tuples_sent == 11
    assert stats.messages == 6


@pytest.mark.parametrize("seed", range(20))
def test_broadcast_variant(seed):
    rng = random.Random(500 + seed)
    p = rng.randint(1, 8)
    r_parts = random_parts(rng, ("A", "B"), rng.randint(0, 15), p, {"A": 4, "B": 3})
    s_parts = random_parts(rng, ("A", "C"), rng.randint(0, 40), p, {"A": 4, "C": 3})
    out, stats = broadcast_join(r_parts, s_parts)
    assert out == dbrel.natural_join(whole(r_parts), whole(s_parts))
    assert stats.tuples_sent == len(whole(r_parts)) * (p - 1)


def test_bad_arguments():
    r = [Relation(("A", "B"), [])]
    s = [Relation(("A", "C"), [])]
    with pytest.raises(ValueError):
        parallel_hash_join(r, s + s)
    with pytest.raises(ValueError):
        parallel_hash_join(r, s, key=("B",))
