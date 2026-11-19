# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brown-clustering/. The authors are listed in prov/HG0BRB.jsonl.

import math
import random

from brown_clustering import (
    average_mutual_information,
    bigram_counts,
    bit_strings,
    brown_clustering,
    vocabulary,
)

EXAMPLE = ["the cat runs and the dog sleeps and a dog runs and the cat sleeps".split()]


def ami_of_partition(corpus: list[list[str]], partition: list[list[str]]) -> float:
    """AMI of a partition, from the word bigrams, with no shared code path."""
    cls = {w: c for c, ws in enumerate(partition) for w in ws}
    pairs = [(a, b) for s in corpus for a, b in zip(s, s[1:])]
    total = len(pairs)
    joint: dict[tuple[int, int], int] = {}
    left: dict[int, int] = {}
    right: dict[int, int] = {}
    for a, b in pairs:
        key = (cls[a], cls[b])
        joint[key] = joint.get(key, 0) + 1
        left[key[0]] = left.get(key[0], 0) + 1
        right[key[1]] = right.get(key[1], 0) + 1
    return sum(c / total * math.log(c * total / (left[l] * right[m])) for (l, m), c in joint.items())


def all_partitions(items: list[str], k: int):
    if not items:
        if k == 0:
            yield []
        return
    first, rest = items[0], items[1:]
    if k > 0:
        for p in all_partitions(rest, k - 1):
            yield [[first]] + p
    for p in all_partitions(rest, k):
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1:]


def check_greedy(corpus: list[list[str]]) -> None:
    """At every step the chosen merge must reach the best AMI over all pairs."""
    words = vocabulary(corpus)
    final, merges = brown_clustering(corpus, 1)
    assert len(merges) == max(len(words) - 1, 0)
    for step, merge in enumerate(merges):
        before, _ = brown_clustering(corpus, len(words) - step)
        after, _ = brown_clustering(corpus, len(words) - step - 1)
        best = max(
            ami_of_partition(corpus, [c for t, c in enumerate(before) if t not in (i, j)] + [before[i] + before[j]])
            for i in range(len(before))
            for j in range(i + 1, len(before))
        )
        got = ami_of_partition(corpus, after)
        assert abs(got - merge.ami) < 1e-9
        assert got > best - 1e-9


def test_example_trace() -> None:
    words = vocabulary(EXAMPLE)
    assert words == ["and", "the", "cat", "dog", "runs", "sleeps", "a"]
    n, total = bigram_counts(EXAMPLE, words)
    assert total == 14
    assert abs(average_mutual_information(n, total) - 1.4377014436) < 1e-9
    classes, merges = brown_clustering(EXAMPLE, 3)
    assert classes == [["and", "the", "a"], ["cat", "dog"], ["runs", "sleeps"]]
    assert [round(m.ami, 4) for m in merges] == [1.4377, 1.3761, 1.3761, 0.7375]
    assert [(m.left, m.right, m.node) for m in merges] == [(4, 5, 7), (1, 6, 8), (2, 3, 9), (0, 8, 10)]
    _, full = brown_clustering(EXAMPLE, 1)
    assert [round(m.ami, 4) for m in full[4:]] == [0.1175, 0.0]
    assert bit_strings(EXAMPLE) == {
        "and": "000", "the": "0010", "a": "0011", "runs": "010", "sleeps": "011", "cat": "10", "dog": "11",
    }


def test_greedy_choice_against_all_pairs() -> None:
    check_greedy(EXAMPLE)
    rng = random.Random(7)
    for _ in range(500):
        vocab = "abcdefg"[: rng.randrange(1, 8)]
        corpus = [[rng.choice(vocab) for _ in range(rng.randrange(1, 9))] for _ in range(rng.randrange(1, 3))]
        check_greedy(corpus)


def test_greedy_is_not_optimal() -> None:
    corpus = ["e a d b c a".split()]
    greedy, _ = brown_clustering(corpus, 2)
    best = max(all_partitions(vocabulary(corpus), 2), key=lambda p: ami_of_partition(corpus, p))
    assert abs(ami_of_partition(corpus, greedy) - 0.1185) < 1e-4
    assert abs(ami_of_partition(corpus, best) - 0.6730) < 1e-4
    assert sorted(sorted(c) for c in best) == [["a", "b"], ["c", "d", "e"]]


def test_edges() -> None:
    assert brown_clustering([], 1) == ([], [])
    assert bit_strings([]) == {}
    assert bit_strings([["x", "x"]]) == {"x": ""}
    classes, merges = brown_clustering([["a", "b"]], 5)
    assert classes == [["a"], ["b"]] and merges == []
    classes, merges = brown_clustering([["a"], ["b"], ["c"]], 1)
    assert sorted(classes[0]) == ["a", "b", "c"]
    assert all(m.ami == 0.0 for m in merges)
    try:
        brown_clustering(EXAMPLE, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("num_classes = 0 must fail")


def test_bit_strings_form_a_prefix_code() -> None:
    rng = random.Random(3)
    for _ in range(100):
        vocab = "abcdefgh"[: rng.randrange(2, 9)]
        corpus = [[rng.choice(vocab) for _ in range(rng.randrange(2, 10))] for _ in range(2)]
        codes = list(bit_strings(corpus).values())
        assert len(codes) == len(vocabulary(corpus))
        for x in codes:
            for y in codes:
                assert x == y or not y.startswith(x)
