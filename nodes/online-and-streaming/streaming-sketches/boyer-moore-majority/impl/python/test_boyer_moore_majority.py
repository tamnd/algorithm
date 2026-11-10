# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boyer-moore-majority/. The authors are listed in prov/FE4TJK.jsonl.

import itertools
import random
from collections import Counter

from boyer_moore_majority import majority, majority_candidate, merge_candidates


def oracle(items):
    if not items:
        return None
    item, c = Counter(items).most_common(1)[0]
    return item if 2 * c > len(items) else None


def test_example() -> None:
    s = list("abacaaba")
    assert majority_candidate(s) == ("a", 2)
    assert majority(s) == "a"


def test_no_majority_needs_second_pass() -> None:
    assert majority_candidate(list("abcabc")) == ("b", 0)
    assert majority(list("abcabc")) is None
    assert majority_candidate(list("aabbc")) == ("c", 1)
    assert majority(list("aabbc")) is None


def test_edges() -> None:
    assert majority_candidate([]) == (None, 0)
    assert majority([]) is None
    assert majority([7]) == 7
    assert majority([4, 4, 4, 4]) == 4
    assert majority([1, 2]) is None
    assert majority([1, 2, 1]) == 1
    assert majority([2, 1, 1, 2]) is None


def test_all_small_sequences() -> None:
    for n in range(0, 9):
        for seq in itertools.product(range(3), repeat=n):
            s = list(seq)
            want = oracle(s)
            cand, _ = majority_candidate(s)
            if want is not None:
                assert cand == want
            assert majority(s) == want


def test_pairing_invariant() -> None:
    # After each prefix, the prefix splits into `count` copies of the
    # candidate and pairs of distinct items: so each other item occurs at most
    # (len - count) / 2 times, and the candidate at least count times.
    rng = random.Random(7)
    for _ in range(500):
        s = [rng.randrange(4) for _ in range(rng.randrange(1, 20))]
        for t in range(1, len(s) + 1):
            cand, count = majority_candidate(s[:t])
            freq = Counter(s[:t])
            assert (t - count) % 2 == 0
            assert freq[cand] >= count
            pairs = (t - count) // 2
            for x, c in freq.items():
                in_pairs = c - count if x == cand else c
                assert 0 <= in_pairs <= pairs


def test_random_against_oracle() -> None:
    rng = random.Random(11)
    for _ in range(1000):
        n = rng.randrange(0, 40)
        k = rng.randrange(1, 5)
        s = [rng.randrange(k) for _ in range(n)]
        if n and rng.random() < 0.5:
            s += [0] * (n + 1)
            rng.shuffle(s)
        assert majority(s) == oracle(s)


def test_merge_matches_concatenation() -> None:
    rng = random.Random(5)
    for _ in range(2000):
        s1 = [rng.randrange(3) for _ in range(rng.randrange(0, 12))]
        s2 = [rng.randrange(3) for _ in range(rng.randrange(0, 12))]
        merged = merge_candidates(majority_candidate(s1), majority_candidate(s2))
        want = oracle(s1 + s2)
        if want is not None:
            assert merged[0] == want
        # The merged count has the parity of the total length and is at
        # least 2 f - m for the merged candidate, like a direct run.
        m = len(s1) + len(s2)
        assert (m - merged[1]) % 2 == 0
        if merged[1] > 0:
            f = sum(1 for x in s1 + s2 if x == merged[0])
            assert merged[1] >= 2 * f - m


def test_index_reduction() -> None:
    # INDEX: Alice holds x, Bob holds j. Alice streams the positions of the
    # ones of x, Bob appends a = |x| copies of j. A majority exists iff x_j = 1.
    for n in range(1, 7):
        for x in itertools.product((0, 1), repeat=n):
            ones = [i for i in range(n) if x[i] == 1]
            for j in range(n):
                stream = ones + [j] * len(ones)
                assert (majority(stream) is not None) == (x[j] == 1)
                if x[j] == 1:
                    assert majority(stream) == j
