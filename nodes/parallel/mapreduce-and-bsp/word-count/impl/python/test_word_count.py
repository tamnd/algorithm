# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/word-count/. The authors are listed in prov/9P6PN4.jsonl.

import random
from collections import Counter

from word_count import (bytes_without_combiner, expected_distinct, in_mapper_combining, make_splits,
                        pairs_with_combiner, word_count, zipf_docs, zipf_probs)


def truth(docs):
    return dict(Counter(w for _, t in docs for w in t.split()))


def test_page_example():
    docs = [(1, "a rose is a rose"), (2, "is a rose"), (3, "a b")]
    counts, st = word_count(docs, 2, 2)
    assert counts == {"a": 4, "rose": 3, "is": 2, "b": 1}
    assert st.pairs_sent == 10 and st.bytes_sent == 31
    counts, st = word_count(docs, 2, 2, use_combiner=True)
    assert counts == {"a": 4, "rose": 3, "is": 2, "b": 1}
    assert st.pairs_sent == 7 and st.map_output_pairs == 10


def test_matches_counter_with_and_without_combiner():
    rng = random.Random(5)
    for _ in range(200):
        vocab = rng.choice([1, 2, 5, 50])
        docs = [(d, " ".join(f"w{rng.randrange(vocab)}" for _ in range(rng.randrange(15))))
                for d in range(rng.randrange(0, 10))]
        m, r = rng.randrange(1, 5), rng.randrange(1, 5)
        want = truth(docs)
        plain, s0 = word_count(docs, m, r, rng=rng)
        comb, s1 = word_count(docs, m, r, use_combiner=True, spill=rng.choice([None, 1, 3]),
                              merge_combine=rng.random() < 0.5, rng=rng)
        imc, s2 = in_mapper_combining(docs, m, r)
        assert plain == comb == imc == want
        assert s0.pairs_sent == sum(want.values())
        assert s0.bytes_sent == bytes_without_combiner(want)
        assert len(want) <= s2.pairs_sent == pairs_with_combiner(docs, m) <= s1.pairs_sent <= s0.pairs_sent


def test_empty_and_one_key():
    counts, st = word_count([], 3, 2, use_combiner=True)
    assert counts == {} and st.pairs_sent == 0
    docs = [(i, "x " * 7) for i in range(6)]
    counts, st = word_count(docs, 3, 4)
    assert counts == {"x": 42} and st.max_reducer_pairs == 42
    counts, st = word_count(docs, 3, 4, use_combiner=True)
    assert counts == {"x": 42} and st.pairs_sent == 3 and st.max_reducer_pairs == 3


def test_zipf_skew_and_combiner_bound():
    rng = random.Random(1)
    docs = zipf_docs(rng, 20, 1000, 1000, 1.0)
    want = truth(docs)
    counts, plain = word_count(docs, 10, 8)
    _, comb = word_count(docs, 10, 8, use_combiner=True)
    top = max(want.values())
    assert counts == want
    # Without a combiner the reducer of the most frequent word gets all of its pairs.
    assert plain.max_reducer_pairs >= top > 2 * plain.pairs_sent / 8 / 2
    # With a combiner each word sends at most one pair per map task.
    keys_per_message = Counter(k for _, _, k, _ in comb.messages)
    assert max(keys_per_message.values()) <= 10
    assert comb.pairs_sent == pairs_with_combiner(docs, 10)
    assert comb.max_reducer_pairs < plain.max_reducer_pairs / 4


def test_expected_distinct_matches_average():
    probs = zipf_probs(200, 1.0)
    rng = random.Random(2)
    trials, m, per_split = 30, 4, 300
    total = 0
    for _ in range(trials):
        docs = zipf_docs(rng, m, per_split, 200, 1.0)
        total += pairs_with_combiner(docs, m)
    mean = total / trials
    want = m * expected_distinct(per_split, probs)
    assert abs(mean - want) < 0.03 * want
