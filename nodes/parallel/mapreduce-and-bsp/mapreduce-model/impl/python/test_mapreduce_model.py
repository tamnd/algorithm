# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mapreduce-model/. The authors are listed in prov/5E46VV.jsonl.

import random
from collections import Counter

from mapreduce_model import (group_sorted, hash_partitioner, make_splits, pair_size, run_job,
                             run_round, stable_hash, sum_reduce, word_count_map)


def random_docs(rng: random.Random, n_docs: int, vocab: int) -> list[tuple[int, str]]:
    return [(d, " ".join(f"w{rng.randrange(vocab)}" for _ in range(rng.randrange(12))))
            for d in range(n_docs)]


def counts_of(outputs):
    return {k: v for out in outputs for k, v in out}


def test_page_example():
    docs = [(1, "a rose is a rose"), (2, "is a rose"), (3, "a b")]
    out, st = run_round(make_splits(docs, 2), word_count_map, sum_reduce, 2)
    assert counts_of(out) == {"a": 4, "rose": 3, "is": 2, "b": 1}
    assert st.map_output_pairs == 10 and st.pairs_sent == 10
    assert st.bytes_sent == sum(pair_size(w, 1) for _, t in docs for w in t.split()) == 31
    assert sum(st.reducer_pairs) == 10


def test_word_count_matches_counter_on_seeded_inputs():
    rng = random.Random(7)
    for trial in range(300):
        docs = random_docs(rng, rng.randrange(0, 12), rng.choice([1, 3, 20]))
        m, r = rng.randrange(1, 6), rng.randrange(1, 6)
        out, st = run_round(make_splits(docs, m), word_count_map, sum_reduce, r, rng=rng)
        want = Counter(w for _, t in docs for w in t.split())
        assert counts_of(out) == dict(want)
        tokens = sum(want.values())
        assert st.pairs_sent == st.map_output_pairs == tokens
        assert sum(st.reducer_pairs) == tokens
        assert st.max_reducer_pairs >= max(want.values(), default=0)


def test_empty_input_and_one_key():
    out, st = run_round(make_splits([], 3), word_count_map, sum_reduce, 4)
    assert counts_of(out) == {} and st.pairs_sent == 0 and st.max_reducer_pairs == 0
    out, st = run_round(make_splits([(i, "x x") for i in range(5)], 5), word_count_map, sum_reduce, 4)
    assert counts_of(out) == {"x": 10}
    assert st.max_reducer_pairs == 10 and sorted(st.reducer_pairs)[:3] == [0, 0, 0]


def test_each_key_goes_to_one_reducer_and_reducer_output_is_sorted():
    rng = random.Random(11)
    docs = random_docs(rng, 40, 30)
    out, st = run_round(make_splits(docs, 4), word_count_map, sum_reduce, 3, rng=rng)
    owner = {}
    for _, dst, k, _ in st.messages:
        assert owner.setdefault(k, dst) == dst == hash_partitioner(k, 3)
    for j, o in enumerate(out):
        keys = [k for k, _ in o]
        assert keys == sorted(keys)
        assert all(owner[k] == j for k in keys)


def test_map_only_round_sends_nothing():
    docs = [(1, "a b"), (2, "c")]
    out, st = run_round(make_splits(docs, 2), word_count_map, None, 0)
    assert out == [[("a", 1), ("b", 1)], [("c", 1)]]
    assert st.pairs_sent == 0 and st.reducers == 0


def test_two_round_job_counts_rounds():
    docs = [(1, "a b a"), (2, "b a c")]
    # Round 2 swaps (word, count) to (count, word) and groups words by count.
    stages = [dict(mapper=word_count_map, reducer=sum_reduce, r=2),
              dict(mapper=lambda w, c: [(c, w)], reducer=lambda c, ws: [(c, sorted(ws))], r=1)]
    out, stats = run_job(make_splits(docs, 2), stages)
    assert len(stats) == 2
    assert out == [[(1, ["c"]), (2, ["b"]), (3, ["a"])]]
    assert stats[1].pairs_sent == 3


def test_group_sorted_and_stable_hash():
    assert group_sorted([("b", 1), ("a", 2), ("b", 3)], lambda k: k, lambda k: k) == [("a", [2]), ("b", [1, 3])]
    assert stable_hash("the") == stable_hash("the")
    assert all(0 <= hash_partitioner(f"k{i}", 7) < 7 for i in range(100))


def test_replication_rate_of_word_count_is_one_pair_per_word():
    rng = random.Random(3)
    docs = random_docs(rng, 30, 10)
    _, st = run_round(make_splits(docs, 3), word_count_map, sum_reduce, 2)
    tokens = sum(len(t.split()) for _, t in docs)
    assert st.pairs_sent == tokens
